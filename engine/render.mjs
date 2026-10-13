// Renders 1080x1080 quote posts to PNG.
//
// single: node engine/render.mjs spec.json out.png
// batch:  node engine/render.mjs --batch batch.json      (array of { ...spec, out })
//
// spec: { "look": "red|blue|green|white|yellow", "tag": "TOPIC", "num": "19",
//         "text": "Plain text with one {{highlighted punch}}.", "handle": "@rohitkaperspective" }
//
// Output JSON per post: { out, look, fontSize, height, lines, lastLineWords, fits, ok }
// ok === false means the post needs a reword: it overflows, or the last line is a single word.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';
import chromium from '@sparticuz/chromium';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const argv = process.argv.slice(2);

let jobs;
if (argv[0] === '--batch') {
  if (!argv[1]) { console.error('usage: node engine/render.mjs --batch batch.json'); process.exit(2); }
  jobs = JSON.parse(fs.readFileSync(argv[1], 'utf8'));
  if (!Array.isArray(jobs)) { console.error('batch file must contain a JSON array'); process.exit(2); }
} else {
  const [specPath, outPath] = argv;
  if (!specPath || !outPath) {
    console.error('usage: node engine/render.mjs spec.json out.png  |  node engine/render.mjs --batch batch.json');
    process.exit(2);
  }
  jobs = [{ ...JSON.parse(fs.readFileSync(specPath, 'utf8')), out: outPath }];
}

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

// Every look's fonts are embedded once, so a batch shares one stylesheet.
let fontCss = '';
const seen = new Set();
for (const L of Object.values(LOOKS)) {
  for (const [fam, pkg, vars] of L.fonts) {
    for (const [w, s] of vars) {
      const key = `${pkg}-${w}-${s}`;
      if (seen.has(key)) continue;
      seen.add(key);
      const f = path.join(ROOT, 'node_modules/@fontsource', pkg, 'files', `${pkg}-latin-${w}-${s}.woff2`);
      const b64 = fs.readFileSync(f).toString('base64');
      fontCss += `@font-face{font-family:'${fam}';font-weight:${w};font-style:${s};src:url(data:font/woff2;base64,${b64}) format('woff2');}\n`;
    }
  }
}

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function buildBody(spec) {
  const L = LOOKS[spec.look];
  if (!L) throw new Error(`unknown look "${spec.look}" (use ${Object.keys(LOOKS).join(', ')})`);
  const handle = spec.handle || '@rohitkaperspective';
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
  return `<div id="card" style="width:1080px;height:1080px;box-sizing:border-box;background:${L.bg};color:${L.color};display:flex;flex-direction:column;justify-content:space-between;padding:96px 150px 88px 150px;font-family:${L.stack};overflow:hidden">
<div style="display:flex;justify-content:space-between;align-items:center;${mono};font-size:24px;letter-spacing:0.14em;text-transform:uppercase;color:${L.tag}"><span>${esc(spec.tag || '')}</span><span>${esc(String(spec.num || ''))}</span></div>
<div id="q" style="font-size:${L.max}px;line-height:${L.lh};font-weight:${L.weight};letter-spacing:${L.ls};text-align:${L.align};text-wrap:balance;${L.upper ? 'text-transform:uppercase;' : ''}">${text}</div>
<div style="display:flex;justify-content:space-between;align-items:center;${L.rule ? `border-top:3px solid ${L.rule};padding-top:28px;` : ''}${mono};font-size:22px;letter-spacing:0.1em"><span>${esc(handle)}</span><span style="color:${L.accent}">SAVE + SHARE</span></div>
</div>`;
}

// Shrinks the quote until it fits, then reports the line count and how many
// words sit on the final visual line (one word reads as an orphan).
function measure({ max, min, lh }) {
  const q = document.getElementById('q');
  const LIMIT = 660;
  let s = max;
  for (; s >= min; s -= 2) {
    q.style.fontSize = s + 'px';
    if (q.getBoundingClientRect().height <= LIMIT) break;
  }
  if (s < min) { s = min; q.style.fontSize = s + 'px'; }
  const h = q.getBoundingClientRect().height;

  // Group words by the vertical position of their own client rect.
  const rows = new Map();
  const walk = document.createTreeWalker(q, NodeFilter.SHOW_TEXT);
  const range = document.createRange();
  let node;
  while ((node = walk.nextNode())) {
    const t = node.textContent;
    for (const m of t.matchAll(/\S+/g)) {
      range.setStart(node, m.index);
      range.setEnd(node, m.index + m[0].length);
      const r = range.getBoundingClientRect();
      if (!r.width && !r.height) continue;
      const key = Math.round(r.top / 4) * 4;
      rows.set(key, (rows.get(key) || 0) + 1);
    }
  }
  const keys = [...rows.keys()].sort((a, b) => a - b);
  const lastLineWords = keys.length ? rows.get(keys[keys.length - 1]) : 0;

  return {
    fontSize: s,
    height: Math.round(h),
    lines: keys.length || Math.round(h / (s * lh)),
    lastLineWords,
    fits: h <= LIMIT,
  };
}

const browser = await puppeteer.launch({
  args: chromium.args,
  executablePath: await chromium.executablePath(),
  headless: 'shell',
});
let bad = 0;
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1080, deviceScaleFactor: 1 });
  await page.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>${fontCss}
body{margin:0}</style></head><body><div id="root"></div></body></html>`, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);

  for (const spec of jobs) {
    const L = LOOKS[spec.look];
    if (!L) throw new Error(`unknown look "${spec.look}" in job for ${spec.out}`);
    await page.evaluate((html) => { document.getElementById('root').innerHTML = html; }, buildBody(spec));
    const fit = await page.evaluate(measure, { max: L.max, min: L.min, lh: L.lh });
    fs.mkdirSync(path.dirname(path.resolve(spec.out)), { recursive: true });
    await page.screenshot({ path: spec.out, clip: { x: 0, y: 0, width: 1080, height: 1080 } });
    const ok = fit.fits && fit.lastLineWords >= 2;
    if (!ok) bad++;
    console.log(JSON.stringify({ out: spec.out, look: spec.look, ...fit, ok }));
  }
  if (bad) {
    console.error(`${bad} post(s) need a reword: overflow, or a single-word last line.`);
    process.exitCode = 3;
  }
} finally {
  await browser.close();
}
