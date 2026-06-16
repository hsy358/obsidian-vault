// Reusable editable architecture PPT template.
// Usage:
//   NODE_PATH=<node_modules paths> node scripts/pptxgenjs-template.js

require("module").Module._initPaths();
const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pptx.layout = "WIDE";
pptx.author = "AI Agent";
pptx.subject = "Editable architecture diagram";
pptx.title = "Editable Architecture PPT";
pptx.theme = {
  headFontFace: "Microsoft YaHei",
  bodyFontFace: "Microsoft YaHei",
  lang: "zh-CN",
};

const C = {
  blue: "0751B8",
  deep: "071F5C",
  line: "357EE2",
  ink: "10254D",
  muted: "4A5A78",
  white: "FFFFFF",
  green: "0B8B52",
  orange: "F26B16",
  purple: "6B35C8",
};

const S = pptx.ShapeType;
const font = "Microsoft YaHei";

function text(slide, value, x, y, w, h, opt = {}) {
  slide.addText(value, {
    x, y, w, h,
    fontFace: font,
    margin: opt.margin ?? 0.02,
    fit: "shrink",
    color: opt.color || C.ink,
    fontSize: opt.fontSize || 8,
    bold: opt.bold ?? false,
    align: opt.align || "center",
    valign: opt.valign || "mid",
  });
}

function round(slide, x, y, w, h, opt = {}) {
  slide.addShape(S.roundRect, {
    x, y, w, h,
    rectRadius: opt.radius ?? 0.06,
    fill: { color: opt.fill || C.white, transparency: opt.transparency || 0 },
    line: { color: opt.line || C.line, width: opt.width || 0.75, dash: opt.dash },
  });
}

function badge(slide, number, x, y) {
  slide.addShape(S.ellipse, {
    x, y, w: 0.34, h: 0.34,
    fill: { color: C.blue },
    line: { color: C.white, width: 1.2 },
  });
  text(slide, String(number), x + 0.02, y + 0.025, 0.30, 0.28, {
    color: C.white, fontSize: 15, bold: true,
  });
}

function stage(slide, item, x, y, w, h, index) {
  round(slide, x, y, w, h, { fill: "FBFDFF", line: C.line, width: 0.9 });
  badge(slide, index + 1, x - 0.04, y - 0.06);
  text(slide, item.title, x + 0.20, y + 0.08, w - 0.26, 0.25, {
    color: C.deep, fontSize: 9.5, bold: true,
  });
  if (item.subtitle) {
    text(slide, item.subtitle, x + 0.20, y + 0.31, w - 0.26, 0.16, {
      color: C.deep, fontSize: 6.5, bold: true,
    });
  }
  const rowH = 0.30;
  item.items.slice(0, 8).forEach((label, i) => {
    const yy = y + 0.55 + i * 0.36;
    round(slide, x + 0.10, yy, w - 0.20, rowH, { fill: C.white, line: "9BC3FF", width: 0.55 });
    text(slide, label, x + 0.15, yy + 0.05, w - 0.30, 0.18, {
      color: C.ink, fontSize: 6.5, bold: true,
    });
  });
}

const model = {
  title: "系统名称 | 可编辑架构流程图",
  subtitle: "用一句话说明这个系统如何把输入转成结果，并如何运行和反馈。",
  stages: [
    { title: "输入", items: ["资料", "目标", "约束"] },
    { title: "知识整理", items: ["抽取", "清洗", "建模"] },
    { title: "方案选择", items: ["配方 A", "配方 B", "配方 C"] },
    { title: "AI 编排", items: ["拆任务", "排依赖", "选能力"] },
    { title: "能力执行", items: ["Agent", "Runtime", "校验"] },
    { title: "资产生成", items: ["结构资产", "内容资产", "产品资产"] },
    { title: "人工编排", items: ["预览", "采纳", "调整"] },
    { title: "发布回流", items: ["发布", "数据", "反馈"] },
  ],
};

async function main() {
  const slide = pptx.addSlide();
  slide.background = { color: "F9FCFF" };
  text(slide, model.title, 2.2, 0.08, 8.9, 0.34, { color: C.deep, fontSize: 22, bold: true });
  text(slide, model.subtitle, 1.8, 0.46, 9.7, 0.20, { color: "333333", fontSize: 9.5 });

  const startX = 0.12, topY = 0.82, sw = 1.46, gap = 0.13, sh = 3.45;
  model.stages.forEach((item, i) => {
    const x = startX + i * (sw + gap);
    stage(slide, item, x, topY, sw, sh, i);
    if (i < model.stages.length - 1) {
      slide.addShape(S.rightArrow, {
        x: x + sw + 0.025, y: topY + 1.62, w: 0.22, h: 0.18,
        fill: { color: C.blue },
        line: { color: C.blue, transparency: 100 },
      });
    }
  });

  round(slide, 0.10, 6.90, 13.12, 0.48, { fill: C.blue, line: C.blue, width: 0 });
  text(slide, "核心原则：结构化输入、任务编排、能力执行、资产承接、发布运行、数据回流。", 0.6, 7.02, 12.1, 0.18, {
    color: C.white, fontSize: 9.5, bold: true,
  });

  await pptx.writeFile({ fileName: "editable-architecture-output.pptx" });
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
