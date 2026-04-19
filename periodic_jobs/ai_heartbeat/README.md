# AI Heartbeat

当前工作区使用的 Heartbeat 主实现。

当前推荐运行方式：

- `launchd` 负责常驻 OpenCode Server 和定时触发 observer / reflector
- `observer.py` 负责 L1 append-only 观测
- `reflector.py` 负责 L2 candidates 提炼
- `docs/CRONTAB.md` 只作为 cron 兼容参考保留

## 目录

- `observer.py`：每日 L1 Observer
- `reflector.py`：每周 L2 Reflector
- `opencode_client.py`：OpenCode Server 客户端
- `jobs/`：相关自动化任务
- `launchd/`：macOS 本地服务与定时任务配置
- `docs/KNOWLEDGE_BASE.md`：Observer / Reflector 的 SOP
- `docs/PRD.md`：记忆系统设计文档

## 依赖

- 本地 OpenCode Server
- OpenCode 中已配置可用 provider
- 根目录 `.env` 中的：
  - `OPENCODE_BASE_URL`
  - `OPENCODE_USERNAME`
  - `OPENCODE_PASSWORD`
  - 可选：`OPENCODE_MESSAGE_TIMEOUT`
  - 可选：`OPENCODE_AGENT`

## 用法

查看 Observer 参数：

```bash
.venv/bin/python periodic_jobs/ai_heartbeat/observer.py --help
```

运行某天的 Observer：

```bash
.venv/bin/python periodic_jobs/ai_heartbeat/observer.py 2026-04-19
```

指定模型运行：

```bash
.venv/bin/python periodic_jobs/ai_heartbeat/observer.py --model openai/gpt-5.4 2026-04-19
```

运行 Reflector：

```bash
.venv/bin/python periodic_jobs/ai_heartbeat/reflector.py --model openai/gpt-5.4
```

## 职责边界

- `observer.py`
  - 写入 `contexts/memory/OBSERVATIONS.md`
  - 先做日期级幂等检查
  - 不修改 `rules/`
- `reflector.py`
  - 读取 `OBSERVATIONS.md`
  - 写入 `contexts/reflection/*_candidates.md`
  - 不直接晋升到 `rules/`

## 推荐测试顺序

不要并发测试 `observer` 和 `reflector`。

正确顺序：

1. 跑 `observer.py <date>`
2. 确认 `OBSERVATIONS.md` 已写入该日期
3. 再跑 `reflector.py`
4. 检查三个 candidate 文件

## 日志与排障

- `launchd` 安装说明：`periodic_jobs/ai_heartbeat/launchd/README.md`
- 常驻 server 日志：`/tmp/agentic-workspace-opencode-server.out.log`
- observer 日志：`/tmp/agentic-workspace-heartbeat-observer.out.log`
- reflector 日志：`/tmp/agentic-workspace-heartbeat-reflector.out.log`

## 当前默认模型

- `observer.py`：`openai/gpt-5.4`
- `reflector.py`：`openai/gpt-5.4`

都可以通过 `--model` 覆盖。
