/**
 * 方案 C：v4 generate-deck.js 限制前 4 页 + 加底图
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const VAULT = "/root/vault";
const PROJECT_DIR = path.join(VAULT, "1-Projects", "ey-24p-v4");
const slidesData = JSON.parse(
  fs.readFileSync(path.join(PROJECT_DIR, "slides.json"), "utf-8")
);

const C = {
  primary: "1B2D5C", secondary: "00A3B4", accent: "1E5BA8",
  ink: "10254D", muted: "4A5A78", white: "FFFFFF",
  bg_subtle: "F9FCFF", bg_alt: "FBFDFF", light_blue: "E8F0F8",
};

const F = { serif: "Georgia", body: "Calibri", zh: "Microsoft YaHei" };

const ICONS_DIR = path.join(VAULT, "1-Projects", "EY-China-AI-Reality", "PPT", "icons");
const PAGES_DIR = path.join(PROJECT_DIR, "pages_jpg");

function addText(slide, value, x, y, w, h, opt = {}) {
  slide.addText(value, {
    x, y, w, h,
    fontFace: opt.font || F.body,
    fontSize: opt.size || 12,
    color: opt.color || C.ink,
    bold: opt.bold ?? false,
    align: opt.align || "left",
    valign: opt.valign || "middle",
    margin: opt.margin ?? 0.05,
  });
}

function addRect(slide, x, y, w, h, opt = {}) {
  slide.addShape("roundRect", {
    x, y, w, h,
    rectRadius: opt.radius ?? 0.05,
    fill: { color: opt.fill || C.white },
    line: { color: opt.line || C.light_blue, width: opt.lineWidth || 0.75 },
  });
}

function addCircle(slide, x, y, w, h, opt = {}) {
  slide.addShape("ellipse", {
    x, y, w, h,
    fill: { color: opt.fill || C.white },
    line: { color: opt.line || C.primary, width: opt.lineWidth || 1 },
  });
}

function addIcon(slide, name, x, y, w, h) {
  const fp = path.join(ICONS_DIR, name + ".png");
  if (fs.existsSync(fp)) slide.addImage({ path: fp, x, y, w, h });
}

function addBackground(slide, pageNum) {
  const jpgPath = path.join(PAGES_DIR, `p${String(pageNum).padStart(2, "0")}.jpg`);
  if (fs.existsSync(jpgPath)) {
    slide.addImage({ path: jpgPath, x: 0, y: 0, w: 13.333, h: 7.5 });
  }
}

function addFooter(slide, page, num) {
  // 不加 footer，避免跟底图重叠
}

function addCallout(slide, text, y = 6.5, icon = "⊕") {
  // 不加 callout，避免跟底图重叠
}

// ============================================================
// Slide handlers（v2 实现）
// ============================================================
function addCoverSlide(slide, page) {
  // 底图已经在前面加了，这里只加 native text
  // 但 v2 cover slide 已经有完整 native text 实现
  // 这里我们让 v2 全部做做，然后在 main 里调换顺序（先底图后 native）
}

function addAgendaSlide(slide, page) {}

function addSectionDividerSlide(slide, page) {}

function addDataDashboardSlide(slide, page) {}

// ============================================================
// 简化版 handlers：每页只调 v2 实现 + 底图覆盖
// ============================================================
const handlers = {
  cover: (slide, page) => {
    // v2 cover 实现
    addText(slide, page.eyebrow, 0.5, 1.2, 6, 0.3, { size: 11, color: C.muted, italic: true });
    addText(slide, page.title, 0.5, 1.7, 6.5, 1.2, {
      size: 44, bold: true, color: C.primary, font: F.serif,
    });
    addRect(slide, 0.5, 3.0, 1.0, 0.05, { radius: 0.02, fill: C.primary });
    addText(slide, page.subtitle, 0.5, 3.2, 7, 0.8, { size: 18, color: C.secondary });
    addText(slide, page.tagline, 0.5, 4.2, 7, 0.5, {
      size: 14, color: C.muted, italic: true,
    });
    // 底部 5 步
    const stepNames = page.decorative.footer_5step;
    const stepW = 2.4;
    stepNames.forEach((name, i) => {
      const x = 0.5 + i * (stepW + 0.05);
      const isAccent = i >= 3;
      addCircle(slide, x + stepW / 2 - 0.3, 6.3, 0.6, 0.6, {
        fill: isAccent ? C.secondary : C.primary,
      });
      addText(slide, String(i + + 1), x + stepW / 2 - 0.3, 6.3, 0.6, 0.6, {
        size: 18, bold: true, color: C.white, align: "center", valign: "middle",
      });
      addText(slide, name, x, 6.95, stepW, 0.3, {
        size: 10, color: C.primary, bold: true, align: "center",
      });
    });
  },

  agenda: (slide, page) => {
    addText(slide, page.title, 0.5, 0.4, 12, 0.8, {
      size: 32, bold: true, color: C.primary, font: F.serif,
    });
    addRect(slide, 0.5, 1.2, 1.0, 0.04, { radius: 0.02, fill: C.primary });
    addText(slide, page.subtitle, 0.5, 1.35, 12, 0.5, {
      size: 14, color: C.secondary, italic: true,
    });
    page.parts.forEach((part, i) => {
      const x = 0.5 + (i % 2) * 6.3;
      const y = 2.2 + Math.floor(i / 2) * 2.2;
      addRect(slide, x, y, 6.0, 1.9, { radius: 0.08, fill: C.bg_subtle, line: C.light_blue });
      addCircle(slide, x + 0.3, y + 0.3, 0.7, 0.7, { fill: C.primary });
      addText(slide, String(part.num), x + 0.3, y + 0.3, 0.7, 0.7, {
        size: 22, bold: true, color: C.white, align: "center", valign: "middle",
      });
      addText(slide, part.title, x + 1.2, y + 0.4, 4.7, 0.6, {
        size: 16, bold: true, color: C.primary, font: F.serif,
      });
      addText(slide, part.desc, x + 1.2, y + 1.0, 4.7, 0.8, {
        size: 11, color: C.muted,
      });
    });
  },

  section_divider: (slide, page) => {
    addText(slide, page.part_label, 0.5, 1.5, 4, 0.4, {
      size: 13, color: C.muted, bold: true, charSpacing: 5,
    });
    addText(slide, page.title, 0.5, 2.2, 7.5, 1.5, {
      size: 36, bold: true, color: C.primary, font: F.serif,
    });
    addText(slide, page.subtitle, 0.5, 3.8, 7.5, 0.8, {
      size: 16, color: C.secondary,
    });
    addRect(slide, 0.5, 5.0, 7.5, 0.7, {
      radius: 0.08, fill: C.bg_subtle, line: C.secondary, lineWidth: 0.75,
    });
    addText(slide, "⊕", 0.6, 5.05, 0.6, 0.6, {
      size: 20, bold: true, color: C.secondary, align: "center",
    });
    addText(slide, page.callout, 1.2, 5.0, 6.7, 0.7, {
      size: 11, color: C.primary, bold: true, valign: "middle",
    });
  },

  data_dashboard: (slide, page) => {
    addText(slide, page.title, 0.5, 0.25, 12.3, 0.6, {
      size: 22, bold: true, color: C.primary, font: F.serif,
    });
    if (page.subtitle) {
      addText(slide, page.subtitle, 0.5, 0.85, 12.3, 0.35, {
        size: 12, color: C.secondary, italic: true,
      });
    }
    const cardW = 4.0, cardH = 1.7;
    page.data_cards.forEach((card, i) => {
      const x = 0.5 + (i % 3) * (cardW + 0.15);
      const y = 1.6 + Math.floor(i / 3) * (cardH + 0.15);
      addRect(slide, x, y, cardW, cardH, {
        radius: 0.06, fill: C.bg_alt, line: C.light_blue, lineWidth: 0.75,
      });
      // 不加 icon（底图已有）
      // 数据数字
      addText(slide, card.value, x + 0.25, y + 0.75, cardW - 0.5, 0.5, {
        size: 28, bold: true, color: C.primary, font: F.serif,
      });
      // 标签
      addText(slide, card.label, x + 0.25, y + 1.25, cardW - 0.5, 0.3, {
        size: 11, color: C.ink, bold: true,
      });
      // 时间
      addText(slide, card.time, x + 0.25, y + 1.45, cardW - 0.5, 0.2, {
        size: 9, color: C.muted, italic: true,
      });
    });
    // 底部 callouts
    if (page.callouts) {
      const cy = 5.4;
      page.callouts.forEach((cb, i) => {
        const x = 0.5 + i * 6.2;
        addRect(slide, x, cy, 6.0, 0.7, {
          radius: 0.06, fill: C.bg_subtle, line: C.secondary, lineWidth: 0.5,
        });
        addText(slide, cb.text, x + 0.2, cy, 5.7, 0.7, {
          size: 11, color: C.primary, bold: true, valign: "middle",
        });
      });
    }
  },
};

async function main() {
  const pptx = new pptxgen();
  pptx.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
  pptx.layout = "WIDE";
  pptx.author = "image-to-editable-ppt skill · 方案 C 前 4 页";
  pptx.title = slidesData.deck_title;

  // 只生成前 4 页
  const firstFour = slidesData.slides.slice(0, 4);
  for (const page of firstFour) {
    const slide = pptx.addSlide();
    slide.background = { color: C.white };
    addBackground(slide, page.id);  // 先加底图
    const handler = handlers[page.type];
    if (handler) handler(slide, page);
  }

  const outputPath = path.join(PROJECT_DIR, "ey-24p-first4.pptx");
  await pptx.writeFile({ fileName: outputPath });
  console.log(`✓ Generated: ${outputPath}（4 页）`);
}

main().catch((e) => { console.error(e); process.exit(1); });