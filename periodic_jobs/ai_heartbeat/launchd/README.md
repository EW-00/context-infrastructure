# launchd Setup

这组文件用于在 macOS 上把 Heartbeat 变成稳定可运行的本地服务。

包含三个 LaunchAgent：

- `ai.erqianwang.agentic-workspace.opencode-server.plist`
  - 登录后启动本地 OpenCode server
  - `KeepAlive=true`
- `ai.erqianwang.agentic-workspace.heartbeat-observer.plist`
  - 每天 8:00 AM 运行 observer
- `ai.erqianwang.agentic-workspace.heartbeat-reflector.plist`
  - 每周日 9:00 AM 运行 reflector

对应的 shell wrapper：

- `run_opencode_server.sh`
- `run_observer.sh`
- `run_reflector.sh`

这些 wrapper 会：

1. 切到 workspace 根目录
2. 读取根目录 `.env`
3. 使用 `.venv/bin/python`
4. 让 observer / reflector 在启动前等待本地 OpenCode server 可连接

安装目标目录：

```text
~/Library/LaunchAgents/
```

典型安装流程：

```bash
chmod +x periodic_jobs/ai_heartbeat/launchd/*.sh
cp periodic_jobs/ai_heartbeat/launchd/*.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.erqianwang.agentic-workspace.opencode-server.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.erqianwang.agentic-workspace.heartbeat-observer.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.erqianwang.agentic-workspace.heartbeat-reflector.plist
```

如需重载，可先 `bootout` 再 `bootstrap`。
