# Crontab 配置指南（兼容参考）

本文档保留 cron 版定时任务示例，用于兼容非 macOS 环境或你明确偏好 cron 的情况。

对当前这份仓库，macOS 主路径已经是：

- `launchd` 常驻 OpenCode Server
- `launchd` 定时触发 observer / reflector

因此这份文档是兼容参考，不是推荐主方案。

---

## 参考时间线

```
3:05 AM   → Situation Awareness: 每日摘要 + 摄像头缓存刷新
4:00 AM   → Session Sync: 导出 AI session 归档
6:30 AM   → WeChat DB Parser: 导出每日消息为 CSV（如适用）
7:00 AM   → Daily Briefing: 生成个人晨报 → Email
8:00 AM   → AI Heartbeat Observer: 扫描文件变动，提取观察写入 OBSERVATIONS.md
Every 2m  → Situation Awareness: 快照采集（交通/摄像头/警报）
Every 12h → Situation Awareness: 风力预警检查
Weekly    → AI Heartbeat Reflector: 合并/提升/清理记忆
Daily     → Crontab Monitor: 健康审计，发现异常则发告警邮件
```

---

## 兼容任务说明

### AI Heartbeat Observer（每日）

扫描 workspace 文件变动，提取有价值的观察写入 `contexts/memory/OBSERVATIONS.md`。这是三层记忆系统的"输入端"。

- **脚本**：`periodic_jobs/ai_heartbeat/observer.py`
- **依赖**：OpenCode Server API（`OPENCODE_BASE_URL`）
- **建议时间**：每日 8:00 AM（在 daily briefing 之后）

### AI Heartbeat Reflector（每周）

合并、提升、清理 OBSERVATIONS.md 中积累的观察，蒸馏为更高层次的认知。

- **脚本**：`periodic_jobs/ai_heartbeat/reflector.py`
- **依赖**：OpenCode Server API（`OPENCODE_BASE_URL`）
- **建议时间**：每周日 9:00 AM

### Crontab Monitor（每日）

自主审计所有 crontab 任务的健康状态，发现异常时发送告警邮件。

- **脚本**：`periodic_jobs/ai_heartbeat/jobs/crontab_monitor.py`
- **依赖**：OpenCode Server API、Gmail（`GMAIL_USERNAME` / `GMAIL_APP_PASSWORD`）
- **建议时间**：每日 9:00 AM

### AI News Survey（每日/每周）

调用 AI Agent 生成 AI 行业日报或周报，可发布到 Kit 订阅者或发送个人邮件。

- **脚本**：`periodic_jobs/ai_heartbeat/jobs/ai_news_survey.py`
- **依赖**：OpenCode Server API、Gmail 或 Kit API
- **建议时间**：每日 8:00 AM（日报）或每周一 8:00 AM（周报）

---

## 示例 crontab 配置

将以下内容添加到 `crontab -e`。以下示例已替换为当前 workspace 实际路径：

- workspace 根目录：`/Users/erqianwang/Repos/agentic-workspace`
- Python：`/Users/erqianwang/Repos/agentic-workspace/.venv/bin/python`

前提：

1. 本地 OpenCode Server 已在 `http://localhost:4096` 运行
2. 根目录 `.env` 已配置 `OPENCODE_BASE_URL / OPENCODE_USERNAME / OPENCODE_PASSWORD`
3. `.env` 由脚本显式加载，不依赖 cron shell 自动 source

```cron
# ── 时区说明 ──────────────────────────────────────────────
# 以下时间均为本地时间。如需指定时区，在 crontab 顶部添加：
# TZ=America/Los_Angeles

# AI Heartbeat Observer — 每日 8:00 AM
0 8 * * * cd /Users/erqianwang/Repos/agentic-workspace && /Users/erqianwang/Repos/agentic-workspace/.venv/bin/python periodic_jobs/ai_heartbeat/observer.py >> /tmp/observer.log 2>&1

# AI Heartbeat Reflector — 每周日 9:00 AM
0 9 * * 0 cd /Users/erqianwang/Repos/agentic-workspace && /Users/erqianwang/Repos/agentic-workspace/.venv/bin/python periodic_jobs/ai_heartbeat/reflector.py >> /tmp/reflector.log 2>&1

# Crontab Monitor — 每日 9:00 AM
0 9 * * * cd /Users/erqianwang/Repos/agentic-workspace && /Users/erqianwang/Repos/agentic-workspace/.venv/bin/python periodic_jobs/ai_heartbeat/jobs/crontab_monitor.py >> /tmp/crontab_monitor.log 2>&1

# AI News Survey 日报 — 每日 8:00 AM（发个人邮件）
0 8 * * * cd /Users/erqianwang/Repos/agentic-workspace && /Users/erqianwang/Repos/agentic-workspace/.venv/bin/python periodic_jobs/ai_heartbeat/jobs/ai_news_survey.py --mode daily >> /tmp/ai_news_survey.log 2>&1

# AI News Survey 周报 — 每周一 8:00 AM（发布到 Kit 订阅者）
0 8 * * 1 cd /Users/erqianwang/Repos/agentic-workspace && /Users/erqianwang/Repos/agentic-workspace/.venv/bin/python periodic_jobs/ai_heartbeat/jobs/ai_news_survey.py --mode weekly --publish-to-kit >> /tmp/ai_news_weekly.log 2>&1
```

---

## 注意事项

1. **推荐优先级**：如果你在 macOS 上使用这套系统，优先看 `periodic_jobs/ai_heartbeat/launchd/README.md`，不要先从 cron 装起。
2. **OpenCode Server**：cron 只会触发 observer / reflector，不会自动拉起 OpenCode Server。你需要额外保证本地 server 常驻。
3. **虚拟环境**：脚本依赖 `.venv` 中的 Python 包，确保先运行 `uv pip install -r requirements.txt`（如有）。
4. **环境变量**：cron 环境不会自动加载 `.env`，建议在脚本中显式加载，或在 crontab 中用 `env $(cat .env | xargs)` 注入。
5. **时区**：macOS cron 默认使用系统时区；Linux 服务器建议在 crontab 顶部显式设置 `TZ=`。
6. **日志**：示例中日志写入 `/tmp/`，生产环境建议改为持久化路径（如 `logs/` 目录）。
7. **依赖顺序**：Observer 依赖当天的文件变动，建议在 daily briefing 和 news survey 之后运行（8:30 AM 以后）。
