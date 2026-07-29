# arXiv Daily Digest

> 自动生成的 arXiv 每日新增论文摘要。类别: math.LO, cs.AI, cs.LG, cs.DB, cs.DC, cs.FL, cs.LO, cs.PL, cs.SE。
> 由 `arxiv_daily.py` 抓取; ★/🧐 推荐由 agent 根据研究兴趣补充(见 `README.md`)。
> 推荐指数: ★=基于当前研究兴趣(五星强烈推荐); 🧐=视野扩展(五个强烈推荐)。

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
