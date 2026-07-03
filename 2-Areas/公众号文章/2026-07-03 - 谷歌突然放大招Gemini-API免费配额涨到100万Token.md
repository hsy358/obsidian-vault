---
title: "谷歌突然放大招！Gemini API免费配额涨到100万Token，还不用绑卡"
author: "无痕哥"
publish_date: "2026-07-03 19:00:00"
saved_date: "2026-07-03"
source: "wechat"
url: "https://mp.weixin.qq.com/s/tnELi7EPofIZ-D_yzFdC7A"
---
# 谷歌突然放大招！Gemini API免费配额涨到100万Token，还不用绑卡
![](https://mmbiz.qpic.cn/sz_mmbiz_png/I5YD6hibuZlXY43uV30KJo0alRV2qhs7QS3H360FLLXUdRqLshtfzB6ts9tVIXAoQ9FaKJQZG94R8gf7rjOYvhL48jLDErPBtuBPLVreG7hg/640?wx_fmt=png&from=appmsg)

说起来有点意外。昨天打开AI Studio，发现我的Gemini API配额突然变了——每分钟Token数从25万直接跳到了100万。

一开始以为是看错了，刷新好几次确认，确实是1,000,000。

查了一下才知道，谷歌7月1日悄悄给部分用户升级了免费配额，Gemini 2.5 Flash和Flash-Lite的免费额度直接翻了4倍。

---

## 一、先看最核心的变化

先说最让人兴奋的部分。

![](https://mmbiz.qpic.cn/mmbiz/I5YD6hibuZlUv8D1S0alUDyIF4Cfh0TwXNjJL4AC49vOMzvVZ7fIlTB1kfkA59MxAno07pKmjs7yVh57wORQia1MZJ6TcJ2iaakyiaI9BxKxlicw/640?wx_fmt=other&from=appmsg)
以前用Gemini API，免费版每分钟只能处理25万Token，写个长文档经常卡额度。现在好了——

**Gemini 2.5 Flash**：每分钟15次请求，每天1500次，每分钟Token数直接冲到100万。

**Gemini 2.5 Flash-Lite**：每分钟30次请求，每天1500次，每分钟Token数也是100万。

最关键的是，**不需要绑信用卡，不限总量**。

直接在ai.google.dev登录，拿到API Key就能用。

我赶紧试了一下，丢给它一篇5万字的文档让总结。以前这种任务分分钟触发限流，现在一次性搞定，输出了整整3000字的总结。

---

## 二、上难度：这个免费额度够怎么用

基础关过了，接下来算算账。

![](https://mmbiz.qpic.cn/mmbiz/I5YD6hibuZlWqe6wAnBhd9ib2wQEiafXoUAc1nVedXtmjT0zW8VEsjAdLvFGiblqRET8ozJ2PG5bfTdRKpusMPgTDtMCVToGm4rgvQG79rwIWRE/640?wx_fmt=other&from=appmsg)
100万Token是什么概念？

正常聊天，一轮对话大概消耗几百到几千Token。就算每天高强度用，1500次请求也足够折腾了。

举个例子：我每天用它写3篇文章（每篇约5000字），再处理10个文档总结，一天下来也就消耗10万Token左右。

100万Token够我用10天，而且是**每分钟**的额度。

更绝的是，如果你只是偶尔用用，比如每天就聊个十几次，这个免费额度基本等于无限。

不过有个细节要注意：不是所有用户都升级到了100万。有些账号显示的还是25万，看来谷歌是分批推送的。

---

## 三、杀手锏：但有个坑你必须知道

到这里还没完，真正需要注意的是——

**你的数据会被拿去训练模型。**

![](https://mmbiz.qpic.cn/sz_mmbiz/I5YD6hibuZlX3UEBYLXHkIfON0r6UnaEmrFNBVRcVib4bUqSn1QOPcqMxVhB1ia1wHoPqRic6C5WGy6gibl9qKnUuJYJiayicPWGpkQS3lvkOcib4IE/640?wx_fmt=other&from=appmsg)
Google AI Studio的免费版有个条款：谷歌保留使用你发送的提示和收到的响应来改进其自身模型的权利。

也就是说，你用免费API聊过的每一句话，都可能成为Gemini的训练数据。

除非你是欧盟用户——欧盟用户的数据不会被拿去训练。

这就有意思了，谷歌突然提高免费额度，是不是因为训练数据不够了？

另外，Pro模型不在免费范围内。如果你想用更强的模型，还是得花钱。价格也不便宜：Gemini 2.5 Pro输入100万Token要1.25美元，输出要10美元。

---

## 四、诚实的槽点

当然不是无脑吹。

![](https://mmbiz.qpic.cn/mmbiz_png/I5YD6hibuZlVFnP2hX3icb5N2cHVmNAIam4TXFM2mdZVeJtDbvPRuxnJibdnYHbfrSE8bgjzgZbYWmiaxR4Soe0RsdsCSEs5vxVAGZCqiaT9fvqE/640?wx_fmt=png&from=appmsg)

首先，不是所有用户都能享受100万Token，部分账号还是25万。其次，每分钟15次请求的限制还在，高频调用还是会受限。

最重要的是数据隐私问题——如果你的对话涉及敏感内容，免费版可能不是最佳选择。

---

## 写在最后

测下来最大的感受是：谷歌这次是真的下血本了。

100万Token的免费额度，对个人开发者来说基本够用了。写脚本、搞自动化、做小型AI应用，完全不用心疼Token。

但也要提醒一句：**免费的往往是最贵的。** 如果你在乎数据隐私，或者需要更高的请求频率，付费版或国内的AI工具可能更合适。

**优秀的AI工具，应该让你专注于创造，而不是操心额度够不够用。**
