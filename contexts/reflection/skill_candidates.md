# Skill Candidates

由 weekly reflector 或后续人工整理补充。

## 2026-04-19

### Candidate: Heartbeat 双阶段记忆管线

- 类型：workflow / best practice
- 适用场景：为 Agent 工作流设计长期记忆系统，需要同时控制幂等性、可追溯性和规则污染风险时。
- 稳定模式：将记忆系统拆成 L1 Observer 和 L2 Reflector 两个角色。L1 只做 append-only 的原始观测写入，并先做日期级幂等检查；L2 只负责候选晋升与低价值 GC，不直接改写正式 `rules/`。
- 证据：`periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md`、`periodic_jobs/ai_heartbeat/observer.py`、`periodic_jobs/ai_heartbeat/reflector.py`、`contexts/memory/OBSERVATIONS.md` 的 2026-04-19 记录相互印证。
- 建议后续：如果未来数周继续稳定执行且没有角色越界，再考虑晋升到 `rules/skills/`。

### Candidate: Lite / 内容型项目的扫描入口优先级

- 类型：workflow / best practice
- 适用场景：扫描混合型 workspace 时，项目中既有代码又有教材、转录、分析产物，容易把内容资产误当成长期记忆信号。
- 稳定模式：先读 `projects/<project>/docs/overview.md` 判断项目模板和主资产类型。对 Lite / 内容型项目，把 `materials/`、`artifacts/`、嵌套 repo 内部文件视为内容资产；只有入口索引、结构变化或可复用方法论结论才考虑进入长期记忆。
- 证据：`periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md` 的 Lite 项目与内容型项目规则，以及 `projects/intro_optimization_ds/docs/overview.md`、`projects/mo_book/docs/overview.md`、`projects/videos_transcribe/docs/overview.md` 的一致结构。
- 建议后续：如果后续新增 Lite 项目仍复现这一模式，可晋升为通用扫描 skill。

### Candidate: 本地定时 Agent 作业的依赖就绪门

- 类型：workflow / ops best practice
- 适用场景：用 `launchd`、`cron` 或类似调度器定时运行 Agent 任务，而任务本身依赖本地 server、环境变量或固定 Python 环境时。
- 稳定模式：不要让调度器直接执行业务脚本。先包一层 wrapper，统一完成工作目录切换、根目录 `.env` 加载、解释器固定和依赖服务可达性检查；只有 readiness probe 通过后才真正启动 observer / reflector 等任务。
- 证据：`periodic_jobs/ai_heartbeat/launchd/README.md`、`periodic_jobs/ai_heartbeat/launchd/run_observer.sh`、`periodic_jobs/ai_heartbeat/launchd/run_reflector.sh` 与 `contexts/memory/OBSERVATIONS.md` 的 2026-04-19 🟡 记录相互印证。
- 建议后续：如果未来新增别的定时 Agent 作业也复用同一层 wrapper，可整理成独立 skill，作为本地 Agent automation 的默认运维模板。
