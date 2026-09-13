"""Tests for :mod:`glean.watch` — list management, source resolution, diffing.

No network and no touching of the real repo files: every path constant is
redirected into ``tmp_path``, and ``collect_items`` is stubbed.
"""

from __future__ import annotations

import pytest

from glean import watch

SAMPLE = """# 学者监控名单

## 监控中

### 魏恒峰 Hengfeng Wei
- homepage: https://hengxin.github.io
- tags: 分布式; 形式化
- enabled: true
- 备注: 南京大学

### Alexey Gotsman
- homepage: https://software.imdea.org/~gotsman/
- s2: 12345
- enabled: true

## 已暂停

### Hagit Attiya
- homepage: https://hagit.net.technion.ac.il
- enabled: false
"""


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    """Redirect every watch path into tmp_path and seed a sample list."""
    wl = tmp_path / "watchlist.md"
    wl.write_text(SAMPLE, encoding="utf-8")
    monkeypatch.setattr(watch, "WATCHLIST_MD", wl)
    monkeypatch.setattr(watch, "WATCH_STATE", tmp_path / "data" / "watch_state.json")
    monkeypatch.setattr(watch, "WATCH_EVENTS", tmp_path / "watch_events.jsonl")
    monkeypatch.setattr(watch, "WATCH_DIGEST_MD", tmp_path / "WATCH-digest.md")
    return tmp_path


# ------------------------------------------------------------------
# basics
# ------------------------------------------------------------------

def test_slugify():
    assert watch.slugify("魏恒峰 Hengfeng Wei") == "魏恒峰-hengfeng-wei"
    assert watch.slugify("  A.  Gotsman!! ") == "a-gotsman"


def test_fingerprint_stable_and_distinct():
    a = {"title": "VeriStrong: A Verified Protocol", "url": "https://x/a.pdf"}
    b = {"title": "veristrong: a verified protocol", "url": "https://x/b.pdf"}
    assert watch.fingerprint(a) == watch.fingerprint(a)
    # same title but a materially different host -> different identity
    assert watch.fingerprint(a) != watch.fingerprint(b)
    assert watch.fingerprint({"title": "Totally Other"}) != watch.fingerprint(a)


def test_load_watchlist_parses_sections(isolated):
    entries = watch.load_watchlist()
    assert [e["name"] for e in entries] == [
        "魏恒峰 Hengfeng Wei",
        "Alexey Gotsman",
        "Hagit Attiya",
    ]
    assert entries[0]["enabled"] is True
    assert entries[0]["tags"] == ["分布式", "形式化"]
    assert entries[1]["s2"] == "12345"
    assert entries[2]["enabled"] is False
    assert "南京大学" in entries[0]["note"]


# ------------------------------------------------------------------
# mutation
# ------------------------------------------------------------------

def test_add_then_remove_roundtrip(isolated):
    watch.add_researcher("New Person", homepage="https://new.edu", tags=["a", "b"])
    entries = watch.load_watchlist()
    assert any(e["key"] == "new-person" for e in entries)

    with pytest.raises(ValueError):
        watch.add_researcher("New Person")

    assert watch.remove_researcher("New Person") is True
    assert watch.remove_researcher("New Person") is False
    assert len(watch.load_watchlist()) == 3


def test_set_enabled_moves_between_sections(isolated):
    assert watch.set_enabled("Hagit Attiya", True) is True
    text = watch.WATCHLIST_MD.read_text(encoding="utf-8")
    # entry must now sit under 监控中 with enabled: true
    active, paused = text.split("## 已暂停")
    assert "Hagit Attiya" in active
    assert "Hagit Attiya" not in paused
    assert watch.load_watchlist()[2]["enabled"] is True

    assert watch.set_enabled("Nonexistent Person", False) is False


def test_remove_forgets_seen_state(isolated):
    watch.add_researcher("Temp Person")
    state = watch.load_state()
    state.setdefault("researchers", {})["temp-person"] = {"fingerprints": ["x"]}
    watch.save_state(state)

    watch.remove_researcher("Temp Person")
    assert "temp-person" not in watch.load_state()["researchers"]


# ------------------------------------------------------------------
# source resolution
# ------------------------------------------------------------------

def _items(prefix: str, n: int):
    return [
        {"title": f"{prefix} {i}", "url": f"https://x/{prefix}{i}", "kind": "paper",
         "year": 2026, "source": prefix}
        for i in range(n)
    ]


def test_collect_prefers_homepage_and_merges_configured_fallbacks(monkeypatch):
    monkeypatch.setattr(watch, "parse_homepage", lambda url: _items("home", 2))
    monkeypatch.setattr(watch, "fetch_dblp", lambda v: _items("dblp", 2))
    monkeypatch.setattr(watch, "fetch_s2", lambda v: _items("s2", 1))

    got = watch.collect_items({"homepage": "https://h", "dblp": "pid/1", "s2": "9"})
    assert [i["source"] for i in got] == ["home", "home", "dblp", "dblp", "s2"]


def test_collect_falls_back_when_homepage_yields_nothing(monkeypatch):
    monkeypatch.setattr(watch, "parse_homepage", lambda url: [])
    monkeypatch.setattr(watch, "fetch_dblp", lambda v: _items("dblp", 3))
    monkeypatch.setattr(watch, "fetch_s2", lambda v: [])

    got = watch.collect_items({"homepage": "https://h", "dblp": "Name"})
    assert len(got) == 3
    assert {i["source"] for i in got} == {"dblp"}


def test_collect_dedups_by_title_across_sources(monkeypatch):
    monkeypatch.setattr(
        watch, "parse_homepage", lambda url: [{"title": "Same Paper", "url": "u", "kind": "paper"}]
    )
    monkeypatch.setattr(
        watch, "fetch_dblp", lambda v: [{"title": "Same Paper", "url": "u2", "kind": "paper"}]
    )
    monkeypatch.setattr(watch, "fetch_s2", lambda v: [])
    got = watch.collect_items({"homepage": "h", "dblp": "x"})
    assert len(got) == 1


def test_collect_offline_returns_nothing():
    assert watch.collect_items({"homepage": "https://h"}, use_network=False) == []


# ------------------------------------------------------------------
# run: baseline then diff
# ------------------------------------------------------------------

def test_run_seeds_baseline_without_pushing(isolated, monkeypatch):
    monkeypatch.setattr(watch, "collect_items", lambda e, **kw: _items("home", 5))

    res = watch.run(push=False)
    assert len(res["new_items"]) == 0  # first run seeds, never spams
    # 2 of the 3 sample entries are enabled; the paused one is not scanned
    assert len(res["baselined"]) == 2
    assert res["grouped"] == {}
    assert watch.load_state()["researchers"]["alexey-gotsman"]["baseline"] is True

    # second run: identical items -> nothing new
    res2 = watch.run(push=False)
    assert res2["new_items"] == []
    assert len(res2["skipped"]) == 2


def test_paused_researchers_are_never_scanned(isolated, monkeypatch):
    seen = []

    def spy(entry, **kw):
        seen.append(entry["name"])
        return []

    monkeypatch.setattr(watch, "collect_items", spy)
    watch.run(push=False)
    assert seen == ["魏恒峰 Hengfeng Wei", "Alexey Gotsman"]
    assert "hagit-attiya" not in watch.load_state()["researchers"]


def test_run_detects_only_unseen_items(isolated, monkeypatch):
    monkeypatch.setattr(watch, "collect_items", lambda e, **kw: _items("home", 5))
    watch.run(push=False)

    # one extra work appears
    monkeypatch.setattr(watch, "collect_items", lambda e, **kw: _items("home", 5) + [
        {"title": "Brand New Work", "url": "https://x/new", "kind": "video", "source": "homepage"}
    ])
    res = watch.run(push=False)
    titles = [i["title"] for i in res["new_items"]]
    assert titles.count("Brand New Work") == 2  # one per *enabled* researcher
    assert res["grouped"]
    assert watch.WATCH_DIGEST_MD.exists()
    assert "Brand New Work" in watch.WATCH_DIGEST_MD.read_text(encoding="utf-8")


def test_run_force_pushes_on_first_sighting(isolated, monkeypatch):
    monkeypatch.setattr(watch, "collect_items", lambda e, **kw: _items("home", 2))
    res = watch.run(force=True, push=False)
    assert len(res["new_items"]) == 4  # 2 items x 2 enabled researchers


def test_run_only_filters_to_one(isolated, monkeypatch):
    monkeypatch.setattr(watch, "collect_items", lambda e, **kw: _items("home", 1))
    res = watch.run(only="Alexey Gotsman", push=False)
    state = watch.load_state()["researchers"]
    assert list(state) == ["alexey-gotsman"]
    assert res["baselined"]


def test_run_only_unknown_name_scans_nothing(isolated, monkeypatch):
    monkeypatch.setattr(watch, "collect_items", lambda e, **kw: _items("home", 1))
    res = watch.run(only="Nobody At All", push=False)
    assert res["baselined"] == [] and res["new_items"] == []
    assert watch.load_state()["researchers"] == {}


def test_run_survives_one_broken_researcher(isolated, monkeypatch):
    def flaky(entry, **kw):
        if entry["name"].startswith("Alexey"):
            raise RuntimeError("boom")
        return _items("home", 1)

    monkeypatch.setattr(watch, "collect_items", flaky)
    res = watch.run(push=False)
    assert any("boom" in e for e in res["errors"])
    # Alexey blew up, the paused entry was not scanned, so only one is seeded
    assert list(watch.load_state()["researchers"]) == ["魏恒峰-hengfeng-wei"]


def test_events_are_logged_once_per_item(isolated, monkeypatch):
    monkeypatch.setattr(watch, "collect_items", lambda e, **kw: _items("home", 1))
    watch.run(push=False)
    monkeypatch.setattr(watch, "collect_items", lambda e, **kw: _items("home", 2))
    watch.run(push=False)
    events = watch.load_events()
    assert len(events) == 2  # 1 extra x 2 enabled researchers
    assert all("researcher" in e and "item" in e for e in events)


# ------------------------------------------------------------------
# digest
# ------------------------------------------------------------------

def test_digest_upsert_is_idempotent(tmp_path, monkeypatch):
    target = tmp_path / "d.md"
    monkeypatch.setattr(watch, "WATCH_DIGEST_MD", target)
    watch.upsert_watch_digest("2026-09-14", watch.render_section("2026-09-14", {"A": [
        {"title": "T1", "url": "", "kind": "paper", "source": "homepage", "confidence": 0.9}
    ]}))
    first = target.read_text(encoding="utf-8")
    watch.upsert_watch_digest("2026-09-14", watch.render_section("2026-09-14", {"A": [
        {"title": "T2", "url": "", "kind": "video", "source": "homepage", "confidence": 0.9}
    ]}))
    second = target.read_text(encoding="utf-8")
    assert "T2" in second and "T1" not in second
    assert second.count("<!-- BEGIN WATCH 2026-09-14 -->") == 1
    assert first  # sanity: first write produced content


def test_render_section_flags_low_confidence():
    md = watch.render_section("2026-09-14", {"A": [
        {"title": "Shaky", "url": "", "kind": "other", "source": "homepage", "confidence": 0.4}
    ]})
    assert "低置信" in md
