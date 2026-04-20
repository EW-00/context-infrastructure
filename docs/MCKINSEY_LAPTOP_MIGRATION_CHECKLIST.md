# McKinsey Laptop Migration Checklist

这份清单的目标是：把当前个人电脑上已经跑通的 `agentic-workspace` 迁到 McKinsey laptop，同时保持更严格的工作内容边界。

核心原则：

- 工作电脑也使用同一套 `agentic-workspace` 骨架
- 共享核心层继续放在根仓库
- `projects/` 作为本地工作区存在，供 AI 阅读
- `projects/<project>/...` 不进入根仓库 git 历史
- 真正跨机器共享的，只是提炼后的 `rules/`、`contexts/`、`docs/`

## 0. 迁移前确认

开始之前，先确认这几件事在 McKinsey laptop 上可行：

- 可以 clone 私有仓库
- 可以安装 `opencode`
- 可以运行本地 `launchd`
- 可以使用 OpenAI API 或其他可在 OpenCode 中配置的 provider
- 允许本地保存工作相关的 `docs/`、`notes/`、handoff 等文件

如果这些都成立，就可以按下面的步骤迁移。

## 1. 在工作电脑上 clone 仓库

建议路径：

```bash
cd ~/Repos
git clone <your-private-repo-url> agentic-workspace
cd agentic-workspace
```

说明：

- 工作电脑上也沿用 `agentic-workspace` 这个目录名
- 这样 `launchd`、脚本路径、文档里的本地说明都更一致

## 2. 安装依赖

### 2.1 Python 环境

如果工作电脑还没有根目录 `.venv`：

```bash
uv venv
```

然后按当前仓库里真正需要的依赖安装。优先使用你已经在个人电脑验证过的依赖清单，不要一开始就扩展到所有可选工具。

### 2.2 OpenCode

确保以下命令可用：

```bash
opencode --help
opencode serve --help
```

如果还没装，可以沿用个人电脑已经验证过的安装方式。

## 3. 配置 OpenCode 凭证与本地 `.env`

### 3.1 先选 OpenAI 凭证来源

工作电脑上有两种可行方式：

#### 方案 A：让 OpenCode 自己管理 provider 凭证

直接登录 OpenAI：

```bash
opencode providers login
```

适合：

- heartbeat 主要通过 OpenCode 跑
- 不希望把 `OPENAI_API_KEY` 放进 repo 本地 `.env`

#### 方案 B：在 repo 本地 `.env` 里放 `OPENAI_API_KEY`

适合：

- 除了 OpenCode 之外，你还有别的脚本会直接读取 `OPENAI_API_KEY`
- 你希望统一用 `.env` 管理本地凭证

当前这台个人电脑实际使用的是 **方案 A**。  
也就是说，OpenCode 通过自己的本地凭证存储管理 OpenAI provider，不依赖这个 repo 的 `.env`。

### 3.2 配置工作电脑本地 `.env`

根目录创建 `.env`，至少包含：

```bash
OPENCODE_BASE_URL=http://localhost:4096
OPENCODE_USERNAME=opencode
OPENCODE_PASSWORD=<local-password>
OPENCODE_MESSAGE_TIMEOUT=3600
OPENCODE_AGENT=build
```

说明：

- `.env` 只保留在本地，不进入 git
- 如果你选择 **方案 B**，再额外加入：

```bash
OPENAI_API_KEY=<your-api-key>
```

- 如果你选择 **方案 A**，`.env` 里不需要 `OPENAI_API_KEY`
- 如果你以后要让工作电脑用别的 provider，可以再改 OpenCode 的 provider 配置，不影响这份 checklist

## 4. 安装 Heartbeat 的 launchd

先确保 wrapper 可执行：

```bash
chmod +x periodic_jobs/ai_heartbeat/launchd/*.sh
```

再安装 LaunchAgents：

```bash
cp periodic_jobs/ai_heartbeat/launchd/*.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.erqianwang.agentic-workspace.opencode-server.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.erqianwang.agentic-workspace.heartbeat-observer.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.erqianwang.agentic-workspace.heartbeat-reflector.plist
```

如果之前装过旧版本，先 `bootout` 再 `bootstrap`。

## 5. 验证基础链路

### 5.1 验证 OpenCode Server

确认 launch agent 正在运行：

```bash
launchctl print gui/$(id -u)/ai.erqianwang.agentic-workspace.opencode-server
```

日志应能看到：

```text
opencode server listening on http://127.0.0.1:4096
```

日志路径：

- `/tmp/agentic-workspace-opencode-server.out.log`

### 5.2 验证 observer

```bash
.venv/bin/python periodic_jobs/ai_heartbeat/observer.py 2026-04-19
```

检查：

- `contexts/memory/OBSERVATIONS.md` 新增 `Date: ...`

### 5.3 验证 reflector

```bash
.venv/bin/python periodic_jobs/ai_heartbeat/reflector.py
```

检查：

- `contexts/reflection/skill_candidates.md`
- `contexts/reflection/axiom_candidates.md`
- `contexts/reflection/sync_candidates.md`

### 5.4 验证 launchd 触发

```bash
launchctl kickstart -k gui/$(id -u)/ai.erqianwang.agentic-workspace.heartbeat-observer
launchctl kickstart -k gui/$(id -u)/ai.erqianwang.agentic-workspace.heartbeat-reflector
```

检查日志：

- `/tmp/agentic-workspace-heartbeat-observer.out.log`
- `/tmp/agentic-workspace-heartbeat-reflector.out.log`

## 6. 在工作电脑上建立项目域

工作侧项目仍然放在：

```text
projects/<project>/
```

但要记住：`projects/` 现在默认已经被根仓库 `.gitignore` 忽略，所以这里的内容是：

- AI 可读
- 本地可维护
- 不进入根仓库 git 历史

推荐工作流：

1. 新建 `projects/<project>/docs/`
2. 新建 `projects/<project>/notes/`
3. 在 `projects/<project>/repos/` 下放真实代码仓库
4. 让 AI 在工作时同时读：
   - 根目录共享规则层
   - `projects/<project>/docs/`
   - `projects/<project>/notes/`
   - `projects/<project>/repos/<repo>/`

## 7. 工作侧最小项目文档

复杂项目开始时，至少补这两份：

- `projects/<project>/docs/repo_map.md`
- `projects/<project>/docs/project_state.md`

这两份足够让 AI 先理解：

- 项目里有哪些 repo
- 当前目标是什么
- 下一步是什么
- 哪些问题还没解

如果设计密度上来，再继续补：

- `architecture.md`
- `decisions.md`
- `handoffs/`
- `notes/notion_mirror/`

## 8. 什么可以同步回共享层

不要直接同步整个工作项目目录。

工作电脑回流到共享层的，只应该是：

- 可复用 skill
- 值得长期保留的 axiom 候选
- 工作中验证出的通用方法论
- 对共享系统本身的改进

这些内容应该先落在：

- `contexts/reflection/skill_candidates.md`
- `contexts/reflection/axiom_candidates.md`
- `contexts/reflection/sync_candidates.md`

然后由你人工审核，再手动同步回个人电脑或共享主仓库。

## 9. 当前阶段不必先做的事

这些都不是 work laptop 迁移的 blocker，可以后置：

- Notion 自动同步
- Slack / Teams 聊天记录接入
- observer 扫描范围精细化
- 更复杂的候选层晋升自动化

先把基础闭环跑起来，再加输入源。

## 10. 验收标准

满足下面这些，就算 McKinsey laptop 迁移成功：

- 仓库已 clone 到 `agentic-workspace`
- `.env` 已配置
- OpenCode Server 可常驻
- observer 可手动跑
- reflector 可手动跑
- LaunchAgent 可 kickstart 成功
- `projects/` 下的工作内容不进入根仓库 git 历史
- AI 能同时读取共享规则层和工作项目内容

达到这一点后，工作电脑就进入可用状态。后面的工作主要是继续补项目文档和提高 heartbeat 质量，而不是再搭基础设施。
