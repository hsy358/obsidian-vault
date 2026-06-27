---
title: Superpowers + OpenSpec 双剑合璧：AI 全栈编程新范式，从零对话式搭建企业级知识库
author: 每天译点晓知识
publish_date: '2026-05-19 22:17:59'
saved_date: '2026-05-30'
source: wechat
url: https://mp.weixin.qq.com/s/NsdUalJWe43xbWCIekcIVA
type: wechat-article
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
  source_url: https://mp.weixin.qq.com/s/NsdUalJWe43xbWCIekcIVA
description: 产品场景：本系统是一个AI驱动的全自动化开发平台，能够根据用户提出的需求自动完成从需求分析到代码生成、测试、评审和部署的完整开发流程。前后端主要以：
timestamp: '2026-05-19T22:17:59'
resource: https://mp.weixin.qq.com/s/NsdUalJWe43xbWCIekcIVA
tags:
- AI
- notes
- 产品经理
- 公众号
---
# Superpowers + OpenSpec 双剑合璧：AI 全栈编程新范式，从零对话式搭建企业级知识库
### 前言

![](https://mmbiz.qpic.cn/sz_mmbiz_png/gphOCPdHkku0dSwqicKrZD0GI03IjG2LuiaibCP0tsibT94L4FXPGhib0EC2o8SCjS0zf3L6YoNsYRPjIS3abNtZBtQ/640?wx_fmt=other&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7Rzic1M87zgYNDGNYticT6Oa3dJycIDGMefZtTp3rq85C7bmznbKUn7nLPjIr66kpUf9LUFtiakiaK0bDAXLa3C5S0ogQeib0nPdu0yE/640?wx_fmt=png&from=appmsg)

用户需求描述：

产品场景：本系统是一个AI驱动的全自动化开发平台，能够根据用户提出的需求自动完成从需求分析到代码生成、测试、评审和部署的完整开发流程。前后端主要以：

![](https://mmbiz.qpic.cn/mmbiz_png/q4xZ6YaA7RyM8NdZibzctrkAC8lUmgO7HEI1I7eFiamVns3vQe2d5ng2Hsn1uQJQ4MdUr0vypK2XpdiaONtBaewciaH6o0npqPMWSbN6Ppz5v0E/640?wx_fmt=png&from=appmsg)

java语言（java.version17+、 Maven 3.8+、SQL Server 2022+、Vue.js ，算法用 AI 目前主流的模型 阿里百炼、智谱 GLM 系列等，还有RAG、向量库，生成一个完整的前后端+AI 项目（全栈）。

![](https://mmbiz.qpic.cn/mmbiz_png/q4xZ6YaA7RwrmEZEreEK6D4MWCicFFic6FRyuk6r4oI47SHhaMbHC7JR6JAU3XglVBVtKDzh1iapdibJc6x9p1c67JGDx49mBAIYO92xiapPgQ1A/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_png/q4xZ6YaA7Rz2Tqbqd0jxxbEIfn0wXQ9nrmAibMN9OPMergrPr7LYw1j8ia8r6BXsKI3MzuXphJSibaibeq0meiczoEwiaorg1zXHOaJLzCDz1z8DI/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_png/q4xZ6YaA7RxibmPPU6fib4ia1x8N6lM3hHBpmckwsJFib49ftibw43Vtn2kKfhpgraj4FQ4uwMkZB1vqiaQfxIO2jCEwAyjicchcKhPFHJvxBJfROw/640?wx_fmt=png&from=appmsg)

落地技术选型：为什么是这套组合拳？

后端：Java 17 + Spring Boot + MyBatis-Plus

由于系统对稳定性要求极高，Java 生态无疑是不错的选择。Spring Boot 提供了完善的 WebFlux 支持，为后续的流式 AI 对话打下基础。MyBatis-Plus 让数据库操作变得异常优雅。

前端：Vue + Element Plus + Vite

现代化的前端框架配合成熟的组件库，可以让你快速完成数十个核心页面的开发。Vite 的 HMR 热更新让调试效率提升 3 倍以上。

AI 层：大模型 LLM + RAG + 流式响应

大模型 LLM 配合 RAG（检索增强生成）架构，让 AI 的回答严格基于特定知识库知识库，避免了「幻觉」问题。流式响应技术让用户获得打字机般的丝滑体验，其中嵌入模型采用：embedding

DBMS存储：SQL Server + 向量数据库 + Redis

用户使用 SQL Server，这是现实约束。向量存储这里暂时采用了轻量级的本地存储方案，像需要支持百万级向量检索，可以升级为 **HNSW 索引**（通过Faiss或pgvector实现），查询耗时可降至10-50ms，同时保持95%以上的召回率。

方案

查询耗时

内存占用

召回率

实现难度

线性搜索

5-10秒

6GB

100%

简单

HNSW索引

10-50ms

2GB

95%

中等

pgvector

20-100ms

3GB

95%

简单

Milvus

10-50ms

4GB

97%

复杂

![](https://mmbiz.qpic.cn/mmbiz_png/q4xZ6YaA7RyicfrkpfIjFiczAUwpGJBRz5XUHs8APdOgp6dnibH2q89iajebyG60bhaG87PKZJ6qtibqHBoovjfowb0Z6m4j1kicQIOBMNq0bAlqY/640?wx_fmt=png&from=appmsg)

智能编写引擎：

传统的文档编写需要查阅大量资料，用户在编辑器中输入需求，系统自动检索知识库，调用 大模型 生成专业内容。

**技术亮点**：

- 基于 LangChain4j 实现 RAG 架构
- 流式输出，逐字显示，体验如 ChatGPT
- 支持续写、润色、摘要、术语检查四大场景

### 项目实战

[基于 ClaudeCode 开发前后端传统基础项目](https://mp.weixin.qq.com/s?__biz=Mzg3MTIyNDA3Mg==&mid=2247500792&idx=1&sn=bb1ebec0de188079be63e008b28fc1c4&scene=21#wechat_redirect)->可参见

[AI 全栈开发最强组合：实战Cursor+Claude Code+Kimi2+Qwen3-Coder，从0-1自动化构建完整应用](https://mp.weixin.qq.com/s?__biz=Mzg3MTIyNDA3Mg==&mid=2247500792&idx=1&sn=bb1ebec0de188079be63e008b28fc1c4&scene=21#wechat_redirect)

本文进阶高级项目：

前提：需要安装（Superpowers+Openspec）

![](https://mmbiz.qpic.cn/mmbiz_png/q4xZ6YaA7RxeZibgOEFb4gq4ryuHy5ibRuF2GTKuhjVf2DibCQ3YEkL7eODzzwl1zgE1t6ibUjKiaic3Ph41ezrW58cic48XJdNJVVPZz8fobzlRgQ/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7RxN5ia2ohq4a5uAkZlNedWWZ9h3nszcicnZqwdicibpcbzVMTn8H8TO8mHbiasqb9glqBlHW6p665tVrumbpX7uegibDPQssragYZdnE/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_png/q4xZ6YaA7RwSUIm9OmPSwXbps4oKNRymXXJvMX0YGSibOdPKtHrW1sH6QjOwmye0MvqQcmkgt5riawk6SQTGYohpD03EfdVhk3kMc3YibOriaT8/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_png/q4xZ6YaA7RwOfHPEdic2G5KIZtYU8ZX8ggGQ10wWfeUBgkyzV4ycWgkhNh5pU2ia4j8ZLClJoXIstHSymNjjdGtbtaO4ah1iajj2paUCUkbEic4/640?wx_fmt=png&from=appmsg)

Superpowers下是一套有先后顺序的开发流水线：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7RxEpykj3zBBhIbEefVM5qkNDrWIwadgxlnPyvg3V288h4lOTApQpmqSJVohnbRBEEJTJwicFIhEibWZ0JlXFs5S9S2gDqUyXlql4/640?wx_fmt=png&from=appmsg)

基于ClaudeCode（Superpowers+Openspec）实战开发自动生成的 AI 全栈项目脚手架：

![](https://mmbiz.qpic.cn/mmbiz_png/q4xZ6YaA7RzJfqpya8DWywque9F2VIF6p4EOpgnzMW5cTs0DQ5JLZCoqcyjfJWxSWlmcqO3bjM00LyicTSFwSedtLGX3uGUm1PSq2iaibhIHiaw/640?wx_fmt=png&from=appmsg)

这里对一些常见使用命令作下简单介绍（一些基础的语法可先提前学习了解）：

-

```
/opsx:propose "实现xxx功能"
```

AI 会进行自动生成：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7Rxsic5E78e0icXXH5UxlsQRj97YkxX7L64T2C85UTsibkPAtlGRicTMdj3eEtoeNzHLHs3ibObYkBuic8Q8lP0ibodZplXXxqjTICgsLQ/640?wx_fmt=png&from=appmsg)

比如像我们需要AI协助修改前后端调试过程中的问题，可以这样指定：

修改前端问题：

-
-
-
-
-

```
 /opsx:propose "后端接口返回正确，但是前端页面没有对应展示，修改技能包列表页面，现在调用后端接口有输出但是页面没有展示，并且有个圈圈在转                                             后端接口详细见，接口日志，回答请进行中文输出" --lang zh 求 URL                                                                                                                      http://localhost:5173/knapi/api/skill/list                                                                                                                                          请求方法                                                                                                                                                                            GET  状态代码  200 OK {      "code": 200,      "message": "success",      "data": [          {              "id": 1,              "packageName": "ai-analysis-skill",              "version": "1.0.0",              "author": "",              "description": "No description",              "fileSize": 0,              "status": "INACTIVE",              "fileName": "ai-analysis-skill.zip",              "uploadTime": null,              "installTime": null,              "installedPath": ""        }      ]  }
```

![](https://mmbiz.qpic.cn/mmbiz_png/q4xZ6YaA7Rxdv6ykgT4OOXZLES2voIL4uL2avzAkTAibaEHd3M7AMxavX7CjSg5FuiaNTQJUyBJLaef1IN9qgHEzqagx9oTnhZfEkR7XicWN0E/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7RwbQCPlkRc98xHPtRnZPYMmibU0PLxh3QOUA9YVqQQnhKew5zY7GU3g8oxpJWE1xdbB8H0HqdGQ86VVEUKLQOvdxdz30yGWL2a0/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7RwJECIriajiawJ3G1zHich8PKlyib6VibGCS6HZfEsiae3alGBgnVN1uHRDDAxvhDzica11GpqpicZOy4NLM53dS4fUicyGAkNV4YSJibjvc/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7RwEXLT64zicVibSxXeVHou9Lia4aGWtWtpOVtuTUtmvAfibrpQXhdHInXww3RJ4oibmet7bwSN1xkdFq9aJSdLbFiarIHftnyXE6IbKo/640?wx_fmt=png&from=appmsg)

修改后端问题：

-
-
-
-

```
❯ /opsx:propose "前端点击多agent系统菜单，点击文档分析，后端接口报错详细见日志，回答请进行中文输出" --lang zh DEBUG 8992 --- [nio-8083-exec-1]              o.s.w.s.m.m.a.HttpEntityMethodProcessor  : Using 'application/json', given [application/json, text/plain, */*] and supported [text/plain, */*, text/plain, */*, application/json,   application/*+json, application/json, application/*+json]                                                                                                                           DEBUG 8992 --- [nio-8083-exec-1] o.s.w.s.m.m.a.HttpEntityMethodProcessor  : Writing ["处理请求时发生错误: <EOL><EOL>### Error querying database.  Cause:    com.microsoft.sqlserver.jdbc.SQLServerException: 列 (truncated)..."]
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7RxEl3oiajIb3x0fjgjBlrINkWXzosvut7tZoJECVI8e1DjWiaibcSRYfNGColRVdAHdeW81cFpv1tRxrsfebpHxOjClnCbWNoGhvU/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7RzMdnsibOdBV7ZR4wNLoaC7C4xcibmWefNUicicbOcU3SRDgic5bo1cOxRcSSHMqQmV5AuKcrKh4T5MtxAyqW7WYoUsEyKBGCbC2wjo/640?wx_fmt=png&from=appmsg)

-
-

```
 /opsx:apply  开始，然后可以人工 Review 再决定提交 /opsx:archive 功能完成最后再归档到openspec/specs/
```

![](https://mmbiz.qpic.cn/mmbiz_png/q4xZ6YaA7RxiapsJsPJ1icwfx5Bhn5kM4E2vBpztdfgGuYmzN2nnQYPeP27xCshc068S9Pxd0jYmD5dqm6W6rVibgSulBAeeX0eQEFX9vN1adQ/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7RwgKrrcsOoALY6w6vT3R3vXe7A6iaBUruIwG5JiccfSafDnvZ12GraP5HgiakeOkypQVReemwuamGcrK5VCIkorbDup2mzhK4yicpw/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7RxbFvOdo4G4luMbDyyLPlQaChewb78ias6EJU4kNiaq2fR6HvxBT71iajUfCyu1OKUgYZILU7ic9wmOkU3j2TNvF0Z8Wzus47LRicgY/640?wx_fmt=png&from=appmsg)

像上述简单的完全可以交给 **OpenSpec ，而对于需要搭配 Superpowers**使用的（进行质量把控）：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7RwCiaUGvT9v5Iyq9rKM1V8Q4WzHM1b3DPXictdXBbS4icafPduwGf74fvmI6AyAFWKoibBbSBWXEV0bRAW5h0zrukbY9n7biaOv3CMA/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_png/q4xZ6YaA7RzTKQ8IVjWTicPrFyBa2NGGVAcAaQaPeyEiaeXUrN8iapPu34tSUmVEmbqSf73U3Ln5TwRMPFnEQcCJeTGJxZvyGMtsmon2vicKrkk/640?wx_fmt=png&from=appmsg)

-
-
-
-
-
-
-
-
-
-
-

```
根据以下OpenSpec规范文档，并基于这些规范使用Superpowers的writing-plans流程拆分实现计划：1. 读取 openspec/changes/fix-intelligent-writing-features/design.md 作为技术方案2. 读取 openspec/changes/fix-intelligent-writing-features/specs/ 下的所有场景作为测试依据3. 读取 openspec/changes/fix-intelligent-writing-features/tasks.md 作为任务列表4. 读取 openspec/changes/fix-intelligent-writing-features/proposal.md 的排除范围作为审查依据每个task拆成Superpowers plan的粒度：1. 写失败测试2. 运行测试3. 写最小实现4. 运行测试5. 重构6. 提交
```

*温馨提示*：OpenSpec->explore、propose、apply、sync、archive，apply这个流程是让AI按照tasks.md实现代码，而选择Superpowers来执行，apply这一步就被Superpowers 的TDD流程所替代——做得更好，有测试纪律、代码审查、验证机制。

企业级知识库-团队多 Agent 智能自动化产研系统展示

... loading ...

AI科技变化可谓是日新月异。像行业内的各个“兵种”，在当下AI利器的加持下变得事半功倍，“ATA”跟“OPC”时代或许即将到来？需要的就是学以致用，持续保持学习以促进全面提升 ... ...

![](https://mmbiz.qpic.cn/mmbiz_png/q4xZ6YaA7RxGpkYW2lRxe6JUFmy5cv446Z9vrxS05w0ttLcib6xZmc4iana1N38DfNjscPVUFU01ibdJcWCeRMpyndfHy4DF9rVDJWs7BTUEQU/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7RwpcEibuZATz6o9FtZDuNMmPtZPhIKcfv7rV04RIibskxErVwbev21fgBhiaK5x6Y0iaibZ9W2zrIjuwaVd2TWicWQEsmsnoZPhIpugs/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7RwxgKdjwN23jO3AWolvaMNLuTtiascmoNhrHic4yzgibYquu6ynmnHfB5VAqicNGCsWHEqzCDq18wlACw6GwjDV69CfUmFG5iaQjlYU/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q4xZ6YaA7RxGjhSEy5dL46Wic05xaZrQzcxnC1OEdsLrcKLnN3b406BH0Yibc2gORBMDxq6ve7IRXA1lH4ESErLIsG5ds5gyuEXfxMZMyJaNA/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_png/q4xZ6YaA7Ry7rY7Df7j8pd9WhQ18qB2B97DIyEHjxVLkfbGZtA2jLNhkl2LUzib3eMfIRXf7wkTjKt2aUiaWnaCictibL4fYB8KKXb9iaOGlPhbc/640?wx_fmt=png&from=appmsg)

### 末尾-附：上述 AI 全栈新范式正在持续迭代推进中，可以后台交流一起探讨。

[从知识中来，到知识中去!](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz=Mzg3MTIyNDA3Mg==&scene=1&album_id=3376222984675311616&count=3#wechat_redirect)

点击下方卡片 关注我

↓↓↓

往期文章

[AI 科普 | 人工智能大模型](http://mp.weixin.qq.com/s?__biz=Mzg3MTIyNDA3Mg==&mid=2247499491&idx=1&sn=0135e38519bb404c3cb27eac386b020b&chksm=ce837884f9f4f19290d0aa1673b931f1cb10f404bbb83104bfa689430ab616aee4e53a0e961d&scene=21#wechat_redirect)

[AI：介绍一种垂类的提示词获取方法！](http://mp.weixin.qq.com/s?__biz=Mzg3MTIyNDA3Mg==&mid=2247499981&idx=2&sn=cf063e5a4a3c166fb822c79085477ce4&chksm=ce8346aaf9f4cfbcccde3c9b6ed5452b211a6c487bddd807e8f9724b2e9c6e7031d6ad9532bd&scene=21#wechat_redirect)

[AI | 从0-1手把手打造一款属于自己的大模型创意应用！](http://mp.weixin.qq.com/s?__biz=Mzg3MTIyNDA3Mg==&mid=2247499443&idx=1&sn=42bca1d20738467a187c1e87ae5623cd&chksm=ce8378d4f9f4f1c28270810bcf4125426ea218fecd959ed331abca84b8322afe005bd2c18e63&scene=21#wechat_redirect)

[走进大模型（LLM）+智能体（Agent）+提示词（Prompt）](https://mp.weixin.qq.com/s?__biz=Mzg3MTIyNDA3Mg==&mid=2247500555&idx=1&sn=a74e82a7130c982461ee09f907ec5f85&scene=21#wechat_redirect)

[AI 有感：智能体 = 提示词工程 + 大模型算力 + 插件类工具？](http://mp.weixin.qq.com/s?__biz=Mzg3MTIyNDA3Mg==&mid=2247500125&idx=1&sn=3b40183cb6cf9aa30c6a59de73406751&chksm=ce83473af9f4ce2c023c7b9bdc37349c549269c87b969ce8d1cfd1c3ebc2b5f4a26ae741af68&scene=21#wechat_redirect)

[新一代 AI 智能化搜索：如何在亿万数据海洋中，高效捕捞“宝藏知识”？](http://mp.weixin.qq.com/s?__biz=Mzg3MTIyNDA3Mg==&mid=2247500210&idx=1&sn=937e6e300acf9c26c15f8d2d3bf54587&chksm=ce8347d5f9f4cec338747c4d930c40420f51f571875f4f4960caf27244fa0a6b5e3c8407f38a&scene=21#wechat_redirect)

[AI 新范式：模型即服务 -> MaaS 开放平台 GLM-4-AllTools（硬核干货）](http://mp.weixin.qq.com/s?__biz=Mzg3MTIyNDA3Mg==&mid=2247500430&idx=1&sn=575090c4189877ac82de30f100664247&chksm=ce8344e9f9f4cdff7128e432fcc2fc34c8cc058f75424dc177db3245a4a435915ef364a111cb&scene=21#wechat_redirect)

[GLM-4-Flash 免费：与你一起共话西游，懂你的“悟空”](https://mp.weixin.qq.com/s?__biz=Mzg3MTIyNDA3Mg==&mid=2247500635&idx=1&sn=b4c669c308f479e6da72ff9d91090a90&scene=21#wechat_redirect)
