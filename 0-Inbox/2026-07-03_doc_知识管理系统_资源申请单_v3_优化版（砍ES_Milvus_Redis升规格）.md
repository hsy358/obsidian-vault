# 知识管理系统（guyu）· 单机全量测试环境 · 资源申请单（v3 优化版）

申请人：何四燕　　日期：2026-07-03　　版本：**v3 精简版**（砍 ES + Milvus、Redis 升规格）

---

## ⚠️ v3 优化要点

| 原项 | v3 调整 | 理由 |
|---|---|---|
| ❌ Elasticsearch | **砍掉** | 最低 3 台集群起，单机不划算 |
| ❌ Milvus | **砍掉** | 难维护、容易出错、对资源要求高 |
| ⚠️ Redis 1 GB | **升到 2 GB** | 云中间件 1 GB 规格不好买，自建也偏小 |
| ℹ️ Nacos | **保留自建** | 云厂商虽有 Nacos 托管（阿里云 MSE / 腾讯云 TSE），但本项目按自建处理 |

> **业务影响**：guyu_python 砍掉 Milvus 后，将只走 **MySQL FULLTEXT + ngram 全文检索 + 外部 LLM API**；如需 RAG 后续可单独加。
> **MySQL 版本**：升到 **MySQL 8.x**，FULLTEXT 中文 ngram 解析比 5.7 好。

---

## 一、服务器规格

### 推荐配置（请按此申请）

- CPU：**8 vCPU**（从 16 降到 8，砍了 ES + Milvus 后业务压力下降）
- 内存：**32 GB**（从 64 降到 32）
- 系统盘：**300 GB SSD**
- 公网带宽：10 Mbps（允许突发）
- 公网 IP：1 个
- 操作系统：Ubuntu 24.04 LTS
- swap：建议关闭（32 GB 内存足够）

### 最低配置（保底）

- CPU：4 vCPU
- 内存：16 GB
- 系统盘：200 GB SSD
- 公网带宽：5 Mbps
- 公网 IP：1 个
- swap：4 GB

> 📌 **如果后期多人并发或文档量大**，可加配到 **16 vCPU / 64 GB / 500 GB SSD** 舒适档。

---

## 二、中间件清单（3 个，全自建）

| # | 组件 | 版本 | 端口 | 内存 |
|---|---|---|---|---|
| 1 | MySQL | **8.x**（含 FULLTEXT + ngram 中文分词）| 3306 | **8 GB**（升档，承载业务 + 全文检索）|
| 2 | Redis | **6.x / 7.x** | 6379 | **2 GB**（升到云中间件标准起步规格）|
| 3 | Nacos | **2.x** | 8848 / 9848 / 7848 | 2 GB |

**中间件合计：12 GB**

> 🟢 已无 ES / Milvus / etcd / MinIO，单机只跑 3 个中间件容器，省心。

---

## 三、业务服务清单

| # | 类别 | 服务 | 端口 | 内存 |
|---|---|---|---|---|
| 1 | Java | gateway（Spring Cloud Gateway）| 8080 | 1 GB |
| 2 | Java | knowledge/server | 8089 | 3 GB |
| 3 | Java | im-platform | 8888 | 3 GB |
| 4 | Java | im-server（Netty 长连接）| Nacos 配置 | 2 GB |
| 5 | Java | model（可选，本地 LLM 时启用）| 47639 | 1 GB |
| 6 | Java | knowledge 子项目（bank / robot / console / audit / common 等 6 个）| – | 5 GB |
| 7 | Python | guyu_python（**无 Milvus，改走 MySQL FULLTEXT + LLM API**）| 8667 | 6 GB（降，从 10-14 降到 6）|
| 8 | Python | preview（文档预览 / 格式转换）| 8669 | 2 GB |
| 9 | 前端 | admin_web（Vue + Node 18 构建）| 经 nginx | < 1 GB |
| 10 | 前端 | serv_web（Vue + Node 16 构建）| 经 nginx | < 1 GB |
| 11 | 代理 | nginx（80/443 反代）| 80 / 443 | 0.5 GB |

**业务合计：约 23.5 GB**

---

## 四、内存分配总计

| 区段 | 内存 |
|---|---|
| 3 个中间件（MySQL + Redis + Nacos）| 12 GB |
| 业务服务（Java + Python + 前端 + nginx）| 约 23.5 GB |
| 系统 + 日志 + Docker 临时 + 余量 | 4–6 GB |
| **总计** | **约 40 GB** |

> 推荐 32 GB：常规约 35 GB、高峰峰值约 40 GB。
> 📌 业务高峰时略紧（余量小），如压力上来建议升档到 16 vCPU / 64 GB。

---

## 五、磁盘分配参考（按 300 GB SSD）

| 区段 | 容量 |
|---|---|
| MySQL 数据 + FULLTEXT 索引（取代 ES 索引 + 部分 Milvus）| 150 GB |
| Redis 持久化 | 20 GB |
| Nacos 配置 + 日志 | 20 GB |
| Java / Python 日志 + Docker 临时 + 系统 | 80 GB |
| 文档上传文件（业务附件）| 30 GB（如需更大可挂对象存储）|
| **合计** | **300 GB** |

> 向量数据存储需求被砍掉（无 Milvus），磁盘压力大幅降低。

---

## 六、网络端口清单（IT 开放白名单用）

### 对外（通过 80/443）

- 80 / 443 → nginx

### 内网白名单（仅服务器内网可达）

| 端口 | 服务 |
|---|---|
| 3306 | MySQL |
| 6379 | Redis |
| 8848 / 9848 / 7848 | Nacos |
| 8080 | gateway |
| 8089 | knowledge/server |
| 8667 | guyu_python |
| 8669 | preview |
| 8888 | im/im-platform |
| 47639 | model（仅启用本地 LLM 时开放）|

> ✅ 比 v2 少 18 个端口（etcd 2379/2380、MinIO 9000/9001、Milvus 19530/9091、ES 9200/9300 全部消失）

---

## 七、软件环境要求

- **JDK 8**（knowledge 子项目）+ **JDK 17**（gateway，Spring Cloud Gateway 现代版官方要求）
- **Python 3.9**（guyu_python） + **Python 3.12**（preview）
- **Node 18**（admin_web 构建）+ **Node 16**（serv_web 构建）
- **Maven 3.8+**
- **Docker** + **Docker Compose V2**
- **Nginx**
- **MySQL 8.x FULLTEXT** ngram parser（中文检索）

---

## 八、关键架构变化（业务影响）

| 项 | v2 方案 | v3 方案 | 影响 |
|---|---|---|---|
| **全文检索** | Elasticsearch 7.x | **MySQL 8.x FULLTEXT + ngram** | 小数据量（万级文档）够用；超大文档库（千万级）需要再补 ES 或 OpenSearch |
| **向量检索** | Milvus | **❌ 砍掉**（纯 LLM API 模式）| 不再支持 RAG；如需 RAG 后续可单独申请 GPU + 单独向量库 |
| **LLM 推理** | 外部 API | **外部 API**（不变）| 维持纯 API 模式，本机不部署大模型 |
| **消息队列** | 无（自实现 Netty + Redis List）| 同 v2 | 维持自实现 |

---

## 九、状态说明

- ✅ **无消息队列（MQ）依赖**（与 v2 一致）
- ✅ IM 实时通讯：Netty（im-server 内嵌）+ Redis List 暂存离线消息
- ✅ 监控 / APM / 短信网关 / SMTP / OnlyOffice：**未部署**（按需追加）
- ✅ Nacos **自建**（不走云厂商托管）
- ✅ 单机只跑 3 个中间件（MySQL / Redis / Nacos），架构精简、维护成本低
