# AI Heartbeat: 渐进式披露记忆系统产品需求文档 (PRD)

## 1. 产品概述

### 1.1 愿景
构建一个**Agentic 驱动的、全局统一但按需披露的观测记忆系统**。彻底摆脱由外部脚本“拼凑 Prompt 并喂给 AI”的低级模式，转而让 OpenCode Agent 在接收到简单的“路径与目标”后，自主探索文件系统、分配子任务并提纯观测结果。系统遵循 **Progressive Disclosure** 理念：记忆池是全局的，但 Agent 接收到的上下文始终保持稀疏（Sparse）和高密度（High Density）。

### 1.2 核心价值主张
- **Agentic 自主探索**: 脚本只负责触发任务和提供线索（文件路径），AI 负责阅读、过滤（如排除仅格式变动的 Blog）和总结。
- **渐进式披露 (Progressive Disclosure)**: 默认不加载详细记忆，仅由 Agent 根据当前任务逻辑主动检索相关的 L1/L2 观测点。
- **全局分层架构**: 
  - **L3**: 全局硬性约束（存放在 `rules/`，全局被动加载）。
  - **L1/L2**: 动态观测日志（存放在全局记忆池，Agent 主动检索）。
- **抗噪设计**: 利用 AI 的语义理解能力识别真正的“新内容”。例如，针对 300+ 篇 Blog 的格式变动，AI 应通过检查元数据（Metadata）中的创建日期来识别真正的新文章。

### 1.3 目标用户
- **OpenCode Agent**: 作为记忆的生产者和核心消费者。
- **开发者**: 仅作为系统边界的定义者和记忆日志的最终审计者。

---

## 2. 核心设计原则 (The Agentic Way)

### 2.1 拒绝 Push 模式，拥抱 Pull 模式
传统的系统试图把所有 Context “推送”给模型。本系统要求 Agent 具备“拉取”意识。脚本告诉 Agent：“这些文件变了，去把有价值的 lessons 学回来”，Agent 应该自己决定读什么、读多少。

### 2.2 记忆稀疏性假设 (Sparse Context Assumption)
我们假设：对于任何给定任务，真正相关的记忆是极少数的。因此，全局记忆池（OBSERVATIONS.md）允许不断增长，但 Agent 必须能够通过标签（Tags）或关键字进行高效的局部加载。

### 2.3 零摩擦资产化
记忆日志采用纯文本追加模式。它不仅是 Agent 的运行状态机，也是开发者的知识资产。

---

## 3. 功能需求：三层分级体系

### 3.1 L3: 全局约束与哲学 (Global Constraints)
- **内容**: 存放于 `rules/SOUL.md` 和 `rules/USER.md`。
- **硬性约束**: 必须包含语言风格约束（不准用大词、不准用营销词、不准用引号、尽量避免 "not" 负向句式）、应对策略等。
- **加载方式**: Session 启动时被动全局加载。

### 3.2 L1: 每日观测与心跳 (Daily Observation)
- **内容**: 过去 24 小时的关键事件、技术决策、真实的错误修复经验。
- **打标格式**: `🔴 High (方法论/约束)`、`🟡 Medium (项目状态/决策)`、`🟢 Low (任务流水)`。
- **产生方式**: 脚本仅负责触发一个独立的 Observer Session，并提供根目录、日期与 SOP。Agent 自主扫描 workspace、过滤噪音并将结果追加到 `contexts/memory/OBSERVATIONS.md`。

### 3.3 L2: 记忆蒸馏与反思 (Weekly Reflection)
- **职责**: 垃圾回收。
- **逻辑**: 每周运行，AI 自主读取 L1 记忆池，删除过期的 🟢，合并同主题的 🟡，并将稳定模式先写入候选层：
  - `contexts/reflection/skill_candidates.md`
  - `contexts/reflection/axiom_candidates.md`
  - `contexts/reflection/sync_candidates.md`
- **人工审核边界**: 候选层内容经人工审核后，才会进入 `rules/` 或其他长期规则层。

---

## 4. 关键业务流 (User Story)

### 4.1 智能体自发的心跳任务
1. **触发**: macOS 主路径由 `launchd` 定时触发脚本；`cron` 仅作为兼容参考。
2. **输入**: 脚本提供目标日期、workspace 根目录与 SOP 路径。
3. **分配**: 脚本启动一个独立的 OpenCode Session。
4. **指令**: “基于这一天的变动，自主扫描 workspace、过滤噪音，并写入观测记录或候选层。”
5. **执行**: Agent 看到任务后，自主读取 L3 约束、扫描项目域、判断哪些变动值得进入长期记忆。
6. **产出**: 结果 Append 到全局 `contexts/memory/OBSERVATIONS.md`。

---

## 5. 技术约束与集成

- **执行引擎**: 本地 OpenCode Server（默认 `127.0.0.1:4096`，由 `.env` 与 `launchd` 配置驱动）。
- **核心模型**: 当前默认使用 `openai/gpt-5.4`，可通过命令行参数覆盖。
- **Agent Identity**: 当前默认使用 OpenCode 的 `build` agent，可通过 `.env` 中的 `OPENCODE_AGENT` 覆盖。
- **记忆存储**: Markdown 文件（支持 Git 版本控制）。
