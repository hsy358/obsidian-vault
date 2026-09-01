/**
 * 方案 C 精准对齐生成脚本
 * 原 PDF 渲染图作为底图 + OCR 提取的 native text 覆盖（精准对齐）
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const SLIDES_JSON = path.join(__dirname, "slides_ocr.json");
const slidesData = JSON.parse(fs.readFileSync(SLIDES_JSON, "utf-8"));
const PAGES_DIR = path.join(__dirname, slidesData.pages_dir);

async function main() {
  const pptx = new pptxgen();
  const ps = slidesData.page_size;
  pptx.defineLayout({ name: "WIDE", width: ps.width, height: ps.height });
  pptx.layout = "WIDE";
  pptx.author = "image-to-editable-ppt skill · 方案 C 精准对齐";
  pptx.title = slidesData.deck_title;

  for (const page of slidesData.slides) {
    const slide = pptx.addSlide();
    slide.background = { color: "FFFFFF" };

    // 1. 加底图（最底层）
    const bgPath = path.join(PAGES_DIR, page.background);
    if (fs.existsSync(bgPath)) {
      slide.addImage({ path: bgPath, x: 0, y: 0, w: ps.width, h: ps.height });
    }

    // 2. 加 OCR 提取的 native text 覆盖（在底图上层）
    for (const t of page.text_overlays || []) {
      slide.addText(t.text, {
        x: t.x, y: t.y, w: t.w, h: t.h,
        fontFace: "Calibri",
        fontSize: t.size || 12,
        color: t.color || "1B2D5C",
        align: "left",
        valign: "top",
        margin: 0.02,
      });
    }
  }

  const outputPath = path.join(__dirname, "ey-24p-v4-ocr.pptx");
  await pptx.writeFile({ fileName: outputPath });
  console.log(`✓ Generated: ${outputPath}`);
}

main().catch((e) => { console.error(e); process.exit(1); });