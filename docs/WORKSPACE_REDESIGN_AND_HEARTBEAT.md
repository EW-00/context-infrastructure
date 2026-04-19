# Workspace 重构蓝图与 Heartbeat 数据流设计

## 当前状态

这份文档同时承担两种角色：

- 已落地的结构说明
- 未来跨机器演进的设计蓝图

当前已经落地的部分：

- 仓库根目录暂时扮演未来 `core/` 的角色
- `projects/` 已经成为项目主入口
- `heavy_template/` 已存在
- `periodic_jobs/ai_heartbeat/` 已从模板态变成可运行实现
- macOS 主路径已经是 `launchd + OpenCode Server + observer/reflector`

仍属于未来态的部分：

- 真正把仓库根目录物理拆成 `core/`
- Notion 镜像工具
- 双机共享层的月度同步流程

## 1. 目标

这份文档定义这套系统未来的目标形态。目标不是保留原 repo 的目录表面，而是保留它的核心思想，并将结构改造成更贴近实际工作流的形式。

目标有三条：

1. AI 在日常工作中能同时读到你的共享心智层和真实项目代码。
2. 每个项目域都有自己的完整上下文，不和其他项目混在一起。
3. Heartbeat 在每台机器本地运行，持续提炼工作流，但只把审核后的通用规则进入共享层。

## 2. 已确认的设计决策

- `McKinsey laptop` 和 `personal laptop` 都运行同一套系统骨架。
- 两台机器都保留完整本地系统，但内容不同。
- `core/` 是跨项目共享的心智层，不承载项目专属内容。
- 项目相关内容按项目域聚合；复杂项目可以从 `heavy_template/` 复制起步。
- Cursor 平时打开的是共同上级目录，而不是单独打开 `core/` 或某个 repo。
- 工作侧 Heartbeat 每天固定运行一次。
- 工作侧高价值输入优先级：`handoff`、代码实现中的反复模式、Notion 镜像。
- 项目状态页是手动维护、AI 辅助更新，不交给 Heartbeat 自动主写。
- `observations` 默认本地保存，不直接共享。
- 共享层同步采用手动审核。最保守的同步通道是 Markdown 经过 Notion 中转，再在另一台机器落盘。

## 3. 推荐拓扑

这一节描述的是未来更完整的目标拓扑，不是当前文件系统已经物理变成了 `core/`。

推荐将当前的单 repo 工作方式升级为一个更高一级的 workspace 根目录。

```text
<workspace-root>/
  core/
    rules/
      SOUL.md
      USER.md
      COMMUNICATION.md
      WORKSPACE.md
      skills/
      axioms/
    contexts/
      memory/
        observations.md
      reflection/
        skill_candidates.md
        axiom_candidates.md
        sync_candidates.md
    tools/
      notion_sync/
      heartbeat/
      semantic_search/
    periodic_jobs/
    docs/

  projects/
    heavy_template/
      repos/
        agentic-ai/
        data-science/
      docs/
        project_state.md
        architecture.md
        decisions.md
        repo_map.md
      handoffs/
      notes/
        daily/
        meetings/
        messages/
        notion_mirror/
          md/
          json/
```

这个结构的核心含义是：

- `core/`：定义你是谁，怎么思考，AI 该怎么工作。
- `projects/heavy_template/`：定义 Heavy 项目的标准骨架，复制后再替换成真实项目名。
- `repos/`：真实代码仓库。
- `docs/`：项目级高信号文档。
- `notes/`：项目级原始上下文和镜像输入。

## 4. 为什么不用“所有内容都塞进 core”

原结构里，`context-infrastructure` 这个旧名字对应的目录同时承担了三种职责：

- 共享规则层
- 项目上下文层
- 真实代码容器

这在项目很少时勉强可用，但对长期多项目工作流不成立。问题有三类：

1. 项目上下文会混在一起，长期难以维护。
2. 旧的 ad hoc 命名和真实工作方式不一致。
3. Heartbeat 很难判断什么是共享规律，什么只是某个项目的临时状态。

重构后，这三层职责分开：

- 共享规则进 `core/`
- 项目上下文进 `projects/<project>/`
- 代码放在项目自己的 `repos/`

## 5. 全局层和项目层的边界

### 5.1 永远属于 `core/` 的内容

- `SOUL.md`
- `USER.md`
- `COMMUNICATION.md`
- `WORKSPACE.md`
- 可跨项目复用的 `skills`
- 足够抽象、跨场景稳定的 `axioms`
- 本机本地的 `observations.md`
- 候选反思文件，例如 `skill_candidates.md`
- Heartbeat 和 Notion 同步脚本

### 5.2 永远属于项目域的内容

- 项目代码仓库
- 项目总览或状态文档
- 项目专属设计文档
- 项目专属决策文档
- handoff 记录
- 每日工作笔记
- 会议记录
- 消息草稿
- Notion 工作镜像

### 5.3 不直接共享的内容

- `contexts/memory/observations.md`
- `projects/*/notes/`
- `projects/*/docs/project_state.md`
- 客户相关代码、数据、决策细节

### 5.4 允许进入共享层的内容

- 经过你审核后的通用 `skills`
- 经过你审核后的通用 `axioms`
- 适合共享的 `SOUL` / `USER` / `COMMUNICATION` 更新

## 6. 项目域模板

`projects/` 下面不应只有一种固定结构。更合理的做法是保留统一语义，再根据项目复杂度选不同模板。

统一语义只有两条：

- 真实代码放 `repos/`
- 项目级上下文放 `docs/` 和 `notes/`

除此之外，目录深度和文件数量应该按项目复杂度裁剪。

### 6.1 Lite 项目

适合小型个人项目、学习型项目、低协作成本项目，例如 `mo_book`。

```text
projects/<project>/
  docs/
    overview.md
  notes/
    learning_notes/
  repos/                # optional
    <repo>/
  materials/            # optional
  artifacts/            # optional
```

特点：

- 用一个 `overview.md` 覆盖项目目的、repo 入口、当前关注点
- `repos/` 是可选的，只有存在真实代码仓库时才需要
- `materials/` 适合课程资料、PDF、原始素材
- `artifacts/` 适合转录稿、分析结果、导出产物
- 不强制要求 `project_state.md`
- 不强制要求 `architecture.md`
- 不强制要求 `decisions.md`
- 不强制要求 `handoffs/`

### 6.2 Standard 项目

适合中等复杂度的个人项目，已经开始需要追踪进展，但还没有到多团队协作级别。

```text
projects/<project>/
  repos/
  docs/
    project_state.md
    repo_map.md
  notes/
    daily/
  handoffs/
```

特点：

- 保留最必要的进展与索引文档
- handoff 可选，但通常有价值
- 适合需要跨多次对话持续推进的项目

### 6.3 Heavy 项目

适合多 repo、高复杂度、决策密度高的 Heavy 项目；模板目录名为 `heavy_template`。

```text
projects/<project>/
  repos/
  docs/
    project_state.md
    architecture.md
    decisions.md
    repo_map.md
  handoffs/
  notes/
    daily/
    meetings/
    messages/
    notion_mirror/
      md/
      json/
```

特点：

- 项目状态页作为高信号面板
- 设计和决策文档长期维护
- handoff 和 Notion 镜像都是高价值输入

### 6.4 选型原则

- 如果项目主要是自己学习和做实验，默认从 Lite 开始
- 如果项目开始出现跨多次会话的持续推进，升级到 Standard
- 如果项目有多 repo、设计权衡密集、需要项目级全局视图，升级到 Heavy

升级应该是渐进的，不需要一开始就铺满所有目录。

## 7. Heartbeat 的职责重定义

原 repo 的设计里，Heartbeat 基于 OpenCode Server 模板脚本。对你的使用场景，这个设计思想可以保留，但实现方式应该重写。

Heartbeat 不应依赖 Cursor 本身，也不应尝试抓取所有外部系统。第一阶段只需要稳定处理以下输入。

### 7.1 每日 Observer 的输入优先级

1. `projects/<project>/notes/handoffs/`
2. `projects/<project>/repos/*` 的最近变更
3. `projects/<project>/notes/notion_mirror/`
4. `projects/<project>/docs/project_state.md` 或 `projects/<project>/docs/overview.md`

说明：

- `handoff` 是高价值输入，因为它浓缩了任务上下文切换点，但 Lite 项目可以不存在。
- 代码变更是高价值输入，因为它最直接反映设计和实现上的真实推进。
- Notion 更适合补 daily log、meeting、message 这类背景信息，不是主要的 skill 提炼来源。
- `project_state.md` 或 `overview.md` 是高信号面板，Observer 应读它，但不自动主写它。

### 7.2 每日 Observer 的输出

Observer 每天运行一次，输出写回本机的 `core/`，不写回项目目录。

建议写这三个目标文件：

- `contexts/memory/observations.md`
  - 当日高价值观察
  - 仍然采用 `Date: YYYY-MM-DD` 形式
  - 重点记录跨天仍有价值的内容，而不是流水账
- `contexts/reflection/skill_candidates.md`
  - 候选 skill
  - 记录触发场景、复用价值、证据片段
- `contexts/reflection/axiom_candidates.md`
  - 候选 axiom
  - 只记录高抽象、反复出现的判断模式

### 7.3 Weekly Reflector 的职责

每周 Reflector 负责：

- 清理低价值观察
- 合并重复主题
- 将足够稳定的方法整理为候选 `skills`
- 将足够稳定的判断整理为候选 `axioms`
- 将“可能值得跨机器共享”的内容写入 `sync_candidates.md`

注意：Reflector 不应自动修改共享层。共享仍然需要你审核。

### 7.4 Monthly Sync 的职责

每月或按需执行一次：

1. 阅读 `sync_candidates.md`
2. 你手动审核
3. 选择少量内容作为共享更新
4. 通过 Notion 或其他合规通道转移到另一台机器
5. 在另一台机器对应落盘

## 8. Notion 在系统中的角色

Notion 不是主记忆库，而是项目原始输入源之一。

它适合承载：

- daily to-do
- 短笔记
- 会议记录
- 消息和邮件草稿

它不适合直接作为最终记忆层，原因有两点：

1. Heartbeat 和本地 AI 更容易稳定处理本地文件系统。
2. 本地文件更适合后续做语义搜索、版本管理和自动提炼。

因此推荐做法是：

- 用 Notion API 拉取指定页面/数据库
- 本地保留 `Markdown + JSON` 双轨镜像
- Heartbeat 读取镜像，不直接依赖在线 Notion 页面

## 9. API 与依赖要求

第一阶段只需要两类外部能力。

### 9.1 Notion 读取能力

需要：

- 一个 Notion integration token
- 需要同步的数据库或页面 ID
- 仅授权工作相关页面

输出：

- `projects/<project>/notes/notion_mirror/md/`
- `projects/<project>/notes/notion_mirror/json/`

### 9.2 LLM 调用能力

Heartbeat 需要一个可脚本调用的稳定模型入口，例如：

- OpenAI API
- Anthropic API
- Gemini API
- 你未来使用的其他稳定 endpoint

Heartbeat 不应绑定到 Cursor chat 本身。Cursor 负责交互式工作，Heartbeat 负责可重复的后台提炼。

## 10. 两台机器的关系

### 10.1 `McKinsey laptop`

特点：

- 是工作侧主机
- 会长期保留
- 是工作版 Heartbeat 的主要运行位置

内容：

- `core/` 的本地副本
- 工作项目域，例如从 `projects/heavy_template/` 复制出的真实项目目录
- 工作侧 `observations.md`

### 10.2 `personal laptop`

特点：

- 承载个人项目、研究和学习
- 也会产出共享心智层的更新

内容：

- `core/` 的本地副本
- 个人项目域
- 个人侧 `observations.md`

### 10.3 一致与不一致

两台机器：

- 结构应一致
- 心智层理念应一致
- 共享 skill / axiom 逐步趋同

但它们：

- `observations.md` 不同
- 项目目录不同
- 项目状态页不同
- Notion 镜像不同

## 11. 实施顺序

建议按以下顺序推进。

### Phase 1. 结构定稿

- 确认 workspace 根目录结构
- 确认 `core/` 和 `projects/` 并列
- 确认 `heavy_template/` 的目录骨架

### Phase 2. 项目域文档骨架

- 建立 `project_state.md`
- 建立 `architecture.md`
- 建立 `decisions.md`
- 建立 `repo_map.md`

### Phase 3. Notion 镜像

- 建立 Notion integration
- 指定数据库和页面
- 实现 `Markdown + JSON` 镜像落盘

### Phase 4. 重写 Observer

- 移除模板脚本里的占位符
- 改为读取 handoff、git 变更、Notion 镜像
- 输出到本地 `observations.md` 和候选文件

### Phase 5. 重写 Reflector

- 从 observation 提炼候选 skill / axiom
- 生成 `sync_candidates.md`

### Phase 6. 月度共享同步

- 审核 `sync_candidates.md`
- 通过 Notion 或其他合规方式同步少量共享规则

## 12. 对现有 repo 的具体影响

这份蓝图落地后，现有 repo 至少需要做以下调整：

- 旧的平铺项目目录退出核心地位
- `rules/WORKSPACE.md` 按新结构重写
- `periodic_jobs/ai_heartbeat/observer.py` 重写
- `periodic_jobs/ai_heartbeat/reflector.py` 重写
- `contexts/memory/OBSERVATIONS.md` 迁移为本机本地 `observations.md`
- 新增 Notion 镜像工具
- 新增项目域文档模板

## 13. 一句话原则

这套系统未来的基本原则是：

共享的东西放进 `core/`，项目的东西放进项目域，本地观察留在本地，只有你审核后的通用方法论才进入跨机器共享层。
