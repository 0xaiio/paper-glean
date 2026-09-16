# arXiv Daily Digest

> 自动生成的 arXiv 每日新增论文摘要。类别: math.LO, cs.AI, cs.LG, cs.DB, cs.DC, cs.FL, cs.LO, cs.PL, cs.SE。
> 由 `arxiv_daily.py` 抓取; ★/🧐 推荐由 agent 根据研究兴趣补充(见 `README.md`)。
> 推荐指数: ★=基于当前研究兴趣(五星强烈推荐); 🧐=视野扩展(五个强烈推荐)。

<!-- BEGIN 20260916 -->
## 20260916

时间窗口(UTC): 2026-09-15 04:06 → 2026-09-16 04:06 | 去重后共 **295** 篇 | 🎯 关键词命中(interests.md): ★ 8 篇 / 🧐 1 篇

### 📌 重点关注(基于研究兴趣, agent 填写)

| 推荐指数 | 论文 | 推荐理由 |
| --- | --- | --- |
| ★★★★★ | **Byzantine Reliable Broadcast with Causal Ordering** — [2609.17074](https://arxiv.org/abs/2609.17074) · [📄](#20260916-2609.17074) (cs.DC) | 命中兴趣点「分布式计算与共识」的 `Byzantine`(条目权重 3，`score_star`=3)。作者 Cachin，正统分布式系统脉络。既有工作几乎都把因果序架在 total-order broadcast 之上，而本文指出：基于进程 happened-before 的经典因果定义在拜占庭模型下**不成立**——拜占庭进程可谎报、省略、伪造消息依赖，因此需要重新定义因果序并与 reliable broadcast 直接组合。同时压在「分布式共识」与「协议正确性论证」两条线上，是本批唯一的核心区命中。 |
| ★★★★☆ | **Vibe-Coded and Tuned: A State-of-the-Art SMT Solver for QF-LRA** — [2609.16706](https://arxiv.org/abs/2609.16706) · [📄](#20260916-2609.16706) (cs.LO) | 命中兴趣点「形式化方法与验证」的 `SMT solver`(权重 3)。求解器 primo 在 QF-LRA 上超过 SMT-COMP 2026 该赛道冠军，路径是「系统文献综述 + 反复 profiling + 参数调优」而非新理论。两个可读点：① 求解器性能工程中调优空间的实证幅度（有意思的反面证据：增益主要来自工程调优）；② 「LLM 辅助实现自动推理工具」这一趋势的量化数据点，与扩展点「LLM 与形式化/系统的交叉」呼应。 |
| ★★★★☆ | **How Can We Shrink the Family of Test Databases? Query Containment with Nulls and Comparisons** — [2609.16218](https://arxiv.org/abs/2609.16218) · [📄](#20260916-2609.16218) (cs.DB) | **关键词未命中(score=0)，按 cs.DB 领域相关性人工补充**。查询包含/等价是查询优化与重写的判定核心：CQ 情形靠对单个 canonical database 求值即可判定，但 SQL 三值语义下的 NULL 与序比较使问题升为 $\Pi_2^p$-complete，既有刻画只能给出**指数族**测试数据库，无法用于等价性认证。本文针对带 NULL 的查询收缩该测试数据库族。与「事务隔离与数据库一致性检测」中的 `database testing` / 一致性判定直接相邻。⚠️ 画像缺此类词条，建议增补 `query containment` / `test database` / `canonical database` / `SQL semantics`。 |

> 排除说明：`consensus` 另有 4 次命中(2609.17331 / 2609.17221 / 2609.16917 / 2609.17138)，语境分别为 agent 社会性共识、LLM 的 "polite consensus"、神经网络优化收敛到 "global consensus"、遥感制图的双人解译一致性，**均非分布式共识协议，不计入**；`Raft` 命中 2609.16637 实为光流模型 **RAFT**(Recurrent All-Pairs Field Transforms)，与共识协议无关。**今日 cs.DB 仅 4 篇(API 窗口内 0 篇，RSS 补回 4 篇)，本期 DB 侧候选池本身很小。** |

### 🧐 视野扩展(agent 填写)

| 推荐指数 | 论文 | 推荐理由 |
| --- | --- | --- |
| 🧐🧐🧐🧐 | **Universal Properties of Petri Net Unfoldings** — [2609.17324](https://arxiv.org/abs/2609.17324) · [📄](#20260916-2609.17324) (cs.LO) | **关键词未命中(score=0)，按形式化方法领域相关性人工补充**。Petri 网展开是并发系统验证(偏序化简、模型检测)的标准工具，但长期存在一个结构性缺口：展开构造看起来像范畴论里的泛构造，却因**忽略网的内部对称性**而不满足预期的泛性质。本文给出两条出路——显式化对称性以取得 "up to symmetry" 的弱泛性质，或直接打破对称性。并发语义 + 范畴论，属「形式化方法与验证」的语义基础侧。 |
| 🧐🧐🧐 | **SWB-DM: A Calibrated Sliced-Wasserstein-Barycenter Aggregator with Delayed-Momentum Caching for Byzantine-Robust Federated Learning under Partial Participation** — [2609.16099](https://arxiv.org/abs/2609.16099) · [📄](#20260916-2609.16099) (cs.LG) | 命中兴趣点「分布式计算与共识」的 `Byzantine`(权重 3)，但**威胁模型不同**：这里的拜占庭指联邦学习中的恶意客户端投毒，目标是鲁棒聚合，不是状态机复制下的共识协议，故列为扩展而非重点。技术点值得一看：把每片客户端更新视为一维分布求裁剪 Wasserstein 重心 + 延迟动量缓存，且明确指出部分参与下 coordinate-wise median / Krum / Bulyan / trimmed mean 的有限样本保证会失效。 |
| 🧐🧐🧐 | **Agentic Search Spaces for Tabular Machine Learning** — [2609.16309](https://arxiv.org/abs/2609.16309) · [📄](#20260916-2609.16309) (cs.LG) | 命中扩展点「LLM 与形式化/系统的交叉」的 `LLM-based agent`(权重 3)。把表格模型拆成 preprocessing / embeddings / architecture / training / inference 的模块化流水线，让 agent 设计扩展版 HPO 搜索空间并与作者给定的标准空间对比——是「agent 能否真正改进系统/配置空间设计」这一 AI for systems 命题的实测，而非又一个代码生成演示。 |
| 🧐🧐🧐 | **Exact Complexity of the Satisfiability Problem for Strategy Logic** — [2609.16173](https://arxiv.org/abs/2609.16173) · [📄](#20260916-2609.16173) (math.LO) | **关键词未命中(score=0)，按逻辑/形式化领域相关性人工补充**。证明 Strategy Logic 的可满足性问题为 $\Pi^1_\infty$-complete，且计算同构于真二阶算术；下界在 next-time Boolean-goal 片段即成立，因而该逻辑**不可递归公理化**（即便允许有效给出的 $\omega$-规则）。对多智能体/博弈性质规约的表达力边界给出了硬结论，属「形式化方法与验证」的表达力与判定性一侧。 |

### 分类清单

#### math.LO (6)

- <a id="20260916-2609.16173"></a>**Exact Complexity of the Satisfiability Problem for Strategy Logic** — [2609.16173](https://arxiv.org/abs/2609.16173)  
  Tikhon Pshenitsyn  
  We show that the satisfiability problem for Strategy Logic introduced by Mogavero, Murano, and Vardi is $\Pi^1_\infty$-complete, and, more strongly, computably isomorphic to true second-order arithmetic. The lower bound is established for the next-time Boolean-goal fragment of Strategy Logic.
- <a id="20260916-2609.16881"></a>**An extension of Subcomplete Forcing Axiom which implies $\diamondsuit^+$** — [2609.16881](https://arxiv.org/abs/2609.16881)  
  Hiroshi Sakai  
  We prove that the Subcomplete Forcing Axiom is consistent with $\diamondsuit^+$.
- <a id="20260916-2609.16922"></a>**Multiplicatively idempotent HSI algebras satisfy all equations of $\mathbb{N}$** — [2609.16922](https://arxiv.org/abs/2609.16922)  
  Tumadhir Alsulami, Marcel Jackson, Michael Kinyon  
  An algebra with binary operations $+,\cdot,\uparrow$ and constant $1$ is called an HSI algebra if it satisfies the basic commutative semiring laws for $+,\cdot,1$ on~$\mathbb{N}$ as well as the familiar index laws for exponentiation $\uparrow$. These basic axioms, known as the ``High School Identities'' are known to be incomplete, and an algebra satisfying $\HSI$ but failing an equation valid on …
- <a id="20260916-2609.17087"></a>**The Boolean Prime Ideal Theorem and Vitali Sets** — [2609.17087](https://arxiv.org/abs/2609.17087)  
  Jindrich Zapletal  
  If ZFC is consistent, then so is ZF+DC+BPI+there is no Vitali set.
- <a id="20260916-2609.17153"></a>**Two variants of minimality in forcing extensions** — [2609.17153](https://arxiv.org/abs/2609.17153)  
  Martin Goldstern, Tatsuya Goto  
  We introduce d-minimal and b-minimal extensions, two weakenings of minimality based respectively on eventual domination and infinitely often domination. We prove that the generic extensions obtained by the full Mathias forcing and by Mathias forcing relative to Ramsey ultrafilters are d-minimal, whereas Hechler extensions are b-minimal.
- <a id="20260916-2609.17177"></a>**Finite Borel asymptotic dimension of bounded-to-one commutative monoid actions** — [2609.17177](https://arxiv.org/abs/2609.17177)  
  Ruijun Wang  
  We prove that every bounded-to-one action of a finitely generated commutative monoid has finite asymptotic dimension, without a freeness assumption. If the group completion has torsion-free rank $r$, we give an explicit upper bound $(3^{r+1}-3)/2$.

#### cs.AI (96)

- <a id="20260916-2609.17331"></a>**Self-Emergence Agent Architecture:Behavior-Inertia HMM, Reflexive Metacognition,and Social-Contrastive Self-Modeling** — [2609.17331](https://arxiv.org/abs/2609.17331) | 🎯★ consensus  
  Xiaoyang Liu  
  Large language model (LLM) agents exhibit strong language-generation and problem-solving capabilities, yet suffer from three structural limitations: personality drift, non-evolutionary reflection, and the absence of a self-other boundary. Existing generative-agent simulations rely on static memory and fixed prompts, maintaining neither behavioral inertia nor endogenous self-evolution.
- <a id="20260916-2609.17527"></a>**Agentic Societies Need a Social Harness** — [2609.17527](https://arxiv.org/abs/2609.17527) | cross: cs.AI, cs.NI  
  Tapan Chugh, Vidushi Singh, Krish Jain, Arvind Krishnamurthy et al.  
  An agentic society is a collection of AI agents that coordinate autonomously across trust boundaries, on behalf of different principals whose objectives may only partially align. We show experimentally that in agentic societies even honest, competent agents often fail to reach satisfactory outcomes with existing harnesses and messaging primitives, and that faulty or malicious agents can stall …
- <a id="20260916-2609.17523"></a>**ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents** — [2609.17523](https://arxiv.org/abs/2609.17523) | cross: cs.CL  
  Shuhan Xue, Jianyuan Zhong, Ziyuan Nan, Wenbin Li et al.  
  We introduce and release ScienceBuddy, an interactive scientific research workspace that brings continually improving scientific agents into researchers' everyday workflows. ScienceBuddy supports researchers in carrying out scientific tasks while transforming their requests, feedback, and execution evidence into tasks and evaluation rubrics for continual learning.
- <a id="20260916-2609.17521"></a>**PhysStream: Streaming Physics-Grounded Video Generation with Structured Scene Memory and Fine-Grained Motion Control** — [2609.17521](https://arxiv.org/abs/2609.17521) | cross: cs.AI, cs.GR  
  Chuhao Chen, Peter Wonka, Chaoyang Wang, Chen Wang et al.  
  Interactive control for video generation is moving from coarse prompts toward fine-grained, physically meaningful manipulation of dynamic scenes. Yet existing controllable methods either require the full control schedule before generation starts, or use pixel-space signals that dictate object positions rather than physical dynamics.
- <a id="20260916-2609.17516"></a>**When Should LLMs Abstain? Chain-of-Self-Questioning for Selective Risk Control** — [2609.17516](https://arxiv.org/abs/2609.17516) | cross: cs.AI  
  Ali Şenol  
  Large language models can produce fluent answers when their factual support is weak. This paper introduces Chain-of-Self-Questioning (CoSQ), a prompt-only framework that makes answer commitment conditional on an explicit assessment of the information required to answer a question.
- <a id="20260916-2609.17509"></a>**LACE: Layer-Wise Compression for Dynamic Frame Rate Codecs** — [2609.17509](https://arxiv.org/abs/2609.17509) | cross: cs.AI, cs.CL  
  Thanapat Trachu, Samuele Cornell, William Chen, Shinji Watanabe  
  Neural audio codecs are a key component in speech language modeling. However, their high frame rates lead to long sequence lengths, increasing computational costs.
- <a id="20260916-2609.17496"></a>**Verifiable Social Reasoning for LLM Assistants** — [2609.17496](https://arxiv.org/abs/2609.17496) | cross: cs.CL  
  Amir Taubenfeld, Zorik Gekhman, Avigail Grinstein-Dabush, Itay Laish et al.  
  LLM assistants are widely used for daily social advice, yet evaluating their social reasoning in such consultation settings remains challenging since (i) it requires setups where the assistant learns about social situations from subjective user narratives, and (ii) social properties, such as others' intentions, typically lack verifiable ground truth. To address these challenges, we introduce …
- <a id="20260916-2609.17488"></a>**LimiX-2: A Contextual Mechanism Network Towards General Structured-Data Intelligence** — [2609.17488](https://arxiv.org/abs/2609.17488)  
  Xingxuan Zhang, Gang Ren, Hao Yuan, Hao Zou et al.  
  We introduce LimiX-2, a new model in the LimiX family, developed through model and data scaling guided by our previously established scaling laws. LimiX-2 adopts the Contextual Mechanism Networks (CMNs) paradigm and is pretrained with Context-Conditional Masked Modeling (CCMM).
- <a id="20260916-2609.17479"></a>**Det-LIME: Detector-Aware, Multi-Instance Local Interpretable Model-Agnostic Explanations for Automated Marine Mammal Detection** — [2609.17479](https://arxiv.org/abs/2609.17479) | cross: cs.AI  
  Jiayi Zhou, David W. Johnston, Brinnae Bent  
  Despite the rapid uptake of black-box object detectors in marine mammal research and monitoring, explainability techniques are rarely integrated into conservation workflows. Furthermore, most classification-oriented explainability tools are ill-suited to detection tasks involving imagery of social organisms or those with colonial life histories, as they ignore multiple detections within a scene …
- <a id="20260916-2609.17475"></a>**JustFit: 200K-Token LLM Serving on a 24 GiB Laptop with Just-in-Time State Management** — [2609.17475](https://arxiv.org/abs/2609.17475) | cross: cs.PF  
  Yuhua Chen  
  Capable open-weight models make local coding and reasoning attractive, but their context and execution state strain laptop memory. We present JustFit, an MLX-based inference runtime that combines KVExec for compressed KV execution, PhaseSwap for component residency, and StateTrans for state-preserving serving transitions.
- <a id="20260916-2609.17464"></a>**Decomposition Buys Integrity, Not Yield** — [2609.17464](https://arxiv.org/abs/2609.17464) | cross: cs.AI, cs.DC  
  Rong He  
  Multi-agent systems split a task across a tree of agents and justify the split with folklore: smaller contexts, cleaner separation, parallelism. We ask what the split does to how much of what the leaves discover reaches the root.
- <a id="20260916-2609.17439"></a>**Evaluating Verified Autonomy in Quantum Engineering** — [2609.17439](https://arxiv.org/abs/2609.17439) | cross: cs.AI  
  Naixu Guo, Changhao Li, Siyu Cheng, Qicheng Tang et al.  
  Reliable quantum engineering is essential for turning quantum phenomena into practical technologies. As quantum platforms grow in scale and complexity, their characterization and operation require increasing human effort and coordination.
- <a id="20260916-2609.17434"></a>**CareMirror: Bringing Caregiver Wellbeing into the Dementia Care Ecosystem** — [2609.17434](https://arxiv.org/abs/2609.17434) | cross: cs.AI, cs.CL, cs.CY  
  Jiayue Melissa Shi, Ethan Nguyen, Drishti Goel, Upasana Natarajan et al.  
  Family caregivers of people living with dementia shoulder emotional and practical responsibilities, yet their own wellbeing often remains peripheral to dementia care. We built CareMirror, an envisioned caregiver wellbeing ecosystem with interconnected caregiver- and clinician-facing interfaces for longitudinal reflection, personalized support, and caregiver-controlled sharing with clinical care.
- <a id="20260916-2609.17427"></a>**Tracking the Unseen: An Occlusion-Robust Framework for Target Tracking Under Full and Long-Term Occlusion** — [2609.17427](https://arxiv.org/abs/2609.17427) | cross: cs.AI  
  Mais Mohammed, Sharifa Mohammed, Hanan Awadh, Haneen Bamaas et al.  
  Real-time multi-object tracking systems remain highly vulnerable to full and long-term occlusion, where targets temporarily or completely disappear from the camera's field of view. Conventional trackers may terminate trajectories prematurely, resulting in identity loss and reduced situational awareness in applications such as defense and surveillance.
- <a id="20260916-2609.17391"></a>**FlashVector: Agent for Hierarchical Model Serving Stack Optimization** — [2609.17391](https://arxiv.org/abs/2609.17391) | cross: cs.PF  
  Qi Wu, Lohan Lemire, Kai Meng, Zhongmou Cai et al.  
  Model serving is one of the largest cost drivers in production recommender systems. Maximizing its throughput requires navigating a deeply layered hierarchy: GPU kernels, the ML framework computation graph, the model server, and on-demand feature processing -- each demanding specialized domain expertise.
- <a id="20260916-2609.17346"></a>**Where Should a Document Live: Context, Representations, or Parameters?** — [2609.17346](https://arxiv.org/abs/2609.17346) | cross: cs.AI  
  Nathanaël Carraz Rakotonirina, Momchil Hardalov, Gonzalo Iglesias, Adrià de Gispert  
  To answer questions outside of their pre-training data, large language models (LLMs) need access to new information, which can be presented in the context window as documents, encoded into the model's parameters, or injected as latent representations. However, each of these methods comes with different efficiency, cost, and performance trade-offs, with no single winner.
- <a id="20260916-2609.17327"></a>**Vroom-Vroom at SHROOM-Visions: A Multi-Judge Committee for Detecting Hallucinated Spans in Vision-Language Outputs** — [2609.17327](https://arxiv.org/abs/2609.17327) | cross: cs.AI  
  Toqeer Ehsan, Nico Penttilä, Richard Schmidt, Arash Hajikhani et al.  
  This paper describes our submission to the SHROOM-Visions shared task on detecting and classifying hallucinated character spans in vision-language model outputs across four languages. We employ several fine-tuned vision-language models as independent annotators and combine their span predictions through character-level majority voting, and additionally explore activation probes.
- <a id="20260916-2609.17326"></a>**From Transient Prompts to Persistent Control: Scientific Poster Generation via Recursive Semantic-Geometric Contracts** — [2609.17326](https://arxiv.org/abs/2609.17326)  
  Runze Li, Yukun Zhao, Can Xu, Yucheng Shen et al.  
  Scientific poster generation distills a multimodal paper into a single-page visual artifact, forcing strict trade-offs between informational coverage and readability under a fixed spatial budget. Existing methods pass plans as transient prompts and validate individual stages in isolation.
- <a id="20260916-2609.17325"></a>**Intrinsic Motivation in Reinforcement Learning: A Research Agenda for Adaptive Self-Organisation** — [2609.17325](https://arxiv.org/abs/2609.17325)  
  Anatoly Belikov  
  Biological cells can be viewed as individual, interacting agents whose collective dynamics give rise to adaptive behaviour at multiple levels of organisation, from individual cells through tissues to whole multicellular organisms. In this perspective and tutorial article we discuss whether intrinsic rewards in artificial neural systems can support adaptation, functional specialisation and …
- <a id="20260916-2609.17306"></a>**Mo' Models, Mo' Problems: How to best select model pools when designing Multi-Agent Systems** — [2609.17306](https://arxiv.org/abs/2609.17306) | cross: cs.AI  
  Sara Vera Marjanović, Jiacheng Xu, Aleksandr Laptev, Grigor Nalbandyan et al.  
  Multi-agent Systems (MAS) combine multiple model outputs to solve complex reasoning tasks. However, despite rapid growth of available open-source models, there is limited research on how to select optimal model candidates out of this massive pool.
- <a id="20260916-2609.17291"></a>**Extracting ontology-compliant knowledge from scientific text describing irradiated materials using large language models** — [2609.17291](https://arxiv.org/abs/2609.17291)  
  Marco Luca Sbodio, Marcos Martínez Galindo, Vanessa Lopez, Blanca Biel et al.  
  The quest for new materials increasingly relies on predictive models and comprehensive simulations that span scales from atomic to macroscopic levels. However, essential data necessary for these models and simulations are often embedded in scientific literature as unstructured text, limiting reusability and posing challenges for researchers seeking to leverage existing knowledge effectively.
- <a id="20260916-2609.17227"></a>**FROD: Feature Matching Residual Denoising Oracle Bone Decipher** — [2609.17227](https://arxiv.org/abs/2609.17227) | cross: cs.AI  
  Yanbin Hou, Biao Xiong, Guojun Xu, Jianwen Xiang et al.  
  Oracle bone script (OBS), one of the earliest Chinese writing systems, plays an important role in the study of Chinese etymology. Traditional decipherment relies heavily on domain experts who analyze characters through semantic context and structural evolution.
- <a id="20260916-2609.17210"></a>**FluxVLA Engine: A One-Stop VLA Engineering Platform for Embodied Intelligence** — [2609.17210](https://arxiv.org/abs/2609.17210) | cross: cs.AI  
  Yinhao Li, Weixin Mao, Zihan Lan, Jikun Rong et al.  
  Vision-language-action (VLA) models, world-action models (WAMs), and offline reinforcement learning methods are rapidly expanding the design space of embodied policies, yet turning these algorithms into reliable robot systems remains constrained by fragmented data formats, training stacks, evaluation protocols, inference runtimes, and embodiment-specific interfaces. We present $\mathrm{FluxVLA}$ …
- <a id="20260916-2609.17193"></a>**End-to-End Latency-Minimizing and Load-Balanced Request Scheduling for Edge LLM Inference in Agentic AI Services** — [2609.17193](https://arxiv.org/abs/2609.17193)  
  Zhen Li, Jun Cai, Haoran Gao, An Li et al.  
  Large language model (LLM)-powered agentic AI services increasingly demand low-latency inference, motivating the deployment of LLMs across distributed edge servers. However, heterogeneous communication and computing capabilities, together with dynamically evolving inference states, make the edge server selection for each incoming request time-varying and tightly coupled across slots.
- <a id="20260916-2609.17181"></a>**Multimodal Cultural Heritage Architectural Style Classification for Residential Buildings in the UAE Based on CLIP Embeddings and SVM** — [2609.17181](https://arxiv.org/abs/2609.17181) | cross: cs.AI  
  Ahmed Ammar Kubba, Manar Abu Talib, Iman Ibrahim, Qassim Nasir  
  The analysis and classification of cultural heritage architectural styles remain challenging due to the complexity of visual images of buildings, which are highly relied on in traditional CNN-based classification approaches in comparison to textual descriptions, and the relative lack of non-western region-specific datasets. This paper addresses this gap by proposing a multimodal machine learning …
- <a id="20260916-2609.17180"></a>**MOCC-R1: Reinforcing Reasoning-Response Consistency for Multimodal Counselor Response Generation** — [2609.17180](https://arxiv.org/abs/2609.17180)  
  Wenjie Zheng, Qiming Xie, Jianfei Yu, Rui Xia  
  Multimodal counselor response generation (MCRG) aims to generate an appropriate counselor response from multimodal dialogue histories. Progress is limited by two gaps: first, existing datasets rarely capture sustained, human-recorded counseling interactions conducted by qualified counselors; Second, existing methods do not explicitly optimize consistency between counseling reasoning and the …
- <a id="20260916-2609.17169"></a>**MUMINS: Metadata-conditioned Uncertainty-aware Medical Image Next-state Synthesis** — [2609.17169](https://arxiv.org/abs/2609.17169) | cross: cs.AI  
  Anna Oliveras, Roger Marí, Rafael Redondo, Oriol Guardià et al.  
  Forecasting anatomical changes such as tumor growth and neurodegeneration is a challenging generative vision task. Morphological evolution is subtle relative to static anatomy, highly patient-specific, and inherently stochastic.
- <a id="20260916-2609.17152"></a>**ResLRP: The Role of Residual Cancellation in Attribution Instability in Vision Transformers** — [2609.17152](https://arxiv.org/abs/2609.17152) | cross: cs.AI, cs.LG  
  Jim Berend, Reduan Achtibat, Daniel Schäffer, Alexander Binder et al.  
  Vision Transformers (ViTs) are central to most modern vision models, yet obtaining input attributions that are fine-grained, faithful, and stable remains challenging. Layer-wise Relevance Propagation (LRP) has been adapted to transformer attention, but in ViTs it often produces noisy, unfaithful explanations.
- <a id="20260916-2609.17147"></a>**Kernel-Based Metrics Learning for Uncertain Opponent Vehicle Trajectory Prediction in Autonomous Racing** — [2609.17147](https://arxiv.org/abs/2609.17147) | cross: cs.AI, cs.LG  
  Hojin Lee, Youngim Nam, Sanghun Lee, Cheolhyeon Kwon  
  Autonomous racing confronts significant challenges in safely overtaking Opponent Vehicles (OVs) that exhibit uncertain trajectories, stemming from unknown driving policies. To address these challenges, this study proposes heterogeneous kernel metrics for Deep Kernel Learning (DKL), designed to robustly capture the diverse driving policies of OVs, and carry out precise trajectory predictions along …
- <a id="20260916-2609.17141"></a>**Continual Learning for Traversability Prediction with Uncertainty-Aware Adaptation** — [2609.17141](https://arxiv.org/abs/2609.17141) | cross: cs.AI, cs.LG  
  Hojin Lee, Yunho Lee, Daniel A Duecker, Cheolhyeon Kwon  
  Traversability prediction is a critical component of autonomous navigation in unstructured environments, where complex and uncertain robot-terrain interactions pose significant challenges such as traction loss and dynamic instability. Despite recent progress in learning-based traversability prediction, these methods often fail to adapt to novel terrains.
- <a id="20260916-2609.17128"></a>**FirmCORe: A Benchmark for Structured Reasoning about Inter-Firm Collaboration Opportunities** — [2609.17128](https://arxiv.org/abs/2609.17128)  
  Tian Du, Tiantong Wu, Yafei Wang, Mengyu Liu et al.  
  Comprehensive structured data on inter-firm relationships is often scarce or inaccessible because many relationships are privately negotiated, selectively disclosed, and fragmented across proprietary databases. This scarcity hinders the discovery of collaboration opportunities, particularly for startups and small and medium-sized enterprises.
- <a id="20260916-2609.17123"></a>**AI for Science with GPT-6 Astra: Thermal Design and Electrothermal Analysis of 2D CFET** — [2609.17123](https://arxiv.org/abs/2609.17123) | cross: cs.AI, cs.AR  
  Min-Hui Kim, Khushi Sharma, Sarah Zhang, Ye Wang  
  Thermal optimization of 2D CFET inverters requires testing structural proposals against their electrical costs. We examine these research tasks using an AI agent workflow within a supplied electrothermal model.
- <a id="20260916-2609.17111"></a>**Finding Common Mistakes In Modelling With Mathematical Formalisms Using LLMs** — [2609.17111](https://arxiv.org/abs/2609.17111) | cross: cs.AI, cs.LO  
  Lilian Killich, Marko Schmellenkamp, Fabian Vehlken, Thomas Zeume  
  Modelling with mathematical formalisms like logical formulas, mathematical equations, or regular expressions is an important yet challenging task for students of computer science and other STEM disciplines. Identifying common mistakes occurring in this context is an important step towards helping struggling students by providing targeted high-quality feedback, e.g.
- <a id="20260916-2609.17109"></a>**Shared-Prefix KV Reuse Across Standard LoRA Adapters: Quality and Serving Tradeoffs** — [2609.17109](https://arxiv.org/abs/2609.17109) | cross: cs.CL  
  Dushyant Rajput  
  A common small-model deployment runs one shared backbone with several LoRA specialists that answer over the same context. Serving them naively re-prefills that shared context once per specialist.
- <a id="20260916-2609.17107"></a>**Symbolic Separation: Grounding Deep Agents in Knowledge Graphs for Trustworthy Operational Data Analytics** — [2609.17107](https://arxiv.org/abs/2609.17107)  
  Baibek Davletiyarov, Junaid Ahmed Khan, Andrea Bartolini  
  Generative AI promises natural language access to the massive numerical telemetry of data centers and Industry 4.0 installations, yet text-to-query and tool-using agents stay unreliable: even frontier models answer little more than half of real-world database questions, and far fewer of the multi-step, operational ones, because the LLM must compose how heterogeneous sources relate and …
- <a id="20260916-2609.17100"></a>**Semi-Supervised Learning-Based Genetic Biomarkers Dataset for Multiple-Stage Hepatocellular Carcinoma Prediction** — [2609.17100](https://arxiv.org/abs/2609.17100)  
  Ahmed Ammar Kubba, Manar Abu Talib, Jibran Sualeh Muhammad, Ali Bou Nassif et al.  
  Liver cancer is a complex disease responsible for a high number of deaths across the globe each year, making automated solutions for liver cancer classification urgent. The most common form of liver cancer is hepatocellular carcinoma (HCC), accounting for over 90% of liver cancer cases.
- <a id="20260916-2609.17091"></a>**Scaling-Score Conformal Prediction for Multi-Target Regression** — [2609.17091](https://arxiv.org/abs/2609.17091)  
  Sylvain Rousseau, Soundouss Messoudi  
  Multi-target regression requires a model to simultaneously predict several related outputs. Conformal prediction provides distribution-free, finite-sample marginal coverage guarantees, but extending these to joint multi-dimensional regions in a model-agnostic, sample-efficient manner remains challenging: max-aggregation ignores scale differences, copula-based methods are only asymptotically …
- <a id="20260916-2609.17088"></a>**Interactive Memory Learning for Long-Term Conversations** — [2609.17088](https://arxiv.org/abs/2609.17088) | cross: cs.CL  
  Cai Ke, Jiangyue Yan, Han Zhang, Xin Liu et al.  
  Recent advancements in large language models have significantly enhanced the capabilities of agents in modeling long-term conversations. Despite these successes, existing approaches typically adopt a static heuristic paradigm, where information is passively archived without adaptive memory valuation.
- <a id="20260916-2609.17076"></a>**Sample-Conditioned Representation Selection for Audio Few-Shot Learning** — [2609.17076](https://arxiv.org/abs/2609.17076) | cross: cs.SD  
  Fengrui Liu, Ningxin Shen, Yi Li, Yiwei Fu et al.  
  Few-shot audio classifiers may rely on foreground-background co-occurrences and fail when those correlations shift. On SpurAudio, the resulting representation shift is concentrated and class dependent: for ResNet12, the top 10 percent of channels explain 82.80 percent of the null-corrected shift contribution.
- <a id="20260916-2609.17068"></a>**Beyond In-Distribution Metrics: A Systematic Out-of-Distribution Evaluation of Congenital Heart Disease Segmentation** — [2609.17068](https://arxiv.org/abs/2609.17068) | cross: cs.AI  
  Aniketh Vijesh, Shrisharanyan Vasu, Abhijit Ramesh, Clare Pomeroy-Ward et al.  
  Congenital heart disease (CHD) diagnosis and surgical planning often require patient-specific 3D anatomical models, but manual segmentation is labor-intensive, particularly in complex anatomies. Although deep-learning methods can automate this process, they are typically evaluated in-distribution, despite clinically relevant shifts in scanner, protocol, institution, population, and imaging …
- <a id="20260916-2609.17065"></a>**Beyond "ChatGPT Can Make Mistakes": Designing Interventions to Support Metacognitive Monitoring in AI-Assisted Work** — [2609.17065](https://arxiv.org/abs/2609.17065) | cross: cs.AI  
  Manuel A. D. Santos, Paul Thiesse, Steeven Villa, Daniela Fernandes et al.  
  AI assistance places a metacognitive demand on users, who must judge their own competence and the system's. Yet designers lack comparative evidence on which interventions to choose, where to place them, and how to tell whether they worked.
- <a id="20260916-2609.17064"></a>**Neuro-Symbolic Hierarchical Intention Anticipation in Human Behavior** — [2609.17064](https://arxiv.org/abs/2609.17064) | cross: cs.CV, cs.HC, cs.LG, cs.NE  
  Farnaz Soleimani, Abdelghani Chibani, Yacine Amirat, Ghazaleh Khodabandelou  
  Assistive autonomous systems must anticipate human goals before an observed behavior is complete. This article formulates anticipation as goal inference from a partially observed multimodal episode together with structured prediction of the remaining behavior, rather than exact motor forecasting.
- <a id="20260916-2609.17043"></a>**Diagnosing the Fact-Grounding Gap in Multi-Hop Question Answering** — [2609.17043](https://arxiv.org/abs/2609.17043) | cross: cs.AI, cs.IR  
  Kevin Mo, Nathan Mo, Richard Zhu  
  Multi-hop question answering requires combining information from multiple documents to answer complex questions. These systems have grown increasingly capable, yet when they fail, the error is typically attributed to not finding the right documents.
- <a id="20260916-2609.17040"></a>**Sparse MLLM Anchors, Dense Adaptation: Breaking the Self-Referential Loop in Wild Test-Time Adaptation** — [2609.17040](https://arxiv.org/abs/2609.17040)  
  Zhenbin Wang, Lei Zhang, Lituan Wang, Yan Wang et al.  
  Wild test-time adaptation (WTTA) updates a source model online under small test batches, concurrent distribution shifts, and time-varying class imbalance. Most WTTA methods derive their adaptation signals, including predictive uncertainty, sample reliability, and local feature geometry, from the model being adapted.
- <a id="20260916-2609.17019"></a>**SKIP: a Self-knowledge-guided Step-wise Preference Learning Framework for Concise Reasoning** — [2609.17019](https://arxiv.org/abs/2609.17019)  
  Qinhong Lin, Yuhao Zhang, Yinglun Feng, Zhongliang Yang et al.  
  While Chain-of-Thought (CoT) reasoning has been proven to be effective, it often leads to overthinking, resulting in computational overhead, inference latency, and even degraded performance in large language models (LLMs). Existing concise reasoning frameworks significantly compromise accuracy while compressing the length of output.
- <a id="20260916-2609.17012"></a>**ORDER: Task-Conditioned Routing for Retrieval-Augmented Generation** — [2609.17012](https://arxiv.org/abs/2609.17012)  
  Aurélien Pellet, Julien Perez, Marie Puren  
  Retrieval-Augmented Generation (RAG) pipelines typically rely on a fixed indexing and retrieval configuration determined at preprocessing time. This one-size-fits-all design is ill-suited to domain-expert settings, where heterogeneous queries require different chunking granularities, metadata constraints, and source-selection strategies.
- <a id="20260916-2609.17010"></a>**ThinkFlow: Self-Evolving Probabilistic Latent Memory for Lifelong Conversational Agents** — [2609.17010](https://arxiv.org/abs/2609.17010) | cross: cs.CL  
  Cai Ke, Xin Liu, Han Zhang, Jiangyue Yan et al.  
  Lifelong conversational agents rely on memory systems to maintain deep, context-aware interactions with users. However, existing explicit textual memory pipelines suffer from a severe information bottleneck, often losing subtle behavioral patterns and emotional shifts.
- <a id="20260916-2609.17008"></a>**FlexEE: Self-Speculative and KV-Compatible Early Exiting for Offloading-Aware LLM Inference** — [2609.17008](https://arxiv.org/abs/2609.17008)  
  Qihu Xie, Ziwei Li, Yi Kang  
  Large language model (LLM) inference is often constrained by both computation and memory, especially in offloading-based deployments where model weights are transferred across memory hierarchies during autoregressive decoding. In this setting, reducing the number of executed layers can lower per-token latency while also avoiding costly weight movement.
- <a id="20260916-2609.16993"></a>**The Role of Implicit and Explicit Demographic Signals in Large Language Model-based Student Assessment** — [2609.16993](https://arxiv.org/abs/2609.16993) | cross: cs.AI, cs.CY  
  Donya Rooein, Luca Benedetto, Dirk Hovy  
  Large Language Models are now common in student assessment, but we know little about how student demographics affect their use. Sometimes, considering student demographics may be necessary -- for example, to improve readability for users with lower educational levels.
- <a id="20260916-2609.16962"></a>**Affect-Prototype Guided Fusion for Open-Vocabulary Incomplete Multi-modal Emotion Recognition** — [2609.16962](https://arxiv.org/abs/2609.16962)  
  Yichi Zhang, Shenyue Wang, Jing Luo, Chunyang Yu et al.  
  Open-vocabulary multimodal emotion recognition (OV-MER) aims to generate open natural-language emotion labels from multimodal affective cues. In real-world scenarios, however, complete and synchronized modal data are difficult to obtain due to limitations of acquisition devices and user privacy constraints.
- <a id="20260916-2609.16948"></a>**AntennaFlow: A Generative Flow Model for Offset Correction in Phaseless Antenna Testing** — [2609.16948](https://arxiv.org/abs/2609.16948) | cross: cs.IT  
  Yongzhi Li, Chongting Shen, Menglin Chen, Xun Jiang et al.  
  Near-field to far-field transformation is central to large-aperture antenna testing, yet two coupled challenges remain: costly phase acquisition at millimeter-wave bands and violations of the centering assumption under offset mounting. Existing methods address these issues separately, requiring either dense full-field data or offset vectors.
- <a id="20260916-2609.16947"></a>**AeroLat: Channel-Aware Latent Space Semantic Communication for Decentralized UAV Swarms** — [2609.16947](https://arxiv.org/abs/2609.16947) | cross: cs.AI  
  Rajdeep Ghosh, Goparaju Venkata Seshachala Sree Vatsava, Sudip Misra  
  Communication in latent space offers an intriguing alternative to symbolic messages for decentralized autonomous Unmanned Aerial Vehicle (UAV) swarms operating over bandwidth-constrained, time-varying wireless links. However, when homogeneous frozen models are prompted with discretized perceptual inputs, their broadcast states collapse toward the shared prompt template.
- <a id="20260916-2609.16931"></a>**Causal Discovery via Transformed Low-Rank Quantile Surfaces** — [2609.16931](https://arxiv.org/abs/2609.16931) | cross: cs.AI, cs.LG, stat.ML  
  Ryo Kamimura, Thong Pham  
  We propose Low-Rank Quantile Surfaces (LRQS), a bivariate causal model in which, in the causal direction, an unknown monotone transformation of the conditional quantile surface admits a low-rank functional decomposition. LRQS subsumes location-scale noise models and post-nonlinear heteroscedastic noise models, while allowing multiple quantile bases to represent changes beyond location-scale …
- <a id="20260916-2609.16887"></a>**QART: A Quantum-Classical Hybrid Architecture for Long-Horizon Reasoning -- Exploring a Conditional Path toward Quantum Scaling** — [2609.16887](https://arxiv.org/abs/2609.16887)  
  Lehao Lin, Yuheng Cheng, Guolong Liu, Yao Li et al.  
  Long-horizon reasoning is vulnerable to early errors that compromise later decisions. We present QART, the Quantum-Augmented Reasoning Transformer, a quantum--classical hybrid architecture combining a backbone language model with quantum encoding, CIM-based QUBO optimization, and quantum decoding.
- <a id="20260916-2609.16884"></a>**Bridging Learned Visual Perception and Symbolic Belief-Space Planning** — [2609.16884](https://arxiv.org/abs/2609.16884) | cross: cs.RO  
  Guy Azran, Michael Navat, Sarah Keren  
  In partially observable settings, agents must act without full knowledge of the world state and rely on uncertain state-estimation pipelines. Obtaining grounded and verifiable symbolic plans under such uncertainty remains a key challenge.
- <a id="20260916-2609.16878"></a>**VOR-Bench: A Human Perception-Driven Benchmark for Video Object Removal** — [2609.16878](https://arxiv.org/abs/2609.16878) | cross: cs.AI  
  Haonan Huang, Tianrui Qiu, Xianghao Zang, Yinan Du et al.  
  Despite its crucial role in video object removal (VOR), existing evaluation paradigms face two critical limitations: questionable references and a misalignment between tradi- tional metrics and human preference. To address these challenges, we introduce VOR- Bench, which advances VOR evaluation through three integrated components.
- <a id="20260916-2609.16856"></a>**The Evolution of Coordination in a Collective Intelligence System: 25 Years of English Wikipedia and the Emergence of Generative AI** — [2609.16856](https://arxiv.org/abs/2609.16856) | cross: cs.AI, cs.SI  
  Neal Reeves, Maja Świeczkowska, Amy Rechkemmer, Elena Simperl  
  English Wikipedia is one of the largest examples of collective intelligence on the Web, sustained not only by article production but also by volunteer coordination and governance. While prior research has examined coordination work in Wikipedia, less attention has been paid to how participation in these spaces has evolved over time.
- <a id="20260916-2609.16852"></a>**CoAdapt: An LLM-based Framework for Adaptive Collaborative Perception in IIoT Robotic Swarms** — [2609.16852](https://arxiv.org/abs/2609.16852) | cross: cs.RO  
  Houssam Hajj Hassan, Antonia Maria Masucci, Lynda Zitoune, Salah-Eddine Elayoubi  
  Industrial IoT environments increasingly deploy autonomous mobile robots for tasks such as material handling, product assembly, or infrastructure inspection. In such deployments, collaborative perception enables robots to share LiDAR observations and collectively construct a richer model of their environment than an individual agent could produce alone.
- <a id="20260916-2609.16847"></a>**RegRet: Enhancing Region-Level Retrieval in Large Multimodal Models** — [2609.16847](https://arxiv.org/abs/2609.16847) | cross: cs.AI, cs.IR  
  Xun Liang, Honghui Yang, Weihang Pan, Ruisi Zhao et al.  
  Region-level retrieval aims to align user-specified image regions with relevant regions or textual descriptions, playing a crucial role in realworld applications such as e-commerce product search and RAG. Although recent Large Multimodal Models (LMMs) have made significant strides in multimodal retrieval, they primarily focus on global-level tasks and struggle to capture effective region-level …
- <a id="20260916-2609.16841"></a>**StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection** — [2609.16841](https://arxiv.org/abs/2609.16841) | cross: cs.AI  
  Zhenbin Wang, Lei Zhang, Lituan Wang, Wei Huang et al.  
  Increasing image resolution produces ever-longer visual-token sequences in vision-language models (VLMs), substantially raising their inference cost. To reduce this overhead without retraining, existing methods select compact token subsets that prioritize query relevance, visual coverage, or a fixed trade-off between them.
- <a id="20260916-2609.16832"></a>**What Breaks Local Watermarks? A Robustness Benchmark for Local Invisible Image Watermarking** — [2609.16832](https://arxiv.org/abs/2609.16832) | cross: cs.AI, cs.CR  
  Kai Yao, Bence Szilágyi, Sebestyén Kamp, Máté Poór et al.  
  Local image watermarking embeds an invisible signal into selected image regions rather than spreading it across the entire image, enabling payload recovery from specific objects or regions without perceptibly altering the image. Existing studies evaluate the robustness of payload recovery and localization under image transformations, but they often focus on their own proposed method, resulting in …
- <a id="20260916-2609.16822"></a>**Execution Flexibility in Automated Planning: A Comparative Evaluation of Deordering and Reordering Strategies** — [2609.16822](https://arxiv.org/abs/2609.16822)  
  Md. Monjurul Islam, Sabah Binte Noor, Fazlul Hasan Siddiqui, Gahangir Hossain  
  This study covers foundational concepts for enhancing plan-execution flexibility, including partial-order planning, the producer-consumer-threat formalism, and a range of deordering and reordering strategies. Creating a partial-order plan from a sequential one by removing unnecessary ordering constraints is a practical way to improve execution flexibility, and several methods have been proposed …
- <a id="20260916-2609.16814"></a>**Can We Do Interpretable NLI with Graphs Based on Atomic Propositions?** — [2609.16814](https://arxiv.org/abs/2609.16814) | cross: cs.IR  
  Younes Boufouss, Luc Pommeret, Thomas Gerald, Patrick Paroubek et al.  
  While Large Language Model (LLM)-based Natural Language Inference (NLI) systems achieve high accuracy, their decision-making processes lack auditable structures. This paper explores whether NLI can be performed using only interpretable, graph-based representations of evidence.
- <a id="20260916-2609.16795"></a>**Layers, Sinks, and Scaling: Adaptive Evidence Selection for Multimodal Large Language Models** — [2609.16795](https://arxiv.org/abs/2609.16795)  
  Zhenbin Wang, Lei Zhang, Lituan Wang, Wei Huang et al.  
  Multimodal large language models (MLLMs) can answer knowledge-intensive visual questions by combining visual evidence from images with facts retrieved from external sources. However, MLLMs may overlook relevant evidence in both modalities, attending weakly to the textual sentences or visual regions needed for the correct answer.
- <a id="20260916-2609.16793"></a>**Available but Unclaimed: An Empirical Study of Human-AI Synergy** — [2609.16793](https://arxiv.org/abs/2609.16793) | cross: cs.AI  
  Robin Welsch, Michelle Rausch, Pascal Knierim, Thomas Kosch et al.  
  People increasingly reason with large language models (LLMs), yet complementary capabilities do not guarantee outperforming both components. In a between-subjects study, participants (N=535) solved a 40-item battery of matrix reasoning, mental rotation, syllogisms, and letter-string analogies, unaided or with GPT-5.6-Luna, Claude Opus 4.8, Gemini 3.6 Flash, or Kimi K3.
- <a id="20260916-2609.16779"></a>**Integrating the Analytic Hierarchy Process with Large Language Models for Transparent Multi-Criteria Decision-Making** — [2609.16779](https://arxiv.org/abs/2609.16779)  
  Han Zhiguang, Farah Benamara, Pascale Zaraté  
  LLMs are increasingly employed in a wide range of decision-making tasks. However, the opacity of their internal reasoning makes it difficult to validate or interpret their outputs, and the need for interpretability becomes especially critical in high-stakes settings.
- <a id="20260916-2609.16768"></a>**Coverage-Aware Virtual IMU Augmentation for Low-Resource Human Activity Recognition** — [2609.16768](https://arxiv.org/abs/2609.16768)  
  Jiayuan Gao, Yingwei Zhang, Ziyao Tang, Yuejia Ma et al.  
  IMU-based human activity recognition (HAR) enables continuous, privacy-friendly monitoring of daily activities using wearable sensors. However, building reliable HAR models that generalize across diverse users and real-world conditions requires large amounts of labeled IMU data, which are expensive and difficult to collect.
- <a id="20260916-2609.16760"></a>**Turn-level Multiscale Density Ratio Estimation for LLM Agents** — [2609.16760](https://arxiv.org/abs/2609.16760)  
  Zishuo Zhao, Kai Chen, Ao Li, Yuan Liu  
  With the rapid development of Large language model (LLM), agent systems enhanced by LLMs show huge potential in being able to deal with complex tasks, especially involving multi-step thinking or interaction with tools. For applying LLM techniques with a well-designed agent paradigm, post-training of LLM in multiple agent scenarios is necessary to achieve better performance.
- <a id="20260916-2609.16752"></a>**Beyond Episodic AI: Cognitive Field Networks for Biologically Inspired Persistent Cognition** — [2609.16752](https://arxiv.org/abs/2609.16752)  
  Byung Gyu Chae  
  Cognitive Field Theory (CFT) proposes that cognition arises from memory-dressed collective dynamics that generate a persistent macroscopic cognitive field. Here we develop a Cognitive Field Network (CFN), a recurrent Transformer in which the organized hidden field re-enters subsequent inference through \[ Φ_{n+1}=F_θ(X_{n+1},Φ_n).
- <a id="20260916-2609.16737"></a>**Seeing What Matters: Visual Cue Guided Video Planning for Generalizable Robot Navigation** — [2609.16737](https://arxiv.org/abs/2609.16737) | cross: cs.AI, cs.CV, cs.LG  
  Hojin Lee, Sizhe Lester Li, Maximilian Hilger, Susie Lu et al.  
  Generative video models can serve as a promising backbone for robot navigation by predicting future observations as video plans. Recent approaches often condition video planning on short-horizon guidance and recover geometric waypoints through scene reconstruction, leaving longer-horizon planning and precise video-to-action translation less explored.
- <a id="20260916-2609.16730"></a>**LSREP: A Longitudinal State-Replay Protocol for Evaluating Conversational Memory, with ICE v2 as an Audited Local-First Architecture** — [2609.16730](https://arxiv.org/abs/2609.16730) | cross: cs.CL, cs.IR  
  Deepesh Sonar  
  Conversational memory changes during use, so endpoint question answering alone cannot establish how a persistent state accumulates, ages, or incorporates revisions. We introduce LSREP, a Longitudinal State-Replay Evaluation Protocol combining ordered replay, explicit lifecycle schedules, repeated probes, evolving reference answers, and mechanism-fidelity checks.
- <a id="20260916-2609.16722"></a>**VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs** — [2609.16722](https://arxiv.org/abs/2609.16722) | cross: cs.CL, cs.CV, cs.MM  
  Haoyu Guo, Yuan Feng, Junlin Lv, Mingjun Xiao et al.  
  Scaling Multimodal Large Language Models (MLLMs) to long-form video understanding is bottlenecked by the explosion of visual tokens, which saturates context windows and incurs prohibitive costs. Current solutions predominantly rely on auxiliary models for token reduction but face a fundamental dilemma: lightweight encoder-driven approaches often overlook critical semantic information, whereas …
- <a id="20260916-2609.16697"></a>**World Models for Embodied Intelligence: From Plausible to Controllable to Actionable** — [2609.16697](https://arxiv.org/abs/2609.16697) | cross: cs.AI  
  Nanjie Yao, Hao Wang, Chong Cheng, Zhikang Chen et al.  
  World models connect perception and decision-making in embodied intelligence by maintaining hidden state, anticipating consequences, comparing interventions, and adapting when execution departs from expectations. Although progress is often measured by visual fidelity, their value lies in improving behavior.
- <a id="20260916-2609.16683"></a>**Weave: Learning Whole-Body Dexterous Loco-Manipulation from Human-Object Interactions** — [2609.16683](https://arxiv.org/abs/2609.16683) | cross: cs.AI, cs.LG  
  Liu Cao, Xingze Wu, Jingzhi Cui, Botian Xu et al.  
  Learning humanoid-object interaction requires coordinating whole-body balance, locomotion, and dexterous hand contact to control both robot and object motion. Human demonstrations provide examples of coordinated interaction, but transferring these behaviors to humanoid robots requires learning how to establish and maintain effective contacts under different embodiments and dynamics.
- <a id="20260916-2609.16680"></a>**little m: An AI Agent for Industrial Process Optimization** — [2609.16680](https://arxiv.org/abs/2609.16680)  
  Yongchao Ye, Xinyu He, Dutliff Boshoff, Way Kuo et al.  
  Manufacturing consumes one third of global energy and still has significant room for improvement in terms of energy efficiency. Optimal process control is essential for this purpose.
- <a id="20260916-2609.16679"></a>**AI for Games in the Foundation Model Era** — [2609.16679](https://arxiv.org/abs/2609.16679)  
  Meng Luo, Yanlin Li, Hao Li, Hongzhan Lin et al.  
  Foundation models, alongside advances in learned game-world models, are reshaping AI across the game lifecycle. Beyond playing games, recent systems model players and game dynamics, support design and development, adapt player-facing experiences at runtime, and evaluate resulting artifacts.
- <a id="20260916-2609.16667"></a>**ANIMASK: What the Model Contributes to Role Play in Simulated Story Worlds** — [2609.16667](https://arxiv.org/abs/2609.16667)  
  Xiucheng Zhang, Zhuoning Xu, Hanjun Luo, Yankai Chen et al.  
  When a language model plays a character, the observed behavior reflects both the assigned persona and the default dispositions of the actor model itself. Existing evaluations test persona fidelity or model defaults in isolation, but neither says, at a specific choice with consequences, what the persona changed and what the model's default kept.
- <a id="20260916-2609.16639"></a>**ReDraft, Don't Just Distill: Reference-Driven Revision for Continual VLLM Post-Training** — [2609.16639](https://arxiv.org/abs/2609.16639)  
  Zhihao Zhang, Mingqi Wu, Qiaole Dong, Enyu Zhou et al.  
  Continual post-training of large multimodal models should add new capabilities while preserving those from pre-training, and the two goals pull in opposite directions. SFT gives explicit target supervision that learns a task from near-zero accuracy, but its off-policy targets move the model far enough to cause forgetting; on-policy methods such as RLVR and self-distillation preserve policy …
- <a id="20260916-2609.16635"></a>**EchoPath: Execution-Level Replayable Memory for GUI Agents** — [2609.16635](https://arxiv.org/abs/2609.16635)  
  Yao Zhao, Aditya Shanmugham, Swastik Roy, Yanxun Xu  
  Computer-use agents increasingly operate browsers, software, and desktop applications via CLI or API portals, but graphical user interface (GUI) still plays an important role in common industrial production scenarios. GUI agents commonly employ fresh observe-plan-ground-act loops, which is inefficient for enterprise tasks that repeatedly update records, process forms, configure tools, and export …
- <a id="20260916-2609.16625"></a>**AURA: Agentic Diagnosis and Refinement for Production Recommender Systems at Scale** — [2609.16625](https://arxiv.org/abs/2609.16625) | cross: cs.AI, cs.LG  
  SungGeun Kim, Abhinav Narain, Daniel Nemirovsky  
  How and why does a recommender system fail the users it serves? Oftentimes, practitioners are left to improve their algorithms based on a combination of feedback from stakeholder teams, domain expertise, and insights from data analyses.
- <a id="20260916-2609.16614"></a>**RoleBreak: Benchmarking Long-Horizon Role-Playing Robustness in Spoken Dialogue** — [2609.16614](https://arxiv.org/abs/2609.16614) | cross: cs.AI  
  Yuqi Wang, Fengyuan Liu, Haochen Luo, Zhiqi Yu et al.  
  Speech-to-speech dialogue models increasingly support persona control, yet existing spoken role-playing benchmarks remain largely character-centric and short-horizon. This leaves open whether spoken dialogue models can sustain diverse roles over extended interactions, especially beyond predefined fictional characters.
- <a id="20260916-2609.16612"></a>**Structure Across Voices: Comparing acoustic-event type accumulation and sequence dependence across four vocal repertoires using frozen audio encoders** — [2609.16612](https://arxiv.org/abs/2609.16612) | cross: cs.AI  
  Mudit Sinha, Sanika Chavan  
  Vocal repertoires can differ in acoustic-event type accumulation and temporal organization, yet direct comparison is difficult because corpora use different native events and unequal amounts of sequence. We compare sperm whale codas, human speech phones, Bengalese finch syllables, and common marmoset calls using the same frozen-audio-encoder procedure while matching event count and local sequence …
- <a id="20260916-2609.16597"></a>**A Vision-Language Foundation Model for Precise and Comprehensive Brain Tumor Diagnosis from Preoperative Multimodal Data** — [2609.16597](https://arxiv.org/abs/2609.16597) | cross: cs.AI, cs.DB  
  Yinong Wang (Joyce), Jianwen Chen (Joyce), Zhou Chen (Joyce), Shuwen Kuang (Joyce) et al.  
  Background Non-invasive presurgical diagnosis of brain tumor types from Magnetic Resonance Imaging (MRI) is essential but challenging due to overlapping imaging features across tumor types, inter-observer variability, and the extensive training required for expertise. We aimed to develop an MRI-based Artificial Intelligence (AI) model for automatic and reliable brain tumor classification with …
- <a id="20260916-2609.16145"></a>**Safe Error Correction for Language Models: Frozen-Base Adjustment with Capability Preservation** — [2609.16145](https://arxiv.org/abs/2609.16145) | cross: cs.CL, cs.LG, cs.NE  
  Gautam Kishore  
  We study a practical question: can a small correction module fix errors in a frozen language model's outputs without degrading its base capabilities? We propose CRN v2, a lightweight logit-level correction module (~34M trainable parameters, 0.73% of the 4.65B text module) that sits atop a fully frozen Gemma 4 E2B model.
- <a id="20260916-2609.16163"></a>**GPEvac: GNN-Based PPO for Adaptive Evacuation Routing During Shooting Events** — [2609.16163](https://arxiv.org/abs/2609.16163) | cross: cs.CY, cs.LG, cs.MA, cs.SY, eess.SY  
  Daniel Perkins, Subhadeep Chakraborty  
  The sharp increase in mass shootings underscores an urgent need for systems that guide victims to safety in real time. An effective evacuation system must minimize threat exposure while also accounting for adversarial uncertainty and crowding dynamics.
- <a id="20260916-2609.16193"></a>**Permutation-Based Stegomalware in Large Language Models: Threats and Countermeasures** — [2609.16193](https://arxiv.org/abs/2609.16193) | cross: cs.AI, cs.LG  
  Danny Wood, James Stringer  
  The difficulty of training large language models (LLMs), together with their ubiquity, raises the threat of stegomalware, where malicious payloads are embedded into model weights. Recent work has demonstrated the use of permutation symmetry in model weights to mitigate these threats, but failed to show neutralization of stegomalware across all weights for LLMs.
- <a id="20260916-2609.16258"></a>**The AI-Enabled Scientific Frontier** — [2609.16258](https://arxiv.org/abs/2609.16258) | cross: cs.LG, cs.PF, econ.GN, q-fin.EC  
  Gabriel Manso, Emma Fu, Neil Thompson  
  As artificial intelligence's capabilities improve, it is increasingly viewed as a general scientific method. But how true are these claims?
- <a id="20260916-2609.16289"></a>**Symmetric solution of the Bellman optimality equation for repeated harmony game** — [2609.16289](https://arxiv.org/abs/2609.16289) | cross: cs.AI, cs.LG  
  Hisato Komatsu  
  In social dilemma games, additional rewards or punishments have been studied as means of promoting cooperation. Therefore, it is important to investigate the ideal situation, in which such an additional payoff would change the game.
- <a id="20260916-2609.16305"></a>**BLINDSPOT: A Benchmark for Safety and Refusal Calibration in Long-Horizon Tool-Using Agents** — [2609.16305](https://arxiv.org/abs/2609.16305) | cross: cs.CE, cs.CL, cs.LG, cs.MA  
  Sadia Asif, Mohammad Mohammadi Amiri, Momin Abbas, Tejaswini Pedapati et al.  
  Large language model (LLM) agents increasingly operate over long-horizon interactions involving tool use, persistent state, evolving authorization, and external environment feedback. In such settings, safety failures may emerge only after multiple turns, yet existing evaluations often reduce agent behavior to task or attack success, obscuring whether an agent acts, refuses, or remains …
- <a id="20260916-2609.16322"></a>**Cross-Anatomy Transfer Versus Sparse Interpolation in Digital-Twin-Oriented Aortic Fluid-Structure Interaction Surrogates** — [2609.16322](https://arxiv.org/abs/2609.16322) | cross: cs.LG  
  Ali Nourbakhsh, Mohammad Reza Niroomand, Erfan Nourbakhsh  
  Surrogate credibility for fluid-structure interac- tion (FSI) requires distinguishing transfer across independent anatomies from interpolation within an already sampled surface. Four de-identified human aortic models from the Vascular Model Repository were reconstructed into separate lumen and nominal 1.5-mm wall domains and analyzed under matched first-cycle two-way FSI.
- <a id="20260916-2609.16338"></a>**Breaking the 1.58-bit Barrier for Ternary LLMs** — [2609.16338](https://arxiv.org/abs/2609.16338) | cross: cs.LG  
  Evangelos Georganas, Alexander Heinecke, Pradeep Dubey  
  Ternary Large Language Models (LLM) store every weight as one of three symbols $\{-1,0,+1\}$, so the cost of a ternary model is conventionally referenced to the information-theoretic $\log_2 3 \approx 1.585$ bits per weight. The prevailing deployment format packs five ternary weights into one byte (five-trit packing), and due to the power-of-two group sizes used in practice this rounds up to …
- <a id="20260916-2609.16407"></a>**Balancing Trial and Reorder: A Hybrid Sequential Transformer-GBDT Ranker for On-Demand Delivery** — [2609.16407](https://arxiv.org/abs/2609.16407) | cross: cs.AI, cs.LG  
  Marcel Kurovski, Attila Nagy, Steffen Klempau, Aleksandr Fedintsev  
  On a delivery platform, personalized store ranking greatly influences what users find and order. Unlike digital-only domains, candidate stores are local and bound by real-time availability and delivery operations.
- <a id="20260916-2609.16412"></a>**On the Expressive Power of Implicit Line-Graph Higher-Order Weisfeiler--Leman** — [2609.16412](https://arxiv.org/abs/2609.16412) | cross: cs.AI, cs.LG  
  Fan Yang  
  Whitney's theorem allows isomorphism testing for connected simple graphs, apart from $K_3$ and $K_{1,3}$, to be formulated as distinguishing their line graphs. However, the relation between fixed-dimensional Weisfeiler--Leman (WL) expressivity on line graphs and on their roots remains unresolved.
- <a id="20260916-2609.16450"></a>**Early-Bird Decoding: Accelerating Diffusion LLMs with Learnable Block Sizes and Parallel Sampling** — [2609.16450](https://arxiv.org/abs/2609.16450) | cross: cs.AI, cs.LG  
  Lixuan Wei, Wei Zhou, Jianwen Wu, Yipeng Shen et al.  
  Diffusion large language models (dLLMs) offer a promising parallel decoding paradigm as an alternative to autoregressive generation through iterative unmasking. However, dLLMs typically require many steps before token confidence reaches the decoding threshold, resulting in inefficient inference even with block-wise KV caching.
- <a id="20260916-2609.16487"></a>**Skill-based Agentic Evaluation for Real-time Data Science Tasks** — [2609.16487](https://arxiv.org/abs/2609.16487) | cross: cs.LG, cs.MA  
  Aniruddha Tamhane, Raghavendra Addanki, Ayushi Aggarwal, Aditya Bansal et al.  
  We present a framework for evaluating data-science agents on live, continuously updated data using executable ground truth and format-agnostic factoid scoring. Consider this example query: "what were last week's audience sizes"---the reference answer changes as the underlying data changes, so static references become outdated and standard LLM-as-a-judge pipelines cannot verify responses against a …
- <a id="20260916-2609.16493"></a>**From Manual Construction to AI-Driven Scenario Emergence: Rethinking Catastrophe Risk Modeling** — [2609.16493](https://arxiv.org/abs/2609.16493) | cross: cs.LG  
  Hang Gao  
  Traditional catastrophe (CAT) risk models rely on costly manual construction to generate extreme weather scenarios, an approach largely unchanged since the 1990s. As climate extremes intensify, this creates mounting challenges to the entire risk transfer chain.

#### cs.LG (163)

- <a id="20260916-2609.16099"></a>**SWB-DM: A Calibrated Sliced-Wasserstein-Barycenter Aggregator with Delayed-Momentum Caching for Byzantine-Robust Federated Learning under Partial Participation** — [2609.16099](https://arxiv.org/abs/2609.16099) | cross: cs.CR, cs.DC | 🎯★ Byzantine  
  Saranraj S, Saranya M S, Alex David S, Ajay Kumar A  
  Robust aggregation methods for federated learning quietly rest on a fragile assumption: that whoever shows up in a given round is a fair sample of the full population. In practice, they rarely are.
- <a id="20260916-2609.16309"></a>**Agentic Search Spaces for Tabular Machine Learning** — [2609.16309](https://arxiv.org/abs/2609.16309) | 🎯🧐 LLM-based agent  
  Renat Sergazinov, Artem Chistyakov, Sergey Pankevich, Artem Babenko  
  Despite the rapid progress of LLM-based agents for planning, code generation, and debugging, their practical value for tabular machine learning remains underexplored. In this paper, we investigate a concrete use case: whether state-of-the-art agentic AI systems can design extended HPO search spaces for established tabular models that outperform the standard search spaces provided by the model …
- <a id="20260916-2609.16637"></a>**Can Knowledge Transfer Parameters Be Learned? LePoKet for Efficient Robotic Vision** — [2609.16637](https://arxiv.org/abs/2609.16637) | cross: cs.LG | 🎯★ Raft  
  Yanick C. Tchenko, Felix Mohr, Hicham Hadj-Abdelkader, Hedi Tabia  
  Efficient perception is central to robotic systems operating under constrained computation, memory, and latency budgets. Knowledge transfer from larger pretrained models offers a practical route to stronger compact perception networks, but existing approaches commonly rely on fixed distillation objectives or manually designed interaction mechanisms.
- <a id="20260916-2609.16917"></a>**Multi-Agent Learning with Cooperation-Driven Optimization Dynamics** — [2609.16917](https://arxiv.org/abs/2609.16917) | cross: cs.LG | 🎯★ consensus  
  Jarod Ketcha Kouakep, Sreyvi UANN, Timoteo Carletti  
  Multilayer Artificial Neural Networks trained via backpropagation are the basic blocks of many, more complex, classification algorithms. Their strength lies in the possibility of realizing, with arbitrary precision, any function.
- <a id="20260916-2609.17138"></a>**From Foundation Embeddings to Cropland Maps: Label Efficiency, Temporal Transferability and Independent Human Validation** — [2609.17138](https://arxiv.org/abs/2609.17138) | cross: cs.LG, eess.IV | 🎯★ consensus  
  Mohammad Ammar Mughees, Giovanni Montefoschi, Zhongxin Chen, Maria Antonia Brovelli  
  Geospatial foundation models provide reusable representations of satellite imagery that support downstream mapping with limited task-specific modelling. We evaluate whether annual AlphaEarth embeddings support binary cultivated-versus-non-cultivated mapping in Maine, USA, using 192 spatially separated patches and labels derived from the USDA Cropland Data Layer (CDL).
- <a id="20260916-2609.17499"></a>**ENCP: Episode-Normalized Conformal Prediction for Vision-and-Language Navigation** — [2609.17499](https://arxiv.org/abs/2609.17499) | cross: cs.AI, cs.RO  
  Vicky Feliren, A. Taufiq Asyhari, Muhamad Risqi U. Saputra  
  Uncertainty estimation for Vision-Language-Navigation (VLN) models is a critical task since it can help identify ambiguous and unreliable predictions, enabling agents to make safer navigation decisions. As one of the most advanced uncertainty estimation frameworks, conformal prediction (CP) offers a promising approach for uncertainty estimation in VLN.
- <a id="20260916-2609.17474"></a>**Coupled Calibration and Learning: Mitigating Teacher Bias in LLM Distillation without Target-Domain Reward Feedback** — [2609.17474](https://arxiv.org/abs/2609.17474) | cross: cs.AI, math.ST, stat.ML  
  Haichen Hu, Yuheng Zhang, David Simchi-Levi  
  Large language model (LLM) distillation aims to transfer the capabilities of a powerful teacher to a smaller student. Direct imitation, however, can also transfer the teacher's systematic bias and errors.
- <a id="20260916-2609.17429"></a>**Learning-Guided Planning in Large Dynamic Action Spaces: Budgeted Tree Search for One-to-Many Mobile Charging** — [2609.17429](https://arxiv.org/abs/2609.17429) | cross: cs.AI  
  Liang-Ching Tao, Pi-Chung Wang  
  Many learned sequential decision systems map the current state directly to an action. That shortcut becomes brittle when candidate actions are numerous, geometrically structured, and rebuilt with the state.
- <a id="20260916-2609.17226"></a>**Easy to Catch a Liar, Hard to Clear an Honest One: Language Models Diagnosing a Corrupted Reward Channel from a Verified Record** — [2609.17226](https://arxiv.org/abs/2609.17226) | cross: cs.AI, cs.CL  
  Arman Nik Khah  
  An agent that learns from rewards has to trust whatever reports those rewards. When the reports suddenly change, either the world changed or the reporter broke.
- <a id="20260916-2609.17171"></a>**A unified framework for global and local interpretability using adaptive derivative-ordered random explanation** — [2609.17171](https://arxiv.org/abs/2609.17171) | cross: cs.AI  
  Lemen Chao, Ming Lei, Anran Fanga  
  The interpretability of complex machine learning models is of paramount importance, especially in real-world high-stakes domains such as healthcare and finance. However, existing post-hoc interpretability methods suffer from inherent limitations: fragmented analytical processes, inadequate capacity to model nonlinear feature interactions, computational inefficiencies, and over-reliance on …
- <a id="20260916-2609.17061"></a>**Repurposing Unified Topological Signatures for Graph Representation Learning** — [2609.17061](https://arxiv.org/abs/2609.17061) | cross: cs.AI  
  Sanyam Sanjay Jain, Anshika Krishnatray, Aditya Sharma, Vinti Agarwal  
  Message-passing Graph Neural Networks (GNNs) iteratively propagate and aggregate local neighborhood information followed by global readout to learn graph representations. However, their discriminative power is upper-bounded by the Weisfeiler--Lehman (1-WL) graph isomorphism test.
- <a id="20260916-2609.17029"></a>**Distributed JEPA: A Self-Supervised Framework for Energy Forecasting** — [2609.17029](https://arxiv.org/abs/2609.17029) | cross: cs.AI  
  Liana Toderean, Tudor Cioara, Vasilis Michalakopoulos, Efstathios Sarantinopoulos et al.  
  Traditional energy forecasting solutions rely on task-specific supervision and energy asset representations, limiting transferability and the ability to capture general temporal dynamics across heterogeneous assets. We address this by proposing a distributed Joint Embedding Predictive Architecture (JEPA) for self-supervised learning from heterogeneous energy time-series.
- <a id="20260916-2609.16937"></a>**Beyond Token-Local Imitation: Reward-Compatible Temporal Credit Assignment for On-Policy Distillation** — [2609.16937](https://arxiv.org/abs/2609.16937) | cross: cs.AI, cs.PL  
  Shiqi Liu, Zeyu He, Letian Tao, Guojian Zhan et al.  
  On-policy distillation (OPD) has emerged as an effective approach for large language model post-training, yet existing objectives face a trade-off between objective fidelity and optimization stability. Token-level OPD provides stable but local supervision, whereas sequence-level OPD captures future credit at the cost of horizon-dependent variance.
- <a id="20260916-2609.16933"></a>**When Confidence Signals Disagree: Local and Global Confidence in Autoregressive Language Models** — [2609.16933](https://arxiv.org/abs/2609.16933) | cross: cs.AI  
  Julio C. Amador Diaz Lopez  
  Modern predictive systems expose multiple quantities that are commonly interpreted as measures of confidence. However, these quantities can summarize different aspects of the predictive process.
- <a id="20260916-2609.16930"></a>**Repurposing Deep Limit Order Book Forecasting for Scenario-Conditioned Market Impact Modeling** — [2609.16930](https://arxiv.org/abs/2609.16930) | cross: cs.AI  
  Eljas Linna, Kestutis Baltakys, Derrick Manoharan, Alexandros Iosifidis et al.  
  Deep Limit Order Book forecasting models capture nonlinear market dynamics, but their ability to quantify the effects of counterfactual order book messages has not been systematically validated. We introduce a model-agnostic framework that compares a trained forecaster's predictive distributions before and after injecting mechanically valid counterfactual messages, defining short-horizon …
- <a id="20260916-2609.16927"></a>**Verbalizing Subliminal Learning Effects Using Text Optimization** — [2609.16927](https://arxiv.org/abs/2609.16927) | cross: cs.AI, cs.CL  
  Nathan Hu, Sanmi Koyejo, Christopher Potts  
  Subliminal learning is a phenomenon in which a distillation dataset transmits traits from the teacher model that are not legibly encoded in the dataset itself. This introduces a new challenge for model development and creates new risks from data poisoning.
- <a id="20260916-2609.16804"></a>**SOTER: A Generative Time-Series Foundation Model for Wearable Human Physiological Signals** — [2609.16804](https://arxiv.org/abs/2609.16804) | cross: cs.AI  
  Fangke Chen, Sirry Chen, Wei Chen, Zhongyu Wei  
  Time-series foundation models have demonstrated strong cross-domain transfer, yet their common architectural assumptions remain poorly aligned with wearable physiological signals, which are multichannel, irregularly sampled, noisy, and governed by coupled continuous-time dynamics spanning distinct spectral scales. We present SOTER, a generative foundation model for wearable physiological time …
- <a id="20260916-2609.16754"></a>**TAME: Token Attribution and Masking for Emergent misalignment** — [2609.16754](https://arxiv.org/abs/2609.16754) | cross: cs.AI, cs.CL  
  Md Rayhanul Masud, Md Rizwan Parvez  
  Fine-tuning an aligned language model on narrow, flawed data can induce harmful behavior far outside the training domain, known as emergent misalignment (EM). Prior work has localized EM in model weights, activations, and training documents, but it remains unclear which training tokens carry the relevant fine-tuning signal.
- <a id="20260916-2609.16710"></a>**Continuous-Time Machine Learning: A Unified Mathematical Perspective** — [2609.16710](https://arxiv.org/abs/2609.16710) | cross: cs.AI  
  Waleed Razzaq, Yun-Sheng Zhao, Yun-Bo Zhao  
  Continuous-time (CT) machine learning has emerged as a principled framework for modeling temporal dynamics as a continuous process, particularly when observations are sampled at arbitrary time points or span long-range horizons. However, major branches of CT machine learning have matured in separate research communities, leaving their mathematical relationships and design trade-offs …
- <a id="20260916-2609.16665"></a>**Right Direction, Wrong Step: Geometric Analysis of Finite-Step Failure in Looped Transformers** — [2609.16665](https://arxiv.org/abs/2609.16665) | cross: cs.AI  
  Zhihao Guo, Zonghan Wu, Haizhou Du, Huan Huo et al.  
  Looped Transformers offer a parameter-efficient route to test-time scaling by reusing shared layers for iterative latent reasoning. However, additional iterations can reduce support for a reference answer, leaving unclear whether an update's direction is locally unhelpful or its full displacement moves too far.
- <a id="20260916-2609.16977"></a>**Structural Negative Transfer in Federated Graph Neural Networks: Diagnosis, Causal Investigation, and the Limits of Divergence-Aware Mitigation** — [2609.16977](https://arxiv.org/abs/2609.16977) | cross: cs.DC  
  Chethana Prasad Kabgere, Shylaja SS  
  Federated learning lets multiple participants train a shared model without pooling raw data, by exchanging locally trained model updates instead. Federated averaging assumes that averaging local models is a reasonable way to solve one shared problem when participants' data are broadly similar.
- <a id="20260916-2609.16054"></a>**Causal neural set filtering for online multi-target tracking** — [2609.16054](https://arxiv.org/abs/2609.16054) | cross: cs.AI  
  Zhongdi Liu, Huangyu Dai  
  Transformer-based multi-target tracking (MTT) jointly learns data association and state estimation, but MT3/Track-MT3-style trackers repeatedly re-encode measurement windows, incurring redundant computation. We propose Causal Neural Set Filtering (CNSF)\footnote{\href{https://github.com/daihuangyu/CNSF}{Code: https://github.com/daihuangyu/CNSF}}, a neural set filter that encodes only current …
- <a id="20260916-2609.16056"></a>**Managing Action Preconditions in Neuro-Symbolic RL: Three Placement Strategies for Embodied Agents** — [2609.16056](https://arxiv.org/abs/2609.16056) | cross: cs.AI  
  Norbert Oswald, Fabian Deuser, Thomas Br\"aunl  
  Humans carry behaviour knowledge of how to act in familiar situations into every new task rather than relearning it from scratch. There is no reason a Reinforcement Learning (RL) agent shouldn't do the same: known behaviour patterns need not be learned, only applied.
- <a id="20260916-2609.16057"></a>**OmniHarness: Harnessing Generalizable Visual Generation via Symbolic Policy Learning** — [2609.16057](https://arxiv.org/abs/2609.16057) | cross: cs.AI  
  Xu Xu (Beihang University), Jinxiu Liu (The Chinese University of Hong Kong), Zhangbo Qiao (Beihang University), Jiaxing Lu (Beihang University) et al.  
  Unified multimodal large language models (MLLMs) and multi-agent systems have advanced visual generation. However, three limitations remain.
- <a id="20260916-2609.16058"></a>**Driver Behavior Estimation at Signalized Intersections Using a Physics-Constrained Decision-Conditioned Autoregressive Transformer** — [2609.16058](https://arxiv.org/abs/2609.16058) | cross: cs.AI, cs.CY, cs.SY, eess.SY  
  Mohammad Khoshkdahan, Pavel Laskov, Alexey Vinel  
  Red-light violations and harsh braking at signalized intersections are major contributors to traffic accidents. This paper analyzes and predicts human driver decision-making and longitudinal trajectory behavior during traffic light signal transitions.
- <a id="20260916-2609.16060"></a>**HintMiner: Automatic Question Hints Mining From Q&A Web Posts with Language Model via Self-Supervised Learning** — [2609.16060](https://arxiv.org/abs/2609.16060) | cross: cs.AI, cs.CL  
  Zhenyu Zhang, JiuDong Yang  
  Users often need ask questions and seek answers online. The Question - Answering (QA) forums such as Stack Overflow cannot always respond to the questions timely and properly.
- <a id="20260916-2609.16061"></a>**POSPAN: Position-Constrained Span Masking for Language Model Pre-training** — [2609.16061](https://arxiv.org/abs/2609.16061) | cross: cs.AI, cs.CL  
  Zhenyu Zhang, Lei Shen, Yuming Zhao, Meng Chen et al.  
  Span-level masked language modeling (MLM) has shown to be advantageous to pre-trained language models over the original single-token MLM, as entities/phrases and their dependencies are critical to language understanding. Previous works only consider span length with some discrete distributions, while the dependencies among spans are ignored, i.e., assuming that the positions of masked spans are …
- <a id="20260916-2609.16063"></a>**Signed p-adic Residual Encodings of Finite-Domain All-Different Systems with a Sudoku Case Study** — [2609.16063](https://arxiv.org/abs/2609.16063)  
  Greg Baker  
  We study signed, weighted affine $p$-adic residual objectives as native encodings of finite-domain constraints. For primes that separate the finite alphabet, sufficiently weighted positive unary rows pin each coefficient to its allowed set, while negative rows reward unequal endpoints or clause satisfaction.
- <a id="20260916-2609.16065"></a>**You Don't Need To Train: Agentic Heuristic Learning Studio for Executable Human Activity Recognition** — [2609.16065](https://arxiv.org/abs/2609.16065) | cross: cs.AI  
  Siyu Yuan, He Zhang, Sizhen Bian, Bin Guo  
  Human activity recognition (HAR) is usually framed as gradient-based training of neural networks. Agentic Heuristic Learning (AHL) Studio explores a complementary view inspired by human cognitive learning: people learn activities by remembering examples, forming rules, and repairing mistakes, not by backpropagating.
- <a id="20260916-2609.16066"></a>**A panoramic aerodynamic performance prediction method for turbomachinery cascades using transformer-enhanced neural operator** — [2609.16066](https://arxiv.org/abs/2609.16066) | cross: physics.comp-ph, physics.flu-dyn  
  Qineng Wang, Zhendong Guo, Liming Song, Tianyuan Liu  
  To enable flexible and rapid aerodynamic performance evaluation in turbomachinery design, this paper proposes a panoramic performance prediction framework. Unlike most previous prediction models that directly predict the objective functions of interest, our approach first predicts the basic parameters of the Navier-Stokes equations, such as temperature, pressure, and density.
- <a id="20260916-2609.16067"></a>**A Dynamic Aggregation Strategy Enhanced Efficient Global Optimization Algorithm for Solving High-Dimensional Turbomachinery Design Problems** — [2609.16067](https://arxiv.org/abs/2609.16067) | cross: cs.CE  
  Qineng Wang, Zhendong Guo, Yun Chen, Guangjian Ma et al.  
  In order to solve the high-dimensional ($d \geq 30$) expensive black-box problems within budget, an efficient global optimization (EGO) algorithm with a dynamic aggregation strategy is proposed, labeled as DA-EGO. Specifically, the DA-EGO decomposes the original high-dimensional design space into a set of low-dimensional subspaces for efficient surrogate-based optimization search, and the optimal …
- <a id="20260916-2609.16069"></a>**Beyond Distribution Matching: Semantics-Consistent Tabular Diffusion with Weak Semantic Priors** — [2609.16069](https://arxiv.org/abs/2609.16069) | cross: cs.AI  
  Yili Wang, Ruxue Shi, Mengnan Du, Hangting Ye et al.  
  Synthetic tabular data can match real data distributions while still violating the semantic constraints that govern valid tabular rows. This reveals a key limitation of existing tabular generators: they mainly optimize distributional fidelity, but do not explicitly model weak semantic priors encoded in tabular schema and textual descriptions.
- <a id="20260916-2609.16071"></a>**Schema-Adaptive Action-Conditioned JEPA for Cross-Machine CNC Transfer under Partial Sensor Overlap** — [2609.16071](https://arxiv.org/abs/2609.16071) | cross: cs.AI  
  Ayoub Louaye Bouaziz, Matthieu Ostertag, Anton Demasles  
  Cross-machine deployment of industrial world models requires transfer across changes in dynamics, sensing interfaces, sampling regimes, and control units. We study a schema-adaptive action-conditioned Joint-Embedding Predictive Architecture (SAAC-JEPA) for CNC dynamics, where the source machine has 17 canonical sensor channels and the target shares only 10.
- <a id="20260916-2609.16077"></a>**Pseudo-Label Augmentation for Affect Sensing in Small Collaborative Groups** — [2609.16077](https://arxiv.org/abs/2609.16077) | cross: cs.AI, cs.HC  
  Meisam Jamshidi Seikavandi, Tanya Ignatenko, Fabricio Batista Narcizo, Paolo Burelli et al.  
  Physiological affect sensing in naturalistic group interaction is often limited by sparse labels rather than sensor data: wearable devices produce many time windows, while self-reports are collected only a few times per session. Using GroupAffect-4, a four-person collaborative dataset with wearable physiology, eye tracking, Big Five personality, and post-task VAD labels, we study pseudo-label …
- <a id="20260916-2609.16091"></a>**Distilling Foundation Models for Agentic What-If Reasoning:Cost, Latency, and Governance in a Hybrid LLM+SLM Architecture** — [2609.16091](https://arxiv.org/abs/2609.16091)  
  Sourish Dey, Aditya Kumar  
  Tabular foundation models deliver strong zero-training predictive performance via in-context learning, but their high inference latency makes them impractical as hot-path decision backends in interactive agentic loops. We distill a TabPFN teacher into a compact feed-forward student across a business-decision simulation on UCI Adult and five OpenML benchmarks: the classification head compresses …
- <a id="20260916-2609.16093"></a>**Evaluating Open-Weight E-Commerce Agents with Environment-Grounded Verification** — [2609.16093](https://arxiv.org/abs/2609.16093)  
  Nimit Shah, Haitz S\'aez de Oc\'ariz Borde  
  A shopping conversation has many routes to the same cart, and a task-success rate reduces all of them to one score. We build a deterministic and reproducible e-commerce environment that precommits each trial's customer and trajectory parameters, including the persona, difficulty, target cart, and an item reveal schedule.
- <a id="20260916-2609.16102"></a>**A Decision-Support Audit Protocol for Supervision Drift in Proxy-Labeled Credit-Risk Prediction** — [2609.16102](https://arxiv.org/abs/2609.16102) | cross: cs.AI  
  Mehrdad Shoeibi, Muhammad Shabanpour, Waldemar Karwowski, Niloofar Yousefi  
  Credit-risk models are trained on proxy labels and deployed under temporal and segment change, yet no single transfer metric separates base-rate shift, probability-scale shift, and feature-label relationship change. We contribute a design-science artifact: a locked, multi-signal audit protocol for supervision drift in proxy-labeled credit-risk prediction.
- <a id="20260916-2609.16155"></a>**LLMs as Master Forgers: Generating Synthetic Time Series Data for Manufacturing** — [2609.16155](https://arxiv.org/abs/2609.16155) | cross: cs.AI  
  Mantek Singh, Jeshwanth Challagundla, Prateek Karnal, Gagan Ganapathy et al.  
  This paper presents a novel framework leveraging Large Language Models (LLMs) to generate synthetic time series data for manufacturing processes. Motivated by the scarcity of labeled time-series data in real-world manufacturing settings, which hinders the development of robust machine learning models, we explore the potential of LLMs to learn complex temporal dependencies and generate realistic …
- <a id="20260916-2609.16161"></a>**LLM Inference in a Flash!** — [2609.16161](https://arxiv.org/abs/2609.16161)  
  Sebastian Zhao, Minseo Kim, Coleman Hooper, Luca Manolache et al.  
  Large Language Models (LLMs) have shown impressive capabilities across a range of natural language processing tasks, and LLM inference has emerged as a critical workload for enabling downstream applications. The demands of serving LLM inference are becoming increasingly challenging as requests shift toward longer sequences and heavier inference, driven by retrieval-augmented generation, …
- <a id="20260916-2609.16170"></a>**Skeletal Prototypes on Iterative Nerve Expansions** — [2609.16170](https://arxiv.org/abs/2609.16170) | cross: stat.ML  
  Jordan Eckert, Henry Schenck  
  Prototype reduction replaces a training set with a smaller representation, and the established methods return a finite set of points. We propose Skeletal Prototypes on Iterative Nerve Expansions (SPINE).
- <a id="20260916-2609.16179"></a>**Z-Loss Backward Geometry in Dense Output Heads and Sparse Routers** — [2609.16179](https://arxiv.org/abs/2609.16179) | cross: cs.CL  
  Bum Jun Kim  
  Z-loss has been widely applied to the logits of language-model output heads and sparse mixture-of-experts routers. Z-loss constrains the softmax log-normalizers of these output heads and routers, thereby limiting large-logit excursions, reducing finite-precision roundoff exposure, and avoiding training-loss divergence.
- <a id="20260916-2609.16183"></a>**Anatomy of Associative Recall in Fixed-State Recurrences: A Matched-State Decomposition, an Interference Wall, and a Curriculum That Breaks It** — [2609.16183](https://arxiv.org/abs/2609.16183) | cross: cs.CL  
  Julian Boesch, Andrew Wee  
  Fixed-state recurrences--linear attention and state-space models--are reported to lag behind attention on associative recall, but whole-architecture comparisons cannot say which ingredient is responsible. We decompose masked multi-query recall at a fixed state budget along three single-knob axes: a short causal convolution, the transition structure (rank-1 delta rule vs.
- <a id="20260916-2609.16204"></a>**Decoy Direction Optimization: A Post-Hoc Defense Against LLM Abliteration** — [2609.16204](https://arxiv.org/abs/2609.16204) | cross: cs.CL, cs.CR  
  Aashiq Muhamed, Mona T. Diab, Virginia Smith  
  Safety guardrails in open-weight language models can be readily bypassed using Refusal Feature Ablation (RFA), a technique that identifies and projects out a linear refusal direction from the residual stream, often achieving a high attack success rate (ASR) while preserving model capability. Defending against these attacks typically requires computationally expensive safety finetuning for every …
- <a id="20260916-2609.16222"></a>**How I learned to stop worrying and love StopGrads: Stationarity, Convergence, and a case study on Flow Map Learning** — [2609.16222](https://arxiv.org/abs/2609.16222)  
  Max W. Shen, Mark Goldstein, Zichu Wang, Aahlad Puli et al.  
  Stopgrads are widely used in training machine learning models, but stopgrads can alter the gradient, stationary points and convergence guarantees of the original objective, which can make stopgrad training theoretically ungrounded. We introduce a stopgrad regression principle, which identifies a general template for stopgrad objectives with a closed-form characterization of stationary points and …
- <a id="20260916-2609.16229"></a>**Test-Time Unlearning via Sparse Autoencoder** — [2609.16229](https://arxiv.org/abs/2609.16229) | cross: cs.CL  
  Pingzhi Li, Jinhao Duan, Vaishnav Tadiparthi, Nakul Agarwal et al.  
  Machine unlearning aims to remove specific knowledge from a trained large language model (LLM) without retraining from scratch. Existing methods modify model weights via gradient ascent and its advances.
- <a id="20260916-2609.16255"></a>**Efficient Reasoning Distillation: Small Video-Language Models via Synthetic CoT and Difficulty-Aware Fine-Tuning** — [2609.16255](https://arxiv.org/abs/2609.16255) | cross: cs.AI, cs.CV  
  Mantek Singh, Jeshwanth Challagundla, Siddharth Raina, Jasmin Jarsania  
  We present an efficient method to distill reasoning capabilities into compact video-language models (VLMs) for video question answering (VideoQA). Our approach fine-tunes a 2B-parameter model using only $\sim$900 uncertainty-selected examples, each augmented with synthetic chain-of-thought (CoT) rationales generated by a 4B teacher.
- <a id="20260916-2609.16267"></a>**The record is part of the task: matched-record evaluation of text classifiers across maintenance, safety and recall reporting** — [2609.16267](https://arxiv.org/abs/2609.16267) | cross: cs.CL  
  Hisham Ihshaish, Peter Mayhew, Tasnim M. A. Zayet, Ana Del Amo  
  Many operational cases are documented more than once, at different workflow stages and for different purposes, yet model evaluations normally select one of these records before model comparison begins. We treat that selection as part of the evaluation and compare matched records of the same cases under fixed labels and splits in three systems: GE Aerospace repair events, NASA ASRS safety reports …
- <a id="20260916-2609.16282"></a>**Scaling Laws for Physics-Aware ACOPF Surrogate Learning** — [2609.16282](https://arxiv.org/abs/2609.16282)  
  Yijiang Li, Emon Dey, Stefano Fenu, Massimiliano Lupo Pasini et al.  
  Learning-based surrogates for AC optimal power flow (ACOPF) promise large speedups over classical solvers, but their operational value depends on physical feasibility as much as predictive accuracy. Physics-aware objectives such as the augmented Lagrangian (AL) improve constraint satisfaction at additional per-step cost, yet how this trade-off behaves with scale is uncharacterized.
- <a id="20260916-2609.16283"></a>**Differentially Private Semantic Plans for Aggregate Insight Generation** — [2609.16283](https://arxiv.org/abs/2609.16283)  
  Behrooz Razeghi  
  \texttt{URANIA} provides end-to-end differential privacy (DP) for summaries of data-dependent clusters. However, its cluster--keyword release does not directly provide collection-wide aggregates for semantic concepts defined independently of the protected corpus.
- <a id="20260916-2609.16288"></a>**Drift Field Net: Learning Ocean Lagrangian advection fields from in-situ and satellite observations** — [2609.16288](https://arxiv.org/abs/2609.16288)  
  Th\'eo Archambault, Pierre Garcia, Mattia Romero, Anastase Charantonis et al.  
  The North Pacific Subtropical Gyre (NPSG) is a major accumulation zone for floating plastic debris, resulting from basin-scale convergent ocean circulation. Effective cleanup strategies in this region rely on accurate forecasts of Lagrangian particle drift.
- <a id="20260916-2609.16314"></a>**Robust Fault Detection in Mechanical Multimodal Time Series via Self-Supervised Cross-Modal Reconstruction** — [2609.16314](https://arxiv.org/abs/2609.16314) | cross: stat.AP  
  Magnus Munk Jensen, Dorte Hammersh{\o}i, Rafa{\l} Wi\'sniewski, Olga Fink  
  Fault detection is essential in industrial systems, enabling early identification of abnormal behaviour and improving safety, reliability, and operational efficiency. Modern systems increasingly rely on heterogeneous sensing modalities that capture complementary aspects of the underlying physical process.
- <a id="20260916-2609.16317"></a>**Generative models for simulation based filtering: Formulations and Empirical Comparisons** — [2609.16317](https://arxiv.org/abs/2609.16317)  
  Mohammad Al-Jarrah, Wei Deng, Bamdad Hosseini, Amirhossein Taghvaei  
  This letter presents a unified formulation and a controlled numerical comparison of generative-model approaches to the nonlinear filtering problem. Under this formulation the analysis step is realized by a transport of the forecast distribution to the posterior, the approaches differing only in how that transport is selected and learned.
- <a id="20260916-2609.16341"></a>**Channel-Informed Neural Network for Physical Layer Key Generation** — [2609.16341](https://arxiv.org/abs/2609.16341) | cross: eess.SP  
  Jose Angel Sanchez Viloria, George Sklivanitis, Dimitris Pados, Elizabeth Serena Bentley  
  Physical-layer key generation (PKG) enables wireless devices to establish shared keys from reciprocal channel observations without directly exchanging the key. This capability is attractive for edge networks, where distributed and resource-constrained devices may require lightweight key establishment with limited access to centralized infrastructure.
- <a id="20260916-2609.16347"></a>**Multi-Label Proportion Learning for Sea-Ice Type Prediction** — [2609.16347](https://arxiv.org/abs/2609.16347)  
  Samira Alkaee Taleghan, Younghyun Koo, Andrew P. Barrett, Farnoush Banaei-Kashani  
  Sea-ice type prediction is important for climate monitoring, maritime navigation, and decision-making in polar regions. The main source of label data for this task is the ice chart, produced manually by ice analysts who interpret satellite imagery to delineate ice zones into polygons.
- <a id="20260916-2609.16350"></a>**Federated stochastic bilevel optimization with fully first-order gradients** — [2609.16350](https://arxiv.org/abs/2609.16350)  
  Yihan Zhang, Rohit Dhaipule, Chiu C Tan, Haibin Ling et al.  
  Federated stochastic bilevel optimization has been actively studied in recent years due to its widespread applications in machine learning. However, most existing federated stochastic bilevel optimization algorithms require the computation of second-order Hessian and Jacobian matrices, which leads to longer running times in practice.
- <a id="20260916-2609.16369"></a>**Autonomous Droplet Navigation via Model-Based Reinforcement Learning** — [2609.16369](https://arxiv.org/abs/2609.16369) | cross: cs.RO, cs.SY, eess.SY, physics.flu-dyn  
  Rajneesh Anand, Mayuresh V. Kothare  
  Precise manipulation of liquid droplets underpins lab-on-a-chip platforms for diagnostics, chemical synthesis, and biological assays. Yet autonomous droplet transport through confined geometries of varying complexity remains an open challenge.
- <a id="20260916-2609.16373"></a>**Certified Uncertainty Propagation in One-Shot Federated Bayesian Models via Posterior Event Transport** — [2609.16373](https://arxiv.org/abs/2609.16373)  
  Mahyar Mohammadi, Mohammad Hossein Badiei, Abolfazl Yaghmaei, Hamed Kebriaei  
  Probabilistic certification of Bayesian neural networks lower-bounds the posterior probability that a model satisfies a verifier-defined safety property. In one-shot federated Bayesian learning, however, the deployed model is obtained by aggregating parameters drawn from client-specific posterior distributions, so local certificates do not directly guarantee safety of the aggregated model.
- <a id="20260916-2609.16380"></a>**Bounded Adjustment with Reliability-Guided Embedding for Imbalanced Learning with Noisy Labels** — [2609.16380](https://arxiv.org/abs/2609.16380) | cross: stat.ML  
  Mushir Akhtar, Akarsh J., M. Tanveer, Mohd. Arshad  
  Class-balanced learning and label noise create a coupled failure mode: frequency correction prevents majority classes from dominating the decision rule, but can amplify incorrectly labeled minority examples. We introduce BARGE (Bounded Adjustment with Reliability-Guided Embeddings), a single-stage objective combining a bounded, prior-adjusted density-power score with reliability-guided angular …
- <a id="20260916-2609.16382"></a>**Attention Mean Fields Predict Average Representation Dynamics and Reveal Context-Specific Computation** — [2609.16382](https://arxiv.org/abs/2609.16382) | cross: cs.CL  
  Micah Adler, John W. Byers, Mark Crovella  
  A language model's representation geometry is not predetermined; it evolves as the model runs. A faithful account of that geometry must capture that dynamic process, and so cannot be based solely on model-independent statistics such as co-occurrence.
- <a id="20260916-2609.16415"></a>**How Good Are Time-Series Foundation Models for Pedestrian Crowd Count Forecasting? A Cross-Dataset Comparative Study** — [2609.16415](https://arxiv.org/abs/2609.16415) | cross: cs.AI  
  Theivaprakasham Hari, Ziteng Li, Yanan Xin, Winnie Daamen et al.  
  Pedestrian-count forecasting supports pedestrian-oriented Intelligent Transportation Systems (ITS), including crowd monitoring, pedestrian-traffic staffing and routing, and proactive risk mitigation during surges. Recent time-series foundation models (FMs) report strong zero-shot accuracy on heterogeneous forecasting benchmarks, but it remains unclear whether these gains transfer reliably to …
- <a id="20260916-2609.16436"></a>**Interpreting and Steering LLM Agents for Social Simulations** — [2609.16436](https://arxiv.org/abs/2609.16436) | cross: cs.AI, cs.CL  
  Jiayue Gaveal Fan, Arul Murugan, Shreyas Krishnan, Abhishek Nagaraj  
  Simulations based on large language models (LLMs) have proven to be powerful for understanding human behavior, making them valuable additions to the social scientific toolkit. However, LLMs are ultimately black boxes based on deep neural networks which limits their value for social science.
- <a id="20260916-2609.16446"></a>**Adaptive Bayesian Partner Selection for Federated Clinical Centers** — [2609.16446](https://arxiv.org/abs/2609.16446) | cross: cs.DC  
  Navid Seidi, Satyaki Roy, Sajal K. Das  
  Federated learning (FL) in healthcare faces pronounced heterogeneity and temporal concept drift across clinical centers, where evolving patient populations and care practices shift data distributions. Existing approaches rely on persistent global communication, incurring substantial bandwidth overhead while risking negative transfer from poorly aligned peers.
- <a id="20260916-2609.16459"></a>**OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation** — [2609.16459](https://arxiv.org/abs/2609.16459) | cross: cs.AI, cs.CV  
  Chenhao Qiu, Dawei Li, Yechao Zhang, Lei Gong et al.  
  Privileged on-policy distillation improves multimodal reasoning by allowing a teacher to evaluate student trajectories using rich, training-only visual evidence. Both models score these trajectories while conditioning on the same student-generated prefix.
- <a id="20260916-2609.16472"></a>**Online Gradient Computation for Warping Gaussian Process Transformations** — [2609.16472](https://arxiv.org/abs/2609.16472) | cross: eess.SP  
  Emilio Ruiz-Moreno, Konstantinos Slavakis, Baltasar Beferull-Lozano  
  Warped Gaussian processes (GPs) handle non-Gaussian observations by mapping them into a latent standard GP via a parametric transformation called warping. Existing streaming variants, however, either optimize the warping parameters periodically or sacrifice analytical tractability for a higher model capacity.
- <a id="20260916-2609.16489"></a>**Decoder Design Matters for ECG Delineation** — [2609.16489](https://arxiv.org/abs/2609.16489) | cross: cs.AI  
  Joseph Scharpf, William Han, Chaojing Duan, Michael A. Rosenberg et al.  
  Electrocardiogram (ECG) delineation identifies the boundaries of P waves, QRS complexes, and T waves, providing structural annotations that can guide AI models in learning to interpret ECGs. However, training accurate delineation models requires manual annotations that are scarce and time-consuming to obtain.
- <a id="20260916-2609.16500"></a>**High-Performance Tensor Formulation of the Viterbi Algorithm for Hidden Semi-Markov Models** — [2609.16500](https://arxiv.org/abs/2609.16500) | cross: cs.DC, cs.DS  
  Lorenzo Piarulli, Elia Belli, Daniele De Sensi  
  Hidden Semi-Markov Models (HSMMs) are fundamental probabilistic models widely adopted across diverse domains, from computational biology to finance and signal processing. The Viterbi algorithm decodes the most likely state sequence given an HSMM and can be applied iteratively for ab initio model learning.
- <a id="20260916-2609.16528"></a>**FlowATC: Aircraft Trajectory Prediction via Flow Matching** — [2609.16528](https://arxiv.org/abs/2609.16528)  
  Mathurin Petit, Emir Torun, Louis Brusset, Jordan Kam et al.  
  Building accurate decision-support tools for next-generation air traffic control requires robust trajectory prediction models. We present a flow-matching architecture trained exclusively on historical aircraft trajectories, with no route labels or chart supervision.
- <a id="20260916-2609.16537"></a>**What Does Layer-Importance Reveal About Transformers and State-Space Models?** — [2609.16537](https://arxiv.org/abs/2609.16537) | cross: cs.AI  
  Istabrak Abbes, Nizar Islah, Irina Rish, Sarath Chandar  
  Transformers and state-space models (SSMs) are the two dominant families of sequence models, and a central open question is how far the analytical knowledge built for transformers transfers to SSMs. We address this through the lens of layer importance which underpins compression, selective fine-tuning, and interpretability across both families.
- <a id="20260916-2609.16540"></a>**On the Importance of Gating: Memorization vs. In-Context Learning in State Space Models** — [2609.16540](https://arxiv.org/abs/2609.16540) | cross: cs.AI  
  William L. Tong, Aryo Lotfi, Emmanuel Abbe, Kostas Vaggelakos et al.  
  State Space Models (SSMs) have emerged as a compelling alternative to Transformers, enabling sequence modeling with constant memory and linear compute. Although SSMs exhibit reasonable performance and favorable computational characteristics, they continue to lag behind Transformers on tasks that require in-context learning and precise retrieval, slowing their adoption for large-scale language …
- <a id="20260916-2609.16573"></a>**AsyncCouple-Flow: Asynchronous Cross-Modal Coupling and Flow Matching for Spatio-Temporal Forecasting** — [2609.16573](https://arxiv.org/abs/2609.16573)  
  Zhixiang Wu, Yining Liu, Bo Zhao, Szu-Yu Chen et al.  
  Multi-modal spatio-temporal forecasting (MM-STF) supports weather nowcasting, traffic prediction, and earth-system modeling by combining heterogeneous sources such as physical fields, satellite imagery, and in-situ sensors. Three obstacles persist: (i) modalities have different spatio-temporal sampling rates, forcing lossy interpolation onto a unified grid; (ii) modalities are frequently missing …
- <a id="20260916-2609.16579"></a>**Recovering Physical Parameters from Fragmented Observations via Exact Distributed Spline Merging** — [2609.16579](https://arxiv.org/abs/2609.16579) | cross: physics.comp-ph  
  Naveen Mysore  
  Scientific measurements are frequently distributed across locations, time periods, and institutions. Combining such fragments into a continuous, differentiable field enables recovering governing physical parameters from its derivatives.
- <a id="20260916-2609.16606"></a>**A Weighted Kernel Method for Approximation that Adapts to Learned Multivariable Structure** — [2609.16606](https://arxiv.org/abs/2609.16606) | cross: cs.NA, math.NA  
  John E. Darges, Laura Weidensager  
  Approximating the input-output behavior of a multivariable black-box function from limited data is challenging when blind to the importance of its inputs and their interactions. We introduce total sensitivity kernels (TSKs), a method based on families of weighted ANOVA kernels that learn and adapt to this multivariable structure.
- <a id="20260916-2609.16617"></a>**Divergence Timing and Cumulative Disagreement under KV-Cache Eviction** — [2609.16617](https://arxiv.org/abs/2609.16617)  
  Xinyue Luo, Fei Yu  
  KV-cache eviction perturbs the conditional token distributions governing autoregressive generation. We investigate how first-divergence timing and subsequent token mismatch determine cumulative disagreement.
- <a id="20260916-2609.16621"></a>**Stable by Construction: Variational Latent Markov Operators for Long-Horizon PDE Prediction** — [2609.16621](https://arxiv.org/abs/2609.16621) | cross: stat.ML  
  Junyi Liao, Johann Guilleminot, Vahid Tarokh  
  Neural PDE solvers provide efficient surrogates for time-dependent physical systems, but autoregressive prediction over long horizons remains challenging because local errors can induce distribution shift and accumulate under recursive deployment. We develop a variational approach to this problem by introducing latent Markov dynamics in which physical states are represented by latent …
- <a id="20260916-2609.16648"></a>**GrowMTP: Can RL Grow Its Own Draft Head?** — [2609.16648](https://arxiv.org/abs/2609.16648) | cross: cs.CL  
  Minghua He, Lingzhe Zhang, Yuan Liu, Xiao Zhou et al.  
  Reinforcement learning (RL) post-training drives the frontier capabilities of large language models, with its wall-clock dominated by autoregressive rollout generation. Speculative decoding is an established remedy for this bottleneck, but existing draft heads must be pretrained or warmed up before RL, introducing substantial training cost outside the RL run to be accelerated.
- <a id="20260916-2609.16744"></a>**A Systematic Evaluation of Machine Learning Methods for Fault Detection and Line Identification in Electrical Power Grids** — [2609.16744](https://arxiv.org/abs/2609.16744) | cross: eess.SP  
  Julian Oelhaf, Georg Kordowich, Paula Andrea P\'erez-Toro, Tom\'as Arias-Vergara et al.  
  The integration of renewable energy sources into the electrical grid introduces complex challenges in fault detection and coordination of grid recovery mechanisms. Traditional relay protection systems, which operate based on static rules and predefined thresholds, are inadequate for addressing these challenges, particularly in detecting and isolating faults such as short circuits.
- <a id="20260916-2609.16788"></a>**Noise2Noise Revisited: Training Pair Distributions Dominate Loss Choice in Self-Supervised Denoising** — [2609.16788](https://arxiv.org/abs/2609.16788) | cross: cs.CV, eess.IV  
  Dingyan Shang, Zhenyu Xu, Youting Wang, Bonan Shen et al.  
  Noise2Noise (N2N) trains denoisers on pairs of independently corrupted observations, eliminating clean references. We stress-test two natural conjectures about why the L1 loss outperforms L2 here.
- <a id="20260916-2609.16805"></a>**Geometry of learning dynamics: Gradient descent versus natural gradient on the ridge of optimization** — [2609.16805](https://arxiv.org/abs/2609.16805) | cross: cs.NE  
  Akira Tamamori  
  High-capacity associative memories based on Kernel Logistic Regression (KLR) exhibit a "Ridge of Optimization" characterized by extreme stability and a highly skewed weight spectrum. However, the dynamical process by which learning converges to this critical regime has remained unclear.
- <a id="20260916-2609.16816"></a>**ImpossibleRubrics: Stress-Testing Generated Rubrics as Reward Signals** — [2609.16816](https://arxiv.org/abs/2609.16816) | cross: cs.CL  
  Bowen Qin, Yi Xie, Yesheng Liu, Xi Yang  
  Language model-generated rubrics are increasingly used as reward signals for rubric-based reinforcement learning, LLM-as-a-judge evaluation, and automated grading. Such rubrics are reliable only if they reward honest answers over adversarial answers optimized to exploit them.
- <a id="20260916-2609.16823"></a>**LCAP: Population-Informed Latent Chip Adaptation from Few Output Probes for Photonic Neural Networks** — [2609.16823](https://arxiv.org/abs/2609.16823)  
  Tianyu Gao, Guantian Zheng  
  Photonic neural networks (PNNs) offer efficient analog inference, but parameters optimized under ideal device models can degrade after fabrication, creating a persistent simulation-to-hardware (sim-to-real) gap. When many identically designed chips are deployed, calibrating each device from scratch compounds this cost.
- <a id="20260916-2609.16824"></a>**Adapting to Decision-Relevant Non-Stationarity in Decentralized Heterogeneous Bandits** — [2609.16824](https://arxiv.org/abs/2609.16824)  
  Zhaojun Peng  
  Decentralized bandit systems often contain heterogeneous agents: rewards can change at individual agents even when the best action for the network stays the same. These local changes may cancel when rewards are averaged across agents, so the number of local changes $\Stloc$ can be much larger than the number of changes in the best common arm $\Stdec$.
- <a id="20260916-2609.16827"></a>**Information Geometric Self-Organization at the Edge of Stability in High-Capacity Kernel Associative Memories** — [2609.16827](https://arxiv.org/abs/2609.16827) | cross: cs.NE  
  Akira Tamamori  
  High-capacity associative memories based on Kernel Logistic Regression (KLR) exhibit exceptional storage capabilities and robustness. Previous empirical studies identified a hyperparameter regime, the "Ridge of Optimization," where attractor stability is maximized.
- <a id="20260916-2609.16853"></a>**Can Deep Learning Achieve Cross-Physics Mapping?** — [2609.16853](https://arxiv.org/abs/2609.16853) | cross: physics.app-ph  
  Pengfei Zhu, Julien Lecompagnon, Mathias Ziegler  
  Can deep learning translate physical fields governed by fundamentally different equations? We address this question by introducing Cross-Physics Mapping (CPM), an operator-learning framework for mappings between heterogeneous physical domains.
- <a id="20260916-2609.16925"></a>**HyCoSeq: Contextual Hyperbolic Representation Learning for Genomic Sequences** — [2609.16925](https://arxiv.org/abs/2609.16925) | cross: q-bio.GN, stat.ML  
  Chenhao Zeng, Zhibin Pu, Shufei Ge  
  Hyperbolic geometry provides a natural inductive bias for genomic representation learning, but existing hyperbolic genomic models primarily use Lorentz convolutions to learn local sequence representations, while their residual pathways do not directly aggregate full Lorentz representations. We propose HyCoSeq, a contextual hyperbolic representation learning framework for genomic sequences.
- <a id="20260916-2609.17026"></a>**CLARE: Scalable Class-Incremental Continual Learning via a Sparsity-Based Framework** — [2609.17026](https://arxiv.org/abs/2609.17026) | cross: cs.CV  
  Yunxiang Fu, Meng Lou, Zicheng Liao, Yizhou Yu  
  Continual learning must balance the learning of new knowledge with the retention of previously learned knowledge to incrementally learn tasks from a data stream without catastrophic forgetting. While leveraging pretrained models has significantly advanced continual learning, existing methods exhibit a scalability bottleneck when trained sequentially on many tasks, suffering from performance …
- <a id="20260916-2609.17042"></a>**Learning Options for Compositional Motor Control with Adapter Banks** — [2609.17042](https://arxiv.org/abs/2609.17042) | cross: cs.RO, q-bio.NC  
  Sreejan Kumar, Marcelo Mattar, Lea Duncker  
  Learning flexible motor primitives is a hallmark of skilled motor control. Recent neuroscience theory proposes that motor primitives may be implemented as low-rank perturbations of a shared recurrent network, but leaves open how such a system is learned.
- <a id="20260916-2609.17101"></a>**High-Fidelity Digital Twin Data Models by Randomized Dynamic Mode Decomposition and Deep Learning with Applications in Fluid Dynamics** — [2609.17101](https://arxiv.org/abs/2609.17101) | cross: cs.NA, math.NA  
  Diana A. Bistrian  
  The purpose of this paper is the identification of high-fidelity digital twin data models from numerical code outputs by non-intrusive techniques (i.e., not requiring Galerkin projection of the governing equations onto the reduced modes basis). In this paper the author defines the concept of the digital twin data model (DTM) as a model of reduced complexity that has the main feature of mirroring …
- <a id="20260916-2609.17160"></a>**Neural Field Ensembles for Aerodynamic Surface Prediction: Winning Solution to the ONERA CRM Wall Distribution 2025 Challenge** — [2609.17160](https://arxiv.org/abs/2609.17160) | cross: physics.flu-dyn  
  Lionel Salesses, Caroline Sainvitu, Tariq Benamara  
  Machine-learning surrogate models offer a promising alternative to high-fidelity Computational Fluid Dynamics (CFD) simulations for aerodynamic analysis and design. However, constructing accurate surrogates for realistic aircraft configurations remain challenging due to complex geometries, multiple flow regimes, and limited training data.
- <a id="20260916-2609.17175"></a>**IRENE: A Convolutional GRU Ensemble Model for Radar Precipitation Nowcasting over Italy** — [2609.17175](https://arxiv.org/abs/2609.17175) | cross: physics.ao-ph  
  Alessandro Camilletti, Gabriele Franch, Elena Tomasi, Marco Cristoforetti  
  We present IRENE (Italian Radar Ensemble Nowcasting Experiment), a deep learning model for probabilistic short-range precipitation nowcasting over the Italian domain at \SI{1}{km} spatial and 5 min temporal resolution. IRENE adopts an encoder--forecaster architecture built on multi-scale Convolutional Gated Recurrent Units (ConvGRUs), trained on the national radar composite produced by the …
- <a id="20260916-2609.17184"></a>**LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers** — [2609.17184](https://arxiv.org/abs/2609.17184) | cross: cs.CL  
  SangLyul Cho, Langqing Cui, Sehoon Kim, Dongsu Han et al.  
  Looped Transformers achieve strong performance with compact parameter sizes by repeatedly applying a shared stack of Transformer blocks across recurrent depths. However, they incur higher decoding latency than standard Transformer models of comparable parameter size because shared weights are accessed at every recurrent depth.
- <a id="20260916-2609.17194"></a>**MyoFlow: Anchor-Tied Rectified Flow for HD-sEMG Gesture Recognition Across Sessions and Subjects** — [2609.17194](https://arxiv.org/abs/2609.17194)  
  Chenhao Wu, Dingjie Peng, Satoshi Funabashi, Satoshi Konishi et al.  
  High-density surface electromyography (HD-sEMG) gesture recognition supports prosthetic control, assistive robotics, and rehabilitation, but electrode re-donning and physiological variability cause distribution shifts that degrade accuracy across sessions and subjects. Generative HD-sEMG models primarily synthesize signals for augmentation; although diffusion models enhance representation …
- <a id="20260916-2609.17223"></a>**Memorisation bias in medical AI** — [2609.17223](https://arxiv.org/abs/2609.17223) | cross: cs.CY  
  Moritz A. Knolle, Martin J. Menten, Laurin Lux, M\'elanie Roschewitz et al.  
  Medical AI models hold immense potential to improve patient outcomes, but they are also known to unintentionally memorise individual records from their training datasets. While such memorisation has been linked to targeted privacy attacks, its consequences for clinical deployment, where patients may be assessed by a model that saw their historical data during training, remain poorly understood.
- <a id="20260916-2609.17284"></a>**Personalized Federated Learning through Global Knowledge Distillation and Local Head Adaptation** — [2609.17284](https://arxiv.org/abs/2609.17284) | cross: stat.ML, stat.OT  
  Polycarpo Souza Neto, Jos\'e Mairton Barros da Silva J\'unior, Charles Casimiro Cavalcante  
  Statistical heterogeneity limits federated learning when a single global classifier cannot represent client-specific label distributions. In this work, we propose Personalized Federated Knowledge Distillation with Head Adaptation (pFedKDH), which aggregates only the shared backbone, keeps persistent client-specific heads, and uses a recalibrated global head as a teacher during local training.
- <a id="20260916-2609.17287"></a>**Same Flow, Different Paths: Variance Reduction in Flow Matching** — [2609.17287](https://arxiv.org/abs/2609.17287) | cross: math.OC  
  Alexander Tyurin  
  In flow matching (FM), a velocity model $v_{\theta}$ is trained using a predefined path $g_t$ that connects data and noise samples (e.g., $g_t(x_0, x_1) = (1 - t) x_0 + t x_1$). In this work, we study the choice of this path from an optimization perspective by analyzing the variance of stochastic gradients.
- <a id="20260916-2609.17358"></a>**Hybrid Variational Quantum Circuits for Multivariate Regression and High-Dimensional Data Reconstruction** — [2609.17358](https://arxiv.org/abs/2609.17358) | cross: stat.ML  
  Koffi Ognandon Ayena (ICB), Fr\'ed\'eric Holweck (ICB), Serge Iovleff (UR4662), Amah S d'Almeida  
  Variational quantum circuits (VQCs) are parameterized quantum circuits optimized classically. We propose a hybrid variational quantum circuit (HVQC) extending VQCs with a classical affine post-measurement layer, enabling vector-valued regression without the linear overhead of independent scalar circuits.
- <a id="20260916-2609.17376"></a>**Large Language Models Develop Belief State Geometry In-Context** — [2609.17376](https://arxiv.org/abs/2609.17376) | cross: cs.CL  
  Daniel Balcells, Andrew Jun Lee, Chirag Rastogi, Paul M. Riechers et al.  
  Large language models (LLMs) trained on next-token prediction exhibit remarkable in-context learning (ICL) abilities, yet the representations that support ICL remain poorly understood. We consider such representations in a controlled setting: prompting LLMs with data emitted from hidden Markov models (HMMs) and probing for the corresponding belief state -- the posterior distribution over the …
- <a id="20260916-2609.17380"></a>**OPEN-1B: A Fully Auditable Training Run** — [2609.17380](https://arxiv.org/abs/2609.17380)  
  John Donaghy, Brian Wilcox, O\u{g}uzhan Ersoy, Shikhar Rastogi et al.  
  Open-source language models have a reproducibility problem. Despite releasing weights, training data, and recipes, none of them are provably reproducible due to the non-associativity of floating-point arithmetic.
- <a id="20260916-2609.17386"></a>**Bridging the Confidence Gap: Temperature Scaling for Calibrating Test-Time Prompt Tuning** — [2609.17386](https://arxiv.org/abs/2609.17386)  
  Yuwei Liang, Jian Liang, Dapeng Hu, Yinuo Xu et al.  
  Test-time prompt tuning (TPT) enables adaptation on a single test instance, achieving improved accuracy but often sacrificing calibration performance. Most existing calibration methods introduce additional regularization terms to promote dispersion across text embeddings and reduce calibration error, yet these methods often suffer from a drop in accuracy.
- <a id="20260916-2609.17417"></a>**Knowledge as Orbit: Finite Collections as Phases of an Exactly Periodic Latent Generator** — [2609.17417](https://arxiv.org/abs/2609.17417) | cross: cs.CV, eess.IV  
  Siddharth Pal, Viktoria Rojkova  
  Finite knowledge is usually stored extensionally, one code or vector per item. We ask whether a finite collection can instead be stored intensionally, as the decoded orbit of one compact law that returns exactly to its start.
- <a id="20260916-2609.17440"></a>**Reduced-Space Multi-Fidelity Bayesian Optimization of Process Simulation Models** — [2609.17440](https://arxiv.org/abs/2609.17440) | cross: math.OC  
  Niki Triantafyllou, Andrea Bernardi, Maria M. Papathanasiou  
  Optimizing industrial process flowsheets is often computationally prohibitive due to the high cost of rigorous simulations and the curse of dimensionality inherent in complex design spaces. To address these challenges, we present a reduced-space multi-fidelity Bayesian optimization (RS-MFBO) framework designed for high-dimensional, expensive black-box functions.
- _…另有 63 篇, 见 `data/20260916.json`_

#### cs.DB (3)

- <a id="20260916-2609.16218"></a>**How Can We Shrink the Family of Test Databases? Query Containment with Nulls and Comparisons** — [2609.16218](https://arxiv.org/abs/2609.16218)  
  Helen Sternbach, Sara Cohen  
  Query containment and equivalence drive database query optimization and rewriting. For plain conjunctive queries, both are decided by evaluating one query over a single canonical database of the other.
- <a id="20260916-2609.16221"></a>**Vector fields, initial scaffolds and database reduction** — [2609.16221](https://arxiv.org/abs/2609.16221) | cross: cs.DB, math.AT  
  Isaac Carcac\'ia-Campos  
  Reduction replaces a mathematical object with a simpler model that retains the relevant information. We introduce left and right vector fields on small categories as tools for reducing finite acyclic categories while preserving their directed homotopical information.
- <a id="20260916-2609.16393"></a>**ParsHate: A Benchmark Dataset for Hate and Target Detection in Persian** — [2609.16393](https://arxiv.org/abs/2609.16393) | cross: cs.DB  
  Zahra Bokaei, Walid Magdy, Bonnie Webber  
  We introduce ParsHate, a manually annotated dataset of 10,000 Persian tweets spanning 2013-2022, representing the first decade-long benchmark for hate speech detection in Persian. The dataset contains 31% hateful content and supports both hate detection and multi-label fine-grained target identification across seven structured target categories.

#### cs.DC (5)

- <a id="20260916-2609.17074"></a>**Byzantine Reliable Broadcast with Causal Ordering** — [2609.17074](https://arxiv.org/abs/2609.17074) | 🎯★ Byzantine  
  Mariarosaria Barbaraci, Christian Cachin  
  Reliable and total-order broadcasts in the Byzantine-fault model are well studied, but adding causal order has received comparatively little attention, largely due to the complexity that stems from actions of Byzantine processes. Existing solutions almost exclusively build causal ordering on top of total-order broadcast.
- <a id="20260916-2609.17185"></a>**DS2-Based Cross-Data-Space Interoperability for Precision Agriculture** — [2609.17185](https://arxiv.org/abs/2609.17185)  
  Katerina Kyriakou, Ilias Syrigos, Ioannis Moutsinas, Panagiotis Tzimotoudis et al.  
  Despite the strategies of modern precision agriculture to leverage the integration of legacy agricultural systems, the challenges of IoT data fragmentation, farmers' sovereignty preservation, and limited interoperability still persist. This paper presents our work, conducted within the Horizon Europe DS2 project (DataSpace, DataShare 2.0), that applies an interoperability-oriented framework …
- <a id="20260916-2609.16787"></a>**Nested Parallel von Neumann Architecture and Nested BSP** — [2609.16787](https://arxiv.org/abs/2609.16787) | cross: cs.AR  
  Heng Liao  
  Large-scale AI computing is no longer a contest of ''one stronger processor,'' but of how an army of processors under one command can still be one computer. This paper offers two interlocking extensions.
- <a id="20260916-2609.16731"></a>**The Price of Random Access: Measuring Block Granularity Across Four Compressed Formats** — [2609.16731](https://arxiv.org/abs/2609.16731) | cross: cs.DS  
  Yakiv Shavidze  
  Random access into compressed data is normally bought with density. We measure the exchange rate.
- <a id="20260916-2609.16682"></a>**DeepShare: Assurance-Driven Deep Learning Job Scheduling for Multi-Tenant Clusters** — [2609.16682](https://arxiv.org/abs/2609.16682)  
  Jinghao Wang, Yihang Zhou, Xiao Zhou, Xinlei Zheng et al.  
  Multi-tenant GPU clusters frequently remain underutilized even when tenants experience long queueing delays, because quota control, queue ordering, preemption, and GPU sharing are driven by different local signals. We present DeepShare, a scheduler that uses a continuous tenant-assurance signal to coordinate these decisions at runtime.

#### cs.FL (1)

- <a id="20260916-2609.16866"></a>**Mining DTA with SMT by Exploiting Simple Elementary Language and Timed Augmented Prefix Acceptor** — [2609.16866](https://arxiv.org/abs/2609.16866)  
  Ziran Wang, Jie An, Naijun Zhan  
  Timed automata, which extend finite state automata by introducing clock variables, serve as a popular formalism for specifying and analyzing the timed behaviors of real-time systems. Extracting the timed behaviors of a black-box, safety-critical system is crucial for designing and analyzing its real-time requirements, yet it remains challenging.

#### cs.LO (6)

- <a id="20260916-2609.16706"></a>**Vibe-Coded and Tuned: A State-of-the-Art SMT Solver for QF-LRA** — [2609.16706](https://arxiv.org/abs/2609.16706) | 🎯★ SMT solver  
  Mikoláš Janota, Jan Jakubův  
  This paper presents the SMT solver primo, which is fully vibe-coded and then parameter-tuned, achieving state-of-the-art results on linear real arithmetic (QF-LRA). The performance of primo is achieved by a systematic literature survey, repeated profiling, and parameter tuning.
- <a id="20260916-2609.17392"></a>**Predictable Modelling and Analysis of Software-defined Vehicle Implementations** — [2609.17392](https://arxiv.org/abs/2609.17392)  
  Pavlo Tokariev, Yosri Ayari, Julien Deantoni  
  Software-Defined Vehicles (SDVs) rely on middleware-based communication and hardware abstraction mechanisms that introduce temporal uncertainty affecting end-to-end timing guarantees. Previous work proposed probabilistic architectural models for early timing analysis, but the representativeness of these abstractions with respect to SDV implementations remained unclear.
- <a id="20260916-2609.17388"></a>**Refining Timing Uncertainty from Logical Time Specification to Operation** — [2609.17388](https://arxiv.org/abs/2609.17388)  
  Pavlo Tokariev, Julien Deantoni  
  Real-time and cyber-physical systems are developed through successive refinements from abstract requirements to platform deployments. While timing knowledge evolves throughout this process, existing stochastic real-time formalisms typically require uncertainty to be embedded from the outset or necessitate model reconstruction when new timing information becomes available, hindering iterative …
- <a id="20260916-2609.17364"></a>**The Classical Weisfeiler-Leman Algorithm Stabilizes in $O(n)$ Rounds** — [2609.17364](https://arxiv.org/abs/2609.17364) | cross: cs.DM, cs.LO  
  Simon Döring, Daniel Neuen  
  The classical Weisfeiler-Leman algorithm (also known as the $2$-dimensional Weisfeiler-Leman algorithm) is a simple combinatorial algorithm that was originally designed as a heuristic for the graph isomorphism problem. However, it has also numerous connections to other areas such as algebraic graph theory, logics, proof complexity, combinatorial optimization and machine learning.
- <a id="20260916-2609.17324"></a>**Universal Properties of Petri Net Unfoldings** — [2609.17324](https://arxiv.org/abs/2609.17324) | cross: math.CT  
  Serge Lechenne, Hugo Paquet  
  It is an established idea in concurrency theory that every Petri net admits an unfolding semantics. This is a denotational object that represents its domain of possible executions.
- <a id="20260916-2609.16798"></a>**On Models of the Planar Lambda Calculus** — [2609.16798](https://arxiv.org/abs/2609.16798) | cross: cs.LO  
  Chad Nester  
  We construct an adjunction relating two approaches to modelling the planar lambda calculus: semi-closed operads and planar lambda-models. We use this to obtain a planar version of Scott's representation theorem.

#### cs.SE (15)

- <a id="20260916-2609.17221"></a>**Grounding SWE-Agent Decisions in Architecture-0 Design: Navigating Unknown Unknowns through Physical Mapping** — [2609.17221](https://arxiv.org/abs/2609.17221) | cross: cs.AI | 🎯★ consensus  
  Zhongkai Wang, Yan Liu  
  Autonomous Software Engineering Agents (SWE-Agents) excel in deterministic coding tasks but struggle with Architecture 0, the nascent system design phase plagued by implicit engineering constraints, or Unknown Unknowns (UUs) that are rarely stated explicitly. To investigate how agents navigate UUs, we explore a progressive trajectory across pure-text self-play, tool-augmented feedback, and …
- <a id="20260916-2609.17394"></a>**Coding Agents Have Converged: Why the SWE-bench Leaderboard Can No Longer Order Its Top Entries, and What to Measure Instead** — [2609.17394](https://arxiv.org/abs/2609.17394) | cross: cs.AI  
  Fengshuo Liu, Ying Liu, Ruize Sun, Lie Luo et al.  
  Small differences on coding-agent leaderboards are often read as an ordering of systems. We audit whether the published verdicts support this reading, using 254 SWE-bench submissions across four splits without running models.
- <a id="20260916-2609.17274"></a>**After the Party: Governing What a Viral Agent-Skill Ecosystem Left Behind** — [2609.17274](https://arxiv.org/abs/2609.17274) | cross: cs.AI, cs.CY  
  Yunpeng Xiong, Ting Zhang  
  AI agents increasingly act through agent skills, i.e., natural-language instructions, that direct a host agent toward shell, network, credential, file, and process actions, and public registries distribute them at scale. In the first half of 2026, the OpenClaw AI agent went viral, and its public skill registry boomed: the observable stock nearly doubled in 91 days, and a majority of the listings …
- <a id="20260916-2609.16936"></a>**RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views** — [2609.16936](https://arxiv.org/abs/2609.16936) | cross: cs.AI  
  Yunxiang Zhang, Haiquan Wang, JiaWei Guo, Hanyang Xia et al.  
  Large language model (LLM)-powered coding agents have made rapid progress in automating software engineering tasks, yet repository-level issue resolution remains challenging. Beyond generating a plausible patch, an agent must localize relevant code across interdependent files and maintain repository context that is both sufficient and focused.
- <a id="20260916-2609.17338"></a>**Type-IV Code Clone Detection via Layer-Wise Non-Contrastive Representation Learning** — [2609.17338](https://arxiv.org/abs/2609.17338) | cross: cs.LG  
  Luciano Marchezan, Kevin Delcourt, Eugene Syriani, Houari Sahraoui  
  Software clones are fragments of code that are similar or functionally equivalent to each other. They pose significant challenges for maintenance, refactoring, and bug detection.
- <a id="20260916-2609.17258"></a>**An Exemplar of a Digital Twin in Mechanical Engineering: Understanding Model Hybridization** — [2609.17258](https://arxiv.org/abs/2609.17258)  
  Mahussi Datongnon, Hubert Lejeune, Yoann Jus, Benoit Combemale et al.  
  Digital Twins (DTs) are widely adopted across a variety of application domains. In industrial sectors, particularly in mechanical engineering, they accelerate product development, reduce risks, enable early issue prediction, and lower sustainment costs .
- <a id="20260916-2609.17236"></a>**A Memorization Floor for LLM Refinement of Decompiled Code** — [2609.17236](https://arxiv.org/abs/2609.17236)  
  Muhammad Asjad  
  We introduce a memorization floor: a within-item control separating what LLM refinement of decompiler output recovers from its input from what it recovers from its prior. Refine a function, then refine it again from an input whose identifiers have been destroyed, and measure what survives.
- <a id="20260916-2609.17084"></a>**Towards an Asset Administration Shell Maturity Model** — [2609.17084](https://arxiv.org/abs/2609.17084) | cross: eess.SY  
  Carsten Ellwein, David Dietrich, Rozana Cvitkovic, Andreas Wortmann  
  The Asset Administration Shell (AAS) is increasingly recognized as a fundamental model for the realization of and data exchange between digital twins in manufacturing. An AAS defines a hierarchical data structure to represent any type of asset throughout its entire lifecycle.
- <a id="20260916-2609.17062"></a>**A Set-Theoretic Evaluation Framework for Assessing Asset Administration Shell Instances: Towards Comparability and Suitability** — [2609.17062](https://arxiv.org/abs/2609.17062) | cross: eess.SY  
  Carsten Ellwein, David Dietrich, Rozana Cvitkovic, Bastian Lang et al.  
  Asset Administration Shells (AAS) provide a standardized means of representing assets and their information in manufacturing and increasingly serve as a basis for software services. However, different AAS instances vary in structure, content, and degree of completion, making it difficult to determine whether a given AAS is suitable for a specific application.
- <a id="20260916-2609.17018"></a>**GANADI: Uncovering C/C++ OSS Reuse Genealogies via Pivotal Function-Based Clustering to Enhance Supply Chain Security** — [2609.17018](https://arxiv.org/abs/2609.17018)  
  Dongyeon Kim, Seunghoon Woo, Heejo Lee  
  We present GANADI, a systematic approach for identifying C/C++ OSS reuse genealogies to enhance software supply chain security. Understanding OSS reuse genealogy is crucial for improving SBOM completeness and prioritizing security remediation across supply chains.
- <a id="20260916-2609.17007"></a>**Search-Based Metamorphic Testing of Vision-Language Models in Autonomous Underwater Robotic Software** — [2609.17007](https://arxiv.org/abs/2609.17007)  
  Muhammad Yousaf, Aitor Arrieta, Shaukat Ali, Paolo Arcaini et al.  
  Our industry partner focuses on quality assurance for industrial systems across multiple domains, including maritime systems, such as overwater vessels and autonomous underwater robots (AURs). Despite the strong performance of vision-language models (VLMs) in scene understanding, image captioning, and object recognition, their use in AUR software operating in underwater environments is …
- <a id="20260916-2609.16987"></a>**TasmScan: Continuation-Aware Taint Analysis for TVM Bytecode with Savelist Abstraction** — [2609.16987](https://arxiv.org/abs/2609.16987) | cross: cs.CR  
  Yixuan Liu, Yin Wu, Yi Li  
  The Open Network (TON), with a peak market capitalization exceeding $20 billion and over 175 million activated on-chain addresses, relies on the TVM (TON Virtual Machine) to execute smart contracts. TVM uses first-class continuations with savelists to manage control flow and register state across continuation invocations.
- <a id="20260916-2609.16764"></a>**RECTIFY: An Interactive Workbench for Post-Evaluation RAG Diagnosis, Repair, and Verification** — [2609.16764](https://arxiv.org/abs/2609.16764)  
  Keerthana Murugaraj, Salima Lamsiyah, Martin Theobald  
  Retrieval-Augmented Generation (RAG) evaluators can identify failures such as weak retrieval, poor grounding, incomplete answers, and unsupported generation, but they rarely help developers decide what to repair next. We present RECTIFY, an interactive Streamlit workbench that turns evaluated RAG cases into auditable repair workflows.
- <a id="20260916-2609.16669"></a>**Memory-Skill Isomorphism: One Skill Carrier, Two Native Uses** — [2609.16669](https://arxiv.org/abs/2609.16669)  
  Kang Ruiyuan  
  Memory and skills improve agents without changing weights: memory carries prior experience, skills carry reusable procedures. Wrapping both in stores, routers, retrieval, reflection, and update paths makes reuse machinery grow with accumulation.
- <a id="20260916-2609.16321"></a>**FairLint-DL: An IDE-Native Tool for Fairness Debugging of Deep Learning Software** — [2609.16321](https://arxiv.org/abs/2609.16321) | cross: cs.AI, cs.LG  
  Archit Rathod, Saeid Tizpaz-Niari  
  Existing fairness analysis tools predominantly operate as post-training evaluation frameworks, requiring practitioners to complete the full model development lifecycle before assessing bias. We present FairLint-DL, a Visual Studio Code extension that implements a shift-left approach to fairness testing by enabling pre-training, IDE-native bias detection directly on tabular datasets.

<!-- END 20260916 -->

<!-- BEGIN 20260915 -->
## 20260915

时间窗口(UTC): 2026-09-15 00:00 → 2026-09-16 00:00 | 去重后共 **326** 篇 | 🎯 关键词命中(interests.md): ★ 9 篇 / 🧐 2 篇

### 📌 重点关注(基于研究兴趣, agent 填写)

| 推荐指数 | 论文 | 推荐理由 |
| --- | --- | --- |
| ★★★★★ | **Specifying Paxos for System Builders: Pseudocode Made Executable** — [2609.12239](https://arxiv.org/abs/2609.12239) · [📄](#20260915-2609.12239) (cs.DC) | 命中兴趣点「分布式计算与共识」的 `consensus` 与 `Paxos`(条目权重 3，`score_star`=3)。把 Paxos for System Builders 的伪代码逐行映射为 DistAlgo 可执行规约，直接执行即可自动检查、追踪、可视化协议运行，并据此发现伪代码中难以察觉的遗漏与 liveness bug——同时落在「分布式共识」与「形式化方法与验证」两条兴趣点上，是本批唯一双线命中。 |
| ★★★★☆ | **Supermartingale Certificates for Parametric MDPs** — [2609.12715](https://arxiv.org/abs/2609.12715) · [📄](#20260915-2609.12715) (cs.LO) | 命中兴趣点「形式化方法与验证」的 `formal verification`(权重 3)。用参数扁平化变换把参数化 MDP 化为语义等价的非参数 MDP，提出参数化上鞅证书，给出首个适用于一般可测状态/动作空间的参数化 MDP 验证与近似综合算法。概率系统的形式化验证，属画像核心区。 |
| ★★★★☆ | **Shards on a Shoestring: Empirical Characterization of NEAR Protocol Nightshade Sharding on Commodity Hardware** — [2609.12091](https://arxiv.org/abs/2609.12091) · [📄](#20260915-2609.12091) (cs.DC) | 命中兴趣点「分布式计算与共识」的 `BFT`(权重 3)。首次在商用硬件(48 核 Chameleon 裸机)上独立实测分片区块链：分片数 N=1→24 全扫描，量化 BFT finality、witness gossip 流水线与磁盘 I/O 三类瓶颈；聚合 TPS 在 N=8 见顶(+40%)后回落，单分片 TPS 至 N=24 衰减 23×。补足官方 ~$700/h 云上基准的不可复现缺口，对分片事务吞吐的实证基线有直接参考价值。 |

> 排除说明：`consensus` 另有 4 次命中(2609.12394 / 2609.12949 / 2609.12331 / 2609.12243)均为「模型/采样/群体一致性」语境(多数投票、SMC 重采样的一致性、swarm 优化)，非分布式共识协议，**不计入**推荐；`formally verified` 命中 2609.12106 见下方视野扩展。

### 🧐 视野扩展(agent 填写)

| 推荐指数 | 论文 | 推荐理由 |
| --- | --- | --- |
| 🧐🧐🧐🧐 | **A Non-constant Lower Bound for Grammar-Based Compression with Greedy** — [2609.12106](https://arxiv.org/abs/2609.12106) · [📄](#20260915-2609.12106) (cs.DS) | 命中扩展点「计算机辅助证明与趣味组合」的 `formally verified`(权重 3)，同时命中兴趣点侧的 `formal verification`。把 Greedy 文法压缩近似比下界从常数推进到 Ω(log n / log log n)，解决悬置 20 余年的问题，且下界本身在 **Lean 4** 中形式化验证——计算机辅助证明的范例。 |
| 🧐🧐🧐🧐 | **Invisible Yet Dominant: Big Stalls of Kernel I/O Mechanisms in Cloud OLTP Databases** — [2609.12597](https://arxiv.org/abs/2609.12597) · [📄](#20260915-2609.12597) (cs.DB) | **关键词未命中(score=0)，按 cs.DB 领域相关性人工补充**。用 eBPF 在内核内观测 buffered I/O 的 writeback 限流停顿：单 flusher 线程 + 高延迟浅队列导致 `iostat` 与所有标准计数器都看不见的大停顿，连触发脏页回收的读也会被拖住。与事务系统尾延迟/存储栈直接相关。⚠️ 画像目前缺此类关键词，建议给「事务隔离与数据库一致性检测」增补 `tail latency` / `writeback` / `OLTP` 一类词条。 |
| 🧐🧐🧐 | **Behavior Quotient Learning for Low-Rank Adaptation of LLM Agents** — [2609.12896](https://arxiv.org/abs/2609.12896) · [📄](#20260915-2609.12896) (cs.LG) | 命中扩展点「LLM 与形式化/系统的交叉」的 `LLM-based agent`(权重 3)。在固定 rank 预算下用局部行为商流形重加权轨迹更新、并在切空间内做保决策分布的压缩，属 LLM agent 能力组织方式的系统侧改造。与形式化/系统交叉方向仅弱相关，作视野扩展。 |

### 分类清单

#### math.LO (5)

- <a id="20260915-2609.12402"></a>**Effective recurrence for computable measure-preserving transformations** — [2609.12402](https://arxiv.org/abs/2609.12402) | cross: math.DS  
  Joey Veltri  
  We prove several necessary and sufficient conditions under which a point satisfies the Poincar\'e Recurrence Theorem for all computable (ergodic) measure-preserving transformations and all sets of a particular complexity. The necessary conditions are obtained by constructing specific measure-preserving transformations which violate recurrence.
- <a id="20260915-2609.12581"></a>**Fra\"iss\'e's conjecture, partial impredicativity and well-ordering principles, part II** — [2609.12581](https://arxiv.org/abs/2609.12581)  
  Anton Freund, Katarzyna W. Kowalik, Davide Manca  
  We exhibit a well-ordering principle that is equivalent to a theory of partial impredicativity. The latter goes back to Towsner and relates to recent work of Suzuki and Yokoyama.
- <a id="20260915-2609.12740"></a>**Finite-tower bounds for Skolem functions** — [2609.12740](https://arxiv.org/abs/2609.12740)  
  Andreas Weiermann  
  We bound the eventual order types of Skolem functions below finite exponential towers. Writing $E_0(u)=u$, $E_{n+1}(u)=2^{E_n(u)}$, and $\omega_0=1$, $\omega_{k+1}=\omega^{\omega_k}$, the argument gives \[ |\Sk_{<E_n(x^m)}|<\omega_{r_n},\qquad r_n=2+\frac{n(n+3)}2\quad(n\ge1,\ m\ge2\text{ fixed}).
- <a id="20260915-2609.12916"></a>**Small masas of the Calkin algebra in the Cohen model** — [2609.12916](https://arxiv.org/abs/2609.12916) | cross: math.FA, math.GN, math.OA  
  Piotr Koszmider  
  We show that maximal abelian C*-subalgebras (masas) of the Calkin algebra (the algebra of all bounded operators on the separable Hilbert space modulo compact operators) may consistently have their densities strictly less than continuum and we describe many isomorphism types of such masas. Specifically, we prove that after adding any number of Cohen reals to a model of CH the algebra …
- <a id="20260915-2609.12031"></a>**The Borel complexity of conjugacy for Cantor minimal systems** — [2609.12031](https://arxiv.org/abs/2609.12031) | cross: math.LO  
  Xinan Dai, Wenhao Deng, Yingdong Shi, Tailin Wu et al.  
  We prove that conjugacy of minimal homeomorphisms of the Cantor space is Borel bireducible with isomorphism of countable graphs, answering the Cantor minimal case of a question of Foreman. We obtain the lower bound by encoding countably based profinite groups.

#### cs.AI (132)

- <a id="20260915-2609.12394"></a>**BlueLM-GUI Technical Report: A Real-Device-Centric Flywheel for Self-Improving Mobile GUI Agents** — [2609.12394](https://arxiv.org/abs/2609.12394) | 🎯★ consensus  
  Tong Ye, Kunyang Han, Guozhi Wang, Longqiang Luo et al.  
  Mobile GUI agents are shifting from multi-module frameworks to native models trained end-to-end, yet industrial deployment faces three persistent gaps. Sandbox training produces a distribution mismatch with production environments; expensive real-device failures remain underutilized; and fixed benchmarks saturate, losing the power to guide iteration.
- <a id="20260915-2609.12949"></a>**EduFair-Bench: Evaluating Pedagogical Fairness of LLM Tutors Across Student Demographics** — [2609.12949](https://arxiv.org/abs/2609.12949) | 🎯★ consensus  
  Jiaxu Zhao, Bahar Radmehr, Fares Fawzi, Tanya Nazaretsky et al.  
  Large language models (LLMs) are increasingly deployed as tutors, but it is unclear whether they support all students equally well. We introduce \textbf{EduFair-Bench}, a benchmark for auditing the pedagogical fairness of LLM tutors---whether tutoring quality varies systematically with student demographics.
- <a id="20260915-2609.12243"></a>**Chopthin-Consensus Power Sampling: A Diversity-Preserving Approach to LLM Decoding** — [2609.12243](https://arxiv.org/abs/2609.12243) | cross: cs.AI, stat.ML | 🎯★ consensus  
  Minoo Ahmadi, Seyedarmin Azizi, Erfan Baghaei Potraghloo, Mehdi Kamal et al.  
  Inference-time power sampling via Sequential Monte Carlo (SMC) can substantially improve large language model (LLM) reasoning without requiring post-training. However, many existing SMC approaches rely on equal-weight resampling, which can aggressively prune low-weight trajectories, discarding potentially correct reasoning paths and degrading the genealogical diversity of the search space.
- <a id="20260915-2609.11977"></a>**Occamy-1.0: Open Pareto-frontier 35B Intelligence for Co-work** — [2609.11977](https://arxiv.org/abs/2609.11977)  
  Wenhui Chen, Shiwen Cheng, Hao Dong, Chenda Duan et al.  
  Co-work agents execute complex workflows that combine information gathering, tool use, coding, and file manipulation across many model invocations. Because cost and latency accumulate over the full episode, their practical value depends not only on peak capability but also on how efficiently that capability is delivered.
- <a id="20260915-2609.11987"></a>**Harness or Model? Isolating the Harness Effect in Agentic Coding with a Contamination-Controlled Private Suite** — [2609.11987](https://arxiv.org/abs/2609.11987) | cross: cs.CL, cs.SE  
  Mohsen Arjmandi  
  An agentic coding system couples a language model to a harness: the tools, prompts and control flow that turn a chat model into an autonomous software engineer. Vendors ship harnesses tuned to their own models, and practitioners assume the vendor-native pairing solves more tasks.
- <a id="20260915-2609.12035"></a>**Reading the Whole Heart: Latent-Attention Masked Autoencoders for Multimodal Cardiac Representation Learning** — [2609.12035](https://arxiv.org/abs/2609.12035)  
  Andrea Agostini, Simon B\"ohi, Moritz Vandenhirtz, Samuel Ruiperez-Campillo et al.  
  Cardiovascular diagnosis rests on integrating complementary modalities, like ECG, echocardiography, chest radiographs, and clinical variables, each capturing distinct but correlated aspects of cardiac physiology. Yet most medical foundation models remain modality-specific, combining modalities only for finetuning or post-training.
- <a id="20260915-2609.12101"></a>**Competence-Gated Pooling of Language Models and Priors for Event Forecasting** — [2609.12101](https://arxiv.org/abs/2609.12101)  
  Aditi Tiwari, Aashrith Bandaru, Heng Ji  
  In hybrid forecasting, a language model is often one of several available signals. A system may already have a market, crowd, or statistical forecast and must decide whether the model adds useful information or should be ignored.
- <a id="20260915-2609.12105"></a>**Language Is an Insufficient Substrate for Quantitative Reasoning, and Consequential Domains Need Large Quantitative Models** — [2609.12105](https://arxiv.org/abs/2609.12105) | cross: cs.LG  
  Reuben Vandeventer, David Imrem, David J. Wild  
  The prevailing assumption in applied machine learning is that progress on consequential quantitative decisions such as pricing risk, allocating capital, triaging patients, or containing a network intrusion will follow from progress in large language models (LLMs). A language model is trained on a representation of the world that was produced by human description; description is a lossy encoding …
- <a id="20260915-2609.12115"></a>**DU-NO: A Parameter-Efficient Double U-Shaped Neural Operator for Phase-Resolving Wave Modeling** — [2609.12115](https://arxiv.org/abs/2609.12115)  
  Enrique Hernandez Noguera, Md Meftahul Ferdaus, Nathan Cooper, Elias Ioup et al.  
  Phase-resolving wave models such as FUNWAVE-TVD are the accuracy standard for nearshore dynamics, resolving the shoaling, refraction, and breaking of individual waves, but their cost rules them out for the ensembles, uncertainty quantification, and real-time warning that operational forecasting demands. Neural operators promise solver-level accuracy at a fraction of that cost, yet on …
- <a id="20260915-2609.12116"></a>**When Successful Knowledge Graph Edits Displace Correct Answers: Rank-Level Locality beyond Parameter Support** — [2609.12116](https://arxiv.org/abs/2609.12116)  
  Yi-Cheng Lai, Jerry Wang, Hsin-Ling Hsu, Li-Chu Chi et al.  
  Editing a knowledge graph embedding (KGE) model to promote a desired answer can displace correct answers from the returned list. Locality tests based only on facts that reuse the edited parameter can miss this ranking effect.
- <a id="20260915-2609.12139"></a>**Mined from Scientific Literature: Process Schemas for Atomic Layer Deposition and Etching in Materials Science** — [2609.12139](https://arxiv.org/abs/2609.12139) | cross: cond-mat.mtrl-sci  
  Sameer Sadruddin, Eleni Poupaki, Alex Watkins, Bora Karasulu et al.  
  Atomic layer deposition (ALD) and atomic layer etching (ALE) are reported heterogeneously across experimental and simulation literature in materials science, hindering comparison and machine-actionable reuse. We present four domain-expert-reviewed JSON Schemas for ALD and ALE experimental and simulation processes.
- <a id="20260915-2609.12162"></a>**Can LLMs in Draft-Verify-Revise Pipelines Resolve Deictic Ambiguity?** — [2609.12162](https://arxiv.org/abs/2609.12162) | cross: cs.CL  
  Obinna I. Ekekezie  
  Draft-verify-revise is a common LLM orchestration pattern for scaling inference-time compute. One LLM drafts, a second critiques the draft and provides feedback, and a third uses that feedback to revise the draft into the final output.
- <a id="20260915-2609.12165"></a>**GLARE: Generative Learning via Adversarial Reward Estimation For Social Dynamics Forecasting** — [2609.12165](https://arxiv.org/abs/2609.12165)  
  Tenghao Huang, Zhaoxuan Tan, Muhao Chen, Jonathan May et al.  
  Meeting continuation requires tracking the agenda, speaker roles, participant intentions, and disagreement across long multi-party discussions. We introduce the Meeting Dynamic Forecasting Benchmark (MDFB), constructed from 2,207 real-world meetings and 24,794 future-facing queries.
- <a id="20260915-2609.12171"></a>**WinSyn: An Automated Pipeline for Realistic Enterprise Question-Answering Evaluation** — [2609.12171](https://arxiv.org/abs/2609.12171)  
  Amey Varhade, Ananya Sutradhar, Ravishankar Krishnaswamy, Navin Goyal  
  Enterprise settings provide a challenging environment for question-answering agents, which often rely on Retrieval-Augmented Generation, Deep Research (DR), and related techniques. Much of this challenge comes from the complexity of enterprise data: information is often spread across evolving and potentially conflict- ing emails, chat messages, documents, and other artifacts.
- <a id="20260915-2609.12247"></a>**Soft Symbol Grounding for Prototypical Concepts** — [2609.12247](https://arxiv.org/abs/2609.12247)  
  Marcos Galv\'an-L\'opez, Nijesh Upreti, Hiram Calvo, Carlos Aguilar-Ib\'a\~nez et al.  
  Neuro-symbolic models are usually trained with supervision only on final labels, leaving the intermediate concepts unobserved. Since many concept assignments are consistent with a given label, training can predict labels correctly while recovering the wrong concepts, a failure known as a reasoning shortcut.
- <a id="20260915-2609.12265"></a>**GTA: Graph Theory Agent and Benchmark for Algorithmic Graph Reasoning with LLMs** — [2609.12265](https://arxiv.org/abs/2609.12265)  
  Zixiang Xu, Yanbo Wang, Chenxi Wang, Lang Gao et al.  
  Large Language Models (LLMs) are increasingly asked to reason over structured data such as graphs, yet how reliably they can carry out multi-step graph algorithms in language remains unclear. Existing evaluations tend to use simple tasks on small graphs, to score code generation rather than reasoning over the graph itself, or to fix a single input format.
- <a id="20260915-2609.12267"></a>**Learning Symbolic Constraint Representations from Examples: A Neuro-Symbolic Approach** — [2609.12267](https://arxiv.org/abs/2609.12267)  
  Nassim Belmecheri, Arnaud Gotlieb, Nadjib Lazaar, Helge Spieker  
  Learning user-defined concepts as constraint networks has been extensively studied in the constraint acquisition (CA) literature. However, existing approaches typically rely on intensive interactions with a human oracle, making the learning process costly in terms of time and number of queries.
- <a id="20260915-2609.12286"></a>**T-GADE: Thermodynamical Generative-AI-Driven Evolution of LLM Artifacts** — [2609.12286](https://arxiv.org/abs/2609.12286) | cross: cs.NE  
  Kyoko Ogawa, Naoki Mori  
  Integrating evolutionary computation and large language models (LLMs) requires control of population diversity as well as generative capability. Among LLM outputs, those with explicit structure, such as a description paired with code, are structured artifacts; we use artifact for short.
- <a id="20260915-2609.12287"></a>**Robust Prototypical Networks for Few-Shot Sensor Fault Diagnosis** — [2609.12287](https://arxiv.org/abs/2609.12287) | cross: cs.LG  
  Mohammed Ayalew Belay, Amirshayan Haghipour, Pierluigi Salvo Rossi  
  Industrial fault diagnosis often operates with only a handful of labeled fault examples, making few-shot learning attractive for sensor monitoring. Standard prototypical networks are simple and effective; however, their class prototypes may become unstable in the very-low-shot regime because each decision relies on a small support set.
- <a id="20260915-2609.12304"></a>**Hybrid Physics-AI Framework of Body Center of Mass Dynamics from Wrist-Worn Sensors** — [2609.12304](https://arxiv.org/abs/2609.12304) | cross: eess.SP  
  Shuhao Que, Valentina Breschi, Ying Wang  
  Wrist-worn IMU has been widely used for daily-life health monitoring. Yet, it does not fully represent whole-body dynamics, for which the body center of mass (COM) is considered the physiological reference standard.
- <a id="20260915-2609.12313"></a>**Do Influence-Derived Data Perturbations Enable Machine Unlearning? A Controlled Study of Three Plausible Roles** — [2609.12313](https://arxiv.org/abs/2609.12313)  
  Chenkai Wu, Chrispine Kambimbi, Qinyang Zeng, Jun Yan  
  We evaluate Deep Perturbation Learning (DPL), which perturbs training images and labels along influence-derived directions, in three roles in which prior work has positioned it for machine unlearning: a direct deletion signal (the strongest claim), a utility-preserving regularizer, and a warm start for adversarial unlearning. Evidence for the weaker roles has been used to support the stronger …
- <a id="20260915-2609.12320"></a>**AIM: A Privacy-Aware Interoperable Memory Framework for Multi-Agent Multi-User LLM Systems** — [2609.12320](https://arxiv.org/abs/2609.12320) | cross: cs.LG  
  Zachary Johnson, Nigel Boachie Kumankumah, Somya Chatterjee, Tejas Sathyamurthi et al.  
  Traditional large language models (LLMs) are scoped to individual user sessions, limiting their knowledge to a single conversation and preventing them from learning user preferences that evolve over time. Existing agentic memory systems address this limitation but generally operate at the individual-user level, restricting the public knowledge that could be shared across users to improve …
- <a id="20260915-2609.12322"></a>**Affective Agent: On-Device Personalized Intervention Reasoning for Wearable Systems** — [2609.12322](https://arxiv.org/abs/2609.12322) | cross: cs.LG  
  Reina Mun, Zishen Wan, Vijay Janapa Reddi  
  Affective computing has advanced wearable state inference, but on-device reasoning about whether, when, and how to intervene remains challenging. We present Affective Agent, a three-layer reference architecture for personalized intervention reasoning under uncertainty on wearable-class hardware.
- <a id="20260915-2609.12327"></a>**LoRA-RC: Reservoir Computing with Low-Rank Adaptation** — [2609.12327](https://arxiv.org/abs/2609.12327) | cross: cs.LG, cs.SY, eess.SY, math.DS  
  Wenbin Wan  
  Reservoir computing (RC) trains only a linear readout over a fixed recurrent layer, making it fast and data-efficient for online prediction. However, a static reservoir degrades under system drift, readout-only adaptation is then insufficient, and unconstrained reservoir adaptation can destroy the echo-state and incremental stability properties that make RC reliable.
- <a id="20260915-2609.12373"></a>**Toward Robust Personalized Alignment for LLMs: Mitigating Persona Drift in Multi-Turn Dialogue** — [2609.12373](https://arxiv.org/abs/2609.12373)  
  Youyuan Zhang, Siyuan Li, Fangming Liu, Jing Li  
  Persona drift remains a central challenge for personalized language models, as user profiles evolve over long interactions rather than remain permanently fixed. Models must therefore revise persistent persona states when preferences genuinely change, while avoiding updates driven by transient, ambiguous, or unresolved observations.
- <a id="20260915-2609.12395"></a>**Is Gaussian Splatting Becoming Neural Again? A Taxonomy and Controlled Study of Learned Parameterization** — [2609.12395](https://arxiv.org/abs/2609.12395)  
  YuanHang Wang, Xin Cao, Yi Zhang  
  Three-dimensional Gaussian Splatting (3DGS) combines explicit primitives with efficient rasterization, yet recent systems increasingly use neural networks to generate or share Gaussian parameters. We characterize this trend along five axes: attribute decoding, spatial sharing, view-conditioned decoding, topology generation, and amortized inference.
- <a id="20260915-2609.12398"></a>**Niching Agents in The Core** — [2609.12398](https://arxiv.org/abs/2609.12398)  
  Gary B. Parker, Jim O'Connor, John Asaro  
  The Core is a unique competitive co-evolution algorithm that allows agents to evolve autonomous control without utilizing a traditional fitness function. The agents evolve via local interactions through tournament selection, crossover, and mutation, producing offspring by evolving better controllers.
- <a id="20260915-2609.12399"></a>**OneLA: Scaling Linear-Attention Decoding to Large Beams in Generative Recommendation** — [2609.12399](https://arxiv.org/abs/2609.12399) | cross: cs.DC, cs.IR  
  Xiangrui Yang, Cheng Peng, Yunfeng Zhao, Liang Zeng et al.  
  Generative recommendation (GR) relies on large-beam decoding to generate hundreds of candidate items, creating a new scaling challenge for recurrent linear attention. Existing linear attention serving systems either materialize a full recurrent state for every beam or repeatedly replay shared history, incurring substantial memory and traffic overhead.
- <a id="20260915-2609.12400"></a>**Decentralized Evolution of Hexapod Gaits with Independent Leg Controllers** — [2609.12400](https://arxiv.org/abs/2609.12400) | cross: cs.RO  
  Gary B. Parker, John Asaro, Jim O'Connor  
  This paper presents a novel approach to hexapod locomotion by evolving each leg's gait independently through a decentralized evolutionary algorithm. Using the Webots simulator and the Mantis hexapod robot, we optimize individual leg controllers without centralized coordination, allowing emergent behaviors to drive the development of efficient, coordinated locomotion.
- <a id="20260915-2609.12403"></a>**Beyond ID Embeddings: Process-Grounded Language Modeling for Cognitive Diagnosis** — [2609.12403](https://arxiv.org/abs/2609.12403) | cross: cs.CL  
  Minghang Liu, Yuanzhuo Wang, Qiang Qiu, Huawei Shen et al.  
  Cognitive Diagnosis Models (CDMs) play a pivotal role in personalized online learning. Traditional CDMs rely on discrete, ID-based embeddings to represent students, exercises, and concepts.
- <a id="20260915-2609.12404"></a>**VRL-Bench: Benchmarking agents on computer control tasks under finite trial budgets** — [2609.12404](https://arxiv.org/abs/2609.12404)  
  Yu Bai, Yukai Miao, Dawei Wang, Li Chen et al.  
  Learning from trial and error is a promising way to improve language agents on complex tasks such as computer control. Reflexion introduced verbal reinforcement learning, which turns failed trials into text that guides later attempts without updating model parameters.
- <a id="20260915-2609.12413"></a>**SoK: Rethinking Jailbreaking in the Era of Agentic AI: Attacks, Defenses, and Practical Consideration** — [2609.12413](https://arxiv.org/abs/2609.12413)  
  Md Jueal Mia, Yanzhao Wu, Selcuk Uluagac, M. Hadi Amini  
  Large language models (LLMs) are rapidly evolving from conversational assistants into agentic AI systems that reason, plan, invoke tools, maintain persistent memory, communicate with other agents, and execute multi-step tasks. At the same time, modern models exhibit substantially stronger native safety alignment than earlier generations on which many jailbreak attacks and defenses were originally …
- <a id="20260915-2609.12422"></a>**Hierarchical Belief Modeling for Zero-Shot Opponent Adaptation in Partially Observable Multi-Agent Navigation** — [2609.12422](https://arxiv.org/abs/2609.12422) | cross: cs.MA  
  Kowei Shih, Lu Cheng, Zeyu Wang, Yeyun Xu et al.  
  Lux AI Season 3 requires agents to act under partial observability, randomized episode level dynamics, and a best of five match structure that rewards both tactical execution and fast adaptation. We present HORIZON, a hierarchical agent that combines symmetry aware spatial perception, dual memory belief tracking, relic centric graph attention, information gain driven exploration, and an opponent …
- <a id="20260915-2609.12436"></a>**LifeFuse-Mem: Lifecycle-Aware State Fusion Against Temporary Overwriting for Long-Term Memory** — [2609.12436](https://arxiv.org/abs/2609.12436)  
  Hanyu Zhao, Yuqian Feng, Zhenyu Song, Yuanchao Cheng et al.  
  Long-running LLM agents require memory mechanisms that maintain coherent internal states across interactions. We study a lifecycle-labeled memory setting in which write episodes provide lifecycle metadata during training, and phase-aware readout is used during evaluation.
- <a id="20260915-2609.12446"></a>**Do LLMs Trust the Accuser or the Accusation? Measuring Belief Shifts in Werewolf** — [2609.12446](https://arxiv.org/abs/2609.12446) | cross: cs.CL  
  Yu-Yu Yang, Ti-Rong Wu, Hung Guei, Hsing-Yu Chen et al.  
  Social-deduction games such as Werewolf are increasingly used to evaluate LLM agents, but existing evaluations often rely on final game outcomes. We propose a belief-shift evaluation benchmark in Werewolf for analyzing communication skills through belief updating.
- <a id="20260915-2609.12459"></a>**EvoRS: On-Policy Self-Evolution of Reward Systems for Open-Ended Reinforcement Learning** — [2609.12459](https://arxiv.org/abs/2609.12459)  
  Weiyuan Li, Aili Chen, Xintao Wang, Yikai Zhang et al.  
  Open-ended reinforcement learning often relies on rubric-based rewards for tasks without directly verifiable answers. Yet the policy and reward system form a dynamic feedback loop: as the policy optimizes the current reward, an initially useful reward system may become unreliable due to reward hacking or reduced response discriminability.
- <a id="20260915-2609.12464"></a>**Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration** — [2609.12464](https://arxiv.org/abs/2609.12464)  
  Nilesh Jaiswal, Aniket Agrawal, Arjit Shukla, Divya Malhotra et al.  
  As enterprises modernize legacy monolithic systems to microservices, Large Language Models (LLMs) are heavily utilized for automated code translation. However, traditional vector-based Retrieval-Augmented Generation (Standard RAG) struggles to capture topological relationships.
- <a id="20260915-2609.12472"></a>**TripPattern: A Pattern-based Text Watermarking Method for Large Language Models** — [2609.12472](https://arxiv.org/abs/2609.12472)  
  Sangjun Moon, Dasom Choi, Jingun Kwon, Hidetaka Kamigaito et al.  
  Text watermarking techniques have gained significant attention for identifying machine-generated text and mitigating risks from large language models (LLMs). Existing methods typically divide an LLM's vocabulary into green and red tokens, but encouraging generation toward green tokens can reduce text quality and naturalness.
- <a id="20260915-2609.12482"></a>**When Does AI Augment Work? A Workflow-Level Framework for Human-Agent Collaboration** — [2609.12482](https://arxiv.org/abs/2609.12482) | cross: cs.CY, cs.HC  
  AI Collaboration, Jiaying Wu, Caleb Ziems, Raymond Chan et al.  
  We aim to characterise the value of artificial intelligence in the workplace. Current studies largely measure this value in terms of the current automation capabilities and public adoption of AI.
- <a id="20260915-2609.12489"></a>**Confidence-Gated Transductive Test Generation for Code Reranking** — [2609.12489](https://arxiv.org/abs/2609.12489) | cross: cs.CL, cs.SE  
  Sungjae Lee, Youngsik Yoon, Seockbean Song, Siwei Wang et al.  
  Test case synthesis is crucial for evaluating and ranking programs generated by large language models (LLMs). However, constructing high-quality test cases remains challenging because reliable expected outputs are often difficult to obtain.
- <a id="20260915-2609.12495"></a>**Information Specialization and Constrained Synthesis in Multi-Agent LLM Forecasting: A Prospective Live-Study of the 2026 FIFA World Cup** — [2609.12495](https://arxiv.org/abs/2609.12495) | cross: cs.CL  
  Julian Varghese, Lucas Bickmann, Sarah Sandmann  
  Large language models are being organized into multi-agent systems with specialized roles, but whether such specialization produces distinct forecasts and whether subsequent synthesis improves utility remains unclear. In this study, we carried out a live, prospective evaluation over the final 56 matches of the information-dense 2026 FIFA World Cup, keeping a frontier foundation model constant …
- <a id="20260915-2609.12578"></a>**From Collaboration to Capability: Internalizing Routed LLM Experts into Compact Reasoners** — [2609.12578](https://arxiv.org/abs/2609.12578)  
  Frank Nie, Shuyao Wang, Ethan B. Liu  
  A compact controller can coordinate stronger experts by selecting whom to consult, formulating requests, and integrating their responses. We study whether learning from both the controller's decisions and the experts' reasoning and code improves its generation after expert removal.
- <a id="20260915-2609.12586"></a>**Reproducing and Evaluating the Generalizability of Subliminal Learning in Open-Weight Models** — [2609.12586](https://arxiv.org/abs/2609.12586)  
  Daan van der Weijden, Nathan Brack, Selene Baez Santamaria  
  In this reproduction paper we investigate subliminal learning, a consequence of distillation where teacher models transmit behavioral preference traits through semantically unrelated data. The original paper explores two types of traits (animal preferences and misalignment), three data modalities (number sequences, code, and chain of thought), and several model families.
- <a id="20260915-2609.12606"></a>**Beyond Generation and Accuracy: Diagnosing and Enhancing Visual Chain-of-Thought for Geometry Problem Solving** — [2609.12606](https://arxiv.org/abs/2609.12606)  
  Zhitong Dong, Jicai Pan, Yingguo Gao, Jingting Ding et al.  
  While multimodal reasoning has advanced rapidly, solving complex geometry problems critically hinges on active visual assistance, such as constructing auxiliary lines, spurring the rise of Visual Chain-of-Thought (VCoT). However, existing evaluations typically assess visual generation quality and final answer accuracy in isolation, failing to examine whether intermediate visual aids are …
- <a id="20260915-2609.12623"></a>**SteerDuplex: Steerable Duplex Speech Dialogue Models** — [2609.12623](https://arxiv.org/abs/2609.12623) | cross: cs.CL  
  Utkarsh Tyagi, Ramaneswaran Selvakumar, Advait Gosai, Sonal Kumar et al.  
  Full-duplex spoken dialogue models support low-latency turn taking, interruption handling, and backchanneling, yet a key capability remains underexplored: steerability, the ability to reliably shift conversational behavior along attributes such as tone, persona, speaking rate, and voice style in response to user instructions. We introduce a taxonomy of text- and audio-based steerability that …
- <a id="20260915-2609.12684"></a>**Generative AI Use Cases In Real Estate Marketing: Adoption and Constraints in Germany** — [2609.12684](https://arxiv.org/abs/2609.12684) | cross: cs.HC  
  Victor Kolominsky-Rabas, Leopold M\"uller, Felicia Perpina, Niklas K\"uhl  
  Generative artificial intelligence (GenAI) is changing how work is organized and performed. Real estate marketing is a prime example of this, yet evidence of GenAI in real estate agents' day-to-day practice remains scarce.
- <a id="20260915-2609.12686"></a>**Residual Vector-based Reconstruction as Long-Context Recall Regardless of Context Window Size** — [2609.12686](https://arxiv.org/abs/2609.12686) | cross: cs.CL  
  MyungHoon Ryu, XinYu Piao, Jong-Kook Kim  
  Large language models (LLMs) process long contexts, including long documents and lengthy conversations, but face token-level memory usage that increases proportionally to input length. Although model optimization and lossy prompt compression are widely used, these methods still fail to solve the long-context recall problem beyond pretrained and size-constrained context windows.
- <a id="20260915-2609.12694"></a>**I Am AdMan: A Pipeline for Automatic Generation of Personalized Advertising Imagery** — [2609.12694](https://arxiv.org/abs/2609.12694) | cross: cs.HC  
  Victor Kolominsky-Rabas, Leopold M\"uller, Claudius Budcke, Niklas K\"uhl  
  Personalized marketing can increase customer engagement, satisfaction, and conversion. While existing personalization approaches have become effective at matching the right product to the right customer, the visual representation of advertisements remains generic and only weakly tailored to the individual.
- <a id="20260915-2609.12697"></a>**Enabling and Understanding Personalization in AI-Generated Advertising Imagery** — [2609.12697](https://arxiv.org/abs/2609.12697) | cross: cs.HC  
  Victor Kolominsky-Rabas, Leopold M\"uller, Claudius Budcke, Claas Christian Germelmann et al.  
  Personalized marketing traditionally matches static products to customers, while dynamic creative optimization focuses mainly on AI-driven text personalization or basic product image modifications. We address this gap by developing and implementing an AI-based framework that generates personalized advertising imagery directly from customer data.
- <a id="20260915-2609.12704"></a>**Implicit Personality Representations in Humans and LLMs** — [2609.12704](https://arxiv.org/abs/2609.12704)  
  Yilin Geng, Omri Abend, Eduard Hovy, Lea Frermann  
  A century of psychology has found that the trait words people use to describe one another vary, but the relational structure among those traits, which ones go together and which oppose, is strikingly consistent across raters and cultures. We test whether the LLM (Qwen 2.5-7B-Instruct) reproduces this structure in its internal trait representations.
- <a id="20260915-2609.12718"></a>**When Rubrics Fail: Hallucinations Reveal Blind Spots in Medical AI Evaluation** — [2609.12718](https://arxiv.org/abs/2609.12718)  
  Griffin Farrow, Lily Sijia Li, Jack Johnson, Tingyan Wang et al.  
  Hallucinations can undermine clinician trust in LLMs, making it important that evaluation methods capture clinically relevant errors. Rubric-based evaluation has become the leading approach for assessing LLMs in medicine, but it is unclear whether rubric scores reflect such errors.
- <a id="20260915-2609.12742"></a>**Skill Issue: Lessons from Optimizing Repository SKILLs for Coding Agents** — [2609.12742](https://arxiv.org/abs/2609.12742)  
  Mykhailo Kozyrev, Andrei Kozyrev, Anton Podkopaev  
  Coding agents increasingly read repository knowledge from SKILLs --- plain \texttt{.md} files versioned alongside the code. Recent work synthesizes these files automatically, by optimizing the document against a benchmark.
- <a id="20260915-2609.12746"></a>**What Drives Recovery in Agentic Text-to-Cypher? LAST-CQ: An LLM Agent Self-Refinement Framework** — [2609.12746](https://arxiv.org/abs/2609.12746) | cross: cs.CL, cs.LG, cs.MA, cs.SE  
  Ioannis Prokopiou, Athanasios Aidinis, Panagiotis-Christos Kyrmpatsos, Pantelis Vikatos  
  Agentic pipelines for structured-query generation are rapidly expanding, but it is unclear which part of the loop produces the gain. We use LAST-CQ -- a five-agent, training-free, execution-grounded Text-to-Cypher framework -- as an instrumented testbed, running three counterfactuals over 2,471 live-database queries and six backbones spanning three vendor scale tiers.
- <a id="20260915-2609.12747"></a>**Assisted Spatial Cognition Through Vision-Language Models** — [2609.12747](https://arxiv.org/abs/2609.12747)  
  H. Riaz, J. B. Fernandez, I. Mills, D. Hickey et al.  
  Multimodal AI, powered by Large Language Models (LLMs) and Vision-Language Models (VLMs), is transforming assistive technologies by enabling simultaneous processing of visual and textual data. This advancement holds significant promise for over 43 million visually impaired and neuro-divergent individuals worldwide who face persistent challenges in navigating indoor and outdoor environments due to …
- <a id="20260915-2609.12749"></a>**SCQ: Stabilizing Conservative Q-Learning with Sigmoid-Bounded Entropy** — [2609.12749](https://arxiv.org/abs/2609.12749)  
  Xiefeng Wu, Shu Zhang, Zhaojie Chu, Mingyu Hu  
  Offline-to-online reinforcement learning reduces interaction cost for real-world robot learning but suffers from persistent value estimation instability. Existing methods address this through pessimistic regularization, lower-bound calibration, and architectural normalization, but an overlooked source of instability lies in the entropy formulation: the standard log-entropy term can become …
- <a id="20260915-2609.12769"></a>**Unified Agentic Video Editing Across Levels of Complexity and Creativity** — [2609.12769](https://arxiv.org/abs/2609.12769) | cross: cs.HC, cs.MM  
  Surabhi S. Nath, Kim Ferres, Milan Petrovi\'c, Lion Schulz  
  Editing is a core component of video production, requiring creative planning and decisions under multiple constraints. Here, we report methods for agentic tooling for automated video editing across three tasks varying in editorial goal, complexity and creativity, namely scene previews, video summaries and cinematic trailers.
- <a id="20260915-2609.12771"></a>**MPT: Missing Prototype Tracking via Barycentric Reconstruction in Vehicular Federated Learning** — [2609.12771](https://arxiv.org/abs/2609.12771) | cross: cs.CV  
  Hanju Jang (Yonsei University), Gyeongmin Han (Yonsei University), Sungmin Lee (Yonsei University), Kichang Lee (Yonsei University) et al.  
  Cross-vehicle federated learning enables vehicles to collaboratively improve perception models while keeping locally collected driving data private. However, vehicle participation is transient, and a vehicle may depart before training converges while permanently taking its local data.
- <a id="20260915-2609.12801"></a>**Interpreting the predictions of neural network classification based on a Taylor Coefficient Analysis (TCA)** — [2609.12801](https://arxiv.org/abs/2609.12801) | cross: physics.data-an  
  Markus Klute, Artur Monsch, Lars Sowa, Roger Wolf  
  We introduce a rigid and comprehensive taxonomy and paradigm for characterizing the influence of the input feature space $X$ on the predictions $\hat{y}$ of a neural network (NN) used for event classification, based on a Taylor expansion of $\hat{y}$ in $X$. The complete process of introspection we refer to as Taylor Coefficient Analysis (TCA).
- <a id="20260915-2609.12808"></a>**K-Bench: A Benchmark for LLM Unlearning in Agentic Deployments** — [2609.12808](https://arxiv.org/abs/2609.12808)  
  Guangsheng Yu, Yanna Jiang, Qin Wang, Baihe Ma et al.  
  Unlearning benchmarks such as TOFU and MUSE certify forgetting by reading the model's final answer, where a model that refuses to answer already counts as having forgotten. We show that this model-level certificate does not transfer once the model is deployed as an agent.
- <a id="20260915-2609.12822"></a>**Scaling Clinical Judgment to Evaluate Medical AI** — [2609.12822](https://arxiv.org/abs/2609.12822)  
  Thomas A. Buckley, Zahir Kanjee, Peter G. Brodeur, Byron Crowe et al.  
  Blinded physician evaluation has been considered by many to be the gold standard for assessing clinical reasoning in large language models (LLMs). This is difficult to scale; thus, prior studies typically rely on small physician panels, often from a single institution or specialty, which both limits the scientific questions investigated and makes it unclear whether findings would be reproduced …
- <a id="20260915-2609.12851"></a>**MedRoundsQA: A Persona and Difficulty Aware Evaluation for Multi-Turn Medical Consultations** — [2609.12851](https://arxiv.org/abs/2609.12851)  
  Youssef Mohamed, Ahmed Heakl, Qinrong Cui, Junhong Liang et al.  
  Medical benchmarks are dominated by single-turn, multiple-choice clinical cases that poorly reflect real consultations. Practically, clinicians elicit evidence interactively and patient communication varies widely.
- <a id="20260915-2609.12897"></a>**Tracing and Coordinating Cross-Layer Influence for Multimodal Model Merging** — [2609.12897](https://arxiv.org/abs/2609.12897)  
  Pengyang Zhou, Xiaobin Tu, Zhengxi Liu, Rongkun Xue et al.  
  Multimodal model merging aims to consolidate task experts into a single model that retains their complementary capabilities. Most unimodal model merging methods combine expert updates within individual layers, and multimodal approaches largely follow this design.
- <a id="20260915-2609.13009"></a>**How Good Are Frontier Models at Physics? Expert Re-Grading Reveals Broken Evaluations and Near-Saturation of Leading Benchmarks** — [2609.13009](https://arxiv.org/abs/2609.13009)  
  Ali Ansari, Haoran Sun, Andy Zeyi Liu, Mark Jabbour et al.  
  Low reported scores on leading physics benchmarks, including those featured in the Artificial Analysis Intelligence Index (2026), suggest that frontier language models still struggle with advanced physics, a demanding test of their scientific reasoning and quantitative problem-solving abilities. Yet this impression does not always align with domain experts' experiences using these models in their …
- <a id="20260915-2609.13047"></a>**Diffusion Models and Concept Formation** — [2609.13047](https://arxiv.org/abs/2609.13047) | cross: cs.LG  
  Zekun Wang, Karthik Singaravadivelan, Christopher J. MacLellan  
  Humans organize knowledge into a taxonomy of concepts with nested levels of abstraction and a \emph{basic level} at which people recognize and name objects with the least cognitive effort. Cobweb is a classic cognitive account of this ability, an incremental learner that builds a probabilistic concept hierarchy by maximizing category utility.
- <a id="20260915-2609.13062"></a>**Anchoring Clinical Events in Time: UID-Preserving Multimodal Reconstruction and Source-Grounded Adjudication** — [2609.13062](https://arxiv.org/abs/2609.13062)  
  Sayantan Kumar, Nicolas Grimaldi, Jack Cummins, Jeremy C. Weiss  
  Clinical timelines support treatment-window analysis and leakage-free modeling, but discharge summaries often obscure chronology and structured EHR tables describe only part of the patient course. We present a UID-preserving framework that links each narrative event occurrence to its source span and retains that identity through text-only estimation, structured-evidence retrieval, timestamped …
- <a id="20260915-2609.13073"></a>**Autonomous Research for Open-Ended Problems: A Case Study on Telecom Ticket Retrieval** — [2609.13073](https://arxiv.org/abs/2609.13073) | cross: cs.IR, cs.LG  
  Junghyun Min, Huseyin Uzunalioglu, Mohamed Trabelsi  
  Recent breakthroughs in LLM-based systems and their abilities in problem solving and coding have allowed progress in the AI for Science paradigm, potentially replacing human roles in machine learning (ML) research. However, while several frameworks of fully autonomous end-to-end ML research have been proposed, successful implementations of them are often limited to problems with narrow search …
- <a id="20260915-2609.13082"></a>**Embodied-BenchForge: A Closed-Loop Agentic Workflow for Embodied Benchmark Construction** — [2609.13082](https://arxiv.org/abs/2609.13082)  
  Baoyang Jiang, Fengchun Zhang, Leyuan Wang, Haotian Li et al.  
  Agentic systems offer a promising way to automate embodied benchmark construction, but existing approaches typically cover isolated stages or remain specialized to predefined environments and task families. More importantly, multi-step construction produces dependent intermediate artifacts that are often passed downstream without artifact-specific verification, allowing local defects to propagate …
- <a id="20260915-2609.13118"></a>**CMA-OT: Hierarchical Expert Supervision for Dance-to-Music Generation** — [2609.13118](https://arxiv.org/abs/2609.13118) | cross: cs.SD  
  Jinting Wang, Chenxing Li, Dong Yu, Li Liu  
  Dance-to-music (D2M) generation aims to synthesize music that is rhythmically and stylistically aligned with dance videos. A key challenge arises from the semantic mismatch between sparse dance cues, such as rhythm and style, and the dense information required for music composition, including structure, instrumentation, and expressive dynamics.
- <a id="20260915-2609.13125"></a>**A Hybrid LSTM-XGBoost Framework for Multi-Horizon Stock Return Prediction Across Diversified Equity Portfolios** — [2609.13125](https://arxiv.org/abs/2609.13125)  
  Seif ElDein Mostafa, Yahia Ahmed, Farah Datwish, Marwa Solayman  
  Accurate prediction of equity returns remains a major challenge in computational finance due to the non-stationary, nonlinear, and low signal-to-noise ratio nature of financial time series. This paper proposes a hybrid two-stage architecture that combines a long short-term memory (LSTM) network with an XGBoost gradient-boosted regressor for multi-horizon stock return prediction across a …
- <a id="20260915-2609.13134"></a>**Rethinking Heterogeneous System Disaggregation for Subquadratic Attention** — [2609.13134](https://arxiv.org/abs/2609.13134)  
  Arya Tschand, Yaosheng Fu, Vikram Sharma Mailthody, Nicolai Oswald et al.  
  Frontier language models are more aggressively using subquadratic attention to reduce the memory footprint and compute requirements during inference while still delivering frontier accuracy. While existing systems make dense attention-centric disaggregated serving decisions, we show that disaggregating inference around the unique arithmetic intensity and memory footprint of subquadratic attention …
- <a id="20260915-2602.09490"></a>**Robust Trust** — [2602.09490](https://arxiv.org/abs/2602.09490) | cross: cs.AI, cs.GT  
  Piotr Dworczak, Alex Smolin  
  An agent chooses an action based on her private information and a recommendation from an informed but potentially misaligned adviser. With a known probability, the adviser truthfully reports his signal; with the remaining probability, he can send any message.
- <a id="20260915-2609.11258"></a>**SoulAuth: An Actor-native Identity Architecture and Rust Reference Implementation for Humans and Long-lived AI Actors** — [2609.11258](https://arxiv.org/abs/2609.11258) | cross: cs.AI, cs.CR  
  Kun Yuan, Harold Wang, Echo Li, Egusi Gui et al.  
  As AI systems move from transient model invocations toward long-lived actors that persist across credentials, clients, sessions, and runtime instances, identity infrastructure must answer a basic question: where should the canonical continuity boundary be placed? This paper introduces Actor-native Identity and presents SoulAuth, an open-source Rust reference implementation for Humans and …
- <a id="20260915-2609.11983"></a>**Who Pays for Open Review? Visible Author Reputation and Its Effect on Ratings** — [2609.11983](https://arxiv.org/abs/2609.11983) | cross: cs.AI  
  Qinghua Zhao, Xinyu Chen, Yanhui Yang, Tengfeng Sun et al.  
  An OpenReview bug in November 2025 broke anonymity at several conferences and prompted calls for open review, which motivate us to ask what shifting from blind to open would mean for authors. Analyzing over 18,000 reviewed submissions to ICLR 2026, split into de facto open and blind groups by arXiv preprint timing, we find that ratings rise with author reputation under both mechanisms, with a …
- <a id="20260915-2609.11990"></a>**Assessment of Non-Institutional AI Tool Usage Among Clinicians** — [2609.11990](https://arxiv.org/abs/2609.11990) | cross: cs.AI  
  Sarah Pungitore, Jarrod Mosier  
  Generative artificial intelligence (AI) tools are increasingly accessible and have the potential to improve efficiency across clinical workflows. However, clinicians may also use non-institutional AI tools that are not provided, managed, or governed by their healthcare institutions, creating potential concerns related to privacy, security, accuracy, and clinician-AI interaction.
- <a id="20260915-2609.12022"></a>**Continuous Learning of Gravity Field Irregularities Around Small Bodies via Neural Hamiltonian ODEs** — [2609.12022](https://arxiv.org/abs/2609.12022) | cross: astro-ph.EP, cs.AI, math.OC, physics.space-ph  
  Giacomo Acciarini, Dario Izzo  
  We propose to learn the unknown dynamics in the proximity of a small body directly from tracking data, representing them as a feed-forward neural network embedded in the system Hamiltonian. The equations of motion form a Neural Hamiltonian Ordinary Differential Equation, whose variational equations provide exact training gradients: estimation uses position and velocity arcs at realistic noise …
- <a id="20260915-2609.12036"></a>**Pelican-Sim 1.0: A General World Model Simulator for Embodied Intelligence** — [2609.12036](https://arxiv.org/abs/2609.12036) | cross: cs.AI  
  Shilong Zou, Shilin Zhang, Yingji Zhang, Yuhang Huang et al.  
  In this technical report, we propose Pelican-Sim 1.0, a general world model simulator for embodied intelligence that predicts future observations from visual context and robot actions to support downstream learning and decision making. The model incorporates four key design features: (1) Unified action representation: a 28-dimensional action value space covering most mainstream embodiments, …
- <a id="20260915-2609.12079"></a>**Hierarchical Prototype Emergence in Modern Hopfield Models** — [2609.12079](https://arxiv.org/abs/2609.12079) | cross: cs.AI, cs.LG  
  Aditya Cowsik, Adithya Sriram  
  Hierarchical correlations are a universal feature of any realistic model of data, and the question of how associative memory models may learn these correlations and generalize beyond them to construct new sensible images is an important step towards understanding more complex modern architectures such as diffusion models. We consider a hierarchical model for memories which are sampled and stored …
- <a id="20260915-2609.12086"></a>**Creating an Atomic User Model for Personality-Aware Large Language Model Interaction** — [2609.12086](https://arxiv.org/abs/2609.12086) | cross: cs.AI, cs.CL  
  B. Sankar, Deepthika S, Pawni Yadav, Amogh A S  
  Assistants built on large language models are expected to write as their user would, and the dominant approach is single-channel: preferences summarised from conversation history and reinserted into context. This inverts the order of inference.
- <a id="20260915-2609.12097"></a>**MAIA: Multi-Agent Intent Articulation for Requirement Discovery in Art Commissions** — [2609.12097](https://arxiv.org/abs/2609.12097) | cross: cs.AI  
  Yu-Chao Wang, Yanhong Lu, Yingjie Victor Chen, Tim McGraw  
  In bespoke art commissions, laypeople know what they feel but lack the words to specify it: one participant wanted a laid-off truck driver depicted as "a ghost in his own machine" but left the medium, scale, and palette unsaid. We frame this as an articulation bottleneck at an under-served upstream stage: requirement discovery, which precedes any artist or image generator and forces the …
- <a id="20260915-2609.12107"></a>**Extracting Dataset Mentions in Forced Displacement and FCV Documents: A Weakly Supervised Framework with LLM-Based Label Refinement** — [2609.12107](https://arxiv.org/abs/2609.12107) | cross: cs.AI, cs.IR, econ.EM  
  Rafael Macalaba, Aivin V. Solatorio, Patrick Michael Brock, Olivier Dupriez  
  Development and humanitarian organizations produce and support surveys, administrative registries, and other data resources to inform research, policy, and operations, yet systematically identifying where these datasets are referenced remains difficult. Such references are dispersed across research papers, project documents, humanitarian reports, and other unstructured text, limiting both the …
- <a id="20260915-2609.12136"></a>**The Anatomy and Boundary of Adaptation under Temporal Tabular Shift** — [2609.12136](https://arxiv.org/abs/2609.12136) | cross: cs.AI  
  Tianyu Wang, Xi Vincent Wang, Lihui Wang, Mian Li et al.  
  Prequential adaptation of frozen tabular foundation models under temporal drift, with each label revealed only after prediction, helps some deployments and harms others, yet current practice does not predict which. We study the sources and limits of these gains.
- <a id="20260915-2609.12154"></a>**Neural Multichannel Distant Speaker Diarization with Heavy-tailed Source Separation Model** — [2609.12154](https://arxiv.org/abs/2609.12154) | cross: cs.AI  
  Sicheng Mao, Baihan Li, Mathieu Fontaine, Anthony Larcher et al.  
  Distant speaker diarization remains challenging due to difficult acoustic environments, varying numbers of speakers and overlapping speech. Model-driven methods are proposed to exploit the speech source features in multi-channel recordings that help diarization.
- <a id="20260915-2609.12168"></a>**USPLIT-VQA: U-Shaped Split Learning for Visual Question Answering with Contribution-Aware Weighted Aggregation** — [2609.12168](https://arxiv.org/abs/2609.12168) | cross: cs.AI  
  Md Khalid Syfullah, Alvi Ataur Khalil  
  Visual Question Answering (VQA) systems, jointly interpreting images and natural language queries, hold significant promise across many domains, yet the privacy-sensitive nature of user data creates a fundamental barrier. Centralized training requires access to all data, while federated learning requires each client to host the full model.
- <a id="20260915-2609.12170"></a>**NDT Factory: Synthesizing Verified Network Digital Twins from Semantic Models via Multi-Agent LLM** — [2609.12170](https://arxiv.org/abs/2609.12170) | cross: cs.AI, cs.MA, cs.SE  
  Sudipta Acharya, Petar Djukic, Burak Kantarci  
  Autonomous network management requires systems that can evaluate Network Service Intents (NSIs) under varying conditions without manual implementation of analysis logic, as envisioned in TM Forum Level~4 (L4) autonomy. Behavioral Network Digital Twins (NDTs) enable such evaluation, but existing NDTs rely on pre-defined analytical logic, limiting adaptability for evolving closed-loop control.
- <a id="20260915-2609.12184"></a>**Agentic TCAD Calibration Workflow for Oxide Semiconductor Transistors** — [2609.12184](https://arxiv.org/abs/2609.12184) | cross: cs.AI, cs.LG, physics.app-ph  
  Gyujun Jeong, Junmo Lee, Sungwon Cho, Woohyun Hwang et al.  
  Experimental TCAD calibration is essential for predictive technology modeling of emerging oxide semiconductor transistors. However, it remains time-consuming and expert dependent because of model ambiguity.
- <a id="20260915-2609.12202"></a>**QuPAINT: Physics-Aware Multimodal Reasoning for Quantum Material Characterization** — [2609.12202](https://arxiv.org/abs/2609.12202) | cross: cs.AI, cs.LG  
  Sankalp Pandey, Xuan-Bac Nguyen, Hoang-Quan Nguyen, Tim Faltermeier et al.  
  Characterizing two-dimensional (2D) quantum materials by optical microscopy requires localizing exfoliated flakes and determining their layer thickness from subtle optical contrast and interference color to select suitable flakes for device fabrication. However, models face synthetic-to-real domain shifts and variation across materials, substrates, laboratories, and imaging conditions.
- <a id="20260915-2609.12230"></a>**Repair Before Reinforce: Context-Augmented Knowledge Graph Reasoning for Multi-Hop Question Answering** — [2609.12230](https://arxiv.org/abs/2609.12230) | cross: cs.AI  
  Tharaka D. Fonseka, Niraj K. Jha  
  Question-answering often requires reasoning across multiple connected facts rather than retrieving a single isolated relation. Knowledge graphs (KGs) provide a structured way to represent such facts, but training large language models (LLMs) only on isolated KG head-relation-tail triples may limit their ability to learn the surrounding context needed for multi-hop reasoning.
- <a id="20260915-2609.12252"></a>**DriftSE: Speech Enhancement with Generative Drifting** — [2609.12252](https://arxiv.org/abs/2609.12252) | cross: cs.AI, eess.AS  
  Liang Xu, Diego Caviedes-Nozal, W. Bastiaan Kleijn, Longfei Felix Yan et al.  
  We propose DriftSE, a novel one-step generative framework for speech enhancement formulated as a latent distribution equilibrium problem. During training, the drifting field aligns the generator's pushforward distribution with the clean speech manifold through drifting in a latent domain.
- <a id="20260915-2609.12254"></a>**Automated Detection and Structuring of Social Tipping Point Evidence in Climate related Documents: A Modular AI Framework** — [2609.12254](https://arxiv.org/abs/2609.12254) | cross: cs.AI  
  Kavindu Perera, Mohammad Abaeiani, Ekaterina Gilman, Lauri Loven et al.  
  The climate literature has grown faster than review teams can read it. That gap matters most for a concept like the environmental social tipping point, the threshold at which a small change triggers rapid, self-reinforcing change in a social system.
- <a id="20260915-2609.12260"></a>**HypoKG: Evidence-Disciplined Biomedical Hypothesis Generation Beyond Endpoint Knowledge** — [2609.12260](https://arxiv.org/abs/2609.12260) | cross: cs.AI, q-bio.QM  
  Dominic Okonkwo, Adetayo Okunoye, Ismailcem Budak Arpinar  
  Large language models (LLMs) can generate biomedical hypotheses, but it remains unclear whether they truly reason from scientific evidence or simply produce convincing-sounding ideas. To study this, we combine three major biological databases: the Kyoto Encyclopedia of Genes and Genomes (KEGG), Rhea, and UniProt, into a unified biochemical knowledge graph and construct a benchmark of 550 paths …
- <a id="20260915-2609.12270"></a>**Recommendation Retrievers Need Verifiers: Universal Generative Reranking for Sequential Recommendations** — [2609.12270](https://arxiv.org/abs/2609.12270) | cross: cs.AI  
  Benyu Zhang, Qiang Zhang, Rui Li, Qunshu Zhang et al.  
  First-stage recommenders in multi-stage systems produce a ranked candidate list from which a limited prefix is forwarded to downstream rankers. Because each forwarded item must be processed by more expensive ranking stages, this shortlist cannot be arbitrarily large.
- <a id="20260915-2609.12303"></a>**Breaking the Token Ceiling: Distilling Smaller, Stronger Byte Models** — [2609.12303](https://arxiv.org/abs/2609.12303) | cross: cs.AI, cs.LG  
  Kalyani Marathe, Artidoro Pagnoni, Tomasz Limisiewicz, Margaret Li et al.  
  Small models are made more capable through distillation from a larger one that shares their tokenization scheme. However, do distilled byte and token models behave similarly in terms of scaling trends as compute and data increases?
- <a id="20260915-2609.12305"></a>**Self-Verifying Anomaly Detection using Explainable AI for Cybersecurity of DER Networks** — [2609.12305](https://arxiv.org/abs/2609.12305) | cross: cs.AI, cs.LG  
  Damilola Popoola, Souradeep Bhattacharya, Manimaran Govindarasu  
  The rapid growth of Distributed Energy Resources (DERs) has significantly expanded the cyber attack surface of modern power grids. Furthermore, increasing sophistication in attack techniques demands anomaly detection systems (ADS) that are accurate, interpretable, and reliable to support DER cybersecurity.
- <a id="20260915-2609.12310"></a>**ESTS at WMT26: Routing-Informed Expert Pruning for Model Compression** — [2609.12310](https://arxiv.org/abs/2609.12310) | cross: cs.AI, cs.LG  
  Liu O. Martin, Lucas Bandarkar, Nanyun Peng  
  We describe six submissions under the team name ESTS to the unconstrained WMT26 Model Compression Shared Task for English--Simplified Chinese and English--Egyptian Arabic. We submit three compression operating points per translation direction, all derived from GPT-OSS-20B.
- <a id="20260915-2609.12366"></a>**ORQA: An Occupation-Realistic Question and Answer Framework for LLM Professional Knowledge** — [2609.12366](https://arxiv.org/abs/2609.12366) | cross: cs.AI  
  Shreyas Krishnan, Serina Chang, Abhishek Nagaraj  
  We present ORQA, a method for testing occupation-level knowledge in large language models. Prior methods either map abstract LLM skills to occupations via task definitions or utilize expert knowledge which is difficult to obtain at scale and expensive.
- <a id="20260915-2609.12388"></a>**RF-VoID: Towards Bandwidth-Efficient Exterior Tile Void Detection via Narrowband Radio-Frequency Representation Learning** — [2609.12388](https://arxiv.org/abs/2609.12388) | cross: cs.AI  
  Xinyan Chen, Ruiqin Ma, Shunsuke Shoda, Changyu Zhou et al.  
  Hidden debonding behind exterior ceramic tiles is a falling-tile hazard, and millimeter-wave radar offers a non-contact way to find it. Conventional interpretation first reconstructs a range profile, so its reliability is bounded by the available bandwidth, yet bandwidth is what sets the cost, the acquisition time, and the regulatory footprint of a deployed system.
- <a id="20260915-2609.12397"></a>**UFO: Chain-of-Evaluation for Omni-Condition Alignment in Multi-Modal Image Generation** — [2609.12397](https://arxiv.org/abs/2609.12397) | cross: cs.AI  
  Danning Zhang, Yijing Lin, Shuhan Zhuang, Mengqi Huang et al.  
  Multi-modal image generation, particularly subject-driven customization, has garnered growing attention in recent years. Despite the rapid advancement of generative models, their evaluation remains largely lagging.
- <a id="20260915-2609.12439"></a>**Debiasing as a Measurement Intervention: Calibrated Ties and Resolution Loss in LLM-as-a-Judge Evaluation** — [2609.12439](https://arxiv.org/abs/2609.12439) | cross: cs.AI  
  Liang Zhao, Yong Wang, Jiangzhe Chen  
  LLM-as-a-judge protocols are commonly debiased by instructing judges to ignore presentation cues such as citation formatting, source labels, and evidence-display style. We show that this intervention can suppress bias while damaging the resolution of the measurement instrument.
- <a id="20260915-2609.12441"></a>**IMPLY: Physically Anchored Consistency for World-Model Rollouts** — [2609.12441](https://arxiv.org/abs/2609.12441) | cross: cs.AI, cs.CV, cs.LG  
  Aman Mehta, Riya Baviskar  
  A world model asked what happens if an object is pushed at several speeds produces several futures. If the model has the object in mind, those futures agree about it: each implies the same mass and friction.
- <a id="20260915-2609.12454"></a>**Bridging Vision Foundation Model Priors with CLIP for Spatial-aware Few-shot Anomaly Detection in Medical Images** — [2609.12454](https://arxiv.org/abs/2609.12454) | cross: cs.AI, cs.LG  
  Juzheng Miao, Yuchen Yuan, Cheng Chen, Pheng-Ann Heng  
  Vision-Language Models such as CLIP enable effective few-shot medical anomaly detection (AD) via strong image-text semantic alignment. However, their globally contrastive pretraining lacks explicit spatial supervision, limiting precise lesion localization.
- _…另有 32 篇, 见 `data/20260915.json`_

#### cs.LG (132)

- <a id="20260915-2609.12896"></a>**Behavior Quotient Learning for Low-Rank Adaptation of LLM Agents** — [2609.12896](https://arxiv.org/abs/2609.12896) | cross: cs.AI | 🎯🧐 LLM-based agent  
  Pengyang Zhou, Xiaobin Tu, Zhengxi Liu, Rongkun Xue et al.  
  LLM-based agents rely on heterogeneous interaction capabilities to accomplish complex tasks. Existing approaches often distribute these capabilities across multiple LoRA adapters, which increases adapter storage requirements and introduces routing overhead during inference.
- <a id="20260915-2609.12331"></a>**Simulating Disengaged Students to Evaluate LLM-based Tutors** — [2609.12331](https://arxiv.org/abs/2609.12331) | 🎯★ consensus  
  Xianghui Meng, Jionghao Lin  
  Simulated students generated by computational models provide a practical way to evaluate tutoring strategies and pedagogical approaches used by human and AI tutors. However, such simulations should account for disengaged behaviors, including gaming the system, wheel-spinning, and off-task behavior, because tutors may need different responses for different learner states.
- <a id="20260915-2609.12002"></a>**Can We Trust LLM Judges: A Study of Capability-Dependent Biases and Multi-Judge Ensemble for Bias Calibration** — [2609.12002](https://arxiv.org/abs/2609.12002) | cross: cs.AI  
  Gemma Zhang, Prachi Badarayani, Asmi Kumar, Sadid Hasan et al.  
  LLMs are increasingly used as automated judges for model training and evaluation, yet individual judges exhibit systematic biases that undermine reliability. Much of prior work has studied biases in pairwise LLM-as-a-judge settings; in this paper, we focus on absolute scoring tasks, which mirror more realistic use cases.
- <a id="20260915-2609.12179"></a>**Explanations-Driven Active Feature Acquisition for Algorithmic Recourse** — [2609.12179](https://arxiv.org/abs/2609.12179) | cross: cs.AI  
  Vinura Galwaduge, Jagath Samarabandu  
  Algorithmic recourse methods typically assume that a predictive model has access to all features of an individual. In practice, decisions are often made with partial information, because features are costly to acquire.
- <a id="20260915-2609.12223"></a>**Predicting Collision Cross Sections with GRACE: Geometric Residual Adduct Conditioning via Early-fusion** — [2609.12223](https://arxiv.org/abs/2609.12223) | cross: cs.AI, q-bio.BM  
  Parthasarathy Suryanarayanan, Susanta Das, Shreyans Sethi, Kenneth M. Merz et al.  
  Collision cross section (CCS), derived from ion mobility mass spectrometry, is a common descriptor for molecular annotation. Prediction is challenging for machine learning models because it reflects the size, shape, and ionization state of a gas-phase molecular ion.
- <a id="20260915-2609.12277"></a>**Reinforcement Learning over Patient Trajectories for Clinical Reasoning in EHR Foundation Models** — [2609.12277](https://arxiv.org/abs/2609.12277) | cross: cs.AI, cs.CY  
  Yuxin Xiao, Sheng Zhang, Chandan Singh, Tristan Naumann et al.  
  Electronic health record (EHR) foundation models trained on longitudinal patient trajectories have demonstrated strong performance across diverse clinical prediction tasks. However, their clinical reasoning capabilities remain constrained by next-token prediction on limited and incomplete EHR data.
- <a id="20260915-2609.12278"></a>**Amortized Low-Rank Adaptation for Model-Based Reinforcement Learning** — [2609.12278](https://arxiv.org/abs/2609.12278) | cross: cs.AI, cs.RO  
  Fernando Palafox, David Fridovich-Keil  
  World models let agents plan by predicting the consequences of their actions, but changes in the environment can make them inaccurate. We study the problem of adapting a world model to an unknown test-time environment, drawn from a known environment family, using only a few episodes of interaction.
- <a id="20260915-2609.12419"></a>**MInTRL: Off-policy Intervention can boost On-policy RL** — [2609.12419](https://arxiv.org/abs/2609.12419) | cross: cs.AI  
  Mingyu Chen, Yefan Tao, Gerald Friedland, Xuezhou Zhang et al.  
  Reinforcement learning with verifiable rewards is typically performed on-policy, keeping training data close to the current policy but limiting learning to trajectories that the policy can discover itself. Off-policy methods such as supervised fine-tuning, on the other hand, can leverage external knowledge beyond the base model's capabilities, but may suffer from large distribution shift.
- <a id="20260915-2609.12435"></a>**Observation-Anchored Selective Assimilation for Longitudinal Tumor-State Proxy Forecasting in Post-Treatment Glioma** — [2609.12435](https://arxiv.org/abs/2609.12435) | cross: cs.AI  
  Yeonjae Jung, Minwoo Shin  
  Post-treatment MRI in patients with glioma provides serial observations for updating patient-specific tumor-state proxy estimates, but variable appearances and trajectories complicate forecasting. We formulate forecasting as an observation-aware digital-twin update in which an intermediate observation anchors the patient-specific state.
- <a id="20260915-2609.12437"></a>**Beyond the Query: Do Retrieval Signals Improve Adaptive Multimodal RAG Routing?** — [2609.12437](https://arxiv.org/abs/2609.12437) | cross: cs.AI  
  Qiaomu Li, Qiuyuan Zhang, Nong Ming  
  Adaptive RAG often uses retrieval-time signals to decide whether another retrieval, reranking, or multimodal step should run. We ask whether these signals add routing value once the query itself is already known.
- <a id="20260915-2609.12442"></a>**3D Digital Twin Visualization of Multiclass GRF-Based Gait Disorder Classification** — [2609.12442](https://arxiv.org/abs/2609.12442) | cross: cs.AI  
  Nayoung Son, Minwoo Shin  
  Automated gait analysis requires accurate classification and interpretable outputs. We propose an integrated framework for classifying healthy gait and multiple musculoskeletal impairment groups using bilateral ground reaction force (GRF) and center-of-pressure (COP) signals.
- <a id="20260915-2609.12563"></a>**TokenMapper: A Step Toward Interoperable Speech Token Translation** — [2609.12563](https://arxiv.org/abs/2609.12563) | cross: cs.AI, cs.SD, eess.AS  
  Tal Kozakov, Tal Rosenwein, Eliya Nachmani  
  Neural audio codecs discretize speech into token sequences, but the resulting token spaces differ in vocabulary and codebook structure, preventing direct communication across models. This limitation affects applications such as conversational voice agents and speech to speech translation systems where multiple speech models must interact.
- <a id="20260915-2609.12579"></a>**SCOPE-OPSD: Fisher-Conditioned Privileged Subspaces for On-Policy Self-Distillation** — [2609.12579](https://arxiv.org/abs/2609.12579) | cross: cs.AI  
  Yunmeng Chen (Chongqing Ant Consumer Finance Co., Ltd), Kunyu Wang (Alibaba Cloud Computing Co., Ltd) et al.  
  On-policy self-distillation (OPSD) scores student-generated prefixes with a solution-conditioned self-teacher, yet transfers supervision only through next-token probabilities. We ask whether the aligned final-layer discrepancy offers a useful second channel, and how to test that channel without confusing its geometry with auxiliary strength.
- <a id="20260915-2609.12584"></a>**Clustering-Based Balanced Sampling and Allocation with Data Parallelism for High-Performance Fine-Tuning** — [2609.12584](https://arxiv.org/abs/2609.12584) | cross: cs.AI  
  Hyunjin Kim, Youngeun Nam, Jaemin Han, Wonhyeok Choi et al.  
  Instruction-tuning datasets for large language models (LLMs) are often large, redundant, and imbalanced, limiting efficient adaptation. Naive large-batch fine-tuning repeatedly includes overrepresented sample groups while weakly covering underrepresented but informative ones, especially under data parallelism (DP) across multiple GPUs.
- <a id="20260915-2609.12599"></a>**SIMS: Scale-Invariant Merit-Function-Based Scalarization for Multi-Task Learning** — [2609.12599](https://arxiv.org/abs/2609.12599) | cross: cs.AI, math.OC  
  Zebin Chen, Fei Xing, Yang Chen, Hua Liu et al.  
  Multi-task learning (MTL) requires navigating unavoidable trade-offs among competing objectives. This paradigm is frequently formulated as multi-objective optimization (MOO), where the scalarization is favored to reduce an MOO problem to a single objective.
- <a id="20260915-2609.12620"></a>**Correlation-Guided Fast Machine Unlearning via Hessian Analysis** — [2609.12620](https://arxiv.org/abs/2609.12620) | cross: cs.AI  
  Ayushi Thakur, Ruchir Gupta, Amit Kumar Jaiswal, Prayag Tiwari  
  The increasing adoption of machine learning in network and distributed security systems has created an urgent need for mechanisms that can selectively and efficiently remove the influence of specific training data to eliminate compromised or adversarial data points from production models. Privacy regulations such as GDPR's \emph{right to be forgotten} also pose similar requirements.
- <a id="20260915-2609.12639"></a>**Explaining Time Series Forecasting with Horizon-Resolved Attribution** — [2609.12639](https://arxiv.org/abs/2609.12639) | cross: cs.AI  
  Seunghan Lee, Jun Seo, Jaehoon Lee, Junhyeok Kang et al.  
  Recent advances in explaining time series (TS) models have produced methods that identify which past values a prediction depends on. However, most existing methods return a single importance vector, assuming that every predicted step depends on the same past values.
- <a id="20260915-2609.12712"></a>**InRTL: Effective Intra-Inter Interaction Learning for Relational Tables** — [2609.12712](https://arxiv.org/abs/2609.12712) | cross: cs.AI  
  Weichen Li, Ken Zhong, Zheng Wang, Li Pan et al.  
  Relational table learning has recently emerged as an important research direction for modeling multiple tables connected through primary key-foreign key (PK-FK) relationships. Despite recent advances, a principled modeling framework tailored to this task remains underexplored.
- <a id="20260915-2609.12814"></a>**RunningTensor: Generalizing Linear Attention to Higher-Order Recurrent States** — [2609.12814](https://arxiv.org/abs/2609.12814) | cross: cs.AI  
  Luca Herranz-Celotti, Vincent Guigue  
  Linear attention and state-space models provide linear-time sequence modeling, but their recurrent memory remains a second-order tensor (a matrix), limiting the order of interactions that can be represented in the state. We introduce the RunningTensor, which generalizes this memory to an order-$o$ tensor, updated by a rank-1 outer product and read by contracting against $o-1$ vector queries.
- <a id="20260915-2609.12890"></a>**Large Distant Gradients Need Not Be Reliable: reliability-weighted credit assignment for long-horizon autoregressive forecasting** — [2609.12890](https://arxiv.org/abs/2609.12890) | cross: cs.AI  
  Junhao Zhao, David Michael Simberg, Jacob Kang, Colin Connor Kurniawan et al.  
  In autoregressive forecasting, long prediction rollouts provide distant supervision, but backpropagation through time (BPTT) carries gradients from those losses through many autoregressive steps. Repeated Jacobian products can make distant gradients dominate the update while amplifying predictable signal and unpredictable noise together; a large distant gradient therefore need not carry reliable …
- <a id="20260915-2609.13031"></a>**Attention Quantization for Tabular Foundation Models** — [2609.13031](https://arxiv.org/abs/2609.13031) | cross: cs.AI  
  Jonas M. K\"ubler, Benjamin J\"ager, Klemens Fl\"oge, Noah Hollmann et al.  
  With the recent rise and adoption of tabular foundation models, optimizing their inference performance becomes an emerging field for efficiency research. While the models are architecturally similar to transformer-based large language models (LLMs), the size and serving patterns differ significantly.
- <a id="20260915-2609.13035"></a>**Groupoid-Based Internal State Representations for Reinforcement Learning with Local Symmetries** — [2609.13035](https://arxiv.org/abs/2609.13035) | cross: cs.AI  
  Ben Opperman, Eduardo Alonso, Esther Mondrag\'on  
  Symmetries play a central role in reducing the complexity of reinforcement learning problems, yet most existing approaches rely on fixed group actions or predefined state abstractions. Classical reinforcement learning algorithms typically assume a globally structured Markov decision process with uniformly applicable actions and transitions, an assumption that limits their ability to exploit …
- <a id="20260915-2609.13042"></a>**DynSHAP: Towards Explainable Dynamic Survival Analysis** — [2609.13042](https://arxiv.org/abs/2609.13042) | cross: cs.AI  
  Nastasya Anokhina, Jonas J\"ur{\ss}, Pietro Li\`o  
  Deep learning models for dynamic survival analysis (DSA) achieve strong predictive performance by incorporating longitudinal patient data, but their black box nature limits clinical trust and adoption. Existing explainability methods cannot handle longitudinal, irregular inputs and functional survival outputs simultaneously, which limits their usability in DSA.
- <a id="20260915-2609.13072"></a>**MAxBench: A Multinomial Concept Recovery Benchmark** — [2609.13072](https://arxiv.org/abs/2609.13072) | cross: cs.AI, cs.CL  
  Divya Appapogu, Freya Behrens, Yonatan Belinkov, Aaron Mueller  
  Fine-grained control of language model behaviors (e.g., steering) is among the more actionable outcomes of interpretability research. For binary concepts such as refusal, a single direction in activation space often suffices for steering.
- <a id="20260915-2609.11934"></a>**Fundamental Dynamical Units for Physics-Informed Structural Inference from Perturbation Time-Series in Networked Systems** — [2609.11934](https://arxiv.org/abs/2609.11934) | cross: physics.comp-ph  
  Nima Nouri  
  In networked dynamical systems, the parameter of primary mechanistic interest is signed interaction structure. Recovering this structure from perturbation time-series data is a fundamental identification problem, compounded by three coupled obstacles: the combinatorial complexity of interaction architectures, ambiguity of causal attribution under limited interventions, and state-dependent …
- <a id="20260915-2609.11935"></a>**Physics-Informed Conformal Prediction: Embedding PDE Consistency into Distribution-Free Uncertainty Quantification for Neural Operators** — [2609.11935](https://arxiv.org/abs/2609.11935)  
  Michael Chin  
  Neural operators such as the Fourier Neural Operator (FNO) achieve remarkable accuracy in approximating solutions to partial differential equations (PDEs). However, providing rigorous uncertainty estimates remains an open challenge.
- <a id="20260915-2609.11937"></a>**Fed-Equilibrium Framework for Topological Pareto Control in Robust and Fair Clinical Federated Learning** — [2609.11937](https://arxiv.org/abs/2609.11937) | cross: cs.DC  
  Ting Xu, Henry Leung  
  The deployment of Federated Learning (FL) in multi-center clinical networks faces the challenge of "knowledge dominance," where high-volume hubs naturally overwhelm minority community nodes, implicitly treating the distinct clinical patterns of smaller cohorts as outliers. Existing geometric defenses provide a security baseline but leave this efficiency-fairness dilemma unresolved.
- <a id="20260915-2609.11954"></a>**Efficient AI Model Deployment Using Quantization Analysis Tool** — [2609.11954](https://arxiv.org/abs/2609.11954)  
  Dwith Chenna, Kanishka Macherla  
  As deep learning models are increasingly deployed on resource constrained devices, the demand for efficient model optimization techniques continues to grow. Effective deployment of AI models on edge and low power platforms requires optimization methods that reduce model size and computational cost while maintaining high accuracy.
- <a id="20260915-2609.11956"></a>**Performance, Efficiency and Collapse -- Advantages and Challenges in Offline Post-training of Code LLMs** — [2609.11956](https://arxiv.org/abs/2609.11956)  
  Abhinav Anand, Sanjana Reddy Pachika, Shweta Verma, Mira Mezini  
  Post-training with reinforcement learning (RL) is a critical phase in the development of code-generating large language models (LLMs), as it ensures adherence to instructions and the production of functionally correct code. This process typically requires computationally intensive code sample generation from Transformer-based LLMs and substantial GPU-CPU communication for sequence verification.
- <a id="20260915-2609.11957"></a>**Look Before You Leap: Pre-Action Verification for LLM Agents** — [2609.11957](https://arxiv.org/abs/2609.11957) | cross: cs.MA  
  Asaad Althoubi  
  An LLM agent acts on the world by emitting actions: shell commands to run, edits to apply. A wrong action does not always fail loudly; it can fail silently, producing a plausible but incorrect effect that raises no error.
- <a id="20260915-2609.11958"></a>**Decoding Mixture Perception through Computational Modeling of Component Interactions** — [2609.11958](https://arxiv.org/abs/2609.11958)  
  Fei Wang, Xiaoya Xie, Junfei Liu, Huihao Wang et al.  
  Olfaction played an indispensable role throughout human evolution and civilization. Even in the contemporary era of advanced technology, olfaction remains a critical channel for person to conduct danger discrimination, emotional experience, and memory formation.
- <a id="20260915-2609.11959"></a>**Space as an Interventional Invariant: Cross-Modal Predictive Geometry for Stratified Cities and Em-Spaced Intelligence** — [2609.11959](https://arxiv.org/abs/2609.11959) | cross: cs.CL  
  Tao Yang, Xuhui Lin, Kunyao Li, Haijiang Li  
  Space is a foundational concept across mathematics, physics, spatial cognition, urban science, and embodied intelligence, yet these fields often treat spatial structure either as a shared geometric container or as a collection of disconnected representations. Such approaches struggle to explain how heterogeneous sensory and urban processes can jointly reveal a common spatial structure, …
- <a id="20260915-2609.11961"></a>**On-Device Language Models for Privacy-Preserving Stress Prediction: A Multimodal Evaluation on Mobile Health** — [2609.11961](https://arxiv.org/abs/2609.11961) | cross: cs.HC  
  Ibukunoluwa Soyebo, Alyssa Donawa, Rodrigo Aguilar Barrios, Brice Patchou et al.  
  Stress is a pervasive determinant of mental health and a key target for mobile health interventions. On-device language models (ODLMs) offer privacy-preserving inference without cloud dependency, yet their feasibility for health prediction under mobile resource constraints remains underexplored.
- <a id="20260915-2609.11993"></a>**FINESSE: An Agent-Based Simulator and Benchmark Dataset for Multimodal Financial Event Sequences** — [2609.11993](https://arxiv.org/abs/2609.11993)  
  Tyler Farnan, Benjamin Eng, Adam Abate, Xirui Hou et al.  
  Machine learning research in financial services is limited by the scarcity of representative open-source datasets. Existing resources are often narrowly focused on a single modality or task and fail to reflect the structured, multimodal, and dynamic nature inherent to many problems in financial services.
- <a id="20260915-2609.11995"></a>**Explainable Prediction from Mobile Sensing Data through LLM-guided Concept Integration** — [2609.11995](https://arxiv.org/abs/2609.11995)  
  Yuning Wang, Iman Azimi, Amir M. Rahmani, Pasi Liljeberg  
  Mobile sensing enables longitudinal monitoring of behavioral and physiological patterns in everyday settings. However, accurate prediction remains challenging in small-cohort health-sensing studies, where task-specific outcome supervision is limited relative to heterogeneous sensing data.
- <a id="20260915-2609.11997"></a>**DCRA: Diffusion-Conditioned Representation Alignment for Robust Time-Series Learning** — [2609.11997](https://arxiv.org/abs/2609.11997) | cross: stat.ML  
  Wenrui Xu, Anas Enanaa, Keshab K. Parhi  
  Learning robust representations for time-series signals under noise and distribution shifts remains challenging, especially in clinical applications such as electroencephalogram (EEG) and electrocardiogram (ECG) analysis. We propose Diffusion-Conditioned Representation Alignment (DCRA), a training framework that repurposes the forward diffusion process as a structured corruption scheduler for …
- <a id="20260915-2609.11998"></a>**Fixed State, Long Reach: What a Constant-Size Cache Buys Block Diffusion at Scale** — [2609.11998](https://arxiv.org/abs/2609.11998)  
  Vaibhav Singh, Pierre-Andr\'e No\"el, Torsten Scholak, Eugene Belilovsky et al.  
  Diffusion language models decode tokens in parallel, but their bidirectional denoiser rules out the naive key--value (KV) cache behind fast autoregressive inference. Block diffusion restores caching by decoding block-by-block, and the block caches deployed on it so far are tied to attention: O(L)in memory and, if used as training-free retrofits, only an approximation of the model's computation.
- <a id="20260915-2609.12011"></a>**QTrans: A Quantum Transformer for Sentiment Classification** — [2609.12011](https://arxiv.org/abs/2609.12011)  
  Ren-Xin Zhao, Xinjie Huang, Yahong Liu, Maoyu Ye et al.  
  In small-scale binary sentiment classification scenarios, factors such as negation, contrastive shifts, and cross-word dependencies lead to the non-linear coupling of sentiment cues, making it difficult for conventional lightweight models to fully capture the contextual relationships between tokens. To address this issue, we propose a model named QTrans, which uses parameterized quantum circuits …
- <a id="20260915-2609.12014"></a>**Certified Safety Curation: Distribution-Free Guarantees for Safe Offline Reinforcement Learning** — [2609.12014](https://arxiv.org/abs/2609.12014)  
  Adam Haroon, Cody Fleming  
  Safe offline reinforcement learning assumes a cost function on every transition. We ask what remains possible when safety can be judged only by comparing short clips and occasionally asking whether an episode exceeded its budget.
- <a id="20260915-2609.12016"></a>**Inverting Self-Triggered Control: Adversarial Reinforcement Learning for Sparse Denial-of-Service Attacks** — [2609.12016](https://arxiv.org/abs/2609.12016) | cross: cs.SY, eess.SY  
  Adam Haroon, Erick J. Rodr\'iguez-Seda, Tristan Schuler, Cody Fleming  
  Self-triggered reinforcement learning control (RL-STC) learns the sparsest control schedule that preserves Lyapunov-decreasing stability under a Run-Time Assurance (RTA) override. We invert this: an adversarial RL agent learns the sparsest jamming or Denial-of-Service (DoS) schedule that destabilizes the closed loop, with a Lyapunov-increase admissibility predicate mirroring the defender's safety …
- <a id="20260915-2609.12018"></a>**Toward Reliable Railway-Bogie Response Prediction Using Multifidelity TDNN and Physics-Informed Residual Learning** — [2609.12018](https://arxiv.org/abs/2609.12018) | cross: physics.app-ph  
  Gyeolhee Lee, Moosun Kim, Taewook Kwon, Jaehun Kim et al.  
  Railway engineers need simulation models that predict vehicle responses across operating scenarios that cannot be tested exhaustively. Agreement with representative measurements provides essential evidence, but calibration at a limited set of conditions does not guarantee accuracy elsewhere.
- <a id="20260915-2609.12020"></a>**Reinforcement Learning for Syndrome Extraction** — [2609.12020](https://arxiv.org/abs/2609.12020) | cross: quant-ph  
  John Zhuoyang Ye, Aarav Pabla, Jens Palsberg  
  A key subtask of quantum error correction is to extract a syndrome that, if nontrivial, signals an error. The number of possible ways to extract a syndrome grows exponentially with the syndrome size, and these implementations vary greatly in fault tolerance, as measured by their logical error rates.
- <a id="20260915-2609.12067"></a>**Scalable Discrete-to-Continuous Channel Simulation for Compression and Privacy** — [2609.12067](https://arxiv.org/abs/2609.12067) | cross: cs.IT, math.IT  
  Joseph Rowan, Buu Phan, Ashish J. Khisti  
  Channel simulation has recently emerged as a useful component in machine learning systems where samples from a prescribed probability distribution are to be compressed. Yet, general channel simulation algorithms often suffer from high computational costs, random stopping times or, in the worst case, can require generating an infinite number of shared random samples.
- <a id="20260915-2609.12113"></a>**Score-based Outlier Generation via Controlling the Radon-Nikodym Derivative** — [2609.12113](https://arxiv.org/abs/2609.12113) | cross: math.AP, math.OC, math.PR, stat.ML  
  Amartya Mukherjee, Tristan Milne, Kry Yik-Chau Lui, Stephanie Hazlewood et al.  
  Outliers are important for stress-testing algorithms and understanding system behaviour under rare conditions. Despite being commonly described as low-likelihood events, existing generative approaches rarely control likelihood explicitly.
- <a id="20260915-2609.12119"></a>**Almost Sure Convergence Analysis of Stochastic Gradient Methods with Clipping and Additive Noise** — [2609.12119](https://arxiv.org/abs/2609.12119) | cross: math.OC, math.PR  
  Amartya Mukherjee, Jun Liu  
  Stochastic gradient descent (SGD) with gradient clipping and additive noise has become a standard technique for training machine learning models, particularly in applications requiring robustness or privacy guarantees. However, clipping introduces a bias in stochastic gradients, while additive noise introduces additional variance, making the long-run behaviour of individual optimization …
- <a id="20260915-2609.12123"></a>**Rank-Efficient LoRA via Joint Tangent-Space Optimization under Isotropic Curvature** — [2609.12123](https://arxiv.org/abs/2609.12123) | cross: math.OC, stat.ML  
  Zihan Zhu, Zhehang Du, Xuyang Chen, Tim Tsz-Kit Lau et al.  
  Low-Rank Adaptation (LoRA) is an effective approach for adapting large pretrained models by learning low-rank weight updates. In practice, the LoRA rank is used to control an adapter's parameter budget and representational capacity.
- <a id="20260915-2609.12137"></a>**GUIDE: Generative Utility Inference and Decision Engine** — [2609.12137](https://arxiv.org/abs/2609.12137)  
  Anagha Tiwari, Alexander G. Gray, Nick Feamster, Brian Jabarian et al.  
  Measuring the preferences of human users remains a fundamental challenge of AI alignment. Existing elicitation approaches struggle to efficiently discover multidimensional preferences or accurately ground these inferences in domain knowledge.
- <a id="20260915-2609.12163"></a>**Certifying Concept Unlearning in Text-to-Image Diffusion Models** — [2609.12163](https://arxiv.org/abs/2609.12163)  
  Mansi, Luca Marzari, Francesco Leofante  
  Existing evaluations of concept unlearning in text-to-image (T2I) diffusion models primarily rely on attack success rates obtained through automated adversarial prompt search. However, these metrics provide only empirical evidence over a finite set of queries and leave residual leakage over the broader prompt space largely unquantified.
- <a id="20260915-2609.12173"></a>**Estimating Pedestrian Volumes from GIS-Derived Built-Environment Features: A Machine Learning Framework** — [2609.12173](https://arxiv.org/abs/2609.12173)  
  Bahareh Golchin, Banafsheh Rekabdar, Sirisha Kothuri, Joseph Broach  
  Transportation agencies need pedestrian volume estimates across entire road networks to prioritize safety investments, yet manual counts are expensive and cover only a small share of intersections. We present a machine learning pipeline that predicts 2-hour PM peak pedestrian volume at 101 urban intersections in Portland, Oregon, from built-environment, land-use, and street-network features drawn …
- <a id="20260915-2609.12224"></a>**Patient-Reported Survey Data Improve Prediction of Opioid Use Disorder** — [2609.12224](https://arxiv.org/abs/2609.12224)  
  Xiyue Jiang, Zihan Ding, Grace Han, Yinan Liu et al.  
  Electronic health records (EHRs) may incompletely capture patient-reported factors associated with opioid use disorder (OUD). We evaluated whether survey data improve prediction of a first recorded OUD diagnosis among 267,747 All of Us participants with documented opioid exposure, including 15,287 OUD cases.
- <a id="20260915-2609.12225"></a>**PLSP (Pre-hoc Liminal Space Profiling): OOD Prediction over Detection -- An Anticipatory Approach for Machine Learning Model Reliability** — [2609.12225](https://arxiv.org/abs/2609.12225) | cross: cs.CV  
  Vipul Bansal, Himanshu Buckchash, Balasubramanian Raman, Deepak Dhungana  
  Out-of-Distribution (OOD) data poses a significant threat to machine learning models, often leading to model failure during deployment. All existing OOD detection methods are post-hoc, relying on evaluation metrics such as accuracy and AUC-ROC during inference to indirectly assess the model's response to OOD data by measuring deviations.
- <a id="20260915-2609.12244"></a>**CRFCAN: A Complex-Valued Cross-Domain Residual Network for Joint Channel and Phase Noise Estimation in Sub-THz OFDM Systems** — [2609.12244](https://arxiv.org/abs/2609.12244) | cross: eess.SP  
  Ruilin Wang, Xiaodai Dong  
  In sub-terahertz (sub-THz) communications, the coupling of ultra-wide bandwidth and severe phase noise (PN) impairments renders conventional joint channel and PN estimation highly complex and computationally prohibitive. To address this, we propose CRFCAN, a complex-valued residual FFT convolutional attention network designed for joint channel and PN estimation.
- <a id="20260915-2609.12259"></a>**The Rank the Task Demands: A Causal Rank Law for Matrix Memories Trained on Group Composition** — [2609.12259](https://arxiv.org/abs/2609.12259)  
  Samuel Larson  
  Matrix-valued memories make rank the natural budget of a learned representation: the number of independent directions a state spans bounds what it can bind, compose, and track. We report causal evidence, on a group-composition testbed trained under a hard single-state bottleneck with a fixed decoder that cannot launder rank, that gradient descent recruits precisely the rank the task's algebra …
- <a id="20260915-2609.12264"></a>**Adaptive Chemotherapy Control under Tumor Heterogeneity via Reinforcement Learning** — [2609.12264](https://arxiv.org/abs/2609.12264) | cross: cs.SY, eess.SY  
  Bereket Sitotaw Kidane, Md Samiul Haque Motayed, Shuo Wang  
  Designing effective chemotherapy regimens is hindered by tumor heterogeneity and drug resistance, which complicate the deployment of patient-specific model-based optimal control across diverse populations. We develop and compare closed-loop deep reinforcement learning (DRL) dosing policies with continuous (TD3) and discrete (DQN) action spaces trained on a high-dimensional heterogeneous tumor …
- <a id="20260915-2609.12298"></a>**FRIST: FMRI Representation Informed Shared-space Training Improves EEG-only Individual-Finger BCI Decoding** — [2609.12298](https://arxiv.org/abs/2609.12298) | cross: eess.SP  
  Jintao Zhang, Yidan Ding, Joshua Kosnoff, Maxim Karrenbach et al.  
  Finger-level motor decoding is important for naturalistic brain-computer interface (BCI) control, yet individual-finger decoding from scalp electroencephalography (EEG) remains challenging because finger representations are spatially close in the sensorimotor cortex and blurred by volume conduction. Leveraging the high spatial resolution of functional MRI (fMRI), we introduce fMRI …
- <a id="20260915-2609.12317"></a>**Sampling via Decision-Flow: Training-Free Extraction of Improved Latent Reasoning Paths in Large Language Models** — [2609.12317](https://arxiv.org/abs/2609.12317)  
  Zhendong Mi, Shaoyi Huang  
  A central question in LLM reasoning is whether reinforcement learning (RL) instills genuinely new capabilities or merely reshapes how existing knowledge is expressed during inference. Building on the distribution-sharpening hypothesis, which holds that RL reallocates probability mass toward high-reward trajectories already latent in base models, we ask: can we unlock those latent paths without …
- <a id="20260915-2609.12337"></a>**Theoretical Guarantees for One-Shot Magnitude Pruning and Compute-Adaptive Early Exit** — [2609.12337](https://arxiv.org/abs/2609.12337)  
  Erdem Koyuncu  
  We study compute reduction in neural networks through a unified partial versus full computation view, captured by one-shot magnitude pruning in the static regime and early exit in the adaptive regime. In an asymptotic single-neuron model, we prove a concentration theorem for one-shot magnitude pruning with explicit rates.
- <a id="20260915-2609.12345"></a>**ParaRecover: A Process-Level Benchmark for Error Localization and Recovery in Parallel Tool-Use Agents** — [2609.12345](https://arxiv.org/abs/2609.12345) | cross: cs.SE  
  Bowen Guan, Zhentao Yin, Yanming Shen  
  Existing agent benchmarks mainly evaluate final task success or tool-call correctness, providing limited insight into whether agents can reliably diagnose and recover from intermediate execution failures. This limitation becomes particularly critical in multi-turn parallel tool-use scenarios, where errors may propagate across dependent branches and trigger cascading failures.
- <a id="20260915-2609.12356"></a>**When Connected Does Not Mean Similar: Charting the Homophily Boundary of SNAP-KG for Streaming Entity Integration** — [2609.12356](https://arxiv.org/abs/2609.12356)  
  Jui-Chien Lin, Oshani Seneviratne  
  SNAP-KG is a framework for assigning newly arriving entities to semantic communities in a growing knowledge graph (KG) using only their raw features, with no graph access and no retraining at inference time. It was evaluated on five multi-view benchmarks and a 2.4M-node OGB-WikiKG2 KG.
- <a id="20260915-2609.12364"></a>**LatentVerse: A Framework for Understanding Shared and Modality-Specific Information in Multimodal Latent Representations** — [2609.12364](https://arxiv.org/abs/2609.12364) | cross: cs.HC  
  Majd Alafrange, Samuel Friedman, John Kitonyo, Sana Tonekaboni et al.  
  Latent embeddings have become a central data abstraction in modern machine learning, especially in biomedicine, where foundation models are increasingly used to encode multimodal data like clinical text, medical images, omics, and physiological signals. However, the utility and value of these representations depends on understanding their quality, structure, and the information they encode.
- <a id="20260915-2609.12365"></a>**Certified AI Triage of ICU Alarms** — [2609.12365](https://arxiv.org/abs/2609.12365)  
  Mohammed Sameer Syed, Rozhin Yasaei  
  In the VTaC benchmark 71% of ventricular-tachycardia alarms are false, but silencing a real one can delay recognition of a dangerous arrhythmia. We reframe alarm reduction as three-way triage (retain, suppress, or defer) and bound the decision this analysis treats as harmful: among suppressed alarms, the fraction that were genuine stays below a user-set budget with 95% confidence, under i.i.d.
- <a id="20260915-2609.12386"></a>**Split Conformal Prediction with Label-Shift-Adjusted Bayesian Scores** — [2609.12386](https://arxiv.org/abs/2609.12386)  
  Hyeonsu Lee, Juyeon Kim, Erkhembayar Jadamba, Seungjin Choi et al.  
  Conformal prediction provides distribution-free uncertainty quantification under exchangeability. However, this assumption is violated by label shift, where the marginal distribution of labels changes while the conditional distribution of inputs given labels remains stable.
- <a id="20260915-2609.12418"></a>**RiPPLE: Cross-Space Performance Prediction from Early Training for Neural Architecture Search** — [2609.12418](https://arxiv.org/abs/2609.12418) | cross: cs.CV  
  Yifan Yang, Zhaoyan Wang, Zheng Gao, Xiaoyu Li et al.  
  Neural architecture search (NAS) evaluates candidate networks, but fully training enough architectures to rank an entire space is expensive. Zero-cost proxies score architectures at initialization, yet their ranking quality varies across search spaces.
- <a id="20260915-2609.12424"></a>**Granularity-Adaptive Credit Assignment for Long-Horizon LLM Agent Reinforcement Learning** — [2609.12424](https://arxiv.org/abs/2609.12424)  
  Taoran Liang, Yang Liu, Shang Luo, Yingguang Yang et al.  
  Reinforcement learning is now the standard way to train large language model agents on long-horizon tasks, where dozens of interdependent actions precede a single sparse reward. Critic-free, group-relative methods such as GRPO suit this regime, but they broadcast one trajectory-level scalar to every step and cannot say which decision drove the outcome.
- <a id="20260915-2609.12455"></a>**SAGE-Loop: Reliable Closed-Loop LLM-Driven AutoML with Trial-and-Correction and Adaptive Ensembling** — [2609.12455](https://arxiv.org/abs/2609.12455)  
  Junquan Gu, Shibo Cui, Xiangfeng Luo, Hang Yu  
  Automated machine learning (AutoML) is reshaping data-driven science and industrial practice, and as large language models are introduced into AutoML, pipeline reliability becomes as important as automation efficiency. However, existing AutoML still struggles to realize instant feedback and adaptive optimization during execution, so once a run drifts into a suboptimal or failed state, it lacks a …
- <a id="20260915-2609.12470"></a>**A Differentially Private Federated Proximal Optimization Framework for Customer Churn Prediction in Heterogeneous Federated Telecom Networks** — [2609.12470](https://arxiv.org/abs/2609.12470)  
  Joydeb Kumar Sana, Subrata Chakraborty, M M Manjurul Islam  
  Customer churn is one of the major issues in the telecommunication industry. To predict customer churn, conventional centralized machine learning approaches have been widely used.
- <a id="20260915-2609.12531"></a>**Temporal Recurrence Favors Fewer Layers** — [2609.12531](https://arxiv.org/abs/2609.12531)  
  Ivan Anokhin, Johan Obando-Ceron, Irina Rish, Sebastian Risi  
  In streaming tasks, recurrent models can carry latent computation across time, allowing each update to build on representations produced earlier. This raises a basic question: once temporal recurrence provides sequential computation across steps, how much depth is still needed within each step?
- <a id="20260915-2609.12532"></a>**$\text{GSF-}\chi$: Global Stereochemical Fields for Chiral Graph Transformers** — [2609.12532](https://arxiv.org/abs/2609.12532)  
  Jiaqing Xie, Yuxin Wang, Xipeng Qiu  
  Enantiomers share atoms, bonds, and pairwise distances yet can behave differently in chiral environments, so molecular encoders must respect atom relabelings and proper rotations without becoming blind to reflection. We introduce GSF-$\chi$, a graph transformer in which stereogenic units modulate all pairwise interactions rather than single out one atom as special.
- <a id="20260915-2609.12550"></a>**Quality-Constrained Routing over a Fixed Pool of Quantized Mixture-of-Experts Instances** — [2609.12550](https://arxiv.org/abs/2609.12550)  
  Zhenghong Huang, Hongfan Wu, Jiheng Zhang  
  Quantized Mixture-of-Experts (MoE) services can hold several pre-materialized instances of one base model, but quantization damage varies sharply across requests and bitwidths. Because instance materialization and replica counts consume memory and require slow reconfiguration, we treat them as upstream provisioning decisions and study routing within a fixed resident pool.
- <a id="20260915-2609.12591"></a>**Where Decoder Cosine Similarity Fails for SAE Feature Flow Discovery** — [2609.12591](https://arxiv.org/abs/2609.12591)  
  Hendrik Droste, Christian Medeiros Adriano, Kathrin Korte, Holger Giese  
  Foundation models are increasingly adapted through fine-tuning, model editing, and alignment procedures while retaining previously acquired capabilities. Understanding the internal computations that support these adaptations is therefore becoming increasingly important for continual model evolution.
- <a id="20260915-2609.12594"></a>**Poisson-Corrector Complexity Bounds for Moreau--Yosida Unadjusted Langevin Sampling** — [2609.12594](https://arxiv.org/abs/2609.12594)  
  Yuchen Xin, Zhihua Zhang  
  We study the classical Moreau--Yosida unadjusted Langevin algorithm (MYULA) for $\pi(\,\mathrm{d} x)\propto e^{-f(x)-g(x)}\,\mathrm{d} x$, where $f\in C^2(\mathbb{R}^d)$ is $m$-strongly convex with $L_f$-Lipschitz gradient and $g:\mathbb{R}^d\to\mathbb{R}$ is convex and globally $G$-Lipschitz. For the Moreau-smoothed target $\pi_\lambda$ and the MYULA invariant law $\widehat\pi_{\lambda,h}$, we …
- <a id="20260915-2609.12627"></a>**Geometric-to-Semantic Spherical Transfer Learning for Cortical Sulci Labeling** — [2609.12627](https://arxiv.org/abs/2609.12627) | cross: cs.CV  
  Saeb Tounsi, Jo\"el Chavas, Pietro Gori, Vincent Frouin et al.  
  Deep learning on cortical surfaces faces a dilemma: capturing the complex topology of over 60 nomenclature-dependent sulci per hemisphere requires high-capacity models, yet the extreme scarcity of expert annotations ($N=62$ subjects) inevitably causes overfitting. Standard supervised approaches fail to generalize in this data-scarce regime, particularly for variable and small sulci where …
- <a id="20260915-2609.12651"></a>**Distortion of AI Alignment Revisited: RLHF is a Decent Utilitarian Aligner** — [2609.12651](https://arxiv.org/abs/2609.12651) | cross: cs.GT  
  Kazusato Oko, Annie Ulichney, Nika Haghtalab, Han Bao  
  While Reinforcement Learning from Human Feedback (RLHF) is the standard paradigm for aligning large language models with human preferences, its effectiveness in pluralistic settings has been called into question. Notably, recent work by G\"olz et al.
- <a id="20260915-2609.12658"></a>**ProactiveBench: Can Streaming Video Models Really Interact Like Humans?** — [2609.12658](https://arxiv.org/abs/2609.12658)  
  Kaixuan Du, Xin Wan, YuKun Wang, Hang Zhang et al.  
  Streaming video understanding requires models to process continuous multimodal input while maintaining temporal context. Existing evaluations are predominantly reactive: they query a model at a selected timestamp and therefore do not assess when it should respond.
- <a id="20260915-2609.12690"></a>**SIFPBPNet: A Dual-Path Network for Wearable and Cuffless Blood Pressure Estimation via Individualized Steady-state Representation** — [2609.12690](https://arxiv.org/abs/2609.12690)  
  Shuailong Tang, Xiaoyu Li, Donglin Xie, Wei Chen et al.  
  Continuous and cuffless blood pressure (BP) monitoring using photoplethysmography (PPG) is of great interest for low-cost and personalized cardiovascular health management. However, significant population heterogeneity and the "one-to-many mapping" problem, where similar waveforms across individuals correspond to different BP levels, limit the accuracy of conventional population-based models.
- <a id="20260915-2609.12702"></a>**Write on Paper and Get the Online Digital Trace:\newline A New Era for Handwriting** — [2609.12702](https://arxiv.org/abs/2609.12702)  
  Florent Imbert, Yann Soullard, Eric Anquetil, Tanja Harbaum et al.  
  Capturing the digital trace of handwriting usually requires a specific stylus and a compatible substrate, be it a capacitive touchscreen, an ElectroMagnetic Resonance (EMR) tablet as used in Wacom systems or special paper. While writing on regular paper offers rich haptics, no latency and is well known for improving information retention, no low-cost and widely accepted, effective solution exists …
- <a id="20260915-2609.12735"></a>**Physics-Guided Synthetic High-Frequency Ultrasound Generation for Skin Layer Segmentation** — [2609.12735](https://arxiv.org/abs/2609.12735) | cross: cs.CV  
  Junkyung ju, Kyungho Yoon, Minwoo Shin  
  High-frequency ultrasound (HFUS) enables noninvasive visualization of superficial skin structures, but automated skin-layer analysis is limited by the scarcity of densely annotated data. Existing real HFUS datasets commonly provide annotations for superficial targets such as the epidermis and subepidermal low-echogenic band (SLEB), while dense labels for deeper structures such as dermis, …
- <a id="20260915-2609.12752"></a>**Optimizing for the decision not the prediction: an exploration of Smooth Net Benefit as a training objective** — [2609.12752](https://arxiv.org/abs/2609.12752)  
  Koen M. F. Gorgels, Lasai Barre\~nada, Maarten van Smeden, Ben Van Calster et al.  
  Objective Prediction models are commonly trained using objectives such as Bernoulli negative log-likelihood (NLL), although downstream clinical decisions may depend on specific risk thresholds. We introduce Smooth Net Benefit ($\sigma$NB), a differentiable approximation of Net Benefit designed to align model training with threshold-specific clinical utility.
- <a id="20260915-2609.12758"></a>**Curriculum-Based Adversarial Heterogeneous Agent Reinforcement Learning for Autonomous Quad-Copter Landing in Maritime Settings** — [2609.12758](https://arxiv.org/abs/2609.12758)  
  Allan Minh-Tam Nguyen, Sree Showrya Kotala, Stefan Banioi-Crijman, Kurt Driessens et al.  
  Recovering unmanned aerial vehicles (UAVs) in maritime environments is challenging due to wind turbulence and ship-deck motion, making it a valuable test case for alternative control and learning approaches as conventional landing approaches often become unreliable. We study simulated mid-air capture of quadrotor UAVs by a ship-mounted robotic arm, learning robust cooperative control policies …
- <a id="20260915-2609.12785"></a>**Convergence of Stochastic Gradient Methods under Heavy-Tailed Noise and H\"{o}lder Smoothness** — [2609.12785](https://arxiv.org/abs/2609.12785) | cross: math.OC, stat.ML  
  Misbah Uz Zaman, Anirbit Mukherjee  
  Classical convergence guarantees for stochastic gradient methods typically assume Lipschitz-smooth objectives and finite-variance gradient noise, both frequently violated in practice. In contrast, we study nonconvex stochastic optimization under the joint relaxation of these assumptions: objectives with $(L,s)$-H\"older continuous gradients, $s\in(0,1]$, and gradient noise satisfying only a …
- <a id="20260915-2609.12793"></a>**VertiFuseX: Generalizable Financial Forecasting via Multi-Stream Temporal Fusion** — [2609.12793](https://arxiv.org/abs/2609.12793) | cross: q-fin.ST  
  Aashish Bohra, Vivek Vijay  
  Stock price prediction remains challenging due to the non-stationary and noisy nature of financial time series. Existing deep learning models often rely on rigid decision-level fusion, ad hoc hyperparameter tuning, and compressed final-layer outputs, causing information loss, overfitting, and limited cross-market generalization.
- <a id="20260915-2609.12863"></a>**GenOR-Twin: A Semantic Middleware for Integrating Operational Discourse with Mathematical Optimization** — [2609.12863](https://arxiv.org/abs/2609.12863)  
  Rahimeh Neamatian Monemi, Shahin Gelareh, Lubin Cui, Nelson Maculan  
  We introduce GenOR-Twin, a neuro-symbolic framework that bridges the translation gap between unstructured operational logs and rigorous mathematical optimization. Our architecture uniquely positions Large Language Models as semantic translators rather than direct solvers, ensuring that the system retains the feasibility guarantees of exact combinatorial methods.
- <a id="20260915-2609.12875"></a>**What an odour descriptor corpus can and cannot measure: valence, attenuation, and the ceiling of the public record** — [2609.12875](https://arxiv.org/abs/2609.12875)  
  Stylianos Kampakis, Fabio Rovai  
  Machine olfaction trains on pooled public descriptor corpora, but whether a shared descriptor word measures the same thing across corpora has not been tested, nor has the ceiling of what any of them can measure. We audit four corpora from Pyrfume.
- <a id="20260915-2609.12891"></a>**Quantifying the Value of Privileged Information Using a PAC-Bayesian Approach** — [2609.12891](https://arxiv.org/abs/2609.12891)  
  Vasily Bokov (aQa, Leiden University, The Netherlands, LIACS et al.  
  In practice, various learning scenarios provide access to auxiliary features exclusively during training. Incorporating such data to enhance model performance gave rise to a paradigm known as Learning Using Privileged Information (LUPI).
- <a id="20260915-2609.12899"></a>**Physical-State-Guided Diffusion Sampling for Full-Waveform Inversion** — [2609.12899](https://arxiv.org/abs/2609.12899)  
  Chen Min, Haowen Jiang, Zheng Ma, Xiongbin Yan  
  Full waveform inversion (FWI) estimates subsurface velocity from seismic recordings, but its ill-posedness and nonlinearity make accurate reconstruction strongly dependent on initialization and prior information. Diffusion posterior sampling provides a learned geological prior, yet directly coupling its denoiser to the nonlinear wave solver can yield unreliable physical guidance.
- <a id="20260915-2609.12903"></a>**Hidden in Rounds: Predicting the Time Cost of 802.11 Contention in Federated Learning** — [2609.12903](https://arxiv.org/abs/2609.12903) | cross: cs.DC  
  Satwat Bashir, Tasos Dagiuklas  
  Federated learning over IEEE~802.11 shares the wireless channel among clients that send model updates. We use ns-3 to measure the frame-delivery ratio and saturation throughput for different client densities and offered loads.
- <a id="20260915-2609.12905"></a>**Offline Reinforcement Learning for Wind Farm Control: A Wind Tunnel Study under Dynamic Wind Directions** — [2609.12905](https://arxiv.org/abs/2609.12905)  
  Yuhan Su, Hongyang Dong, Simone Tamaro, Filippo Campagnolo et al.  
  This paper addresses the wind farm power maximization problem in the presence of wind direction changes. Specifically, a model-free Modified Twin Delayed Deep Deterministic Policy Gradient with Behavior Cloning (MTD3-BC) algorithm is proposed to tackle this task through yaw control under varying wind direction conditions.
- <a id="20260915-2609.12938"></a>**A Large-Scale AIS Dataset from Finnish Water** — [2609.12938](https://arxiv.org/abs/2609.12938)  
  Debayan Bhattacharya, Ikram Ul Haq, Carlos Pichardo Vicencio, Sebastien Lafond  
  This research paper contributes to the maritime research community by introducing a comprehensive AIS dataset from Finnish waters, specifically the Baltic Sea region. AIS data, initially designed for collision prevention, have evolved into a versatile tool with applications across diverse maritime domains.
- <a id="20260915-2609.12991"></a>**Information-Induced Training Geometry: Exact Reduction, Canonical Completion, and Structured Expressivity** — [2609.12991](https://arxiv.org/abs/2609.12991) | cross: math.OC  
  Zavier Li  
  Training data constrains optimizer geometry through the covectors visible to a declared information channel. We study how such partial information determines a full positive cometric relative to a reference and which degrees of freedom remain unidentified.
- <a id="20260915-2609.12994"></a>**Dimension-Corrected Hitting Times for Heavy-Tailed Spectral Emergence in Neural Optimizer Dynamics** — [2609.12994](https://arxiv.org/abs/2609.12994) | cross: cs.NE, stat.ML  
  Zongmin Liu  
  Heavy-tailed empirical spectral densities of neural-network weight matrices are widely used as diagnostics of implicit self-regularization, but the step complexity of heavy-tail emergence remains poorly understood. We formulate spectral heavy-tail formation as a right-censored hitting-time problem: a run that does not reach a heavy-tail diagnostic within the observation horizon is treated as …
- <a id="20260915-2609.12996"></a>**A Full Adam Theorem for Spectral Heavy-Tail Onset** — [2609.12996](https://arxiv.org/abs/2609.12996) | cross: math.PR, stat.ML  
  Zongmin Liu  
  We prove a full Adam theorem for spectral heavy-tail onset in a closed Gaussian Stein-Hermite teacher-student state-evolution model. The theorem begins with the actual full-batch Adam recurrences, derives the population gradient by Stein-Hermite calculus, proves finite-width covariance concentration, converts multi-step Adam momentum into an exact non-centered Gaussian sign kernel, controls the …
- <a id="20260915-2609.13010"></a>**Dual-guided Hierarchical Edge Localization for Large-scale Optimal Transport Across Dimensions** — [2609.13010](https://arxiv.org/abs/2609.13010)  
  Wenzhou Xia, Qiaoqiao Ding, Jingwei Liang, Xiaoqun Zhang  
  Optimal transport (OT) compares distributions and aligns datasets in machine learning, yet unregularized discrete OT requires a linear program with quadratically many transport variables. We propose HELLO, a hierarchical solver that casts large-scale discrete OT as edge localization and uses dual potentials to guide both coarse-to-fine initialization and within-level refinement.
- <a id="20260915-2609.13039"></a>**Transfer Learning for Evolving Domains** — [2609.13039](https://arxiv.org/abs/2609.13039) | cross: stat.ML  
  Ricardo Ribeiro Pereira, Jacopo Bono, Hugo Ferreira, Pedro Ribeiro et al.  
  Transfer learning explores how to leverage knowledge from various tasks or domains (sources) to enhance predictive performance in related tasks or domains (targets). Typically, transfer learning research is segmented into several isolated sub-areas (such as domain generalisation, domain adaptation, or multi-domain learning), each making distinct assumptions about target data availability, namely …
- <a id="20260915-2609.13040"></a>**Quantile-based Loss Filtering for Outlier-Robust Stochastic Gradient Descent** — [2609.13040](https://arxiv.org/abs/2609.13040) | cross: cs.NA, math.NA  
  Jamie Haddock, Anna Ma, Elizaveta Rebrova  
  We study loss-based filtering for finite-sum optimization with a subset of corrupted component functions whose gradients may be highly unreliable. Motivated by minimum-loss-based SGD (min-$k$-loss) and quantile-based methods for corrupted linear systems, we propose and analyze a general loss-filtering framework -- Quantile-\(k\)-Loss SGD (Q\(k\)L-SGD) -- that samples \(k\) component losses at …
- <a id="20260915-2609.13044"></a>**Robust Policy Optimization via Adversarial Importance Sampling** — [2609.13044](https://arxiv.org/abs/2609.13044)  
  Amine Andam, Jamal Bentahar, Mustapha Hedabou  
  Significant progress has been made in safeguarding deep reinforcement learning (DRL) policies against input perturbations. Developing robust DRL involves three main stages: algorithm design, implementation, and evaluation.
- <a id="20260915-2609.13048"></a>**MCRL2: Multi-resource Cross-attention-based Representation Learning-augmented Reinforcement Learning for Cloud Microservice Scheduling** — [2609.13048](https://arxiv.org/abs/2609.13048)  
  Tiangang Li, Shi Ying, Xiangbo Tian, Chuan Shi et al.  
  Efficient microservice scheduling is crucial for maintaining load balance across nodes in data centers and ensuring high quality of service. However, achieving this in practice remains challenging due to dynamic resource imbalance under fluctuating workloads, nonlinear coupling across multiple resource dimensions, and the heterogeneity of microservice resource demands.
- <a id="20260915-2609.13050"></a>**A Unified and Constrained View of Regularization-Based Robust Reinforcement Learning** — [2609.13050](https://arxiv.org/abs/2609.13050)  
  Amine Andam, Jamal Bentahar, Mustapha Hedabou  
  Regularization-based methods have become a standard approach for training Deep Reinforcement Learning policies against adversarial input perturbations. In this paper, we unify these methods by deriving new upper bounds on the performance gap between the nominal and worst-case policies.
- <a id="20260915-2609.13057"></a>**Benign Loss Landscapes Can Coexist with Worst-Case Hardness** — [2609.13057](https://arxiv.org/abs/2609.13057) | cross: stat.ML  
  Zach Furman, Stephan W\"aldchen, Yangda Bei, Liam Hodgkinson  
  Deep neural networks are expressive enough to contain worst-case targets that can be evaluated in polynomial time but cannot be learned in polynomial time by gradient descent. For practical tasks they nonetheless learn well, raising the question of what non-generic structure of real-world targets enables this.
- <a id="20260915-2609.13060"></a>**CanvasAnneal: Curriculum Reinforcement Learning for Diffusion Language Models** — [2609.13060](https://arxiv.org/abs/2609.13060)  
  Blake Olson, Yuhang Song, Emmett McQuinn, Yuan Shangguan  
  Diffusion Language Models (DLMs) offer promising parallel generation capabilities but lag behind autoregressive models in complex reasoning and tool-use tasks. While Reinforcement Learning (RL) has recently been applied to enhance DLMs, standard RL approaches suffer from an exploration bottleneck.
- <a id="20260915-2609.11933"></a>**Towards Sustainable Hydrogen Systems: Supply Chain Optimization with Model Predictive Control and Reinforcement Learning** — [2609.11933](https://arxiv.org/abs/2609.11933) | cross: cs.LG  
  Mahammad Valiyev  
  Hydrogen supply chains are expected to play a central role in future low-carbon energy systems by enabling renewable energy integration, long-duration storage, and decarbonization of industrial and transportation sectors. However, their operation is challenged by renewable generation variability, electricity price fluctuations, uncertain hydrogen demand, and engineering constraints associated …
- _…另有 32 篇, 见 `data/20260915.json`_

#### cs.DB (3)

- <a id="20260915-2609.12535"></a>**QEmbed: A Deep Learning Based Cardinality Estimator for Efficient Query Processing** — [2609.12535](https://arxiv.org/abs/2609.12535)  
  Pooja Rajput, Suman Banerjee  
  Cardinality estimation is at the core of any commercial database system for efficient query processing. Over the decades, non-learning-based estimation techniques (e.g., histogram-based, sampling-based) have been widely used in both commercial and open-source database platforms.
- <a id="20260915-2609.12597"></a>**Invisible Yet Dominant: Big Stalls of Kernel I/O Mechanisms in Cloud OLTP Databases** — [2609.12597](https://arxiv.org/abs/2609.12597) | cross: cs.OS  
  Mitsumasa Kondo  
  Most databases, including PostgreSQL, RocksDB, and recent AI KV-cache middleware, rely on buffered I/O, delegating write-back to the Linux kernel. On the distributed block storage standard in the cloud, this delegation inherits a hidden bottleneck: each device is drained by a single kernel flusher thread over a high-latency, shallow-queue path.
- <a id="20260915-2609.12745"></a>**How Do Data Collection Strategy and Data Quality Influence the Outcomes of Digital Technology Adoption?** — [2609.12745](https://arxiv.org/abs/2609.12745)  
  Xuejiao Li, Cheng Yang  
  In the era of Industry 4.0 (I4.0), data has become the essential foundation for digital transformation, yet many organizations still struggle to link data practices with digital performance outcomes. This study investigates how data collection strategy and data quality jointly influence the success of digital technology adoption (DTA) in manufacturing firms.

#### cs.DC (24)

- <a id="20260915-2609.12091"></a>**Shards on a Shoestring: Empirical Characterization of NEAR Protocol Nightshade Sharding on Commodity Hardware** — [2609.12091](https://arxiv.org/abs/2609.12091) | 🎯★ BFT  
  Sohini Sahukar, Om Amit Gandhi, Ioan Raicu  
  NEAR Protocol's Nightshade architecture targets one million transactions per second (TPS) through horizontal sharding of both state and computation. Published benchmarks were produced on expensive Google Cloud Platform infrastructure costing approximately \$700 per hour, leaving a significant reproducibility gap for academic research.
- <a id="20260915-2609.12143"></a>**Consensus-based Decentralized Distributed Swarm Learning with Heterogeneous Big Data** — [2609.12143](https://arxiv.org/abs/2609.12143) | 🎯★ consensus  
  Zhuoyu Yao, Dong Yang, Yue Wang, Songyang Zhang et al.  
  Artificial intelligence increasingly relies on large-scale, distributed, and heterogeneous data collected by edge devices. However, the practice of edge intelligence remains challenging due to non-convex objectives, data heterogeneity, and complex wireless network topology.
- <a id="20260915-2609.12239"></a>**Specifying Paxos for System Builders: Pseudocode Made Executable** — [2609.12239](https://arxiv.org/abs/2609.12239) | 🎯★ consensus, Paxos  
  Yanhong A. Liu, Rahul Sihag  
  This paper presents a precise executable specification---as a faithful mapping from the pseudocode---of Paxos for System Builders, a practical protocol for replication and consensus in distributed systems. Paxos for System Builders has both a robust implementation in C and a clean pseudocode for critical protocol details.
- <a id="20260915-2609.12551"></a>**RoofLang: Enabling AI-Driven Architecting of LLM Inference Systems** — [2609.12551](https://arxiv.org/abs/2609.12551) | cross: cs.AI  
  Ziyue Yang, Yuting Jiang, Lei Qu, Peng Cheng  
  AI is beginning to make substantive contributions to LLM inference optimization. Existing AI optimizations are predominantly profiling-based.
- <a id="20260915-2609.11936"></a>**One Simple Trick for Improving the Performance of Energy-Limited Local Inference and Training** — [2609.11936](https://arxiv.org/abs/2609.11936) | cross: cs.DC, cs.LG  
  Erik Schultheis, Maximilian Kleinegger, Dan Alistarh  
  Energy supply and heat dissipation are two of the main challenges with modern GPU deployments. While typically discussed in the context of new datacenter constructions, the same constraints also apply to small form-factor consumer devices, such as the DGX spark.
- <a id="20260915-2609.11946"></a>**Hyperion: An AI-powered HPC cluster for sciences and humanities research that utilizes ML for predicting job turnaround time** — [2609.11946](https://arxiv.org/abs/2609.11946) | cross: cs.LG  
  Jun Zhou, Nathan Elgar, Tawnee Benedetto, John Richards et al.  
  Hyperion is an innovative high-performance computing (HPC) cluster developed for researchers in both science and humanities disciplines at the University of South Carolina (USC). Our approach involved constructing a HPC cluster designed to meet the current research needs while accommodating future expansion.
- <a id="20260915-2609.12075"></a>**Efficient Vision-Language-Action Management and Serving for Robot Factories** — [2609.12075](https://arxiv.org/abs/2609.12075) | cross: cs.AR, cs.LG, cs.PF, cs.RO  
  Dionysios Adamopoulos, Nattapol Chanpaisit, Basel Fakhri, Christina Giannoula  
  Vision-Language-Action (VLA) models show high robotic manipulation capabilities via a two-stage design: a Vision-Language Model (VLM) stage followed by an Action Diffusion Transformer (ADiT) stage. Since robots must meet strict Service-Level Objectives (SLOs) for safety, VLA inference is inherently latency-critical.
- <a id="20260915-2609.12412"></a>**HoliBench: A Cross-Platform Benchmarking and Deployment Toolkit for Foundation Models in CPS-IoT Applications** — [2609.12412](https://arxiv.org/abs/2609.12412) | cross: cs.LG, cs.PF  
  Inesh Chakrabarti, Zejun Xiong, Pragya Sharma, Mani Srivastava  
  Foundation models, including large language models, vision-language models, and time-series foundation models, are increasingly deployed on embedded and edge platforms for CPS and IoT applications, where energy, latency, and memory are as critical as task accuracy. Existing benchmarking tools evaluate model capability in isolation, reporting accuracy assuming sufficient compute, while hardware …
- <a id="20260915-2609.12923"></a>**Dissecting GPU Utilization for LLM Inference on Nvidia Hopper** — [2609.12923](https://arxiv.org/abs/2609.12923) | cross: cs.AR, cs.DC, cs.LG  
  Mohammad Siavashi, Gerald Q. Maguire Jr., Dejan Kostic, Marco Chiesa  
  A single SM utilization percentage can make an LLM inference workload look compute-saturated while hiding how much useful work is being done. The problem is not that the counter is wrong, but that it collapses several different mechanisms into one number.
- <a id="20260915-2609.11944"></a>**Asynchronous Parallel Search for Exact Multi-Objective Shortest Paths with Versioned Frontier Snapshots and Indexed Dominance Pruning** — [2609.11944](https://arxiv.org/abs/2609.11944)  
  Xiaoqing Xu, Ning Zhang, Liuyihui Qian, Xiaojun Liu et al.  
  Exact multi-objective shortest-path (MOSP) search computes the complete Pareto set between specified start and goal vertices, and its computational cost can grow rapidly with expanding nondominated label sets and frequent dominance tests over per-vertex Pareto frontiers. Efficiently parallelizing exact MOSP remains an open challenge.
- <a id="20260915-2609.12299"></a>**Argus: Orchestrating Cross-Layer GPU Performance Measurements around Semantic Regions** — [2609.12299](https://arxiv.org/abs/2609.12299) | cross: cs.PF  
  Jianzhu Yao, Yue Guan, Srivatsan Ramesh, Yuanwei Fang et al.  
  GPU developers and automated optimizers need performance evidence for semantic code regions--such as neural-network operator implementations and pipeline stages--but this evidence is fragmented across profiling tools. Answering a region-level question can require manually constructing probes and program variants, isolating interfering measurements, and mapping evidence to regions and execution …
- <a id="20260915-2609.12330"></a>**Unleashing the Power of Equality Saturation for Tensor Program Superoptimization** — [2609.12330](https://arxiv.org/abs/2609.12330)  
  Qi Zhan, Xing Hu, Xin Xia, Shanping Li  
  Efficient GPU implementations of tensor programs often require joint optimization of high-level algebraic formulations and low-level execution strategies. However, the resulting search space grows rapidly as transformations combine across operators, making joint optimization difficult to scale.
- <a id="20260915-2609.12379"></a>**ForgeMegakernel: A General Framework for Efficient Auto-Regressive Model Decode Megakernels** — [2609.12379](https://arxiv.org/abs/2609.12379)  
  Leshan Li, Zhui Zhu, Xianglong Deng, Yaojian Chen et al.  
  Auto-regressive model decode is bandwidth-bound, since every weight and key/value-cache byte crosses high-bandwidth memory once per token. A megakernel is an ideal solution, but existing automatic megakernel generation approaches cannot achieve both generalization across models and correctness guarantees.
- <a id="20260915-2609.12449"></a>**HeatCache: Thermal-aware Energy-efficient LLM Inference Scheduling for Chassis-level Liquid Cooling in Sustainable Edge Server Rooms** — [2609.12449](https://arxiv.org/abs/2609.12449) | cross: cs.PF, cs.SY, eess.SY  
  Rui Lu, Huanghuang Liang, Kaiqi Guan, Dan Wang  
  LLM inference is increasingly deployed at institution-scale edges to meet service requirements. However, multi-GPU inference consumes a large amount of electricity and produces substantial heat.
- <a id="20260915-2609.12602"></a>**GreenDirector: carbon- and water-aware workload placement for sustainable computing** — [2609.12602](https://arxiv.org/abs/2609.12602)  
  Jime Iglesias Blanco, Ignacio Heredia, Mar\'ia Castrillo, Andrei Tsaregorodtsev et al.  
  The rapid growth of data center electricity demand, accelerated by AI, makes carbon-only accounting an incomplete measure of computing's environmental impact: low-carbon electricity mixes are often water-intensive, and the resulting harm depends on local, seasonal scarcity rather than on the volume of water consumed. We propose the Environmental Score (ES), a unified, dimensionless index in $[0, …
- <a id="20260915-2609.12975"></a>**A Dynamic Vertical Scaling Strategy for Distributed Stream Processing Applications in Edge Computing** — [2609.12975](https://arxiv.org/abs/2609.12975)  
  Guilherme Hiago Costa dos Santos, Carlos Henrique Kayser, Tiago Coelho Ferreto  
  Distributed Stream Processing applications at the edge must reconcile low latency and high throughput with limited and heterogeneous resources. This paper presents a dynamic vertical scaling strategy based on Proximal Policy Optimization, formulated as a Partially Observable Markov Decision Process.
- <a id="20260915-2609.11932"></a>**Throughput per Megabyte: A Pilot Benchmark of Language-Stack Efficiency for Self-Hosted HTTP Services on a Raspberry Pi 5** — [2609.11932](https://arxiv.org/abs/2609.11932) | cross: cs.DC, cs.PL  
  William Oliveira  
  Cloud-centric web benchmarks miss constraints that matter for self-hosted services on ARM64 single-board computers, especially idle RAM footprint and energy per request. We ran a pilot benchmark on one Raspberry Pi 5, measuring equivalent SQLite-backed CRUD APIs implemented in Go 1.26/net/http, Rust 1.95/Axum, Python 3.13/FastAPI+Granian, Node.js 24/Fastify, and .NET 10 Native AOT across N=50 …
- <a id="20260915-2609.11938"></a>**Hardware-Attributed Operator Profiling for PyTorch** — [2609.11938](https://arxiv.org/abs/2609.11938) | cross: cs.DC, cs.PF  
  Logan Chu, Dong Li  
  Framework profilers expose operator timing without hardware counters; GPU profilers expose hardware counters without operator attribution. Bridging this gap manually is error-prone and does not scale.
- <a id="20260915-2609.11939"></a>**Adaptive AI: Energy Efficient Multi-exit TinyML on Intelligent Vision Systems at the Edge** — [2609.11939](https://arxiv.org/abs/2609.11939) | cross: cs.CV, cs.DC  
  Luca Crupi, Lorenzo Lamberti, Alessandro Giusti, Daniele Palossi  
  Traditional TinyML systems for edge devices achieve high accuracy by relying on fixed-depth models that require a constant number of multiply-accumulate (MAC) operations regardless of the input complexity. This approach wastes critical resources in battery-powered Internet-of-Things (IoT) devices and limits the real-time performance of edge cyber-physical systems.
- <a id="20260915-2609.12582"></a>**NovaFabric: Tamper-Evident, Replayable Evidence for Autonomous AI Agent Runs** — [2609.12582](https://arxiv.org/abs/2609.12582) | cross: cs.DC  
  Mohsen Seyedkazemi Ardebili  
  When an autonomous AI agent does something consequential, what can be proven about what it did? Agent-observability platforms capture traces, but a trace is mutable: alterable undetected, with no recipe for re-executing it, silent on whether captured secrets were removed.
- <a id="20260915-2609.12605"></a>**A Feature-Rich Embedded NIDS with eBPF/XDP: Detector and Architecture Trade-offs** — [2609.12605](https://arxiv.org/abs/2609.12605) | cross: cs.DC, cs.NI  
  Shiqi Wu, Oleksii Koshovyi, Georgios Pseiridis Pseiras, Victor Morel et al.  
  Distributed Denial-of-Service (DDoS) attacks remain a serious threat to transport networks, with recent attack volumes exceeding 30 Tbps, and the telecommunications industry being the main target. Recent work has yet to study the impact of the hosting software architecture on network monitoring solutions, or to assess recent algorithms for improving attack detection.
- <a id="20260915-2609.12649"></a>**Hybrid Monitoring for Early Fault Detection in Cloud-Native 5G Systems** — [2609.12649](https://arxiv.org/abs/2609.12649) | cross: cs.DC  
  Anton Andersson, Sai Akshara Naineni, Mats Jansborg, Yixing Zhang et al.  
  This paper presents the design implementation and evaluation of NetMon a hybrid network monitoring system designed for Kubernetes-based 5G packet core deployments specifically evaluated on Ericssons Access and Mobility Management Function AMF clusters NetMon combines eBPF-based passive kernel-level traffic observation with active TCP probing and centralized correlation to detect and localize …
- <a id="20260915-2609.13064"></a>**NFT-Based Reward Mechanisms: Sybil Farming, Vesting, and Stochastic Verification** — [2609.13064](https://arxiv.org/abs/2609.13064) | cross: cs.DC, cs.GT  
  Marco Alberto Javarone, Stefanos Leonardos, Carmine Ventre  
  We study NFT-based reward mechanisms in which a user can create multiple identities and submit fraudulent claims that mature a reward subject to vesting. We assume that the issuer stochastically verifies claims during the vesting period and that identities can be linked into clusters so that the detection of one identity submitting a fraudulent claim causes the whole cluster to be forfeited …
- <a id="20260915-2609.13115"></a>**Extreme-Scale Linear-Scaling Kohn-Sham DFT at 100 Million Atoms: Bridging Quantum Simulations and Experiments** — [2609.13115](https://arxiv.org/abs/2609.13115) | cross: cs.DC, physics.comp-ph  
  Qimen Xu, Yu Zhang, Dixing Ni, Lei Gao et al.  
  Kohn-Sham density functional theory (DFT) remains the workhorse of ab initio materials simulation, yet cubic computational and quadratic memory scaling have confined calculations to a few hundred to thousands of atoms, spanning only nanometers, far below experimentally relevant length scales. We introduce XLSDFT, a linear-scaling DFT framework based on divide-and-conquer decomposition of the …

#### cs.FL (2)

- <a id="20260915-2609.12106"></a>**A Non-constant Lower Bound for Grammar-Based Compression with Greedy** — [2609.12106](https://arxiv.org/abs/2609.12106) | cross: cs.FL | 🎯★ formally verified | 🎯🧐 formally verified  
  Danny Hucke  
  We prove a lower bound of {\Omega}(log n/ log log n) on the approximation ratio of the global grammar-based compression algorithm Greedy. To our knowledge, the previously best lower bound was a constant, and the existence of a nonconstant lower bound had remained open for more than twenty years.
- <a id="20260915-2609.12209"></a>**Stochastic Hybrid Automata for Power Profile Modeling in Energy Systems** — [2609.12209](https://arxiv.org/abs/2609.12209)  
  Lisa Willemsen, Anne Remke, Johann L. Hurink  
  Power profiles are widely used to describe power demand and production in energy systems. Yet, real-world usage often involves uncertainty, making it challenging to determine, e.g., whether a battery can reliably meet a given profile.

#### cs.LO (1)

- <a id="20260915-2609.12715"></a>**Supermartingale Certificates for Parametric MDPs** — [2609.12715](https://arxiv.org/abs/2609.12715) | cross: cs.AI, cs.SY, eess.SY | 🎯★ formal verification  
  Kaushik Mallik, {\DH}or{\dj}e \v{Z}ikeli\'c  
  We consider the problems of formal verification and synthesis in parametric Markov decision processes (MDPs) with general measurable state and action spaces. The heart of our approach is a parameter flattening transformation, which allows us to transform parametric MDPs into semantically equivalent non-parametric MDPs.

#### cs.SE (27)

- <a id="20260915-2609.10630"></a>**AI Safety: Not Optional, Not Later** — [2609.10630](https://arxiv.org/abs/2609.10630) | cross: cs.AI  
  Qinghua Lu, Yoshua Bengio  
  Incidents show that AI safety failures often arise across multiple layers. We present a safety-by-design assurance architecture combining model-level supervision, such as Scientist AI, with system-level controls over scaffolds and harnesses, independent verification, monitoring, and evidence infrastructure, supported by governance for accountability and evidence interoperability.
- <a id="20260915-2609.11559"></a>**PRISMA-LLM: An Empirical Reporting Framework for AI-Assisted Systematic Reviews** — [2609.11559](https://arxiv.org/abs/2609.11559) | cross: cs.AI, cs.CL  
  Miguel Zabaleta, Baihan Lin  
  Large language models (LLMs) and AI-enabled software increasingly participate in systematic-review decisions, yet the information needed to audit these workflows is reported inconsistently. We analyze SciLitBench, a corpus of 888 review-automation papers with 14,726 annotations, to characterize changes in methods, review-stage use, evaluation and reported limitations.
- <a id="20260915-2609.12017"></a>**When Agent Metrics Measure Different Things: An Evidence-Grounded Audit of the Praxa AI Pipeline** — [2609.12017](https://arxiv.org/abs/2609.12017) | cross: cs.AI  
  Stefan G. Creadore, Peyton Woakz  
  Agent evaluations can be numerically correct while measuring a different construct from the one implied by their labels. We present a retrospective measurement audit of selected Praxa AI implementation files, historical evaluation artifacts, and operational records.
- <a id="20260915-2609.12039"></a>**Reality Is the Final Verifier: On Two Key Gaps in Agentic Software Engineering** — [2609.12039](https://arxiv.org/abs/2609.12039) | cross: cs.AI  
  Alexander Krentsel, Shubham Agarwal, Mert Cemri, Shu Liu et al.  
  Software development follows an implementation-verification loop in which developers or agents iteratively revise an implementation until an evaluator, such as a test suite, accepts it. The evaluator checks the implementation against a set of requirements under a model of the deployment environment.
- <a id="20260915-2609.12156"></a>**A decision-basis contract for auditable LLM-assisted medical billing verification: deterministic rules, verbatim evidence, and fail-closed abstention** — [2609.12156](https://arxiv.org/abs/2609.12156) | cross: cs.AI  
  Jan H\"olter, Kevin Geis, Benjamin Raab, Boris Bauke  
  This work presents a proof of concept for auditable LLM-assisted medical billing verification based on a decision-basis contract. The contract separates deterministic checks of versioned fee-catalog rules from LLM-based assessment of free-text documentation.
- <a id="20260915-2609.12190"></a>**Retrieval-Augmented Generation for Scientific Code Understanding** — [2609.12190](https://arxiv.org/abs/2609.12190) | cross: cs.AI  
  Aaron Nobile, Andreas Adelmann, Mohsen Sadr  
  Large language models have become central to modern coding assistants, but state-of-the-art systems such as Claude Code or Codex rely on very large, cloud-hosted models with significant computational cost and data-privacy implications. This work investigates whether a useful, fully local coding agent can be built around small open-source models by shifting the computational burden away from …
- <a id="20260915-2609.12231"></a>**Learning to adapt GR(1) specifications through degradation** — [2609.12231](https://arxiv.org/abs/2609.12231) | cross: cs.AI, cs.LO  
  Tiberiu-Andrei Georgescu, Dalal Alrajeh, Sebastian Uchitel  
  Reactive synthesis is a powerful tool for generating correct-by-construction controllers from formal specifications. GR(1) is an assume-guarantee specification framework that enables efficient synthesis, allowing synthesised controllers to be used in a wide array of applications.
- <a id="20260915-2609.12656"></a>**Separating Engineering Reasoning from DEXPI Serialization in LLM-Based Greenfield Surface-Process Design: A Three-Case Study for Underground Gas Storage** — [2609.12656](https://arxiv.org/abs/2609.12656) | cross: cs.AI  
  Qingchuan Zhu, Shuyue Tong, Pengju Ren  
  Large language models can produce engineering descriptions and structured process representations, but standards-level serialization can substantially increase the generation burden. This diagnostic study examines whether separating engineering reasoning from Data Exchange in the Process Industry (DEXPI) serialization changes where representation and engineering failures occur in constrained …
- <a id="20260915-2609.12708"></a>**What is the Difference Between Me and You? Benchmarking the Quality Gap Between Human-Written and AI-Generated Code** — [2609.12708](https://arxiv.org/abs/2609.12708) | cross: cs.AI  
  Cristina Improta, Pietro Liguori, Domenico Cotroneo  
  AI coding assistants are becoming co-authors of production software, yet their evaluation centers on functional correctness, leaving open whether their code differs from human code in the quality dimensions dominating lifecycle cost. We compare human-written and AI-generated code at scale: 787,562 function pairs across Python, Java, and C, each human function mined from open-source repositories …
- <a id="20260915-2609.12757"></a>**GraphAHA: Graph-Based Adaptive Search with Heterogeneous Actions for Test-Time Code Generation** — [2609.12757](https://arxiv.org/abs/2609.12757) | cross: cs.AI  
  Xitao Li, Haijun Wang, Gege Yuan, Qiyuan Wu et al.  
  Test-time scaling improves code generation by spending additional inference budget (e.g., calls or tokens) on direct sampling, feedback-conditioned repair, and reasoning-guided implementation. Search-based methods can allocate this budget adaptively, but two challenges remain.
- <a id="20260915-2609.13071"></a>**Involving before Evolving: A Vision for Trustworthy Enterprise Digital Twin Engineering** — [2609.13071](https://arxiv.org/abs/2609.13071) | cross: cs.AI, cs.HC  
  K\'erian Fiter, Adil Lagrou, Franck Dervault, Bentley Oakes  
  Enterprise Digital Twins (EDTs) promise data-driven decision support at organizational scale, but realizing them requires navigating siloed departments, tacit knowledge, and high-stakes decisions with long-horizon consequences. Existing approaches involve domain experts during model development but focus less on early organizational buy-in in EDTs.
- <a id="20260915-2609.11941"></a>**A Case-Bundle Operating Model for Coding Agents in OpenFOAM-Based CFD** — [2609.11941](https://arxiv.org/abs/2609.11941) | cross: cs.CE, cs.DC  
  Ke Xiao, Han Li, Teng Zhang, Yangchen Xu et al.  
  General-purpose coding agents can set up computational fluid dynamics (CFD) cases, execute solvers, and manage remote jobs. Reviewable and reusable work additionally depends on persistent engineering context and evidence.
- <a id="20260915-2609.11999"></a>**Is Bash All You Need? An Empirical Study of Tool Interfaces for Enterprise Digital Worker Agents** — [2609.11999](https://arxiv.org/abs/2609.11999) | cross: cs.CL  
  Hazel Mak, Susheel Suresh, Sahil Bhatnagar, Barry Wang et al.  
  In this study, we examine whether a general shell can outperform specialized tools on enterprise tasks. Shell-based agents have shown strong results in coding, but enterprise work also involves moving between applications and services, coordinating with coworkers, and performing professional analysis.
- <a id="20260915-2609.12008"></a>**Investigating Developer-Reported Software Security Testing Challenges** — [2609.12008](https://arxiv.org/abs/2609.12008) | cross: cs.CR  
  Md Erfan, Ahmed Ryan, Md Rayhanur Rahman  
  Software security testing (SST) is essential for identifying vulnerabilities and improving software security, but developers often face practical challenges when selecting tools, configuring test environments, interpreting scanner outputs, testing authentication workflows, and acting on reported vulnerabilities. This study empirically characterizes developer-reported SST challenges in Stack …
- <a id="20260915-2609.12012"></a>**Test-Driven Approaches to Software Engineering with Large Language Models: A Survey of Phases, Tasks, and Agent Skills** — [2609.12012](https://arxiv.org/abs/2609.12012)  
  Yunhao Liang, Chengguang Gan, Ruixuan Ying, Hanjun Wei et al.  
  Tests increasingly participate in the decisions made by large language models and software engineering agents. They specify intended behavior, guide program construction and repair, select candidates, constrain transformations, and provide execution evidence for software analysis.
- <a id="20260915-2609.12131"></a>**Missing Dimensions: Integrating Human and Social Systems into Digital Twin Engineering** — [2609.12131](https://arxiv.org/abs/2609.12131)  
  Francis Bordeleau, Mark van den Brand  
  Digital twins (DTs) have emerged as a key technology at the core of digital transformation, yet their engineering practice remains too narrowly focused on engineered and natural systems. This paper argues that four system dimensions must be explicitly recognized in DT engineering: Engineered, Natural/Biological, Human, and Social.
- <a id="20260915-2609.12236"></a>**Open Source Stewardship Communities: "We need you, but not your pull request"** — [2609.12236](https://arxiv.org/abs/2609.12236)  
  Gregorio Robles, Daniel M. German  
  Human-centric AI for software engineering means keeping humans responsible for work performed with AI. In Open Source Software (OSS), AI lowers the cost of implementing changes, but reviewing someone else's contribution remains comparatively expensive, so some projects now restrict who may contribute implementations while still welcoming other participation---not because the code is AI-generated, …
- <a id="20260915-2609.12309"></a>**PQLS: A High-Performance Python Library for Steady-State Simulation of Open Quantum Systems** — [2609.12309](https://arxiv.org/abs/2609.12309)  
  Evan Simanovskis, Raviraj Adve, Javane Rostampoor  
  PQLS (Parallel Quantum Liouvillian Solver) is a high-performance Python library for computing steady-state solutions of the Lindblad master equation. It provides a layered user-facing API with three levels of abstraction.
- <a id="20260915-2609.12457"></a>**Hieronym: Leveraging Hierarchical Multi-Source Information for Function Renaming in Stripped Binary** — [2609.12457](https://arxiv.org/abs/2609.12457)  
  Xiaoling Zhang, Jian Sun, Dawei Wang, Chongyu Wang et al.  
  Function renaming in stripped binaries can substantially assist reverse engineers by improving code readability, yet it is a challenging task. The difficulty stems from the need to accurately capture function semantics from low-level binary code across diverse instruction sets, architectures, and compiler optimizations, and to express these semantics in concise, human-readable names.
- <a id="20260915-2609.12576"></a>**A Retrieval-Augmented Automated Stakeholder for Requirements Elicitation Education: A Comparative Study** — [2609.12576](https://arxiv.org/abs/2609.12576)  
  Manal Binkhonain, Ohoud Mosa Alharbi  
  Developing the skills required for requirements engineering students to conduct effective requirements elicitation interviews is critical yet challenging, as it requires the development of soft skills in addition to technical knowledge. Role-playing is widely adopted in requirements engineering education to support the development of these skills but is often constrained by time and resource …
- <a id="20260915-2609.12770"></a>**Detecting HTTP Status Code Misuses in REST APIs via Static and Dynamic Analysis** — [2609.12770](https://arxiv.org/abs/2609.12770)  
  Alix Decrop, Andrea Arcuri, Mike Papadakis, Pierre-Yves Schobbens et al.  
  REST APIs are widely used on the web for client-server communications. As REST is based on HTTP, server responses contain status codes to indicate the outcome of requests (e.g., 200 OK for a success and 404 Not Found for an unavailable resource).
- <a id="20260915-2609.12921"></a>**Intelligent Semantic Matching (ISM) for Video Tutorial Search using Transformer Models** — [2609.12921](https://arxiv.org/abs/2609.12921)  
  Ahmad J. Tayeb, Sonia Haiduc  
  The rise in the number and diversity of available software development video tutorials has enhanced digital learning for developers but also introduced challenges in locating relevant content efficiently. Existing video search methods, including keyword-based approaches and tools like CodeTube and TechTube, rely primarily on retrieval algorithms such as BM25, which fail to capture the semantic …
- <a id="20260915-2609.13089"></a>**Beyond Establishing the Four-Day Workweek: Understanding Adaptation and Long-Term Survival in an Agile Software Organization** — [2609.13089](https://arxiv.org/abs/2609.13089)  
  Michael Neumann, Darja \v{S}mite  
  Context: Existing research on the four-day workweek (4DWW) has primarily examined its introduction and short-term effects, with limited understanding of its long-term survival or its interaction with agile software development. Objective: We study how a reduced-hour 4DWW is introduced, adapted, institutionalized, and sustained under changing organizational and external conditions in an agile …
- <a id="20260915-2609.11931"></a>**MaRDMO: FAIR Documentation of In-Silico Research** — [2609.11931](https://arxiv.org/abs/2609.11931) | cross: cs.SE  
  Marco Reidelbach, Marcus Weber  
  MaRDMO is a plugin for the Research Data Management Organiser (RDMO) that enables the structured, FAIR-compliant documentation and discovery of mathematical research data. By embedding mathematics-specific questionnaires into a widely used data management plan tool, MaRDMO lowers the barrier to contributing and querying the MaRDI Knowledge Graph for researchers across all disciplines.
- <a id="20260915-2609.12001"></a>**Scan the Skill, Govern the Action: Composing Registry Verdicts with Runtime Consequence Control** — [2609.12001](https://arxiv.org/abs/2609.12001) | cross: cs.SE  
  Rohit Taneja, Travis Weber  
  Agent skill registries screen what they publish. OpenClaw's security team reported that its scanners overlap on at most 10.4% of combined positives, and 81.9% of flagged skills are caught by one scanner alone.
- <a id="20260915-2609.12127"></a>**Local Edits, Global Ripples: Replay-Informed Policy Adaptation for Workflow Synthesis** — [2609.12127](https://arxiv.org/abs/2609.12127) | cross: cs.SE  
  Manqing Mao, Hong Wang, Samson Koelle, Jie Yuan et al.  
  Prompt-policy editing offers a practical way to improve agents that synthesize executable workflows without updating the underlying model. However, persistent prompt editing has two coupled properties.
- <a id="20260915-2609.12292"></a>**Mission Performance: Automatic and Adaptive Race Pace Progression for Autonomous Racing** — [2609.12292](https://arxiv.org/abs/2609.12292) | cross: cs.SE, cs.SY, eess.SY  
  Giovanni Lambertini, Matteo Pini, Nicola Musiu, Ayoub Raji et al.  
  In this paper, we describe the Mission Performance module implemented for a fully autonomous racing car to automatically manage the longitudinal, lateral, and combined performances, aiming to speedup the laptime progression while assuring safety. Motivated by the difficulty and risks of applying the real-time estimation of the grip to critical modules like the motion planner and controller, the …

<!-- END 20260915 -->

<!-- BEGIN 20260914 -->
## 20260914

时间窗口(UTC): 2026-09-14 00:00 → 2026-09-15 00:00 | 去重后共 **326** 篇 | 🎯 关键词命中(interests.md): ★ 9 篇 / 🧐 2 篇

> 补抓说明: 本期 arXiv API(`export.arxiv.org/api/query`)对本机出口 IP 返回 **429 Rate exceeded**，
> 改由 `scripts/backfill_rss.py` 从 9 个分类的 RSS 当日批次补抓(当日 announce 粒度, 非 24h 窗口),
> 并过滤 `replace` / `replace-cross`(旧论文新版本)。字段与 API 抓取完全兼容。

### 📌 重点关注(基于研究兴趣, agent 填写)

| 推荐 | 论文 | 理由 |
|------|------|------|
| ★★★★★ | **Supermartingale Certificates for Parametric MDPs** — [2609.12715](https://arxiv.org/abs/2609.12715) · [📄](#20260914-2609.12715) (cs.LO) | 命中「形式化方法与验证」条目(weight 3)的关键词 `formal verification`：把超鞅证书从非参数 MDP 推广到参数化 MDP(一般可测状态/动作空间)，并据此给出多项式算术 pMDP 的验证与近似合成算法；Žikelić 组在 pMDP 验证上的连续推进，与不变式/证书推断这条兴趣线直接对口 |
| ★★★★★ | **Specifying Paxos for System Builders: Pseudocode Made Executable** — [2609.12239](https://arxiv.org/abs/2609.12239) · [📄](#20260914-2609.12239) (cs.DC) | 命中「分布式计算与共识」条目(weight 3)的 **两条**关键词 `consensus` + `Paxos`：用 DistAlgo 把 Paxos for System Builders 的伪代码**逐行映射成可直接执行的规约**，同时覆盖共识协议与可执行规约两条兴趣线；Yanhong A. Liu(TLA+/DistAlgo 一系)署名 |
| ★★★★ | **Learning to adapt GR(1) specifications through degradation** — [2609.12231](https://arxiv.org/abs/2609.12231) · [📄](#20260914-2609.12231) (cs.SE) | **未字面命中关键词**, agent 依据「形式化方法与验证」画像判断: Uchitel / Alrajeh 组(Imperial)做 GR(1) assume-guarantee 规约在环境假设被违反时的自适应修复, 走 oracle-guided inductive synthesis, 并在尽量少降级系统保证的前提下维护可综合性——与不变式推断、规约演化高度相邻 |
| ★★★★ | **A Non-constant Lower Bound for Grammar-Based Compression with Greedy** — [2609.12106](https://arxiv.org/abs/2609.12106) · [📄](#20260914-2609.12106) (cs.DS) | 本期**权重最高**(★+🧐 合计 6): 同时命中「形式化方法与验证」(weight 3)与「计算机辅助证明与趣味组合」(weight 3)共有的关键词 `formally verified`——给出 Greedy 近似比 Ω(log n / log log n) 的下界, 终结该问题 20 年的开放状态, 且**结论在 Lean 4 中机器验证** |
| ★★★ | **Invisible Yet Dominant: Big Stalls of Kernel I/O Mechanisms in Cloud OLTP Databases** — [2609.12597](https://arxiv.org/abs/2609.12597) · [📄](#20260914-2609.12597) (cs.DB) | **未字面命中关键词**, agent 依据画像中的「数据库系统」主线判断: SOSP 2026 poster(SteelDB 姊妹篇), 用 eBPF 在内核里观测到 buffered I/O 的写回节流会让 OLTP 的 write()、乃至需要驱逐脏页的 read() 长时间停顿, 而 `iostat` 与所有标准计数器都看不见——云 OLTP 尾延迟的真实根因证据 |

### 🧐 视野扩展(agent 填写)

| 推荐 | 论文 | 理由 |
|------|------|------|
| 🧐🧐🧐 | **Behavior Quotient Learning for Low-Rank Adaptation of LLM Agents** — [2609.12896](https://arxiv.org/abs/2609.12896) · [📄](#20260914-2609.12896) (cs.LG) | 命中「LLM 与形式化/系统的交叉」条目(weight 3)的关键词 `LLM-based agent` 与 `agent memory`: 用"行为商"(behavior quotient)在固定 rank 预算下把多 LoRA 压成单 LoRA 并保持异构轨迹的决策等价性——agent 能力的参数化压缩问题, 与 agent memory 管理(如 MemLens 那条线)互为镜像 |
| 🧐🧐🧐 | **QEmbed: A Deep Learning Based Cardinality Estimator for Efficient Query Processing** — [2609.12535](https://arxiv.org/abs/2609.12535) · [📄](#20260914-2609.12535) (cs.DB) | 语义相关但**未字面命中** `learned database`(摘要未出现该词组), agent 依据「LLM 与形式化/系统的交叉」画像判断: MADE 自回归框架 + one-hot/embedding 混合编码学联合分布做选择率估计, 主打把极端最大 q-error 压下来——learned cardinality estimation 的老问题新攻法 |
| 🧐🧐 | **Shards on a Shoestring: Empirical Characterization of NEAR Protocol Nightshade Sharding on Commodity Hardware** — [2609.12091](https://arxiv.org/abs/2609.12091) · [📄](#20260914-2609.12091) (cs.DC) | 命中「分布式计算与共识」条目(weight 3)的关键词 `BFT`: 把官方"$700/小时 GCP"的百万 TPS 声明拉到 Chameleon 裸金属(48 核 + HDD)上复测, 给出分片数/硬件的可复现上界——这是对共识与分片系统做**可审计复现**的样本, 契合本仓库"可解释/可复现"的取向 |

### 分类清单

#### math.LO (5)

- <a id="20260914-2609.12402"></a>**Effective recurrence for computable measure-preserving transformations** — [2609.12402](https://arxiv.org/abs/2609.12402) | cross: math.DS  
  Joey Veltri  
  We prove several necessary and sufficient conditions under which a point satisfies the Poincar\'e Recurrence Theorem for all computable (ergodic) measure-preserving transformations and all sets of a particular complexity. The necessary conditions are obtained by constructing specific measure-preserving transformations which violate recurrence.
- <a id="20260914-2609.12581"></a>**Fra\"iss\'e's conjecture, partial impredicativity and well-ordering principles, part II** — [2609.12581](https://arxiv.org/abs/2609.12581)  
  Anton Freund, Katarzyna W. Kowalik, Davide Manca  
  We exhibit a well-ordering principle that is equivalent to a theory of partial impredicativity. The latter goes back to Towsner and relates to recent work of Suzuki and Yokoyama.
- <a id="20260914-2609.12740"></a>**Finite-tower bounds for Skolem functions** — [2609.12740](https://arxiv.org/abs/2609.12740)  
  Andreas Weiermann  
  We bound the eventual order types of Skolem functions below finite exponential towers. Writing $E_0(u)=u$, $E_{n+1}(u)=2^{E_n(u)}$, and $\omega_0=1$, $\omega_{k+1}=\omega^{\omega_k}$, the argument gives \[ |\Sk_{<E_n(x^m)}|<\omega_{r_n},\qquad r_n=2+\frac{n(n+3)}2\quad(n\ge1,\ m\ge2\text{ fixed}).
- <a id="20260914-2609.12916"></a>**Small masas of the Calkin algebra in the Cohen model** — [2609.12916](https://arxiv.org/abs/2609.12916) | cross: math.FA, math.GN, math.OA  
  Piotr Koszmider  
  We show that maximal abelian C*-subalgebras (masas) of the Calkin algebra (the algebra of all bounded operators on the separable Hilbert space modulo compact operators) may consistently have their densities strictly less than continuum and we describe many isomorphism types of such masas. Specifically, we prove that after adding any number of Cohen reals to a model of CH the algebra …
- <a id="20260914-2609.12031"></a>**The Borel complexity of conjugacy for Cantor minimal systems** — [2609.12031](https://arxiv.org/abs/2609.12031) | cross: math.LO  
  Xinan Dai, Wenhao Deng, Yingdong Shi, Tailin Wu et al.  
  We prove that conjugacy of minimal homeomorphisms of the Cantor space is Borel bireducible with isomorphism of countable graphs, answering the Cantor minimal case of a question of Foreman. We obtain the lower bound by encoding countably based profinite groups.

#### cs.AI (132)

- <a id="20260914-2609.12394"></a>**BlueLM-GUI Technical Report: A Real-Device-Centric Flywheel for Self-Improving Mobile GUI Agents** — [2609.12394](https://arxiv.org/abs/2609.12394) | 🎯★ consensus  
  Tong Ye, Kunyang Han, Guozhi Wang, Longqiang Luo et al.  
  Mobile GUI agents are shifting from multi-module frameworks to native models trained end-to-end, yet industrial deployment faces three persistent gaps. Sandbox training produces a distribution mismatch with production environments; expensive real-device failures remain underutilized; and fixed benchmarks saturate, losing the power to guide iteration.
- <a id="20260914-2609.12949"></a>**EduFair-Bench: Evaluating Pedagogical Fairness of LLM Tutors Across Student Demographics** — [2609.12949](https://arxiv.org/abs/2609.12949) | 🎯★ consensus  
  Jiaxu Zhao, Bahar Radmehr, Fares Fawzi, Tanya Nazaretsky et al.  
  Large language models (LLMs) are increasingly deployed as tutors, but it is unclear whether they support all students equally well. We introduce \textbf{EduFair-Bench}, a benchmark for auditing the pedagogical fairness of LLM tutors---whether tutoring quality varies systematically with student demographics.
- <a id="20260914-2609.12243"></a>**Chopthin-Consensus Power Sampling: A Diversity-Preserving Approach to LLM Decoding** — [2609.12243](https://arxiv.org/abs/2609.12243) | cross: cs.AI, stat.ML | 🎯★ consensus  
  Minoo Ahmadi, Seyedarmin Azizi, Erfan Baghaei Potraghloo, Mehdi Kamal et al.  
  Inference-time power sampling via Sequential Monte Carlo (SMC) can substantially improve large language model (LLM) reasoning without requiring post-training. However, many existing SMC approaches rely on equal-weight resampling, which can aggressively prune low-weight trajectories, discarding potentially correct reasoning paths and degrading the genealogical diversity of the search space.
- <a id="20260914-2609.11977"></a>**Occamy-1.0: Open Pareto-frontier 35B Intelligence for Co-work** — [2609.11977](https://arxiv.org/abs/2609.11977)  
  Wenhui Chen, Shiwen Cheng, Hao Dong, Chenda Duan et al.  
  Co-work agents execute complex workflows that combine information gathering, tool use, coding, and file manipulation across many model invocations. Because cost and latency accumulate over the full episode, their practical value depends not only on peak capability but also on how efficiently that capability is delivered.
- <a id="20260914-2609.11987"></a>**Harness or Model? Isolating the Harness Effect in Agentic Coding with a Contamination-Controlled Private Suite** — [2609.11987](https://arxiv.org/abs/2609.11987) | cross: cs.CL, cs.SE  
  Mohsen Arjmandi  
  An agentic coding system couples a language model to a harness: the tools, prompts and control flow that turn a chat model into an autonomous software engineer. Vendors ship harnesses tuned to their own models, and practitioners assume the vendor-native pairing solves more tasks.
- <a id="20260914-2609.12035"></a>**Reading the Whole Heart: Latent-Attention Masked Autoencoders for Multimodal Cardiac Representation Learning** — [2609.12035](https://arxiv.org/abs/2609.12035)  
  Andrea Agostini, Simon B\"ohi, Moritz Vandenhirtz, Samuel Ruiperez-Campillo et al.  
  Cardiovascular diagnosis rests on integrating complementary modalities, like ECG, echocardiography, chest radiographs, and clinical variables, each capturing distinct but correlated aspects of cardiac physiology. Yet most medical foundation models remain modality-specific, combining modalities only for finetuning or post-training.
- <a id="20260914-2609.12101"></a>**Competence-Gated Pooling of Language Models and Priors for Event Forecasting** — [2609.12101](https://arxiv.org/abs/2609.12101)  
  Aditi Tiwari, Aashrith Bandaru, Heng Ji  
  In hybrid forecasting, a language model is often one of several available signals. A system may already have a market, crowd, or statistical forecast and must decide whether the model adds useful information or should be ignored.
- <a id="20260914-2609.12105"></a>**Language Is an Insufficient Substrate for Quantitative Reasoning, and Consequential Domains Need Large Quantitative Models** — [2609.12105](https://arxiv.org/abs/2609.12105) | cross: cs.LG  
  Reuben Vandeventer, David Imrem, David J. Wild  
  The prevailing assumption in applied machine learning is that progress on consequential quantitative decisions such as pricing risk, allocating capital, triaging patients, or containing a network intrusion will follow from progress in large language models (LLMs). A language model is trained on a representation of the world that was produced by human description; description is a lossy encoding …
- <a id="20260914-2609.12115"></a>**DU-NO: A Parameter-Efficient Double U-Shaped Neural Operator for Phase-Resolving Wave Modeling** — [2609.12115](https://arxiv.org/abs/2609.12115)  
  Enrique Hernandez Noguera, Md Meftahul Ferdaus, Nathan Cooper, Elias Ioup et al.  
  Phase-resolving wave models such as FUNWAVE-TVD are the accuracy standard for nearshore dynamics, resolving the shoaling, refraction, and breaking of individual waves, but their cost rules them out for the ensembles, uncertainty quantification, and real-time warning that operational forecasting demands. Neural operators promise solver-level accuracy at a fraction of that cost, yet on …
- <a id="20260914-2609.12116"></a>**When Successful Knowledge Graph Edits Displace Correct Answers: Rank-Level Locality beyond Parameter Support** — [2609.12116](https://arxiv.org/abs/2609.12116)  
  Yi-Cheng Lai, Jerry Wang, Hsin-Ling Hsu, Li-Chu Chi et al.  
  Editing a knowledge graph embedding (KGE) model to promote a desired answer can displace correct answers from the returned list. Locality tests based only on facts that reuse the edited parameter can miss this ranking effect.
- <a id="20260914-2609.12139"></a>**Mined from Scientific Literature: Process Schemas for Atomic Layer Deposition and Etching in Materials Science** — [2609.12139](https://arxiv.org/abs/2609.12139) | cross: cond-mat.mtrl-sci  
  Sameer Sadruddin, Eleni Poupaki, Alex Watkins, Bora Karasulu et al.  
  Atomic layer deposition (ALD) and atomic layer etching (ALE) are reported heterogeneously across experimental and simulation literature in materials science, hindering comparison and machine-actionable reuse. We present four domain-expert-reviewed JSON Schemas for ALD and ALE experimental and simulation processes.
- <a id="20260914-2609.12162"></a>**Can LLMs in Draft-Verify-Revise Pipelines Resolve Deictic Ambiguity?** — [2609.12162](https://arxiv.org/abs/2609.12162) | cross: cs.CL  
  Obinna I. Ekekezie  
  Draft-verify-revise is a common LLM orchestration pattern for scaling inference-time compute. One LLM drafts, a second critiques the draft and provides feedback, and a third uses that feedback to revise the draft into the final output.
- <a id="20260914-2609.12165"></a>**GLARE: Generative Learning via Adversarial Reward Estimation For Social Dynamics Forecasting** — [2609.12165](https://arxiv.org/abs/2609.12165)  
  Tenghao Huang, Zhaoxuan Tan, Muhao Chen, Jonathan May et al.  
  Meeting continuation requires tracking the agenda, speaker roles, participant intentions, and disagreement across long multi-party discussions. We introduce the Meeting Dynamic Forecasting Benchmark (MDFB), constructed from 2,207 real-world meetings and 24,794 future-facing queries.
- <a id="20260914-2609.12171"></a>**WinSyn: An Automated Pipeline for Realistic Enterprise Question-Answering Evaluation** — [2609.12171](https://arxiv.org/abs/2609.12171)  
  Amey Varhade, Ananya Sutradhar, Ravishankar Krishnaswamy, Navin Goyal  
  Enterprise settings provide a challenging environment for question-answering agents, which often rely on Retrieval-Augmented Generation, Deep Research (DR), and related techniques. Much of this challenge comes from the complexity of enterprise data: information is often spread across evolving and potentially conflict- ing emails, chat messages, documents, and other artifacts.
- <a id="20260914-2609.12247"></a>**Soft Symbol Grounding for Prototypical Concepts** — [2609.12247](https://arxiv.org/abs/2609.12247)  
  Marcos Galv\'an-L\'opez, Nijesh Upreti, Hiram Calvo, Carlos Aguilar-Ib\'a\~nez et al.  
  Neuro-symbolic models are usually trained with supervision only on final labels, leaving the intermediate concepts unobserved. Since many concept assignments are consistent with a given label, training can predict labels correctly while recovering the wrong concepts, a failure known as a reasoning shortcut.
- <a id="20260914-2609.12265"></a>**GTA: Graph Theory Agent and Benchmark for Algorithmic Graph Reasoning with LLMs** — [2609.12265](https://arxiv.org/abs/2609.12265)  
  Zixiang Xu, Yanbo Wang, Chenxi Wang, Lang Gao et al.  
  Large Language Models (LLMs) are increasingly asked to reason over structured data such as graphs, yet how reliably they can carry out multi-step graph algorithms in language remains unclear. Existing evaluations tend to use simple tasks on small graphs, to score code generation rather than reasoning over the graph itself, or to fix a single input format.
- <a id="20260914-2609.12267"></a>**Learning Symbolic Constraint Representations from Examples: A Neuro-Symbolic Approach** — [2609.12267](https://arxiv.org/abs/2609.12267)  
  Nassim Belmecheri, Arnaud Gotlieb, Nadjib Lazaar, Helge Spieker  
  Learning user-defined concepts as constraint networks has been extensively studied in the constraint acquisition (CA) literature. However, existing approaches typically rely on intensive interactions with a human oracle, making the learning process costly in terms of time and number of queries.
- <a id="20260914-2609.12286"></a>**T-GADE: Thermodynamical Generative-AI-Driven Evolution of LLM Artifacts** — [2609.12286](https://arxiv.org/abs/2609.12286) | cross: cs.NE  
  Kyoko Ogawa, Naoki Mori  
  Integrating evolutionary computation and large language models (LLMs) requires control of population diversity as well as generative capability. Among LLM outputs, those with explicit structure, such as a description paired with code, are structured artifacts; we use artifact for short.
- <a id="20260914-2609.12287"></a>**Robust Prototypical Networks for Few-Shot Sensor Fault Diagnosis** — [2609.12287](https://arxiv.org/abs/2609.12287) | cross: cs.LG  
  Mohammed Ayalew Belay, Amirshayan Haghipour, Pierluigi Salvo Rossi  
  Industrial fault diagnosis often operates with only a handful of labeled fault examples, making few-shot learning attractive for sensor monitoring. Standard prototypical networks are simple and effective; however, their class prototypes may become unstable in the very-low-shot regime because each decision relies on a small support set.
- <a id="20260914-2609.12304"></a>**Hybrid Physics-AI Framework of Body Center of Mass Dynamics from Wrist-Worn Sensors** — [2609.12304](https://arxiv.org/abs/2609.12304) | cross: eess.SP  
  Shuhao Que, Valentina Breschi, Ying Wang  
  Wrist-worn IMU has been widely used for daily-life health monitoring. Yet, it does not fully represent whole-body dynamics, for which the body center of mass (COM) is considered the physiological reference standard.
- <a id="20260914-2609.12313"></a>**Do Influence-Derived Data Perturbations Enable Machine Unlearning? A Controlled Study of Three Plausible Roles** — [2609.12313](https://arxiv.org/abs/2609.12313)  
  Chenkai Wu, Chrispine Kambimbi, Qinyang Zeng, Jun Yan  
  We evaluate Deep Perturbation Learning (DPL), which perturbs training images and labels along influence-derived directions, in three roles in which prior work has positioned it for machine unlearning: a direct deletion signal (the strongest claim), a utility-preserving regularizer, and a warm start for adversarial unlearning. Evidence for the weaker roles has been used to support the stronger …
- <a id="20260914-2609.12320"></a>**AIM: A Privacy-Aware Interoperable Memory Framework for Multi-Agent Multi-User LLM Systems** — [2609.12320](https://arxiv.org/abs/2609.12320) | cross: cs.LG  
  Zachary Johnson, Nigel Boachie Kumankumah, Somya Chatterjee, Tejas Sathyamurthi et al.  
  Traditional large language models (LLMs) are scoped to individual user sessions, limiting their knowledge to a single conversation and preventing them from learning user preferences that evolve over time. Existing agentic memory systems address this limitation but generally operate at the individual-user level, restricting the public knowledge that could be shared across users to improve …
- <a id="20260914-2609.12322"></a>**Affective Agent: On-Device Personalized Intervention Reasoning for Wearable Systems** — [2609.12322](https://arxiv.org/abs/2609.12322) | cross: cs.LG  
  Reina Mun, Zishen Wan, Vijay Janapa Reddi  
  Affective computing has advanced wearable state inference, but on-device reasoning about whether, when, and how to intervene remains challenging. We present Affective Agent, a three-layer reference architecture for personalized intervention reasoning under uncertainty on wearable-class hardware.
- <a id="20260914-2609.12327"></a>**LoRA-RC: Reservoir Computing with Low-Rank Adaptation** — [2609.12327](https://arxiv.org/abs/2609.12327) | cross: cs.LG, cs.SY, eess.SY, math.DS  
  Wenbin Wan  
  Reservoir computing (RC) trains only a linear readout over a fixed recurrent layer, making it fast and data-efficient for online prediction. However, a static reservoir degrades under system drift, readout-only adaptation is then insufficient, and unconstrained reservoir adaptation can destroy the echo-state and incremental stability properties that make RC reliable.
- <a id="20260914-2609.12373"></a>**Toward Robust Personalized Alignment for LLMs: Mitigating Persona Drift in Multi-Turn Dialogue** — [2609.12373](https://arxiv.org/abs/2609.12373)  
  Youyuan Zhang, Siyuan Li, Fangming Liu, Jing Li  
  Persona drift remains a central challenge for personalized language models, as user profiles evolve over long interactions rather than remain permanently fixed. Models must therefore revise persistent persona states when preferences genuinely change, while avoiding updates driven by transient, ambiguous, or unresolved observations.
- <a id="20260914-2609.12395"></a>**Is Gaussian Splatting Becoming Neural Again? A Taxonomy and Controlled Study of Learned Parameterization** — [2609.12395](https://arxiv.org/abs/2609.12395)  
  YuanHang Wang, Xin Cao, Yi Zhang  
  Three-dimensional Gaussian Splatting (3DGS) combines explicit primitives with efficient rasterization, yet recent systems increasingly use neural networks to generate or share Gaussian parameters. We characterize this trend along five axes: attribute decoding, spatial sharing, view-conditioned decoding, topology generation, and amortized inference.
- <a id="20260914-2609.12398"></a>**Niching Agents in The Core** — [2609.12398](https://arxiv.org/abs/2609.12398)  
  Gary B. Parker, Jim O'Connor, John Asaro  
  The Core is a unique competitive co-evolution algorithm that allows agents to evolve autonomous control without utilizing a traditional fitness function. The agents evolve via local interactions through tournament selection, crossover, and mutation, producing offspring by evolving better controllers.
- <a id="20260914-2609.12399"></a>**OneLA: Scaling Linear-Attention Decoding to Large Beams in Generative Recommendation** — [2609.12399](https://arxiv.org/abs/2609.12399) | cross: cs.DC, cs.IR  
  Xiangrui Yang, Cheng Peng, Yunfeng Zhao, Liang Zeng et al.  
  Generative recommendation (GR) relies on large-beam decoding to generate hundreds of candidate items, creating a new scaling challenge for recurrent linear attention. Existing linear attention serving systems either materialize a full recurrent state for every beam or repeatedly replay shared history, incurring substantial memory and traffic overhead.
- <a id="20260914-2609.12400"></a>**Decentralized Evolution of Hexapod Gaits with Independent Leg Controllers** — [2609.12400](https://arxiv.org/abs/2609.12400) | cross: cs.RO  
  Gary B. Parker, John Asaro, Jim O'Connor  
  This paper presents a novel approach to hexapod locomotion by evolving each leg's gait independently through a decentralized evolutionary algorithm. Using the Webots simulator and the Mantis hexapod robot, we optimize individual leg controllers without centralized coordination, allowing emergent behaviors to drive the development of efficient, coordinated locomotion.
- <a id="20260914-2609.12403"></a>**Beyond ID Embeddings: Process-Grounded Language Modeling for Cognitive Diagnosis** — [2609.12403](https://arxiv.org/abs/2609.12403) | cross: cs.CL  
  Minghang Liu, Yuanzhuo Wang, Qiang Qiu, Huawei Shen et al.  
  Cognitive Diagnosis Models (CDMs) play a pivotal role in personalized online learning. Traditional CDMs rely on discrete, ID-based embeddings to represent students, exercises, and concepts.
- <a id="20260914-2609.12404"></a>**VRL-Bench: Benchmarking agents on computer control tasks under finite trial budgets** — [2609.12404](https://arxiv.org/abs/2609.12404)  
  Yu Bai, Yukai Miao, Dawei Wang, Li Chen et al.  
  Learning from trial and error is a promising way to improve language agents on complex tasks such as computer control. Reflexion introduced verbal reinforcement learning, which turns failed trials into text that guides later attempts without updating model parameters.
- <a id="20260914-2609.12413"></a>**SoK: Rethinking Jailbreaking in the Era of Agentic AI: Attacks, Defenses, and Practical Consideration** — [2609.12413](https://arxiv.org/abs/2609.12413)  
  Md Jueal Mia, Yanzhao Wu, Selcuk Uluagac, M. Hadi Amini  
  Large language models (LLMs) are rapidly evolving from conversational assistants into agentic AI systems that reason, plan, invoke tools, maintain persistent memory, communicate with other agents, and execute multi-step tasks. At the same time, modern models exhibit substantially stronger native safety alignment than earlier generations on which many jailbreak attacks and defenses were originally …
- <a id="20260914-2609.12422"></a>**Hierarchical Belief Modeling for Zero-Shot Opponent Adaptation in Partially Observable Multi-Agent Navigation** — [2609.12422](https://arxiv.org/abs/2609.12422) | cross: cs.MA  
  Kowei Shih, Lu Cheng, Zeyu Wang, Yeyun Xu et al.  
  Lux AI Season 3 requires agents to act under partial observability, randomized episode level dynamics, and a best of five match structure that rewards both tactical execution and fast adaptation. We present HORIZON, a hierarchical agent that combines symmetry aware spatial perception, dual memory belief tracking, relic centric graph attention, information gain driven exploration, and an opponent …
- <a id="20260914-2609.12436"></a>**LifeFuse-Mem: Lifecycle-Aware State Fusion Against Temporary Overwriting for Long-Term Memory** — [2609.12436](https://arxiv.org/abs/2609.12436)  
  Hanyu Zhao, Yuqian Feng, Zhenyu Song, Yuanchao Cheng et al.  
  Long-running LLM agents require memory mechanisms that maintain coherent internal states across interactions. We study a lifecycle-labeled memory setting in which write episodes provide lifecycle metadata during training, and phase-aware readout is used during evaluation.
- <a id="20260914-2609.12446"></a>**Do LLMs Trust the Accuser or the Accusation? Measuring Belief Shifts in Werewolf** — [2609.12446](https://arxiv.org/abs/2609.12446) | cross: cs.CL  
  Yu-Yu Yang, Ti-Rong Wu, Hung Guei, Hsing-Yu Chen et al.  
  Social-deduction games such as Werewolf are increasingly used to evaluate LLM agents, but existing evaluations often rely on final game outcomes. We propose a belief-shift evaluation benchmark in Werewolf for analyzing communication skills through belief updating.
- <a id="20260914-2609.12459"></a>**EvoRS: On-Policy Self-Evolution of Reward Systems for Open-Ended Reinforcement Learning** — [2609.12459](https://arxiv.org/abs/2609.12459)  
  Weiyuan Li, Aili Chen, Xintao Wang, Yikai Zhang et al.  
  Open-ended reinforcement learning often relies on rubric-based rewards for tasks without directly verifiable answers. Yet the policy and reward system form a dynamic feedback loop: as the policy optimizes the current reward, an initially useful reward system may become unreliable due to reward hacking or reduced response discriminability.
- <a id="20260914-2609.12464"></a>**Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration** — [2609.12464](https://arxiv.org/abs/2609.12464)  
  Nilesh Jaiswal, Aniket Agrawal, Arjit Shukla, Divya Malhotra et al.  
  As enterprises modernize legacy monolithic systems to microservices, Large Language Models (LLMs) are heavily utilized for automated code translation. However, traditional vector-based Retrieval-Augmented Generation (Standard RAG) struggles to capture topological relationships.
- <a id="20260914-2609.12472"></a>**TripPattern: A Pattern-based Text Watermarking Method for Large Language Models** — [2609.12472](https://arxiv.org/abs/2609.12472)  
  Sangjun Moon, Dasom Choi, Jingun Kwon, Hidetaka Kamigaito et al.  
  Text watermarking techniques have gained significant attention for identifying machine-generated text and mitigating risks from large language models (LLMs). Existing methods typically divide an LLM's vocabulary into green and red tokens, but encouraging generation toward green tokens can reduce text quality and naturalness.
- <a id="20260914-2609.12482"></a>**When Does AI Augment Work? A Workflow-Level Framework for Human-Agent Collaboration** — [2609.12482](https://arxiv.org/abs/2609.12482) | cross: cs.CY, cs.HC  
  AI Collaboration, Jiaying Wu, Caleb Ziems, Raymond Chan et al.  
  We aim to characterise the value of artificial intelligence in the workplace. Current studies largely measure this value in terms of the current automation capabilities and public adoption of AI.
- <a id="20260914-2609.12489"></a>**Confidence-Gated Transductive Test Generation for Code Reranking** — [2609.12489](https://arxiv.org/abs/2609.12489) | cross: cs.CL, cs.SE  
  Sungjae Lee, Youngsik Yoon, Seockbean Song, Siwei Wang et al.  
  Test case synthesis is crucial for evaluating and ranking programs generated by large language models (LLMs). However, constructing high-quality test cases remains challenging because reliable expected outputs are often difficult to obtain.
- <a id="20260914-2609.12495"></a>**Information Specialization and Constrained Synthesis in Multi-Agent LLM Forecasting: A Prospective Live-Study of the 2026 FIFA World Cup** — [2609.12495](https://arxiv.org/abs/2609.12495) | cross: cs.CL  
  Julian Varghese, Lucas Bickmann, Sarah Sandmann  
  Large language models are being organized into multi-agent systems with specialized roles, but whether such specialization produces distinct forecasts and whether subsequent synthesis improves utility remains unclear. In this study, we carried out a live, prospective evaluation over the final 56 matches of the information-dense 2026 FIFA World Cup, keeping a frontier foundation model constant …
- <a id="20260914-2609.12578"></a>**From Collaboration to Capability: Internalizing Routed LLM Experts into Compact Reasoners** — [2609.12578](https://arxiv.org/abs/2609.12578)  
  Frank Nie, Shuyao Wang, Ethan B. Liu  
  A compact controller can coordinate stronger experts by selecting whom to consult, formulating requests, and integrating their responses. We study whether learning from both the controller's decisions and the experts' reasoning and code improves its generation after expert removal.
- <a id="20260914-2609.12586"></a>**Reproducing and Evaluating the Generalizability of Subliminal Learning in Open-Weight Models** — [2609.12586](https://arxiv.org/abs/2609.12586)  
  Daan van der Weijden, Nathan Brack, Selene Baez Santamaria  
  In this reproduction paper we investigate subliminal learning, a consequence of distillation where teacher models transmit behavioral preference traits through semantically unrelated data. The original paper explores two types of traits (animal preferences and misalignment), three data modalities (number sequences, code, and chain of thought), and several model families.
- <a id="20260914-2609.12606"></a>**Beyond Generation and Accuracy: Diagnosing and Enhancing Visual Chain-of-Thought for Geometry Problem Solving** — [2609.12606](https://arxiv.org/abs/2609.12606)  
  Zhitong Dong, Jicai Pan, Yingguo Gao, Jingting Ding et al.  
  While multimodal reasoning has advanced rapidly, solving complex geometry problems critically hinges on active visual assistance, such as constructing auxiliary lines, spurring the rise of Visual Chain-of-Thought (VCoT). However, existing evaluations typically assess visual generation quality and final answer accuracy in isolation, failing to examine whether intermediate visual aids are …
- <a id="20260914-2609.12623"></a>**SteerDuplex: Steerable Duplex Speech Dialogue Models** — [2609.12623](https://arxiv.org/abs/2609.12623) | cross: cs.CL  
  Utkarsh Tyagi, Ramaneswaran Selvakumar, Advait Gosai, Sonal Kumar et al.  
  Full-duplex spoken dialogue models support low-latency turn taking, interruption handling, and backchanneling, yet a key capability remains underexplored: steerability, the ability to reliably shift conversational behavior along attributes such as tone, persona, speaking rate, and voice style in response to user instructions. We introduce a taxonomy of text- and audio-based steerability that …
- <a id="20260914-2609.12684"></a>**Generative AI Use Cases In Real Estate Marketing: Adoption and Constraints in Germany** — [2609.12684](https://arxiv.org/abs/2609.12684) | cross: cs.HC  
  Victor Kolominsky-Rabas, Leopold M\"uller, Felicia Perpina, Niklas K\"uhl  
  Generative artificial intelligence (GenAI) is changing how work is organized and performed. Real estate marketing is a prime example of this, yet evidence of GenAI in real estate agents' day-to-day practice remains scarce.
- <a id="20260914-2609.12686"></a>**Residual Vector-based Reconstruction as Long-Context Recall Regardless of Context Window Size** — [2609.12686](https://arxiv.org/abs/2609.12686) | cross: cs.CL  
  MyungHoon Ryu, XinYu Piao, Jong-Kook Kim  
  Large language models (LLMs) process long contexts, including long documents and lengthy conversations, but face token-level memory usage that increases proportionally to input length. Although model optimization and lossy prompt compression are widely used, these methods still fail to solve the long-context recall problem beyond pretrained and size-constrained context windows.
- <a id="20260914-2609.12694"></a>**I Am AdMan: A Pipeline for Automatic Generation of Personalized Advertising Imagery** — [2609.12694](https://arxiv.org/abs/2609.12694) | cross: cs.HC  
  Victor Kolominsky-Rabas, Leopold M\"uller, Claudius Budcke, Niklas K\"uhl  
  Personalized marketing can increase customer engagement, satisfaction, and conversion. While existing personalization approaches have become effective at matching the right product to the right customer, the visual representation of advertisements remains generic and only weakly tailored to the individual.
- <a id="20260914-2609.12697"></a>**Enabling and Understanding Personalization in AI-Generated Advertising Imagery** — [2609.12697](https://arxiv.org/abs/2609.12697) | cross: cs.HC  
  Victor Kolominsky-Rabas, Leopold M\"uller, Claudius Budcke, Claas Christian Germelmann et al.  
  Personalized marketing traditionally matches static products to customers, while dynamic creative optimization focuses mainly on AI-driven text personalization or basic product image modifications. We address this gap by developing and implementing an AI-based framework that generates personalized advertising imagery directly from customer data.
- <a id="20260914-2609.12704"></a>**Implicit Personality Representations in Humans and LLMs** — [2609.12704](https://arxiv.org/abs/2609.12704)  
  Yilin Geng, Omri Abend, Eduard Hovy, Lea Frermann  
  A century of psychology has found that the trait words people use to describe one another vary, but the relational structure among those traits, which ones go together and which oppose, is strikingly consistent across raters and cultures. We test whether the LLM (Qwen 2.5-7B-Instruct) reproduces this structure in its internal trait representations.
- <a id="20260914-2609.12718"></a>**When Rubrics Fail: Hallucinations Reveal Blind Spots in Medical AI Evaluation** — [2609.12718](https://arxiv.org/abs/2609.12718)  
  Griffin Farrow, Lily Sijia Li, Jack Johnson, Tingyan Wang et al.  
  Hallucinations can undermine clinician trust in LLMs, making it important that evaluation methods capture clinically relevant errors. Rubric-based evaluation has become the leading approach for assessing LLMs in medicine, but it is unclear whether rubric scores reflect such errors.
- <a id="20260914-2609.12742"></a>**Skill Issue: Lessons from Optimizing Repository SKILLs for Coding Agents** — [2609.12742](https://arxiv.org/abs/2609.12742)  
  Mykhailo Kozyrev, Andrei Kozyrev, Anton Podkopaev  
  Coding agents increasingly read repository knowledge from SKILLs --- plain \texttt{.md} files versioned alongside the code. Recent work synthesizes these files automatically, by optimizing the document against a benchmark.
- <a id="20260914-2609.12746"></a>**What Drives Recovery in Agentic Text-to-Cypher? LAST-CQ: An LLM Agent Self-Refinement Framework** — [2609.12746](https://arxiv.org/abs/2609.12746) | cross: cs.CL, cs.LG, cs.MA, cs.SE  
  Ioannis Prokopiou, Athanasios Aidinis, Panagiotis-Christos Kyrmpatsos, Pantelis Vikatos  
  Agentic pipelines for structured-query generation are rapidly expanding, but it is unclear which part of the loop produces the gain. We use LAST-CQ -- a five-agent, training-free, execution-grounded Text-to-Cypher framework -- as an instrumented testbed, running three counterfactuals over 2,471 live-database queries and six backbones spanning three vendor scale tiers.
- <a id="20260914-2609.12747"></a>**Assisted Spatial Cognition Through Vision-Language Models** — [2609.12747](https://arxiv.org/abs/2609.12747)  
  H. Riaz, J. B. Fernandez, I. Mills, D. Hickey et al.  
  Multimodal AI, powered by Large Language Models (LLMs) and Vision-Language Models (VLMs), is transforming assistive technologies by enabling simultaneous processing of visual and textual data. This advancement holds significant promise for over 43 million visually impaired and neuro-divergent individuals worldwide who face persistent challenges in navigating indoor and outdoor environments due to …
- <a id="20260914-2609.12749"></a>**SCQ: Stabilizing Conservative Q-Learning with Sigmoid-Bounded Entropy** — [2609.12749](https://arxiv.org/abs/2609.12749)  
  Xiefeng Wu, Shu Zhang, Zhaojie Chu, Mingyu Hu  
  Offline-to-online reinforcement learning reduces interaction cost for real-world robot learning but suffers from persistent value estimation instability. Existing methods address this through pessimistic regularization, lower-bound calibration, and architectural normalization, but an overlooked source of instability lies in the entropy formulation: the standard log-entropy term can become …
- <a id="20260914-2609.12769"></a>**Unified Agentic Video Editing Across Levels of Complexity and Creativity** — [2609.12769](https://arxiv.org/abs/2609.12769) | cross: cs.HC, cs.MM  
  Surabhi S. Nath, Kim Ferres, Milan Petrovi\'c, Lion Schulz  
  Editing is a core component of video production, requiring creative planning and decisions under multiple constraints. Here, we report methods for agentic tooling for automated video editing across three tasks varying in editorial goal, complexity and creativity, namely scene previews, video summaries and cinematic trailers.
- <a id="20260914-2609.12771"></a>**MPT: Missing Prototype Tracking via Barycentric Reconstruction in Vehicular Federated Learning** — [2609.12771](https://arxiv.org/abs/2609.12771) | cross: cs.CV  
  Hanju Jang (Yonsei University), Gyeongmin Han (Yonsei University), Sungmin Lee (Yonsei University), Kichang Lee (Yonsei University) et al.  
  Cross-vehicle federated learning enables vehicles to collaboratively improve perception models while keeping locally collected driving data private. However, vehicle participation is transient, and a vehicle may depart before training converges while permanently taking its local data.
- <a id="20260914-2609.12801"></a>**Interpreting the predictions of neural network classification based on a Taylor Coefficient Analysis (TCA)** — [2609.12801](https://arxiv.org/abs/2609.12801) | cross: physics.data-an  
  Markus Klute, Artur Monsch, Lars Sowa, Roger Wolf  
  We introduce a rigid and comprehensive taxonomy and paradigm for characterizing the influence of the input feature space $X$ on the predictions $\hat{y}$ of a neural network (NN) used for event classification, based on a Taylor expansion of $\hat{y}$ in $X$. The complete process of introspection we refer to as Taylor Coefficient Analysis (TCA).
- <a id="20260914-2609.12808"></a>**K-Bench: A Benchmark for LLM Unlearning in Agentic Deployments** — [2609.12808](https://arxiv.org/abs/2609.12808)  
  Guangsheng Yu, Yanna Jiang, Qin Wang, Baihe Ma et al.  
  Unlearning benchmarks such as TOFU and MUSE certify forgetting by reading the model's final answer, where a model that refuses to answer already counts as having forgotten. We show that this model-level certificate does not transfer once the model is deployed as an agent.
- <a id="20260914-2609.12822"></a>**Scaling Clinical Judgment to Evaluate Medical AI** — [2609.12822](https://arxiv.org/abs/2609.12822)  
  Thomas A. Buckley, Zahir Kanjee, Peter G. Brodeur, Byron Crowe et al.  
  Blinded physician evaluation has been considered by many to be the gold standard for assessing clinical reasoning in large language models (LLMs). This is difficult to scale; thus, prior studies typically rely on small physician panels, often from a single institution or specialty, which both limits the scientific questions investigated and makes it unclear whether findings would be reproduced …
- <a id="20260914-2609.12851"></a>**MedRoundsQA: A Persona and Difficulty Aware Evaluation for Multi-Turn Medical Consultations** — [2609.12851](https://arxiv.org/abs/2609.12851)  
  Youssef Mohamed, Ahmed Heakl, Qinrong Cui, Junhong Liang et al.  
  Medical benchmarks are dominated by single-turn, multiple-choice clinical cases that poorly reflect real consultations. Practically, clinicians elicit evidence interactively and patient communication varies widely.
- <a id="20260914-2609.12897"></a>**Tracing and Coordinating Cross-Layer Influence for Multimodal Model Merging** — [2609.12897](https://arxiv.org/abs/2609.12897)  
  Pengyang Zhou, Xiaobin Tu, Zhengxi Liu, Rongkun Xue et al.  
  Multimodal model merging aims to consolidate task experts into a single model that retains their complementary capabilities. Most unimodal model merging methods combine expert updates within individual layers, and multimodal approaches largely follow this design.
- <a id="20260914-2609.13009"></a>**How Good Are Frontier Models at Physics? Expert Re-Grading Reveals Broken Evaluations and Near-Saturation of Leading Benchmarks** — [2609.13009](https://arxiv.org/abs/2609.13009)  
  Ali Ansari, Haoran Sun, Andy Zeyi Liu, Mark Jabbour et al.  
  Low reported scores on leading physics benchmarks, including those featured in the Artificial Analysis Intelligence Index (2026), suggest that frontier language models still struggle with advanced physics, a demanding test of their scientific reasoning and quantitative problem-solving abilities. Yet this impression does not always align with domain experts' experiences using these models in their …
- <a id="20260914-2609.13047"></a>**Diffusion Models and Concept Formation** — [2609.13047](https://arxiv.org/abs/2609.13047) | cross: cs.LG  
  Zekun Wang, Karthik Singaravadivelan, Christopher J. MacLellan  
  Humans organize knowledge into a taxonomy of concepts with nested levels of abstraction and a \emph{basic level} at which people recognize and name objects with the least cognitive effort. Cobweb is a classic cognitive account of this ability, an incremental learner that builds a probabilistic concept hierarchy by maximizing category utility.
- <a id="20260914-2609.13062"></a>**Anchoring Clinical Events in Time: UID-Preserving Multimodal Reconstruction and Source-Grounded Adjudication** — [2609.13062](https://arxiv.org/abs/2609.13062)  
  Sayantan Kumar, Nicolas Grimaldi, Jack Cummins, Jeremy C. Weiss  
  Clinical timelines support treatment-window analysis and leakage-free modeling, but discharge summaries often obscure chronology and structured EHR tables describe only part of the patient course. We present a UID-preserving framework that links each narrative event occurrence to its source span and retains that identity through text-only estimation, structured-evidence retrieval, timestamped …
- <a id="20260914-2609.13073"></a>**Autonomous Research for Open-Ended Problems: A Case Study on Telecom Ticket Retrieval** — [2609.13073](https://arxiv.org/abs/2609.13073) | cross: cs.IR, cs.LG  
  Junghyun Min, Huseyin Uzunalioglu, Mohamed Trabelsi  
  Recent breakthroughs in LLM-based systems and their abilities in problem solving and coding have allowed progress in the AI for Science paradigm, potentially replacing human roles in machine learning (ML) research. However, while several frameworks of fully autonomous end-to-end ML research have been proposed, successful implementations of them are often limited to problems with narrow search …
- <a id="20260914-2609.13082"></a>**Embodied-BenchForge: A Closed-Loop Agentic Workflow for Embodied Benchmark Construction** — [2609.13082](https://arxiv.org/abs/2609.13082)  
  Baoyang Jiang, Fengchun Zhang, Leyuan Wang, Haotian Li et al.  
  Agentic systems offer a promising way to automate embodied benchmark construction, but existing approaches typically cover isolated stages or remain specialized to predefined environments and task families. More importantly, multi-step construction produces dependent intermediate artifacts that are often passed downstream without artifact-specific verification, allowing local defects to propagate …
- <a id="20260914-2609.13118"></a>**CMA-OT: Hierarchical Expert Supervision for Dance-to-Music Generation** — [2609.13118](https://arxiv.org/abs/2609.13118) | cross: cs.SD  
  Jinting Wang, Chenxing Li, Dong Yu, Li Liu  
  Dance-to-music (D2M) generation aims to synthesize music that is rhythmically and stylistically aligned with dance videos. A key challenge arises from the semantic mismatch between sparse dance cues, such as rhythm and style, and the dense information required for music composition, including structure, instrumentation, and expressive dynamics.
- <a id="20260914-2609.13125"></a>**A Hybrid LSTM-XGBoost Framework for Multi-Horizon Stock Return Prediction Across Diversified Equity Portfolios** — [2609.13125](https://arxiv.org/abs/2609.13125)  
  Seif ElDein Mostafa, Yahia Ahmed, Farah Datwish, Marwa Solayman  
  Accurate prediction of equity returns remains a major challenge in computational finance due to the non-stationary, nonlinear, and low signal-to-noise ratio nature of financial time series. This paper proposes a hybrid two-stage architecture that combines a long short-term memory (LSTM) network with an XGBoost gradient-boosted regressor for multi-horizon stock return prediction across a …
- <a id="20260914-2609.13134"></a>**Rethinking Heterogeneous System Disaggregation for Subquadratic Attention** — [2609.13134](https://arxiv.org/abs/2609.13134)  
  Arya Tschand, Yaosheng Fu, Vikram Sharma Mailthody, Nicolai Oswald et al.  
  Frontier language models are more aggressively using subquadratic attention to reduce the memory footprint and compute requirements during inference while still delivering frontier accuracy. While existing systems make dense attention-centric disaggregated serving decisions, we show that disaggregating inference around the unique arithmetic intensity and memory footprint of subquadratic attention …
- <a id="20260914-2602.09490"></a>**Robust Trust** — [2602.09490](https://arxiv.org/abs/2602.09490) | cross: cs.AI, cs.GT  
  Piotr Dworczak, Alex Smolin  
  An agent chooses an action based on her private information and a recommendation from an informed but potentially misaligned adviser. With a known probability, the adviser truthfully reports his signal; with the remaining probability, he can send any message.
- <a id="20260914-2609.11258"></a>**SoulAuth: An Actor-native Identity Architecture and Rust Reference Implementation for Humans and Long-lived AI Actors** — [2609.11258](https://arxiv.org/abs/2609.11258) | cross: cs.AI, cs.CR  
  Kun Yuan, Harold Wang, Echo Li, Egusi Gui et al.  
  As AI systems move from transient model invocations toward long-lived actors that persist across credentials, clients, sessions, and runtime instances, identity infrastructure must answer a basic question: where should the canonical continuity boundary be placed? This paper introduces Actor-native Identity and presents SoulAuth, an open-source Rust reference implementation for Humans and …
- <a id="20260914-2609.11983"></a>**Who Pays for Open Review? Visible Author Reputation and Its Effect on Ratings** — [2609.11983](https://arxiv.org/abs/2609.11983) | cross: cs.AI  
  Qinghua Zhao, Xinyu Chen, Yanhui Yang, Tengfeng Sun et al.  
  An OpenReview bug in November 2025 broke anonymity at several conferences and prompted calls for open review, which motivate us to ask what shifting from blind to open would mean for authors. Analyzing over 18,000 reviewed submissions to ICLR 2026, split into de facto open and blind groups by arXiv preprint timing, we find that ratings rise with author reputation under both mechanisms, with a …
- <a id="20260914-2609.11990"></a>**Assessment of Non-Institutional AI Tool Usage Among Clinicians** — [2609.11990](https://arxiv.org/abs/2609.11990) | cross: cs.AI  
  Sarah Pungitore, Jarrod Mosier  
  Generative artificial intelligence (AI) tools are increasingly accessible and have the potential to improve efficiency across clinical workflows. However, clinicians may also use non-institutional AI tools that are not provided, managed, or governed by their healthcare institutions, creating potential concerns related to privacy, security, accuracy, and clinician-AI interaction.
- <a id="20260914-2609.12022"></a>**Continuous Learning of Gravity Field Irregularities Around Small Bodies via Neural Hamiltonian ODEs** — [2609.12022](https://arxiv.org/abs/2609.12022) | cross: astro-ph.EP, cs.AI, math.OC, physics.space-ph  
  Giacomo Acciarini, Dario Izzo  
  We propose to learn the unknown dynamics in the proximity of a small body directly from tracking data, representing them as a feed-forward neural network embedded in the system Hamiltonian. The equations of motion form a Neural Hamiltonian Ordinary Differential Equation, whose variational equations provide exact training gradients: estimation uses position and velocity arcs at realistic noise …
- <a id="20260914-2609.12036"></a>**Pelican-Sim 1.0: A General World Model Simulator for Embodied Intelligence** — [2609.12036](https://arxiv.org/abs/2609.12036) | cross: cs.AI  
  Shilong Zou, Shilin Zhang, Yingji Zhang, Yuhang Huang et al.  
  In this technical report, we propose Pelican-Sim 1.0, a general world model simulator for embodied intelligence that predicts future observations from visual context and robot actions to support downstream learning and decision making. The model incorporates four key design features: (1) Unified action representation: a 28-dimensional action value space covering most mainstream embodiments, …
- <a id="20260914-2609.12079"></a>**Hierarchical Prototype Emergence in Modern Hopfield Models** — [2609.12079](https://arxiv.org/abs/2609.12079) | cross: cs.AI, cs.LG  
  Aditya Cowsik, Adithya Sriram  
  Hierarchical correlations are a universal feature of any realistic model of data, and the question of how associative memory models may learn these correlations and generalize beyond them to construct new sensible images is an important step towards understanding more complex modern architectures such as diffusion models. We consider a hierarchical model for memories which are sampled and stored …
- <a id="20260914-2609.12086"></a>**Creating an Atomic User Model for Personality-Aware Large Language Model Interaction** — [2609.12086](https://arxiv.org/abs/2609.12086) | cross: cs.AI, cs.CL  
  B. Sankar, Deepthika S, Pawni Yadav, Amogh A S  
  Assistants built on large language models are expected to write as their user would, and the dominant approach is single-channel: preferences summarised from conversation history and reinserted into context. This inverts the order of inference.
- <a id="20260914-2609.12097"></a>**MAIA: Multi-Agent Intent Articulation for Requirement Discovery in Art Commissions** — [2609.12097](https://arxiv.org/abs/2609.12097) | cross: cs.AI  
  Yu-Chao Wang, Yanhong Lu, Yingjie Victor Chen, Tim McGraw  
  In bespoke art commissions, laypeople know what they feel but lack the words to specify it: one participant wanted a laid-off truck driver depicted as "a ghost in his own machine" but left the medium, scale, and palette unsaid. We frame this as an articulation bottleneck at an under-served upstream stage: requirement discovery, which precedes any artist or image generator and forces the …
- <a id="20260914-2609.12107"></a>**Extracting Dataset Mentions in Forced Displacement and FCV Documents: A Weakly Supervised Framework with LLM-Based Label Refinement** — [2609.12107](https://arxiv.org/abs/2609.12107) | cross: cs.AI, cs.IR, econ.EM  
  Rafael Macalaba, Aivin V. Solatorio, Patrick Michael Brock, Olivier Dupriez  
  Development and humanitarian organizations produce and support surveys, administrative registries, and other data resources to inform research, policy, and operations, yet systematically identifying where these datasets are referenced remains difficult. Such references are dispersed across research papers, project documents, humanitarian reports, and other unstructured text, limiting both the …
- <a id="20260914-2609.12136"></a>**The Anatomy and Boundary of Adaptation under Temporal Tabular Shift** — [2609.12136](https://arxiv.org/abs/2609.12136) | cross: cs.AI  
  Tianyu Wang, Xi Vincent Wang, Lihui Wang, Mian Li et al.  
  Prequential adaptation of frozen tabular foundation models under temporal drift, with each label revealed only after prediction, helps some deployments and harms others, yet current practice does not predict which. We study the sources and limits of these gains.
- <a id="20260914-2609.12154"></a>**Neural Multichannel Distant Speaker Diarization with Heavy-tailed Source Separation Model** — [2609.12154](https://arxiv.org/abs/2609.12154) | cross: cs.AI  
  Sicheng Mao, Baihan Li, Mathieu Fontaine, Anthony Larcher et al.  
  Distant speaker diarization remains challenging due to difficult acoustic environments, varying numbers of speakers and overlapping speech. Model-driven methods are proposed to exploit the speech source features in multi-channel recordings that help diarization.
- <a id="20260914-2609.12168"></a>**USPLIT-VQA: U-Shaped Split Learning for Visual Question Answering with Contribution-Aware Weighted Aggregation** — [2609.12168](https://arxiv.org/abs/2609.12168) | cross: cs.AI  
  Md Khalid Syfullah, Alvi Ataur Khalil  
  Visual Question Answering (VQA) systems, jointly interpreting images and natural language queries, hold significant promise across many domains, yet the privacy-sensitive nature of user data creates a fundamental barrier. Centralized training requires access to all data, while federated learning requires each client to host the full model.
- <a id="20260914-2609.12170"></a>**NDT Factory: Synthesizing Verified Network Digital Twins from Semantic Models via Multi-Agent LLM** — [2609.12170](https://arxiv.org/abs/2609.12170) | cross: cs.AI, cs.MA, cs.SE  
  Sudipta Acharya, Petar Djukic, Burak Kantarci  
  Autonomous network management requires systems that can evaluate Network Service Intents (NSIs) under varying conditions without manual implementation of analysis logic, as envisioned in TM Forum Level~4 (L4) autonomy. Behavioral Network Digital Twins (NDTs) enable such evaluation, but existing NDTs rely on pre-defined analytical logic, limiting adaptability for evolving closed-loop control.
- <a id="20260914-2609.12184"></a>**Agentic TCAD Calibration Workflow for Oxide Semiconductor Transistors** — [2609.12184](https://arxiv.org/abs/2609.12184) | cross: cs.AI, cs.LG, physics.app-ph  
  Gyujun Jeong, Junmo Lee, Sungwon Cho, Woohyun Hwang et al.  
  Experimental TCAD calibration is essential for predictive technology modeling of emerging oxide semiconductor transistors. However, it remains time-consuming and expert dependent because of model ambiguity.
- <a id="20260914-2609.12202"></a>**QuPAINT: Physics-Aware Multimodal Reasoning for Quantum Material Characterization** — [2609.12202](https://arxiv.org/abs/2609.12202) | cross: cs.AI, cs.LG  
  Sankalp Pandey, Xuan-Bac Nguyen, Hoang-Quan Nguyen, Tim Faltermeier et al.  
  Characterizing two-dimensional (2D) quantum materials by optical microscopy requires localizing exfoliated flakes and determining their layer thickness from subtle optical contrast and interference color to select suitable flakes for device fabrication. However, models face synthetic-to-real domain shifts and variation across materials, substrates, laboratories, and imaging conditions.
- <a id="20260914-2609.12230"></a>**Repair Before Reinforce: Context-Augmented Knowledge Graph Reasoning for Multi-Hop Question Answering** — [2609.12230](https://arxiv.org/abs/2609.12230) | cross: cs.AI  
  Tharaka D. Fonseka, Niraj K. Jha  
  Question-answering often requires reasoning across multiple connected facts rather than retrieving a single isolated relation. Knowledge graphs (KGs) provide a structured way to represent such facts, but training large language models (LLMs) only on isolated KG head-relation-tail triples may limit their ability to learn the surrounding context needed for multi-hop reasoning.
- <a id="20260914-2609.12252"></a>**DriftSE: Speech Enhancement with Generative Drifting** — [2609.12252](https://arxiv.org/abs/2609.12252) | cross: cs.AI, eess.AS  
  Liang Xu, Diego Caviedes-Nozal, W. Bastiaan Kleijn, Longfei Felix Yan et al.  
  We propose DriftSE, a novel one-step generative framework for speech enhancement formulated as a latent distribution equilibrium problem. During training, the drifting field aligns the generator's pushforward distribution with the clean speech manifold through drifting in a latent domain.
- <a id="20260914-2609.12254"></a>**Automated Detection and Structuring of Social Tipping Point Evidence in Climate related Documents: A Modular AI Framework** — [2609.12254](https://arxiv.org/abs/2609.12254) | cross: cs.AI  
  Kavindu Perera, Mohammad Abaeiani, Ekaterina Gilman, Lauri Loven et al.  
  The climate literature has grown faster than review teams can read it. That gap matters most for a concept like the environmental social tipping point, the threshold at which a small change triggers rapid, self-reinforcing change in a social system.
- <a id="20260914-2609.12260"></a>**HypoKG: Evidence-Disciplined Biomedical Hypothesis Generation Beyond Endpoint Knowledge** — [2609.12260](https://arxiv.org/abs/2609.12260) | cross: cs.AI, q-bio.QM  
  Dominic Okonkwo, Adetayo Okunoye, Ismailcem Budak Arpinar  
  Large language models (LLMs) can generate biomedical hypotheses, but it remains unclear whether they truly reason from scientific evidence or simply produce convincing-sounding ideas. To study this, we combine three major biological databases: the Kyoto Encyclopedia of Genes and Genomes (KEGG), Rhea, and UniProt, into a unified biochemical knowledge graph and construct a benchmark of 550 paths …
- <a id="20260914-2609.12270"></a>**Recommendation Retrievers Need Verifiers: Universal Generative Reranking for Sequential Recommendations** — [2609.12270](https://arxiv.org/abs/2609.12270) | cross: cs.AI  
  Benyu Zhang, Qiang Zhang, Rui Li, Qunshu Zhang et al.  
  First-stage recommenders in multi-stage systems produce a ranked candidate list from which a limited prefix is forwarded to downstream rankers. Because each forwarded item must be processed by more expensive ranking stages, this shortlist cannot be arbitrarily large.
- <a id="20260914-2609.12303"></a>**Breaking the Token Ceiling: Distilling Smaller, Stronger Byte Models** — [2609.12303](https://arxiv.org/abs/2609.12303) | cross: cs.AI, cs.LG  
  Kalyani Marathe, Artidoro Pagnoni, Tomasz Limisiewicz, Margaret Li et al.  
  Small models are made more capable through distillation from a larger one that shares their tokenization scheme. However, do distilled byte and token models behave similarly in terms of scaling trends as compute and data increases?
- <a id="20260914-2609.12305"></a>**Self-Verifying Anomaly Detection using Explainable AI for Cybersecurity of DER Networks** — [2609.12305](https://arxiv.org/abs/2609.12305) | cross: cs.AI, cs.LG  
  Damilola Popoola, Souradeep Bhattacharya, Manimaran Govindarasu  
  The rapid growth of Distributed Energy Resources (DERs) has significantly expanded the cyber attack surface of modern power grids. Furthermore, increasing sophistication in attack techniques demands anomaly detection systems (ADS) that are accurate, interpretable, and reliable to support DER cybersecurity.
- <a id="20260914-2609.12310"></a>**ESTS at WMT26: Routing-Informed Expert Pruning for Model Compression** — [2609.12310](https://arxiv.org/abs/2609.12310) | cross: cs.AI, cs.LG  
  Liu O. Martin, Lucas Bandarkar, Nanyun Peng  
  We describe six submissions under the team name ESTS to the unconstrained WMT26 Model Compression Shared Task for English--Simplified Chinese and English--Egyptian Arabic. We submit three compression operating points per translation direction, all derived from GPT-OSS-20B.
- <a id="20260914-2609.12366"></a>**ORQA: An Occupation-Realistic Question and Answer Framework for LLM Professional Knowledge** — [2609.12366](https://arxiv.org/abs/2609.12366) | cross: cs.AI  
  Shreyas Krishnan, Serina Chang, Abhishek Nagaraj  
  We present ORQA, a method for testing occupation-level knowledge in large language models. Prior methods either map abstract LLM skills to occupations via task definitions or utilize expert knowledge which is difficult to obtain at scale and expensive.
- <a id="20260914-2609.12388"></a>**RF-VoID: Towards Bandwidth-Efficient Exterior Tile Void Detection via Narrowband Radio-Frequency Representation Learning** — [2609.12388](https://arxiv.org/abs/2609.12388) | cross: cs.AI  
  Xinyan Chen, Ruiqin Ma, Shunsuke Shoda, Changyu Zhou et al.  
  Hidden debonding behind exterior ceramic tiles is a falling-tile hazard, and millimeter-wave radar offers a non-contact way to find it. Conventional interpretation first reconstructs a range profile, so its reliability is bounded by the available bandwidth, yet bandwidth is what sets the cost, the acquisition time, and the regulatory footprint of a deployed system.
- <a id="20260914-2609.12397"></a>**UFO: Chain-of-Evaluation for Omni-Condition Alignment in Multi-Modal Image Generation** — [2609.12397](https://arxiv.org/abs/2609.12397) | cross: cs.AI  
  Danning Zhang, Yijing Lin, Shuhan Zhuang, Mengqi Huang et al.  
  Multi-modal image generation, particularly subject-driven customization, has garnered growing attention in recent years. Despite the rapid advancement of generative models, their evaluation remains largely lagging.
- <a id="20260914-2609.12439"></a>**Debiasing as a Measurement Intervention: Calibrated Ties and Resolution Loss in LLM-as-a-Judge Evaluation** — [2609.12439](https://arxiv.org/abs/2609.12439) | cross: cs.AI  
  Liang Zhao, Yong Wang, Jiangzhe Chen  
  LLM-as-a-judge protocols are commonly debiased by instructing judges to ignore presentation cues such as citation formatting, source labels, and evidence-display style. We show that this intervention can suppress bias while damaging the resolution of the measurement instrument.
- <a id="20260914-2609.12441"></a>**IMPLY: Physically Anchored Consistency for World-Model Rollouts** — [2609.12441](https://arxiv.org/abs/2609.12441) | cross: cs.AI, cs.CV, cs.LG  
  Aman Mehta, Riya Baviskar  
  A world model asked what happens if an object is pushed at several speeds produces several futures. If the model has the object in mind, those futures agree about it: each implies the same mass and friction.
- <a id="20260914-2609.12454"></a>**Bridging Vision Foundation Model Priors with CLIP for Spatial-aware Few-shot Anomaly Detection in Medical Images** — [2609.12454](https://arxiv.org/abs/2609.12454) | cross: cs.AI, cs.LG  
  Juzheng Miao, Yuchen Yuan, Cheng Chen, Pheng-Ann Heng  
  Vision-Language Models such as CLIP enable effective few-shot medical anomaly detection (AD) via strong image-text semantic alignment. However, their globally contrastive pretraining lacks explicit spatial supervision, limiting precise lesion localization.
- _…另有 32 篇, 见 `data/20260914.json`_

#### cs.LG (132)

- <a id="20260914-2609.12896"></a>**Behavior Quotient Learning for Low-Rank Adaptation of LLM Agents** — [2609.12896](https://arxiv.org/abs/2609.12896) | cross: cs.AI | 🎯🧐 LLM-based agent  
  Pengyang Zhou, Xiaobin Tu, Zhengxi Liu, Rongkun Xue et al.  
  LLM-based agents rely on heterogeneous interaction capabilities to accomplish complex tasks. Existing approaches often distribute these capabilities across multiple LoRA adapters, which increases adapter storage requirements and introduces routing overhead during inference.
- <a id="20260914-2609.12331"></a>**Simulating Disengaged Students to Evaluate LLM-based Tutors** — [2609.12331](https://arxiv.org/abs/2609.12331) | 🎯★ consensus  
  Xianghui Meng, Jionghao Lin  
  Simulated students generated by computational models provide a practical way to evaluate tutoring strategies and pedagogical approaches used by human and AI tutors. However, such simulations should account for disengaged behaviors, including gaming the system, wheel-spinning, and off-task behavior, because tutors may need different responses for different learner states.
- <a id="20260914-2609.12002"></a>**Can We Trust LLM Judges: A Study of Capability-Dependent Biases and Multi-Judge Ensemble for Bias Calibration** — [2609.12002](https://arxiv.org/abs/2609.12002) | cross: cs.AI  
  Gemma Zhang, Prachi Badarayani, Asmi Kumar, Sadid Hasan et al.  
  LLMs are increasingly used as automated judges for model training and evaluation, yet individual judges exhibit systematic biases that undermine reliability. Much of prior work has studied biases in pairwise LLM-as-a-judge settings; in this paper, we focus on absolute scoring tasks, which mirror more realistic use cases.
- <a id="20260914-2609.12179"></a>**Explanations-Driven Active Feature Acquisition for Algorithmic Recourse** — [2609.12179](https://arxiv.org/abs/2609.12179) | cross: cs.AI  
  Vinura Galwaduge, Jagath Samarabandu  
  Algorithmic recourse methods typically assume that a predictive model has access to all features of an individual. In practice, decisions are often made with partial information, because features are costly to acquire.
- <a id="20260914-2609.12223"></a>**Predicting Collision Cross Sections with GRACE: Geometric Residual Adduct Conditioning via Early-fusion** — [2609.12223](https://arxiv.org/abs/2609.12223) | cross: cs.AI, q-bio.BM  
  Parthasarathy Suryanarayanan, Susanta Das, Shreyans Sethi, Kenneth M. Merz et al.  
  Collision cross section (CCS), derived from ion mobility mass spectrometry, is a common descriptor for molecular annotation. Prediction is challenging for machine learning models because it reflects the size, shape, and ionization state of a gas-phase molecular ion.
- <a id="20260914-2609.12277"></a>**Reinforcement Learning over Patient Trajectories for Clinical Reasoning in EHR Foundation Models** — [2609.12277](https://arxiv.org/abs/2609.12277) | cross: cs.AI, cs.CY  
  Yuxin Xiao, Sheng Zhang, Chandan Singh, Tristan Naumann et al.  
  Electronic health record (EHR) foundation models trained on longitudinal patient trajectories have demonstrated strong performance across diverse clinical prediction tasks. However, their clinical reasoning capabilities remain constrained by next-token prediction on limited and incomplete EHR data.
- <a id="20260914-2609.12278"></a>**Amortized Low-Rank Adaptation for Model-Based Reinforcement Learning** — [2609.12278](https://arxiv.org/abs/2609.12278) | cross: cs.AI, cs.RO  
  Fernando Palafox, David Fridovich-Keil  
  World models let agents plan by predicting the consequences of their actions, but changes in the environment can make them inaccurate. We study the problem of adapting a world model to an unknown test-time environment, drawn from a known environment family, using only a few episodes of interaction.
- <a id="20260914-2609.12419"></a>**MInTRL: Off-policy Intervention can boost On-policy RL** — [2609.12419](https://arxiv.org/abs/2609.12419) | cross: cs.AI  
  Mingyu Chen, Yefan Tao, Gerald Friedland, Xuezhou Zhang et al.  
  Reinforcement learning with verifiable rewards is typically performed on-policy, keeping training data close to the current policy but limiting learning to trajectories that the policy can discover itself. Off-policy methods such as supervised fine-tuning, on the other hand, can leverage external knowledge beyond the base model's capabilities, but may suffer from large distribution shift.
- <a id="20260914-2609.12435"></a>**Observation-Anchored Selective Assimilation for Longitudinal Tumor-State Proxy Forecasting in Post-Treatment Glioma** — [2609.12435](https://arxiv.org/abs/2609.12435) | cross: cs.AI  
  Yeonjae Jung, Minwoo Shin  
  Post-treatment MRI in patients with glioma provides serial observations for updating patient-specific tumor-state proxy estimates, but variable appearances and trajectories complicate forecasting. We formulate forecasting as an observation-aware digital-twin update in which an intermediate observation anchors the patient-specific state.
- <a id="20260914-2609.12437"></a>**Beyond the Query: Do Retrieval Signals Improve Adaptive Multimodal RAG Routing?** — [2609.12437](https://arxiv.org/abs/2609.12437) | cross: cs.AI  
  Qiaomu Li, Qiuyuan Zhang, Nong Ming  
  Adaptive RAG often uses retrieval-time signals to decide whether another retrieval, reranking, or multimodal step should run. We ask whether these signals add routing value once the query itself is already known.
- <a id="20260914-2609.12442"></a>**3D Digital Twin Visualization of Multiclass GRF-Based Gait Disorder Classification** — [2609.12442](https://arxiv.org/abs/2609.12442) | cross: cs.AI  
  Nayoung Son, Minwoo Shin  
  Automated gait analysis requires accurate classification and interpretable outputs. We propose an integrated framework for classifying healthy gait and multiple musculoskeletal impairment groups using bilateral ground reaction force (GRF) and center-of-pressure (COP) signals.
- <a id="20260914-2609.12563"></a>**TokenMapper: A Step Toward Interoperable Speech Token Translation** — [2609.12563](https://arxiv.org/abs/2609.12563) | cross: cs.AI, cs.SD, eess.AS  
  Tal Kozakov, Tal Rosenwein, Eliya Nachmani  
  Neural audio codecs discretize speech into token sequences, but the resulting token spaces differ in vocabulary and codebook structure, preventing direct communication across models. This limitation affects applications such as conversational voice agents and speech to speech translation systems where multiple speech models must interact.
- <a id="20260914-2609.12579"></a>**SCOPE-OPSD: Fisher-Conditioned Privileged Subspaces for On-Policy Self-Distillation** — [2609.12579](https://arxiv.org/abs/2609.12579) | cross: cs.AI  
  Yunmeng Chen (Chongqing Ant Consumer Finance Co., Ltd), Kunyu Wang (Alibaba Cloud Computing Co., Ltd) et al.  
  On-policy self-distillation (OPSD) scores student-generated prefixes with a solution-conditioned self-teacher, yet transfers supervision only through next-token probabilities. We ask whether the aligned final-layer discrepancy offers a useful second channel, and how to test that channel without confusing its geometry with auxiliary strength.
- <a id="20260914-2609.12584"></a>**Clustering-Based Balanced Sampling and Allocation with Data Parallelism for High-Performance Fine-Tuning** — [2609.12584](https://arxiv.org/abs/2609.12584) | cross: cs.AI  
  Hyunjin Kim, Youngeun Nam, Jaemin Han, Wonhyeok Choi et al.  
  Instruction-tuning datasets for large language models (LLMs) are often large, redundant, and imbalanced, limiting efficient adaptation. Naive large-batch fine-tuning repeatedly includes overrepresented sample groups while weakly covering underrepresented but informative ones, especially under data parallelism (DP) across multiple GPUs.
- <a id="20260914-2609.12599"></a>**SIMS: Scale-Invariant Merit-Function-Based Scalarization for Multi-Task Learning** — [2609.12599](https://arxiv.org/abs/2609.12599) | cross: cs.AI, math.OC  
  Zebin Chen, Fei Xing, Yang Chen, Hua Liu et al.  
  Multi-task learning (MTL) requires navigating unavoidable trade-offs among competing objectives. This paradigm is frequently formulated as multi-objective optimization (MOO), where the scalarization is favored to reduce an MOO problem to a single objective.
- <a id="20260914-2609.12620"></a>**Correlation-Guided Fast Machine Unlearning via Hessian Analysis** — [2609.12620](https://arxiv.org/abs/2609.12620) | cross: cs.AI  
  Ayushi Thakur, Ruchir Gupta, Amit Kumar Jaiswal, Prayag Tiwari  
  The increasing adoption of machine learning in network and distributed security systems has created an urgent need for mechanisms that can selectively and efficiently remove the influence of specific training data to eliminate compromised or adversarial data points from production models. Privacy regulations such as GDPR's \emph{right to be forgotten} also pose similar requirements.
- <a id="20260914-2609.12639"></a>**Explaining Time Series Forecasting with Horizon-Resolved Attribution** — [2609.12639](https://arxiv.org/abs/2609.12639) | cross: cs.AI  
  Seunghan Lee, Jun Seo, Jaehoon Lee, Junhyeok Kang et al.  
  Recent advances in explaining time series (TS) models have produced methods that identify which past values a prediction depends on. However, most existing methods return a single importance vector, assuming that every predicted step depends on the same past values.
- <a id="20260914-2609.12712"></a>**InRTL: Effective Intra-Inter Interaction Learning for Relational Tables** — [2609.12712](https://arxiv.org/abs/2609.12712) | cross: cs.AI  
  Weichen Li, Ken Zhong, Zheng Wang, Li Pan et al.  
  Relational table learning has recently emerged as an important research direction for modeling multiple tables connected through primary key-foreign key (PK-FK) relationships. Despite recent advances, a principled modeling framework tailored to this task remains underexplored.
- <a id="20260914-2609.12814"></a>**RunningTensor: Generalizing Linear Attention to Higher-Order Recurrent States** — [2609.12814](https://arxiv.org/abs/2609.12814) | cross: cs.AI  
  Luca Herranz-Celotti, Vincent Guigue  
  Linear attention and state-space models provide linear-time sequence modeling, but their recurrent memory remains a second-order tensor (a matrix), limiting the order of interactions that can be represented in the state. We introduce the RunningTensor, which generalizes this memory to an order-$o$ tensor, updated by a rank-1 outer product and read by contracting against $o-1$ vector queries.
- <a id="20260914-2609.12890"></a>**Large Distant Gradients Need Not Be Reliable: reliability-weighted credit assignment for long-horizon autoregressive forecasting** — [2609.12890](https://arxiv.org/abs/2609.12890) | cross: cs.AI  
  Junhao Zhao, David Michael Simberg, Jacob Kang, Colin Connor Kurniawan et al.  
  In autoregressive forecasting, long prediction rollouts provide distant supervision, but backpropagation through time (BPTT) carries gradients from those losses through many autoregressive steps. Repeated Jacobian products can make distant gradients dominate the update while amplifying predictable signal and unpredictable noise together; a large distant gradient therefore need not carry reliable …
- <a id="20260914-2609.13031"></a>**Attention Quantization for Tabular Foundation Models** — [2609.13031](https://arxiv.org/abs/2609.13031) | cross: cs.AI  
  Jonas M. K\"ubler, Benjamin J\"ager, Klemens Fl\"oge, Noah Hollmann et al.  
  With the recent rise and adoption of tabular foundation models, optimizing their inference performance becomes an emerging field for efficiency research. While the models are architecturally similar to transformer-based large language models (LLMs), the size and serving patterns differ significantly.
- <a id="20260914-2609.13035"></a>**Groupoid-Based Internal State Representations for Reinforcement Learning with Local Symmetries** — [2609.13035](https://arxiv.org/abs/2609.13035) | cross: cs.AI  
  Ben Opperman, Eduardo Alonso, Esther Mondrag\'on  
  Symmetries play a central role in reducing the complexity of reinforcement learning problems, yet most existing approaches rely on fixed group actions or predefined state abstractions. Classical reinforcement learning algorithms typically assume a globally structured Markov decision process with uniformly applicable actions and transitions, an assumption that limits their ability to exploit …
- <a id="20260914-2609.13042"></a>**DynSHAP: Towards Explainable Dynamic Survival Analysis** — [2609.13042](https://arxiv.org/abs/2609.13042) | cross: cs.AI  
  Nastasya Anokhina, Jonas J\"ur{\ss}, Pietro Li\`o  
  Deep learning models for dynamic survival analysis (DSA) achieve strong predictive performance by incorporating longitudinal patient data, but their black box nature limits clinical trust and adoption. Existing explainability methods cannot handle longitudinal, irregular inputs and functional survival outputs simultaneously, which limits their usability in DSA.
- <a id="20260914-2609.13072"></a>**MAxBench: A Multinomial Concept Recovery Benchmark** — [2609.13072](https://arxiv.org/abs/2609.13072) | cross: cs.AI, cs.CL  
  Divya Appapogu, Freya Behrens, Yonatan Belinkov, Aaron Mueller  
  Fine-grained control of language model behaviors (e.g., steering) is among the more actionable outcomes of interpretability research. For binary concepts such as refusal, a single direction in activation space often suffices for steering.
- <a id="20260914-2609.11934"></a>**Fundamental Dynamical Units for Physics-Informed Structural Inference from Perturbation Time-Series in Networked Systems** — [2609.11934](https://arxiv.org/abs/2609.11934) | cross: physics.comp-ph  
  Nima Nouri  
  In networked dynamical systems, the parameter of primary mechanistic interest is signed interaction structure. Recovering this structure from perturbation time-series data is a fundamental identification problem, compounded by three coupled obstacles: the combinatorial complexity of interaction architectures, ambiguity of causal attribution under limited interventions, and state-dependent …
- <a id="20260914-2609.11935"></a>**Physics-Informed Conformal Prediction: Embedding PDE Consistency into Distribution-Free Uncertainty Quantification for Neural Operators** — [2609.11935](https://arxiv.org/abs/2609.11935)  
  Michael Chin  
  Neural operators such as the Fourier Neural Operator (FNO) achieve remarkable accuracy in approximating solutions to partial differential equations (PDEs). However, providing rigorous uncertainty estimates remains an open challenge.
- <a id="20260914-2609.11937"></a>**Fed-Equilibrium Framework for Topological Pareto Control in Robust and Fair Clinical Federated Learning** — [2609.11937](https://arxiv.org/abs/2609.11937) | cross: cs.DC  
  Ting Xu, Henry Leung  
  The deployment of Federated Learning (FL) in multi-center clinical networks faces the challenge of "knowledge dominance," where high-volume hubs naturally overwhelm minority community nodes, implicitly treating the distinct clinical patterns of smaller cohorts as outliers. Existing geometric defenses provide a security baseline but leave this efficiency-fairness dilemma unresolved.
- <a id="20260914-2609.11954"></a>**Efficient AI Model Deployment Using Quantization Analysis Tool** — [2609.11954](https://arxiv.org/abs/2609.11954)  
  Dwith Chenna, Kanishka Macherla  
  As deep learning models are increasingly deployed on resource constrained devices, the demand for efficient model optimization techniques continues to grow. Effective deployment of AI models on edge and low power platforms requires optimization methods that reduce model size and computational cost while maintaining high accuracy.
- <a id="20260914-2609.11956"></a>**Performance, Efficiency and Collapse -- Advantages and Challenges in Offline Post-training of Code LLMs** — [2609.11956](https://arxiv.org/abs/2609.11956)  
  Abhinav Anand, Sanjana Reddy Pachika, Shweta Verma, Mira Mezini  
  Post-training with reinforcement learning (RL) is a critical phase in the development of code-generating large language models (LLMs), as it ensures adherence to instructions and the production of functionally correct code. This process typically requires computationally intensive code sample generation from Transformer-based LLMs and substantial GPU-CPU communication for sequence verification.
- <a id="20260914-2609.11957"></a>**Look Before You Leap: Pre-Action Verification for LLM Agents** — [2609.11957](https://arxiv.org/abs/2609.11957) | cross: cs.MA  
  Asaad Althoubi  
  An LLM agent acts on the world by emitting actions: shell commands to run, edits to apply. A wrong action does not always fail loudly; it can fail silently, producing a plausible but incorrect effect that raises no error.
- <a id="20260914-2609.11958"></a>**Decoding Mixture Perception through Computational Modeling of Component Interactions** — [2609.11958](https://arxiv.org/abs/2609.11958)  
  Fei Wang, Xiaoya Xie, Junfei Liu, Huihao Wang et al.  
  Olfaction played an indispensable role throughout human evolution and civilization. Even in the contemporary era of advanced technology, olfaction remains a critical channel for person to conduct danger discrimination, emotional experience, and memory formation.
- <a id="20260914-2609.11959"></a>**Space as an Interventional Invariant: Cross-Modal Predictive Geometry for Stratified Cities and Em-Spaced Intelligence** — [2609.11959](https://arxiv.org/abs/2609.11959) | cross: cs.CL  
  Tao Yang, Xuhui Lin, Kunyao Li, Haijiang Li  
  Space is a foundational concept across mathematics, physics, spatial cognition, urban science, and embodied intelligence, yet these fields often treat spatial structure either as a shared geometric container or as a collection of disconnected representations. Such approaches struggle to explain how heterogeneous sensory and urban processes can jointly reveal a common spatial structure, …
- <a id="20260914-2609.11961"></a>**On-Device Language Models for Privacy-Preserving Stress Prediction: A Multimodal Evaluation on Mobile Health** — [2609.11961](https://arxiv.org/abs/2609.11961) | cross: cs.HC  
  Ibukunoluwa Soyebo, Alyssa Donawa, Rodrigo Aguilar Barrios, Brice Patchou et al.  
  Stress is a pervasive determinant of mental health and a key target for mobile health interventions. On-device language models (ODLMs) offer privacy-preserving inference without cloud dependency, yet their feasibility for health prediction under mobile resource constraints remains underexplored.
- <a id="20260914-2609.11993"></a>**FINESSE: An Agent-Based Simulator and Benchmark Dataset for Multimodal Financial Event Sequences** — [2609.11993](https://arxiv.org/abs/2609.11993)  
  Tyler Farnan, Benjamin Eng, Adam Abate, Xirui Hou et al.  
  Machine learning research in financial services is limited by the scarcity of representative open-source datasets. Existing resources are often narrowly focused on a single modality or task and fail to reflect the structured, multimodal, and dynamic nature inherent to many problems in financial services.
- <a id="20260914-2609.11995"></a>**Explainable Prediction from Mobile Sensing Data through LLM-guided Concept Integration** — [2609.11995](https://arxiv.org/abs/2609.11995)  
  Yuning Wang, Iman Azimi, Amir M. Rahmani, Pasi Liljeberg  
  Mobile sensing enables longitudinal monitoring of behavioral and physiological patterns in everyday settings. However, accurate prediction remains challenging in small-cohort health-sensing studies, where task-specific outcome supervision is limited relative to heterogeneous sensing data.
- <a id="20260914-2609.11997"></a>**DCRA: Diffusion-Conditioned Representation Alignment for Robust Time-Series Learning** — [2609.11997](https://arxiv.org/abs/2609.11997) | cross: stat.ML  
  Wenrui Xu, Anas Enanaa, Keshab K. Parhi  
  Learning robust representations for time-series signals under noise and distribution shifts remains challenging, especially in clinical applications such as electroencephalogram (EEG) and electrocardiogram (ECG) analysis. We propose Diffusion-Conditioned Representation Alignment (DCRA), a training framework that repurposes the forward diffusion process as a structured corruption scheduler for …
- <a id="20260914-2609.11998"></a>**Fixed State, Long Reach: What a Constant-Size Cache Buys Block Diffusion at Scale** — [2609.11998](https://arxiv.org/abs/2609.11998)  
  Vaibhav Singh, Pierre-Andr\'e No\"el, Torsten Scholak, Eugene Belilovsky et al.  
  Diffusion language models decode tokens in parallel, but their bidirectional denoiser rules out the naive key--value (KV) cache behind fast autoregressive inference. Block diffusion restores caching by decoding block-by-block, and the block caches deployed on it so far are tied to attention: O(L)in memory and, if used as training-free retrofits, only an approximation of the model's computation.
- <a id="20260914-2609.12011"></a>**QTrans: A Quantum Transformer for Sentiment Classification** — [2609.12011](https://arxiv.org/abs/2609.12011)  
  Ren-Xin Zhao, Xinjie Huang, Yahong Liu, Maoyu Ye et al.  
  In small-scale binary sentiment classification scenarios, factors such as negation, contrastive shifts, and cross-word dependencies lead to the non-linear coupling of sentiment cues, making it difficult for conventional lightweight models to fully capture the contextual relationships between tokens. To address this issue, we propose a model named QTrans, which uses parameterized quantum circuits …
- <a id="20260914-2609.12014"></a>**Certified Safety Curation: Distribution-Free Guarantees for Safe Offline Reinforcement Learning** — [2609.12014](https://arxiv.org/abs/2609.12014)  
  Adam Haroon, Cody Fleming  
  Safe offline reinforcement learning assumes a cost function on every transition. We ask what remains possible when safety can be judged only by comparing short clips and occasionally asking whether an episode exceeded its budget.
- <a id="20260914-2609.12016"></a>**Inverting Self-Triggered Control: Adversarial Reinforcement Learning for Sparse Denial-of-Service Attacks** — [2609.12016](https://arxiv.org/abs/2609.12016) | cross: cs.SY, eess.SY  
  Adam Haroon, Erick J. Rodr\'iguez-Seda, Tristan Schuler, Cody Fleming  
  Self-triggered reinforcement learning control (RL-STC) learns the sparsest control schedule that preserves Lyapunov-decreasing stability under a Run-Time Assurance (RTA) override. We invert this: an adversarial RL agent learns the sparsest jamming or Denial-of-Service (DoS) schedule that destabilizes the closed loop, with a Lyapunov-increase admissibility predicate mirroring the defender's safety …
- <a id="20260914-2609.12018"></a>**Toward Reliable Railway-Bogie Response Prediction Using Multifidelity TDNN and Physics-Informed Residual Learning** — [2609.12018](https://arxiv.org/abs/2609.12018) | cross: physics.app-ph  
  Gyeolhee Lee, Moosun Kim, Taewook Kwon, Jaehun Kim et al.  
  Railway engineers need simulation models that predict vehicle responses across operating scenarios that cannot be tested exhaustively. Agreement with representative measurements provides essential evidence, but calibration at a limited set of conditions does not guarantee accuracy elsewhere.
- <a id="20260914-2609.12020"></a>**Reinforcement Learning for Syndrome Extraction** — [2609.12020](https://arxiv.org/abs/2609.12020) | cross: quant-ph  
  John Zhuoyang Ye, Aarav Pabla, Jens Palsberg  
  A key subtask of quantum error correction is to extract a syndrome that, if nontrivial, signals an error. The number of possible ways to extract a syndrome grows exponentially with the syndrome size, and these implementations vary greatly in fault tolerance, as measured by their logical error rates.
- <a id="20260914-2609.12067"></a>**Scalable Discrete-to-Continuous Channel Simulation for Compression and Privacy** — [2609.12067](https://arxiv.org/abs/2609.12067) | cross: cs.IT, math.IT  
  Joseph Rowan, Buu Phan, Ashish J. Khisti  
  Channel simulation has recently emerged as a useful component in machine learning systems where samples from a prescribed probability distribution are to be compressed. Yet, general channel simulation algorithms often suffer from high computational costs, random stopping times or, in the worst case, can require generating an infinite number of shared random samples.
- <a id="20260914-2609.12113"></a>**Score-based Outlier Generation via Controlling the Radon-Nikodym Derivative** — [2609.12113](https://arxiv.org/abs/2609.12113) | cross: math.AP, math.OC, math.PR, stat.ML  
  Amartya Mukherjee, Tristan Milne, Kry Yik-Chau Lui, Stephanie Hazlewood et al.  
  Outliers are important for stress-testing algorithms and understanding system behaviour under rare conditions. Despite being commonly described as low-likelihood events, existing generative approaches rarely control likelihood explicitly.
- <a id="20260914-2609.12119"></a>**Almost Sure Convergence Analysis of Stochastic Gradient Methods with Clipping and Additive Noise** — [2609.12119](https://arxiv.org/abs/2609.12119) | cross: math.OC, math.PR  
  Amartya Mukherjee, Jun Liu  
  Stochastic gradient descent (SGD) with gradient clipping and additive noise has become a standard technique for training machine learning models, particularly in applications requiring robustness or privacy guarantees. However, clipping introduces a bias in stochastic gradients, while additive noise introduces additional variance, making the long-run behaviour of individual optimization …
- <a id="20260914-2609.12123"></a>**Rank-Efficient LoRA via Joint Tangent-Space Optimization under Isotropic Curvature** — [2609.12123](https://arxiv.org/abs/2609.12123) | cross: math.OC, stat.ML  
  Zihan Zhu, Zhehang Du, Xuyang Chen, Tim Tsz-Kit Lau et al.  
  Low-Rank Adaptation (LoRA) is an effective approach for adapting large pretrained models by learning low-rank weight updates. In practice, the LoRA rank is used to control an adapter's parameter budget and representational capacity.
- <a id="20260914-2609.12137"></a>**GUIDE: Generative Utility Inference and Decision Engine** — [2609.12137](https://arxiv.org/abs/2609.12137)  
  Anagha Tiwari, Alexander G. Gray, Nick Feamster, Brian Jabarian et al.  
  Measuring the preferences of human users remains a fundamental challenge of AI alignment. Existing elicitation approaches struggle to efficiently discover multidimensional preferences or accurately ground these inferences in domain knowledge.
- <a id="20260914-2609.12163"></a>**Certifying Concept Unlearning in Text-to-Image Diffusion Models** — [2609.12163](https://arxiv.org/abs/2609.12163)  
  Mansi, Luca Marzari, Francesco Leofante  
  Existing evaluations of concept unlearning in text-to-image (T2I) diffusion models primarily rely on attack success rates obtained through automated adversarial prompt search. However, these metrics provide only empirical evidence over a finite set of queries and leave residual leakage over the broader prompt space largely unquantified.
- <a id="20260914-2609.12173"></a>**Estimating Pedestrian Volumes from GIS-Derived Built-Environment Features: A Machine Learning Framework** — [2609.12173](https://arxiv.org/abs/2609.12173)  
  Bahareh Golchin, Banafsheh Rekabdar, Sirisha Kothuri, Joseph Broach  
  Transportation agencies need pedestrian volume estimates across entire road networks to prioritize safety investments, yet manual counts are expensive and cover only a small share of intersections. We present a machine learning pipeline that predicts 2-hour PM peak pedestrian volume at 101 urban intersections in Portland, Oregon, from built-environment, land-use, and street-network features drawn …
- <a id="20260914-2609.12224"></a>**Patient-Reported Survey Data Improve Prediction of Opioid Use Disorder** — [2609.12224](https://arxiv.org/abs/2609.12224)  
  Xiyue Jiang, Zihan Ding, Grace Han, Yinan Liu et al.  
  Electronic health records (EHRs) may incompletely capture patient-reported factors associated with opioid use disorder (OUD). We evaluated whether survey data improve prediction of a first recorded OUD diagnosis among 267,747 All of Us participants with documented opioid exposure, including 15,287 OUD cases.
- <a id="20260914-2609.12225"></a>**PLSP (Pre-hoc Liminal Space Profiling): OOD Prediction over Detection -- An Anticipatory Approach for Machine Learning Model Reliability** — [2609.12225](https://arxiv.org/abs/2609.12225) | cross: cs.CV  
  Vipul Bansal, Himanshu Buckchash, Balasubramanian Raman, Deepak Dhungana  
  Out-of-Distribution (OOD) data poses a significant threat to machine learning models, often leading to model failure during deployment. All existing OOD detection methods are post-hoc, relying on evaluation metrics such as accuracy and AUC-ROC during inference to indirectly assess the model's response to OOD data by measuring deviations.
- <a id="20260914-2609.12244"></a>**CRFCAN: A Complex-Valued Cross-Domain Residual Network for Joint Channel and Phase Noise Estimation in Sub-THz OFDM Systems** — [2609.12244](https://arxiv.org/abs/2609.12244) | cross: eess.SP  
  Ruilin Wang, Xiaodai Dong  
  In sub-terahertz (sub-THz) communications, the coupling of ultra-wide bandwidth and severe phase noise (PN) impairments renders conventional joint channel and PN estimation highly complex and computationally prohibitive. To address this, we propose CRFCAN, a complex-valued residual FFT convolutional attention network designed for joint channel and PN estimation.
- <a id="20260914-2609.12259"></a>**The Rank the Task Demands: A Causal Rank Law for Matrix Memories Trained on Group Composition** — [2609.12259](https://arxiv.org/abs/2609.12259)  
  Samuel Larson  
  Matrix-valued memories make rank the natural budget of a learned representation: the number of independent directions a state spans bounds what it can bind, compose, and track. We report causal evidence, on a group-composition testbed trained under a hard single-state bottleneck with a fixed decoder that cannot launder rank, that gradient descent recruits precisely the rank the task's algebra …
- <a id="20260914-2609.12264"></a>**Adaptive Chemotherapy Control under Tumor Heterogeneity via Reinforcement Learning** — [2609.12264](https://arxiv.org/abs/2609.12264) | cross: cs.SY, eess.SY  
  Bereket Sitotaw Kidane, Md Samiul Haque Motayed, Shuo Wang  
  Designing effective chemotherapy regimens is hindered by tumor heterogeneity and drug resistance, which complicate the deployment of patient-specific model-based optimal control across diverse populations. We develop and compare closed-loop deep reinforcement learning (DRL) dosing policies with continuous (TD3) and discrete (DQN) action spaces trained on a high-dimensional heterogeneous tumor …
- <a id="20260914-2609.12298"></a>**FRIST: FMRI Representation Informed Shared-space Training Improves EEG-only Individual-Finger BCI Decoding** — [2609.12298](https://arxiv.org/abs/2609.12298) | cross: eess.SP  
  Jintao Zhang, Yidan Ding, Joshua Kosnoff, Maxim Karrenbach et al.  
  Finger-level motor decoding is important for naturalistic brain-computer interface (BCI) control, yet individual-finger decoding from scalp electroencephalography (EEG) remains challenging because finger representations are spatially close in the sensorimotor cortex and blurred by volume conduction. Leveraging the high spatial resolution of functional MRI (fMRI), we introduce fMRI …
- <a id="20260914-2609.12317"></a>**Sampling via Decision-Flow: Training-Free Extraction of Improved Latent Reasoning Paths in Large Language Models** — [2609.12317](https://arxiv.org/abs/2609.12317)  
  Zhendong Mi, Shaoyi Huang  
  A central question in LLM reasoning is whether reinforcement learning (RL) instills genuinely new capabilities or merely reshapes how existing knowledge is expressed during inference. Building on the distribution-sharpening hypothesis, which holds that RL reallocates probability mass toward high-reward trajectories already latent in base models, we ask: can we unlock those latent paths without …
- <a id="20260914-2609.12337"></a>**Theoretical Guarantees for One-Shot Magnitude Pruning and Compute-Adaptive Early Exit** — [2609.12337](https://arxiv.org/abs/2609.12337)  
  Erdem Koyuncu  
  We study compute reduction in neural networks through a unified partial versus full computation view, captured by one-shot magnitude pruning in the static regime and early exit in the adaptive regime. In an asymptotic single-neuron model, we prove a concentration theorem for one-shot magnitude pruning with explicit rates.
- <a id="20260914-2609.12345"></a>**ParaRecover: A Process-Level Benchmark for Error Localization and Recovery in Parallel Tool-Use Agents** — [2609.12345](https://arxiv.org/abs/2609.12345) | cross: cs.SE  
  Bowen Guan, Zhentao Yin, Yanming Shen  
  Existing agent benchmarks mainly evaluate final task success or tool-call correctness, providing limited insight into whether agents can reliably diagnose and recover from intermediate execution failures. This limitation becomes particularly critical in multi-turn parallel tool-use scenarios, where errors may propagate across dependent branches and trigger cascading failures.
- <a id="20260914-2609.12356"></a>**When Connected Does Not Mean Similar: Charting the Homophily Boundary of SNAP-KG for Streaming Entity Integration** — [2609.12356](https://arxiv.org/abs/2609.12356)  
  Jui-Chien Lin, Oshani Seneviratne  
  SNAP-KG is a framework for assigning newly arriving entities to semantic communities in a growing knowledge graph (KG) using only their raw features, with no graph access and no retraining at inference time. It was evaluated on five multi-view benchmarks and a 2.4M-node OGB-WikiKG2 KG.
- <a id="20260914-2609.12364"></a>**LatentVerse: A Framework for Understanding Shared and Modality-Specific Information in Multimodal Latent Representations** — [2609.12364](https://arxiv.org/abs/2609.12364) | cross: cs.HC  
  Majd Alafrange, Samuel Friedman, John Kitonyo, Sana Tonekaboni et al.  
  Latent embeddings have become a central data abstraction in modern machine learning, especially in biomedicine, where foundation models are increasingly used to encode multimodal data like clinical text, medical images, omics, and physiological signals. However, the utility and value of these representations depends on understanding their quality, structure, and the information they encode.
- <a id="20260914-2609.12365"></a>**Certified AI Triage of ICU Alarms** — [2609.12365](https://arxiv.org/abs/2609.12365)  
  Mohammed Sameer Syed, Rozhin Yasaei  
  In the VTaC benchmark 71% of ventricular-tachycardia alarms are false, but silencing a real one can delay recognition of a dangerous arrhythmia. We reframe alarm reduction as three-way triage (retain, suppress, or defer) and bound the decision this analysis treats as harmful: among suppressed alarms, the fraction that were genuine stays below a user-set budget with 95% confidence, under i.i.d.
- <a id="20260914-2609.12386"></a>**Split Conformal Prediction with Label-Shift-Adjusted Bayesian Scores** — [2609.12386](https://arxiv.org/abs/2609.12386)  
  Hyeonsu Lee, Juyeon Kim, Erkhembayar Jadamba, Seungjin Choi et al.  
  Conformal prediction provides distribution-free uncertainty quantification under exchangeability. However, this assumption is violated by label shift, where the marginal distribution of labels changes while the conditional distribution of inputs given labels remains stable.
- <a id="20260914-2609.12418"></a>**RiPPLE: Cross-Space Performance Prediction from Early Training for Neural Architecture Search** — [2609.12418](https://arxiv.org/abs/2609.12418) | cross: cs.CV  
  Yifan Yang, Zhaoyan Wang, Zheng Gao, Xiaoyu Li et al.  
  Neural architecture search (NAS) evaluates candidate networks, but fully training enough architectures to rank an entire space is expensive. Zero-cost proxies score architectures at initialization, yet their ranking quality varies across search spaces.
- <a id="20260914-2609.12424"></a>**Granularity-Adaptive Credit Assignment for Long-Horizon LLM Agent Reinforcement Learning** — [2609.12424](https://arxiv.org/abs/2609.12424)  
  Taoran Liang, Yang Liu, Shang Luo, Yingguang Yang et al.  
  Reinforcement learning is now the standard way to train large language model agents on long-horizon tasks, where dozens of interdependent actions precede a single sparse reward. Critic-free, group-relative methods such as GRPO suit this regime, but they broadcast one trajectory-level scalar to every step and cannot say which decision drove the outcome.
- <a id="20260914-2609.12455"></a>**SAGE-Loop: Reliable Closed-Loop LLM-Driven AutoML with Trial-and-Correction and Adaptive Ensembling** — [2609.12455](https://arxiv.org/abs/2609.12455)  
  Junquan Gu, Shibo Cui, Xiangfeng Luo, Hang Yu  
  Automated machine learning (AutoML) is reshaping data-driven science and industrial practice, and as large language models are introduced into AutoML, pipeline reliability becomes as important as automation efficiency. However, existing AutoML still struggles to realize instant feedback and adaptive optimization during execution, so once a run drifts into a suboptimal or failed state, it lacks a …
- <a id="20260914-2609.12470"></a>**A Differentially Private Federated Proximal Optimization Framework for Customer Churn Prediction in Heterogeneous Federated Telecom Networks** — [2609.12470](https://arxiv.org/abs/2609.12470)  
  Joydeb Kumar Sana, Subrata Chakraborty, M M Manjurul Islam  
  Customer churn is one of the major issues in the telecommunication industry. To predict customer churn, conventional centralized machine learning approaches have been widely used.
- <a id="20260914-2609.12531"></a>**Temporal Recurrence Favors Fewer Layers** — [2609.12531](https://arxiv.org/abs/2609.12531)  
  Ivan Anokhin, Johan Obando-Ceron, Irina Rish, Sebastian Risi  
  In streaming tasks, recurrent models can carry latent computation across time, allowing each update to build on representations produced earlier. This raises a basic question: once temporal recurrence provides sequential computation across steps, how much depth is still needed within each step?
- <a id="20260914-2609.12532"></a>**$\text{GSF-}\chi$: Global Stereochemical Fields for Chiral Graph Transformers** — [2609.12532](https://arxiv.org/abs/2609.12532)  
  Jiaqing Xie, Yuxin Wang, Xipeng Qiu  
  Enantiomers share atoms, bonds, and pairwise distances yet can behave differently in chiral environments, so molecular encoders must respect atom relabelings and proper rotations without becoming blind to reflection. We introduce GSF-$\chi$, a graph transformer in which stereogenic units modulate all pairwise interactions rather than single out one atom as special.
- <a id="20260914-2609.12550"></a>**Quality-Constrained Routing over a Fixed Pool of Quantized Mixture-of-Experts Instances** — [2609.12550](https://arxiv.org/abs/2609.12550)  
  Zhenghong Huang, Hongfan Wu, Jiheng Zhang  
  Quantized Mixture-of-Experts (MoE) services can hold several pre-materialized instances of one base model, but quantization damage varies sharply across requests and bitwidths. Because instance materialization and replica counts consume memory and require slow reconfiguration, we treat them as upstream provisioning decisions and study routing within a fixed resident pool.
- <a id="20260914-2609.12591"></a>**Where Decoder Cosine Similarity Fails for SAE Feature Flow Discovery** — [2609.12591](https://arxiv.org/abs/2609.12591)  
  Hendrik Droste, Christian Medeiros Adriano, Kathrin Korte, Holger Giese  
  Foundation models are increasingly adapted through fine-tuning, model editing, and alignment procedures while retaining previously acquired capabilities. Understanding the internal computations that support these adaptations is therefore becoming increasingly important for continual model evolution.
- <a id="20260914-2609.12594"></a>**Poisson-Corrector Complexity Bounds for Moreau--Yosida Unadjusted Langevin Sampling** — [2609.12594](https://arxiv.org/abs/2609.12594)  
  Yuchen Xin, Zhihua Zhang  
  We study the classical Moreau--Yosida unadjusted Langevin algorithm (MYULA) for $\pi(\,\mathrm{d} x)\propto e^{-f(x)-g(x)}\,\mathrm{d} x$, where $f\in C^2(\mathbb{R}^d)$ is $m$-strongly convex with $L_f$-Lipschitz gradient and $g:\mathbb{R}^d\to\mathbb{R}$ is convex and globally $G$-Lipschitz. For the Moreau-smoothed target $\pi_\lambda$ and the MYULA invariant law $\widehat\pi_{\lambda,h}$, we …
- <a id="20260914-2609.12627"></a>**Geometric-to-Semantic Spherical Transfer Learning for Cortical Sulci Labeling** — [2609.12627](https://arxiv.org/abs/2609.12627) | cross: cs.CV  
  Saeb Tounsi, Jo\"el Chavas, Pietro Gori, Vincent Frouin et al.  
  Deep learning on cortical surfaces faces a dilemma: capturing the complex topology of over 60 nomenclature-dependent sulci per hemisphere requires high-capacity models, yet the extreme scarcity of expert annotations ($N=62$ subjects) inevitably causes overfitting. Standard supervised approaches fail to generalize in this data-scarce regime, particularly for variable and small sulci where …
- <a id="20260914-2609.12651"></a>**Distortion of AI Alignment Revisited: RLHF is a Decent Utilitarian Aligner** — [2609.12651](https://arxiv.org/abs/2609.12651) | cross: cs.GT  
  Kazusato Oko, Annie Ulichney, Nika Haghtalab, Han Bao  
  While Reinforcement Learning from Human Feedback (RLHF) is the standard paradigm for aligning large language models with human preferences, its effectiveness in pluralistic settings has been called into question. Notably, recent work by G\"olz et al.
- <a id="20260914-2609.12658"></a>**ProactiveBench: Can Streaming Video Models Really Interact Like Humans?** — [2609.12658](https://arxiv.org/abs/2609.12658)  
  Kaixuan Du, Xin Wan, YuKun Wang, Hang Zhang et al.  
  Streaming video understanding requires models to process continuous multimodal input while maintaining temporal context. Existing evaluations are predominantly reactive: they query a model at a selected timestamp and therefore do not assess when it should respond.
- <a id="20260914-2609.12690"></a>**SIFPBPNet: A Dual-Path Network for Wearable and Cuffless Blood Pressure Estimation via Individualized Steady-state Representation** — [2609.12690](https://arxiv.org/abs/2609.12690)  
  Shuailong Tang, Xiaoyu Li, Donglin Xie, Wei Chen et al.  
  Continuous and cuffless blood pressure (BP) monitoring using photoplethysmography (PPG) is of great interest for low-cost and personalized cardiovascular health management. However, significant population heterogeneity and the "one-to-many mapping" problem, where similar waveforms across individuals correspond to different BP levels, limit the accuracy of conventional population-based models.
- <a id="20260914-2609.12702"></a>**Write on Paper and Get the Online Digital Trace:\newline A New Era for Handwriting** — [2609.12702](https://arxiv.org/abs/2609.12702)  
  Florent Imbert, Yann Soullard, Eric Anquetil, Tanja Harbaum et al.  
  Capturing the digital trace of handwriting usually requires a specific stylus and a compatible substrate, be it a capacitive touchscreen, an ElectroMagnetic Resonance (EMR) tablet as used in Wacom systems or special paper. While writing on regular paper offers rich haptics, no latency and is well known for improving information retention, no low-cost and widely accepted, effective solution exists …
- <a id="20260914-2609.12735"></a>**Physics-Guided Synthetic High-Frequency Ultrasound Generation for Skin Layer Segmentation** — [2609.12735](https://arxiv.org/abs/2609.12735) | cross: cs.CV  
  Junkyung ju, Kyungho Yoon, Minwoo Shin  
  High-frequency ultrasound (HFUS) enables noninvasive visualization of superficial skin structures, but automated skin-layer analysis is limited by the scarcity of densely annotated data. Existing real HFUS datasets commonly provide annotations for superficial targets such as the epidermis and subepidermal low-echogenic band (SLEB), while dense labels for deeper structures such as dermis, …
- <a id="20260914-2609.12752"></a>**Optimizing for the decision not the prediction: an exploration of Smooth Net Benefit as a training objective** — [2609.12752](https://arxiv.org/abs/2609.12752)  
  Koen M. F. Gorgels, Lasai Barre\~nada, Maarten van Smeden, Ben Van Calster et al.  
  Objective Prediction models are commonly trained using objectives such as Bernoulli negative log-likelihood (NLL), although downstream clinical decisions may depend on specific risk thresholds. We introduce Smooth Net Benefit ($\sigma$NB), a differentiable approximation of Net Benefit designed to align model training with threshold-specific clinical utility.
- <a id="20260914-2609.12758"></a>**Curriculum-Based Adversarial Heterogeneous Agent Reinforcement Learning for Autonomous Quad-Copter Landing in Maritime Settings** — [2609.12758](https://arxiv.org/abs/2609.12758)  
  Allan Minh-Tam Nguyen, Sree Showrya Kotala, Stefan Banioi-Crijman, Kurt Driessens et al.  
  Recovering unmanned aerial vehicles (UAVs) in maritime environments is challenging due to wind turbulence and ship-deck motion, making it a valuable test case for alternative control and learning approaches as conventional landing approaches often become unreliable. We study simulated mid-air capture of quadrotor UAVs by a ship-mounted robotic arm, learning robust cooperative control policies …
- <a id="20260914-2609.12785"></a>**Convergence of Stochastic Gradient Methods under Heavy-Tailed Noise and H\"{o}lder Smoothness** — [2609.12785](https://arxiv.org/abs/2609.12785) | cross: math.OC, stat.ML  
  Misbah Uz Zaman, Anirbit Mukherjee  
  Classical convergence guarantees for stochastic gradient methods typically assume Lipschitz-smooth objectives and finite-variance gradient noise, both frequently violated in practice. In contrast, we study nonconvex stochastic optimization under the joint relaxation of these assumptions: objectives with $(L,s)$-H\"older continuous gradients, $s\in(0,1]$, and gradient noise satisfying only a …
- <a id="20260914-2609.12793"></a>**VertiFuseX: Generalizable Financial Forecasting via Multi-Stream Temporal Fusion** — [2609.12793](https://arxiv.org/abs/2609.12793) | cross: q-fin.ST  
  Aashish Bohra, Vivek Vijay  
  Stock price prediction remains challenging due to the non-stationary and noisy nature of financial time series. Existing deep learning models often rely on rigid decision-level fusion, ad hoc hyperparameter tuning, and compressed final-layer outputs, causing information loss, overfitting, and limited cross-market generalization.
- <a id="20260914-2609.12863"></a>**GenOR-Twin: A Semantic Middleware for Integrating Operational Discourse with Mathematical Optimization** — [2609.12863](https://arxiv.org/abs/2609.12863)  
  Rahimeh Neamatian Monemi, Shahin Gelareh, Lubin Cui, Nelson Maculan  
  We introduce GenOR-Twin, a neuro-symbolic framework that bridges the translation gap between unstructured operational logs and rigorous mathematical optimization. Our architecture uniquely positions Large Language Models as semantic translators rather than direct solvers, ensuring that the system retains the feasibility guarantees of exact combinatorial methods.
- <a id="20260914-2609.12875"></a>**What an odour descriptor corpus can and cannot measure: valence, attenuation, and the ceiling of the public record** — [2609.12875](https://arxiv.org/abs/2609.12875)  
  Stylianos Kampakis, Fabio Rovai  
  Machine olfaction trains on pooled public descriptor corpora, but whether a shared descriptor word measures the same thing across corpora has not been tested, nor has the ceiling of what any of them can measure. We audit four corpora from Pyrfume.
- <a id="20260914-2609.12891"></a>**Quantifying the Value of Privileged Information Using a PAC-Bayesian Approach** — [2609.12891](https://arxiv.org/abs/2609.12891)  
  Vasily Bokov (aQa, Leiden University, The Netherlands, LIACS et al.  
  In practice, various learning scenarios provide access to auxiliary features exclusively during training. Incorporating such data to enhance model performance gave rise to a paradigm known as Learning Using Privileged Information (LUPI).
- <a id="20260914-2609.12899"></a>**Physical-State-Guided Diffusion Sampling for Full-Waveform Inversion** — [2609.12899](https://arxiv.org/abs/2609.12899)  
  Chen Min, Haowen Jiang, Zheng Ma, Xiongbin Yan  
  Full waveform inversion (FWI) estimates subsurface velocity from seismic recordings, but its ill-posedness and nonlinearity make accurate reconstruction strongly dependent on initialization and prior information. Diffusion posterior sampling provides a learned geological prior, yet directly coupling its denoiser to the nonlinear wave solver can yield unreliable physical guidance.
- <a id="20260914-2609.12903"></a>**Hidden in Rounds: Predicting the Time Cost of 802.11 Contention in Federated Learning** — [2609.12903](https://arxiv.org/abs/2609.12903) | cross: cs.DC  
  Satwat Bashir, Tasos Dagiuklas  
  Federated learning over IEEE~802.11 shares the wireless channel among clients that send model updates. We use ns-3 to measure the frame-delivery ratio and saturation throughput for different client densities and offered loads.
- <a id="20260914-2609.12905"></a>**Offline Reinforcement Learning for Wind Farm Control: A Wind Tunnel Study under Dynamic Wind Directions** — [2609.12905](https://arxiv.org/abs/2609.12905)  
  Yuhan Su, Hongyang Dong, Simone Tamaro, Filippo Campagnolo et al.  
  This paper addresses the wind farm power maximization problem in the presence of wind direction changes. Specifically, a model-free Modified Twin Delayed Deep Deterministic Policy Gradient with Behavior Cloning (MTD3-BC) algorithm is proposed to tackle this task through yaw control under varying wind direction conditions.
- <a id="20260914-2609.12938"></a>**A Large-Scale AIS Dataset from Finnish Water** — [2609.12938](https://arxiv.org/abs/2609.12938)  
  Debayan Bhattacharya, Ikram Ul Haq, Carlos Pichardo Vicencio, Sebastien Lafond  
  This research paper contributes to the maritime research community by introducing a comprehensive AIS dataset from Finnish waters, specifically the Baltic Sea region. AIS data, initially designed for collision prevention, have evolved into a versatile tool with applications across diverse maritime domains.
- <a id="20260914-2609.12991"></a>**Information-Induced Training Geometry: Exact Reduction, Canonical Completion, and Structured Expressivity** — [2609.12991](https://arxiv.org/abs/2609.12991) | cross: math.OC  
  Zavier Li  
  Training data constrains optimizer geometry through the covectors visible to a declared information channel. We study how such partial information determines a full positive cometric relative to a reference and which degrees of freedom remain unidentified.
- <a id="20260914-2609.12994"></a>**Dimension-Corrected Hitting Times for Heavy-Tailed Spectral Emergence in Neural Optimizer Dynamics** — [2609.12994](https://arxiv.org/abs/2609.12994) | cross: cs.NE, stat.ML  
  Zongmin Liu  
  Heavy-tailed empirical spectral densities of neural-network weight matrices are widely used as diagnostics of implicit self-regularization, but the step complexity of heavy-tail emergence remains poorly understood. We formulate spectral heavy-tail formation as a right-censored hitting-time problem: a run that does not reach a heavy-tail diagnostic within the observation horizon is treated as …
- <a id="20260914-2609.12996"></a>**A Full Adam Theorem for Spectral Heavy-Tail Onset** — [2609.12996](https://arxiv.org/abs/2609.12996) | cross: math.PR, stat.ML  
  Zongmin Liu  
  We prove a full Adam theorem for spectral heavy-tail onset in a closed Gaussian Stein-Hermite teacher-student state-evolution model. The theorem begins with the actual full-batch Adam recurrences, derives the population gradient by Stein-Hermite calculus, proves finite-width covariance concentration, converts multi-step Adam momentum into an exact non-centered Gaussian sign kernel, controls the …
- <a id="20260914-2609.13010"></a>**Dual-guided Hierarchical Edge Localization for Large-scale Optimal Transport Across Dimensions** — [2609.13010](https://arxiv.org/abs/2609.13010)  
  Wenzhou Xia, Qiaoqiao Ding, Jingwei Liang, Xiaoqun Zhang  
  Optimal transport (OT) compares distributions and aligns datasets in machine learning, yet unregularized discrete OT requires a linear program with quadratically many transport variables. We propose HELLO, a hierarchical solver that casts large-scale discrete OT as edge localization and uses dual potentials to guide both coarse-to-fine initialization and within-level refinement.
- <a id="20260914-2609.13039"></a>**Transfer Learning for Evolving Domains** — [2609.13039](https://arxiv.org/abs/2609.13039) | cross: stat.ML  
  Ricardo Ribeiro Pereira, Jacopo Bono, Hugo Ferreira, Pedro Ribeiro et al.  
  Transfer learning explores how to leverage knowledge from various tasks or domains (sources) to enhance predictive performance in related tasks or domains (targets). Typically, transfer learning research is segmented into several isolated sub-areas (such as domain generalisation, domain adaptation, or multi-domain learning), each making distinct assumptions about target data availability, namely …
- <a id="20260914-2609.13040"></a>**Quantile-based Loss Filtering for Outlier-Robust Stochastic Gradient Descent** — [2609.13040](https://arxiv.org/abs/2609.13040) | cross: cs.NA, math.NA  
  Jamie Haddock, Anna Ma, Elizaveta Rebrova  
  We study loss-based filtering for finite-sum optimization with a subset of corrupted component functions whose gradients may be highly unreliable. Motivated by minimum-loss-based SGD (min-$k$-loss) and quantile-based methods for corrupted linear systems, we propose and analyze a general loss-filtering framework -- Quantile-\(k\)-Loss SGD (Q\(k\)L-SGD) -- that samples \(k\) component losses at …
- <a id="20260914-2609.13044"></a>**Robust Policy Optimization via Adversarial Importance Sampling** — [2609.13044](https://arxiv.org/abs/2609.13044)  
  Amine Andam, Jamal Bentahar, Mustapha Hedabou  
  Significant progress has been made in safeguarding deep reinforcement learning (DRL) policies against input perturbations. Developing robust DRL involves three main stages: algorithm design, implementation, and evaluation.
- <a id="20260914-2609.13048"></a>**MCRL2: Multi-resource Cross-attention-based Representation Learning-augmented Reinforcement Learning for Cloud Microservice Scheduling** — [2609.13048](https://arxiv.org/abs/2609.13048)  
  Tiangang Li, Shi Ying, Xiangbo Tian, Chuan Shi et al.  
  Efficient microservice scheduling is crucial for maintaining load balance across nodes in data centers and ensuring high quality of service. However, achieving this in practice remains challenging due to dynamic resource imbalance under fluctuating workloads, nonlinear coupling across multiple resource dimensions, and the heterogeneity of microservice resource demands.
- <a id="20260914-2609.13050"></a>**A Unified and Constrained View of Regularization-Based Robust Reinforcement Learning** — [2609.13050](https://arxiv.org/abs/2609.13050)  
  Amine Andam, Jamal Bentahar, Mustapha Hedabou  
  Regularization-based methods have become a standard approach for training Deep Reinforcement Learning policies against adversarial input perturbations. In this paper, we unify these methods by deriving new upper bounds on the performance gap between the nominal and worst-case policies.
- <a id="20260914-2609.13057"></a>**Benign Loss Landscapes Can Coexist with Worst-Case Hardness** — [2609.13057](https://arxiv.org/abs/2609.13057) | cross: stat.ML  
  Zach Furman, Stephan W\"aldchen, Yangda Bei, Liam Hodgkinson  
  Deep neural networks are expressive enough to contain worst-case targets that can be evaluated in polynomial time but cannot be learned in polynomial time by gradient descent. For practical tasks they nonetheless learn well, raising the question of what non-generic structure of real-world targets enables this.
- <a id="20260914-2609.13060"></a>**CanvasAnneal: Curriculum Reinforcement Learning for Diffusion Language Models** — [2609.13060](https://arxiv.org/abs/2609.13060)  
  Blake Olson, Yuhang Song, Emmett McQuinn, Yuan Shangguan  
  Diffusion Language Models (DLMs) offer promising parallel generation capabilities but lag behind autoregressive models in complex reasoning and tool-use tasks. While Reinforcement Learning (RL) has recently been applied to enhance DLMs, standard RL approaches suffer from an exploration bottleneck.
- <a id="20260914-2609.11933"></a>**Towards Sustainable Hydrogen Systems: Supply Chain Optimization with Model Predictive Control and Reinforcement Learning** — [2609.11933](https://arxiv.org/abs/2609.11933) | cross: cs.LG  
  Mahammad Valiyev  
  Hydrogen supply chains are expected to play a central role in future low-carbon energy systems by enabling renewable energy integration, long-duration storage, and decarbonization of industrial and transportation sectors. However, their operation is challenged by renewable generation variability, electricity price fluctuations, uncertain hydrogen demand, and engineering constraints associated …
- _…另有 32 篇, 见 `data/20260914.json`_

#### cs.DB (3)

- <a id="20260914-2609.12535"></a>**QEmbed: A Deep Learning Based Cardinality Estimator for Efficient Query Processing** — [2609.12535](https://arxiv.org/abs/2609.12535)  
  Pooja Rajput, Suman Banerjee  
  Cardinality estimation is at the core of any commercial database system for efficient query processing. Over the decades, non-learning-based estimation techniques (e.g., histogram-based, sampling-based) have been widely used in both commercial and open-source database platforms.
- <a id="20260914-2609.12597"></a>**Invisible Yet Dominant: Big Stalls of Kernel I/O Mechanisms in Cloud OLTP Databases** — [2609.12597](https://arxiv.org/abs/2609.12597) | cross: cs.OS  
  Mitsumasa Kondo  
  Most databases, including PostgreSQL, RocksDB, and recent AI KV-cache middleware, rely on buffered I/O, delegating write-back to the Linux kernel. On the distributed block storage standard in the cloud, this delegation inherits a hidden bottleneck: each device is drained by a single kernel flusher thread over a high-latency, shallow-queue path.
- <a id="20260914-2609.12745"></a>**How Do Data Collection Strategy and Data Quality Influence the Outcomes of Digital Technology Adoption?** — [2609.12745](https://arxiv.org/abs/2609.12745)  
  Xuejiao Li, Cheng Yang  
  In the era of Industry 4.0 (I4.0), data has become the essential foundation for digital transformation, yet many organizations still struggle to link data practices with digital performance outcomes. This study investigates how data collection strategy and data quality jointly influence the success of digital technology adoption (DTA) in manufacturing firms.

#### cs.DC (24)

- <a id="20260914-2609.12091"></a>**Shards on a Shoestring: Empirical Characterization of NEAR Protocol Nightshade Sharding on Commodity Hardware** — [2609.12091](https://arxiv.org/abs/2609.12091) | 🎯★ BFT  
  Sohini Sahukar, Om Amit Gandhi, Ioan Raicu  
  NEAR Protocol's Nightshade architecture targets one million transactions per second (TPS) through horizontal sharding of both state and computation. Published benchmarks were produced on expensive Google Cloud Platform infrastructure costing approximately \$700 per hour, leaving a significant reproducibility gap for academic research.
- <a id="20260914-2609.12143"></a>**Consensus-based Decentralized Distributed Swarm Learning with Heterogeneous Big Data** — [2609.12143](https://arxiv.org/abs/2609.12143) | 🎯★ consensus  
  Zhuoyu Yao, Dong Yang, Yue Wang, Songyang Zhang et al.  
  Artificial intelligence increasingly relies on large-scale, distributed, and heterogeneous data collected by edge devices. However, the practice of edge intelligence remains challenging due to non-convex objectives, data heterogeneity, and complex wireless network topology.
- <a id="20260914-2609.12239"></a>**Specifying Paxos for System Builders: Pseudocode Made Executable** — [2609.12239](https://arxiv.org/abs/2609.12239) | 🎯★ consensus, Paxos  
  Yanhong A. Liu, Rahul Sihag  
  This paper presents a precise executable specification---as a faithful mapping from the pseudocode---of Paxos for System Builders, a practical protocol for replication and consensus in distributed systems. Paxos for System Builders has both a robust implementation in C and a clean pseudocode for critical protocol details.
- <a id="20260914-2609.12551"></a>**RoofLang: Enabling AI-Driven Architecting of LLM Inference Systems** — [2609.12551](https://arxiv.org/abs/2609.12551) | cross: cs.AI  
  Ziyue Yang, Yuting Jiang, Lei Qu, Peng Cheng  
  AI is beginning to make substantive contributions to LLM inference optimization. Existing AI optimizations are predominantly profiling-based.
- <a id="20260914-2609.11936"></a>**One Simple Trick for Improving the Performance of Energy-Limited Local Inference and Training** — [2609.11936](https://arxiv.org/abs/2609.11936) | cross: cs.DC, cs.LG  
  Erik Schultheis, Maximilian Kleinegger, Dan Alistarh  
  Energy supply and heat dissipation are two of the main challenges with modern GPU deployments. While typically discussed in the context of new datacenter constructions, the same constraints also apply to small form-factor consumer devices, such as the DGX spark.
- <a id="20260914-2609.11946"></a>**Hyperion: An AI-powered HPC cluster for sciences and humanities research that utilizes ML for predicting job turnaround time** — [2609.11946](https://arxiv.org/abs/2609.11946) | cross: cs.LG  
  Jun Zhou, Nathan Elgar, Tawnee Benedetto, John Richards et al.  
  Hyperion is an innovative high-performance computing (HPC) cluster developed for researchers in both science and humanities disciplines at the University of South Carolina (USC). Our approach involved constructing a HPC cluster designed to meet the current research needs while accommodating future expansion.
- <a id="20260914-2609.12075"></a>**Efficient Vision-Language-Action Management and Serving for Robot Factories** — [2609.12075](https://arxiv.org/abs/2609.12075) | cross: cs.AR, cs.LG, cs.PF, cs.RO  
  Dionysios Adamopoulos, Nattapol Chanpaisit, Basel Fakhri, Christina Giannoula  
  Vision-Language-Action (VLA) models show high robotic manipulation capabilities via a two-stage design: a Vision-Language Model (VLM) stage followed by an Action Diffusion Transformer (ADiT) stage. Since robots must meet strict Service-Level Objectives (SLOs) for safety, VLA inference is inherently latency-critical.
- <a id="20260914-2609.12412"></a>**HoliBench: A Cross-Platform Benchmarking and Deployment Toolkit for Foundation Models in CPS-IoT Applications** — [2609.12412](https://arxiv.org/abs/2609.12412) | cross: cs.LG, cs.PF  
  Inesh Chakrabarti, Zejun Xiong, Pragya Sharma, Mani Srivastava  
  Foundation models, including large language models, vision-language models, and time-series foundation models, are increasingly deployed on embedded and edge platforms for CPS and IoT applications, where energy, latency, and memory are as critical as task accuracy. Existing benchmarking tools evaluate model capability in isolation, reporting accuracy assuming sufficient compute, while hardware …
- <a id="20260914-2609.12923"></a>**Dissecting GPU Utilization for LLM Inference on Nvidia Hopper** — [2609.12923](https://arxiv.org/abs/2609.12923) | cross: cs.AR, cs.DC, cs.LG  
  Mohammad Siavashi, Gerald Q. Maguire Jr., Dejan Kostic, Marco Chiesa  
  A single SM utilization percentage can make an LLM inference workload look compute-saturated while hiding how much useful work is being done. The problem is not that the counter is wrong, but that it collapses several different mechanisms into one number.
- <a id="20260914-2609.11944"></a>**Asynchronous Parallel Search for Exact Multi-Objective Shortest Paths with Versioned Frontier Snapshots and Indexed Dominance Pruning** — [2609.11944](https://arxiv.org/abs/2609.11944)  
  Xiaoqing Xu, Ning Zhang, Liuyihui Qian, Xiaojun Liu et al.  
  Exact multi-objective shortest-path (MOSP) search computes the complete Pareto set between specified start and goal vertices, and its computational cost can grow rapidly with expanding nondominated label sets and frequent dominance tests over per-vertex Pareto frontiers. Efficiently parallelizing exact MOSP remains an open challenge.
- <a id="20260914-2609.12299"></a>**Argus: Orchestrating Cross-Layer GPU Performance Measurements around Semantic Regions** — [2609.12299](https://arxiv.org/abs/2609.12299) | cross: cs.PF  
  Jianzhu Yao, Yue Guan, Srivatsan Ramesh, Yuanwei Fang et al.  
  GPU developers and automated optimizers need performance evidence for semantic code regions--such as neural-network operator implementations and pipeline stages--but this evidence is fragmented across profiling tools. Answering a region-level question can require manually constructing probes and program variants, isolating interfering measurements, and mapping evidence to regions and execution …
- <a id="20260914-2609.12330"></a>**Unleashing the Power of Equality Saturation for Tensor Program Superoptimization** — [2609.12330](https://arxiv.org/abs/2609.12330)  
  Qi Zhan, Xing Hu, Xin Xia, Shanping Li  
  Efficient GPU implementations of tensor programs often require joint optimization of high-level algebraic formulations and low-level execution strategies. However, the resulting search space grows rapidly as transformations combine across operators, making joint optimization difficult to scale.
- <a id="20260914-2609.12379"></a>**ForgeMegakernel: A General Framework for Efficient Auto-Regressive Model Decode Megakernels** — [2609.12379](https://arxiv.org/abs/2609.12379)  
  Leshan Li, Zhui Zhu, Xianglong Deng, Yaojian Chen et al.  
  Auto-regressive model decode is bandwidth-bound, since every weight and key/value-cache byte crosses high-bandwidth memory once per token. A megakernel is an ideal solution, but existing automatic megakernel generation approaches cannot achieve both generalization across models and correctness guarantees.
- <a id="20260914-2609.12449"></a>**HeatCache: Thermal-aware Energy-efficient LLM Inference Scheduling for Chassis-level Liquid Cooling in Sustainable Edge Server Rooms** — [2609.12449](https://arxiv.org/abs/2609.12449) | cross: cs.PF, cs.SY, eess.SY  
  Rui Lu, Huanghuang Liang, Kaiqi Guan, Dan Wang  
  LLM inference is increasingly deployed at institution-scale edges to meet service requirements. However, multi-GPU inference consumes a large amount of electricity and produces substantial heat.
- <a id="20260914-2609.12602"></a>**GreenDirector: carbon- and water-aware workload placement for sustainable computing** — [2609.12602](https://arxiv.org/abs/2609.12602)  
  Jime Iglesias Blanco, Ignacio Heredia, Mar\'ia Castrillo, Andrei Tsaregorodtsev et al.  
  The rapid growth of data center electricity demand, accelerated by AI, makes carbon-only accounting an incomplete measure of computing's environmental impact: low-carbon electricity mixes are often water-intensive, and the resulting harm depends on local, seasonal scarcity rather than on the volume of water consumed. We propose the Environmental Score (ES), a unified, dimensionless index in $[0, …
- <a id="20260914-2609.12975"></a>**A Dynamic Vertical Scaling Strategy for Distributed Stream Processing Applications in Edge Computing** — [2609.12975](https://arxiv.org/abs/2609.12975)  
  Guilherme Hiago Costa dos Santos, Carlos Henrique Kayser, Tiago Coelho Ferreto  
  Distributed Stream Processing applications at the edge must reconcile low latency and high throughput with limited and heterogeneous resources. This paper presents a dynamic vertical scaling strategy based on Proximal Policy Optimization, formulated as a Partially Observable Markov Decision Process.
- <a id="20260914-2609.11932"></a>**Throughput per Megabyte: A Pilot Benchmark of Language-Stack Efficiency for Self-Hosted HTTP Services on a Raspberry Pi 5** — [2609.11932](https://arxiv.org/abs/2609.11932) | cross: cs.DC, cs.PL  
  William Oliveira  
  Cloud-centric web benchmarks miss constraints that matter for self-hosted services on ARM64 single-board computers, especially idle RAM footprint and energy per request. We ran a pilot benchmark on one Raspberry Pi 5, measuring equivalent SQLite-backed CRUD APIs implemented in Go 1.26/net/http, Rust 1.95/Axum, Python 3.13/FastAPI+Granian, Node.js 24/Fastify, and .NET 10 Native AOT across N=50 …
- <a id="20260914-2609.11938"></a>**Hardware-Attributed Operator Profiling for PyTorch** — [2609.11938](https://arxiv.org/abs/2609.11938) | cross: cs.DC, cs.PF  
  Logan Chu, Dong Li  
  Framework profilers expose operator timing without hardware counters; GPU profilers expose hardware counters without operator attribution. Bridging this gap manually is error-prone and does not scale.
- <a id="20260914-2609.11939"></a>**Adaptive AI: Energy Efficient Multi-exit TinyML on Intelligent Vision Systems at the Edge** — [2609.11939](https://arxiv.org/abs/2609.11939) | cross: cs.CV, cs.DC  
  Luca Crupi, Lorenzo Lamberti, Alessandro Giusti, Daniele Palossi  
  Traditional TinyML systems for edge devices achieve high accuracy by relying on fixed-depth models that require a constant number of multiply-accumulate (MAC) operations regardless of the input complexity. This approach wastes critical resources in battery-powered Internet-of-Things (IoT) devices and limits the real-time performance of edge cyber-physical systems.
- <a id="20260914-2609.12582"></a>**NovaFabric: Tamper-Evident, Replayable Evidence for Autonomous AI Agent Runs** — [2609.12582](https://arxiv.org/abs/2609.12582) | cross: cs.DC  
  Mohsen Seyedkazemi Ardebili  
  When an autonomous AI agent does something consequential, what can be proven about what it did? Agent-observability platforms capture traces, but a trace is mutable: alterable undetected, with no recipe for re-executing it, silent on whether captured secrets were removed.
- <a id="20260914-2609.12605"></a>**A Feature-Rich Embedded NIDS with eBPF/XDP: Detector and Architecture Trade-offs** — [2609.12605](https://arxiv.org/abs/2609.12605) | cross: cs.DC, cs.NI  
  Shiqi Wu, Oleksii Koshovyi, Georgios Pseiridis Pseiras, Victor Morel et al.  
  Distributed Denial-of-Service (DDoS) attacks remain a serious threat to transport networks, with recent attack volumes exceeding 30 Tbps, and the telecommunications industry being the main target. Recent work has yet to study the impact of the hosting software architecture on network monitoring solutions, or to assess recent algorithms for improving attack detection.
- <a id="20260914-2609.12649"></a>**Hybrid Monitoring for Early Fault Detection in Cloud-Native 5G Systems** — [2609.12649](https://arxiv.org/abs/2609.12649) | cross: cs.DC  
  Anton Andersson, Sai Akshara Naineni, Mats Jansborg, Yixing Zhang et al.  
  This paper presents the design implementation and evaluation of NetMon a hybrid network monitoring system designed for Kubernetes-based 5G packet core deployments specifically evaluated on Ericssons Access and Mobility Management Function AMF clusters NetMon combines eBPF-based passive kernel-level traffic observation with active TCP probing and centralized correlation to detect and localize …
- <a id="20260914-2609.13064"></a>**NFT-Based Reward Mechanisms: Sybil Farming, Vesting, and Stochastic Verification** — [2609.13064](https://arxiv.org/abs/2609.13064) | cross: cs.DC, cs.GT  
  Marco Alberto Javarone, Stefanos Leonardos, Carmine Ventre  
  We study NFT-based reward mechanisms in which a user can create multiple identities and submit fraudulent claims that mature a reward subject to vesting. We assume that the issuer stochastically verifies claims during the vesting period and that identities can be linked into clusters so that the detection of one identity submitting a fraudulent claim causes the whole cluster to be forfeited …
- <a id="20260914-2609.13115"></a>**Extreme-Scale Linear-Scaling Kohn-Sham DFT at 100 Million Atoms: Bridging Quantum Simulations and Experiments** — [2609.13115](https://arxiv.org/abs/2609.13115) | cross: cs.DC, physics.comp-ph  
  Qimen Xu, Yu Zhang, Dixing Ni, Lei Gao et al.  
  Kohn-Sham density functional theory (DFT) remains the workhorse of ab initio materials simulation, yet cubic computational and quadratic memory scaling have confined calculations to a few hundred to thousands of atoms, spanning only nanometers, far below experimentally relevant length scales. We introduce XLSDFT, a linear-scaling DFT framework based on divide-and-conquer decomposition of the …

#### cs.FL (2)

- <a id="20260914-2609.12106"></a>**A Non-constant Lower Bound for Grammar-Based Compression with Greedy** — [2609.12106](https://arxiv.org/abs/2609.12106) | cross: cs.FL | 🎯★ formally verified | 🎯🧐 formally verified  
  Danny Hucke  
  We prove a lower bound of {\Omega}(log n/ log log n) on the approximation ratio of the global grammar-based compression algorithm Greedy. To our knowledge, the previously best lower bound was a constant, and the existence of a nonconstant lower bound had remained open for more than twenty years.
- <a id="20260914-2609.12209"></a>**Stochastic Hybrid Automata for Power Profile Modeling in Energy Systems** — [2609.12209](https://arxiv.org/abs/2609.12209)  
  Lisa Willemsen, Anne Remke, Johann L. Hurink  
  Power profiles are widely used to describe power demand and production in energy systems. Yet, real-world usage often involves uncertainty, making it challenging to determine, e.g., whether a battery can reliably meet a given profile.

#### cs.LO (1)

- <a id="20260914-2609.12715"></a>**Supermartingale Certificates for Parametric MDPs** — [2609.12715](https://arxiv.org/abs/2609.12715) | cross: cs.AI, cs.SY, eess.SY | 🎯★ formal verification  
  Kaushik Mallik, {\DH}or{\dj}e \v{Z}ikeli\'c  
  We consider the problems of formal verification and synthesis in parametric Markov decision processes (MDPs) with general measurable state and action spaces. The heart of our approach is a parameter flattening transformation, which allows us to transform parametric MDPs into semantically equivalent non-parametric MDPs.

#### cs.SE (27)

- <a id="20260914-2609.10630"></a>**AI Safety: Not Optional, Not Later** — [2609.10630](https://arxiv.org/abs/2609.10630) | cross: cs.AI  
  Qinghua Lu, Yoshua Bengio  
  Incidents show that AI safety failures often arise across multiple layers. We present a safety-by-design assurance architecture combining model-level supervision, such as Scientist AI, with system-level controls over scaffolds and harnesses, independent verification, monitoring, and evidence infrastructure, supported by governance for accountability and evidence interoperability.
- <a id="20260914-2609.11559"></a>**PRISMA-LLM: An Empirical Reporting Framework for AI-Assisted Systematic Reviews** — [2609.11559](https://arxiv.org/abs/2609.11559) | cross: cs.AI, cs.CL  
  Miguel Zabaleta, Baihan Lin  
  Large language models (LLMs) and AI-enabled software increasingly participate in systematic-review decisions, yet the information needed to audit these workflows is reported inconsistently. We analyze SciLitBench, a corpus of 888 review-automation papers with 14,726 annotations, to characterize changes in methods, review-stage use, evaluation and reported limitations.
- <a id="20260914-2609.12017"></a>**When Agent Metrics Measure Different Things: An Evidence-Grounded Audit of the Praxa AI Pipeline** — [2609.12017](https://arxiv.org/abs/2609.12017) | cross: cs.AI  
  Stefan G. Creadore, Peyton Woakz  
  Agent evaluations can be numerically correct while measuring a different construct from the one implied by their labels. We present a retrospective measurement audit of selected Praxa AI implementation files, historical evaluation artifacts, and operational records.
- <a id="20260914-2609.12039"></a>**Reality Is the Final Verifier: On Two Key Gaps in Agentic Software Engineering** — [2609.12039](https://arxiv.org/abs/2609.12039) | cross: cs.AI  
  Alexander Krentsel, Shubham Agarwal, Mert Cemri, Shu Liu et al.  
  Software development follows an implementation-verification loop in which developers or agents iteratively revise an implementation until an evaluator, such as a test suite, accepts it. The evaluator checks the implementation against a set of requirements under a model of the deployment environment.
- <a id="20260914-2609.12156"></a>**A decision-basis contract for auditable LLM-assisted medical billing verification: deterministic rules, verbatim evidence, and fail-closed abstention** — [2609.12156](https://arxiv.org/abs/2609.12156) | cross: cs.AI  
  Jan H\"olter, Kevin Geis, Benjamin Raab, Boris Bauke  
  This work presents a proof of concept for auditable LLM-assisted medical billing verification based on a decision-basis contract. The contract separates deterministic checks of versioned fee-catalog rules from LLM-based assessment of free-text documentation.
- <a id="20260914-2609.12190"></a>**Retrieval-Augmented Generation for Scientific Code Understanding** — [2609.12190](https://arxiv.org/abs/2609.12190) | cross: cs.AI  
  Aaron Nobile, Andreas Adelmann, Mohsen Sadr  
  Large language models have become central to modern coding assistants, but state-of-the-art systems such as Claude Code or Codex rely on very large, cloud-hosted models with significant computational cost and data-privacy implications. This work investigates whether a useful, fully local coding agent can be built around small open-source models by shifting the computational burden away from …
- <a id="20260914-2609.12231"></a>**Learning to adapt GR(1) specifications through degradation** — [2609.12231](https://arxiv.org/abs/2609.12231) | cross: cs.AI, cs.LO  
  Tiberiu-Andrei Georgescu, Dalal Alrajeh, Sebastian Uchitel  
  Reactive synthesis is a powerful tool for generating correct-by-construction controllers from formal specifications. GR(1) is an assume-guarantee specification framework that enables efficient synthesis, allowing synthesised controllers to be used in a wide array of applications.
- <a id="20260914-2609.12656"></a>**Separating Engineering Reasoning from DEXPI Serialization in LLM-Based Greenfield Surface-Process Design: A Three-Case Study for Underground Gas Storage** — [2609.12656](https://arxiv.org/abs/2609.12656) | cross: cs.AI  
  Qingchuan Zhu, Shuyue Tong, Pengju Ren  
  Large language models can produce engineering descriptions and structured process representations, but standards-level serialization can substantially increase the generation burden. This diagnostic study examines whether separating engineering reasoning from Data Exchange in the Process Industry (DEXPI) serialization changes where representation and engineering failures occur in constrained …
- <a id="20260914-2609.12708"></a>**What is the Difference Between Me and You? Benchmarking the Quality Gap Between Human-Written and AI-Generated Code** — [2609.12708](https://arxiv.org/abs/2609.12708) | cross: cs.AI  
  Cristina Improta, Pietro Liguori, Domenico Cotroneo  
  AI coding assistants are becoming co-authors of production software, yet their evaluation centers on functional correctness, leaving open whether their code differs from human code in the quality dimensions dominating lifecycle cost. We compare human-written and AI-generated code at scale: 787,562 function pairs across Python, Java, and C, each human function mined from open-source repositories …
- <a id="20260914-2609.12757"></a>**GraphAHA: Graph-Based Adaptive Search with Heterogeneous Actions for Test-Time Code Generation** — [2609.12757](https://arxiv.org/abs/2609.12757) | cross: cs.AI  
  Xitao Li, Haijun Wang, Gege Yuan, Qiyuan Wu et al.  
  Test-time scaling improves code generation by spending additional inference budget (e.g., calls or tokens) on direct sampling, feedback-conditioned repair, and reasoning-guided implementation. Search-based methods can allocate this budget adaptively, but two challenges remain.
- <a id="20260914-2609.13071"></a>**Involving before Evolving: A Vision for Trustworthy Enterprise Digital Twin Engineering** — [2609.13071](https://arxiv.org/abs/2609.13071) | cross: cs.AI, cs.HC  
  K\'erian Fiter, Adil Lagrou, Franck Dervault, Bentley Oakes  
  Enterprise Digital Twins (EDTs) promise data-driven decision support at organizational scale, but realizing them requires navigating siloed departments, tacit knowledge, and high-stakes decisions with long-horizon consequences. Existing approaches involve domain experts during model development but focus less on early organizational buy-in in EDTs.
- <a id="20260914-2609.11941"></a>**A Case-Bundle Operating Model for Coding Agents in OpenFOAM-Based CFD** — [2609.11941](https://arxiv.org/abs/2609.11941) | cross: cs.CE, cs.DC  
  Ke Xiao, Han Li, Teng Zhang, Yangchen Xu et al.  
  General-purpose coding agents can set up computational fluid dynamics (CFD) cases, execute solvers, and manage remote jobs. Reviewable and reusable work additionally depends on persistent engineering context and evidence.
- <a id="20260914-2609.11999"></a>**Is Bash All You Need? An Empirical Study of Tool Interfaces for Enterprise Digital Worker Agents** — [2609.11999](https://arxiv.org/abs/2609.11999) | cross: cs.CL  
  Hazel Mak, Susheel Suresh, Sahil Bhatnagar, Barry Wang et al.  
  In this study, we examine whether a general shell can outperform specialized tools on enterprise tasks. Shell-based agents have shown strong results in coding, but enterprise work also involves moving between applications and services, coordinating with coworkers, and performing professional analysis.
- <a id="20260914-2609.12008"></a>**Investigating Developer-Reported Software Security Testing Challenges** — [2609.12008](https://arxiv.org/abs/2609.12008) | cross: cs.CR  
  Md Erfan, Ahmed Ryan, Md Rayhanur Rahman  
  Software security testing (SST) is essential for identifying vulnerabilities and improving software security, but developers often face practical challenges when selecting tools, configuring test environments, interpreting scanner outputs, testing authentication workflows, and acting on reported vulnerabilities. This study empirically characterizes developer-reported SST challenges in Stack …
- <a id="20260914-2609.12012"></a>**Test-Driven Approaches to Software Engineering with Large Language Models: A Survey of Phases, Tasks, and Agent Skills** — [2609.12012](https://arxiv.org/abs/2609.12012)  
  Yunhao Liang, Chengguang Gan, Ruixuan Ying, Hanjun Wei et al.  
  Tests increasingly participate in the decisions made by large language models and software engineering agents. They specify intended behavior, guide program construction and repair, select candidates, constrain transformations, and provide execution evidence for software analysis.
- <a id="20260914-2609.12131"></a>**Missing Dimensions: Integrating Human and Social Systems into Digital Twin Engineering** — [2609.12131](https://arxiv.org/abs/2609.12131)  
  Francis Bordeleau, Mark van den Brand  
  Digital twins (DTs) have emerged as a key technology at the core of digital transformation, yet their engineering practice remains too narrowly focused on engineered and natural systems. This paper argues that four system dimensions must be explicitly recognized in DT engineering: Engineered, Natural/Biological, Human, and Social.
- <a id="20260914-2609.12236"></a>**Open Source Stewardship Communities: "We need you, but not your pull request"** — [2609.12236](https://arxiv.org/abs/2609.12236)  
  Gregorio Robles, Daniel M. German  
  Human-centric AI for software engineering means keeping humans responsible for work performed with AI. In Open Source Software (OSS), AI lowers the cost of implementing changes, but reviewing someone else's contribution remains comparatively expensive, so some projects now restrict who may contribute implementations while still welcoming other participation---not because the code is AI-generated, …
- <a id="20260914-2609.12309"></a>**PQLS: A High-Performance Python Library for Steady-State Simulation of Open Quantum Systems** — [2609.12309](https://arxiv.org/abs/2609.12309)  
  Evan Simanovskis, Raviraj Adve, Javane Rostampoor  
  PQLS (Parallel Quantum Liouvillian Solver) is a high-performance Python library for computing steady-state solutions of the Lindblad master equation. It provides a layered user-facing API with three levels of abstraction.
- <a id="20260914-2609.12457"></a>**Hieronym: Leveraging Hierarchical Multi-Source Information for Function Renaming in Stripped Binary** — [2609.12457](https://arxiv.org/abs/2609.12457)  
  Xiaoling Zhang, Jian Sun, Dawei Wang, Chongyu Wang et al.  
  Function renaming in stripped binaries can substantially assist reverse engineers by improving code readability, yet it is a challenging task. The difficulty stems from the need to accurately capture function semantics from low-level binary code across diverse instruction sets, architectures, and compiler optimizations, and to express these semantics in concise, human-readable names.
- <a id="20260914-2609.12576"></a>**A Retrieval-Augmented Automated Stakeholder for Requirements Elicitation Education: A Comparative Study** — [2609.12576](https://arxiv.org/abs/2609.12576)  
  Manal Binkhonain, Ohoud Mosa Alharbi  
  Developing the skills required for requirements engineering students to conduct effective requirements elicitation interviews is critical yet challenging, as it requires the development of soft skills in addition to technical knowledge. Role-playing is widely adopted in requirements engineering education to support the development of these skills but is often constrained by time and resource …
- <a id="20260914-2609.12770"></a>**Detecting HTTP Status Code Misuses in REST APIs via Static and Dynamic Analysis** — [2609.12770](https://arxiv.org/abs/2609.12770)  
  Alix Decrop, Andrea Arcuri, Mike Papadakis, Pierre-Yves Schobbens et al.  
  REST APIs are widely used on the web for client-server communications. As REST is based on HTTP, server responses contain status codes to indicate the outcome of requests (e.g., 200 OK for a success and 404 Not Found for an unavailable resource).
- <a id="20260914-2609.12921"></a>**Intelligent Semantic Matching (ISM) for Video Tutorial Search using Transformer Models** — [2609.12921](https://arxiv.org/abs/2609.12921)  
  Ahmad J. Tayeb, Sonia Haiduc  
  The rise in the number and diversity of available software development video tutorials has enhanced digital learning for developers but also introduced challenges in locating relevant content efficiently. Existing video search methods, including keyword-based approaches and tools like CodeTube and TechTube, rely primarily on retrieval algorithms such as BM25, which fail to capture the semantic …
- <a id="20260914-2609.13089"></a>**Beyond Establishing the Four-Day Workweek: Understanding Adaptation and Long-Term Survival in an Agile Software Organization** — [2609.13089](https://arxiv.org/abs/2609.13089)  
  Michael Neumann, Darja \v{S}mite  
  Context: Existing research on the four-day workweek (4DWW) has primarily examined its introduction and short-term effects, with limited understanding of its long-term survival or its interaction with agile software development. Objective: We study how a reduced-hour 4DWW is introduced, adapted, institutionalized, and sustained under changing organizational and external conditions in an agile …
- <a id="20260914-2609.11931"></a>**MaRDMO: FAIR Documentation of In-Silico Research** — [2609.11931](https://arxiv.org/abs/2609.11931) | cross: cs.SE  
  Marco Reidelbach, Marcus Weber  
  MaRDMO is a plugin for the Research Data Management Organiser (RDMO) that enables the structured, FAIR-compliant documentation and discovery of mathematical research data. By embedding mathematics-specific questionnaires into a widely used data management plan tool, MaRDMO lowers the barrier to contributing and querying the MaRDI Knowledge Graph for researchers across all disciplines.
- <a id="20260914-2609.12001"></a>**Scan the Skill, Govern the Action: Composing Registry Verdicts with Runtime Consequence Control** — [2609.12001](https://arxiv.org/abs/2609.12001) | cross: cs.SE  
  Rohit Taneja, Travis Weber  
  Agent skill registries screen what they publish. OpenClaw's security team reported that its scanners overlap on at most 10.4% of combined positives, and 81.9% of flagged skills are caught by one scanner alone.
- <a id="20260914-2609.12127"></a>**Local Edits, Global Ripples: Replay-Informed Policy Adaptation for Workflow Synthesis** — [2609.12127](https://arxiv.org/abs/2609.12127) | cross: cs.SE  
  Manqing Mao, Hong Wang, Samson Koelle, Jie Yuan et al.  
  Prompt-policy editing offers a practical way to improve agents that synthesize executable workflows without updating the underlying model. However, persistent prompt editing has two coupled properties.
- <a id="20260914-2609.12292"></a>**Mission Performance: Automatic and Adaptive Race Pace Progression for Autonomous Racing** — [2609.12292](https://arxiv.org/abs/2609.12292) | cross: cs.SE, cs.SY, eess.SY  
  Giovanni Lambertini, Matteo Pini, Nicola Musiu, Ayoub Raji et al.  
  In this paper, we describe the Mission Performance module implemented for a fully autonomous racing car to automatically manage the longitudinal, lateral, and combined performances, aiming to speedup the laptime progression while assuring safety. Motivated by the difficulty and risks of applying the real-time estimation of the grip to critical modules like the motion planner and controller, the …

<!-- END 20260914 -->

<!-- BEGIN 20260729 -->
## 20260729

时间窗口(UTC): 2026-07-28 10:31 → 2026-07-29 10:31 | 去重后共 **128** 篇

### 📌 重点关注(基于研究兴趣, agent 填写)

> 兴趣画像(hengxin.github.io): 数据库系统(事务隔离级别检测/可串行化验证/黑盒检测)、分布式计算(一致性/CRDT/共识/BFT/复制)、形式化方法(TLA+/模型检测/定理证明/不变式推断+LLM)。

| 推荐 | 论文 | 理由 |
|------|------|------|
| ★★★★★ | **Hermes: Low Tail-Latency Via Prefix Consensus** — [2607.25916](https://arxiv.org/abs/2607.25916) · [📄](#20260729-2607.25916) (cs.DC) | Malkhi 团队新作: 以 prefix consensus 化解 leader-based BFT 的超时两难(保守超时=长停顿, 激进超时=误废视图), 直击共识/BFT 核心兴趣; 已下载 |
| ★★★★ | **Verification of Provers and Solvers** — [2607.25793](https://arxiv.org/abs/2607.25793) · [📄](#20260729-2607.25793) (cs.LO) | Thiemann 综述: SAT/SMT/定理证明器与证明助手的 certification vs. verification 两条路线对比, 与可信求解器/证书检查兴趣高度相关; 已下载 |
| ★★★ | **dtControl2+ε: Trading Optimality for Explainability in MDPs via Decision Trees** — [2607.25925](https://arxiv.org/abs/2607.25925) · [📄](#20260729-2607.25925) (cs.AI) | Křetínský 组: 用决策树表示 MDP 控制器, 在最优性与可解释性间做量化权衡, 概率模型检测方向; 已下载 |
| ★★★ | **Input Relation Prompting for Metamorphic Testing on Query-Based Systems** — [2607.25603](https://arxiv.org/abs/2607.25603) · [📄](#20260729-2607.25603) (cs.SE) | 面向查询系统(无 ground truth)的蜕变测试关系识别, 与 DBMS 黑盒测试方法论互补; 已下载 |
| ★★★ | **Demystifying Deep Learning Compiler Frontend Bugs: An LLM-Aided Empirical Study** — [2607.25651](https://arxiv.org/abs/2607.25651) · [📄](#20260729-2607.25651) (cs.PL) | DL 编译器前端 bug 实证研究(LLM 辅助), 系统测试/编译器可靠性视角; 已下载 |

### 🧐 视野扩展(agent 填写)

| 推荐 | 论文 | 理由 |
|------|------|------|
| 🧐🧐🧐🧐🧐 | **MemLens: A Value-Aware Memory Management System with Interactive Analytics for LLM-based Agents** — [2607.25992](https://arxiv.org/abs/2607.25992) · [📄](#20260729-2607.25992) (cs.DB) | "agent 记忆"正在变成一类新的数据管理基础设施 — 数据库社区切入 LLM agent 的绝佳样本; 已下载 |
| 🧐🧐🧐🧐 | **Reinforcement Learning for Code Optimization** — [2607.25970](https://arxiv.org/abs/2607.25970) · [📄](#20260729-2607.25970) (cs.LG) | 从"RL 保证正确性"到"RL 优化性能"的延伸及其 reward 设计陷阱, 对程序优化+学习交叉方向的入门观察; 已下载 |
| 🧐🧐🧐 | **Combinatorial structures connecting Latin squares and bireversible automata** — [2607.26013](https://arxiv.org/abs/2607.26013) · [📄](#20260729-2607.26013) (cs.FL) | 拉丁方与双可逆自动机的组合对应, 自动机理论的另类几何视角; 已下载 |
| 🧐🧐🧐 | **The Internal Modal Logic of Forcing** — [2607.25977](https://arxiv.org/abs/2607.25977) · [📄](#20260729-2607.25977) (math.LO) | 模态逻辑 × 布尔值模型/力迫法: 逻辑基础方向的跨界阅读; 已下载 |
| 🧐🧐 | **Kernel-Checked Exclusions for the Erdős-Selfridge Odd Covering Problem** — [2607.25628](https://arxiv.org/abs/2607.25628) · [📄](#20260729-2607.25628) (cs.LO) | 机器可检验证书攻击 Erdős 覆盖系统问题, 与收藏中"计算机辅助证明/趣味复杂性"一脉相承; 已下载 |

### 分类清单

#### math.LO (2)

- <a id="20260729-2607.25979"></a>**Carrier ideals, tail obstructions, and remainder traces for ladder-system spaces** — [2607.25979](https://arxiv.org/abs/2607.25979) | cross: math.GN  
  Xing-Yu Hu  
  For a ladder-system space $X_L$ with carrier $S\subseteq E^{ω_1}_ω$, the finite-label uniformization property $M_{<ω}$ characterizes countable metacompactness, and countable metacompactness is equivalent to the $Δ$-property. Both equivalences are known for stationary carriers.
- <a id="20260729-2607.25977"></a>**The Internal Modal Logic of Forcing** — [2607.25977](https://arxiv.org/abs/2607.25977)  
  Santiago Jockwich, Sourav Tarafder, Giorgio Venturi  
  We connect modal set theory with Boolean-valued models by developing an \emph{internal} Kripke semantics for modal formulas whose atomic propositions are set-theoretic sentences. Given a complete Boolean algebra $B$, we view its elements as ``local perspectives on truth'' inside the Boolean-valued universe $V^{(B)}$ and interpret the modal operators using an accessibility relation $R$ on $B$ …

#### cs.AI (65)

- <a id="20260729-2607.26057"></a>**Pass the Baton: Trajectory-Relayed On-Policy Distillation** — [2607.26057](https://arxiv.org/abs/2607.26057) | cross: cs.AI  
  Haolei Xu, Xiaowen Xu, Haiwen Hong, Zixuan Ni et al.  
  On-policy distillation (OPD) grounds token-level supervision in the student's own trajectory, yet suffers from prefix failure: once the student commits to a wrong reasoning direction, all subsequent generation builds on this deviation, producing misdirected continuations that elicit unreliable supervision and waste compute. We identify a teacher-student continuation asymmetry on failed prefixes, …
- <a id="20260729-2607.26055"></a>**$π\mathbf{R}^2$: Reactive Real-time Flow Policies** — [2607.26055](https://arxiv.org/abs/2607.26055) | cross: cs.AI, cs.LG  
  Sungjae Park, Shubham Tulsiani  
  Generalist manipulation policies increasingly take the form of action-chunking flow policies built on large pretrained backbones. Such chunks run open-loop, so the policy cannot react to sensory input arriving mid-execution, sacrificing \emph{reactivity}.
- <a id="20260729-2607.26041"></a>**Desktop-Delta Bench: Do Computer-Use Models Understand Desktop GUI Transitions?** — [2607.26041](https://arxiv.org/abs/2607.26041) | cross: cs.CV  
  Abhishek Pillai, Samir Kumar Nayak, Yuan Chen  
  Computer-use agents (CUAs) increasingly act through desktop GUIs to complete long-horizon tasks. Current benchmarks primarily measure end-task success or single-frame grounding.
- <a id="20260729-2607.26034"></a>**Falling Behind Drives Unsafe Development in an Idealised AI Race Experiment** — [2607.26034](https://arxiv.org/abs/2607.26034) | cross: cs.CY, cs.GT, econ.GN  
  Elias Fernández Domingos, The Anh Han  
  Technological races create tension between speed and safety: actors may gain by moving faster than competitors, even when risky development is harmful. This is prominent in debates about artificial intelligence (AI), where competitive pressure is often argued to incentivise riskier, less safety-conscious development.
- <a id="20260729-2607.26023"></a>**CHARM: A Multimodal Graph Foundation Model with Hierarchical Context Modeling for Zero-Shot Transfer** — [2607.26023](https://arxiv.org/abs/2607.26023)  
  Ankang Yang, Jitao Zhao, Di Jin, Yuxiao Huang et al.  
  Graph foundation models (GFMs) have emerged as a promising paradigm for transferring knowledge across graph domains and tasks. Real-world graphs associate nodes with text, images, and other modalities, making multimodal graphs essential for representing complex entities and relations.
- <a id="20260729-2607.26016"></a>**MDTransformer: A Hardware-Software Co-Design of Mode-Division Photonic Transformer Accelerator with Inverse-Designed Coherent Crossbar** — [2607.26016](https://arxiv.org/abs/2607.26016) | cross: cs.AI, cs.DC  
  Solomon Micheal Serunjogi, Rachmad Vidya Wicaksana Putra, Ayat Taha, Muhammad Shafique et al.  
  Recently, photonic transformer accelerators (PTAs) have successfully achieved significant speedup and energy efficiency improvements over electronic accelerators for expediting Transformer inference. However, state-of-the-art rely on expensive multi-wavelength light generation and large dot-product units due to active phase-shifter components, thus making their approach inefficient and …
- <a id="20260729-2607.26005"></a>**Pictura: Perspective-View Self-Play at Scale for Driving** — [2607.26005](https://arxiv.org/abs/2607.26005) | cross: cs.AI, cs.RO  
  Yuan Yin, Elias Ramzi, Marc Lafon, Valentin Charraut et al.  
  Self-play in simulation produces robust driving policies at scale. Demonstrations of such behavior have been made using privileged vectorized observations such as exact poses and velocities, even for occluded agents.
- <a id="20260729-2607.25995"></a>**Does Runtime Topology Context Improve LLM-Generated Kubernetes Security Patches?** — [2607.25995](https://arxiv.org/abs/2607.25995) | cross: cs.AI  
  Farooq Shaikh  
  Kubernetes is central to the cloud-native ecosystem, orchestrating containerised workloads. Recent work suggests that large language models (LLMs) can automate cluster security remediation, generating configuration patches from Kubernetes Security Posture Management (KSPM) findings without human authoring.
- <a id="20260729-2607.25961"></a>**Knowledge-Guided Multimodal Reasoning over Interacting Streams for Video-Level Ambivalence and Hesitancy Recognition** — [2607.25961](https://arxiv.org/abs/2607.25961) | cross: cs.AI  
  Podakanti Satyajith Chary, Barath Parthiban, Pranesh Velmurugan, Adeeba Khan et al.  
  Ambivalence and hesitancy (A/H) are conflicting affective states that precede the delay or abandonment of health behaviour change. Recognition of A/H at the video level is difficult, since the signal arises from disagreement across and within facial, vocal, linguistic, and bodily modalities, and manifests differently across individuals.
- <a id="20260729-2607.25959"></a>**Detecting Knowledge Inconsistencies Across Text, Tables, and Knowledge Graphs** — [2607.25959](https://arxiv.org/abs/2607.25959) | cross: cs.AI  
  Fanfu Wei, Thibault Ehrhart, Raphaël Troncy  
  Wikipedia and Wikidata are widely used for information access, LLM pre-training, and retrieval-augmented generation. Their knowledge is deeply connected but scattered across text, tables, and knowledge graphs.
- <a id="20260729-2607.25956"></a>**Large Language Model for Operations Research Formulation Selection in Multi-Warehouse Inventory Allocation** — [2607.25956](https://arxiv.org/abs/2607.25956) | cross: math.OC  
  Jintao Xu, Yingzheng Ma, Jiong Dong, Yongzhi Qi et al.  
  Multi-warehouse inventory allocation is typically formulated as a mixed-integer programming (MIP) problem, yet no single formulation consistently matches heterogeneous instance-level regimes induced by demand concentration, inventory imbalance, replenishment scale, service constraints, and forecast volatility. We study this issue as instance-wise operations research (OR) formulation selection, …
- <a id="20260729-2607.25948"></a>**MODUS: Decoder-Only Any-to-Any Modeling of Diverse Modalities** — [2607.25948](https://arxiv.org/abs/2607.25948) | cross: cs.AI, cs.LG  
  Mingqiao Ye, Zhaochong An, Zhitong Gao, Xian Liu et al.  
  Any-to-any models predict any modality from any combination of others within a single network, a formulation used in multimodal vision and vision-language models, and increasingly in scientific domains such as ecology and astronomy. Existing any-to-any models are typically trained from scratch using encoder-decoder or diffusion architectures, impacting their performance and preventing them from …
- <a id="20260729-2607.25947"></a>**A Cost-Effective Multimodal LLM Reasoning Framework for Question Answering over Irregular Clinical Time Series** — [2607.25947](https://arxiv.org/abs/2607.25947) | cross: cs.CL  
  Frank Nie, Ethan B Liu, Yuan Zhu, Wei Fan et al.  
  Question answering (QA) over irregular clinical time series (ICTS) plays a pivotal role in a wide range of healthcare applications. Although recent multimodal time-series large language models (LLMs) have shown considerable promise in general-purpose time-series QA, they remain poorly equipped to model the sparsity, asynchrony, and irregular sampling patterns of clinical observations.
- <a id="20260729-2607.25933"></a>**Evaluating Multi-Turn Multimodal Diagnostic Reasoning on Challenging Real-World Clinical Cases** — [2607.25933](https://arxiv.org/abs/2607.25933) | cross: cs.AI  
  Rui Yang, Weihao Xuan, Yi Lin, Zhuhan Bao et al.  
  Clinical diagnostic evaluation should not only assess whether models can provide correct diagnoses, but also reflect the realities of clinical practice, including progressive disclosure of multimodal information, dynamic updating of diagnostic hypotheses, and continuous refinement of clinical reasoning. However, existing evaluations of multimodal large language models (MLLMs) typically rely on …
- <a id="20260729-2607.25926"></a>**Face De-Identification: A Domain-Centric Survey from Capture to Processing** — [2607.25926](https://arxiv.org/abs/2607.25926) | cross: cs.AI  
  Hui Wei, Hao Yu, Guoying Zhao  
  Face de-identification (De-ID) aims to remove or conceal personally identifiable facial features in images or videos to prevent identity recognition while preserving utility for downstream tasks. With the rising emphasis on data privacy and responsible AI, face De-ID has emerged as an active research area spanning computer vision and privacy-preserving communities.
- <a id="20260729-2607.25925"></a>**dtControl2+$\varepsilon$: Trading Optimality for Explainability in MDPs via Decision Trees** — [2607.25925](https://arxiv.org/abs/2607.25925)  
  Tereza Kinská, Jan Křetínský, Tobias Meggendorfer, Sabine Rieder et al.  
  Over the past decade, decision trees have been used to represent controllers (a.k.a. policies) in an explainable way, with dtControl2 as a current state-of-the-art tool.
- <a id="20260729-2607.25921"></a>**Evaluating VLMs for Autonomous Agent-Driven Geometry Clipping Detection in Video Game QA** — [2607.25921](https://arxiv.org/abs/2607.25921) | cross: cs.AI  
  Carlos Celemin, Benedict Wilkins, Adrián Barahona-Ríos, Saman Zadtootaghaj et al.  
  In this work, we study the use of Vision-Language Models (VLMs) for anomaly detection in an agent-driven game Quality Assurance (QA) pipeline focusing on geometry clipping. In this evaluation, a custom exploration agent navigates a game level to collect visual observations, while the automatic annotation pipeline provides frame-level clipping labels.
- <a id="20260729-2607.25915"></a>**Penelope: Localized Latent Recurrence for Efficient Structured Reasoning** — [2607.25915](https://arxiv.org/abs/2607.25915)  
  Yutong Chen, Shouqian Shi, Xinran Liu, Haochen Wang et al.  
  Complex structured reasoning tasks often require additional computation, yet current language models obtain it mainly by increasing parameter scale or by serializing intermediate steps as chain-of-thought (CoT) tokens. The former raises training and deployment costs, while the latter ties reasoning computation to autoregressive output length.
- <a id="20260729-2607.25914"></a>**Toward Standardized Cross-Vendor Agent Tool Trust Management in Autonomous Networks** — [2607.25914](https://arxiv.org/abs/2607.25914) | cross: cs.CR, cs.NI  
  Ravi Kant Sharma, Ashutosh Uttam, Ajay Kumar  
  Autonomous Network Levels 4-5 require AI agents to invoke tools across vendor boundaries without human oversight, yet existing management standards lack a standardized mechanism for cross-vendor trust visibility. When a tool from Vendor B is compromised, agents from Vendor A continue invoking it -- unaware of the trust degradation -- causing cascading service impact.
- <a id="20260729-2607.25912"></a>**SAM3D-Guided Object-Centric Representation Alignment for Vision-Language-Action Models** — [2607.25912](https://arxiv.org/abs/2607.25912) | cross: cs.AI  
  Zonghe Liu, Shanyuan Jie, Xiaoquan Sun, Chen Cao et al.  
  Vision-Language-Action (VLA) models have shown strong potential for general robot manipulation, but most existing models rely on 2D visual-language backbones and lack fine-grained 3D understanding of target objects, especially under occlusion, pose variation, scale changes, and precise spatial interaction. We propose an object-centric 3D representation alignment framework built upon $π_0$, using …
- <a id="20260729-2607.25911"></a>**AnnoBench: A Benchmark for Visualization Annotation Generation** — [2607.25911](https://arxiv.org/abs/2607.25911) | cross: cs.AI  
  Md Rahat-uz-Zaman, Md Dilshadur Rahman, Andrew McNutt, Paul Rosen  
  Annotation is among the most demanding visualization tasks to automate, as it simultaneously requires correctly navigating visual, semantic, and stylistic constraints. Failure to meet any of these conditions severely undermines the utility of an annotation, rendering it challenging to read, inaccurate, or visually discordant.
- <a id="20260729-2607.25904"></a>**Interactive Reward Agent: GUI Task Evaluation via Environment-State Verification** — [2607.25904](https://arxiv.org/abs/2607.25904)  
  Chenrui Shi, Yuwei Wu, Yang Liu, Ruining Feng et al.  
  Graphical user interface task evaluation aims to determine whether a GUI agent has successfully completed a user instruction. Automated GUI task evaluation has received increasing attention because the evaluation results can serve as reward signals for both test-time scaling and post-training.
- <a id="20260729-2607.25891"></a>**Messier: A High-Resolution Corpus for Cross-Benchmark Agent Evaluation** — [2607.25891](https://arxiv.org/abs/2607.25891) | cross: cs.DB  
  Stefan Krsteski, Charlotte Meyer, Guillaume Allegre, Tony O'Halloran et al.  
  Evaluating AI agents in interactive environments is hindered by fragmented tasks, scaffolds, verifiers, and scoring rules. Existing efforts focus on narrow settings, remain limited in scale, or require costly reruns, leaving much of the empirical record incomparable.
- <a id="20260729-2607.25890"></a>**Distributing Security Controls Through Harness Engineering** — [2607.25890](https://arxiv.org/abs/2607.25890)  
  William Robert Gore  
  AI coding agents are being adopted at historic speed, yet security and risk concerns remain the primary barrier to scaling agentic AI across organizations. Existing security controls for coding agents are not systematically distributed to engineering teams, and vendor-native solutions introduce ecosystem dependencies that may not suit every deployment context.
- <a id="20260729-2607.25888"></a>**Depression Markers in Speech: An Approach based on Tract Variables Dynamics** — [2607.25888](https://arxiv.org/abs/2607.25888) | cross: cs.AI  
  Sahar Altalhi, Tanaya Guha, Alessandro Vinciarelli  
  This study identifies new depression biomarkers based on the dynamical properties of tract variables, which represent geometric features describing the configuration of the speech articulators. A key advantage of this approach lies in its ability to quantify aspects of the articulatory process that have not been previously explored in the context of depression, namely predictability, complexity, …
- <a id="20260729-2607.25887"></a>**Device Invariance using Domain Adaptation on Acoustic Scene Classification** — [2607.25887](https://arxiv.org/abs/2607.25887) | cross: cs.AI, cs.SD  
  Abhishek dileep, Shubham Sharma, Padmanabhan Rajan  
  This paper explores the effectiveness of domain adaptation techniques when using convolutional neural network (CNN)-based and transformer-based feature representations for acoustic scene classification. Two well-known domain adaptation techniques, namely domain adversarial neural network (also called DANN) and conditional domain adversarial network (also called CDAN) are evaluated under various …
- <a id="20260729-2607.25880"></a>**Stemma: Induced Decision Regions Reveal LLM Provenance** — [2607.25880](https://arxiv.org/abs/2607.25880) | cross: cs.AI, cs.CL  
  Keyu Zhang, Vadim Safronov, Andrew Martin  
  LLM provenance testing asks whether a suspect LLM belongs to the same lineage as a source. Existing black-box methods largely infer this relationship from response-level characteristics, but these characteristics may shift under adaptation or deployment even when the underlying meaning remains unchanged, weakening the reliability of provenance evidence.
- <a id="20260729-2607.25877"></a>**Runtime Uncertainty Monitoring for LLM-Based Multi-Agent Systems Using Bayesian Networks** — [2607.25877](https://arxiv.org/abs/2607.25877)  
  Bart Custers, Koorosh Aslansefat  
  This paper investigates how multi-agent systems (MAS)-based on large language models (LLMs) can support actuarial risk modelling, with a particular focus on uncertainty quantification. Actuarial workflows represent a high-stakes decision-support setting where unreliable outputs may lead to incorrect risk assessment, unfair pricing, and regulatory non-compliance.
- <a id="20260729-2607.25865"></a>**OmniQEC: discovering practical quantum error-correcting codes by an AI scientist** — [2607.25865](https://arxiv.org/abs/2607.25865) | cross: cs.AI, cs.MA  
  Ge Yan, Shanchuan Li, Pengyue Ma, Qixin Zhang et al.  
  Quantum error correction (QEC) is indispensable for scalable fault-tolerant quantum computing. However, discovering QEC codes that remain effective is challenging, as logical performance depends on the interplay between code structure, hardware, syndrome extraction, and decoding, which often impose competing requirements.
- <a id="20260729-2607.25853"></a>**HiSkill: Empowering LLM Agents with Hierarchical Skill Graphs** — [2607.25853](https://arxiv.org/abs/2607.25853)  
  Yu Hao, Jinxuan Cai, Qi Zhang, Yawen Li et al.  
  Skills have become an important abstraction for enabling large language model (LLM) agents to reuse past experience in long-horizon interactive tasks. However, existing trajectory-to-skill methods often produce flat collections of high-level textual skills that are stored and retrieved independently, leaving skill relations underutilized and maintaining a gap between high-level skills and …
- <a id="20260729-2607.25835"></a>**Distributed Constraint Optimization via Online Learning and Iterative Pricing with Application to Large-Scale Satellite Scheduling** — [2607.25835](https://arxiv.org/abs/2607.25835) | cross: cs.GT  
  Itai Zilberstein, Pranav Rajbhandari, Steve Chien, Tuomas Sandholm  
  Distributed constraint optimization problems (DCOPs) provide a popular framework for distributed decision making under limited communication, but many real-world instances are too large to solve monolithically. We address this challenge from two complementary directions.
- <a id="20260729-2607.25834"></a>**Lowering the implementation barrier of neutral-atom quantum computing with agentic workflows** — [2607.25834](https://arxiv.org/abs/2607.25834) | cross: cond-mat.quant-gas, cs.AI  
  Constantin Dalyac, Alexandre Dauphin, Loïc Henriet, Christophe Jurczak  
  Quantum computers are moving from research laboratories to industrial machines accessible via the cloud and integrated into high-performance computing facilities. However, translating theoretical quantum protocols into hardware experiments remains a major bottleneck, requiring expertise across protocol design, compilation, simulation, and cloud execution.
- <a id="20260729-2607.25816"></a>**Speculate While You Reason: Teaching Agents to Predict Their Next Tool Call via Joint Agent-Speculator RL** — [2607.25816](https://arxiv.org/abs/2607.25816)  
  Jiabao Ji, Yujian Liu, Li An, Rohit Jain et al.  
  Large language model agents often spend substantial wall-clock time waiting for tool call results. Tool-call speculation can hide this latency by predicting and pre-executing an agent's next tool call if the prediction matches the agent's eventual tool call, but existing speculators are typically separate draft models or cached traces that are poorly aligned with the deployed agent's own behavior.
- <a id="20260729-2607.25748"></a>**Loss Invariance Determines What Concept Layers Encode: Volume Grounding in Echocardiography** — [2607.25748](https://arxiv.org/abs/2607.25748)  
  Hyunkyung Han, Min Jung Kim  
  Objective: Concept bottleneck models route prediction through interpretable intermediate variables, and their validity is normally judged by how accurately those variables are predicted. We ask whether that judgement is sufficient, using left ventricular volumes as the concepts underlying ejection fraction estimation from echocardiographic video.
- <a id="20260729-2607.25736"></a>**Image Quality Dependent Degradation for AI Systems** — [2607.25736](https://arxiv.org/abs/2607.25736) | cross: cs.AI  
  Yannick Kees, Elena Hoemann, Frank Köster, Sven Hallerbach  
  Perception is one of the primary applications where neural networks outperform conventional algorithms. One example is AI systems for automated driving, which can detect pedestrians based on image data and avoid them accordingly.
- <a id="20260729-2607.25728"></a>**Shared Voxel-Map-Based Cooperative Indoor UAV Guidance with a Multi-Agent Soft Actor-Critic Controller** — [2607.25728](https://arxiv.org/abs/2607.25728) | cross: cs.AI, cs.LG  
  Thomas Hickling, Dylan Wynne, Yu Su, Nabil Aouf  
  This paper presents a cooperative indoor UAV guidance framework that combines a shared voxel-map world model with a multi-agent Soft Actor-Critic (MASAC) controller. Multiple drones fuse 360 LiDAR observations into a common world-frame occupancy map, which is converted into a compact bird's-eye-view (BEV) representation and provided to each agent as an ego-aligned local crop.
- <a id="20260729-2607.25726"></a>**Nudging Sustainable Choices through LLM-Generated Recommendation Explanations** — [2607.25726](https://arxiv.org/abs/2607.25726)  
  Haya Halimeh, Dietmar Jannach, Oliver Müller  
  Recommender systems mediate everyday consumption, offering a promising channel for encouraging sustainable choices. Prior research shows that explanations influence users' perceptions of recommendations and can support more informed decisions.
- <a id="20260729-2607.25681"></a>**Cognivia: A Cognitive Behavioral Therapy Copilot for Evidence-Based Mental Healthcare** — [2607.25681](https://arxiv.org/abs/2607.25681)  
  Qi Chen, Siria Xiyueyao Luo, Jian Wang, Yuan Shi et al.  
  Cognitive distortion amplifies negative emotions and contributes to mental health disorders. Cognitive Behavioral Therapy (CBT) is an effective way to address cognitive distortions, but its large-scale application is limited by the shortage of professional therapists.
- <a id="20260729-2607.25675"></a>**DecoEvo: Score-Decoupled Co-Evolution of Solver and Rubric-Generator Skills in Text Space** — [2607.25675](https://arxiv.org/abs/2607.25675)  
  Jiangwang Chen, Zixin Song, Junlin Liu, Shuaiyu Zhou et al.  
  Text-space optimization adapts large language models (LLMs) by editing external natural-language artifacts rather than model weights, so the optimized artifacts remain inspectable and the model can be treated as a black box. However, most existing text-space methods keep evaluation fixed.
- <a id="20260729-2607.25669"></a>**OmniDelta: Skill-Driven Budget Allocation for Token Compression in OmniLLMs** — [2607.25669](https://arxiv.org/abs/2607.25669)  
  Haoyang Huang, Wenjie Huang, Tianqi Xu, Hongyaoxing Gu et al.  
  Emerging Omni-modal Large Language Models (OmniLLMs) enable unified understanding of text, audio, and video, but their long audio-video token sequences introduce substantial memory and inference costs. Existing compression methods mainly focus on selecting important tokens under fixed budgets, leaving the preceding budget-allocation problem underexplored.
- <a id="20260729-2607.25667"></a>**MyMentorLLM: A psychotherapy GenAI environment with multimodal voice/text patients, trainees and experts for deliberate practice** — [2607.25667](https://arxiv.org/abs/2607.25667) | cross: cs.AI  
  Rodolfo Rizzi, Alessandro Grecucci, Massimo Stella  
  Psychotherapists need repeated training and supervision by experts; however, scalability is problematic. Here we present MyMentorLLM, a multimodal voice- and text-based simulation environment for deliberate practice, used to generate 2,100 complete Cognitive Behavioural Therapy (CBT) training sessions.
- <a id="20260729-2607.25663"></a>**Localized Adaptation Reveals Distinct Learning Signatures in Transformers** — [2607.25663](https://arxiv.org/abs/2607.25663) | cross: cs.CL  
  Rebecca Ramnauth, Brian Scassellati  
  Transformer adaptation is typically distributed across model depth, even when the intended change is narrow. We investigate how adaptation site shapes what a model learns, how well that learning generalizes, and how selectively it is applied.
- <a id="20260729-2607.25659"></a>**CoRT: Counterfactual Replay for Token-Level Rubric-Guided Policy Optimization** — [2607.25659](https://arxiv.org/abs/2607.25659)  
  Bo-Wen Zhang, Junwei He, Wen Wang, Song-Lin Lv et al.  
  Rubric-based reinforcement learning enriches language model training by evaluating model outputs against explicit criteria. Yet in GRPO-style pipelines, these structured judgments are reduced to a scalar response-level reward and converted into a response-level advantage, which is broadcast uniformly to all generated tokens.
- <a id="20260729-2607.25656"></a>**OrchBench: Evaluating Multi-Agent Orchestration Plans in Isolation via Deterministic Simulation** — [2607.25656](https://arxiv.org/abs/2607.25656)  
  Zhenzhen Ren, Jiyan He, Xinpeng Zhang, Zhenxing Qian et al.  
  Complex tasks often decompose into parallelizable yet interdependent subtasks, making orchestration critical to the performance of multi-agent systems (MAS). Existing evaluations typically rely on end-to-end execution, which conflates orchestration-plan quality with worker capabilities, tool reliability, and environmental noise.
- <a id="20260729-2607.25655"></a>**Engine-Equal, Human-Unequal: A Reproducible Outcome Skew in Engine-Assessed Equal Chess Positions** — [2607.25655](https://arxiv.org/abs/2607.25655) | cross: physics.soc-ph, stat.AP  
  Jesung Park  
  Among chess opening positions that a strong engine judges essentially equal (Stockfish 18 evaluation within 10 centipawns of zero, depth-stable) and that humans actually reach on Lichess (October 2025; 1,661 positions, 16.1M occurrences), human results are not balanced. Positions carry outcome skews, each the gap between its games' actual results and what the players' ratings predict, whose …
- <a id="20260729-2607.25648"></a>**Why Public Service AI Governance Frameworks Risk Failing in the Age of General-Purpose AI: Lessons from Policing** — [2607.25648](https://arxiv.org/abs/2607.25648) | cross: cs.AI  
  Sam Relins, Daniel Birks  
  Public services face growing pressure to adopt artificial intelligence (AI) to close the gap between rising demand and falling resources. That pressure has intensified with general-purpose AI (GPAI): AI built on large language models that can be directed by prompt alone to perform an effectively unbounded range of tasks.
- <a id="20260729-2607.25641"></a>**OmniPhys: Knowledge-Graph-Driven Benchmarking and Collective Optimization for Physical Commonsense in Text-to-Image Generation** — [2607.25641](https://arxiv.org/abs/2607.25641) | cross: cs.AI  
  Yajing Xu, Yarong Lan, Jiaoyan Chen, Yichi Zhang et al.  
  While text-to-image models exhibit remarkable visual fidelity, they frequently violate fundamental physical commonsense. Existing benchmarks often rely on coarse-grained descriptions, failing to diagnose the mastery of specific physical principles.
- <a id="20260729-2607.25637"></a>**F(AI)2R: Who Did What, and Who Checked? Verifiable AI Provenance as an Executable Skill** — [2607.25637](https://arxiv.org/abs/2607.25637) | cross: cs.AI, cs.SI  
  Florian Krebs  
  F(AI)2R is FAIR research with AI in the loop, twice: an AI-assisted authoring pass and a machine-readable audit pass over every artefact. AI systems now draft, refactor, and verify research artefacts, yet their contributions are rarely recorded in a form a later human or machine can audit.
- <a id="20260729-2607.25634"></a>**AIriskEval-edu Demo: Auditing of Pedagogical Risks in Educational Explanations** — [2607.25634](https://arxiv.org/abs/2607.25634) | cross: cs.CL  
  Javier Irigoyen, Roberto Daza, Francisco Jurado, Julian Fierrez et al.  
  We present AIriskEval-edu Demo, a platform that audits the pedagogical quality of instructional explanations and provides explainable audit results. The platform evaluates an explanation against a rubric covering five dimensions of pedagogical risk: factual accuracy, depth and completeness, focus and relevance, student-level appropriateness, and ideological bias.
- <a id="20260729-2607.25633"></a>**Construction-Driven Injection: Linguistically-Grounded Edit-Based Code-Mixing Fingerprints for Large Language Models** — [2607.25633](https://arxiv.org/abs/2607.25633) | cross: cs.AI  
  Yongyi Cui, Yue Li, Tianbao Jiang, Xin Yi  
  Large language models (LLMs) are costly intellectual assets that remain exposed to unauthorized redistribution and commercial misuse. Injected fingerprints, i.e., trigger--target pairs embedded in model behavior, offer a practical, black-box-verifiable ownership signal, but existing methods decouple the two stages of the fingerprint life cycle: how a fingerprint is constructed and how it is …
- <a id="20260729-2607.25630"></a>**A Human-in-the-Loop Corpus for LLM-Based Simplification of Scientific Summaries** — [2607.25630](https://arxiv.org/abs/2607.25630) | cross: cs.AI, cs.HC  
  Kyuri Im, Michael Färber  
  Interdisciplinary research is accelerating, yet scientific papers remain difficult to understand outside their home fields. We study large language model (LLM)-based simplification of scientific texts and present a human-in-the-loop workflow that transforms expert summaries into more accessible versions for non-specialists.
- <a id="20260729-2607.25626"></a>**Joint Text-Audio Alignment for EEG-to-Text Decoding in Chinese Speech Production and Perception** — [2607.25626](https://arxiv.org/abs/2607.25626)  
  Tian Zheng, Xurong Xie, Xinxin Zhu, Xiaolan Peng et al.  
  Decoding speech information directly from scalp electroencephalography (EEG) into text provides a potential non-invasive neural communication pathway for individuals with severe speech and motor impairments. Compared with invasive approaches such as electrocorticography, EEG is safer and more widely deployable, yet substantially more challenging to decode.This challenge is exacerbated for Chinese …
- <a id="20260729-2607.25624"></a>**Quotient Dynamics, Effective Curvature, and Implicit Bias in Positive Quadratic Networks** — [2607.25624](https://arxiv.org/abs/2607.25624)  
  Pengcheng Cheng  
  Positive quadratic networks admit the low-rank representation f_U(x)=x^top UU^top x, where Uinmathbb{R}^{dtimes r} is identifiable only up to right orthogonal multiplication, representing a rank-r PSD matrix Q=UU^top. We study how this quotient structure governs training dynamics, curvature, recovery, and interpolation bias.
- <a id="20260729-2607.25620"></a>**Beyond Epistemia: Epistemic Schizologia and Large Language Models as Techno-Semiotic Machines** — [2607.25620](https://arxiv.org/abs/2607.25620) | cross: cs.HC  
  Federico Cabitza, Gianluca Colombo  
  Quattrociocchi and colleagues warn that the fluent outputs of large language models may allow linguistic plausibility to substitute for epistemic evaluation, producing the condition they call *Epistemia*: the experience of possessing knowledge without undertaking the practices through which judgment would ordinarily be warranted. This article accepts that diagnosis but challenges its explanatory …
- <a id="20260729-2607.25612"></a>**Multi-Sensor Alignment for Weather Simulations** — [2607.25612](https://arxiv.org/abs/2607.25612)  
  Samsad Alam, Devyani Lambhate, Aditya Mohan, Vishal Kumar et al.  
  Perception tasks for autonomous vehicles need to work satisfactorily in adverse weather conditions. Due to lack of real-world weather datasets, weather simulations are a promising alternative.
- <a id="20260729-2607.25605"></a>**Computational Extraction of Legal Causes via al-Sabr wa al-Taqsim: A Set-Theoretic Formalization for Closed Fiqh Chapters** — [2607.25605](https://arxiv.org/abs/2607.25605)  
  Elnaser Abdelwahab  
  This paper presents a set-theoretic formalization of the classical usuli method of al-Sabr wa al-Taqsim (Examination and Division) for extracting legal causes ('ilal) within closed chapters of jurisprudence. A computational algorithm is introduced that extracts minimal operational rules from a truth table of juristic verdicts.
- <a id="20260729-2607.25600"></a>**Beyond Self-Knowledge: Propagating Uncertainty Across Reasoning and Retrieval in LLMs** — [2607.25600](https://arxiv.org/abs/2607.25600) | cross: cs.AI, cs.CL  
  Chandan Kumar Sah, Xiaoli Lian, Li Zhang  
  Retrieval-augmented generation improves knowledge-intensive question answering, but indiscriminate retrieval can introduce irrelevant evidence and unnecessary computation. We investigate whether verbalized confidence from black-box language models can serve as an actionable signal for retrieval routing.
- <a id="20260729-2607.25597"></a>**A Density-Matrix Framework for Electronic-Structure Analysis of Functional-Group and Salt Effects in Lithium-Metal Electrolytes** — [2607.25597](https://arxiv.org/abs/2607.25597)  
  Mingkang Liu, Huize Yu, Yanbin Gao, Nan Yao et al.  
  The reactivity of lithium-metal electrolytes arises from the interplay of molecular functional groups, Li$^+$ solvation, and salt-anion participation. This interplay operates through the redistribution of electron density across donor, anion, and cation centers, which is most directly read out from the electronic structure resolved in space.
- <a id="20260729-2607.25583"></a>**How Small Can You Go? A Controlled Study of LoRA Rank, Target Modules, and Quantization Trade-offs for Text-to-SQL on a 60M-Parameter Model** — [2607.25583](https://arxiv.org/abs/2607.25583)  
  Mahendra Singh Rathor, Anagheem Azzam  
  Parameter-efficient fine-tuning (PEFT) and low-bit quantization are now standard tools for adapting language models under tight compute budgets, yet their interaction is most often studied on billion-parameter models where the design space is expensive to explore. We ask a complementary question: on a specific, fully reproducible 60M-parameter encoder-decoder model (T5-small) and a single-table …
- <a id="20260729-2607.25579"></a>**IRIS: Reusable Identity Representations from Frozen LLMs for Entity Alignment** — [2607.25579](https://arxiv.org/abs/2607.25579) | cross: cs.AI  
  Xinran Liu, Shengtao Li, Shouqian Shi, Ge Wang et al.  
  Entity alignment (EA) identifies entities across knowledge graphs (KGs) that refer to the same real-world object. Conventional EA methods mainly exploit explicit graph structures and textual fields, which often provide insufficient semantic understanding to recognize the same entity under heterogeneous descriptions and distinguish it from semantically similar entities.
- <a id="20260729-2607.25576"></a>**Matrix-Free Photoacoustic Image Reconstruction via Sensor-Token Self-Attention** — [2607.25576](https://arxiv.org/abs/2607.25576)  
  Mary John, Shibili Said, Imad Barhumi, Sherzod Turaev et al.  
  Photoacoustic tomography (PAT) combines the optical absorption contrast of biological tissue with the spatial resolution of ultrasound, yet recovering the initial pressure distribution from sparse-view sensor measurements remains an ill-posed inverse problem. Iterative compressive-sensing solvers and unrolled deep networks both retain a dependence on the system matrix at inference, which leaves …
- <a id="20260729-2607.25570"></a>**The LAIA Dataset: Labelled Attention for Intelligent Automobiles** — [2607.25570](https://arxiv.org/abs/2607.25570) | cross: cs.AI, cs.SE  
  A. Contreras, D. Porres, R. Abad, P. Cano et al.  
  The development of autonomous vehicles (AVs) usually relies heavily on data-driven artificial intelligence (AI) models that require large volumes of sensor data with ground-truth annotations. While modular architectures are widely used, end-to-end driving paradigms offer a promising alternative by directly mapping sensor inputs to control actions.
- <a id="20260729-2607.25569"></a>**CORF-GS: Real-Time Wireless Radiance Field Reconstruction via Coupled Optical-RF Gaussian Splatting** — [2607.25569](https://arxiv.org/abs/2607.25569) | cross: cs.AI, cs.CV, cs.IT  
  Jinya Zhang, Jiajia Guo, Chao-Kai Wen, Shi Jin  
  Recent advances in 3D Gaussian Splatting (3DGS)-based wireless radiance field (WRF) reconstruction provide an efficient solution for wireless channel modeling. However, existing WRF reconstruction methods rely on pre-collected observations and offline optimization, and thus struggle to provide real-time channel knowledge.
- <a id="20260729-2607.25560"></a>**Agent Skills Matter: Inferring Proprietary Skills from Execution Trajectories** — [2607.25560](https://arxiv.org/abs/2607.25560)  
  Jianing Geng, Ruiqi He, Zekun Fei, Biao Yi et al.  
  Agent skills package reusable procedures that improve downstream performance. Their lightweight, portable form enables marketplace monetization and private deployment behind cloud-hosted agent interfaces, giving providers incentives to keep high-value skills proprietary.
- <a id="20260729-2607.25554"></a>**Distilling Temporal Search and Reasoning: Evolving LLMs for Future Prediction via Harness-Assisted Efficient Data Synthesis** — [2607.25554](https://arxiv.org/abs/2607.25554)  
  Wanxu Cai, Zhengyu Chen, Huaisheng Zhu, Wei Wang et al.  
  Future event prediction carries broad social impact yet remains challenging. SOTA approaches augment LLMs with external agent frameworks whose predictive capability vanishes once the harness is removed.

#### cs.LG (37)

- <a id="20260729-2607.26000"></a>**Empirical Evaluation of Out-Of-Distribution Performance of Tabular Foundation Models** — [2607.26000](https://arxiv.org/abs/2607.26000) | cross: cs.AI  
  Malena Loza, David Chushig-Muzo, Eva Milara, Luis Bote-Curiel et al.  
  Tabular Foundation Models (TFMs) have emerged as novel approaches for tabular predictive tasks, demonstrating competitive predictive performance to ensemble tree-based models. Most TFMs are trained and evaluated on independent and identically distributed data, but this assumption changes in real-world scenarios due to distribution shifts, which compromise the robustness of models.
- <a id="20260729-2607.25970"></a>**Reinforcement Learning for Code Optimization** — [2607.25970](https://arxiv.org/abs/2607.25970) | cross: cs.AI  
  Pierre Chambon, Kunhao Zheng, Juliette Decugis, Benoit Sagot et al.  
  RL for code correctness is now established: have the model generate a program, run it against hidden test cases, and reward solutions that pass. Extending this to code optimization seems straightforward: just add execution time to the reward.
- <a id="20260729-2607.25907"></a>**Minimizing Targeted Activations: Input-Only Suppression of Evaluation-Awareness Latents in Large Language Models** — [2607.25907](https://arxiv.org/abs/2607.25907) | cross: cs.AI, cs.CL  
  Deepanshu Mody, Samarth Agarwal, Utkarsh Mittal, Dipesh Mahato  
  Activation steering controls model behavior by editing internal activations at inference time. We study its input-side dual: optimizing a fluent prompt so that a chosen internal latent is driven toward zero, with no inference-time model access.
- <a id="20260729-2607.25885"></a>**A Machine-Learning-Based Gas Lift Optimization Workflow for Unconventional Fields** — [2607.25885](https://arxiv.org/abs/2607.25885) | cross: cs.AI, cs.SE  
  Sha, Miao, Alexandra Vendetti, Logan Smart et al.  
  In this paper, we present an automated data-driven workflow using Machine Learning (ML) for gas lift optimization in unconventional fields. This workflow integrates a ML model that accurately forecasts the Gas Lift Performance Curve, and a Bayesian Optimization Framework to solve for the optimal gas injection rates under the constraints of facility capacity.
- <a id="20260729-2607.25875"></a>**A2TTA: Anchored-and-Agile Test-Time Adaptation for Evolving Traffic Sensor Networks** — [2607.25875](https://arxiv.org/abs/2607.25875) | cross: cs.AI  
  Du Yin, Xiachong Lin, Yue Tan, Jinliang Deng et al.  
  Traffic forecasting is important for efficient traffic management and route planning in smart cities. Existing traffic forecasting studies typically assume fixed sensor graphs, overlooking the continuous evolution of real-world traffic networks, e.g., ongoing road network construction and evolving human mobility patterns.
- <a id="20260729-2607.25790"></a>**SpectONet: A Physics-Guided Spectral Deep Operator Network for Euler-Bernoulli Beam Dynamics** — [2607.25790](https://arxiv.org/abs/2607.25790) | cross: cs.AI, math.DS  
  Shivani Saini, Ramesh Kumar Vats, Arup Kumar Sahoo  
  This paper proposes a novel physics-guided spectral deep operator network, termed SpectONet, for solving Euler-Bernoulli beam (EBB) vibration problems. The proposed framework integrates the operator-learning capability of DeepONet with physics-informed constraints and Chebyshev-Gauss-Lobatto (CGL) sensor placement.
- <a id="20260729-2607.25718"></a>**Tools Are Not Islands: Set-Level Tool Retrieval for LLM Agents via Query-Conditioned Hyperedge Prediction** — [2607.25718](https://arxiv.org/abs/2607.25718) | cross: cs.AI, cs.IR  
  Xinyi Hong, Pinjun Dong, Xinyang Yu, Binyan Jiang  
  Large language model (LLM) agents increasingly rely on invoking external tools to complete real-world tasks. Tool retrieval, which selects a small task-relevant subset from a library of thousands of tools before the agent acts, has therefore become a critical component of LLM agent pipelines.
- <a id="20260729-2607.25687"></a>**From Deterministic to Generative Deep Learning for Urban Air Quality Reconstruction from Sparse Observations** — [2607.25687](https://arxiv.org/abs/2607.25687) | cross: cs.AI  
  Abhishek A. Sabnis, Mihai Mitrea, Lya Lugon, Karine Sartelet et al.  
  Full-field reconstruction of air pollution is essential for evaluating pollution exposure and supporting public health decision-making. However, the complex interactions among pollutants, hard-to-predict weather patterns, and limited monitoring station coverage make this a complex task.
- <a id="20260729-2607.25680"></a>**Rashomon Alignment** — [2607.25680](https://arxiv.org/abs/2607.25680) | cross: cs.AI  
  Moisés Santos, Peter van der Putten, Bernhard Pfahringer, Carlos Soares  
  We propose Rashomon Alignment (RA), a new measure to assess functional similarity between two models. Existing functional similarity measures are distributional, quantifying differences between outputs of models applied to real-world data.
- <a id="20260729-2607.25679"></a>**DynaBridge: Dynamic Summary-Guided Cross-Task Multimodal Fusion for DASS-Structured Mental Health Assessment** — [2607.25679](https://arxiv.org/abs/2607.25679) | cross: cs.AI, cs.MM  
  Shiyu Teng, Haichen Yu, Jiaqing Liu, Hao Sun et al.  
  Multimodal behavioral analysis offers a scalable approach to assessing depression, anxiety, and stress, yet generic fusion models often ignore the psychometric structure of questionnaire labels. In DASS-21, risk labels are derived from ordered symptom items through fixed item-to-subscale mappings.
- <a id="20260729-2607.25609"></a>**Contrastive Representation Learning of Longitudinal Disease Trajectories on Temporal Graphs** — [2607.25609](https://arxiv.org/abs/2607.25609) | cross: cs.AI, q-bio.QM  
  Bastian Pfeifer  
  Understanding disease trajectories from longitudinal clinical data remains challenging due to complex temporal dynamics and heterogeneous patient cohorts. Here, we present a contrastive representation learning framework that models multivariate disease trajectories as temporal graphs and learns representations using contrastive graph neural networks.
- <a id="20260729-2607.25608"></a>**Physics-Informed Broad Learning System: An Efficient Backpropagation-Free Framework for Solving Partial Differential Equations** — [2607.25608](https://arxiv.org/abs/2607.25608) | cross: cs.AI  
  Pinki Khatun, M. Sajid, Abhinav Jha, M. Tanveer  
  Physics-informed neural networks (PINNs) have emerged as a powerful paradigm for solving partial differential equations (PDEs) by embedding governing physical laws into deep neural networks. However, their reliance on computationally expensive gradient-based optimization and deep architectures often results in slow training, high computational cost, and limited scalability.
- <a id="20260729-2607.26052"></a>**Spend Experts Where You Are Unsure: Confidence-Adaptive Routing for Mixture-of-Experts LoRA** — [2607.26052](https://arxiv.org/abs/2607.26052)  
  Tom Saliencro, Rohan Desai, Priya Nair, Maya Lindqvist et al.  
  Mixture-of-Experts (MoE) variants of Low-Rank Adaptation (LoRA) route every token to a fixed number of experts $k$. Tokens differ in how uncertain the model is about them, so a single k over-spends on easy tokens and under-serves hard ones.
- <a id="20260729-2607.26043"></a>**Re-thinking Mammography Transfer Learning: The Dataset-Informed Transfer Learning (DITL) Framework for Breast Cancer Screening and Lesion Diagnosis** — [2607.26043](https://arxiv.org/abs/2607.26043)  
  Adarsh Bhandary Panambur, Siming Bayer, Andreas Maier  
  Enhancing classification performance in mammography remains a persistent challenge across both small curated datasets and large-scale clinical cohorts. Conventional transfer learning approaches often neglect dataset-specific characteristics, while recent neighborhood-informed methods have been restricted to narrow tasks with rigid formulations, limiting their scalability to population-level …
- <a id="20260729-2607.26042"></a>**VetClaw: An Edge-Cloud Multimodal Agentic System for Veterinary Disease Screening** — [2607.26042](https://arxiv.org/abs/2607.26042) | cross: cs.LG  
  Syed Mhamudul Hasan, Anas AlSobeh, Hussein Zangoti, Abdur R. Shahid  
  We present VetClaw, an edge-cloud multimodal agentic system for early veterinary disease screening. VetClaw uses a camera module as an edge sensing device and sends captured images, together with optional symptom descriptions, to a server-hosted vision-language model for zero-shot disease classification.
- <a id="20260729-2607.26040"></a>**Reinformed Dreamer: An Asymmetric World Model Efficiently Trained through Latent Guidance** — [2607.26040](https://arxiv.org/abs/2607.26040) | cross: stat.ML  
  Gaspard Lambrechts, Adrien Bolland, Daniel Ebi, Damien Ernst  
  Much like humans benefit from guidance while learning, reinforcement learning algorithms may benefit from additional supervision beyond rewards. Leveraging additional information during training to learn better representations and behaviors has been the focus of asymmetric reinforcement learning.
- <a id="20260729-2607.26004"></a>**Parallel Decoding Distillation for Fast Image and Video Generation** — [2607.26004](https://arxiv.org/abs/2607.26004) | cross: cs.LG  
  Neta Shaul, Chao Liu, Arash Vahdat, Julius Berner  
  Generation in video diffusion or flow models is computationally expensive due to the slow and iterative sampling process. Current state-of-the-art (SOTA) acceleration methods heavily rely on variational score distillation (VSD) and adversarial losses to distill diffusion models into few-step generators.
- <a id="20260729-2607.26001"></a>**Sharpness-Aware Minimization and Muon: Robustness under the Spectral Norm** — [2607.26001](https://arxiv.org/abs/2607.26001) | cross: stat.ML  
  Wenzhi Zhong, Edward Milsom, Michael Murray  
  Sharpness-Aware Minimization (SAM) aims to improve generalization by encouraging insensitivity to small, worst-case parameter perturbations. However, the notion of a "small" perturbation is inherently geometry-dependent: while existing SAM variants have explored a wide range of choices, a clear perspective on which geometries are most effective in practice remains elusive.
- <a id="20260729-2607.25989"></a>**Untangling Co-Drift: Proactive Multi-Intent Failure Prediction and Root-Cause Disambiguation for Self-Driving Networks** — [2607.25989](https://arxiv.org/abs/2607.25989) | cross: cs.LG, cs.RO  
  Md. Kamrul Hossain, Walid Aljoby  
  The vision of self-driving networks that monitor, reason, and act upon themselves with minimal human intervention relies on tightly coupled monitoring, analytics, and actuation functions. In this work, we treat these functions as three operational macro-intents: continuous telemetry, real-time analytics, and programmatic actuation, and formalize the health of each function as an intent that the …
- <a id="20260729-2607.25988"></a>**Generator-Aligned Representation Interfaces for Diagnostic Soft Equivariance** — [2607.25988](https://arxiv.org/abs/2607.25988)  
  Weitao Li, Gong Cheng  
  Exact-equivariant architectures typically encode prescribed group actions in specialized operators, which can complicate their reuse with generic backbones and across data modalities. We introduce the Generator-Aligned Representation Interface (GARI), a representation-level design principle that exposes selected transformation generators to a generic sequence backbone through aligned canonical …
- <a id="20260729-2607.25985"></a>**Physics-Aware End-to-End Deep Reinforcement Learning for Quadcopter Control with Actuator Dynamics** — [2607.25985](https://arxiv.org/abs/2607.25985) | cross: cs.LG, eess.SY  
  Ya-Chia Shen, Woei-Leong Chan  
  Unmanned aerial vehicles (UAVs), particularly quadcopters, present unique challenges for autonomous control due to their underactuated dynamics: only four available control inputs must govern six degrees of freedom. This paper investigates a physics-aware, end-to-end deep reinforcement learning (DRL) approach that acts directly on low-level body inputs, total thrust and body torques $(T, τ_x, …
- <a id="20260729-2607.25984"></a>**Schrödinger's Cat: Probabilistic Representation and Prediction of Potential Scene Kinematics** — [2607.25984](https://arxiv.org/abs/2607.25984) | cross: cs.LG  
  Timy Phan, Jannik Wiese, Björn Ommer  
  Predicting how a scene may evolve from partial observations requires reasoning about multiple possible futures rather than committing to a single trajectory. Existing approaches either generate appearance-dominated video predictions or sample a small number of trajectories without explicitly modeling the distribution of possible motion.
- <a id="20260729-2607.25967"></a>**Quasi-SVD: Learning a Lie-constrained matrix factorisation for real-time imaging** — [2607.25967](https://arxiv.org/abs/2607.25967) | cross: cs.LG, math.NA  
  Christopher Hahne  
  Singular Value Decomposition (SVD) underlies matrix factorisation tasks across computational imaging, with medical applications increasingly demanding real-time processing. Yet SVD algorithms are inherently sequential, constraining real-time GPU throughput and limit online deployment in clinical pipelines.
- <a id="20260729-2607.25929"></a>**Can Deep Generative Models Reproduce Non-Stationary Gaussian Random Fields?** — [2607.25929](https://arxiv.org/abs/2607.25929) | cross: cs.LG  
  Daniel Kua, Yan Song  
  Deep generative models (DGMs) are widely used for complex high-dimensional data and increasingly applied to spatial and spatio-temporal modeling. Their generated samples implicitly represent the learned data distribution and associated uncertainty.
- <a id="20260729-2607.25895"></a>**HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone** — [2607.25895](https://arxiv.org/abs/2607.25895) | cross: cs.CV, cs.LG  
  Simple AI, :, Yuteng Wei, Jinming Ma et al.  
  Learning deployable manipulation policies is bottlenecked by the scarcity of data that is both high-fidelity and scalable. Real-robot teleoperation is accurate but costly to scale; robot-free UMI capture scales readily, and current practice uses the resulting data mainly for pre-training, adding a small real-robot "anchor" at post-training.
- <a id="20260729-2607.25870"></a>**VAD to the Bone: Ultra-Tiny Speech Activity Detection for Edge Deployment** — [2607.25870](https://arxiv.org/abs/2607.25870) | cross: cs.LG  
  Stephen Bauer, Sheila Seidel, Shanza Iftikhar, Scott Veidenheimer et al.  
  Voice activity detection (VAD) triggers downstream speech processing in always-on systems under strict memory, latency, and compute constraints. Recent compact models report strong accuracy but rely on components that are not widely supported: learnable filterbanks, recurrent layers, or non-causal post-processing.
- <a id="20260729-2607.25864"></a>**DRIFT: Direct-Recursive Intervention-Conditioned Forecasting of ICU Physiological Trajectories** — [2607.25864](https://arxiv.org/abs/2607.25864) | cross: eess.SP  
  Weixin Liu, Juming Xiong, Congning Ni, Yanfan Zhu et al.  
  Many time-series forecasts depend not only on prior observations but also on actions specified during the forecast period. In intensive care units (ICUs), future vital signs and laboratory values are influenced by treatments such as vasopressors.
- <a id="20260729-2607.25826"></a>**Prototype Adaptation for Zero-Shot sEMG Movement Classification** — [2607.25826](https://arxiv.org/abs/2607.25826)  
  Rui Liu, Benjamin Paassen  
  Surface electromyography (sEMG) enables the control of prostheses, allowing upper-limb amputees to re-gain some hand function. Most current research focuses on recognizing basic movements for prosthesis control.
- <a id="20260729-2607.25785"></a>**Variance-Reduced Conditional Gradient Methods under Markovian Sampling for Nonconvex Composite Optimization** — [2607.25785](https://arxiv.org/abs/2607.25785) | cross: cs.LG  
  Zhaojun Peng  
  We study stochastic composite nonconvex optimization over a compact convex set when gradient samples arrive along a single trajectory of a fixed ergodic Markov chain. Existing single-trajectory variance-reduction theory covers smooth unconstrained objectives; we address the projection-free composite setting using the generalized Frank-Wolfe gap.
- <a id="20260729-2607.25763"></a>**WALoMA: A Multitask Wireless Foundation Model via Adaptive Low-Rank Masked Autoencoders** — [2607.25763](https://arxiv.org/abs/2607.25763) | cross: cs.LG  
  Madi Makin, Asmaa Abdallah, Abdulkadir Celik, Ahmed M. Eltawil  
  This paper proposes a multitask wireless foundation model via adaptive low-rank masked autoencoders (WALoMA), a unified multi-task foundation model for sixth-generation (6G) wireless physical layer architectures, to address the limitations of specialized, task-specific deep learning models and the practical challenge of scarce labeled wireless datasets. By leveraging concepts inspired by …
- <a id="20260729-2607.25751"></a>**An Embarrassingly Simple Rule-based Visiting Circulation Approach to Trip Destination Prediction** — [2607.25751](https://arxiv.org/abs/2607.25751)  
  Eng-Shen Tu, Yong-Han Chen, En-Chao Liu, Hao-Yun Keng et al.  
  In this paper, we propose the Rule-based Visiting Circulation (RVC) model in tackling the challenge in the IEEE Big Data Cup 2022: Trip Destination Prediction. Given trips containing travel information, personal attributes, origin zones, and their features in the training metropolitan areas, the task is to predict the destination of every trip in a targeted metropolitan area whose destinations …
- <a id="20260729-2607.25750"></a>**Detecting CSAM Text-to-Image LoRAs From Weights** — [2607.25750](https://arxiv.org/abs/2607.25750) | cross: cs.CY  
  David Demitri Africa, Cate Heine, Nadine Staes-Polet, Kimberly Mai  
  Low-rank adaptation (LoRA) fine-tuning has made it cheap and easy to customize open-weight image generation models for specific tasks, including the production of child sexual abuse material (CSAM). Existing moderation relies on metadata or generated outputs, but metadata can be deceptive and generating outputs may itself be unacceptable or illegal.
- <a id="20260729-2607.25719"></a>**Optimization with Dynamic Constraint Learning (DCL)** — [2607.25719](https://arxiv.org/abs/2607.25719) | cross: math.OC  
  Ezgi Oztekin, Figen Oztoprak, S. Ilker Birbil  
  We propose Dynamic Constraint Learning (DCL), a data-driven framework for constrained optimization when constraint functions are unknown and cannot be queried during optimization. At each iteration, the method learns a local surrogate from nearby data and solves a subproblem within a data-supported trust region.
- <a id="20260729-2607.25668"></a>**A Physics-Informed Neural Operator for Thermal Ranking of Low-Cost Wall Materials in Hot-Dry Climates** — [2607.25668](https://arxiv.org/abs/2607.25668) | cross: math.NA, physics.comp-ph  
  Muhammad Akbar Khan, Fahim Raees, Ubaida Fatima  
  Identifying cost-effective indigenous building materials that minimise heat penetration through walls is critical for indoor thermal comfort in low-income rural housing in hot-dry climates, where summer temperatures routinely exceed 45 C. We present a two-stage computational framework for thermal ranking of five low-cost indigenous wall materials: mud brick, clay-straw adobe, lime-stabilised …
- <a id="20260729-2607.25664"></a>**Contextual Deconvolution for Variance-Stable Demand Sensing: Kernel-Modulated Operators in Promotional Retail** — [2607.25664](https://arxiv.org/abs/2607.25664) | cross: math.OC, stat.ML  
  Mohammad Forouhesh  
  Machine learning demand forecasts optimize statistical accuracy yet leave excess operational volatility that inflates safety stock and amplifies the Bullwhip effect. We introduce \textbf{Contextual Deconvolution} (CD), a two-stage estimator that reframes demand sensing as a convex decomposition: a kernel-modulated banded operator separates transient promotion-driven shocks from a smooth …
- <a id="20260729-2607.25636"></a>**Using Data-Derived Priors to Guide CNN Architecture Design for NIR Chemometrics** — [2607.25636](https://arxiv.org/abs/2607.25636) | cross: physics.app-ph, physics.comp-ph  
  Dário Passos  
  Convolutional neural networks (CNN) for near-infrared (NIR) chemometrics are often designed using generic architectural rules, although spectral datasets differ in sampling, smoothness, redundancy, and sample size. We tested whether these properties can provide empirical priors for CNN design.
- <a id="20260729-2607.25614"></a>**MemSFT: Mitigating Alignment Tax with an External Parametric Memory** — [2607.25614](https://arxiv.org/abs/2607.25614) | cross: cs.CL  
  Jiarui Wang, Xiang Shi, Jiaqi Cao, Rubin Wei et al.  
  Adapting Large Language Models (LLMs) to specialized domains often incurs an alignment tax, as fine-tuning on domain-specific tasks can cause catastrophic forgetting and substantially degrade performance on general tasks. We propose MemSFT, which mitigates the alignment tax by decoupling domain specialization from backbone parameter updates through a plug-and-play parametric memory.

#### cs.DB (2)

- <a id="20260729-2607.25992"></a>**MemLens: A Value-Aware Memory Management System with Interactive Analytics for LLM-based Agents** — [2607.25992](https://arxiv.org/abs/2607.25992) | cross: cs.AI  
  Shuyue Wei, Chang Liu, Zimu Zhou, Yongxin Tong et al.  
  Recently, memory management has become a key infrastructure for LLM-based agents, as it directly affects long-horizon reasoning, personalized responses, and knowledge reuse. However, existing LLM memory systems typically adopt a coarse-grained (utility-agnostic) manner that treats heterogeneous user-LLM interaction records uniformly, leading to redundant and low-impact records persisting in the …
- <a id="20260729-2607.25765"></a>**WorkSurface-Bench: Benchmarking Enterprise Agents on Multi-Surface Knowledge Routing** — [2607.25765](https://arxiv.org/abs/2607.25765) | cross: cs.DB  
  Hao Liang, Meiyi Qiang, Sizhe Qiu, Linzhuang Sun et al.  
  Enterprise agents often need to integrate heterogeneous knowledge sources: documents for narrative facts, tables for computation, and dependency graphs for file relationships. Existing benchmarks typically evaluate retrieval or tool use without distinguishing whether an agent first selects the appropriate knowledge sources.

#### cs.DC (3)

- <a id="20260729-2607.25916"></a>**Hermes: Low Tail-Latency Via Prefix Consensus** — [2607.25916](https://arxiv.org/abs/2607.25916) | cross: cs.CR  
  Alejandro Ranchal-Pedrosa, Dakai Kang, Neil Giridharan, Dahlia Malkhi et al.  
  Leader-based BFT protocols finalize through their leaders: a view whose leader is crashed or slow finalizes nothing, and the timeout that ends it admits no good setting. A conservative timeout turns every crashed leader into a long stall; an aggressive one voids the views of leaders that are merely slow.
- <a id="20260729-2607.25866"></a>**Massively parallel numerical simulations with Julia** — [2607.25866](https://arxiv.org/abs/2607.25866) | cross: cs.DC, cs.MS, cs.PF  
  Simon Candelaresi, Benedict Geihe, Marco Artiano, Lars Christmann et al.  
  The Julia programming language aims to provide a modern approach to develop high-performance computing (HPC) applications. It tries to achieve this by combining a high-level, dynamic interface with just-in-time compilation to native machine code, thereby facilitating high developer productivity and native code performance at the same time.
- <a id="20260729-2607.25650"></a>**PowerScale: Energy-Efficient Geo-Distributed Model Training with Federated Datacenter Power** — [2607.25650](https://arxiv.org/abs/2607.25650)  
  Talha Mehboob, Zhe Xu, Michael Zink, David Irwin  
  The power demands of large-scale AI training increasingly exceed the capacity of any single data center, making geo-distributed training across power-constrained sites a practical necessity. Prior work optimizes such training mainly for time-to-accuracy using single-tier aggregation, where every site exchanges model updates directly with a central aggregator over the WAN each synchronization …

#### cs.FL (1)

- <a id="20260729-2607.26013"></a>**Combinatorial structures connecting Latin squares and bireversible automata** — [2607.26013](https://arxiv.org/abs/2607.26013) | cross: math.CO, math.GR  
  Brian Curtin, Dmytro Savchuk  
  This paper explores the theory of letter transducers, Mealy automata, and bireversible automata from a combinatorial perspective analogous to the theory of Latin squares. We view the sets of transitions of letter transducers as analogs of orthogonal arrays, and discuss two other combinatorial encodings of Mealy automata analogous to orthogonal pairs of Latin squares and to $(k,n)$-nets.

#### cs.LO (3)

- <a id="20260729-2607.25793"></a>**Verification of Provers and Solvers** — [2607.25793](https://arxiv.org/abs/2607.25793) | cross: cs.SC  
  René Thiemann  
  Automatic deduction tools such as automatic theorem provers, SAT (satisfiability) solvers, SMT (satisfiability modulo theories) solvers, and termination analyzers can be connected to proof assistants using various approaches, notably by certification and verification. This chapter reviews and compares the approaches available, and mentions several successful applications.
- <a id="20260729-2607.25712"></a>**Universal Individual-Sequence Prediction with a Primitive-Recursive Superpredictor** — [2607.25712](https://arxiv.org/abs/2607.25712) | cross: cs.LO  
  Amir Leshem  
  We study sequential prediction of individual binary sequences under zero-one loss. No computable master can compete on every sequence with all total computable predictors.
- <a id="20260729-2607.25628"></a>**Kernel-Checked Exclusions for the Erdős-Selfridge Odd Covering Problem: Any Odd Covering of $\mathbb{Z}$ Has lcm Exceeding 10000** — [2607.25628](https://arxiv.org/abs/2607.25628) | cross: math.NT  
  Ibrahim Mian, Shayaan Siddique  
  The Erdős-Selfridge odd covering problem (Erdős problem #7) asks whether a covering system of $\mathbb{Z}$ exists whose moduli are all odd, distinct, and greater than 1. The problem is open.

#### cs.PL (1)

- <a id="20260729-2607.25651"></a>**Demystifying Deep Learning Compiler Frontend Bugs: An LLM-Aided Empirical Study** — [2607.25651](https://arxiv.org/abs/2607.25651) | cross: cs.SE  
  Xinyi Yuan, Wei Chen, Jinyi Liu, Pengyu Chen et al.  
  Deep learning compilers (DLCs) are designed to translate deep learning programs into optimized, hardware-specific code. Typically, DLC frontends translate programs into graph-based intermediate representations (IRs) to enable optimizations.

#### cs.SE (14)

- <a id="20260729-2607.25873"></a>**How Do LLMs Read Bug Reports? An Empirical Study of Attention in LLMs for Automated Program Repair** — [2607.25873](https://arxiv.org/abs/2607.25873) | cross: cs.AI  
  Ramtin Ehsani, Irene Manotas, Saurabh Pujar, Luca Buratti et al.  
  Large Language Model (LLM)-based Automated Program Repair systems are advancing rapidly, yet their performance remains inconsistent. Even when provided with the same contextual information, an LLM may generate a correct patch for one bug but fail on another closely related bug.
- <a id="20260729-2607.25647"></a>**KQFuzz: Knowledge-Guided Fuzzing for Quantum Libraries via Large Language Models** — [2607.25647](https://arxiv.org/abs/2607.25647) | cross: cs.AI, cs.MA, quant-ph  
  Fuyuan Xia, Qixin Zhang, Chenhao Ying, Haojin Zhu et al.  
  As quantum computing continually improves, ensuring the reliability and correctness of quantum libraries has become increasingly critical. To this end, many LLM-based fuzzing approaches towards quantum libraries have been proposed to uncover potential bugs.
- <a id="20260729-2607.25996"></a>**RepoReasoner: Evaluating Repository-Level Code Reasoning Ability of Long-Context Language Models** — [2607.25996](https://arxiv.org/abs/2607.25996)  
  Yanlin Wang, Suiquan Wang, Yanli Wang, Bowen Zhang et al.  
  Recent large language models (LLMs) have shown strong performance on software engineering tasks, yet most existing benchmarks evaluate code reasoning at the function level, where all relevant information is localized. This setting fails to reflect real-world development, which requires reasoning across multiple files and complex dependency structures.
- <a id="20260729-2607.25987"></a>**\textsc{IH-Benchmark}: A Conflict-Centered Benchmark for Instruction-Hierarchy Robustness in LLM Applications** — [2607.25987](https://arxiv.org/abs/2607.25987) | cross: cs.SE  
  Conor McCauley, Zeliang Kan, Jason Martin  
  When a language model receives conflicting instructions from different priority levels, which one does it actually follow? This question lies at the heart of reliable LLM deployment.
- <a id="20260729-2607.25946"></a>**A Low-Cost Human-in-the-Loop Investigation of Toxicity on GitHub at Scale** — [2607.25946](https://arxiv.org/abs/2607.25946)  
  Rahat Rizvi Rahman, Mia Mohammad Imran, Kostadin Damevski  
  Toxic interactions in open source discussions can alienate contributors and threaten project sustainability, yet prior empirical studies of GitHub toxicity have been limited in scale, raising questions about their generalizability. Scaling up is difficult because toxicity on GitHub is often implicit and context-dependent, making both fully manual annotation and LLM-based labeling unreliable.
- <a id="20260729-2607.25886"></a>**RSIBench-Data: Benchmarking Data-Centric Research for Recursive Self-Improvement** — [2607.25886](https://arxiv.org/abs/2607.25886) | cross: cs.CL  
  Fanqing Meng, Lingxiao Du, Qiguang Chen, Ziqi Zhao et al.  
  Recursive self-improvement requires turning evidence of model failures into better models. Data-centric post-training research entails diagnosing capability gaps, designing and validating training-data strategies, and learning from checkpoint feedback.
- <a id="20260729-2607.25884"></a>**CONQuER: Hardware-Aware Mixed-Precision Quantisation with Online-Calibrated Surrogates** — [2607.25884](https://arxiv.org/abs/2607.25884)  
  Aidan Dakhama, Ajitha Rajan  
  Deploying deep neural networks on resource-constrained hardware relies on mixed-precision quantisation (MPQ). current deployment toolchains severely fragment this process.
- <a id="20260729-2607.25851"></a>**Rethinking Training Data for Generating Code Review Comments** — [2607.25851](https://arxiv.org/abs/2607.25851)  
  Leonardo Centellas-Claros, Estefania Pakarati-Cofre, Juan Pablo Sandoval Alcocer, Diego Elias Costa  
  Generating code review comments has become a prominent research direction in automated code review, commonly formulated as a text generation task over diff-comment pairs. Despite advances in learning-based approaches, generated review comments are often generic, weakly grounded, or non-actionable.
- <a id="20260729-2607.25831"></a>**WarmTuner: Program-Specific Warm Starts for Compiler Autotuning via Offline-to-Online Reinforcement Learning** — [2607.25831](https://arxiv.org/abs/2607.25831)  
  Tianlu Qiao, Mingxuan Zhu, Zeyu Sun, Dan Hao  
  Compilers are fundamental software tools that translate high-level programs into machine code. Modern compilers expose hundreds of optimizations, each turned on or off through an optimization flag, to improve the performance of the generated code.
- <a id="20260729-2607.25695"></a>**Delta Debugging for Cyber-Physical Systems with Flaky Test Executions** — [2607.25695](https://arxiv.org/abs/2607.25695)  
  Pablo Valle, Shaukat Ali, Aitor Arrieta  
  Simulation-based testing is widely used to validate Cyber-Physical Systems (CPSs), yet modern CPS simulators frequently exhibit non-deterministic (flaky) behavior, making failures difficult to reproduce and debug. Although delta debugging has proven effective for deterministic systems, its underlying assumptions do not hold in stochastic environments.
- <a id="20260729-2607.25635"></a>**An Empirical Study of Model Context Protocol Applications** — [2607.25635](https://arxiv.org/abs/2607.25635)  
  Muhammad Hamza Arshad Majeed, May Mahmoud, Sarah Nadi  
  The Model Context Protocol (MCP) standardizes how large language model applications communicate with external tools, but leaves the application side unspecified: unlike traditional dependencies resolved through package managers, developers integrating MCP servers face no conventions for configuration, communication, or human oversight. This ecosystem is also under-researched, with existing work …
- <a id="20260729-2607.25619"></a>**SkillGate: Cost Efficient Runtime Malicious Skill File Detection in Coding Agents** — [2607.25619](https://arxiv.org/abs/2607.25619) | cross: cs.CR  
  Rui Yang, Michael Fu, Kla Tantithamthavorn, Chetan Arora et al.  
  Software engineering teams now deploy AI coding agents (Cursor, Claude Code, GitHub Copilot) as first-class productivity tools, installing domain-specific skill files to tailor agent behavior to project APIs, framework conventions, and organizational workflows. These complex Markdown files are easily downloaded from public registries with a single npx skills add command and no real security …
- <a id="20260729-2607.25603"></a>**Input Relation Prompting for Metamorphic Testing on Query-Based Systems** — [2607.25603](https://arxiv.org/abs/2607.25603)  
  Eng-Shen Tu, Shin-Jie Lee  
  Testing query-based systems (QBSs) presents significant challenges due to the absence of ground truth for validation and the extensive time and effort required for manual testing. This paper addresses these challenges by proposing an approach that assists testers in identifying metamorphic relations (MRs) for metamorphic testing (MT) instead of solely and exhaustively relying on prerequisite …
- <a id="20260729-2607.25566"></a>**ARCHER: Agentic Rule and Compliance Harness for Executable Regulations** — [2607.25566](https://arxiv.org/abs/2607.25566) | cross: cs.CE, cs.SE  
  Chiraag Singh Anand, Xue Wen Tan, Lionel Teo, Eric Tan  
  Verifying building compliance requires validating thousands of rules against large Building Information Modeling (BIM) designs, which is laborious, capital-intensive, and unscalable. Existing Automated Compliance Checkers (ACCs) are often difficult to generalize across different scenarios, as they are typically developed for highly specific rule sets and use cases.

<!-- END 20260729 -->
