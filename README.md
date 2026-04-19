# Agentic Workspace — Reference Implementation

> 背景阅读：[为什么AI只会说正确的废话，以及怎么把它逼出舒适区](https://yage.ai/context-infrastructure.html)

这是一个运行了一年的 context infrastructure 系统的完整结构。主要价值是作为 reference implementation，让你看到系统长什么样、数据如何流动、记忆如何积累。

**核心定位**：这不是开箱即用的产品，而是一套可改造的工作流骨架。Clone 下来后，你可以立刻体验「有 context vs 没有 context」的差异；但要让 AI 真正变成你自己的，需要继续替换路径、项目结构、记忆来源和高频技能。

**当前这份仓库的真实状态**：

- 仓库根目录暂时扮演未来 `core/` 的角色
- 项目内容已经迁入 `projects/`
- Heartbeat 主路径已经是 `launchd + OpenCode server + observer/reflector`
- `cron` 只作为兼容参考保留，不再是推荐主方案

---

## Quick Start（5 分钟）

```bash
git clone https://github.com/grapeot/context-infrastructure agentic-workspace
cd agentic-workspace
# 用 Claude Code / OpenCode / Cursor 打开这个目录
```

然后：打开 [`rules/USER.md`](rules/USER.md)，填写你的基本信息。这是 ROI 最高的一步，完成后 AI 的行为立刻个性化。

详细步骤见 [`setup_guide.md`](setup_guide.md)。

---

## 目录结构

```
agentic-workspace/
├── AGENTS.md                    # 根路由表（AI 每次 session 的起点）
├── setup_guide.md               # 配置指引
├── .env.example                 # 环境变量模板
│
├── docs/
│   ├── CRONTAB.md               # cron 兼容参考（非 macOS 主路径）
│   └── WORKSPACE_REDESIGN_AND_HEARTBEAT.md
│
├── rules/
│   ├── SOUL.md                  # AI 的身份和行为基调（模板）
│   ├── USER.md                  # 你的偏好和背景（模板）
│   ├── COMMUNICATION.md         # 沟通风格指南（可直接用）
│   ├── WORKSPACE.md             # 目录路由索引
│   ├── axioms/                  # 43 条决策公理（展示层）
│   └── skills/                  # 25+ 个可复用 skill（展示层）
│
├── contexts/
│   ├── memory/
│   │   └── OBSERVATIONS.md      # 三层记忆系统的 L1/L2 层
│   ├── survey_sessions/         # 调研报告存放目录
│   ├── daily_records/           # 日常记录存放目录
│   └── thought_review/          # 思考复盘存放目录
│
├── periodic_jobs/
│   └── ai_heartbeat/
│       ├── docs/
│       │   ├── PRD.md           # 记忆系统设计文档
│       │   └── KNOWLEDGE_BASE.md # 观察和反思的 SOP
│       ├── observer.py          # 每日观察脚本
│       ├── reflector.py         # 每周反思脚本
│       ├── opencode_client.py   # OpenCode Server 客户端
│       ├── launchd/             # macOS 主方案：server 常驻 + observer/reflector 定时任务
│       └── jobs/                # 相关自动化任务
│
├── tools/
│   ├── semantic_search/         # 语义搜索（Tier 2）
│   └── share_report/            # 报告发布（Tier 2）
│
└── projects/                    # 项目域工作区
```

---

## 当前推荐理解

**展示层（可以参考，不能复制）**：[`rules/axioms/`](rules/axioms/) 和 [`rules/skills/`](rules/skills/) 包含了这个系统积累一年的内容。它们展示了“如何沉淀”，不代表你应该直接继承其具体结论。

**可复用层（可直接落地）**：[`rules/SOUL.md`](rules/SOUL.md)、[`rules/USER.md`](rules/USER.md)、[`rules/COMMUNICATION.md`](rules/COMMUNICATION.md)、[`rules/WORKSPACE.md`](rules/WORKSPACE.md) 与 [`periodic_jobs/ai_heartbeat/`](periodic_jobs/ai_heartbeat/) 共同组成当前的核心工作流。macOS 上优先走 [`periodic_jobs/ai_heartbeat/launchd/`](periodic_jobs/ai_heartbeat/launchd/)。

**项目层（你自己的工作内容）**：[`projects/`](projects/) 下的 Lite / Standard / Heavy 项目域是本地工作区的主入口。AI 需要同时看到项目代码、项目文档和共享规则层，才会真正“懂你的工作”。

## 推荐阅读顺序

1. [`setup_guide.md`](setup_guide.md)
2. [`rules/WORKSPACE.md`](rules/WORKSPACE.md)
3. [`projects/README.md`](projects/README.md)
4. [`periodic_jobs/ai_heartbeat/README.md`](periodic_jobs/ai_heartbeat/README.md)
5. [`docs/WORKSPACE_REDESIGN_AND_HEARTBEAT.md`](docs/WORKSPACE_REDESIGN_AND_HEARTBEAT.md)

---

## License

MIT
