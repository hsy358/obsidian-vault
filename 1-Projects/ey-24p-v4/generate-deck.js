/**
 * EY China AI Reality — 24P 复刻生成脚本
 * pptxgenjs 4.0.1
 * Usage: cd /root/.openclaw/workspace/tmp/ey-deck-gen && node generate-deck.js
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// ============================================================
// 1. 加载 slides.json
// ============================================================
const VAULT = "/root/vault";
const PROJECT_DIR = path.join(VAULT, "1-Projects", "ey-24p-v4");
const slidesData = JSON.parse(
  fs.readFileSync(
    path.join(PROJECT_DIR, "slides.json"),
    "utf-8"
  )
);

// ============================================================
// 2. 主题常量（EY 风格）
// ============================================================
const ICONS_DIR = path.join(VAULT, "1-Projects", "EY-China-AI-Reality", "PPT", "icons");
const PAGES_DIR = path.join(VAULT, "1-Projects", "ey-24p-v4", "pages_jpg");
const CHINA_MAP = path.join(ICONS_DIR, "china_map.png");

function addIcon(slide, name, x, y, w, h) {
  const fp = path.join(ICONS_DIR, name + ".png");
  if (fs.existsSync(fp)) {
    slide.addImage({ path: fp, x, y, w, h });
  }
}

function addBackground(slide, pageNum) {
  const jpgPath = path.join(PAGES_DIR, `p${String(pageNum).padStart(2, "0")}.jpg`);
  if (fs.existsSync(jpgPath)) {
    slide.addImage({ path: jpgPath, x: 0, y: 0, w: 13.333, h: 7.5 });
  }
}

const C = {
  primary: "1B2D5C",     // EY 深海军蓝
  secondary: "00A3B4",   // EY teal 青色
  accent: "1E5BA8",      // 亮蓝
  ink: "10254D",         // 标题用深蓝
  muted: "4A5A78",       // 次要文字
  white: "FFFFFF",
  black: "000000",
  bg_subtle: "F9FCFF",
  bg_alt: "FBFDFF",
  light_blue: "E8F0F8",
  border_gray: "D1D5DB",
  success: "0B8B52",
  warning: "F26B16",
};

const F = {
  serif: "Georgia",
  body: "Calibri",
  zh: "Microsoft YaHei",
};

// ============================================================
// 3. 通用 helper
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
    fit: opt.fit || "shrink",
  });
}

function addRect(slide, x, y, w, h, opt = {}) {
  slide.addShape("roundRect", {
    x, y, w, h,
    rectRadius: opt.radius ?? 0.05,
    fill: { color: opt.fill || C.white, transparency: opt.transparency || 0 },
    line: { color: opt.line || C.light_blue, width: opt.lineWidth || 0.75 },
  });
}

function addCircle(slide, x, y, w, h, opt = {}) {
  slide.addShape("ellipse", {
    x, y, w, h,
    fill: { color: opt.fill || C.white, transparency: opt.transparency || 0 },
    line: { color: opt.line || C.primary, width: opt.lineWidth || 1 },
  });
}

function addArrow(slide, x1, y1, x2, y2, color = C.primary, width = 1.5) {
  // 简化：用矩形+三角形组合做箭头（pptxgenjs 内置 line 类型有限）
  // 这里用连接线 + 终点三角形近似
  slide.addShape("line", {
    x: x1, y: y1, w: x2 - x1, h: y2 - y1,
    line: { color, width, endArrowType: "triangle" },
  });
}

function addFooter(slide, page, num) {
  // 左下角：地球图标 + footer text
  addText(slide, "⊙", 0.3, 7.05, 0.25, 0.3, { size: 9, color: C.muted });
  addText(slide, page.footer.left, 0.55, 7.05, 10, 0.3, { size: 8, color: C.muted });
  // 右下角：页码
  addText(slide, String(num), 12.5, 7.05, 0.6, 0.3, { size: 10, color: C.primary, bold: true, align: "right" });
}

function addPageTitle(slide, title, subtitle, color = C.primary) {
  // 顶部标题区
  addText(slide, title, 0.5, 0.25, 12.3, 0.6, {
    size: 22, bold: true, color, font: F.serif, valign: "middle",
  });
  if (subtitle) {
    addText(slide, subtitle, 0.5, 0.85, 12.3, 0.35, {
      size: 12, color: C.secondary, font: F.body, italic: true,
    });
    // 短装饰线
    addRect(slide, 0.5, 1.22, 1.5, 0.03, { radius: 0.01, fill: C.secondary, line: C.secondary, lineWidth: 0 });
  }
}

function addCallout(slide, text, y = 6.5, icon = "⊕") {
  // 底部金句条
  addRect(slide, 0.5, y, 12.3, 0.5, {
    radius: 0.06, fill: C.bg_subtle, line: C.secondary, lineWidth: 0.5,
  });
  addText(slide, icon, 0.6, y + 0.05, 0.4, 0.4, { size: 14, align: "center" });
  addText(slide, text, 1.1, y, 11.5, 0.5, {
    size: 11, color: C.primary, bold: true, valign: "middle", align: "left",
  });
}

// ============================================================
// 4. 各页类型函数
// ============================================================

function addCoverSlide(slide, page) {
  slide.background = { color: C.white };
  
  // 左侧文字区
  addText(slide, page.eyebrow, 0.5, 1.2, 6, 0.3, {
    size: 11, color: C.muted, italic: true,
  });
  addText(slide, page.title, 0.5, 1.7, 6.5, 1.2, {
    size: 44, bold: true, color: C.primary, font: F.serif,
  });
  addRect(slide, 0.5, 3.0, 1.0, 0.05, { radius: 0.02, fill: C.primary, line: C.primary, lineWidth: 0 });
  addText(slide, page.subtitle, 0.5, 3.2, 7, 0.8, {
    size: 18, color: C.secondary, font: F.body,
  });
  addText(slide, page.tagline, 0.5, 4.2, 7, 0.5, {
    size: 14, color: C.muted, italic: true,
  });
  
  // 右侧：中国地图节点网络图（用散点近似）
  for (let i = 0; i < 50; i++) {
    const cx = 8 + Math.random() * 4.5;
    const cy = 1 + Math.random() * 4.5;
    const r = 0.05 + Math.random() * 0.08;
    addCircle(slide, cx, cy, r, r, {
      fill: C.primary, transparency: 30, line: C.primary, lineWidth: 0,
    });
  }
  // 简化上海天际线（矩形+椭圆轮廓）
  addRect(slide, 10.5, 3.5, 0.6, 1.5, {
    radius: 0.05, fill: C.white, transparency: 50, line: C.primary, lineWidth: 1,
  });
  addCircle(slide, 10.7, 3.3, 0.2, 0.2, {
    fill: C.white, transparency: 50, line: C.primary, lineWidth: 1,
  });
  
  // 底部 5 步流程图
  const stepNames = page.decorative.footer_5step;
  const stepW = 2.4;
  const startX = 0.5;
  stepNames.forEach((name, i) => {
    const x = startX + i * (stepW + 0.05);
    const isAccent = i >= 3; // 后两步是青色（未来/中国特色）
    addCircle(slide, x + stepW / 2 - 0.3, 6.3, 0.6, 0.6, {
      fill: isAccent ? C.secondary : C.primary, line: C.white, lineWidth: 1.5,
    });
    addText(slide, String(i + 1), x + stepW / 2 - 0.3, 6.3, 0.6, 0.6, {
      size: 18, bold: true, color: C.white, align: "center", valign: "middle",
    });
    addText(slide, name, x, 6.95, stepW, 0.3, {
      size: 10, color: C.primary, bold: true, align: "center",
    });
  });
}

function addAgendaSlide(slide, page) {
  slide.background = { color: C.white };
  addText(slide, page.title, 0.5, 0.4, 12, 0.8, {
    size: 32, bold: true, color: C.primary, font: F.serif,
  });
  addRect(slide, 0.5, 1.2, 1.0, 0.04, { radius: 0.02, fill: C.primary, line: C.primary, lineWidth: 0 });
  addText(slide, page.subtitle, 0.5, 1.35, 12, 0.5, {
    size: 14, color: C.secondary, italic: true,
  });
  
  // 4 个 Part 卡片
  const colW = 6.0;
  page.parts.forEach((part, i) => {
    const x = 0.5 + (i % 2) * (colW + 0.3);
    const y = 2.2 + Math.floor(i / 2) * 2.2;
    addRect(slide, x, y, colW, 1.9, {
      radius: 0.08, fill: C.bg_subtle, line: C.light_blue, lineWidth: 1,
    });
    addCircle(slide, x + 0.3, y + 0.3, 0.7, 0.7, {
      fill: C.primary, line: C.white, lineWidth: 2,
    });
    addText(slide, String(part.num), x + 0.3, y + 0.3, 0.7, 0.7, {
      size: 22, bold: true, color: C.white, align: "center", valign: "middle",
    });
    addText(slide, part.title, x + 1.2, y + 0.4, colW - 1.5, 0.6, {
      size: 16, bold: true, color: C.primary, font: F.serif,
    });
    addText(slide, part.desc, x + 1.2, y + 1.0, colW - 1.5, 0.8, {
      size: 11, color: C.muted,
    });
  });
  
  addFooter(slide, page, page.id);
}

function addSectionDividerSlide(slide, page) {
  slide.background = { color: C.white };
  // PART 标识
  addText(slide, page.part_label, 0.5, 1.5, 4, 0.4, {
    size: 13, color: C.muted, bold: true, charSpacing: 5,
  });
  // 短装饰线
  addRect(slide, 0.5, 1.95, 1.0, 0.04, { radius: 0.02, fill: C.secondary, line: C.secondary, lineWidth: 0 });
  // 主标题
  addText(slide, page.title, 0.5, 2.2, 7.5, 1.5, {
    size: 36, bold: true, color: C.primary, font: F.serif,
  });
  // 副标题
  addText(slide, page.subtitle, 0.5, 3.8, 7.5, 0.8, {
    size: 16, color: C.secondary, font: F.body,
  });
  // Callout 信息框
  addRect(slide, 0.5, 5.0, 7.5, 0.7, {
    radius: 0.08, fill: C.bg_subtle, line: C.secondary, lineWidth: 0.75,
  });
  addText(slide, "⊕", 0.6, 5.05, 0.6, 0.6, { size: 16, align: "center" });
  addText(slide, page.callout, 1.2, 5.0, 6.7, 0.7, {
    size: 11, color: C.primary, bold: true, valign: "middle",
  });
  // 右侧装饰：建筑/流动曲线（简化为多线）
  for (let i = 0; i < 8; i++) {
    const cx = 8.5 + i * 0.5;
    const cy = 3.5;
    addArrow(slide, cx, cy, cx + 0.4, cy + (i % 2 === 0 ? -0.5 : 0.5), C.secondary, 1.5);
  }
  // 装饰建筑
  addRect(slide, 11.5, 2.5, 0.6, 2.0, { fill: C.white, transparency: 0, line: C.primary, lineWidth: 1.2 });
  addRect(slide, 12.2, 2.0, 0.6, 2.5, { fill: C.white, transparency: 0, line: C.primary, lineWidth: 1.2 });
  addCircle(slide, 12.35, 1.7, 0.3, 0.3, { fill: C.white, line: C.primary, lineWidth: 1.2 });
  
  addFooter(slide, page, page.id);
}

function addDataDashboardSlide(slide, page) {
  slide.background = { color: C.white };
  addPageTitle(slide, page.title, page.subtitle);
  
  // 6 张数据卡片（2x3）
  const cardW = 4.0;
  const cardH = 1.7;
  const gapX = 0.15;
  const gapY = 0.15;
  const startX = 0.5;
  const startY = 1.6;
  
  page.data_cards.forEach((card, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = startX + col * (cardW + gapX);
    const y = startY + row * (cardH + gapY);
    
    addRect(slide, x, y, cardW, cardH, {
      radius: 0.06, fill: C.bg_alt, line: C.light_blue, lineWidth: 0.75,
    });
    // icon 圆圈 + PNG 图标
    addCircle(slide, x + 0.25, y + 0.25, 0.45, 0.45, {
      fill: C.bg_subtle, line: C.secondary, lineWidth: 1,
    });
    const iconMap = { users: "users", gauge: "gauge", network: "network", buildings: "buildings", robot_arm: "robot_arm", download: "download" };
    const iconFile = iconMap[card.icon];
    if (iconFile && fs.existsSync(path.join(ICONS_DIR, iconFile + ".png"))) {
      addIcon(slide, iconFile, x + 0.30, y + 0.30, 0.35, 0.35);
    } else {
      addText(slide, "▲", x + 0.25, y + 0.25, 0.45, 0.45, {
        size: 14, color: C.secondary, bold: true, align: "center", valign: "middle",
      });
    }
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
  
  // 底部 callouts（两条）
  const cy = 5.4;
  page.callouts.forEach((cb, i) => {
    const x = 0.5 + i * 6.2;
    addRect(slide, x, cy, 6.0, 0.7, {
      radius: 0.06, fill: C.bg_subtle, line: C.secondary, lineWidth: 0.5,
    });
    addText(slide, "⭐", x + 0.15, cy + 0.05, 0.4, 0.6, {
      size: 16, align: "center", valign: "middle",
    });
    addText(slide, cb.text, x + 0.6, cy, 5.3, 0.7, {
      size: 11, color: C.primary, bold: true, valign: "middle",
    });
  });
  
  addFooter(slide, page, page.id);
}

function addTimelineSlide(slide, page) {
  slide.background = { color: C.white };
  addPageTitle(slide, page.title, page.subtitle);
  
  // 时间轴主箭头（用粗线近似）
  addArrow(slide, 0.5, 4.0, 12.8, 4.0, C.primary, 4);
  
  // 4 个里程碑
  const milestoneW = 2.8;
  const gap = 0.25;
  page.milestones.forEach((m, i) => {
    const x = 0.5 + i * (milestoneW + gap);
    // 节点圆 + PNG 图标
    addCircle(slide, x + milestoneW / 2 - 0.4, 3.6, 0.8, 0.8, {
      fill: C.bg_subtle, line: C.secondary, lineWidth: 2,
    });
    const iconMap = { doc: "doc", people: "people", factory: "factory", rising_bars: "rising_bars" };
    const iconFile = iconMap[m.icon];
    if (iconFile && fs.existsSync(path.join(ICONS_DIR, iconFile + ".png"))) {
      addIcon(slide, iconFile, x + milestoneW / 2 - 0.30, 3.70, 0.60, 0.60);
    } else {
      addText(slide, String(i + 1), x + milestoneW / 2 - 0.4, 3.6, 0.8, 0.8, {
        size: 24, bold: true, color: C.secondary, align: "center", valign: "middle",
      });
    }
    // 时间
    addText(slide, m.time, x, 2.2, milestoneW, 0.4, {
      size: 13, bold: true, color: C.primary, align: "center",
    });
    // 大数字
    addText(slide, m.value, x, 4.7, milestoneW, 0.6, {
      size: 32, bold: true, color: C.primary, font: F.serif, align: "center",
    });
    // 标签
    addText(slide, m.label, x, 5.4, milestoneW, 0.4, {
      size: 11, color: C.ink, bold: true, align: "center",
    });
    // 副
    addText(slide, m.sub, x, 5.75, milestoneW, 0.4, {
      size: 9, color: C.muted, align: "center",
    });
  });
  
  addCallout(slide, page.callout, 6.4, "★");
  addFooter(slide, page, page.id);
}

function addLoopSlide(slide, page) {
  slide.background = { color: C.white };
  addPageTitle(slide, page.title, page.subtitle);
  
  // 左：3 行数据
  page.left_data.forEach((d, i) => {
    const y = 1.7 + i * 1.5;
    addText(slide, d.value, 0.5, y, 3.5, 0.7, {
      size: 28, bold: true, color: C.primary, font: F.serif,
    });
    addText(slide, d.label, 0.5, y + 0.7, 3.5, 0.7, {
      size: 10, color: C.muted,
    });
  });
  
  // 中：5 节点循环（圆形排布）
  const cx = 6.7;
  const cy = 4.0;
  const r = 1.3;
  const stepNames = page.center_loop_5steps;
  stepNames.forEach((name, i) => {
    const angle = (i * 2 * Math.PI) / 5 - Math.PI / 2;
    const x = cx + r * Math.cos(angle) - 0.5;
    const y = cy + r * Math.sin(angle) - 0.4;
    addCircle(slide, x, y, 1.0, 0.8, {
      fill: C.white, line: C.secondary, lineWidth: 1.5,
    });
    addText(slide, String(i + 1), x, y, 1.0, 0.3, {
      size: 11, bold: true, color: C.secondary, align: "center", valign: "middle",
    });
    addText(slide, name, x, y + 0.25, 1.0, 0.55, {
      size: 8, color: C.primary, align: "center", valign: "middle", bold: true,
    });
    // 连接箭头（简化：用直线）
    if (i < stepNames.length - 1) {
      const nextAngle = ((i + 1) * 2 * Math.PI) / 5 - Math.PI / 2;
      const nx1 = cx + r * Math.cos(angle) + 0.3 * Math.cos(angle);
      const ny1 = cy + r * Math.sin(angle) + 0.3 * Math.sin(angle);
      const nx2 = cx + r * Math.cos(nextAngle) - 0.3 * Math.cos(nextAngle);
      const ny2 = cy + r * Math.sin(nextAngle) - 0.3 * Math.sin(nextAngle);
      addArrow(slide, nx1, ny1, nx2, ny2, C.secondary, 1.2);
    }
  });
  
  // 右：3 个速度含义
  page.right_definition.items.forEach((item, i) => {
    const y = 1.7 + i * 1.5;
    addCircle(slide, 9.7, y, 0.5, 0.5, {
      fill: C.secondary, line: C.secondary, lineWidth: 0,
    });
    addText(slide, item.text, 10.3, y, 2.8, 0.5, {
      size: 11, color: C.primary, bold: true, valign: "middle",
    });
  });
  addText(slide, page.right_definition.title, 9.5, 1.3, 3.5, 0.4, {
    size: 13, bold: true, color: C.primary, font: F.serif,
  });
  
  addCallout(slide, page.callout, 6.4, "⊕");
  addFooter(slide, page, page.id);
}

function addHubAndSpokeSlide(slide, page) {
  slide.background = { color: C.white };
  addPageTitle(slide, page.title, page.subtitle);
  
  // 左：消费层
  page.left_consumer.forEach((d, i) => {
    const y = 1.7 + i * 1.4;
    addText(slide, d.value, 0.5, y, 2.5, 0.5, {
      size: 20, bold: true, color: C.primary, font: F.serif,
    });
    addText(slide, d.label, 0.5, y + 0.5, 2.5, 0.4, {
      size: 9, color: C.muted,
    });
  });
  
  // 中：放射图（中心 + 8 个 spoke）
  const cx = 6.7;
  const cy = 4.0;
  const centerSize = 1.5;
  // 中心 hub
  addCircle(slide, cx - centerSize / 2, cy - centerSize / 2, centerSize, centerSize, {
    fill: C.primary, line: C.primary, lineWidth: 0,
  });
  addText(slide, page.center_hub, cx - centerSize / 2, cy - centerSize / 2, centerSize, centerSize, {
    size: 11, bold: true, color: C.white, align: "center", valign: "middle",
  });
  // 8 个 spoke
  const r = 1.7;
  page.spokes_8_scenarios.forEach((name, i) => {
    const angle = (i * 2 * Math.PI) / 8 - Math.PI / 2;
    const x = cx + r * Math.cos(angle) - 0.6;
    const y = cy + r * Math.sin(angle) - 0.25;
    addRect(slide, x, y, 1.2, 0.5, {
      radius: 0.06, fill: C.bg_subtle, line: C.secondary, lineWidth: 1,
    });
    addText(slide, name, x, y, 1.2, 0.5, {
      size: 9, color: C.primary, bold: true, align: "center", valign: "middle",
    });
    // 连接线
    addArrow(slide, cx, cy, x + 0.6, y + 0.25, C.secondary, 0.75);
  });
  
  // 右：产业层
  page.right_industrial.forEach((d, i) => {
    const y = 1.7 + i * 1.4;
    addText(slide, d.value, 9.7, y, 2.5, 0.5, {
      size: 20, bold: true, color: C.primary, font: F.serif,
    });
    addText(slide, d.label, 9.7, y + 0.5, 3.2, 0.4, {
      size: 9, color: C.muted,
    });
  });
  
  addCallout(slide, page.callout, 6.4, "⊕");
  addFooter(slide, page, page.id);
}

function addFlow5StepSlide(slide, page) {
  slide.background = { color: C.white };
  addPageTitle(slide, page.title, page.subtitle);
  
  // 左：3 个 KPI（圆形+大数字）
  page.left_kpis.forEach((d, i) => {
    const y = 1.7 + i * 1.5;
    addCircle(slide, 0.5, y, 1.2, 1.2, {
      fill: C.bg_subtle, line: C.primary, lineWidth: 1.5,
    });
    addText(slide, d.value, 1.7, y + 0.1, 2.5, 0.7, {
      size: 22, bold: true, color: C.primary, font: F.serif,
    });
    addText(slide, d.label, 1.7, y + 0.8, 2.5, 0.5, {
      size: 9, color: C.muted,
    });
  });
  
  // 中：5 步流程（水平）
  const flow = page.center_flow_5steps;
  const stepW = 0.95;
  const flowX = 4.8;
  flow.forEach((name, i) => {
    const x = flowX + i * (stepW + 0.15);
    addRect(slide, x, 3.5, stepW, 1.0, {
      radius: 0.06, fill: C.bg_alt, line: C.secondary, lineWidth: 1,
    });
    addText(slide, String(i + 1), x, 3.55, stepW, 0.3, {
      size: 14, bold: true, color: C.secondary, align: "center",
    });
    addText(slide, name, x, 3.85, stepW, 0.6, {
      size: 8, color: C.primary, bold: true, align: "center", valign: "middle",
    });
    if (i < flow.length - 1) {
      addArrow(slide, x + stepW + 0.02, 4.0, x + stepW + 0.13, 4.0, C.secondary, 1.5);
    }
  });
  // 3 个 tag
  page.tags_below_flow.forEach((tag, i) => {
    const x = 4.8 + i * 2.7;
    addRect(slide, x, 4.7, 2.5, 0.4, {
      radius: 0.04, fill: C.secondary, line: C.secondary, lineWidth: 0,
    });
    addText(slide, tag, x, 4.7, 2.5, 0.4, {
      size: 10, color: C.white, bold: true, align: "center", valign: "middle",
    });
  });
  
  // 右：4 个业务影响
  page.right_business_impact.forEach((item, i) => {
    const y = 1.7 + i * 1.0;
    addRect(slide, 11.5, y, 1.6, 0.8, {
      radius: 0.06, fill: C.bg_subtle, line: C.secondary, lineWidth: 0.75,
    });
    addText(slide, item.text, 11.5, y, 1.6, 0.8, {
      size: 9, color: C.primary, bold: true, align: "center", valign: "middle",
    });
  });
  
  // Examples pills
  addText(slide, "Examples:", 4.8, 5.5, 1.5, 0.3, {
    size: 10, color: C.muted, italic: true,
  });
  page.examples_pills.forEach((pill, i) => {
    const x = 5.7 + i * 1.7;
    addRect(slide, x, 5.5, 1.5, 0.35, {
      radius: 0.04, fill: C.bg_alt, line: C.primary, lineWidth: 0.5,
    });
    addText(slide, pill, x, 5.5, 1.5, 0.35, {
      size: 9, color: C.primary, bold: true, align: "center", valign: "middle",
    });
  });
  
  addCallout(slide, page.callout, 6.0, "⊕");
  addFooter(slide, page, page.id);
}

function add3ColFrameworkSlide(slide, page) {
  slide.background = { color: C.white };
  addPageTitle(slide, page.title, page.subtitle);
  
  // 左：2 个环形数据
  addText(slide, page.left_snapshot.title, 0.5, 1.7, 3.8, 0.4, {
    size: 13, bold: true, color: C.primary, font: F.serif,
  });
  page.left_snapshot.items.forEach((item, i) => {
    const y = 2.3 + i * 2.0;
    addCircle(slide, 0.6, y, 1.2, 1.2, {
      fill: C.bg_subtle, line: C.secondary, lineWidth: 2.5,
    });
    addText(slide, item.ring, 0.6, y + 0.05, 1.2, 0.7, {
      size: 18, bold: true, color: C.secondary, align: "center", valign: "middle",
    });
    addText(slide, item.label, 2.0, y, 2.3, 1.2, {
      size: 9, color: C.muted, valign: "middle",
    });
  });
  
  // 中：5 阶段成熟度
  addText(slide, page.center_5stage_maturity.title, 4.8, 1.7, 3.8, 0.4, {
    size: 13, bold: true, color: C.primary, font: F.serif,
  });
  const stages = page.center_5stage_maturity.stages;
  const stageW = 0.7;
  stages.forEach((s, i) => {
    const x = 4.8 + i * (stageW + 0.1);
    addRect(slide, x, 2.4, stageW, 0.7, {
      radius: 0.05, fill: C.bg_alt, line: C.secondary, lineWidth: 1,
    });
    addText(slide, s, x, 2.4, stageW, 0.7, {
      size: 8, color: C.primary, bold: true, align: "center", valign: "middle",
    });
  });
  // 3 个底部 band
  page.center_5stage_maturity.bottom_bands.forEach((band, i) => {
    const x = 4.8 + i * 1.3;
    addRect(slide, x, 3.3, 1.2, 0.4, {
      radius: 0.04, fill: C.light_blue, line: C.primary, lineWidth: 0.5,
    });
    addText(slide, band, x, 3.3, 1.2, 0.4, {
      size: 8, color: C.primary, bold: true, align: "center", valign: "middle",
    });
  });
  // frontier marker
  addText(slide, "→ The frontier", 7.5, 3.3, 2.0, 0.4, {
    size: 10, color: C.secondary, italic: true, bold: true,
  });
  
  // 右：5 个特性 + 4 个应用领域
  addText(slide, page.right_what_changes.title, 9.5, 1.7, 3.5, 0.4, {
    size: 13, bold: true, color: C.primary, font: F.serif,
  });
  page.right_what_changes.items.forEach((item, i) => {
    const y = 2.3 + i * 0.7;
    addCircle(slide, 9.5, y, 0.3, 0.3, {
      fill: C.secondary, line: C.secondary, lineWidth: 0,
    });
    addText(slide, item.text, 9.9, y, 3.0, 0.3, {
      size: 10, color: C.primary, valign: "middle",
    });
  });
  // 应用领域标签
  const appY = 6.0;
  addText(slide, "Apps:", 9.5, appY, 0.7, 0.3, {
    size: 9, color: C.muted, italic: true,
  });
  page.right_what_changes.app_areas.forEach((area, i) => {
    const x = 10.2 + i * 0.85;
    addRect(slide, x, appY, 0.8, 0.3, {
      radius: 0.03, fill: C.bg_subtle, line: C.primary, lineWidth: 0.5,
    });
    addText(slide, area, x, appY, 0.8, 0.3, {
      size: 8, color: C.primary, bold: true, align: "center", valign: "middle",
    });
  });
  
  addCallout(slide, page.callout, 6.4, "◐");
  addFooter(slide, page, page.id);
}

function add3ColCompositeSlide(slide, page) {
  slide.background = { color: C.white };
  addPageTitle(slide, page.title, page.subtitle);
  
  // 左：Industrial signals
  addText(slide, page.left_industrial_signals.title, 0.5, 1.6, 3.0, 0.4, {
    size: 12, bold: true, color: C.primary,
  });
  page.left_industrial_signals.items.forEach((d, i) => {
    const y = 2.1 + i * 1.0;
    addText(slide, d.value, 0.5, y, 1.5, 0.5, {
      size: 20, bold: true, color: C.primary, font: F.serif,
    });
    addText(slide, d.label, 2.1, y, 2.0, 0.5, {
      size: 8, color: C.muted, valign: "middle",
    });
  });
  addText(slide, page.left_industrial_signals.source, 0.5, 6.3, 3.0, 0.3, {
    size: 8, color: C.muted, italic: true,
  });
  
  // 中：Physical AI 中心 + 5 节点放射
  addText(slide, page.center_physical_ai_hub.title, 4.6, 1.6, 3.8, 0.4, {
    size: 12, bold: true, color: C.primary,
  });
  const cx = 6.5;
  const cy = 4.0;
  // 中心
  addCircle(slide, cx - 0.7, cy - 0.7, 1.4, 1.4, {
    fill: C.primary, line: C.primary, lineWidth: 0,
  });
  addText(slide, page.center_physical_ai_hub.center, cx - 0.7, cy - 0.7, 1.4, 1.4, {
    size: 12, bold: true, color: C.white, align: "center", valign: "middle",
  });
  // 5 spoke
  const r = 1.5;
  page.center_physical_ai_hub.spokes_5.forEach((s, i) => {
    const angle = (i * 2 * Math.PI) / 5 - Math.PI / 2;
    const x = cx + r * Math.cos(angle) - 0.4;
    const y = cy + r * Math.sin(angle) - 0.25;
    addRect(slide, x, y, 0.8, 0.5, {
      radius: 0.04, fill: C.bg_subtle, line: C.secondary, lineWidth: 1,
    });
    addText(slide, s.text, x, y, 0.8, 0.5, {
      size: 8, color: C.primary, bold: true, align: "center", valign: "middle",
    });
    addArrow(slide, cx, cy, x + 0.4, y + 0.25, C.secondary, 0.75);
  });
  // bottom loop
  const loop = page.center_physical_ai_hub.bottom_loop;
  const loopW = 0.7;
  loop.forEach((step, i) => {
    const x = 4.6 + i * (loopW + 0.1);
    addRect(slide, x, 5.7, loopW, 0.4, {
      radius: 0.03, fill: C.secondary, line: C.secondary, lineWidth: 0,
    });
    addText(slide, step, x, 5.7, loopW, 0.4, {
      size: 7, color: C.white, bold: true, align: "center", valign: "middle",
    });
    if (i < loop.length - 1) {
      addArrow(slide, x + loopW + 0.01, 5.9, x + loopW + 0.09, 5.9, C.secondary, 1.2);
    }
  });
  // tags
  page.center_physical_ai_hub.tags.forEach((tag, i) => {
    const x = 4.6 + i * 1.0;
    addText(slide, tag, x, 6.2, 0.95, 0.3, {
      size: 7, color: C.muted, italic: true, align: "center",
    });
  });
  
  // 右：Why it matters
  addText(slide, page.right_why_it_matters.title, 9.5, 1.6, 3.5, 0.4, {
    size: 12, bold: true, color: C.primary,
  });
  page.right_why_it_matters.items.forEach((it, i) => {
    const y = 2.1 + i * 0.55;
    addText(slide, "• " + it, 9.5, y, 3.5, 0.5, {
      size: 9, color: C.ink,
    });
  });
  // highlight box
  addRect(slide, 9.5, 5.0, 3.5, 1.2, {
    radius: 0.06, fill: C.primary, line: C.primary, lineWidth: 0,
  });
  addText(slide, page.right_why_it_matters.highlight_box, 9.6, 5.05, 3.3, 1.1, {
    size: 10, color: C.white, bold: true, valign: "middle",
  });
  
  addCallout(slide, page.callout, 6.6, "◐");
  addFooter(slide, page, page.id);
}

function addFramework5StageSlide(slide, page) {
  slide.background = { color: C.white };
  addPageTitle(slide, page.title, page.subtitle);
  
  // 5 阶段卡片
  const stageW = 2.3;
  const startX = 0.5;
  const startY = 1.7;
  page.stages_5.forEach((s, i) => {
    const x = startX + i * (stageW + 0.15);
    addRect(slide, x, startY, stageW, 2.5, {
      radius: 0.08, fill: C.bg_alt, line: C.secondary, lineWidth: 1,
    });
    addCircle(slide, x + 0.3, startY + 0.2, 0.5, 0.5, {
      fill: C.primary, line: C.white, lineWidth: 1.5,
    });
    addText(slide, String(s.num), x + 0.3, startY + 0.2, 0.5, 0.5, {
      size: 16, bold: true, color: C.white, align: "center", valign: "middle",
    });
    addText(slide, s.name, x + 0.2, startY + 0.85, stageW - 0.4, 0.5, {
      size: 12, bold: true, color: C.primary, align: "center",
    });
    addText(slide, s.desc, x + 0.2, startY + 1.4, stageW - 0.4, 1.0, {
      size: 9, color: C.muted, align: "center", valign: "top",
    });
  });
  
  // 左：What changes
  addText(slide, page.left_what_changes.title, 0.5, 4.6, 6.0, 0.4, {
    size: 13, bold: true, color: C.primary, font: F.serif,
  });
  page.left_what_changes.items.forEach((it, i) => {
    const y = 5.0 + i * 0.35;
    addText(slide, "→ " + it, 0.5, y, 6.0, 0.3, {
      size: 11, color: C.ink,
    });
  });
  
  // 右：Why it matters
  addText(slide, page.right_why_it_matters.title, 7.0, 4.6, 6.0, 0.4, {
    size: 13, bold: true, color: C.primary, font: F.serif,
  });
  page.right_why_it_matters.items.forEach((it, i) => {
    const y = 5.0 + i * 0.35;
    addText(slide, "• " + it, 7.0, y, 6.0, 0.3, {
      size: 11, color: C.ink,
    });
  });
  
  addCallout(slide, page.callout, 6.5, "⊕");
  addFooter(slide, page, page.id);
}

function addCoreFoundationSlide(slide, page) {
  slide.background = { color: C.white };
  addPageTitle(slide, page.title, page.subtitle);
  
  // 左：Model layer（5 个）+ Context（12 个资产）
  addRect(slide, 0.5, 1.7, 3.5, 1.3, {
    radius: 0.06, fill: C.bg_subtle, line: C.secondary, lineWidth: 1,
  });
  addText(slide, "Model Layer", 0.6, 1.8, 3.3, 0.3, {
    size: 11, bold: true, color: C.primary,
  });
  page.model_layer_5.forEach((m, i) => {
    const x = 0.6 + (i % 3) * 1.1;
    const y = 2.2 + Math.floor(i / 3) * 0.4;
    addText(slide, m, x, y, 1.0, 0.3, {
      size: 9, color: C.ink, valign: "middle",
    });
  });
  
  // Context 12 资产（2 列 6 行）
  addRect(slide, 0.5, 3.1, 3.5, 2.6, {
    radius: 0.06, fill: C.bg_alt, line: C.primary, lineWidth: 1,
  });
  addText(slide, "Enterprise Context (12 assets)", 0.6, 3.2, 3.3, 0.3, {
    size: 11, bold: true, color: C.primary,
  });
  page.context_12_assets.forEach((a, i) => {
    const x = 0.6 + (i % 2) * 1.7;
    const y = 3.55 + Math.floor(i / 2) * 0.35;
    addText(slide, "• " + a, x, y, 1.6, 0.3, {
      size: 8, color: C.ink, valign: "middle",
    });
  });
  
  // 右：3 段箭头链
  page.right_arrow_chain.forEach((s, i) => {
    const y = 1.7 + i * 1.4;
    addRect(slide, 4.5, y, 3.0, 1.2, {
      radius: 0.06, fill: C.bg_alt, line: C.secondary, lineWidth: 1,
    });
    addText(slide, s.stage, 4.6, y + 0.1, 2.8, 0.4, {
      size: 12, bold: true, color: C.primary, font: F.serif,
    });
    s.items.forEach((it, j) => {
      addText(slide, "• " + it, 4.7, y + 0.5 + j * 0.13, 2.7, 0.2, {
        size: 8, color: C.muted,
      });
    });
    if (i < 2) {
      addArrow(slide, 6.0, y + 1.2, 6.0, y + 1.4, C.secondary, 2);
    }
  });
  
  // 最右：Business Value 卡片
  addRect(slide, 8.0, 1.7, 5.0, 4.2, {
    radius: 0.06, fill: C.primary, line: C.primary, lineWidth: 0,
  });
  addText(slide, "Business Value", 8.2, 1.8, 4.7, 0.4, {
    size: 14, bold: true, color: C.white, font: F.serif,
  });
  addText(slide, "↑ From Execution", 8.2, 2.2, 4.7, 0.3, {
    size: 9, color: C.white, italic: true,
  });
  page.right_arrow_chain[2].items.forEach((it, i) => {
    addText(slide, "✓ " + it, 8.2, 2.7 + i * 0.5, 4.5, 0.4, {
      size: 11, color: C.white,
    });
  });
  
  // 底部 5 步流程
  const flow = page.bottom_flow_5step;
  const flowW = 1.8;
  flow.forEach((s, i) => {
    const x = 0.5 + i * (flowW + 0.4);
    addRect(slide, x, 6.0, flowW, 0.5, {
      radius: 0.04, fill: C.secondary, line: C.secondary, lineWidth: 0,
    });
    addText(slide, s, x, 6.0, flowW, 0.5, {
      size: 10, color: C.white, bold: true, align: "center", valign: "middle",
    });
    if (i < flow.length - 1) {
      addArrow(slide, x + flowW + 0.1, 6.25, x + flowW + 0.35, 6.25, C.secondary, 2);
    }
  });
  
  addCallout(slide, page.callout, 6.6, "⊕");
  addFooter(slide, page, page.id);
}

function addCaseStudy3ColSlide(slide, page, opts = {}) {
  slide.background = { color: C.white };
  addPageTitle(slide, page.title, page.subtitle);
  
  // 左：传统流程（标题栏 + 节点）
  const leftTitle = opts.leftTitle || "Traditional";
  const leftSteps = opts.leftSteps;
  const middleSteps = opts.middleSteps;
  
  addRect(slide, 0.5, 1.7, 2.8, 0.4, {
    radius: 0.04, fill: C.primary, line: C.primary, lineWidth: 0,
  });
  addText(slide, leftTitle, 0.5, 1.7, 2.8, 0.4, {
    size: 11, bold: true, color: C.white, align: "center", valign: "middle",
  });
  leftSteps.forEach((s, i) => {
    const y = 2.2 + i * 0.5;
    addRect(slide, 0.5, y, 2.8, 0.4, {
      radius: 0.03, fill: C.bg_alt, line: C.primary, lineWidth: 0.5,
    });
    addText(slide, s, 0.55, y, 2.7, 0.4, {
      size: 8, color: C.ink, valign: "middle",
    });
  });
  
  // 中：AI 流程
  addRect(slide, 3.6, 1.7, 3.5, 0.4, {
    radius: 0.04, fill: C.secondary, line: C.secondary, lineWidth: 0,
  });
  addText(slide, "AI-Enabled Flow", 3.6, 1.7, 3.5, 0.4, {
    size: 11, bold: true, color: C.white, align: "center", valign: "middle",
  });
  middleSteps.forEach((s, i) => {
    const y = 2.2 + i * 0.5;
    const isHighlight = s.includes("Agent");
    addRect(slide, 3.6, y, 3.5, 0.4, {
      radius: 0.03,
      fill: isHighlight ? C.primary : C.bg_subtle,
      line: isHighlight ? C.primary : C.secondary,
      lineWidth: isHighlight ? 0 : 0.5,
    });
    addText(slide, s, 3.65, y, 3.4, 0.4, {
      size: 8, color: isHighlight ? C.white : C.ink, bold: isHighlight, valign: "middle",
    });
  });
  
  // 右：根据 case 不同
  if (opts.renderRight) {
    opts.renderRight(slide, page);
  }
  
  addCallout(slide, page.callout, 6.4, opts.calloutIcon || "⊕");
  addFooter(slide, page, page.id);
}

function addCaseStudyCompareSlide(slide, page) {
  // 通用 3 栏：传统 vs AI vs 价值
  addCaseStudy3ColSlide(slide, page, {
    leftTitle: "Traditional Tax Work",
    leftSteps: page.left_traditional_flow_6,
    middleSteps: page.middle_ai_flow_8,
    renderRight: (slide, page) => {
      // 6 个人类高价值场景
      addText(slide, "Where human judgment creates value", 7.4, 1.7, 5.5, 0.4, {
        size: 12, bold: true, color: C.primary, font: F.serif,
      });
      page.right_human_judgment_6.forEach((item, i) => {
        const x = 7.4 + (i % 3) * 1.85;
        const y = 2.2 + Math.floor(i / 3) * 0.95;
        addRect(slide, x, y, 1.7, 0.85, {
          radius: 0.05, fill: C.bg_subtle, line: C.secondary, lineWidth: 0.5,
        });
        addText(slide, item.text, x, y, 1.7, 0.85, {
          size: 9, color: C.primary, bold: true, align: "center", valign: "middle",
        });
      });
      // 3 指标
      page.value_metrics_3.forEach((m, i) => {
        const x = 7.4 + i * 1.85;
        const y = 4.2;
        addRect(slide, x, y, 1.7, 0.6, {
          radius: 0.04, fill: C.secondary, line: C.secondary, lineWidth: 0,
        });
        addText(slide, m, x, y, 1.7, 0.6, {
          size: 8, color: C.white, bold: true, align: "center", valign: "middle",
        });
      });
    },
  });
}

function addActionRoadmapSlide(slide, page) {
  slide.background = { color: C.white };
  addPageTitle(slide, page.title, page.subtitle);
  
  // 8 步（2x4）
  const cardW = 3.0;
  const cardH = 1.5;
  const gapX = 0.1;
  const gapY = 0.15;
  page.steps_8.forEach((s, i) => {
    const col = i % 4;
    const row = Math.floor(i / 4);
    const x = 0.5 + col * (cardW + gapX);
    const y = 1.6 + row * (cardH + gapY);
    addRect(slide, x, y, cardW, cardH, {
      radius: 0.06, fill: C.bg_alt, line: C.secondary, lineWidth: 1,
    });
    addCircle(slide, x + 0.15, y + 0.15, 0.5, 0.5, {
      fill: C.primary, line: C.white, lineWidth: 1.5,
    });
    addText(slide, String(s.num), x + 0.15, y + 0.15, 0.5, 0.5, {
      size: 16, bold: true, color: C.white, align: "center", valign: "middle",
    });
    addText(slide, s.title, x + 0.75, y + 0.15, cardW - 0.85, 0.4, {
      size: 11, bold: true, color: C.primary,
    });
    addText(slide, s.desc, x + 0.15, y + 0.7, cardW - 0.3, cardH - 0.75, {
      size: 8, color: C.muted,
    });
  });
  
  // 底部 8 个指标 pills
  addText(slide, "Pilot Metrics:", 0.5, 5.0, 2.0, 0.4, {
    size: 12, bold: true, color: C.primary, font: F.serif,
  });
  page.pilot_metrics_8.forEach((m, i) => {
    const x = 2.0 + i * 1.35;
    addRect(slide, x, 5.0, 1.3, 0.4, {
      radius: 0.04, fill: C.bg_subtle, line: C.secondary, lineWidth: 0.5,
    });
    addText(slide, m, x, 5.0, 1.3, 0.4, {
      size: 8, color: C.primary, bold: true, align: "center", valign: "middle",
    });
  });
  
  addCallout(slide, page.callout, 5.7, "⊕");
  addFooter(slide, page, page.id);
}

function addQuestions3ColSlide(slide, page) {
  slide.background = { color: C.white };
  addPageTitle(slide, page.title, page.subtitle);
  
  const cardW = 4.0;
  page.questions_3.forEach((q, i) => {
    const x = 0.5 + i * (cardW + 0.15);
    const y = 1.7;
    addRect(slide, x, y, cardW, 4.0, {
      radius: 0.08, fill: C.bg_subtle, line: C.secondary, lineWidth: 1,
    });
    addCircle(slide, x + 0.3, y + 0.3, 0.6, 0.6, {
      fill: C.primary, line: C.white, lineWidth: 1.5,
    });
    addText(slide, String(q.num), x + 0.3, y + 0.3, 0.6, 0.6, {
      size: 18, bold: true, color: C.white, align: "center", valign: "middle",
    });
    addText(slide, q.title, x + 1.05, y + 0.4, cardW - 1.2, 0.5, {
      size: 13, bold: true, color: C.primary, font: F.serif,
    });
    addText(slide, q.main, x + 0.25, y + 1.2, cardW - 0.5, 0.8, {
      size: 11, color: C.ink, bold: true,
    });
    if (q.sub_questions) {
      q.sub_questions.forEach((sq, j) => {
        addText(slide, "→ " + sq, x + 0.3, y + 2.1 + j * 0.4, cardW - 0.6, 0.3, {
          size: 10, color: C.muted,
        });
      });
    }
    if (q.candidates_4) {
      addText(slide, "Candidates:", x + 0.3, y + 2.1, cardW - 0.6, 0.3, {
        size: 10, bold: true, color: C.primary,
      });
      q.candidates_4.forEach((c, j) => {
        const cx = x + 0.3 + (j % 2) * 1.85;
        const cy = y + 2.5 + Math.floor(j / 2) * 0.5;
        addRect(slide, cx, cy, 1.7, 0.4, {
          radius: 0.03, fill: C.white, line: C.secondary, lineWidth: 0.5,
        });
        addText(slide, c, cx, cy, 1.7, 0.4, {
          size: 8, color: C.primary, bold: true, align: "center", valign: "middle",
        });
      });
    }
  });
  
  // 底部 follow-up 4 个问题
  addRect(slide, 0.5, 5.9, 12.3, 0.5, {
    radius: 0.06, fill: C.bg_alt, line: C.primary, lineWidth: 0.5,
  });
  addText(slide, "Follow-up: ", 0.7, 5.9, 1.5, 0.5, {
    size: 11, bold: true, color: C.primary, valign: "middle",
  });
  addText(slide, page.follow_up_4.join("  •  "), 2.0, 5.9, 10.5, 0.5, {
    size: 10, color: C.muted, valign: "middle",
  });
  
  addCallout(slide, page.callout, 6.5, "⊕");
  addFooter(slide, page, page.id);
}

function addJudgments3ColSlide(slide, page) {
  slide.background = { color: C.white };
  addPageTitle(slide, page.title, page.subtitle);
  
  const cardW = 4.0;
  page.judgments_3.forEach((j, i) => {
    const x = 0.5 + i * (cardW + 0.15);
    const y = 1.7;
    addRect(slide, x, y, cardW, 3.8, {
      radius: 0.08, fill: C.bg_subtle, line: C.secondary, lineWidth: 1,
    });
    addCircle(slide, x + cardW / 2 - 0.5, y + 0.3, 1.0, 1.0, {
      fill: C.bg_alt, line: C.primary, lineWidth: 1.5,
    });
    addText(slide, String(i + 1), x + cardW / 2 - 0.5, y + 0.3, 1.0, 1.0, {
      size: 28, bold: true, color: C.primary, font: F.serif, align: "center", valign: "middle",
    });
    addText(slide, j.title, x + 0.2, y + 1.5, cardW - 0.4, 0.5, {
      size: 13, bold: true, color: C.primary, font: F.serif, align: "center",
    });
    addText(slide, j.main, x + 0.25, y + 2.1, cardW - 0.5, 0.8, {
      size: 11, color: C.ink, align: "center", bold: true,
    });
    addText(slide, j.support, x + 0.25, y + 3.0, cardW - 0.5, 0.8, {
      size: 9, color: C.muted, align: "center", italic: true,
    });
  });
  
  // 底部 3 阶段流程
  const flow = page.bottom_flow_3stage;
  const fw = 1.5;
  flow.forEach((s, i) => {
    const x = 4.5 + i * (fw + 0.5);
    addRect(slide, x, 5.8, fw, 0.5, {
      radius: 0.04, fill: C.secondary, line: C.secondary, lineWidth: 0,
    });
    addText(slide, s, x, 5.8, fw, 0.5, {
      size: 11, color: C.white, bold: true, align: "center", valign: "middle",
    });
    if (i < flow.length - 1) {
      addArrow(slide, x + fw + 0.1, 6.05, x + fw + 0.4, 6.05, C.secondary, 2);
    }
  });
  
  addCallout(slide, page.callout, 6.5, "⊕");
  addFooter(slide, page, page.id);
}

function addClosingChallengeSlide(slide, page) {
  slide.background = { color: C.white };
  addText(slide, page.title, 0.5, 0.5, 12.3, 0.8, {
    size: 32, bold: true, color: C.primary, font: F.serif,
  });
  addText(slide, page.subtitle, 0.5, 1.3, 12.3, 0.4, {
    size: 14, color: C.secondary, italic: true,
  });
  
  // 3 股力量 → 中心 Management Agenda
  const forceW = 3.2;
  const forceY = 2.3;
  page.three_forces.forEach((f, i) => {
    const x = 0.5 + i * (forceW + 0.4);
    addRect(slide, x, forceY, forceW, 1.8, {
      radius: 0.08, fill: C.bg_subtle, line: C.secondary, lineWidth: 1,
    });
    addText(slide, f.name, x + 0.2, forceY + 0.15, forceW - 0.4, 0.4, {
      size: 13, bold: true, color: C.primary, font: F.serif, align: "center",
    });
    f.items.forEach((it, j) => {
      addText(slide, "• " + it, x + 0.2, forceY + 0.6 + j * 0.3, forceW - 0.4, 0.3, {
        size: 10, color: C.ink, align: "center",
      });
    });
    // 汇聚箭头
    if (i < 2) {
      addArrow(slide, x + forceW, forceY + 0.9, x + forceW + 0.4, forceY + 0.9, C.secondary, 2);
    }
  });
  
  // 中心汇聚标签
  addCircle(slide, 5.5, 4.5, 2.5, 0.7, {
    fill: C.primary, line: C.primary, lineWidth: 0,
  });
  addText(slide, page.center_convergence, 5.5, 4.5, 2.5, 0.7, {
    size: 14, bold: true, color: C.white, align: "center", valign: "middle",
  });
  
  // 右侧 4 个讨论问题
  addText(slide, "Discussion Questions:", 11.0, 2.3, 2.0, 0.4, {
    size: 11, bold: true, color: C.primary, font: F.serif,
  });
  page.right_4_discussion_questions.forEach((q, i) => {
    const y = 2.7 + i * 0.6;
    addText(slide, "?", 11.0, y, 0.3, 0.5, {
      size: 14, bold: true, color: C.secondary, valign: "middle",
    });
    addText(slide, q, 11.3, y, 2.0, 0.5, {
      size: 9, color: C.ink, valign: "middle",
    });
  });
  
  addCallout(slide, page.callout, 6.0, "⊕");
  addFooter(slide, page, page.id);
}

// ============================================================
// 5. 主流程
// ============================================================
async function main() {
  const pptx = new pptxgen();
  pptx.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
  pptx.layout = "WIDE";
  pptx.author = "AI Agent";
  pptx.subject = "EY China AI Reality — 1:1 PPTX reproduction";
  pptx.title = slidesData.deck_title;
  
  const handlers = {
    cover: addCoverSlide,
    agenda: addAgendaSlide,
    section_divider: addSectionDividerSlide,
    data_dashboard: addDataDashboardSlide,
    timeline: addTimelineSlide,
    loop: addLoopSlide,
    hub_and_spoke: addHubAndSpokeSlide,
    flow_5step: addFlow5StepSlide,
    "3_column_framework": add3ColFrameworkSlide,
    "3_column_composite": add3ColCompositeSlide,
    framework_5stage: addFramework5StageSlide,
    core_foundation: addCoreFoundationSlide,
    case_study_3col: (s, p) => addCaseStudy3ColSlide(s, p, {
      leftTitle: "Traditional Flow",
      leftSteps: p.left_traditional_flow_7 || p.left_traditional_mode_5 || p.left_signals_5,
      middleSteps: p.middle_ai_flow_7 || p.middle_ai_proactive_6 || p.middle_closed_loop_6,
      renderRight: (slide, page) => {
        // 通用右栏渲染（Finance / Proactive / Manufacturing）
        if (page.right_qa_example) {
          addRect(slide, 7.4, 1.7, 5.5, 0.5, {
            radius: 0.04, fill: C.secondary, line: C.secondary, lineWidth: 0,
          });
          addText(slide, "◐ " + page.right_qa_example.question, 7.5, 1.7, 5.3, 0.5, {
            size: 11, bold: true, color: C.white, valign: "middle",
          });
          page.right_qa_example.drivers_8_icons.forEach((d, i) => {
            const x = 7.4 + (i % 4) * 1.4;
            const y = 2.4 + Math.floor(i / 4) * 0.7;
            addCircle(slide, x, y, 0.5, 0.5, {
              fill: C.bg_subtle, line: C.secondary, lineWidth: 0.75,
            });
            addText(slide, d.split(" ")[0], x, y, 0.5, 0.5, {
              size: 8, color: C.primary, bold: true, align: "center", valign: "middle",
            });
            addText(slide, d, x - 0.4, y + 0.55, 1.3, 0.2, {
              size: 7, color: C.muted, align: "center",
            });
          });
          page.right_qa_example.value_metrics_3.forEach((m, i) => {
            const x = 7.4 + i * 1.85;
            const y = 4.6;
            addRect(slide, x, y, 1.7, 0.6, {
              radius: 0.04, fill: C.bg_alt, line: C.primary, lineWidth: 0.5,
            });
            addText(slide, m, x, y, 1.7, 0.6, {
              size: 9, color: C.primary, bold: true, align: "center", valign: "middle",
            });
          });
        } else if (page.right_7_issues_ai_can_surface) {
          page.right_7_issues_ai_can_surface.forEach((it, i) => {
            const x = 7.4 + (i % 3) * 1.85;
            const y = 2.2 + Math.floor(i / 3) * 1.0;
            addRect(slide, x, y, 1.7, 0.85, {
              radius: 0.05, fill: C.bg_subtle, line: C.secondary, lineWidth: 0.5,
            });
            addText(slide, it, x, y, 1.7, 0.85, {
              size: 9, color: C.primary, bold: true, align: "center", valign: "middle",
            });
          });
          page.value_metrics_3.forEach((m, i) => {
            const x = 7.4 + i * 1.85;
            const y = 5.0;
            addRect(slide, x, y, 1.7, 0.6, {
              radius: 0.04, fill: C.secondary, line: C.secondary, lineWidth: 0,
            });
            addText(slide, m, x, y, 1.7, 0.6, {
              size: 8, color: C.white, bold: true, align: "center", valign: "middle",
            });
          });
        } else if (page.right_3_kpis) {
          page.right_3_kpis.forEach((kpi, i) => {
            const y = 2.0 + i * 1.2;
            addRect(slide, 7.4, y, 5.5, 1.0, {
              radius: 0.06, fill: C.bg_subtle, line: C.secondary, lineWidth: 0.5,
            });
            addText(slide, kpi.value, 7.5, y + 0.1, 2.0, 0.5, {
              size: 24, bold: true, color: C.primary, font: F.serif,
            });
            addText(slide, kpi.label, 9.5, y + 0.15, 3.3, 0.7, {
              size: 11, color: C.muted, valign: "middle",
            });
          });
          if (page.illustrative_note) {
            addText(slide, "i  " + page.illustrative_note, 7.4, 5.8, 5.5, 0.3, {
              size: 8, color: C.muted, italic: true,
            });
          }
        }
      },
    }),
    case_study_compare: addCaseStudyCompareSlide,
    case_study_3col_kpi: (s, p) => addCaseStudy3ColSlide(s, p, {
      leftTitle: "Why It's Accelerating",
      leftSteps: p.left_why_accelerating_5,
      middleSteps: [...(p.middle_how_ai_coding_used.above_3 || []), p.middle_how_ai_coding_used.center, ...(p.middle_how_ai_coding_used.below_3 || [])],
      calloutIcon: "⊕",
      renderRight: (slide, page) => {
        addText(slide, "Business Implications", 7.4, 1.7, 5.5, 0.4, {
          size: 13, bold: true, color: C.primary, font: F.serif,
        });
        page.right_business_implications_5.forEach((it, i) => {
          const y = 2.2 + i * 0.45;
          addText(slide, "→ " + it, 7.4, y, 5.5, 0.4, {
            size: 10, color: C.ink,
          });
        });
        // 2 KPI
        page.kpi_2.forEach((kpi, i) => {
          const x = 7.4 + i * 2.8;
          const y = 4.7;
          addCircle(slide, x, y, 1.5, 1.2, {
            fill: C.bg_subtle, line: C.primary, lineWidth: 2,
          });
          addText(slide, kpi.value, x, y + 0.1, 1.5, 0.5, {
            size: 24, bold: true, color: C.primary, font: F.serif, align: "center",
          });
          addText(slide, kpi.label, x, y + 0.7, 1.5, 0.4, {
            size: 8, color: C.muted, align: "center",
          });
        });
        if (page.kpi_note) {
          addText(slide, page.kpi_note, 7.4, 6.0, 5.5, 0.3, {
            size: 8, color: C.muted, italic: true, align: "center",
          });
        }
      },
    }),
    case_study_3col_loop: (s, p) => addCaseStudy3ColSlide(s, p, {
      leftTitle: "Manufacturing Signals",
      leftSteps: p.left_signals_5,
      middleSteps: p.middle_closed_loop_6,
      renderRight: (slide, page) => {
        // AI capabilities
        page.middle_ai_capabilities_4.forEach((cap, i) => {
          const x = 7.4 + (i % 2) * 2.8;
          const y = 1.7 + Math.floor(i / 2) * 0.6;
          addRect(slide, x, y, 2.6, 0.5, {
            radius: 0.04, fill: C.bg_subtle, line: C.secondary, lineWidth: 0.5,
          });
          addText(slide, "✦ " + cap, x, y, 2.6, 0.5, {
            size: 10, color: C.primary, bold: true, align: "center", valign: "middle",
          });
        });
        // KPIs
        addText(slide, "Impact:", 7.4, 3.1, 1.5, 0.4, {
          size: 12, bold: true, color: C.primary, font: F.serif,
        });
        page.right_3_kpis.forEach((kpi, i) => {
          const y = 3.5 + i * 0.85;
          addRect(slide, 7.4, y, 5.5, 0.75, {
            radius: 0.05, fill: C.bg_alt, line: C.secondary, lineWidth: 0.5,
          });
          addText(slide, kpi.value, 7.5, y + 0.1, 1.5, 0.5, {
            size: 18, bold: true, color: C.primary, font: F.serif,
          });
          addText(slide, kpi.label, 9.0, y + 0.15, 3.8, 0.5, {
            size: 10, color: C.muted, valign: "middle",
          });
        });
        if (page.illustrative_note) {
          addText(slide, "i  " + page.illustrative_note, 7.4, 6.0, 5.5, 0.3, {
            size: 8, color: C.muted, italic: true,
          });
        }
      },
    }),
    action_roadmap_8step: addActionRoadmapSlide,
    questions_3col: addQuestions3ColSlide,
    judgments_3col: addJudgments3ColSlide,
    closing_challenge: addClosingChallengeSlide,
  };
  
  slidesData.slides.forEach((page) => {
    const slide = pptx.addSlide();
    slide.background = { color: C.white };
    // 先加原 PDF 底图（最底层）
    addBackground(slide, page.id);
    // 再加 native text/shape（在底图上层，可编辑）
    const handler = handlers[page.type];
    if (handler) {
      try {
        handler(slide, page);
      } catch (e) {
        console.error(`Error on slide ${page.id} (${page.type}):`, e.message);
      }
    } else {
      console.warn(`No handler for type: ${page.type} on slide ${page.id}`);
      addText(slide, `[${page.type}] ${page.title}`, 1, 3, 11, 1, {
        size: 20, color: C.primary, bold: true, align: "center",
      });
    }
  });
  
  const outputPath = path.join(
    PROJECT_DIR,
    "ey-24p-v4-editable.pptx"
  );
  await pptx.writeFile({ fileName: outputPath });
  console.log(`✓ Generated: ${outputPath}`);
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});