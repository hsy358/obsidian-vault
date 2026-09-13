# 人月聊IT（sharptoolbox）4 个开源项目

> **来源**：何大人微信分享（2026-09-13 09:01）+ 自行 web_fetch GitHub 主页与各仓库 README 验证
> **作者**：人月聊IT（GitHub: github.com/sharptoolbox）
> **核心特征**：4 个项目都是 AI Coding 技能包（SKILL.md + references/ + scripts/ + techbase/），全部用 MIT License，**格式兼容 WorkBuddy / Claude Code / Codex / Cursor / Cline / Aider**，都强调**人工门禁**（每阶段必须暂停等人确认），都用**本体论 + 七模型 + 强制追溯** 防止"模型一套、代码一套"。

---

## 项目总览（GitHub 主页 popular repos）

| # | 仓库 | Stars | Forks | 说明 |
|---|---|---|---|---|
| 1 | [ontology-driven-dev](https://github.com/sharptoolbox/ontology-driven-dev) | 250 | 101 | **本体驱动业务系统开发技能**（三步法） |
| 2 | [visual-model](https://github.com/sharptoolbox/visual-model) | 86 | 50 | **可视化建模提示词**（KSB/MBSE/SBR 三套） |
| 3 | [codebase-reverse](https://github.com/sharptoolbox/codebase-reverse) | 70 | 34 | **Java 源码逆向工程技能包** |
| 4 | [mobile-manufacturing-togaf](https://github.com/sharptoolbox/mobile-manufacturing-togaf) | 47 | 39 | **手机厂商 TOGAF 企业架构案例** |
| - | Onto-DataAnalyse | 37 | 34 | demo：电商数据分析（本体驱动实例） |
| - | Onto-Contract | 35 | 24 | demo：合同管理（= ontology-driven-dev 的 example） |

---

## 1️⃣ ontology-driven-dev — 本体驱动一体化开发技能

**核心方法论**：需求探索 → 本体建模 → 应用构建 **三步法**

**强制约束**：
- 基于**七模型本体 YAML**（M1 对象 / M2 行为 / M3 规则 / M5 主体 / M6 流程 / M7 查询报表 / MU UI）
- **code-paas 技术底座**：Flask + SQLite + React/TS 单体应用（系统管理 + 流程引擎 + 工作台 + 本体注册表）
- 需求探索分 8 阶段（总体理解 → 业务对象 → 业务功能与规则 → 跨对象联动 → 端到端协同/审批流 → 查询统计与报表 → 角色权限 → UI 原型），**每阶段必须暂停等人确认**
- 应用自带**强制 AI 对话框**（本体注册表注入 + 工具调用 + SSE 流式 + 只读 SQL 安全边界）

**实物 demo**：销售合同执行管理系统（合同登记与分级审批、开票审批、收款及冲销、跨对象状态联动、固定报表、系统管理、右侧 AI 智能助理）

**目录结构**：
```
SKILL.md                                # 方法论 + 三阶段管线 + 纪律
references/                             # 5 份方法论文档（强制规范）
  AI需求探索与确认提示词V9.0.md          # 含《软件需求编写规范 V9.0》全文
  ontology_modeling_framework_v9.md      # 七模型元规范 + YAML 模板
  本体模型业务功能开发指导书.md           # 模型→实现映射、10 步流水线
  AI原生应用技术架构设计文档.md           # 技术栈 / 语义注册表 / AI 编排 / SSE
  UI-UE界面设计规范.md                   # 配色 token / 布局 / 完整 CSS 库
reference-example/                      # 黄金范例（销售合同执行管理跑通实物）
techbase/                               # code-paas 干净源码（复制到 code-app 后扩展）
code-app-example/                       # 基于七模型生成的销售合同执行管理完整应用样例
```

**多工具兼容**（README 明确写）：
- ✅ WorkBuddy（.workbuddy/skills/）
- ✅ Claude Code（.claude/skills/，frontmatter 完全兼容）
- ✅ Codex（.codex/skills/ + AGENTS.md 引用）
- ✅ Cursor（.cursorrules）
- ✅ Cline / Aider（对话开头粘贴 SKILL.md 全文）

**运行**：
```bash
# 后端
cd code-app/backend && pip install -r requirements.txt && python app.py  # :5000
# 前端
cd code-app/frontend && npm install && npm run dev  # :5173
# 默认账号 admin / admin123
```

---

## 2️⃣ visual-model — 可视化建模提示词

**核心**：三套**相互独立、可单独使用**的中文建模提示词规范，目标是让 AI 生成**高质量、可复用的 SVG / D3.js 可视化图**

| 规范 | 方法论 | 输出 |
|---|---|---|
| **KSB_V4**（v3.6）| 知识体系构建 — 「三层递进 + 四图联动」 | 顶层思维导图 → 中间多维矩阵 → 底层知识图谱 + 学习路线图（D3.js 交互页）|
| **MBSE** | 基于模型的系统工程（SysML 标准）— 五层视图 | 需求图 / 块定义图 / 内部块图 / 活动图 / 状态机图 SVG |
| **SBR_v2**（v2.0）| 结构-行为-关系 三维框架 | 1600×900 SVG 系统结构图（防交叉贝塞尔曲线）|

**官方分工**：
- **SBR 画系统**、**MBSE 画工程**、**KSB 画知识**

**示例覆盖**（sample/ 131 个文件）：
- KSB：人工智能、金融、心理学、数学、哲学知识图谱 + 学习路径
- MBSE：企业架构、云原生、数字化转型、知识管理
- SBR：软件、业务、AI 系统结构图 + D3.js 交互页

**License**：CC BY 4.0（注明出处可自由改编）

---

## 3️⃣ codebase-reverse — Java 源码逆向工程技能包

**核心**：把存量源码逆向成**完整、可追溯、可继续钻取**的项目元模型

**逆向产出**：
| 文件 | 内容 |
|---|---|
| source-asset-inventory.md | 源码资产台账与归属 |
| business-function-requirements.md | 每个业务功能的需求功能面板 |
| function-chain-index.md | 每个功能的完整主实现穿透链 |
| database-inventory.md / schema.md / relations.md / access-matrix.md | 逐物理表、逐字段数据库逆向与 R/C/U/D 矩阵 |
| source-coverage-report.md | 从源码反查文档覆盖是否完整 |
| consistency-report.md | 独立语义与关系一致性检查 |
| function-drilldowns/FUNC-xxx.md | F-FULL 模式：业务 + 技术实现全集 |
| function-requirements/FUNC-xxx.md | F-REQ 模式：技术实现无关需求规格 |

**两种模式**：
- **F-FULL**：业务 + 技术实现全集（每个页面控件/事件纵向贯穿前端、接口、类方法、规则、对象、数据库）
- **F-REQ**：只输出业务界面、功能、规则、状态、验收、数据库对象模型（不混入类/方法/架构）

**Java 生态深度绑定**：
- 入口识别：@RestController / @RequestMapping / Spring MVC 注解 + app.get/post 前端路由
- 调度事件：@Scheduled、@XxlJob、Kafka @KafkaListener、@RabbitListener、CDC
- 数据访问：MyBatis Mapper XML / 注解 SQL、JPA / ORM、DAO / Repository / Mapper
- 对象分类：Entity / Model / DTO / VO / Command / Query / Event / Enum / Config
- 数据库逆向：物理表 / 视图 / 字段为最小单元；DDL 缺失时由 Java 类型/SQL/DAO 推断（unknown 项显式标记）

**校验脚本**：`scripts/validate_meta_model.ps1`（PowerShell；macOS/Linux 用 pwsh）
- 自动核对登记的入口 / DAO / 模型文件是否真实存在、是否有未归属资产
- 只有自动校验 + 人工 Pass A-O 都 PASS、ERROR = 0 才算完成

**推广到非 Java**：C# / TypeScript / Python / Go / PHP / Ruby 都可以，只需按 references/exhaustive-discovery.md 校准入口与对象命名约定

**覆盖完整度 ≠ 实现细节深度**：基线必须全量枚举，细节可以分层；禁止用"核心功能""代表表"缩小覆盖

---

## 4️⃣ mobile-manufacturing-togaf — 手机厂商 TOGAF 案例

**核心**：一份**手机制造行业**的完整 EA 规划案例，覆盖 TOGAF **四大架构域**（业务/数据/应用/技术）+ 战略与实施

**目录结构**：
```
第0章 手机厂商企业架构规划总纲.md       # 总纲：范围、方法、4A 关系、LTC 主线
第1章_企业战略与业务目标.md              # 战略：PEST、战略屋、战略地图、KPI
第2章_业务架构.md                        # 业务能力地图、价值流、LTC 流程、RACI
第3章_数据架构.md                        # 主题域、概念/逻辑模型、主数据、数据治理
第4章_应用架构.md                        # 应用组合、能力中心、API、微服务拆分
第5章_技术架构.md                        # 技术中台、云平台、部署、安全容灾
第6章_实施规划.md                        # 路线图、迁移波次、收益与治理
架构可视化浏览系统_需求与设计方案.md    # ★ AI 编程实现整套系统的蓝图
html/                                   # 76 个 ECharts / D3 可视化 HTML 原型
ea-ltc-demo/                            # LTC 知识图谱可运行原型
附件/                                    # 50+ Excel / Word 附件原始数据
image/                                   # 文档配图（约 55MB）
```

**亮点**：**「架构可视化浏览系统_需求与设计方案.md」不是思路文，是工程蓝图**——直接把技术栈（Flask + SQLite + React 18 + TS + Vite + Shadcn + Tailwind + AntV X6 / ECharts / Mermaid）、数据库表清单、API 八类（Document / Architecture / LTC / Matrix / Impact / Metadata / Import / Search）、十大功能模块全部写死。**把这份文档 + 6 章正文 + Excel 附件 + 现有原型 喂给 AI 编程工具，就能端到端生成整套系统**。

**四步落地**：
1. 资料入库（结构化）：6 章 Markdown + 50+ Excel → 抽取为 SQLite 元数据
2. 后端脚手架（Flask + SQLite）：八类 API
3. 前端 + 可视化（React + TS + Vite + Shadcn + Tailwind）：十大模块
4. 复用既有原型：html/ 76 个 ECharts 原型 + ea-ltc-demo/ 的 LTC 知识图谱

**仓库体量**：~60MB（含 image/ 55MB + 附件 xlsx）

---

## 我的分析（2026-09-13 09:15）

### 与何大人当前项目的关联（重点）

#### 🔴 项目 3（codebase-reverse）→ **直接可借鉴到德勤项目**

**Why**：
- 德勤项目第一阶段是**盘点现有技术资产**（平安云 Agent 智能体平台 + 内部知识库 + 客户既有系统）
- codebase-reverse 的「全量架构与功能基线逆向」**正好对应这个阶段**
- B0-B9 阶段流程（范围界定 → 源码资产台账 → 技术架构 → 业务架构 → 接口 → 数据库 → 功能穿透链 → 公共能力 → 覆盖对账 → 独立校验）可以直接借鉴

**How**：
- 不需要装 skill，只要把 B0-B9 流程图做成一份**「德勤项目盘点 SOP」**放到 `/root/vault/1-Projects/德勤/AI-Native/盘点-SOP/`
- 把 codebase-reverse 的 `references/output-contract.md` 改成我们的产出契约（"功能穿透链" → "Agent 能力盘点链"）

#### 🟡 项目 4（mobile-manufacturing-togaf）→ **「需求与设计方案 = AI 编程蓝图」的模式可借鉴**

**Why**：
- 德勤项目 MVP 文档如果能**写到 codebase-reverse / ontology-driven-dev 这个颗粒度**（技术栈、数据库表、API 分组、十大功能模块全写死），AI Coding 就能直接端到端生成系统
- 第 4 步"复用既有原型，不要从零造"是反"speculative feature"的好实践

**How**：
- 德勤 MVP 写到这一级时，**先收齐 50+ Excel 附件 + 76 个 HTML 原型 + 业务蓝图的 Markdown**，再让 AI Coding 干活
- 这个模式叫 **"结构化需求即系统"** —— 可以借鉴到 OpenClaw 工作流的 "vault 需求 → AgentSpace MVP"

#### 🟢 项目 1（ontology-driven-dev）→ **与 Hermes Agent 框架正交，不冲突**

**Why**：
- ontology-driven-dev 做的是"业务管理系统"（Flask + SQLite + React/TS）
- Hermes Agent 做的是"Agent 执行器"（StateGraph + LLM 调用）
- **两者解耦**——本体驱动的销售合同管理系统可以用 Hermes 做"合同审批 AI 助理"

#### ⚪ 项目 2（visual-model）→ **已经存过类似样本**

KSB V4 + MBSE + SBR 三套提示词已存。**直接引用**到德勤项目文档化时可用。

### 建议下一步动作

| 优先级 | 动作 | 输出 |
|---|---|---|
| 🟡 | Clone codebase-reverse 到 `/tmp/` 借鉴 B0-B9 流程 | 写一份"德勤项目盘点 SOP v0.1" |
| 🟡 | 把 mobile-manufacturing-togaf 的「需求与设计方案」模式**抽出来** | 通用模板"AI 编程蓝图写作规范" |
| 🟢 | 把 ontology-driven-dev 的「强制人工门禁」概念应用到 Hermes dispatcher | 防止 dispatcher 标 blocked（参考 6-29 Hermes blocked 事件）|
| ⚪ | 收藏 visual-model 到 vault 索引 | 已存本文件即足够 |

### 横向关联（vault 已有内容）

- **6-29 Hermes Agent 验证**：本体驱动 + 人工门禁 → 可借鉴到 Hermes dispatcher 防 blocked
- **6-29 PARA 重构**：ontology-driven-dev 的「需求/模型/代码一一对应」与 vault PARA 概念相通
- **7-09 Goal-Driven Execution**：项目 1 的"每阶段门禁" + 项目 3 的"覆盖完整度 ≠ 实现细节深度" + 项目 4 的"复用原型不从零造" = 都是反 speculative feature 的实践

---

## 文件信息

- 微信消息时间：2026-09-13 09:01 GMT+8
- web_fetch 时间：2026-09-13 09:01 GMT+8
- 4 个仓库 README 完整内容已抓取（每个约 4500-5000 字）
- 全文已合并入本文件，无需额外链接
