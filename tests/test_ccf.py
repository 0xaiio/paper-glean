"""Tests for :mod:`glean.ccf` — venue list management, source selection, diffing.

No network and no touching of the real repo files: every path constant is
redirected into ``tmp_path`` and the two remote sources are stubbed.
"""

from __future__ import annotations

import pytest

from glean import ccf, notify

SAMPLE = """# CCF-A 会议 / 期刊监控名单

## 会议

- [x] **SIGMOD** — ACM Conference on Management of Data
  - area: 数据库/数据挖掘/内容检索 (DB)
  - homepage: https://2027.sigmod.org/
  - dblp: https://dblp.org/db/conf/sigmod
  - ccf: A

- [ ] **PODS** — ACM Symposium on Principles of Database Systems
  - area: 数据库/数据挖掘/内容检索 (DB)
  - homepage: https://sigmod.org/pods/
  - ccf: A

## 期刊

- [x] **TODS** — ACM Transactions on Database Systems
  - area: 数据库/数据挖掘/内容检索 (DB)
  - homepage: https://dl.acm.org/journal/tods
  - ccf: A
  - issn: 0362-5915
"""

RSS = """<rss><channel>
<item><title>SIGMOD 2027 Deadline</title>
<link>https://2027.sigmod.org/</link>
<description>ACM Conference on Management of Data
Deadline (UTC-12): 2026-08-01 23:59:59
Category: 数据库</description></item>
<item><title>PODS 2027 Deadline</title>
<link>https://2027.sigmod.org/</link>
<description>x
Deadline (UTC-12): 2026-11-01 23:59:59</description></item>
</channel></rss>"""


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    md = tmp_path / "ccf.md"
    md.write_text(SAMPLE, encoding="utf-8")
    monkeypatch.setattr(ccf, "CCF_MD", md)
    monkeypatch.setattr(ccf, "CCF_STATE", tmp_path / "ccf_state.json")
    monkeypatch.setattr(ccf, "CCF_EVENTS", tmp_path / "ccf_events.jsonl")
    monkeypatch.setattr(ccf, "CCF_DIGEST_MD", tmp_path / "CCF-digest.md")
    monkeypatch.setattr(notify, "CCF_NEW", tmp_path / "ccf_new.json")
    return tmp_path


@pytest.fixture
def offline(isolated, monkeypatch):
    """Stub the two remote sources so tests never touch the network."""
    monkeypatch.setattr(ccf, "fetch_rss", lambda *a, **k: RSS)
    monkeypatch.setattr(
        ccf,
        "parse_venue_page",
        lambda url, **k: [
            {
                "title": "Accepted Papers",
                "url": url + "/accepted",
                "kind": "papers",
                "year": 2027,
                "deadline": "",
                "venue": "",
                "source": "homepage",
                "confidence": 0.85,
            }
        ],
    )
    monkeypatch.setattr(
        ccf,
        "fetch_crossref_issues",
        lambda issn, venue, homepage, **k: [
            {
                "title": f"{venue} Volume 51 Issue 4",
                "url": homepage,
                "kind": "papers",
                "year": 2026,
                "deadline": "",
                "venue": venue,
                "source": "crossref",
                "confidence": 0.95,
                "article_count": 6,
            }
        ] if issn else [],
    )
    return isolated


# ------------------------------------------------------------------
# ccf.md parsing / mutation
# ------------------------------------------------------------------

def test_parse_ccf_md_reads_kind_checkbox_and_fields(isolated):
    entries = ccf.load_venues()
    assert [e["name"] for e in entries] == ["SIGMOD", "PODS", "TODS"]
    assert [e["kind"] for e in entries] == ["conference", "conference", "journal"]
    assert [e["enabled"] for e in entries] == [True, False, True]
    assert entries[0]["area"].startswith("数据库")
    assert entries[0]["dblp"].endswith("conf/sigmod")
    assert entries[2]["issn"] == "0362-5915"
    assert entries[2]["full"] == "ACM Transactions on Database Systems"


def test_add_then_remove_roundtrip(isolated):
    entry = ccf.add_venue("ICDT", homepage="https://example.org/icdt", area="数据库 (DB)")
    assert entry["key"] == "icdt"
    assert "ICDT" in [e["name"] for e in ccf.load_venues()]
    with pytest.raises(ValueError):
        ccf.add_venue("ICDT", homepage="https://example.org/icdt")
    assert ccf.remove_venue("ICDT") is True
    assert ccf.remove_venue("ICDT") is False


def test_add_requires_a_homepage(isolated):
    """A venue with no public page cannot be monitored — refuse loudly."""
    with pytest.raises(ValueError):
        ccf.add_venue("NoPage", homepage="")


def test_set_enabled_rewrites_the_checkbox(isolated):
    assert ccf.set_enabled("SIGMOD", False) is True
    assert ccf.load_venues()[0]["enabled"] is False
    assert "[ ] **SIGMOD**" in ccf.CCF_MD.read_text(encoding="utf-8")
    assert ccf.set_enabled("Nope", True) is False


def test_set_enabled_area_is_bulk(isolated):
    touched = ccf.set_enabled_area("DB", False)
    assert set(touched) == {"SIGMOD", "PODS", "TODS"}
    assert all(not e["enabled"] for e in ccf.load_venues())
    assert ccf.set_enabled_area("量子计算", False) == []


def test_sync_catalog_keeps_user_ticks(isolated):
    added, _ = ccf.sync_catalog(default_enabled=False)
    assert added >= 70  # the built-in catalogue is large; only new names count
    by_key = {e["key"]: e for e in ccf.load_venues()}
    # SIGMOD was ticked and PODS unticked in the sample — both must survive.
    assert by_key["sigmod"]["enabled"] is True
    assert by_key["pods"]["enabled"] is False
    # Newly discovered venues honour the caller's default.
    assert by_key["icse"]["enabled"] is False
    assert by_key["tods"]["issn"] == "0362-5915"


# ------------------------------------------------------------------
# collection
# ------------------------------------------------------------------

def test_conference_prefers_ccfddl_then_homepage(offline):
    entry = [e for e in ccf.load_venues() if e["name"] == "SIGMOD"][0]
    items = ccf.collect_items(entry, rss_text=RSS)
    kinds = [i["kind"] for i in items]
    assert kinds.count("cfp") == 1
    assert "papers" in kinds
    cfp = next(i for i in items if i["kind"] == "cfp")
    assert cfp["source"] == "ccfddl"
    assert cfp["deadline"].startswith("2026-08-01")
    assert all(i["venue"] == "SIGMOD" for i in items)


def test_journal_uses_crossref_not_ccfddl(offline):
    entry = [e for e in ccf.load_venues() if e["name"] == "TODS"][0]
    items = ccf.collect_items(entry, rss_text=RSS)
    assert [i["kind"] for i in items] == ["papers", "papers"]
    assert {i["source"] for i in items} == {"crossref", "homepage"}


def test_collect_is_offline_when_asked(offline):
    entry = ccf.load_venues()[0]
    assert ccf.collect_items(entry, use_network=False) == []


def test_items_are_deduped_by_fingerprint(offline, monkeypatch):
    monkeypatch.setattr(
        ccf,
        "parse_venue_page",
        lambda url, **k: [
            {"title": "Accepted Papers", "url": "https://x/accepted", "kind": "papers",
             "source": "homepage", "confidence": 0.9},
            {"title": "accepted papers!", "url": "https://x/accepted", "kind": "papers",
             "source": "homepage", "confidence": 0.9},
        ],
    )
    entry = [e for e in ccf.load_venues() if e["name"] == "SIGMOD"][0]
    items = ccf.collect_items(entry, rss_text=RSS)
    titles = [i["title"] for i in items]
    assert titles.count("Accepted Papers") == 1
    assert len([t for t in titles if t.lower() == "accepted papers!"]) == 0


# ------------------------------------------------------------------
# run / state / digest
# ------------------------------------------------------------------

def test_run_seeds_baseline_without_pushing(offline):
    res = ccf.run(request_interval=0)
    # PODS is unticked in the sample list, so only two venues are scanned.
    assert sorted(res["baselined"]) == [
        "SIGMOD（2 条基线）",
        "TODS（2 条基线）",
    ]
    assert res["new_items"] == []
    assert res["pushed_to"] == []
    assert notify.load_new("ccf") == []
    # An empty run still writes a "nothing today" section.
    assert "没有发现更新" in ccf.CCF_DIGEST_MD.read_text(encoding="utf-8")


def test_unticked_venues_are_never_scanned(offline):
    ccf.run(request_interval=0)
    state = ccf.load_state()
    assert "pods" not in state["venues"]
    assert set(state["venues"]) == {"sigmod", "tods"}


def test_run_detects_only_unseen_items(offline, monkeypatch):
    ccf.run(request_interval=0)
    # A new CFP appears on ccfddl for the next edition.
    monkeypatch.setattr(
        ccf,
        "fetch_rss",
        lambda *a, **k: RSS
        + """<item><title>SIGMOD 2028 Deadline</title><link>https://2028.sigmod.org/</link>
        <description>x
Deadline (UTC-12): 2027-08-01 23:59:59</description></item>""",
    )
    res = ccf.run(request_interval=0)
    assert res["grouped"] == {"SIGMOD": res["grouped"].get("SIGMOD", [])}
    assert len(res["new_items"]) == 1
    assert res["new_items"][0]["title"] == "SIGMOD 2028 Deadline"
    assert "file" in res["pushed_to"]
    assert len(notify.load_new("ccf")) == 1
    digest = ccf.CCF_DIGEST_MD.read_text(encoding="utf-8")
    assert "SIGMOD 2028 Deadline" in digest
    assert "## " + res["day"] in digest


def test_force_pushes_on_first_sighting(offline):
    res = ccf.run(force=True, push=False, request_interval=0)
    assert len(res["new_items"]) == 4  # 2 venues x 2 items
    assert res["pushed_to"] == []  # push=False honoured


def test_events_are_logged_once_per_item(offline):
    ccf.run(force=True, push=False, request_interval=0)
    events = ccf.load_events()
    assert len(events) == 4
    assert {e["venue"] for e in events} == {"SIGMOD", "TODS"}
    assert all(e["pushed_to"] == [] for e in events)


def test_run_survives_one_broken_venue(offline, monkeypatch):
    def boom(url, **kwargs):
        raise RuntimeError("dns exploded")

    monkeypatch.setattr(ccf, "parse_venue_page", boom)
    res = ccf.run(request_interval=0)
    assert any("SIGMOD" in e for e in res["errors"])
    assert res["baselined"] == []


def test_digest_upsert_is_idempotent(offline):
    day = "2026-09-14"
    section = ccf.render_section(day, {"SIGMOD": [{"title": "x", "kind": "cfp", "url": ""}]})
    ccf.upsert_ccf_digest(day, section)
    first = ccf.CCF_DIGEST_MD.read_text(encoding="utf-8")
    ccf.upsert_ccf_digest(day, section)
    assert ccf.CCF_DIGEST_MD.read_text(encoding="utf-8") == first


def test_render_section_labels_kinds():
    out = ccf.render_section(
        "2026-09-14",
        {"SIGMOD": [{"title": "t", "kind": "cfp", "deadline": "2026-08-01", "url": ""}]},
    )
    assert "征稿 (CFP)" in out
    assert "BEGIN CCF 2026-09-14" in out
