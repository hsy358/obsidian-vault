---
type: article-metadata
file_type: html
file_path: /root/vault/2-Areas/公众号文章/2026-10-20 - CADCraft - 纯Rust开源CAD设计工具.md
source: https://github.com/storytold/cadcraft
uploaded_date: 2026-10-20
title: "CADCraft - 纯Rust开源AutoCAD风格CAD制图工具"
description: "Clean-room纯Rust实现的开源CAD应用，兼容AutoCAD命令行习惯，Agent可通过MCP驱动，支持DXF/DWG文件"
size_bytes: 0
tags: [CAD, Rust, open-source, MCP, AI-agent, CADCraft, AutoCAD]
---

# CADCraft

> GitHub: https://github.com/storytold/cadcraft
> License: MIT OR Apache-2.0
> 语言: Pure Rust
> 平台: macOS / Windows / Linux / FreeBSD / Web (WASM)
> 状态: 早期开发（v0.5.0）

## 核心定位

CADCraft 是一个**clean-room 纯 Rust 重写的 AutoCAD 替代品**，不是逆向工程，而是按 AutoCAD 的命令行习惯和文件格式**重新实现**。

核心理念：
- 兼容 AutoCAD 命令行操作习惯（命令行提示、对象捕捉、极轴、正交、grips、右键重复）
- 开放文件格式（DXF/DWG 支持）
- **Agent 可通过 MCP 驱动**画图

## 同家族 Crafting Apps

ArtCraft 团队做了一整套：

| 项目 | 对标 | 状态 |
|---|---|---|
| CADCraft | AutoCAD | v0.5.0 |
| Photocraft | Photoshop | 开发中 |
| Vectorcraft | Illustrator | 开发中 |
| Filmcraft | Premiere | 开发中 |
| Lightcraft | Lightroom | 开发中 |
| Pdfcraft | Acrobat | 开发中 |
| Effectcraft | After Effects | 开发中 |
| Designcraft | Figma? | 开发中 |

## Agent 驱动方式

启动：`cargo run --release -p cadcraft -- --sample --control PORT`

通过 JSON-RPC 控制（127.0.0.1:PORT）：

```json
// 方式1：命令行输入（完全模拟用户输入）
{"id":1,"method":"cmdline.input","params":{"text":"circle 0,0 5"}}

// 方式2：JSON 结构化命令
{"id":2,"method":"engine.execute","params":{"command":"line","params":{"points":[[0,0],[5,5]]}}}
```

## 技术特点

- **纯 Rust**：性能+内存安全
- **Clean-room**：无 Autodesk/Adobe 代码，图标/字体/图案全自研
- **WASM**：浏览器里跑 CAD
- **MCP 支持**：AI Agent 直接驱动

## 最新版本

v0.5.0 (2026-10-11)，提供 Linux AppImage / rpm / tar.gz 多格式下载
