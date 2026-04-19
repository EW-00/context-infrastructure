# Sync Candidates

记录可能值得跨机器共享的内容，最终是否同步由你审核决定。

## 2026-04-19

### Candidate: 跨机器同步的最小边界

- 候选内容：共享 `rules/`、审核后的 `skills` / `axioms`、以及候选层中已确认可迁移的抽象；保留 `contexts/memory/OBSERVATIONS.md` 为 machine-local，不直接跨机器同步。
- 为什么值得同步：这条边界直接决定多机器上的认知一致性和隐私控制，也能减少把临时项目噪音扩散到共享层的风险。
- 证据：`docs/WORKSPACE_REDESIGN_AND_HEARTBEAT.md`、`rules/WORKSPACE.md`、`contexts/memory/OBSERVATIONS.md` 的 2026-04-19 🔴 记录。
- 审核点：确认未来工作机和个人机都继续采用“本地观测 + 人工审核后同步抽象”的机制，再决定是否进入正式共享规则。
