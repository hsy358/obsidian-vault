---
title: "MiniCPM-OCR 开源：把 “Jev” 用在文字识别"
author: "赛博禅心"
publish_date: "2026-10-28 20:03:03"
saved_date: "2026-10-28"
source: "wechat"
url: "https://mp.weixin.qq.com/s/X0SN4vxg8QoN9unqVja5yA"
---
# MiniCPM-OCR 开源：把 “Jev” 用在文字识别
刚刚，面壁智能和 OpenBMB 开源了 MiniCPM-OCR，这是一个非常有趣的 OCR 组合，包含两个部分：**一个负责识别文字，一个负责判断正确性**

一个认字，一个判卷MiniCPM-OCR · 发了什么原图认出的字0.980.960.410.97认字模型1.3B判卷模型2B两个都开源 · Apache 2.0

想在自己电脑上装，复制这句话，交给你的 agent 就行

阅读并执行 https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/SKILL_en.md

---

## 发了什么

先说文字识别的 MiniCPM-OCR，这个模型只有 1.3B，也是 MiniCPM-V/o 家族第一个专做 OCR 的模型，可以将各种文件（无论是照片、扫描件、还是 PDF），识别并导出一份能直接编辑的 Markdown

报纸、图表、公式，都能认MiniCPM-OCR · 发了什么认出来的报纸→ Markdown2026年8月31日 星期一连线评论员# 从一条渠读懂正确政绩观对话人：周珊珊 本报评论员许庆光 新疆日报评论员# 智能时代，如何与算法共处柱状图→ 表格YearLowMiddleHighVery high2014327462252016325775292018156573402020859695720227537360202411446276复杂公式→ LaTeX左边是原图，右边是认出来的

这一个模型有趣的一点是，它们会动态地调整文字的方向和大小，以便于更好地识别我们经常是对着一些拍歪了的文件进行图像识别，这就很能派得上用场了

拍歪了、字太小，也能认MiniCPM-OCR · 发了什么金额  62.00元真实拍摄评测 Real5：，第一

这里还有一份 benchmark，可见效果还是不错的

六项评测，四项第一MiniCPM-OCR 1.0 · 评测真实拍摄 Real5MiniCPM-OCR 1.093.68PaddleOCR-VL-1.693.19Xiaomi-OCR-092.73真实场景 WildMiniCPM-OCR 1.092.39Xiaomi-OCR-092.06PaddleOCR-VL-1.691.49通用 OCRBench v2MiniCPM-OCR 1.054.7Nanonets-OCR-s47.4Xiaomi-OCR-047.0语义先验噪声场景 CHAOSMiniCPM-OCR 1.029.78TeleOCR21.28Xiaomi-OCR-017.84OmniDocBench v1.6TeleOCR96.91Xiaomi-OCR-096.83Ovis-OCR296.58MiniCPM-OCR 1.096.51olmOCR-Benchchandra-ocr-285.8LightOnOCR-3-1B84.5Surya OCR 283.3MiniCPM-OCR 1.082.714 个开源 OCR 模型同场

在识别速度上，这一款模型也是十分的有优势。对于包含 1651 张页面图的 OmniDocBench v1.6 数据集，在同一张 NVIDIA GeForce RTX 5090 的显卡下，各种模型的速度如下

同样的文档，它认得最快MiniCPM-OCR · 发了什么MiniCPM-OCR 1.013.7 分钟GLM-OCR14.1 分钟PaddleOCR-VL20.4 分钟MinerU2.5-Pro49.6 分钟01020304050分钟认完 1000 页，约 14 分钟

**下面容我介绍下那个「Jev」**同一时间发布的还有一个 Jev 模型（2B），我觉得这是非常有创新性的一点，它的作用是把原图和识别出来的文字放在一起，给一个可信度的打分。如果分数较低，就可以提醒你这里或许是有问题的，需要人工处理一下

判卷模型给每一块打分MiniCPM-OCR · 发了什么合同编号：HT-2026-018合同编号：HT-2026-01800.510.99签订日期：10 月 28 日签订日期：10 月 28 日0.97金额：12,800 元金额：12,300 元0.31付款方式：银行转账付款方式：银行转账0.96分数在 0 到 1 之间，越高越可能认对

作为一个专用模型，在“判卷”这件事情上，它是能够和很多的大模型去掰一掰手腕的

判卷模型不大，判得很准MiniCPM-OCR Jev · 评测Qwen3.52B50.6Qwen3.59B72.0Qwen3.535B89.8JEV35B90.1Gemma 431B90.5MiniCPM-OCR Jev2B93.6Qwen3.5397B93.8JEV-VL27B94.0Qwen3.7-Plus未公开94.3Kimi K32.8T96.9Gemini 3.8 Flash未公开97.150 = 瞎猜100 = 全判对2B 的 Jev，和 397B 的 Qwen3.5 差不多准

两个模型的权重、推理代码和微调工具，都放在 GitHub 的 OpenBMB/MiniCPM-OCR 里

全部开源MiniCPM-OCR · 发了什么OpenBMB / MiniCPM-OCRApache 2.0两套权重BF16GGUFAWQGPTQ推理框架vLLMSGLangllama.cppOllama交给 agentSkill.md微调LLaMA-FactorySwiftApache 2.0

---

## 两个模型怎么配合

那接下来我们就看一看这两款模型是怎么配合的对此，我做了一个非常生动的动画，看一看

两个模型怎么接力MiniCPM-OCR · 怎么配合直接入库交给人看认字模型1.0判卷模型Jev

分高的识别区块能够直接录入，而分数低的可以让人再看一眼

人只看低分的几块MiniCPM-OCR · 怎么配合没有判卷模型有判卷模型复核完成

那如果大模型说这个区块确实没有问题，就会给它标记一个叫“免检”的 tag但这玩意儿真的可靠吗？面壁拿内部不同业务的 900 块图试过，还真是挺可靠的

大部分内容，不用人再看MiniCPM-OCR · 怎么配合免检法律文书财务票据复杂文档免检，直接录入交给人看法律文书 85% 免检，免检的部分全部认对

当然，这个判卷模型还能当裁判：比如你可以把同一页交给几个 OCR 各认一遍，然后每一块留下分最高的那份，这何尝不是一种拼好 R

几个模型一起认，挑最好的MiniCPM-OCR · 怎么配合MiniCPM-OCRXiaomi OCRPaddleOCR-VL拼起来原图0.970.950.930.710.940.880.620.580.910.960.900.97PaddleOCR-VL 　MiniCPM-OCR

---

## 怎么用

整套的模型与服务已经上线了 MiniCPM 的网站，国内是 platform.modelbest.cn，海外是 platform.modelbest.ai，开箱即用

网页上传就能试MiniCPM-OCR · 怎么用文档解析工作台+ 新建识别拖拽文件到此处，或 点击上传支持 PDF、JPG、PNG、WebP、GIF旋转自适应印章识别原始文档已摆正预览Markdown 源码二、相互作用—力(6)重力：G = mg  方向：竖直向下重力做功 WG = mgh重力的平均功率 PG = WG / t瞬时功率 PG = mgVy

当然，你也可以选择把这套东西装在自己电脑上，就把开头那句交给 agent，它会照着仓库里的说明一步步装好

第一次装好、把服务跑起来，大约要 3 分钟

一句话，让 agent 装好MiniCPM-OCR · 怎么用agent›Readandexecutegithub.com/OpenBMB/MiniCPM-OCR/…/SKILL_en.md检查显卡显存 ≥ 24 GB检查磁盘空间 ≥ 20 GB安装环境下载模型MiniCPM-OCR-1.0 + DSpark启动服务127.0.0.1:18499显存至少 24 GB

装好以后，一条命令就能把 PDF 变成 Markdown，表格也会一并转成 HTML

一条命令，PDF 变 MarkdownMiniCPM-OCR · 怎么用terminal$minicpmvocrparse--input采购合同.pdf--outputout.mdout.md#采购合同第一条甲方向乙方采购……<table><tr><td>品名</td>…

而对于那个 Jev，则可以直接在在 Hugging Face 上一行 Ollama

判卷模型，一行跑起来MiniCPM-OCR · 怎么用Hugging Faceopenbmb / MiniCPM-OCR-Jev-ggufImage-Text-to-TextGGUFquality-assessmentllama.cppLicense: apache-2.0Model cardFilesCommunityUse this model ▾MiniCPM-OCR Jev (2B) scores OCR candidatesfor text, formula, and table regions,returning a quality score from 0 to 1.Model size2B params4-bit  Q4_K_M1.27 GB8-bit  Q8_02.01 GBLocal Appsllama.cppLM StudiovLLMOllamaHow to use from Ollamaollama run hf.co/openbmb/MiniCPM-OCR-Jev-gguf:Q4_K_MCopyCopiedterminal$ollama run hf.co/openbmb/MiniCPM-OCR-Jev-gguf:Q4_K_M1.27 GB

对了，这俩模型的 api 后续还会放出来，敬请期待

---

## 原理

说回 Jev：为啥非要单独做一个判卷的模型？

现在新一代的 OCR，几乎都换成了能看图写字的大模型，整页看一遍就直接把结果写出来问题在于...OCR 模型这玩意儿，它识别错了，自己也不知道

认错了，它自己不知道MiniCPM-OCR · 原理原图认字模型认出来的认字模型把下标写错了，照样打勾说完成

倘若在平时办公也好，一个错别字影响并不大但在财务、法务、医疗这些地方就很要了老命了，比如说，你是切 5 厘米还是切 5 毫米，是吧？那在这种情况下，走一轮校验，看不清的天书，就能更准确地进入人工流程了

认错的字，判卷模型挑得出来MiniCPM-OCR · 原理原图候选 1纯种的甜玉米与纯种的非甜玉米实行间种植，收获时发现…………但在非甜玉米的果穗上找不到非甜玉米的子粒0.0067候选 2纯种的甜玉米与纯种的非甜玉米实行间行种植，收获时发现…………但在非甜玉米的果穗上找不到甜玉米的子粒0.984错两处的候选，分数掉到 0.0067

很显然，这种方法是非常省时、省力、省人工的

判卷模型给的分，靠得住MiniCPM-OCR · 原理它说：85% 可能对认对 它说：30% 可能对认对 人工核对：认对认错说 85% 可能对，就真有八成五对

另外得说一下，为什么这个模型是这么快？靠的一套叫 DSpark 投机采样小妙招：先让一个小模型猜几个字，再由大模型一次核对

认字模型为什么快MiniCPM-OCR · 原理猜定小模型大模型核对合同金颔合同金颔额为一万二为一万二千八百元千八百元DSpark 投机采样：效率

---

## 最后

业务里 OCR 用的多的朋友，不妨来试一试，两个模型加起来不到 4B，人人能跑了是

可以试试把下面这段话发给你的 Agent

阅读并执行 https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/SKILL_en.md

代码和模型，都在 GitHub 上MiniCPM-OCR · 最后OpenBMB / MiniCPM-OCRPublicStarCodeIssuesPull requestsActions.github/workflowsassets/minicpm-ocrdocsscriptssdkAGENTS.mdLICENSEREADME.mdAboutAn open-source OCR solutionfor fast, accurate documentparsing with correctnessassessment.image2textminicpm-vocrApache-2.0 licenseSkill：把这句话发给 coding agentRead and execute github.com/OpenBMB/MiniCPM-OCR/…/docs/SKILL_en.mdCopied!github.com/OpenBMB/MiniCPM-OCR
