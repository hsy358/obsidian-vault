# Gemini API 免费使用实操教程（2026-07-03）

> 来源：何大人 2026-07-03 微信推送文章《谷歌突然放大招！Gemini API 免费配额涨到 100 万 Token，还不用绑卡》
> https://mp.weixin.qq.com/s/tnELi7EPofIZ-D_yzFdC7A

---

## 🎁 谷歌这次改了什么（2026-07-01）

| 模型 | 免费额度（RPM） | 免费额度（RPD） | 每分钟 Token |
|---|---|---|---|
| **Gemini 2.5 Flash** | 15 次/分钟 | 1500 次/天 | **100 万**（从 25 万翻 4 倍）|
| **Gemini 2.5 Flash-Lite** | 30 次/分钟 | 1500 次/天 | **100 万** |
| Gemini 2.5 Pro | ❌ 不免费 | — | — |

**最大亮点**：**不需要绑信用卡**，拿 Google 账号登录就能用。

---

## ⚠️ 必须先看的 3 个坑

1. **⚠️ 你的对话会被拿去训练模型**（欧盟用户除外）
   - 如果你处理的是**敏感数据**（代码 / 公司业务 / 私有客户）— **别用免费版**
2. **Pro 模型要钱**（100 万 Token 输入 $1.25 / 输出 $10.00）
3. **不是全员推送**——部分账号可能仍是 25 万/分钟，刷新几次或换账号试试

---

## 🚀 4 步开始用

### Step 1 — 拿 API Key（1 分钟）

```
1. 打开 https://aistudio.google.com/
2. 用 Google 账号登录（无需绑卡）
3. 左侧菜单点 "Get API key"
4. 点 "Create API key" → 选 / 新建一个 GCP 项目
5. 复制 API key（只显示一次！）
```

### Step 2 — 选调用方式（按你的技术栈）

```bash
# 验证 key 立即可用（curl 测）
curl -sS -X POST \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"你好"}]}]}' \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=YOUR_KEY"
```

成功返回：JSON 含 `candidates[0].content.parts[0].text` → AI 回复。

### Step 3 — Python SDK（推荐生产用）

```bash
pip install google-generativeai
```

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content("用 100 字总结 RAG 的核心")
print(response.text)
```

### Step 4 — Node.js SDK

```bash
npm install @google/generative-ai
```

```javascript
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });
const result = await model.generateContent("hello");
console.log(result.response.text());
```

---

## 🔁 100 万 Token / 分钟够不够用？实测参考

| 场景 | 单次 Token | 估算 |
|---|---|---|
| 普通问答 | 几百～几千 | 一轮对话 < 1 万 |
| 5 万字文档总结 | 30K 输入 + 3K 输出 | 一次性跑完，**不再卡额度** |
| 写 3 篇 5000 字文章 | 3 × 6K = 18K | 一小时搞定 |
| 一天对话 100 轮 | 100K～500K | **完全够用** |

**结论**：日常场景**基本等于无限**。仅在批量跑 / 长上下文（500K+）才需要担心。

---

## 🔐 数据隐私应对方案

如果你担心数据被训练：

| 方案 | 推荐度 | 说明 |
|---|---|---|
| **欧盟 Google 账号**（地址选 EEA）| ⭐⭐⭐⭐⭐ | 自动豁免训练数据收集 |
| **不传敏感内容**（去标识化 / 摘要）| ⭐⭐⭐⭐ | 业务层处理 |
| **付费 Pro** | ⭐⭐⭐ | 数据不训练，但贵 |
| **国内替代**：智谱 GLM-4 / 通义千问 / DeepSeek | ⭐⭐⭐⭐ | 同等能力，更好合规 |

---

## 📋 中文场景最佳实践

```python
import google.generativeai as genai

model = genai.GenerativeModel("gemini-2.5-flash")

# 1. 长文档总结
long_text = open("doc.md").read()
prompt = f"用 3 段不超过 200 字总结以下文档：\n{long_text[:50_000]}"  # 不超 100 万 Token
resp = model.generate_content(prompt)
print(resp.text)

# 2. 流式输出（实时反馈）
response = model.generate_content("讲个笑话", stream=True)
for chunk in response:
    print(chunk.text, end="", flush=True)

# 3. 对话上下文管理
chat = model.start_chat()
chat.send_message("我叫张三")
chat.send_message("我叫什么？")  # Gemini 自动记住上下文
```

---

## 🎯 立即可做的 3 件事

| # | 操作 | 时间 |
|---|---|---|
| 1 | 去 aistudio.google.com 拿 API Key | 1 分钟 |
| 2 | 用 curl 测一次，问"你好" | 30 秒 |
| 3 | 把 GEMINI_API_KEY 加到 `~/.bashrc`，写进 vault `0-Inbox/2026-07-03_*.md` | 5 分钟 |

**完成：你的私有 Gemini 客户端就跑通了**，不花一分钱。

---

## 🚧 常见问题

**Q1：拿到 key 但 401？**
- 确认 key 是从 AI Studio **生成**的，不是 Vertex AI 的
- URL 用 `generativelanguage.googleapis.com`，不是 `*-aiplatform.googleapis.com`

**Q2：每次响应说 "免费配额已用完"？**
- 刷新 AI Studio 看是否被升级到 100 万
- 或检查 `systemInstruction` 别挂大文本

**Q3：怎么调上下文窗口？**
- Gemini 2.5 Flash 支持 **100 万 Token 上下文**（输入 + 输出合计）
- 但 per-minute 限速 100 万，所以你**单次请求可以发到 100 万 Token**（但要小心处理时长）

**Q4：API Key 泄漏怎么办？**
- 立即回 AI Studio "Revoke"
- 检查 billing account 没被滥用
- 监控 Google Cloud Console → API → Quota & System Limits

---

## 🎁 福利：5 个推荐用法

1. **本地 RAG 替代**：用 Gemini 直接处理 vault 文档，免自己部署向量库（适合小型项目）
2. **代码 review**：丢 diff 进去，说 "review this PR"
3. **公众号抓存**：跟我 wechat-article-to-obsidian skill 配合，整篇 5 万字文章直接 Gemini 总结
4. **Hermes 替换代理**：把 Hermes 默认的 `cc-vibe.com 第三方代理` 换成 Gemini 直连（更稳 + 不限速）
5. **日常 IDE**：Claude Code / OpenCode 里把 Gemini 设为 fallback 模型（主模型崩溃时走）

---

**📁 关联**：
- 文章存档：`/root/vault/2-Areas/公众号文章/2026-07-03 - 谷歌突然放大招Gemini API免费配额涨到100万Token.md`
- 来源：`https://mp.weixin.qq.com/s/tnELi7EPofIZ-D_yzFdC7A`
