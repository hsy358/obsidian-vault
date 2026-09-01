/**
 * 方案 C：前 4 页精准对齐生成（OCR 坐标 + v2 校对文字）
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const PROJECT_DIR = path.join("/root/vault", "1-Projects", "ey-24p-v4");
const slidesData = JSON.parse(fs.readFileSync(path.join(PROJECT_DIR, "slides_top4.json"), "utf-8"));
const PAGES_DIR = path.join(PROJECT_DIR, slidesData.pages_dir);

async function main() {
  const pptx = new pptxgen();
  const ps = slidesData.page_size;
  pptx.defineLayout({ name: "WIDE", width: ps.width, height: ps.height });
  pptx.layout = "WIDE";
  pptx.author = "image-to-editable-ppt skill · 方案 C 精准对齐（前 4 页）";
  pptx.title = slidesData.deck_title;

  for (const page of slidesData.slides) {
    const slide = pptx.addSlide();
    slide.background = { color: "FFFFFF" };

    // 1. 底图
    const bgPath = path.join(PAGES_DIR, page.background);
    if (fs.existsSync(bgPath)) {
      slide.addImage({ path: bgPath, x: 0, y: 0, w: ps.width, h: ps.height });
    }

    // 2. OCR 定位的 native text 覆盖
    for (const t of page.text_overlays || []) {
      slide.addText(t.text, {
        x: t.x, y: t.y, w: t.w, h: t.h,
        fontFace: t.font === "serif" ? "Georgia" : "Calibri",
        fontSize: t.size || 12,
        color: t.color || "1B2D5C",
        bold: t.bold ?? false,
        italic: t.italic ?? false,
        align: t.align || "left",
        valign: "middle",
        margin: 0.02,
      });
    }
  }

  const outputPath = path.join(PROJECT_DIR, "ey-24p-top4.pptx");
  await pptx.writeFile({ fileName: outputPath });
  console.log(`✓ Generated: ${outputPath}`);
}

main().catch((e) => { console.error(e); process.exit(1); });