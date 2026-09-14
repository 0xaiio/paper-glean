"""共享的「名单 → 抓取 → diff → 落盘 → 推送」引擎。

为什么需要这个模块
------------------
``watch``（按人）与 ``ccf``（按会议 / 期刊）在用户眼里是两个功能，在代码里却是
**同一套机制的两份拷贝**：都以 Markdown 做名单事实源，都按 ``fingerprint`` 与上次
状态 diff 出「新」条目，都在首次运行时静默建基线（``--force`` 例外），都落盘一份带
幂等标记的 Markdown digest，都经 ``notify`` 多通道推送并追加审计事件。

两份拷贝的差别只有三处：**抓什么**、**每条的主语叫什么**（``researcher`` / ``venue``）、
**写到哪个文件**。把这三点留成参数，其余共性收敛成一份实现——否则修一次 diff、基线
或推送的缺陷要改两处，而两处迟早会漂移。

职责边界
--------
本模块**不做任何网络请求**：抓取函数由调用方通过 :class:`MonitorJob` 注入，因此它可以
在无网络、无仓库文件的情况下被完整测试。

术语
----
``spec.subject_field``  新条目挂在谁名下（``researcher`` / ``venue``）——推送摘要分组、
                        事件日志、digest 小标题都用它。
``spec.state_key``      状态 JSON 的顶层键，形如 ``{"version": 1, "<state_key>": {...}}``。
``spec.digest_marker``  digest 幂等标记，形如 ``<!-- BEGIN <marker> <day> -->``。
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from glean import notify

# ------------------------------------------------------------------
# 身份与分类基元（watch / ccf 共用）
# ------------------------------------------------------------------

_SLUG_STRIP_RE = re.compile(r"[^0-9a-z\u4e00-\u9fff]+")
_NORM_TITLE_RE = re.compile(r"[^a-z0-9]+")


def slugify(name: str) -> str:
    """把名字折成稳定 key：小写、保留中日韩字符、其余折成连字符。

    兜底值刻意保持为 ``"researcher"``（而不是更中性的 ``"entry"``）：它是既有状态
    文件里的历史取值，换掉会让全部单调空名字的条目在下次运行时被判定成「新主体」。
    """
    s = name.strip().lower()
    s = _SLUG_STRIP_RE.sub("-", s)
    return s.strip("-") or "researcher"


def norm_title(title: str) -> str:
    """标题归一化：只保留字母数字、转小写、截断 100 字符。"""
    return _NORM_TITLE_RE.sub("", (title or "").lower())[:100]


def fingerprint(item: dict[str, Any]) -> str:
    """条目的稳定身份，决定什么算「新」。

    标题承载身份；URL 只在是真链接时参与，用来区分「同名但不同宿主」的
    preprint / published 版本。
    """
    basis = norm_title(item.get("title", ""))
    url = (item.get("url") or "").split("?")[0].rstrip("/").lower()
    if url and not url.startswith(("http://www.", "https://www.")):
        basis = basis + "|" + hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def kind_of(value: str | None, allowed: tuple[str, ...]) -> str:
    """把来源自由填写的 kind 钳到该子系统允许的取值，未知一律 ``other``。"""
    v = (value or "").strip().lower()
    return v if v in allowed else "other"


def year_of(value: Any) -> int | None:
    """从任意脏值里取一个合理的年份；取不到返回 ``None``。"""
    try:
        y = int(str(value).strip()[:4])
    except (TypeError, ValueError):
        return None
    return y if 1900 <= y <= 2100 else None


# ------------------------------------------------------------------
# 任务描述
# ------------------------------------------------------------------


@dataclass(frozen=True)
class MonitorSpec:
    """一个监控子系统的**静态身份**：决定写到哪、主语叫什么、文案怎么说。

    Attributes:
        namespace: ``notify`` 命名空间（``watch`` / ``ccf``），决定未读集合互不干扰。
        subject_field: 条目主语字段名（``researcher`` / ``venue``）。
        state_key: 状态 JSON 顶层键（``researchers`` / ``venues``）。
        digest_marker: digest 幂等标记（``WATCH`` / ``CCF``）。
        item_noun: 条目中文量词（``新作`` / ``更新``），用于 digest 文案。
        max_items: 每个主语保留的指纹上限，防止状态文件无界增长。
    """

    namespace: str
    subject_field: str
    state_key: str
    digest_marker: str
    item_noun: str
    max_items: int


@dataclass(frozen=True)
class MonitorJob:
    """把「一份名单」接到引擎上所需的一切。

    注入点全部在**调用时**才解析，所以测试可以 monkeypatch 名字。

    Attributes:
        spec: 子系统的静态身份。
        entries: 读取名单（``load_watchlist`` / ``load_venues``）。
        state_path: 已见指纹状态文件。
        events_path: append-only 审计日志。
        digest_path: 人类可读的 Markdown digest。
        digest_header: digest 首次创建时的文件头。
        render_item: 单条条目 → digest 里的一行 Markdown。
        collect: 把名单条目变成候选条目；签名 ``(entry, use_network, context)``。
        prepare: 循环前的一次性准备（ccf 用它把 ccfddl RSS 只下载一次），
            返回 ``(errors, context)``，``context`` 会原样传给 ``collect``。
        accept: 采集后的清洗钩子（watch 用它按年份砍掉过老的主页条目）。
    """

    spec: MonitorSpec
    entries: Callable[[], list[dict[str, Any]]]
    state_path: Path
    events_path: Path
    digest_path: Path
    digest_header: str
    render_item: Callable[[dict[str, Any]], str]
    collect: Callable[[dict[str, Any], bool, Any], list[dict[str, Any]]]
    prepare: Callable[[], tuple[list[str], Any]] | None = None
    accept: Callable[[dict[str, Any], list[dict[str, Any]]], list[dict[str, Any]]] | None = None


# ------------------------------------------------------------------
# 状态（已见指纹）
# ------------------------------------------------------------------


def load_state(path: Path, state_key: str) -> dict[str, Any]:
    """读取状态文件；缺失或损坏时返回空壳，**绝不抛异常**。"""
    blank: dict[str, Any] = {"version": 1, state_key: {}}
    if not path.exists():
        return blank
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return blank


def save_state(path: Path, state: dict[str, Any]) -> None:
    """写回状态文件（缩进 2 空格 + 结尾换行，便于 git diff 与人工审阅）。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


# ------------------------------------------------------------------
# 审计事件（append-only JSONL）
# ------------------------------------------------------------------


def append_events(
    path: Path,
    items: list[dict[str, Any]],
    pushed_to: list[str],
    run_id: str,
    subject_field: str,
) -> None:
    """每个新条目追加一行 JSON 审计记录。"""
    if not items:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    with open(path, "a", encoding="utf-8") as fh:
        for it in items:
            fh.write(
                json.dumps(
                    {
                        "time": now,
                        "run_id": run_id,
                        "key": it.get("key"),
                        subject_field: it.get(subject_field),
                        "item": {
                            k: v
                            for k, v in it.items()
                            if k not in ("key", subject_field)
                        },
                        "pushed_to": pushed_to,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )


def load_events(path: Path, limit: int = 200) -> list[dict[str, Any]]:
    """最近的审计事件，最新在前；坏行跳过而不是整份失败。"""
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    for line in reversed(path.read_text(encoding="utf-8").splitlines()[-limit:]):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


# ------------------------------------------------------------------
# digest（幂等分节）
# ------------------------------------------------------------------


def render_section(
    spec: MonitorSpec,
    day: str,
    grouped: dict[str, list[dict[str, Any]]],
    render_item: Callable[[dict[str, Any]], str],
) -> str:
    """渲染单日 digest 章节，用幂等标记 ``<!-- BEGIN/END <marker> <day> -->`` 包住。"""
    lines = [f"<!-- BEGIN {spec.digest_marker} {day} -->", "", f"## {day}", ""]
    if not grouped:
        lines += [f"_本次运行没有发现{spec.item_noun}。_", ""]
    for name, items in grouped.items():
        lines.append(f"### {name}　`{len(items)} 条{spec.item_noun}`")
        lines.append("")
        lines.extend("- " + render_item(i) for i in items)
        lines.append("")
    lines.append(f"<!-- END {spec.digest_marker} {day} -->")
    return "\n".join(lines)


def upsert_digest(
    path: Path,
    header: str,
    marker: str,
    day: str,
    section: str,
) -> None:
    """插入 / 替换该日章节，最新在前（与 :func:`glean.core.upsert_digest` 同一约定）。"""
    content = path.read_text(encoding="utf-8") if path.exists() else header
    begin, endm = f"<!-- BEGIN {marker} {day} -->", f"<!-- END {marker} {day} -->"
    if begin in content and endm in content:
        pre = content[: content.index(begin)]
        post = content[content.index(endm) + len(endm) :].lstrip("\n")
        content = pre + section + "\n" + post
    elif f"<!-- BEGIN {marker} " in content:
        idx = content.index(f"<!-- BEGIN {marker} ")
        content = content[:idx] + section + "\n" + content[idx:]
    else:
        # 结尾换行是必须的：否则「首次写入」与「之后每次写入」结果不同，
        # 幂等 upsert 就不再幂等。
        content = content.rstrip("\n") + "\n\n" + section + "\n"
    path.write_text(content, encoding="utf-8")


# ------------------------------------------------------------------
# 运行
# ------------------------------------------------------------------


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _baseline_record(name: str, items: list[dict[str, Any]], max_items: int) -> dict[str, Any]:
    """首次见到某主语时写入的基线记录：只记指纹，不推送历史。"""
    return {
        "name": name,
        "baseline": True,
        "last_checked": _now(),
        "fingerprints": [it["fingerprint"] for it in items][-max_items:],
        "sources": sorted({it.get("source", "?") for it in items}),
    }


def _advance_record(rec: dict[str, Any], fresh: list[dict[str, Any]], max_items: int) -> None:
    """就地把本次新增指纹与来源并进已有记录（指纹列表截尾保留）。"""
    rec["last_checked"] = _now()
    rec["fingerprints"] = (
        rec.get("fingerprints", []) + [it["fingerprint"] for it in fresh]
    )[-max_items:]
    rec["sources"] = sorted(
        set(rec.get("sources", [])) | {it.get("source", "?") for it in fresh}
    )


def run_monitor(
    job: MonitorJob,
    *,
    only: str | None = None,
    use_network: bool = True,
    force: bool = False,
    push: bool = True,
    delay: float | None = None,
) -> dict[str, Any]:
    """扫描名单，返回本次新发现的条目。

    语义（与历史行为逐条对齐，watch / ccf 完全一致）：

    * 只有 ``enabled`` 的条目会被扫描；``only`` 按 key 收窄到单个条目。
    * **首次见到某条目时只建基线、不推送**（``force=True`` 例外）——否则一上线就是
      一整份历史书目。
    * 单个条目抛异常只记进 ``errors``，不影响同轮其余条目。
    * 有新条目才推送；无论有无新条目都会落盘一份当日 digest。
    * 审计事件在推送**之后**写，才能记录每条最终落到了哪些通道。

    返回 ``{"run_id", "day", "new_items", "grouped", "baselined", "skipped",
    "errors", "pushed_to"}``。
    """
    spec = job.spec
    state = load_state(job.state_path, spec.state_key)
    subjects: dict[str, Any] = state.setdefault(spec.state_key, {})

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    day = datetime.now().strftime("%Y-%m-%d")

    new_items: list[dict[str, Any]] = []
    grouped: dict[str, list[dict[str, Any]]] = {}
    baselined: list[str] = []
    skipped: list[str] = []
    errors: list[str] = []

    context: Any = None
    if use_network and job.prepare is not None:
        pre_errors, context = job.prepare()
        errors.extend(pre_errors)

    entries = [e for e in job.entries() if e.get("enabled", True)]
    if only:
        wanted = slugify(only)
        entries = [e for e in entries if e["key"] == wanted]

    for i, entry in enumerate(entries):
        if i and delay:
            time.sleep(delay)
        key = entry["key"]
        try:
            items = job.collect(entry, use_network, context)
        except Exception as exc:  # 一个坏源不该拖垮整轮
            errors.append(f"{entry['name']}: {type(exc).__name__}: {exc}")
            continue

        for it in items:
            it["fingerprint"] = fingerprint(it)
        if job.accept is not None:
            items = job.accept(entry, items)

        rec = subjects.get(key)
        if rec is None:
            subjects[key] = _baseline_record(entry["name"], items, spec.max_items)
            baselined.append(f"{entry['name']}（{len(items)} 条基线）")
            fresh = items if force else []
        else:
            seen = set(rec.get("fingerprints", []))
            fresh = [it for it in items if it["fingerprint"] not in seen]
            _advance_record(rec, fresh, spec.max_items)
            if not fresh:
                skipped.append(entry["name"])

        for it in fresh:
            enriched = dict(it)
            enriched["key"] = key
            enriched[spec.subject_field] = entry["name"]
            new_items.append(enriched)
        if fresh:
            grouped.setdefault(entry["name"], []).extend(fresh)

    save_state(job.state_path, state)

    pushed_to: list[str] = []
    if new_items:
        upsert_digest(
            job.digest_path,
            job.digest_header,
            spec.digest_marker,
            day,
            render_section(spec, day, grouped, job.render_item),
        )
        if push:
            try:
                pushed_to = notify.push(new_items, day=day, namespace=spec.namespace) or []
            except Exception as exc:
                errors.append(f"push: {type(exc).__name__}: {exc}")
        append_events(job.events_path, new_items, pushed_to, run_id, spec.subject_field)
    else:
        upsert_digest(
            job.digest_path,
            job.digest_header,
            spec.digest_marker,
            day,
            render_section(spec, day, {}, job.render_item),
        )

    return {
        "run_id": run_id,
        "day": day,
        "new_items": new_items,
        "grouped": grouped,
        "baselined": baselined,
        "skipped": skipped,
        "errors": errors,
        "pushed_to": pushed_to,
    }
