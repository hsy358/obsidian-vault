---
title: "一步步教你用 Streamlit + Pydantic AI 搭建深度研究智能体应用"
author: "AI大模型观察站"
publish_date: ""
saved_date: "2026-06-26"
source: "wechat-monitor"
url: "https://mp.weixin.qq.com/s/fThH4Xu-_mDdb9VIIz0hlA"
---

---
title: "一步步教你用 Streamlit + Pydantic AI 搭建深度研究智能体应用"
author: "AI大模型观察站"
publish_date: "2025-09-03 08:18:00"
saved_date: "2026-06-26"
source: "wechat"
url: "https://mp.weixin.qq.com/s/fThH4Xu-_mDdb9VIIz0hlA"
---
# 一步步教你用 Streamlit + Pydantic AI 搭建深度研究智能体应用
> 为你的深度研究 AI Agent 打造一个 Streamlit 前端

---

如果你曾经好奇如何通过结合智能的后端 Agent 和流畅的交互式前端来释放人工智能的真正力量，那你来对地方了！今天，我们将把你的知识提升到一个新高度，通过将强大的 Pydantic AI 研究 Agent 作为后端，与动态的 Streamlit 界面作为前端进行整合。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/6Ex6Atic0gTxaMlTyfOEMUY0G3056CfQOnyeC19icZUb3OianeXVt8yceWHAZusaDQOxaEwQ1h2edZfzeowoQO8IQ/640?wx_fmt=webp&from=appmsg)

AI 的世界发展得快如闪电。现代 Web 应用早已不再是静态网站。得益于 AI Agent 的魔力，它们变得智能、响应迅速且交互性强。将 AI Agent 后端与用户友好的前端结合，你就能打造出充满活力的应用：用实时网络数据回答问题，自动化研究，让用户能实时与结果互动，而无需复杂的 Web 开发麻烦。

这次整合有什么令人兴奋的地方？你将学会如何：

- • 使用 Pydantic AI 和 Tavily 在后端协调强大的语言模型和实时搜索
- • 通过 Streamlit 这个基于 Python 的美观前端，展现所有这些能力
在本教程结束时，你将能够：

- • 理解从后端 Agent 逻辑到前端可视化的清晰路径
- • 将你的 AI Agent 和仪表板代码复用并整合成一个统一的解决方案
- • 获得信心去实验其他 AI 驱动的 Web 应用

### 前提条件

这篇实践指南是你在前几篇博客中培养的基础技能的桥梁：

- • [新手指南：用 Pydantic AI 搭建第一个研究 Agent](https://mp.weixin.qq.com/s?__biz=MzkzMjkwMjk3Mw==&mid=2247485870&idx=1&sn=271067cce9e8fa771b2429e506eff9df&scene=21#wechat_redirect)
- • [数据可视化神器：Streamlit + Python 打造交互式仪表盘实战](https://mp.weixin.qq.com/s?__biz=MzkzMjkwMjk3Mw==&mid=2247485869&idx=1&sn=bcde2baab6e2e819e3f0ff5422d27247&scene=21#wechat_redirect)
虽然推荐阅读这两篇博客，但如果你时间有限，可以跳过 Python 仪表板那篇。不过我强烈建议阅读 Pydantic AI 研究 Agent 那篇，因为我们会复用那里的很多代码。不过别担心，我在这儿也包含了关键概念的解释，所以如果你想直接开始，也能跟得上，必要时可以回头参考之前的文章。

---

## 回顾：已有的构建模块

在深入探讨后端与前端无缝整合的乐趣之前 😉，让我们回顾一下你在前两篇教程中涵盖的关键学习里程碑。如果你已经迫不及待想动手，可以直接跳到下一节。

### 1. 用 Pydantic AI 和 Tavily 打造现代研究 Agent

在我们的第一次旅程中，我们解锁了 AI 驱动的研究 Agent 世界。利用 Pydantic AI 进行类型检查的结构化数据管道，以及 Tavily 获取实时网络信息，你学会了：

- • **环境设置**：安装必要的 Python 包，如 pydantic_ai 和 tavily_python，并管理 API 密钥的配置文件。
- • **设计稳健的数据模型**：利用 Pydantic 的 BaseModel 类定义搜索结果和 Agent 输出的预期结构，确保数据始终干净、可靠、可预测。
- • **用 Tavily 搜索赋能**：你将 Agent 连接到实时网络数据，掌握了异步查询的艺术，通过 Tavily 的 API 收集、过滤并返回相关内容。
- • **像 Agent 一样思考**：通过 Pydantic AI 的 Agent 类（以及可选的高级推理，使用像 Llama 3 或 GPT-4 这样强大的 LLM），你编写了能生成带上下文、验证和清晰结构输出的 Agent，这对任何研究流程都至关重要。
掌握这些概念将你的 Python 脚本技能提升到了 AI Agent 时代。重点在于后端智能、韧性和确保你的 AI 能在实时、杂乱的网络数据上推理。

### 2. 用 Streamlit 构建交互式仪表板

在我们的第二篇基础博客中，焦点从计算智能转向了引人入胜的展示。你学会了将静态代码转变为充满活力的 Web 应用，使用的是 Streamlit：

- • **轻松创建 Web 应用**：Streamlit 简化了将 Python 脚本转为响应式网页的过程，只需几行代码，无需 Flask、Django 或前端经验。
- • **数据处理与 EDA**：你练习了使用 pandas 和 numpy 等库导入和处理数据，进行探索性数据分析（EDA）以挖掘洞见。
- • **动态可视化**：Streamlit 的内置图表功能让你能展示趋势和比较，配合交互式控件和美观的图表。
- • **直观的用户控制**：下拉菜单、滑块和侧边栏让用户能引导分析，为你的仪表板带来真正的交互性。

---

## 整合一切

### 文件夹结构

创建一个项目文件夹，包含以下文件：

```
Project-Folder/├── 📄 agent.py                    # 核心 AI Agent 实现├── 📄 app.py                      # Streamlit Web 界面├── 📄 requirements.txt            # Python 依赖├── 📄 README.md                   # 项目文档└── 📄 .env                        # 环境变量（不跟踪）
```

---

## 理解研究 Agent 后端代码

现在你已经了解了什么是研究 Agent，以及为什么 Pydantic AI 和 Tavily 是动态组合，让我们详细讲解驱动这个智能研究助手的后端代码。准备好一杯咖啡 ☕，我们开始吧。

### 1. 导入语句：搭建舞台

每个研究项目都从引入正确的库开始。使用你之前创建的 agent.py 脚本。在脚本顶部，你需要导入 Python 库和模块，为代码赋予必要能力：

```
from tavily import TavilyClientimport osfrom dotenv import load_dotenvfrom pydantic import BaseModel, Fieldfrom typing import Listfrom pydantic_ai import Agent, Toolfrom pydantic_ai.models.openai import OpenAIModelfrom pydantic_ai.providers.openai import OpenAIProviderimport asyncio
```

- • `from tavily import TavilyClient` 引入客户端以访问 Tavily 的实时网络搜索工具。
- • `os` 和 `load_dotenv` 通过环境变量安全管理敏感的 API 密钥，这是处理 API 的最佳实践。
- • `pydantic.BaseModel/Field/List` 强制执行严格的数据验证和清晰的 Agent 输入输出模式（就像一份合同：你的代码始终知道期待什么数据）。
- • `pydantic_ai` 模块让你定义和运行 AI 驱动的 Agent，最终接入大型语言模型（LLM）和像网络搜索这样的外部工具。
- • `asyncio` 启用异步（非阻塞）代码。网络搜索在后台进行，让你的应用保持快速和响应性。
**提示**：始终使用环境变量（比如 .env靠近文件）来存储密钥，绝不硬编码。

### 2. Tavily 客户端初始化

```
load_dotenv()client = TavilyClient(os.getenv("TAVILY_API_KEY"))
```

- • `load_dotenv()` 从 .env 文件加载变量，使你的 API 密钥（如 TAVILY_API_KEY）可供脚本使用。
- • `TavilyClient()` 用你的密钥初始化，允许脚本向 Tavily 的网络搜索 API 发出安全、认证的请求。

### 3. Pydantic 数据模型：结构化输出

```
class SearchResult(BaseModel):  title: str  url: str  snippet: strclass SearchResults(BaseModel):  results: List[SearchResult]  main_content: str = Field(description="The main content of the blog")
```

**目的**：这些 BaseModel 类精确描述了 Agent 的输出结构：搜索结果列表（SearchResult）和可选的主要内容摘要（main_content）。
**好处**：后端与前端之间的数据传递始终可预测、类型检查、安全。
**最佳实践**：清晰定义的模型减少错误，提高可读性，便于调试。

### 4. 编写搜索逻辑：异步网络搜索

```
async deftavily_search(query: str) -> dict:  search_response = client.search(query=query, search_depth="advanced", max_results=5)return {      "results": [          {              "title": res["title"],              "url": res["url"],              "snippet": res["content"]          }          for res in search_response["results"]        ]      }asyncdefsearch_tool(query: str):returnawait tavily_search(query)
```

- • **异步模式**：`async` 关键字允许函数暂停而不阻塞整个程序，这对等待慢速网络 API 尤为重要。
- • **为何两个函数**？`tavily_search` 执行实际查询和格式化，`search_tool` 是一个包装器，方便直接插入 Agent 的工具接口。
- • **定制化**：最大结果数、搜索深度和结果格式都可轻松调整。

### 5. 模型与 Agent 设置：核心大脑

```
model = OpenAIModel('gpt-4.1', provider=OpenAIProvider(api_key=os.getenv('OPENAI_API_KEY')))web_agent = Agent(    system_prompt="You are a research assistant. Answer questions using live web data and provide the main content explaining the topic in detail in markdown format with proper sections and sub-sections",    tools=[Tool(search_tool, takes_ctx=False)],    output_type=SearchResults,    model=model)
```

- • **OpenAI 模型**：定义 LLM（如 GPT-4），使用从环境变量安全获取的 API 密钥。
- • **系统提示**：指导 AI 的行为（例如，“作为研究助手，使用实时网络数据，以 markdown 格式提供详细的主题解释，包含适当的章节和子章节”）。可以尝试调整系统提示，观察响应的质量和细节变化，真的很有趣！
- • **工具**：将网络搜索功能提供给 Agent，供其在需要实时数据时调用。
- • **输出类型**：确保 Agent 仅返回符合 SearchResults 模式的响应（超安全、干净）。
- • **注意**：Pydantic AI 的输出类型让你避免了 LLM 通常无结构的混乱输出，真是救星！这就是为什么我个人更喜欢这个框架，而不是更流行的 LangChain 或 LangGraph。

### 6. Agent 运行器：整合一切

```
async def run_agent(query):    response = await web_agent.run(query)    return response.data.results, response.data.main_content
```

**目的**：这个函数是你的 Web 前端调用的部分。它接收用户的问题，让 Agent 施展魔法，并直接为 UI 返回搜索详情和主要内容摘要。
**异步**：保持应用的响应性，多个用户或请求不会拖慢速度。

### 最终思考与最佳实践

- • **关注点分离**：代码的每个部分（搜索、模式、Agent、运行器）都有明确的任务，便于更新或调试。
- • **安全性**：使用环境变量，而不是硬编码密钥。
- • **可读性**：使用 Pydantic 模型确保清晰，强制类型检查。
- • **异步优先**：现代 Python，尤其是 Web 开发，应使用 asyncio 以获得更好性能。
这个模块化、经过测试的后端是接下来要构建的 Streamlit 前端的完美搭档。

---

## 构建 Streamlit 前端：展示 AI 搜索结果

恭喜！🎉 如果你跟到这里，你已经拥有了一个强大的研究 Agent 后端，随时提供深刻的搜索结果和摘要。下一个任务：用 Streamlit 让这些洞见变得易于访问且美观。

Streamlit 是一个友好的 Python 库，能将你的脚本变成交互式 Web 应用。无需连夜成为前端开发者！在本节中，我们将构建一个简单但精致的 Streamlit 界面，用于查询你的研究 Agent，并展示搜索结果和主要内容摘要。让我们用一个流畅的 UI 为你的项目赋能，完美分享给朋友、团队或全世界。

### 1. 设置 Streamlit 应用

首先，确保 Streamlit 已安装：

```
pip install streamlit
```

创建一个名为 app.py 的新文件。在顶部导入核心库：

```
import streamlit as stimport asynciofrom agent import run_agent  # 导入你的异步 run_agent 函数
```

**专业提示**：如果在 Jupyter 中运行，可能需要使用 nest_asyncio：

```
import nest_asyncionest_asyncio.apply()
```

### 2. 设计用户输入部分

用标题和友好的提示欢迎用户：

```
st.set_page_config(page_title="AI Research Assistant", page_icon="🔎")st.title("🔎 AI 研究仪表板")st.write("在下方输入你的研究问题。你的个人研究 Agent 将搜索网络并为你总结结果——随时待命！")query = st.text_input("今天想研究什么？", "强化学习是如何工作的？")
```

### 3. 处理搜索请求（异步来救场！）

这里是魔法时刻：当用户提交查询时，调用你的 Agent 并展示结果。由于 run_agent 是异步的，优雅地包装它的调用：

```
if st.button("运行研究"):  with st.spinner('正在咨询你的研究 Agent，请稍候...'):      results, main_content = asyncio.run(run_agent(query))
```

**提示**：Streamlit 的 st.spinner 非常适合让用户知道应用正在忙碌，避免尴尬的沉默等待。

### 4. 优雅地展示结果

将输出组织成清晰分隔的部分，增加清晰度和风格：

```
if "main_content" in locals():  st.subheader("📝 摘要")  st.markdown(main_content, unsafe_allow_html=True)    st.subheader("🔗 顶级搜索结果")  for idx, result in enumerate(results, 1):    with st.container():      st.markdown(f"**{idx}. [{result.title}]({result.url})**")      st.markdown(result.snippet)      st.markdown("---")
```

**一些 UI/UX 小技巧**：

- • 使用 st.container() 或 st.expander() 进行视觉分组。
- • 标题和图标（如 📝 或 🔗）打破单调，引导视线。
- • Markdown 允许你注入丰富的格式、链接甚至 LaTeX 方程，所以别害羞，美化那些摘要吧！

### 5. 高级优化：响应式与精致

想提升外观和体验？试试这些：

- • 使用 st.sidebar 添加设置（比如选择结果数量，切换摘要或完整答案）。
- • 通过 st.markdown 和 unsafe_allow_html=True 添加自定义 CSS，打造主题背景和卡片。
- • 使用 st.error 或 st.warning 优雅地显示错误信息。
- • **记住**：可访问性和鼓励很重要。添加工具提示、占位符文本和欢快的成功消息！

### 6. 测试你的应用！🚦

保存文件，然后在终端中导航到项目目录，运行以下命令启动 Streamlit：

```
streamlit run app.py
```

你的友好 AI 研究仪表板现在在 localhost:8501 上线了！

---

## 你做到了！

构建这个 UI 真是一个成就。你不仅实现了高质量、验证过的按需研究，还让它变得任何人都能轻松使用。如果你想冒险，探索 Streamlit 的文档，了解更多图表、标签和其他交互功能！

继续实验，别犹豫展现你的风格和 UX 调整。你正在成为全栈 AI 驱动数据应用的专家。快乐构建！🛠️

---

## 连接后端与前端的基础：实现无缝协作

你已经用 Pydantic AI 和 Tavily 构建了一个强大的后端研究 Agent，并设置了一个吸引人的 Streamlit UI。下一步——也是最棘手的——是让这两部分顺畅沟通，让用户能在你的便捷仪表板中提出问题并立即看到高质量、验证过的 AI 答案。

本节将带你完成 Streamlit UI 与异步研究 Agent 后端的连接，处理同步 UI 框架中的异步操作，解决新手常遇到的常见问题，并提供一个简洁、可复制粘贴的示例。同时，你会找到故障排除提示和清单，将困惑转化为信心。💡

### 1. 为什么连接异步后端到 Streamlit 很棘手？

你的 run_agent(query) 函数是异步的，但 Streamlit 期望普通的（同步）函数用于 UI 回调。这种不匹配可能导致错误，比如 `RuntimeError: This event loop is already running`，或者按下按钮后什么也没发生。在 Streamlit 环境中处理异步通常是第一个重要的“顿悟”时刻。

**问题**：

- • 异步函数适合非阻塞代码，但 Streamlit 的主循环是同步的。
- • 顶级 Streamlit 代码中不允许使用原生的 await。
**快速解决方案**：

- • 如果你不在异步循环中，使用 Python 的 asyncio.run()。
- • 如果在 Jupyter 中遇到循环错误，使用 nest_asyncio 修补循环。

### 2. 最小示例：整合前端与后端

以下是 app.py Streamlit 脚本所需的基本模式：

```
import streamlit as stimport asynciofrom your_backend_module import run_agent  # 你的异步研究 Agent 运行器try:    import nest_asyncio    nest_asyncio.apply()except ImportError:    pass# 非笔记本环境不需要st.title("🔎 AI 研究仪表板")st.write("在下方输入你的研究问题。Agent 将获取新鲜的网络数据和深刻的摘要！")query = st.text_input("今天想研究什么？", "强化学习是如何工作的？")if st.button("运行研究"):    with st.spinner('正在咨询你的研究 Agent，请稍候...'):      try:        results, main_content = asyncio.run(run_agent(query))        st.subheader("📝 摘要")        st.markdown(main_content, unsafe_allow_html=True)        st.subheader("🔗 顶级搜索结果")        for idx, result inenumerate(results, 1):            st.markdown(f"**{idx}. [{result.title}]({result.url})**")            st.markdown(result.snippet)            st.markdown("---")       except Exception as e:         st.error(f"发生错误：{e}")
```

**关键步骤**：

- • 使用 asyncio.run 桥接异步和同步世界。
- • 优雅地处理错误，确保 UI 不会无声崩溃。
- • 为笔记本/colab 环境应用可选的 nest_asyncio。

### 3. 故障排除与优化的清单 🛠️

以下是调试和优化的快速清单：

- • 正确导入和调用你的异步 Agent。
- • 在笔记本中使用 nest_asyncio 修补循环。
- • 用 try/except 包装 Agent 调用以处理错误。
- • 显示 UI 加载动画以提高响应性。
- • 将摘要和搜索结果渲染成清晰的部分。
- • 修改后端代码后重启 Streamlit！
- • 如果出现认证错误，检查 .env 和凭据。
- • 如果有问题，打印/记录调试信息。
- • 阅读错误堆栈跟踪，它们通常会告诉你哪一步失败了。

### 4. 常见问题与解决方案

**问题**：按下按钮后什么也没发生！

**检查**：确认你保存了后端更改，重启了 Streamlit，并检查按钮代码是否有拼写错误。

**问题**：出现 `RuntimeError: This event loop is already running`。

**修复**：在 Jupyter 环境中调用 nest_asyncio.apply()，命令行环境不需要。

**问题**：结果看起来很奇怪/为空！

**修复**：先将原始结果打印或显示到 Streamlit，可能是模式更新或查询错误导致对象为空。

**问题**：API 认证/权限错误。

**修复**：仔细检查 .env 并重新加载凭据。在 Streamlit 开发控制台中打印配置以验证密钥。

### 5. 更进一步：打造强大的实时 UI

熟悉同步调用后，尝试拓展：

- • 添加加载动画或骨架屏以增加精致感。
- • 如果你的 Agent 支持流式传输，尝试实时显示部分输出。
- • 考虑使用 Streamlit 的 session_state 添加对话历史。
- • **注意**：我们将在未来的帖子中涵盖以上内容。
太棒了！通过有条不紊地将后端研究逻辑连接到 Streamlit 仪表板，你已经完成了一个真正的端到端 AI 驱动数据产品管道。继续调整、扩展，庆祝吧，你正在成为全栈数据科学家！🚀

---

## 结论：后续步骤与提示

恭喜你走到这一步！你已经构建了一个研究 Agent 系统，结合了 Pydantic AI 的强大功能、Tavily 的实时网络搜索和 Streamlit 仪表板的实用性，全程使用模块化、可理解的 Python 代码。

---
