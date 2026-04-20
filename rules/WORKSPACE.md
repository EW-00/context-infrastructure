# WORKSPACE.md - 目录路由速查

目标：让 AI 每轮 session 都能快速知道"去哪里找/放什么"。**找任何文件前先查这里。**

## 当前阶段

当前仓库已完成项目目录迁移：

- 仓库根目录暂时承载未来 workspace 里的 `core/` 角色
- 新项目结构优先使用 `projects/`

## 路由规则

### 项目与代码
- 项目域工作区：`projects/<project>/`
- 项目代码仓库：`projects/<project>/repos/`
- 项目高信号文档：`projects/<project>/docs/`
- 项目原始上下文：`projects/<project>/notes/`
- Lite 项目原始素材：`projects/<project>/materials/`
- Lite 项目产物输出：`projects/<project>/artifacts/`
- 工具脚本（邮件、语义搜索、分享报告等）：`tools/`
- 定时任务：`periodic_jobs/`

### 知识与记录
- 通用调研报告：`contexts/survey_sessions/`
- 思考 / 复盘 / 方法论：`contexts/thought_review/`
- 全局每日记录：`contexts/daily_records/`
- Lite 项目学习笔记：`projects/<project>/notes/learning_notes/`
- Standard / Heavy 项目每日记录：`projects/<project>/notes/daily/`
- Heavy 项目会议记录：`projects/<project>/notes/meetings/`
- Standard / Heavy 项目 handoff：`projects/<project>/handoffs/`
- Standard / Heavy 项目聊天蒸馏：`projects/<project>/chat_session_distillations/`
- Heavy 项目消息存档：`projects/<project>/notes/messages/`
- Heavy 项目 Notion 本地镜像：`projects/<project>/notes/notion_mirror/`

### 系统与规则
- 跨项目共享核心层：仓库根目录下的 `rules/`、`contexts/`、`tools/`、`periodic_jobs/`
- 可复用技术方案 / Skill：`rules/skills/`
- 核心公理（Axioms）：`rules/axioms/`
- 记忆系统：`contexts/memory/` + `periodic_jobs/ai_heartbeat/`

## 命名规则
- 目录和文件名：小写 + 下划线 (snake_case)
- 临时一次性项目：`tmp_<name>/`
- 项目域名称：优先使用稳定项目名；模板目录使用 `heavy_template/`
- 项目模板：允许 Lite / Standard / Heavy 共存，不要求每个项目目录完全同构

## Python 环境
- 根目录 `.venv/` 为工作区级环境，用 `uv pip install` 管理依赖
- 需要隔离时优先在 `projects/<project>/repos/<repo>/.venv/` 建独立环境

## 快速查询

<!-- 随着你的项目增长，在这里添加活跃项目的快捷路由 -->
<!-- 格式：- `project-name` → `projects/project_name/` (说明) -->
- `heavy_template` → `projects/heavy_template/` (Heavy 项目模板；复制后作为复杂项目的起点)
