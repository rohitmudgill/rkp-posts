// Painted-flat illustration posts: white page, condensed brown/red type, hand-built SVG scenes.
// usage: node engine/illu/render_illu.mjs spec.json   (array of {scene, w, h, lines, color, out, ...})
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';
import chromium from '@sparticuz/chromium';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const font = fs.readFileSync(path.join(ROOT,'node_modules/@fontsource/fira-sans-extra-condensed/files/fira-sans-extra-condensed-latin-500-normal.woff2')).toString('base64');

const C = { ink:'#4a1d12', red:'#a8241b', olive:'#556b2a', mustard:'#e9b52f', cream:'#f3e6c4', skin:'#e9a877', hair:'#2b1810', black:'#2c2c2e', brown:'#8a3a1c', white:'#fffdf8' };

const FILTER = `<defs><filter id="paint" x="-5%" y="-5%" width="110%" height="110%">
<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4" result="warp"/>
<feDisplacementMap in="SourceGraphic" in2="warp" scale="4.5" result="d"/>
<feTurbulence type="fractalNoise" baseFrequency="0.012 0.32" numOctaves="3" seed="11" result="st"/>
<feColorMatrix in="st" type="matrix" values="0 0 0 0 0.12  0 0 0 0 0.05  0 0 0 0 0.02  0 0 0 -2.2 1.25" result="sa"/>
<feComponentTransfer in="sa" result="sb"><feFuncA type="linear" slope="0.30"/></feComponentTransfer>
<feComposite in="sb" in2="d" operator="in" result="tex"/>
<feTurbulence type="fractalNoise" baseFrequency="0.02 0.28" numOctaves="2" seed="21" result="st2"/>
<feColorMatrix in="st2" type="matrix" values="0 0 0 0 1  0 0 0 0 0.97  0 0 0 0 0.88  0 0 0 -2.4 1.1" result="la"/>
<feComponentTransfer in="la" result="lb"><feFuncA type="linear" slope="0.22"/></feComponentTransfer>
<feComposite in="lb" in2="d" operator="in" result="lite"/>
<feMerge><feMergeNode in="d"/><feMergeNode in="tex"/><feMergeNode in="lite"/></feMerge></filter></defs>`;

// ---------- scenes (all drawn on a 1080-wide canvas; y offset passed in) ----------
const scenes = {
  // seated man looking up at a storm in his head, calm tea beside him
  imagination: (ox=0, oy=0, tr) => `<g transform="${tr || `translate(${ox},${oy})`}" filter="url(#paint)">
    <!-- storm bubble -->
    <g transform="translate(120,-165)"><path d="M520 150 C470 150 440 190 455 228 C415 240 410 300 455 318 C470 365 545 372 580 340 C625 372 705 352 712 300 C760 290 765 225 715 207 C710 160 640 140 600 170 C575 150 545 145 520 150Z" fill="${C.black}"/>
    <path d="M590 235 L545 305 L585 300 L560 365 L640 275 L598 280 L625 235Z" fill="${C.mustard}"/>
    </g><circle cx="640" cy="232" r="15" fill="${C.black}"/><circle cx="598" cy="262" r="9" fill="${C.black}"/>
    <!-- armchair -->
    <path d="M205 590 L205 840 L260 840 L270 640Z" fill="${C.brown}"/>
    <path d="M215 640 L330 620 L360 800 L230 810Z" fill="${C.mustard}"/>
    <path d="M205 830 L215 1010 L250 1010 L262 835Z" fill="${C.brown}"/>
    <path d="M520 820 L535 1010 L570 1010 L560 820Z" fill="${C.brown}"/>
    <path d="M230 800 L610 800 L620 850 L225 850Z" fill="${C.brown}"/>
    <path d="M250 760 L585 760 L600 810 L245 810Z" fill="${C.mustard}"/>
    <!-- man: legs crossed -->
    <path d="M330 720 L560 705 C610 703 650 735 655 770 L650 790 L560 790 L330 800Z" fill="${C.cream}"/>
    <path d="M610 790 C650 780 700 790 735 830 L760 900 L700 920 L670 860 L610 835Z" fill="${C.cream}"/>
    <path d="M690 905 L790 880 C820 880 835 910 815 925 L700 945Z" fill="#f6f1e6" stroke="${C.ink}" stroke-width="3"/>
    <path d="M560 790 C580 840 590 900 585 985 L640 985 L650 840Z" fill="${C.cream}"/>
    <path d="M575 975 L700 970 C715 985 705 1005 690 1008 L585 1008Z" fill="#f6f1e6" stroke="${C.ink}" stroke-width="3"/>
    <!-- torso -->
    <path d="M300 520 C330 470 420 450 470 470 C520 490 545 560 560 640 L575 740 L335 750 C300 690 285 600 300 520Z" fill="${C.olive}"/>
    <path d="M420 470 C435 520 440 600 430 750" stroke="#3f5220" stroke-width="5" fill="none"/>
    <path d="M430 560 L445 570 M430 640 L445 650" stroke="${C.cream}" stroke-width="10" stroke-linecap="round"/>
    <!-- arm to chin -->
    <path d="M470 520 C530 520 585 560 575 640 L520 650 C505 600 480 585 470 585Z" fill="#46591f"/>
    <path d="M500 405 C530 380 575 395 585 430 C580 470 550 495 520 492Z" fill="${C.skin}"/>
    <!-- head -->
    <path d="M395 365 C395 320 430 285 480 290 C535 295 560 340 556 395 C552 445 520 480 470 478 C420 474 395 430 395 365Z" fill="${C.skin}"/>
    <path d="M388 355 C385 295 430 262 485 268 C545 275 575 320 560 372 C548 340 520 322 480 325 C440 328 418 345 405 380Z" fill="${C.hair}"/>
    <path d="M556 380 L586 402 L556 418Z" fill="#dc9568"/>
    <circle cx="518" cy="378" r="7" fill="${C.ink}"/>
    <path d="M498 358 L538 352" stroke="${C.hair}" stroke-width="6" stroke-linecap="round"/>
    <path d="M495 445 C515 452 535 446 548 432" stroke="${C.ink}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <!-- side table + calm tea -->
    <ellipse cx="900" cy="905" rx="95" ry="22" fill="${C.mustard}"/>
    <path d="M820 915 L835 1010 L860 1010 L850 925Z M940 915 L930 1010 L955 1010 L970 925Z" fill="${C.brown}"/>
    <path d="M858 820 L942 820 L935 895 C930 912 870 912 865 895Z" fill="${C.cream}" stroke="${C.ink}" stroke-width="3"/>
    <path d="M940 840 C975 835 975 880 935 878" fill="none" stroke="${C.ink}" stroke-width="7"/>
    <path d="M880 800 C865 780 895 770 880 745 M915 800 C900 780 930 770 915 745" stroke="${C.red}" stroke-width="7" fill="none" stroke-linecap="round"/>
  </g>`,
};

const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
function page(spec){
  const {w,h,lines,by,color=C.ink,handle='@rohitkaperspective',scene,size=118,num} = spec;
  const text = lines.map((l,i)=>`<div>${esc(l)}</div>`).join('');
  return `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'FSC';font-weight:500;src:url(data:font/woff2;base64,${font}) format('woff2');}
html,body{margin:0;background:${C.white}}
#c{position:relative;width:${w}px;height:${h}px;background:${C.white};overflow:hidden;font-family:'FSC',sans-serif}
#t{position:absolute;left:62px;top:${spec.top ?? 64}px;font-size:${size}px;line-height:1.02;font-weight:500;color:${color};letter-spacing:0.005em}
#by{position:absolute;left:66px;font-size:40px;letter-spacing:0.06em;color:${C.red}}
#h{position:absolute;left:0;right:0;bottom:22px;text-align:center;font-size:30px;color:${C.ink};letter-spacing:0.03em}
svg{position:absolute;left:0;top:0}
</style></head><body><div id="c">
<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${FILTER}${scenes[scene](spec.ox||0,spec.oy||0,spec.tr)}</svg>
<div id="t">${text}</div><div id="by">${esc(by||'')}</div><div id="h">${handle}</div></div></body></html>`;
}
const jobs = JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const browser = await puppeteer.launch({args:chromium.args,executablePath:await chromium.executablePath(),headless:'shell'});
try{
  const p = await browser.newPage();
  for(const j of jobs){
    await p.setViewport({width:j.w,height:j.h,deviceScaleFactor:1});
    await p.setContent(page(j),{waitUntil:'load'});
    await p.evaluate(()=>document.fonts.ready);
    // place attribution right under the text block
    await p.evaluate(()=>{const t=document.getElementById('t').getBoundingClientRect();document.getElementById('by').style.top=(t.bottom+14)+'px';});
    fs.mkdirSync(path.dirname(path.resolve(j.out)),{recursive:true});
    await p.screenshot({path:j.out,clip:{x:0,y:0,width:j.w,height:j.h}});
    console.log('ok',j.out);
  }
} finally { await browser.close(); }
