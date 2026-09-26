"""条目类型（``kind``）的图标与文案 —— 全项目唯一事实源。

为什么需要这个模块
------------------
``kind`` 词表此前在 :mod:`glean.watch`、:mod:`glean.ccf`、:mod:`glean.notify`
各存一份，其中 ``notify`` 那份是前两份的**手工合并副本**。手工合并必然漂移，
而且已经漂了：``program`` 在 digest 里写作「会议日程」、在推送文案里写作
「会议日程 (Program)」，``papers`` 则是「接收论文」/「接收论文列表」——
同一件事在两处给人看到两种说法。

把词表下沉到这里，三处引用同一份定义，漂移从「迟早发生」变成「不可能发生」。

约束：本模块**不得 import 任何同层模块**
----------------------------------------
``watch`` / ``ccf`` / ``notify`` 都要 import 它；而 ``notify`` 又被
:mod:`glean.monitor` 依赖（``monitor → notify``）。一旦本模块反向 import
``watch`` 之类，立刻成环。因此这里只允许 import 标准库。
"""

from __future__ import annotations

# 学者监控：主页 / DBLP / S2 能产出的成果类型。
WATCH_KIND_ICONS = {
    "paper": "\U0001f4c4",  # 📄
    "video": "\U0001f3a5",  # 🎥
    "report": "\U0001f4d5",  # 📕
    "talk": "\U0001f3a4",  # 🎤
    "other": "\U0001f517",  # 🔗
}

WATCH_KIND_LABELS = {
    "paper": "论文",
    "video": "视频",
    "report": "技术报告",
    "talk": "报告/演讲",
    "other": "其它",
}

# CCF 监控：会议 / 期刊能被监控到的三类事件。
CCF_KIND_ICONS = {
    "cfp": "\U0001f4e2",  # 📢
    "program": "\U0001f4c5",  # 📅
    "papers": "\U0001f4c4",  # 📄
    "other": "\U0001f517",  # 🔗
}

CCF_KIND_LABELS = {
    "cfp": "征稿 (CFP)",
    "program": "会议日程",
    "papers": "接收论文",
    "other": "其它",
}

#: 合并视图，给需要同时处理两类条目的消费者用（如 :mod:`glean.notify` 的推送文案、
#: Web 的 NEW 徽标）。两组 key 互不重叠。
KIND_ICONS: dict[str, str] = {**WATCH_KIND_ICONS, **CCF_KIND_ICONS}
KIND_LABELS: dict[str, str] = {**WATCH_KIND_LABELS, **CCF_KIND_LABELS}
