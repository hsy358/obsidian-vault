/**
 * Image-to-Editable-PPT · pptxgenjs 生成模板
 * 基于 EY 24P 复刻项目沉淀。
 *
 * Usage:
 *   1. 准备好 slides.json + theme-tokens.json + icons/
 *   2. cd <output-dir>
 *   3. NODE_PATH=/root/.nvm/versions/node/v22.22.2/lib/node_modules node generate-deck.js
 *
 * Required:
 *   - pptxgenjs (npm install -g pptxgenjs)
 *   - slides.json (24 页结构化定义)
 *   - theme-tokens.json (主题配置)
 *   - icons/ 目录 (PNG 图标，可选)
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// ============================================================
// 1. 加载配置
// ============================================================
const SLIDES_JSON = path.join(__dirname, "slides.json");
const THEME_JSON = path.join(__dirname, "theme-tokens.json");
const ICONS_DIR = path.join(__dirname, "icons");

const slidesData = JSON.parse(fs.readFileSync(SLIDES_JSON, "utf-8"));
const theme = JSON.parse(fs.readFileSync(THEME_JSON, "utf-8"));

// ============================================================
// 2. 颜色（从 theme tokens 提取）
// ============================================================
const C = {
  primary: theme.colors.primary.value.replace("#", ""),
  secondary: theme.colors.secondary.value.replace("#", ""),
  accent: theme.colors.accent.value.replace("#", ""),
  ink: theme.colors.neutral.gray_900.replace("#", ""),
  muted: theme.colors.neutral.gray_500.replace("#", ""),
  white: theme.colors.neutral.white.replace("#", ""),
  bg_subtle: theme.colors.background.subtle.replace("#", ""),
  bg_alt: theme.colors.background.card_alt.replace("#", ""),
  light_blue: theme.colors.neutral.very_light_blue.replace("#", ""),
};

// ============================================================
// 3. 字体
// ============================================================
const F = {
  serif: theme.typography.serif_font.value,
  body: theme.typography.primary_font_en.value,
  zh: theme.typography.primary_font_zh.value,
};

// ============================================================
// 4. Helper
// ============================================================
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
  if (fs.existsSync(fp)) {
    slide.addImage({ path: fp, x, y, w, h });
  }
}

function addPageTitle(slide, title, subtitle) {
  addText(slide, title, 0.5, 0.25, 12.3, 0.6, {
    size: 22, bold: true, color: C.primary, font: F.serif,
  });
  if (subtitle) {
    addText(slide, subtitle, 0.5, 0.85, 12.3, 0.35, {
      size: 12, color: C.secondary, italic: true,
    });
  }
}

function addCallout(slide, text, y = 6.5, icon = "⊕") {
  addRect(slide, 0.5, y, 12.3, 0.5, { fill: C.bg_subtle, line: C.secondary });
  addText(slide, icon, 0.6, y + 0.05, 0.4, 0.4, {
    size: 18, bold: true, color: C.secondary, align: "center",
  });
  addText(slide, text, 1.1, y, 11.5, 0.5, {
    size: 11, color: C.primary, bold: true, valign: "middle",
  });
}

function addFooter(slide, page, num) {
  addText(slide, "⊙", 0.3, 7.05, 0.25, 0.3, { size: 9, color: C.muted, bold: true });
  addText(slide, page.footer.left, 0.55, 7.05, 10, 0.3, { size: 8, color: C.muted });
  addText(slide, String(num), 12.5, 7.05, 0.6, 0.3, {
    size: 10, color: C.primary, bold: true, align: "right",
  });
}

// ============================================================
// 5. Slide Type 处理器（13 种）
// ============================================================
// 注意：这里只给出最简实现，覆盖 13 种 type。
// 完整实现见 references/slide-patterns.md 和 EY 项目 generate-deck.js。

const handlers = {
  cover: (slide, page) => {
    slide.background = { color: C.white };
    addText(slide, page.eyebrow || "", 0.5, 1.2, 6, 0.3, { size: 11, color: C.muted, italic: true });
    addText(slide, page.title, 0.5, 1.7, 6.5, 1.2, {
      size: 44, bold: true, color: C.primary, font: F.serif,
    });
    addRect(slide, 0.5, 3.0, 1.0, 0.05, { fill: C.primary });
    addText(slide, page.subtitle, 0.5, 3.2, 7, 0.8, { size: 18, color: C.secondary });
    addText(slide, page.tagline || "", 0.5, 4.2, 7, 0.5, {
      size: 14, color: C.muted, italic: true,
    });
    // 右侧底图（如果有）
    const bg = path.join(ICONS_DIR, "china_map.png");
    if (fs.existsSync(bg)) {
      slide.addImage({ path: bg, x: 7.5, y: 0.8, w: 5.5, h: 5.5 });
    }
  },

  data_dashboard: (slide, page) => {
    slide.background = { color: C.white };
    addPageTitle(slide, page.title, page.subtitle);
    const cardW = 4.0, cardH = 1.7;
    page.data_cards.forEach((card, i) => {
      const x = 0.5 + (i % 3) * (cardW + 0.15);
      const y = 1.6 + Math.floor(i / 3) * (cardH + 0.15);
      addRect(slide, x, y, cardW, cardH, { fill: C.bg_alt });
      if (card.icon) addIcon(slide, card.icon, x + 0.30, y + 0.30, 0.35, 0.35);
      addText(slide, card.value, x + 0.25, y + 0.75, cardW - 0.5, 0.5, {
        size: 28, bold: true, color: C.primary, font: F.serif,
      });
      addText(slide, card.label, x + 0.25, y + 1.25, cardW - 0.5, 0.3, {
        size: 11, color: C.ink, bold: true,
      });
      addText(slide, card.time || "", x + 0.25, y + 1.45, cardW - 0.5, 0.2, {
        size: 9, color: C.muted, italic: true,
      });
    });
    if (page.callout) addCallout(slide, page.callout, 6.5);
  },

  // 其他 11 种 type 的实现留作 TODO 或参考 EY 项目
  // 完整实现见 references/slide-patterns.md
};

// 占位 handler（未知 type）
const fallback = (slide, page) => {
  slide.background = { color: C.white };
  addText(slide, `[${page.type}] ${page.title}`, 1, 3, 11, 1, {
    size: 20, color: C.primary, bold: true, align: "center",
  });
  addCallout(slide, page.callout || "TODO: add handler", 6.5);
};

// ============================================================
// 6. 主流程
// ============================================================
async function main() {
  const pptx = new pptxgen();
  pptx.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
  pptx.layout = "WIDE";
  pptx.author = "AI Agent";
  pptx.title = slidesData.deck_title;

  slidesData.slides.forEach((page) => {
    const slide = pptx.addSlide();
    slide.background = { color: C.white };
    const handler = handlers[page.type] || fallback;
    try {
      handler(slide, page);
      addFooter(slide, page, page.id);
    } catch (e) {
      console.error(`Error on slide ${page.id} (${page.type}):`, e.message);
    }
  });

  const outputPath = path.join(__dirname, slidesData.deck_title.replace(/[^\w]/g, "_") + "-editable.pptx");
  await pptx.writeFile({ fileName: outputPath });
  console.log(`✓ Generated: ${outputPath}`);
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});