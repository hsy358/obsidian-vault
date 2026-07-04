---
title: "16万Star的免费Obsidian入库转换神器：微软官方开源MarkItDown：PDF/Word/PPT一键转Markdown"
author: "obsidian黑曜石"
publish_date: "2026-07-03 07:20:00"
saved_date: "2026-07-04"
source: "wechat"
url: "https://mp.weixin.qq.com/s/Q5N5VyR0N5fevbkNgvZ73w"
---
# 16万Star的免费Obsidian入库转换神器：微软官方开源MarkItDown：PDF/Word/PPT一键转Markdown
![](https://mmbiz.qpic.cn/mmbiz_jpg/yib5IbOMe3l4O7sNj3zXEZ4EZ3XwIxnBYXic9Be92J43z6WmHoxmXia3SV9wT8oD5eCWs8iaicMZFiazhTZsD1nALfzsbqKRIfYwrrDiaB2vmJFoNA/640?wx_fmt=jpeg&from=appmsg)

#

各位黑曜石的伙伴：又到周五了，一周下来你是不是有很多工作中的PDF、Word、Excel、PPT文档或者收藏的html网页想存入Obsidian?

上个月我在 Obsidian 里搭知识库，想把公司两年的项目文档导进来。PDF 用 Clipper 抓——排版炸了。Word 复制粘贴——表格变成乱码。PPT 更离谱，图文飞得到处都是。

三个小时，一个文档都没搞定。

直到我翻到了微软的 MarkItDown。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/yib5IbOMe3l655QSpnWqMA6dkia73LiafNiciawORbv9HjU4thUyCtUVLq4IquZruC4XmvyJhlbNENluRZHCGQNBEIgTWBNcI9K4Wicpeicysk72VI/640?wx_fmt=jpeg&from=appmsg)

## 一句话说清楚它是什么

MarkItDown 是微软 AutoGen 团队开源的 Python 工具，专做一件事：**把任何文件转成干净 Markdown**。

不是生硬抽文本。是完整保留标题层级、列表结构、表格、链接——转出来的 Markdown 人看得舒服，AI 读得顺畅。

GitHub 16 万 Star，PyPI 周下载量超 150 万。MIT 开源，免费商用。

## 它支持什么格式？

20+ 种。覆盖你电脑里几乎所有文件类型：

类别

格式

Office

Word (.docx)、PPT (.pptx)、Excel (.xlsx/.xls)

文档

PDF（含扫描件 OCR）、EPUB

多媒体

图片（OCR + 元数据）、音频（语音转写）

数据

CSV、JSON、XML

网页

HTML

黑科技

ZIP 自动解压批量转、YouTube 链接扒字幕

我最常用的是 PDF 转 Markdown——以前用 PyPDF2 抽出来的文本段落全粘在一起，MarkItDown 出来的结果标题、段落、列表分得清清楚楚。

## 3 行代码上手

安装就一行：

```
pip install'markitdown[all]'
```

不想装全量？按需选：

```
pip install'markitdown[pdf,docx,pptx]'
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/yib5IbOMe3l6Hjwf4VXmicvEIiaWh6AiaD3YmxEJicECbL1usIMebeMNSsss7L2viaKPkz2rNWfCvdV5M6qhEK8qETkCiaHzhne45OMhwibhu94UrLE/640?wx_fmt=jpeg&from=appmsg)

转换也只需要三行 Python：

```
from markitdown import MarkItDownmd = MarkItDown()result = md.convert("项目报告.pdf")print(result.text_content)
```

命令行更简单——一行搞定：

```
markitdown 项目报告.pdf -o 输出.md
```

## Obsidian 最佳搭档

我现在的日常流程：

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/yib5IbOMe3l6yztIPl6nMx0G87SYtLp4UMNodyftYg5tZUQBQMFC5keGysn8YV7Njc5Kr3PbmY87VQtWbXTmkv2jVQJPC2y2K8IrSef2e32s/640?wx_fmt=jpeg&from=appmsg)

**① 拖入文件** → **② MarkItDown 自动转 Markdown** → **③ 写入 Obsidian vault**

同事发来的 Word 周报、客户给的 PDF 方案、会议录音转写的文本——全部一键变成 Obsidian 里的 双向链接 就绪笔记。

如果你搭了 RAG 知识库或者用 AI 做文档分析，MarkItDown 是预处理第一步。大模型读 Markdown 比读 PDF 省 Token、解析更准——这是实测出来的，不是我猜的。

## 进阶：接大模型做图像描述

PPT 里的图、扫描件里的照片，默认转不出来文字。接上 GPT-4o 就行：

```
from markitdown import MarkItDownfrom openai import OpenAIclient = OpenAI()md = MarkItDown(llm_client=client, llm_model="gpt-4o")result = md.convert("季度汇报.pptx")print(result.text_content)
```

PPT 里的流程图、架构图——AI 自动生成文字描述，嵌进 Markdown。带图的 PPT 转出来不再是「[图片]」占位符。

## 谁适合用

•

**Obsidian 用户**：外部文档一键入库，双向链接就绪

•

**搭 RAG 知识库的开发者**：文档预处理省掉 80% 清洗工作

•

**职场人**：统一团队文档格式、做 AI 摘要、整理项目资料

•

**学生/研究者**：课件转笔记、文献整理、录音转文字

❌ 不适合：需要高保真排版（比如出版级 PDF 还原）——MarkItDown 的目标是"让 AI 读懂"，不是"让人打印"。

## 入手方式

```
pip install'markitdown[all]'
```

GitHub：github.com/microsoft/markitdown

16 万 Star，MIT 开源。微软维护，持续更新。

---

我踩过的坑是：不要自己写格式转换脚本。PDF 一个库、Word 一个库、PPT 又一个库——维护三套代码，每个都有边缘 case。MarkItDown 一个 `convert()` 全搞定，出问题去 GitHub 提 issue 比你自己 debug 快。

**如果今天的内容对你有用：**

🔴 **点亮「推荐❤️」** — 让你的同事也能告别文档格式内耗

📌 **收藏** — 下次导文档时翻出来照做

**评论区聊聊：你平时用什么工具把外部文档导入 Obsidian？**

**把这篇文章转给还在手动复制粘贴的同事** 🤫

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/yib5IbOMe3l51MLatLzvVBYb4Vu456gCaIZkibuC1wRCWwn51FxpXS7Q64NBFxmroPibkoKypAiakRI1lRDTXwibrx9maYg4CENwZHkq0ROg8Ggc/640?wx_fmt=jpeg&from=appmsg)

我是黑曜石，陪你打造第二大脑。微软 16 万 Star 的开源工具，三行代码让你的 Obsidian 吃掉任何格式。

## Obsidian最新热文

[发布60天评分 95 下载 9000+——这个 Obsidian AI插件自动把你的笔记变成知识库](https://mp.weixin.qq.com/s?__biz=MzkyODM0MzI3MA==&mid=2247484818&idx=1&sn=f59bf8b705feedd281a17a64f4732406&scene=21#wechat_redirect)

[Obsidian笔记一键导出多图，发小红书/朋友圈：预览即排版，5大增强让分享图秒变成品——Export Image XHS 完全指南](https://mp.weixin.qq.com/s?__biz=MzkyODM0MzI3MA==&mid=2247484806&idx=1&sn=49ab6ef2c0965584ab45185d18f44e35&scene=21#wechat_redirect)

[最好的Obsidian移动端体验，不在手机App里——在微信里](https://mp.weixin.qq.com/s?__biz=MzkyODM0MzI3MA==&mid=2247484710&idx=1&sn=f953aa2be893a3ba3bbaa4d15033c7d9&scene=21#wechat_redirect)
