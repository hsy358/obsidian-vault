/**
 * image-to-editable-ppt skill · 方案 B（修复版）生成脚本
 * 原 PDF 渲染 PNG 作为底图
 * 不覆盖任何文字（避免错位）
 * 可编辑性通过 PowerPoint 用户的 native text 工具手动加文字框
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const SLIDES_JSON = path.join(__dirname, "slides.json");
const slidesData = JSON.parse(fs.readFileSync(SLIDES_JSON, "utf-8"));
const PAGES_DIR = path.join(__dirname, slidesData.pages_dir || "pages");

async function main() {
  const pptx = new pptxgen();
  const ps = slidesData.page_size || { width: 13.333, height: 7.5 };
  pptx.defineLayout({ name: "WIDE", width: ps.width, height: ps.height });
  pptx.layout = "WIDE";
  pptx.author = "image-to-editable-ppt skill · 方案 B";
  pptx.title = slidesData.deck_title;

  for (const page of slidesData.slides) {
    const slide = pptx.addSlide();
    slide.background = { color: "FFFFFF" };

    // 底图（覆盖整页）
    const bgPath = path.join(PAGES_DIR, page.background);
    if (fs.existsSync(bgPath)) {
      slide.addImage({
        path: bgPath,
        x: 0, y: 0,
        w: ps.width,
        h: ps.height,
      });
    } else {
      console.warn(`⚠️ p${page.id}: 底图 ${bgPath} 不存在`);
    }

    // 仅在底图外的安全位置加 native text（如编辑标记）
    if (page.id === 1) {
      // 封面：右下角加编辑标记
      slide.addText("[可编辑示例 · image-to-editable-ppt]", {
        x: 10, y: 7.1, w: 3.2, h: 0.3,
        fontFace: "Calibri",
        fontSize: 9,
        color: "888888",
        italic: true,
        align: "right",
      });
    } else {
      // 其他页：右下角加页码 native text（用户可改）
      slide.addText(String(page.id), {
        x: 12.5, y: 7.05, w: 0.6, h: 0.3,
        fontFace: "Calibri",
        fontSize: 10,
        color: "888888",
        align: "right",
      });
    }
  }

  const outputPath = path.join(__dirname, "ey-24p-v3-editable.pptx");
  await pptx.writeFile({ fileName: outputPath });
  console.log(`✓ Generated: ${outputPath}`);
}

main().catch((e) => { console.error(e); process.exit(1); });