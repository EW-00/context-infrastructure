# Skill: 任务交接协议（Task Handoff Protocol）

## When to Use

- 用户说"checkpoint"、"存档"、"写交接"、"handoff"
- 用户说"继续 XX 任务"、"resume XX"
- Context window 消耗较大，主动提议做一次 checkpoint
- 任务到达阶段性节点

## 定位项目

Handoff 按项目域组织，存放在 `projects/<project>/handoffs/`。

1. 如果当前对话已在某个项目上下文中工作，直接使用该项目
2. 如果用户指定了项目名，用 WORKSPACE.md 快速查询定位
3. 如果不确定，扫描 `projects/*/handoffs/INDEX.md` 找到匹配的任务

## 创建新任务

1. 确定目标项目（见"定位项目"）
2. 在 `projects/<project>/handoffs/` 下创建目录（snake_case）
3. 创建 `HANDOFF.md`，填写下方模板
4. 更新 `projects/<project>/handoffs/INDEX.md`

## 写交接（Checkpoint / Handoff）

更新 `HANDOFF.md`，确保覆盖以下所有区块：

```markdown
# Task: <任务名>
Updated: YYYY-MM-DD HH:MM

## Objective
一句话：最终要达成什么。

## Key Decisions
- 决策 1：选了 X，因为 Y（排除 Z 的原因）
- 决策 2：...

## Current Status
- [x] 已完成的步骤
- [ ] 🔵 当前进行中（卡点/进展）
- [ ] 待做的步骤

## Important Context
- 关键文件与作用
- 已知坑和绕过方式
- 外部依赖（API、服务、数据）

## Open Questions
- 待确认事项
- 需要用户决策的问题
```

### 写交接的原则

- **写给下一个完全没有上下文的 AI**，不要假设它知道任何之前的对话
- **决策背景比结论更重要**——写清楚"为什么"，不只是"是什么"
- **文件路径要具体**——写 `projects/<project>/repos/repo-name/path/to/file.py` 的 `ClassName.method()`，不要写"那个文件"
- **状态要可执行**——下一步能直接动手，不需要再问"从哪开始"

## 恢复任务（Resume）

用户说"继续 XX"时：

1. 定位项目（见"定位项目"）
2. 读 `projects/<project>/handoffs/INDEX.md` 找到任务目录
3. 读该任务的 `HANDOFF.md`
4. 向用户确认当前状态是否准确，有无新变化
5. 从 Current Status 中第一个未完成项开始工作

## 完成任务

1. 更新 `HANDOFF.md`，所有步骤标记完成
2. 在 `INDEX.md` 中将任务从"任务列表"移到"归档"
3. 如有跨任务通用的经验教训，写入 `contexts/memory/OBSERVATIONS.md`

## 主动提醒时机

当以下条件成立时，主动建议用户做 checkpoint：
- 对话已经很长，且完成了一个阶段性目标
- 即将开始一个可能出错需要回退的操作
- 用户明确说"今天先到这"或类似结束信号
