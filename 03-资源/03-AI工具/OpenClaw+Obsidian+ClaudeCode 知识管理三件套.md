---
type: ai-tool-review
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
---

# OpenClaw + Obsidian + Claude Code｜AI 时代知识管理的神

> 原文：[摸鱼小李](https://mp.weixin.qq.com/s/EMahAzgfAbRQrYukWE7_IQ)  
> 修改于：2026年2月27日 21:29

---

## 核心观点

2026 年最顺手的知识管理三件套：**OPC 必备**

```
收集 ✓ → 整理 ✓ → 创作 ✓ → 分享 ✓
   OpenClaw    Obsidian    Claude Code
```

---

## Part 01：先看效果

### 三个真实使用场景

#### Case 1：爆款笔记拆解
- 刷小红书看到好帖子
- 直接飞书转发给 **OpenClaw**
- 它会拆解底层逻辑
- 还能顺着聊选题、聊原理
- 经验自动沉淀到 **Obsidian** 知识库

#### Case 2：创意前的功课
- 在外面吃饭时突然有想法
- 用小龙虾调研行业和品牌资料
- 沉淀到 OB 中
- 晚上回家和 Claude Code 深聊
- 完善调研、探索创意方向

---

## Part 02：安装基建（6 步装好全套）

> 推荐使用 Cherry Studio 免命令安装（对小白最简单）

### Step 1：下载 Cherry Studio
- 下载对应系统的安装包（Mac / Windows / Linux）
- 安装后打开

### Step 2：一键安装 OpenClaw
1. 在 Cherry Studio 首页找到 OpenClaw 图标（红色小龙虾）
2. 点「OpenClaw 未安装」页面的绿色「安装 OpenClaw」按钮
3. 等待进度条走完

### Step 3：购买阿里云百炼
1. 打开 [百炼 Coding Plan](https://dashscope.console.aliyun.com/) 页面
2. 选 **Lite 版本**，点「立即购买」
3. 在百炼控制台找到 API Key（点「生成 Key」）
4. 复制 API Key

### Step 4：在 Cherry Studio 里添加模型

#### 4.1 添加阿里云百炼服务商
- 点右上角 ⚙️ 设置 → 左侧选「模型服务」→ 拉到最下面点「+ 添加」
- 提供商名称：填「阿里」
- 提供商类型：选 OpenAI
- 点「确定」

#### 4.2 配置 API Key 和地址
- API 密钥：粘贴百炼的 Key
- API 地址：`https://coding.dashscope.aliyuncs.com/v1`

#### 4.3 添加模型
依次添加以下 4 个模型：
| 序号 | 模型 ID | 特点 |
|------|---------|------|
| 1 | kimi-k2.5 | 默认模型 |
| 2 | glm-5 | 稳定可靠 |
| 3 | MiniMax-M2.5 | 响应速度快 |
| 4 | qwen3.5-plus | 百万上下文 |

### Step 5：启动小龙虾
1. 回到 Cherry Studio 左侧，点 OpenClaw 图标
2. 模型下拉框选 `kimi-k2.5 | 阿里云百炼`
3. 点绿色的「▶ 启动」按钮
4. 打个「你好」测试

### Step 6：对接飞书（手机端使用）
在 Dashboard 对话框发给小龙虾：
```
帮我配置飞书，让我能通过飞书手机端跟你对话。一步步引导我，每步做完等我确认再继续
```

### Step 7：安装 Obsidian + Claude Code
发给小龙虾：
```
帮我安装 Obsidian 知识库和 Claude Code，请按以下步骤引导我：
第一步：安装 Obsidian
第二步：安装 Claudian 插件
第三步：安装 cc-switch
第四步：验证
每一步做完等我确认再继续
```

---

## Part 03：装备技能（4 个必备 Skill）

小龙虾装好后会了基础能力，但需要以下 4 个关键 Skill 才能跑通「输入→处理→输出」循环：

| Skill | 功能 | 安装命令 |
|-------|------|----------|
| **Multi Search Engine** | 免费搜索引擎，17 个搜索引擎覆盖国内外 | `npx clawhub@latest install multi-search-engine` |
| **x-reader** | 国内链接解析：微信公众号、小红书、B 站、X 等 | `pip install git+https://github.com/runesleo/x-reader.git` |
| **Obsidian** | 直接往 OB 知识库存东西 | `npx clawhub@latest install obsidian` |
| **find-skills** | 搜索和发现更多 Skill | `npx clawhub@latest install find-skills` |

**完整链路**：搜索 → 解析链接 → 存进 OB → 发现新能力

---

### 进阶：一个精选的开源 Skill 库

> 推荐：[public-agent-skills](https://github.com/cafe3310/public-agent-skills)

四大场景：
- **创作与知识管理**：语音转写、研究报告、去 AI 味
- **在线平台**：部署到 ModelScope，一键发布到社区
- **项目管理**：PMP 迭代、TDD、轻量管理
- **辅助工具**：媒体库整理、表情包制作

---

## Part 04：玩起来

### 实用玩法

1. **随手记**：在飞书里把碎碎念、文章链接、截图发给小龙虾，它帮你整理存进 OB
2. **定时简报**：设定每天早上推送天气 + 日程 + 行业新闻
3. **知识库管理**：定时让小龙虾整理本周笔记，生成周报
4. **文件整理**：「帮我把桌面上的文件按类型分到不同文件夹里」

---

### 训练你的小龙虾

小龙虾的 workspace 里有 4 个核心文件，每次对话都会读取：

| 文件 | 作用 |
|------|------|
| **USER.md** | 你是谁：名字、职业、工作时间、沟通偏好 |
| **SOUL.md** | 小龙虾的性格和行事准则 |
| **IDENTITY.md** | 小龙虾的名字和形象 |
| **AGENTS.md** | 工作手册：记忆规则、文件结构、工作流程 |

**建议**：第一天就把 USER.md 填好，告诉它你的基本信息。其他文件可以慢慢调。越聊越懂你。

---

### 打通 OB 和小龙虾

发给小龙虾：
```
帮我建一个软链接，把你的工作区链接到我的 OB 仓库里，建一个叫「龙虾工作区」的文件夹。你自己找到路径，直接帮我搞定
```

**效果**：双向实时同步
- 在 OB 编辑 SOUL.md → 小龙虾立即生效
- 小龙虾更新配置 → OB 里立即看到

---

## 总结

三件套配齐：
- **Obsidian** + **Claude Code** → 本地 AI 知识库
- **OpenClaw** → AI 助理，帮你收集、整理、输出

---

*来源：摸鱼小李 Knowledge Management 系列*