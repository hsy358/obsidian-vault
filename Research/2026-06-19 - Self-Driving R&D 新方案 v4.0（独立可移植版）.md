# Self-Driving R&D · 独立可移植版 v4.0

> **版本定位**：完全脱离 OpenClaw 依赖，做成真正可移植的独立系统
> **核心参考**：YX AI Delivery Harness（前端）+ Comet（状态脚本）+ v3.5（架构设计）
> **更新日期**：2026-06-19

---

## 一、系统全景图

```
┌─────────────────────────────────────────────────────────────┐
│  前端 Dashboard  (React + Vite)  localhost:5173             │
│  ├─ Pipeline 进度条（8 阶段）                               │
│  ├─ 过程面板（左：日志/调用/研判/思考轮次）                   │
│  ├─ 决策面板（右：环境检查/检查项/裁决/人工 PASS）            │
│  └─ Agent 工作台（ReAct 状态 + 当前决策）                    │
└─────────────────────────────────────────────────────────────┘
                              ↕  WebSocket / REST
┌─────────────────────────────────────────────────────────────┐
│  后端 Core（Python）                                        │
│  ├─ LoopEngine         ← GAMD 主循环                        │
│  ├─ StateManager       ← 状态机 + .comet.yaml              │
│  ├─ DecisionAgent      ← 门禁裁决（独立模块）               │
│  ├─ SkillRouter        ← 技能路由（核心！按阶段调用 skill） │
│  └─ LLMInterface       ← 模型适配层（不绑定具体模型）       │
└─────────────────────────────────────────────────────────────┘
         │                   │                    │
         ▼                   ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐
│  Stage Agents   │  │  Skill System   │  │  Model Pool        │
│  ├─ Access     │  │  （见第三节）   │  │  ├─ OpenAI        │
│  ├─ Explore    │  │                 │  │  ├─ Anthropic      │
│  ├─ Propose    │  │                 │  │  ├─ MiniMax        │
│  ├─ Task       │  │                 │  │  ├─ DeepSeek       │
│  ├─ Apply      │  │                 │  │  └─ 任意兼容 API   │
│  ├─ Verify     │  │                 │  └─────────────────────┘
│  ├─ Review     │  │                 │
│  └─ Archive    │  │                 │
└─────────────────┘  └─────────────────┘
```

---

## 二、8 阶段 × Skill 矩阵（核心）

每个阶段声明自己需要哪些 Skill，由 SkillRouter 在该阶段触发时自动加载：

| 阶段 | 主要工作 | 调用的 Skills | 说明 |
|------|---------|--------------|------|
| **01 接入** | 用户需求 → spec.md | `requirement-parser`, `spec-writer` | 把自然语言转规格 |
| **02 探索** | 调研可行性 | `web-search`, `code-search`, `doc-reader` | 爬竞品/查技术栈 |
| **03 提案** | 出方案 + 选型 | `proposal-writer`, `architecture Advisor` | 生成多个方案 |
| **04 任务** | 拆解任务 | `task-decomposer`, `dependency-analyzer` | 拆成可执行任务 |
| **05 应用** | 编码实现 | `code-generator`, `test-writer`, `linter` | 写代码 + 写测试 |
| **06 验证** | 验证质量 | `test-runner`, `security-scanner`, `benchmark-runner` | 运行测试/安全扫描 |
| **07 评审** | AI 自评 | `review-writer`, `doc-generator` | 生成评审报告 |
| **08 归档** | 沉淀经验 | `archive-writer`, `lesson-extractor` | 写 lessons + 更新知识库 |

**关键设计**：同一个 Skill 可以被多个阶段调用，比如 `web-search` 在探索阶段用，`lesson-extractor` 在归档阶段用。

---

## 三、Skill System（技能系统）

### 3.1 Skill 的三层类型

```
┌──────────────────────────────────────────────────────────────┐
│  Layer 1: 内置 Skill（Python 实现）                          │
│  ├─ 代码生成：直接 import 进来                               │
│  ├─ 任务分解：直接 import 进来                               │
│  └─ 评审生成：直接 import 进来                               │
├──────────────────────────────────────────────────────────────┤
│  Layer 2: 脚本 Skill（Shell/Python 脚本，可自定义）          │
│  ├─ web-search/                                             │
│  │   ├─ SKILL.md（描述 + 输入输出）                          │
│  │   ├─ run.sh（执行脚本）                                   │
│  │   └─ requirements.txt                                     │
│  ├─ code-generator/                                          │
│  │   └─ ...                                                  │
│  └─ test-runner/                                            │
├──────────────────────────────────────────────────────────────┤
│  Layer 3: API Skill（外部服务）                              │
│  ├─ feishu-notifier/    ← 发飞书消息                        │
│  ├─ github-repo/        ← 操作 GitHub API                  │
│  └─ screenshot/         ← 网页截图                         │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 Skill 目录结构

```
self-driving-rd/
├── skills/                          ← 所有 Skill 在这里
│   ├── _registry.yaml               ← Skill 注册表（核心！）
│   │
│   ├── requirement-parser/           ← 内置：需求解析
│   │   ├── SKILL.md
│   │   ├── run.py
│   │   └── schema.json
│   │
│   ├── web-search/                  ← 脚本：网页搜索
│   │   ├── SKILL.md
│   │   ├── run.sh
│   │   └── requirements.txt
│   │
│   ├── ppt-generator/               ← 脚本：PPT 生成
│   │   ├── SKILL.md
│   │   ├── run.sh
│   │   └── template/
│   │
│   ├── code-generator/              ← 脚本：代码生成
│   │   ├── SKILL.md
│   │   ├── run.py
│   │   └── schema.json
│   │
│   ├── test-runner/                 ← 脚本：测试运行
│   │   ├── SKILL.md
│   │   └── run.sh
│   │
│   ├── archive-writer/               ← 脚本：归档写作
│   │   ├── SKILL.md
│   │   └── run.sh
│   │
│   ├── feishu-notifier/             ← API：飞书通知
│   │   ├── SKILL.md
│   │   └── run.py
│   │
│   └── lesson-extractor/             ← 脚本：经验提取
│       ├── SKILL.md
│       └── run.py
```

### 3.3 Skill 注册表（`_registry.yaml`）

```yaml
# skills/_registry.yaml
# 整个系统的 Skill 全局注册表
skills:
  requirement-parser:
    type: builtin          # builtin | script | api
    module: skills.requirement_parser
    description: "把自然语言需求解析成结构化 spec"
    input: "用户需求（文本）"
    output: "spec.md"
    stages: [access]       # 在哪些阶段调用

  web-search:
    type: script
    entry: skills/web-search/run.sh
    description: "搜索网页内容"
    input: "搜索关键词"
    output: "搜索结果列表"
    stages: [explore]

  ppt-generator:
    type: script
    entry: skills/ppt-generator/run.sh
    description: "生成 PPT 文件"
    input: "内容大纲 + 风格配置"
    output: "PPTX 文件路径"
    stages: [review]

  code-generator:
    type: script
    entry: skills/code-generator/run.py
    description: "根据 spec 生成代码"
    input: "spec.md + 技术栈"
    output: "代码文件列表"
    stages: [apply]

  test-runner:
    type: script
    entry: skills/test-runner/run.sh
    description: "运行测试并返回结果"
    input: "测试命令 + 超时时间"
    output: "测试报告 JSON"
    stages: [verify]

  archive-writer:
    type: script
    entry: skills/archive-writer/run.sh
    description: "写归档文档"
    input: "项目目录 + 阶段产物"
    output: "归档 Markdown"
    stages: [archive]

  lesson-extractor:
    type: script
    entry: skills/lesson-extractor/run.py
    description: "从项目中提取经验教训"
    input: "项目路径"
    output: "lessons/ 目录更新"
    stages: [archive]

  feishu-notifier:
    type: api
    module: skills.feishu_notifier
    description: "发飞书通知"
    input: "标题 + 内容 + 接收人"
    output: "发送状态"
    stages: [all]          # all = 所有阶段 Hard Gate 时通知
```

### 3.4 SkillRouter（技能路由器）

**这是"合适的时候调用"的核心逻辑**：

```python
class SkillRouter:
    """根据当前阶段 + 任务上下文，自动调用正确的 Skill"""

    def __init__(self, registry_path: str):
        with open(registry_path) as f:
            self.registry = yaml.safe_load(f)

    def route(self, stage: str, task: dict) -> list[SkillResult]:
        """主路由方法"""
        # 1. 查注册表：这个 stage 需要哪些 skill
        needed_skills = self._skills_for_stage(stage)

        # 2. 按依赖顺序执行（有些 skill 依赖前一个的输出）
        results = []
        for skill_name in needed_skills:
            skill = self.registry["skills"][skill_name]
            result = self._invoke_skill(skill, task, results)
            results.append(result)

            # 3. 检查 skill 输出，决定是否继续
            if result.is_critical and not result.success:
                # 关键 skill 失败 → 写入 Dead Letter Queue
                self._dlq.add(skill_name, task, result.error)
                raise SkillError(f"Critical skill {skill_name} failed")

        return results

    def _invoke_skill(self, skill: dict, task: dict, prev_results: list) -> SkillResult:
        """调用单个 skill"""
        if skill["type"] == "builtin":
            return self._call_builtin(skill["module"], task, prev_results)
        elif skill["type"] == "script":
            return self._run_script(skill["entry"], task, prev_results)
        elif skill["type"] == "api":
            return self._call_api(skill["module"], task, prev_results)

    def _skills_for_stage(self, stage: str) -> list[str]:
        """查出这个 stage 需要的所有 skill"""
        return [
            name for name, meta in self.registry["skills"].items()
            if stage in meta.get("stages", []) or "all" in meta.get("stages", [])
        ]
```

### 3.5 Skill 触发时机

```
阶段开始
    │
    ▼
StateManager 加载 .comet.yaml
    │
    ▼
DecisionAgent 检查前置条件
    │
    ├─ 通过 → SkillRouter.route(当前阶段, 上下文)
    │              │
    │              ▼
    │          按 registry 顺序调用 skill
    │              │
    │              ▼
    │          Stage Agent 执行 LLM 任务
    │              │
    │              ▼
    │          DecisionAgent 裁决（得分 >= 70?）
    │              │
    │              ▼
    │          通过 → 写 .comet.yaml next_stage
    │              │
    └─ 不通过 → Hard Gate 通知（飞书/微信）
                    │
                    ▼
                人工 PASS 或 修复后重跑
```

---

## 四、状态架构（Comet 风格）

```yaml
# projects/<project>/.comet.yaml
project: my-tool
version: 4.0
created: 2026-06-19T10:00:00

current_stage: verify
previous_stage: apply

llm:
  generator: minimax/MiniMax-M2.7
  evaluator: deepseek/DeepSeek-R1
  planner: minimax/MiniMax-M3

stage_history:
  access:  {status: completed, score: 92, skills_used: [requirement-parser], ended_at: ...}
  explore: {status: completed, score: 88, skills_used: [web-search, doc-reader], ended_at: ...}
  propose: {status: completed, score: 85, skills_used: [proposal-writer, architecture-advisor], ended_at: ...}
  task:    {status: completed, score: 82, skills_used: [task-decomposer, dependency-analyzer], ended_at: ...}
  apply:   {status: completed, score: 0, skills_used: [code-generator, test-writer, linter], ended_at: ...}
  verify:  {status: in_progress, skills_used: [test-runner, security-scanner], started_at: ...}
  review:  {status: pending, skills_used: [review-writer, doc-generator]}
  archive: {status: pending, skills_used: [archive-writer, lesson-extractor]}

gate_history:
  - stage: access
    decision: PASS
    score: 92
    by: auto
  - stage: explore
    decision: PASS
    score: 88
    by: auto
  - stage: verify
    decision: BLOCK
    score: 68
    by: DecisionAgent
    message: "test coverage < 80%"

skills_registry_version: "4.0"
```

---

## 五、部署架构

### 5.1 部署拓扑

```
┌────────────────────────────────────────────────────┐
│  开发者机器（Mac/Linux/Windows）                    │
│  ├─ Docker Desktop 或 直接 pip + npm              │
│  ├─ 配置文件 config.yaml（API key 在这里）        │
│  └─ projects/（工作目录，可挂载到 host）           │
└────────────────────────────────────────────────────┘
         │
         │ 可选：如果要远程访问
         ▼
    Nginx 反向代理（可选）
         │
         ▼
    任何有公网的 Linux 服务器
```

### 5.2 config.yaml（模型配置）

```yaml
# config.yaml
models:
  generator:
    provider: minimax
    model: MiniMax-M2.7
    api_key: ${MINIMAX_API_KEY}

  evaluator:
    provider: deepseek
    model: DeepSeek-R1
    api_key: ${DEEPSEEK_API_KEY}

  planner:
    provider: minimax
    model: MiniMax-M3
    api_key: ${MINIMAX_API_KEY}

skills:
  registry: ./skills/_registry.yaml
  skills_dir: ./skills

storage:
  projects_root: ./projects
  lessons_dir: ./lessons

notification:
  feishu:
    enabled: true
    webhook: ${FEISHU_WEBHOOK}
```

### 5.3 Docker Compose 一键部署

```yaml
# docker-compose.yaml
version: "3.9"
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    volumes:
      - ./projects:/app/projects
      - ./lessons:/app/lessons
      - ./skills:/app/skills
      - ./config.yaml:/app/config.yaml
    environment:
      - MINIMAX_API_KEY=${MINIMAX_API_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      - FEISHU_WEBHOOK=${FEISHU_WEBHOOK}

  frontend:
    build: ./frontend
    ports: ["5173:5173"]
    environment:
      - API_BASE=http://localhost:8000
```

---

## 六、与 OpenClaw 版 v3.5 的核心差异

| 维度 | v3.5（OpenClaw 依赖）| v4.0（独立版）|
|------|---------------------|--------------|
| **运行依赖** | 必须有 OpenClaw | pip + npm 独立跑 |
| **前端** | 无 | React Dashboard |
| **Skill 调用** | sessions_spawn 间接调用 | SkillRouter 直接路由 |
| **Skill 存储** | OpenClaw workspace | 本地 `skills/` 目录 |
| **模型绑定** | 限 MiniMax M2.7/M3 | 任意 LLM API |
| **状态文件** | 散落多处 | 统一 `.comet.yaml` |
| **部署** | 依赖 OpenClaw | docker-compose 一键 |
| **可移植** | 差 | 好（任何服务器）|

---

## 七、开发计划建议

| 优先级 | 模块 | 工作量 | 理由 |
|--------|------|--------|------|
| **P0** | SkillRouter + 注册表 | 3-5 天 | 核心调度逻辑 |
| **P0** | LLMInterface（适配层）| 2-3 天 | 模型无关 |
| **P0** | StateManager + .comet.yaml | 2 天 | 状态是一切 |
| **P1** | 8 个 Stage Agent | 5-7 天 | 主要功能 |
| **P1** | DecisionAgent | 2-3 天 | 门禁裁决 |
| **P2** | React 前端 | 5-7 天 | 参考 YX Harness |
| **P2** | 核心 Skills 实现 | 7-10 天 | 代码生成/测试等 |
| **P3** | Self-Improvement | 5 天 | 自改进引擎 |

**预计总工期**：约 4-6 周（1 人）或 2-3 周（3 人团队）
