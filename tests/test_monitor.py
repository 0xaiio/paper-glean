"""Tests for :mod:`glean.monitor` — the engine shared by the two monitors.

The engine performs no network I/O by design, so everything here runs offline
and never touches the real repository files (paths go to ``tmp_path``).
"""

from __future__ import annotations

import json

import pytest

from glean import monitor


# ------------------------------------------------------------------
# identity primitives
# ------------------------------------------------------------------

def test_slugify_keeps_cjk_and_folds_punctuation():
    assert monitor.slugify("魏恒峰 Hengfeng Wei") == "魏恒峰-hengfeng-wei"
    assert monitor.slugify("  A.  Gotsman!! ") == "a-gotsman"


def test_slugify_falls_back_for_punctuation_only():
    """A degenerate name must still yield a usable, stable key."""
    assert monitor.slugify("!!!") == "researcher"
    assert monitor.slugify("   ") == "researcher"


def test_norm_title_is_alnum_lowercase_and_bounded():
    assert monitor.norm_title("VeriStrong: A Verified Protocol!") == "veristrongaverifiedprotocol"
    assert len(monitor.norm_title("x" * 500)) == 100


def test_fingerprint_is_stable_and_host_sensitive():
    a = {"title": "VeriStrong: A Verified Protocol", "url": "https://x/a.pdf"}
    b = {"title": "veristrong: a verified protocol", "url": "https://x/b.pdf"}
    assert monitor.fingerprint(a) == monitor.fingerprint(a)
    assert monitor.fingerprint(a) != monitor.fingerprint(b)
    assert monitor.fingerprint({"title": "Totally Other"}) != monitor.fingerprint(a)


def test_kind_of_clamps_unknown_values():
    allowed = ("paper", "video")
    assert monitor.kind_of("paper", allowed) == "paper"
    assert monitor.kind_of("  VIDEO ", allowed) == "video"
    assert monitor.kind_of("podcast", allowed) == "other"
    assert monitor.kind_of(None, allowed) == "other"


def test_year_of_rejects_nonsense():
    assert monitor.year_of("2026") == 2026
    assert monitor.year_of("2026-09-14") == 2026
    assert monitor.year_of("1234") is None
    assert monitor.year_of("n/a") is None
    assert monitor.year_of(None) is None


# ------------------------------------------------------------------
# state
# ------------------------------------------------------------------

def test_load_state_tolerates_missing_and_corrupt(tmp_path):
    path = tmp_path / "state.json"
    assert monitor.load_state(path, "researchers") == {"version": 1, "researchers": {}}

    path.write_text("{not json", encoding="utf-8")
    assert monitor.load_state(path, "researchers") == {"version": 1, "researchers": {}}


def test_save_state_creates_parent_dirs(tmp_path):
    path = tmp_path / "nested" / "state.json"
    monitor.save_state(path, {"version": 1, "researchers": {"a": {}}})
    assert json.loads(path.read_text(encoding="utf-8"))["researchers"] == {"a": {}}


# ------------------------------------------------------------------
# audit events
# ------------------------------------------------------------------

def test_append_events_hoists_the_subject_out_of_item(tmp_path):
    path = tmp_path / "events.jsonl"
    monitor.append_events(
        path,
        [{"key": "sigmod", "venue": "SIGMOD", "title": "CFP", "kind": "cfp"}],
        ["file"],
        "RUN1",
        "venue",
    )
    (event,) = monitor.load_events(path)
    assert event["venue"] == "SIGMOD"
    assert event["run_id"] == "RUN1"
    assert event["pushed_to"] == ["file"]
    # the subject lives at the top level, so it must not be duplicated inside
    assert "venue" not in event["item"]
    assert "key" not in event["item"]
    assert event["item"]["title"] == "CFP"


def test_append_events_noop_for_empty_input(tmp_path):
    path = tmp_path / "events.jsonl"
    monitor.append_events(path, [], ["file"], "RUN1", "researcher")
    assert not path.exists()


def test_load_events_skips_corrupt_lines_and_is_newest_first(tmp_path):
    path = tmp_path / "events.jsonl"
    path.write_text(
        '{"run_id": "A"}\nnot json\n\n{"run_id": "B"}\n', encoding="utf-8"
    )
    assert [e["run_id"] for e in monitor.load_events(path)] == ["B", "A"]


# ------------------------------------------------------------------
# digest
# ------------------------------------------------------------------

def _spec(**overrides) -> monitor.MonitorSpec:
    base = {
        "namespace": "watch",
        "subject_field": "researcher",
        "state_key": "researchers",
        "digest_marker": "WATCH",
        "item_noun": "新作",
        "max_items": 10,
    }
    return monitor.MonitorSpec(**{**base, **overrides})


def test_upsert_digest_is_idempotent_for_the_same_day(tmp_path):
    path = tmp_path / "digest.md"
    section = monitor.render_section(
        _spec(), "2026-09-14", {"A": [{"title": "T1"}]}, lambda i: i["title"]
    )
    monitor.upsert_digest(path, "# H\n\n", "WATCH", "2026-09-14", section)
    first = path.read_text(encoding="utf-8")
    monitor.upsert_digest(path, "# H\n\n", "WATCH", "2026-09-14", section)
    assert path.read_text(encoding="utf-8") == first
    assert first.count("<!-- BEGIN WATCH 2026-09-14 -->") == 1


def test_upsert_digest_puts_the_newest_day_first(tmp_path):
    path = tmp_path / "digest.md"
    for day in ("2026-09-14", "2026-09-15"):
        section = monitor.render_section(
            _spec(), day, {"A": [{"title": day}]}, lambda i: i["title"]
        )
        monitor.upsert_digest(path, "# H\n\n", "WATCH", day, section)
    text = path.read_text(encoding="utf-8")
    assert text.index("2026-09-15") < text.index("2026-09-14")


def test_render_section_says_nothing_was_found_when_empty():
    md = monitor.render_section(_spec(item_noun="更新"), "2026-09-14", {}, lambda i: "")
    assert "_本次运行没有发现更新。_" in md
    assert "<!-- BEGIN WATCH 2026-09-14 -->" in md


# ------------------------------------------------------------------
# run_monitor
# ------------------------------------------------------------------

ENTRIES = [
    {"name": "Alice", "key": "alice", "enabled": True},
    {"name": "Bob", "key": "bob", "enabled": False},
]


def _job(tmp_path, collect, saved=None, **overrides) -> monitor.MonitorJob:
    """Build a job over a fixed roster.

    ``saved`` 可选：传入一个 list 时，``save_entries`` 会把每次写回的名单快照
    append 进去，供「启停 / 移除」类断言使用。扫描流程本身不写名单，所以多数
    用例不需要它。
    """
    kwargs = {
        "spec": _spec(),
        "entries": lambda: ENTRIES,
        "save_entries": (
            (lambda entries: saved.append([dict(e) for e in entries]))
            if saved is not None
            else (lambda entries: None)
        ),
        "state_path": tmp_path / "state.json",
        "events_path": tmp_path / "events.jsonl",
        "digest_path": tmp_path / "digest.md",
        "digest_header": "# H\n\n",
        "render_item": lambda i: i["title"],
        "collect": collect,
    }
    return monitor.MonitorJob(**{**kwargs, **overrides})


def _fixed(titles):
    def collect(entry, use_network, context):
        return [{"title": t, "url": "", "source": "stub"} for t in titles]

    return collect


# ------------------------------------------------------------------
# 名单变更（启停 / 遗忘指纹）
#
# 这一段是 watch 与 ccf 的**共用**实现，所以在这里测一次即可覆盖两条线；
# 两侧各自的 `set_enabled` / `remove_*` 只是转发（见 test_watch / test_ccf）。
# ------------------------------------------------------------------


def _mutation_job(tmp_path, entries, saved):
    """A job over a caller-owned roster, so mutation tests can't leak state.

    ``ENTRIES``（上面那个共享名单）不能用于本组用例：`set_enabled_where` 会
    **就地**改名单，用它会污染其它用例。
    """
    return monitor.MonitorJob(
        spec=_spec(),
        entries=lambda: entries,
        save_entries=lambda es: saved.append([dict(e) for e in es]),
        state_path=tmp_path / "state.json",
        events_path=tmp_path / "events.jsonl",
        digest_path=tmp_path / "digest.md",
        digest_header="# H\n\n",
        render_item=lambda i: i["title"],
        collect=lambda entry, use_network, _ctx: [],
    )


def test_set_enabled_toggles_one_and_leaves_the_rest_alone(tmp_path):
    entries = [
        {"name": "Alice", "key": "alice", "enabled": True},
        {"name": "Bob", "key": "bob", "enabled": False},
    ]
    saved: list[list[dict[str, object]]] = []
    job = _mutation_job(tmp_path, entries, saved)

    assert monitor.set_enabled(job, "Bob", True) is True
    assert saved[-1][0]["enabled"] is True  # Alice 不受影响
    assert saved[-1][1]["enabled"] is True


def test_set_enabled_is_false_for_unknown_name_and_writes_nothing(tmp_path):
    entries = [{"name": "Alice", "key": "alice", "enabled": True}]
    saved: list[list[dict[str, object]]] = []
    job = _mutation_job(tmp_path, entries, saved)

    assert monitor.set_enabled(job, "Nobody", True) is False
    assert saved == []  # 没命中就不写盘，避免无意义的 mtime 变化


def test_set_enabled_where_is_bulk_and_reports_touched(tmp_path):
    entries = [
        {"name": "Alice", "key": "alice", "area": "数据库", "enabled": True},
        {"name": "Bob", "key": "bob", "area": "理论", "enabled": True},
        {"name": "Carol", "key": "carol", "area": "数据库", "enabled": True},
    ]
    saved: list[list[dict[str, object]]] = []
    job = _mutation_job(tmp_path, entries, saved)

    touched = monitor.set_enabled_where(
        job, lambda e: "数据库" in e.get("area", ""), False
    )
    assert touched == ["Alice", "Carol"]
    assert [e["enabled"] for e in saved[-1]] == [False, True, False]


def test_forget_state_removes_seen_fingerprints(tmp_path):
    """移除名单条目后必须连指纹一起删，否则重新加入时会「全都见过」而永不推送。"""
    entries = [{"name": "Alice", "key": "alice", "enabled": True}]
    saved: list[list[dict[str, object]]] = []
    job = _mutation_job(tmp_path, entries, saved)
    monitor.save_state(
        job.state_path, {"version": 1, "researchers": {"alice": {"fingerprints": ["abc"]}}}
    )

    assert monitor.forget_state(job, "alice") is True
    assert "alice" not in monitor.load_state(job.state_path, "researchers")["researchers"]
    # 幂等：状态里本来就没记录时也不会报错（移除名单条目时无法保证一定有）
    assert monitor.forget_state(job, "alice") is False


def test_each_subsystem_wires_its_own_request_interval_into_the_job():
    """节流值挂在 job 上，两个子系统就不必各写一遍「取配置 or 取入参」的样板。"""
    from glean import ccf, watch
    from glean.config import CCF_REQUEST_INTERVAL, WATCH_REQUEST_INTERVAL

    assert watch._job().request_interval == WATCH_REQUEST_INTERVAL
    assert ccf._job().request_interval == CCF_REQUEST_INTERVAL


def test_run_monitor_prefers_an_explicit_delay_over_the_job_default(tmp_path):
    """显式入参优先——`run(..., request_interval=0)` 必须能关掉节流。"""
    job = _job(tmp_path, _fixed(["P1"]), request_interval=99.0)
    result = monitor.run_monitor(job, push=False, delay=0)
    assert result["baselined"] == ["Alice（1 条基线）"]


# ------------------------------------------------------------------
# 共享词表：同一 kind 不得在不同界面出现两种说法
# ------------------------------------------------------------------


def test_kind_vocabulary_has_one_source_of_truth():
    """`program` 曾漂移成「会议日程」(digest) / 「会议日程 (Program)」(推送)。"""
    from glean import ccf, kinds, notify, watch

    assert watch.KIND_LABELS is kinds.WATCH_KIND_LABELS
    assert ccf.KIND_LABELS is kinds.CCF_KIND_LABELS
    # 推送文案用的是合并视图，必须与子系统自身的说法逐字一致
    assert notify._KIND_LABEL is kinds.KIND_LABELS
    for key, label in ccf.KIND_LABELS.items():
        assert kinds.KIND_LABELS[key] == label


def test_first_run_baselines_silently_then_reports_only_the_delta(tmp_path):
    job = _job(tmp_path, _fixed(["P1", "P2"]))
    first = monitor.run_monitor(job, push=False)
    assert first["new_items"] == []
    assert first["baselined"] == ["Alice（2 条基线）"]
    assert first["baselined"] and "bob" not in job.state_path.read_text(encoding="utf-8")

    job2 = _job(tmp_path, _fixed(["P1", "P2", "P3"]))
    second = monitor.run_monitor(job2, push=False)
    assert [i["title"] for i in second["new_items"]] == ["P3"]
    assert second["grouped"] == {"Alice": second["grouped"]["Alice"]}
    assert second["new_items"][0]["researcher"] == "Alice"


def test_force_pushes_the_whole_first_sighting(tmp_path):
    job = _job(tmp_path, _fixed(["P1", "P2"]))
    res = monitor.run_monitor(job, force=True, push=False)
    assert [i["title"] for i in res["new_items"]] == ["P1", "P2"]
    assert res["baselined"] == ["Alice（2 条基线）"]


def test_one_broken_entry_does_not_abort_the_run(tmp_path):
    def collect(entry, use_network, context):
        if entry["key"] == "alice":
            raise RuntimeError("boom")
        return []

    entries = [
        {"name": "Alice", "key": "alice", "enabled": True},
        {"name": "Carol", "key": "carol", "enabled": True},
    ]
    job = _job(tmp_path, collect, entries=lambda: entries)
    res = monitor.run_monitor(job, push=False)
    assert any("boom" in e for e in res["errors"])
    assert res["baselined"] == ["Carol（0 条基线）"]


def test_prepare_errors_are_collected_and_context_reaches_collect(tmp_path):
    seen = {}

    def prepare():
        return ["ccfddl: TimeoutError: slow"], "CTX"

    def collect(entry, use_network, context):
        seen["context"] = context
        return []

    job = _job(tmp_path, collect, prepare=prepare)
    res = monitor.run_monitor(job, push=False)
    assert res["errors"] == ["ccfddl: TimeoutError: slow"]
    assert seen["context"] == "CTX"


def test_accept_hook_filters_collected_items(tmp_path):
    def accept(entry, items):
        return [i for i in items if i["title"] != "P2"]

    job = _job(tmp_path, _fixed(["P1", "P2"]), accept=accept)
    res = monitor.run_monitor(job, force=True, push=False)
    assert [i["title"] for i in res["new_items"]] == ["P1"]


def test_empty_run_still_writes_a_digest_section(tmp_path):
    job = _job(tmp_path, _fixed([]))
    monitor.run_monitor(job, push=False)
    assert "_本次运行没有发现新作。_" in job.digest_path.read_text(encoding="utf-8")


def test_push_failure_is_recorded_not_raised(tmp_path, monkeypatch):
    def boom(*args, **kwargs):
        raise OSError("no channel")

    monkeypatch.setattr(monitor.notify, "push", boom)
    job = _job(tmp_path, _fixed(["P1"]))
    res = monitor.run_monitor(job, force=True)
    assert any(e.startswith("push: OSError") for e in res["errors"])
    # the audit trail is still written, so the run stays reproducible
    assert len(monitor.load_events(job.events_path)) == 1


def test_unknown_only_name_scans_nothing_without_touching_state(tmp_path):
    """`only` matching nothing must not seed a baseline for anything else."""
    job = _job(tmp_path, _fixed(["P1"]))
    res = monitor.run_monitor(job, only="ghost", push=False)
    assert res["new_items"] == [] and res["baselined"] == []
    assert "alice" not in job.state_path.read_text(encoding="utf-8")


@pytest.mark.parametrize("use_network", [False, True])
def test_collect_receives_the_network_flag(tmp_path, use_network):
    seen = {}

    def collect(entry, net, context):
        seen["net"] = net
        return []

    job = _job(tmp_path, collect)
    monitor.run_monitor(job, use_network=use_network, push=False)
    assert seen["net"] is use_network
