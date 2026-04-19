# Axiom Candidates

由 weekly reflector 或后续人工整理补充。

## 2026-04-19

### Candidate: 共享认知层与项目执行层必须物理分层

- 类型：decision principle
- 核心判断：跨项目共享的认知资产应集中在 `rules/`、`contexts/`、`tools/`、`periodic_jobs/`；项目专属代码、状态和原始上下文应收敛到 `projects/<project>/`。边界清晰，AI 才能区分长期规则和局部任务状态。
- 适用场景：设计 AI workspace、重构多项目目录、判断新文件应落在哪一层时。
- 证据：`docs/WORKSPACE_REDESIGN_AND_HEARTBEAT.md`、`rules/WORKSPACE.md`、`projects/heavy_template/docs/decisions.md`、`contexts/memory/OBSERVATIONS.md` 的 2026-04-19 🔴 记录。

### Candidate: 原始素材不是长期记忆，抽象后的入口和规律才是

- 类型：decision principle
- 核心判断：长期记忆的价值来自可复用的入口、结构和规律，而不是文件本身的新旧。面对课程资料、转录稿、分析产物或一次性输出时，应优先提炼入口索引与稳定模式，再决定是否保留到高层记忆。
- 适用场景：判断内容型项目、Lite 项目、文档库是否值得进入候选层或规则层时。
- 证据：`periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md` 的内容型项目识别规则，以及三个 Lite 项目 overview 的共同结构。
