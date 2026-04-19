# Projects

项目相关内容按项目域聚合，而不是按文件类型混放。

每个项目域目录应尽量包含：

- `repos/`：真实代码仓库
- `docs/`：高信号项目文档
- `notes/`：daily log、meeting、message、handoff、Notion 镜像

目标是让 AI 能在同一个工作区里同时看到：

- 项目代码
- 项目级上下文
- 跨项目共享的规则层

Git 边界说明见 [docs/GIT_BOUNDARIES.md](/Users/erqianwang/Repos/agentic-workspace/docs/GIT_BOUNDARIES.md)。

当前默认策略：

- `projects/` 作为 AI 可读的本地工作区存在
- `projects/<project>/...` 默认不进入 workspace 根仓库的 git 历史
- 只有提炼后的共享知识才进入 `rules/`、`contexts/`、`docs/`

## 模板选择

- Lite：学习型项目、内容型项目、小型个人实验。通常只需要 `docs/overview.md`，再按需加 `materials/`、`artifacts/`、`repos/`。
- Standard：已经有持续推进、跨多次会话接力的项目。至少补 `docs/project_state.md` 和 `docs/repo_map.md`。
- Heavy：多 repo、设计密度高、需要项目级全局视图的项目。以 `heavy_template/` 为起点。

选择原则：

- 先从 Lite 开始
- 复杂度上升时再升级
- 不要一开始就把每个项目都铺成 Heavy
