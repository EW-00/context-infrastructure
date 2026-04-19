# Git Boundaries

这份文档定义当前 workspace 的 git 管理边界。

目标只有一个：`workspace` 根仓库只管理共享核心层。`projects/` 作为 AI 可读的本地工作区存在，但默认不进入根仓库的 git 历史。真实代码仓库各自独立管理，避免嵌套仓库互相污染。

## 推荐结构

当前推荐使用两层 git：

1. **workspace 根仓库**
   - 当前仓库本身
   - 管共享规则层、记忆系统、工具、定时任务、系统文档

2. **真实代码仓库**
   - 位于 `projects/<project>/repos/<repo>/`
   - 各自独立 branch、commit、push、PR

不建议再让 `projects/<project>/` 本身单独成为第三层 git repo。

原因：

- 一个项目域下可能有多个真实代码仓库
- 项目级 `docs/` 和 `notes/` 更适合作为 workspace 的一部分
- 如果再加一层 project repo，commit 边界会变得模糊

## Workspace 根仓库应该追踪什么

根仓库应该追踪：

- `rules/`
- `contexts/`
- `tools/`
- `periodic_jobs/`
- `docs/`
- `projects/README.md`

根仓库不应该追踪：

- `projects/<project>/docs/`
- `projects/<project>/notes/`
- `projects/<project>/materials/`
- `projects/<project>/artifacts/`
- `projects/<project>/repos/<repo>/` 里的真实代码仓库
- 各种项目本地 `.venv/`
- cache、build、logs、临时文件
- 大体积原始数据
- 纯运行产物

## 当前 workspace 的 ignore 规则

根仓库的 `.gitignore` 已经显式忽略：

```gitignore
/projects/*
!/projects/README.md
```

含义：

- `projects/` 下的项目内容默认都只存在于本地
- AI 仍然可以读取这些内容
- 只有 `projects/README.md` 作为结构说明被根仓库保留

因此，在 workspace 根目录执行 `git add .` 时，不会把子代码仓库误收进来。

## 每个 code repo 应该怎么管

每个 `projects/<project>/repos/<repo>/` 都应该把自己当作一个独立代码库。

建议各自维护自己的：

- `.gitignore`
- `README.md`
- repo 内部开发文档
- branch / PR / release 流程

### Python code repo baseline

如果子 repo 是 Python 项目，推荐至少包含：

```gitignore
# env
.venv/
venv/
.env
.env.*

# caches
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/

# notebooks
.ipynb_checkpoints/

# local IDE
.vscode/
.cursor/

# build
build/
dist/
*.egg-info/

# local outputs
data/
outputs/
tmp/
logs/
```

再根据 repo 类型做裁剪：

- library / app repo：通常忽略 `data/`、`outputs/`
- notebook / research repo：保留 notebook，本地数据和临时输出仍然忽略
- 少量样例数据需要版本控制时，用更细的白名单，比如只追踪 `data/sample/`

## 项目文档放哪一层

默认放在 `projects/` 本地目录：

- `projects/<project>/docs/project_state.md`
- `projects/<project>/docs/repo_map.md`
- `projects/<project>/docs/architecture.md`
- `projects/<project>/docs/decisions.md`
- `projects/<project>/notes/`

这些文件服务的是“项目域全局上下文”，不是某一个具体代码仓库。但它们默认是 **local-only**，不进入 workspace 根仓库的 git 历史。

放在子 code repo：

- repo 自己的 `README.md`
- repo 层面的架构说明
- repo 层面的开发说明
- 与代码强绑定的设计文档

判断标准：

- **跨 repo 的项目语义**：放 `projects/<project>/`
- **单 repo 的工程语义**：放 repo 自己

如果某个项目经验已经足够通用，值得跨机器共享，不要直接提交整个项目目录；而是把提炼后的结果晋升到：

- `rules/`
- `contexts/`
- `docs/`
- 或候选层 `contexts/reflection/`

## 新项目的推荐做法

1. 在 `projects/<project>/` 下建立 `docs/`、`notes/`、`repos/`
2. 在 `repos/` 下克隆或初始化真实代码仓库
3. 在每个代码仓库内部单独配置 `.gitignore`
4. 默认把整个 `projects/<project>/` 当作本地工作区，不纳入 workspace 根仓库
5. 只有提炼后的共享知识再晋升到 `rules/`、`contexts/`、`docs/`

这样以后你会有清晰的边界：

- 在 workspace 根目录做系统和共享知识管理
- 在子 repo 目录做代码开发和 git 操作
