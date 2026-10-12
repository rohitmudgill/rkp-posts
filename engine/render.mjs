// Renders one 1080x1080 quote post to PNG.
// usage: node engine/render.mjs spec.json out.png
// spec: { "look": "red|blue|green|white|yellow", "tag": "TOPIC", "num": "19",
//         "text": "Plain text with one {{highlighted punch}}.", "handle": "@rohitkaperspective" }
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';
import chromium from '@sparticuz/chromium';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [, , specPath, outPath] = process.argv;
if (!specPath || !outPath) {
  console.error('usage: node engine/render.mjs spec.json out.png');
  process.exit(2);
}
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const handle = spec.handle || '@rohitkaperspective';

const MONO = ['Space Mono', 'space-mono', [[700, 'normal']]];
const LOOKS = {
  red: {
    bg: '#E1261C', color: '#FFFFFF', stack: "'Anton', sans-serif", weight: 400, upper: true,
    ls: '0.01em', lh: 1.25, align: 'left', max: 104, min: 70, tag: '#FFFFFF', accent: '#FFFFFF',
    hl: 'block', hlBg: '#0A0A0A', hlColor: '#FFFFFF', rule: null,
    fonts: [['Anton', 'anton', [[400, 'normal']]], MONO],
  },
  blue: {
    bg: '#0D2B6B', color: '#FFFFFF', stack: "'Bricolage Grotesque', sans-serif", weight: 800, upper: false,
    ls: '-0.02em', lh: 1.08, align: 'left', max: 92, min: 58, tag: '#FFD43B', accent: '#FFD43B',
    hl: 'color', hlColor: '#FFD43B', rule: null,
    fonts: [['Bricolage Grotesque', 'bricolage-grotesque', [[800, 'normal']]], MONO],
  },
  green: {
    bg: '#0C5A3E', color: '#F6F3EC', stack: "'Syne', sans-serif", weight: 700, upper: false,
    ls: '-0.01em', lh: 1.16, align: 'center', max: 84, min: 54, tag: '#C8F560', accent: '#C8F560',
    hl: 'color', hlColor: '#C8F560', rule: null,
    fonts: [['Syne', 'syne', [[700, 'normal']]], MONO],
  },
  white: {
    bg: '#FFFFFF', color: '#0A0A0A', stack: "'Space Mono', monospace", weight: 700, upper: false,
    ls: '0', lh: 1.36, align: 'left', max: 66, min: 44, tag: '#E1261C', accent: '#E1261C',
    hl: 'underline', hlColor: '#E1261C', rule: '#0A0A0A',
    fonts: [MONO],
  },
  yellow: {
    bg: '#FFD43B', color: '#0A1F52', stack: "'Instrument Serif', serif", weight: 400, upper: false,
    ls: '-0.015em', lh: 1.04, align: 'left', max: 124, min: 76, tag: '#0A1F52', accent: '#0A1F52',
    hl: 'italic', hlColor: '#B3171B', rule: '#0A1F52',
    fonts: [['Instrument Serif', 'instrument-serif', [[400, 'normal'], [400, 'italic']]], MONO],
  },
};
const L = LOOKS[spec.look];
if (!L) throw new Error(`unknown look "${spec.look}" (use ${Object.keys(LOOKS).join(', ')})`);

let fontCss = '';
for (const [fam, pkg, vars] of L.fonts) {
  for (const [w, s] of vars) {
    const f = path.join(ROOT, 'node_modules/@fontsource', pkg, 'files', `${pkg}-latin-${w}-${s}.woff2`);
    const b64 = fs.readFileSync(f).toString('base64');
    fontCss += `@font-face{font-family:'${fam}';font-weight:${w};font-style:${s};src:url(data:font/woff2;base64,${b64}) format('woff2');}\n`;
  }
}

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const hlCss = {
  block: `background:${L.hlBg};color:${L.hlColor};padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone`,
  color: `color:${L.hlColor}`,
  underline: `text-decoration:underline;text-decoration-color:${L.hlColor};text-decoration-thickness:6px;text-underline-offset:10px`,
  italic: `font-style:italic;color:${L.hlColor}`,
}[L.hl];

let text = esc(spec.text);
text = text.replace(/\b\w+(?:-\w+)+\b/g, (m) => `<span style="white-space:nowrap">${m}</span>`);
text = text.replace(/\{\{([\s\S]+?)\}\}/g, (_, t) => `<span style="${hlCss}">${t}</span>`);

const mono = "font-family:'Space Mono',monospace;font-weight:700";
const html = `<!doctype html><html><head><meta charset="utf-8"><style>${fontCss}
body{margin:0}</style></head><body>
<div style="width:1080px;height:1080px;box-sizing:border-box;background:${L.bg};color:${L.color};display:flex;flex-direction:column;justify-content:space-between;padding:96px 150px 88px 150px;font-family:${L.stack};overflow:hidden">
<div style="display:flex;justify-content:space-between;align-items:center;${mono};font-size:24px;letter-spacing:0.14em;text-transform:uppercase;color:${L.tag}"><span>${esc(spec.tag || '')}</span><span>${esc(String(spec.num || ''))}</span></div>
<div id="q" style="font-size:${L.max}px;line-height:${L.lh};font-weight:${L.weight};letter-spacing:${L.ls};text-align:${L.align};text-wrap:balance;${L.upper ? 'text-transform:uppercase;' : ''}">${text}</div>
<div style="display:flex;justify-content:space-between;align-items:center;${L.rule ? `border-top:3px solid ${L.rule};padding-top:28px;` : ''}${mono};font-size:22px;letter-spacing:0.1em"><span>${esc(handle)}</span><span style="color:${L.accent}">SAVE + SHARE</span></div>
</div></body></html>`;

const browser = await puppeteer.launch({
  args: chromium.args,
  executablePath: await chromium.executablePath(),
  headless: 'shell',
});
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1080, deviceScaleFactor: 1 });
  await page.setContent(html, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const fit = await page.evaluate(({ max, min, lh }) => {
    const q = document.getElementById('q');
    const LIMIT = 660;
    let s = max;
    for (; s >= min; s -= 2) {
      q.style.fontSize = s + 'px';
      if (q.getBoundingClientRect().height <= LIMIT) break;
    }
    if (s < min) { s = min; q.style.fontSize = s + 'px'; }
    const h = q.getBoundingClientRect().height;
    return { fontSize: s, height: Math.round(h), lines: Math.round(h / (s * lh)), fits: h <= LIMIT };
  }, { max: L.max, min: L.min, lh: L.lh });
  fs.mkdirSync(path.dirname(path.resolve(outPath)), { recursive: true });
  await page.screenshot({ path: outPath, clip: { x: 0, y: 0, width: 1080, height: 1080 } });
  console.log(JSON.stringify({ out: outPath, look: spec.look, ...fit }));
  if (!fit.fits) {
    console.error('TEXT TOO LONG for this look: shorten the quote and render again');
    process.exitCode = 3;
  }
} finally {
  await browser.close();
}
