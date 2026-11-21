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

// ---- shared figure helpers (local coordinates) ----
function headAt(cx, cy, f=1, hair=C.hair){
  return `<g transform="translate(${cx},0) scale(${f},1) translate(${-cx},0)">
    <ellipse cx="${cx}" cy="${cy}" rx="40" ry="46" fill="${C.skin}"/>
    <path d="M${cx-43} ${cy-6} C${cx-48} ${cy-62} ${cx+30} ${cy-72} ${cx+43} ${cy-20} C${cx+26} ${cy-36} ${cx-10} ${cy-40} ${cx-43} ${cy-6}Z" fill="${hair}"/>
    <path d="M${cx+40} ${cy+2} L${cx+58} ${cy+16} L${cx+38} ${cy+22}Z" fill="#dc9568"/>
    <circle cx="${cx+20}" cy="${cy+2}" r="5.5" fill="${C.ink}"/>
    <path d="M${cx+6} ${cy-14} L${cx+32} ${cy-18}" stroke="${hair}" stroke-width="5" stroke-linecap="round"/>
    <path d="M${cx+8} ${cy+30} C${cx+22} ${cy+36} ${cx+34} ${cy+32} ${cx+40} ${cy+24}" stroke="${C.ink}" stroke-width="4" fill="none" stroke-linecap="round"/>
  </g>`;
}
function man(cx, by, o={}){
  const {shirt=C.red, pants=C.black, f=1, armL=[-40,40], armR=[40,40]} = o;
  const sh=[cx, by-300];
  const arm=(dx)=>{const [ax,ay]=dx; const ex=sh[0]+ax*0.5, ey=sh[1]+60+ay*0.35, hx=sh[0]+ax, hy=sh[1]+90+ay; return `<path d="M${sh[0]} ${sh[1]+12} Q${ex} ${ey} ${hx} ${hy}" stroke="${shirt}" stroke-width="38" fill="none" stroke-linecap="round"/><circle cx="${hx}" cy="${hy}" r="21" fill="${C.skin}"/>`;};
  const g = `
    <path d="M${cx-52} ${by-160} L${cx-46} ${by-14} L${cx-8} ${by-14} L${cx-2} ${by-160}Z" fill="${pants}"/>
    <path d="M${cx+2} ${by-160} L${cx+8} ${by-14} L${cx+46} ${by-14} L${cx+52} ${by-160}Z" fill="${pants}"/>
    <path d="M${cx-60} ${by-12} L${cx-4} ${by-12} L${cx-6} ${by+8} L${cx-66} ${by+8}Z M${cx+4} ${by-12} L${cx+60} ${by-12} L${cx+66} ${by+8} L${cx+6} ${by+8}Z" fill="#f6f1e6" stroke="${C.ink}" stroke-width="4"/>
    ${arm(armL)}
    <path d="M${cx-62} ${by-292} C${cx-62} ${by-312} ${cx+62} ${by-312} ${cx+62} ${by-292} L${cx+56} ${by-150} L${cx-56} ${by-150}Z" fill="${shirt}"/>
    ${arm(armR)}
    <rect x="${cx-16}" y="${by-322}" width="32" height="34" fill="${C.skin}"/>
    ${headAt(cx, by-355, 1)}`;
  return f===1 ? `<g>${g}</g>` : `<g transform="translate(${cx},0) scale(-1,1) translate(${-cx},0)">${g}</g>`;
}

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

  way: () => `<g filter="url(#paint)">
    <path d="M0 880 L1000 880 L1000 1000 L0 1000Z" fill="${C.mustard}"/>
    <path d="M120 880 C200 600 330 470 470 470 C700 470 860 640 880 880Z" fill="#8c8a82"/>
    <path d="M300 880 C330 700 420 600 520 590 C640 590 720 700 760 880Z" fill="#a3a199"/>
    ${man(520,590,{shirt:C.red,pants:C.black,f:1,armL:[-70,-60],armR:[80,-100]})}
  </g>`,
  hourglass: () => `<g filter="url(#paint)">
    <path d="M0 960 L1000 960 L1000 1000 L0 1000Z" fill="${C.mustard}"/>
    <rect x="360" y="230" width="280" height="36" rx="10" fill="${C.brown}"/><rect x="360" y="900" width="280" height="36" rx="10" fill="${C.brown}"/>
    <path d="M385 266 L615 266 C615 400 540 450 520 500 C540 550 615 600 615 900 L385 900 C385 600 460 550 480 500 C460 450 385 400 385 266Z" fill="#f6f1e6" stroke="${C.ink}" stroke-width="6"/>
    <path d="M400 290 L600 290 C600 380 545 430 500 470Z" fill="${C.mustard}"/>
    <path d="M385 900 C390 800 440 740 500 700 C560 740 610 800 615 900Z" fill="${C.mustard}"/>
    <path d="M497 500 L503 500 L503 700 L497 700Z" fill="${C.mustard}"/>
    ${man(790,960,{shirt:C.olive,pants:C.cream,f:-1,armL:[-60,-60],armR:[-40,-110]})}
  </g>`,
  lantern: () => `<g filter="url(#paint)">
    <path d="M0 940 L1000 940 L1000 1000 L0 1000Z" fill="${C.olive}"/>
    <circle cx="470" cy="560" r="230" fill="${C.mustard}" opacity="0.28"/>
    ${man(500,940,{shirt:C.red,pants:C.black,f:1,armL:[70,-50],armR:[85,-5]})}
    <rect x="610" y="640" width="64" height="88" rx="10" fill="${C.cream}" stroke="${C.ink}" stroke-width="5"/>
    <path d="M642 665 C625 690 630 712 642 712 C654 712 660 690 642 665Z" fill="${C.red}"/>
    <path d="M628 640 C628 610 656 610 656 640" fill="none" stroke="${C.ink}" stroke-width="5"/>
  </g>`,
  sunrise: () => `<g filter="url(#paint)">
    <circle cx="500" cy="640" r="300" fill="${C.mustard}"/>
    <path d="M0 780 C200 700 340 760 520 740 C720 720 860 780 1000 740 L1000 1000 L0 1000Z" fill="${C.olive}"/>
    <path d="M0 880 C250 830 500 900 1000 850 L1000 1000 L0 1000Z" fill="#3f5220"/>
    ${man(500,860,{shirt:C.red,pants:C.black,f:1,armL:[-60,-150],armR:[60,-150]})}
  </g>`,
  boat: () => `<g filter="url(#paint)">
    <path d="M0 760 C120 730 220 790 340 760 C460 730 560 790 680 760 C800 730 900 790 1000 760 L1000 1000 L0 1000Z" fill="#2f6f73"/>
    <path d="M0 860 C120 830 220 890 340 860 C460 830 560 890 680 860 C800 830 900 890 1000 860 L1000 1000 L0 1000Z" fill="#265a5e"/>
    <path d="M500 220 L500 740" stroke="${C.ink}" stroke-width="12"/>
    <path d="M512 240 C640 330 700 520 700 700 L512 700Z" fill="${C.cream}" stroke="${C.ink}" stroke-width="4"/>
    <path d="M488 300 C400 400 360 560 360 700 L488 700Z" fill="${C.mustard}"/>
    <path d="M250 740 L760 740 C720 830 640 860 520 860 C400 860 300 830 250 740Z" fill="${C.brown}"/>
    ${man(380,740,{shirt:C.red,pants:C.black,f:1,armL:[70,-80],armR:[80,-110]})}
    <circle cx="470" cy="620" r="26" fill="${C.cream}" stroke="${C.ink}" stroke-width="5"/><path d="M470 600 L478 628" stroke="${C.red}" stroke-width="6"/>
  </g>`,
  citadel: () => `<g filter="url(#paint)">
    <path d="M0 930 L1000 930 L1000 1000 L0 1000Z" fill="${C.olive}"/>
    <path d="M60 80 C40 150 120 190 190 150 C250 220 360 200 380 140 C470 150 520 80 450 40 C420 -10 320 -10 290 40 C230 -20 110 0 60 80Z" fill="${C.black}" transform="translate(30,40)"/>
    <path d="M620 60 C600 120 680 160 740 120 C800 190 900 170 920 110 C990 120 1010 60 950 30 C920 -15 830 -10 800 30 C750 -20 650 0 620 60Z" fill="${C.black}" transform="translate(-20,80)"/>
    <path d="M130 250 l-30 70 M200 280 l-30 70 M280 240 l-30 70 M760 260 l-30 70 M840 290 l-30 70 M900 250 l-30 70 M170 380 l-30 70 M860 410 l-30 70" stroke="#2f6f73" stroke-width="8" stroke-linecap="round"/>
    <path d="M330 930 L330 420 L350 420 L350 380 L400 380 L400 420 L450 420 L450 380 L500 380 L500 420 L550 420 L550 380 L600 380 L600 420 L670 420 L670 930Z" fill="${C.cream}" stroke="${C.ink}" stroke-width="6"/>
    <path d="M440 930 L440 780 C440 720 560 720 560 780 L560 930Z" fill="${C.brown}"/>
    <rect x="430" y="500" width="62" height="100" rx="30" fill="${C.mustard}"/><rect x="520" y="500" width="62" height="100" rx="30" fill="${C.mustard}"/>
    <path d="M330 610 L670 610" stroke="${C.brown}" stroke-width="8"/>
  </g>`,
  listen: () => `<g filter="url(#paint)">
    <path d="M0 960 L1000 960 L1000 1000 L0 1000Z" fill="${C.mustard}"/>
    <ellipse cx="500" cy="800" rx="220" ry="40" fill="${C.red}"/><rect x="480" y="800" width="40" height="160" fill="${C.brown}"/>
    <path d="M395 760 L440 700 L470 700 L470 770Z M590 760 L550 700 L520 700 L520 770Z" fill="#f6f1e6" stroke="${C.ink}" stroke-width="4"/>
    <!-- speaker left -->
    <path d="M140 960 L140 560 C140 500 200 480 260 480 C330 480 350 540 350 600 L350 800 L330 960Z" fill="${C.red}"/>
    <g>${headAt(230,400,1)}</g>
    <path d="M300 410 C330 395 360 405 372 428 M310 440 C345 430 375 445 380 470" stroke="${C.ink}" stroke-width="6" fill="none" stroke-linecap="round"/>
    <!-- listener right -->
    <path d="M860 960 L860 560 C860 500 800 480 740 480 C670 480 650 540 650 600 L650 800 L670 960Z" fill="${C.olive}"/>
    <g>${headAt(770,400,-1)}</g>
    <ellipse cx="800" cy="408" rx="28" ry="46" fill="#e0976a" stroke="${C.ink}" stroke-width="4"/>
    <path d="M640 600 C600 640 590 690 640 710" stroke="#46591f" stroke-width="34" fill="none" stroke-linecap="round"/>
  </g>`,
  goldfire: () => `<g filter="url(#paint)">
    <path d="M0 940 L1000 940 L1000 1000 L0 1000Z" fill="${C.brown}"/>
    <path d="M330 940 C300 860 360 800 400 720 C410 780 450 790 470 740 C480 660 460 600 500 540 C540 620 590 650 580 740 C620 720 640 690 640 640 C700 710 720 830 680 940Z" fill="${C.red}"/>
    <path d="M410 940 C400 880 440 850 470 800 C490 850 520 860 540 820 C590 880 600 910 580 940Z" fill="${C.mustard}"/>
    <path d="M250 520 L750 520 L710 400 L290 400Z" fill="${C.mustard}" stroke="${C.ink}" stroke-width="6"/>
    <path d="M300 420 L690 420" stroke="#fff3c2" stroke-width="10" opacity="0.6"/>
    <rect x="230" y="520" width="540" height="40" rx="8" fill="${C.black}"/>
  </g>`,
  chain: () => `<g filter="url(#paint)">
    <path d="M0 950 L1000 950 L1000 1000 L0 1000Z" fill="${C.olive}"/>
    <circle cx="500" cy="420" r="280" fill="${C.mustard}" opacity="0.4"/>
    ${man(500,950,{shirt:C.olive==='x'?C.red:C.red,pants:C.black,f:1,armL:[-120,-170],armR:[120,-170]})}
    <g stroke="${C.black}" stroke-width="9" fill="none"><rect x="270" y="560" width="46" height="26" rx="13" transform="rotate(-25 293 573)"/><rect x="250" y="620" width="46" height="26" rx="13" transform="rotate(20 273 633)"/><rect x="690" y="560" width="46" height="26" rx="13" transform="rotate(25 713 573)"/><rect x="720" y="630" width="46" height="26" rx="13" transform="rotate(-20 743 643)"/></g>
  </g>`,
  sapling: () => `<g filter="url(#paint)">
    <path d="M0 900 L1000 900 L1000 1000 L0 1000Z" fill="${C.brown}"/>
    <circle cx="120" cy="880" r="22" fill="${C.black}"/>
    <path d="M290 900 C290 860 290 840 292 810 M292 830 C260 820 250 790 262 770 C290 770 302 800 292 830 M292 840 C322 830 332 800 320 780 C294 780 284 810 292 840" stroke="${C.olive}" stroke-width="10" fill="${C.olive}"/>
    <path d="M470 900 L470 700" stroke="${C.brown}" stroke-width="22"/><circle cx="470" cy="650" r="80" fill="${C.olive}"/><circle cx="420" cy="690" r="55" fill="#46591f"/>
    <path d="M680 900 L680 480" stroke="${C.brown}" stroke-width="40"/><circle cx="680" cy="400" r="150" fill="${C.olive}"/><circle cx="590" cy="470" r="95" fill="#46591f"/><circle cx="780" cy="470" r="90" fill="#3f5220"/>
    <circle cx="880" cy="140" r="80" fill="${C.mustard}"/>
  </g>`,
  stars: () => `<g filter="url(#paint)">
    <path d="M0 800 C250 720 500 760 760 700 C880 690 940 720 1000 740 L1000 1000 L0 1000Z" fill="${C.olive}"/>
    <circle cx="800" cy="200" r="90" fill="${C.mustard}"/><circle cx="835" cy="180" r="80" fill="${C.white}"/>
    ${[[160,170],[330,110],[470,260],[600,150],[240,320],[90,420],[650,330]].map(([x,y])=>`<path d="M${x} ${y-26} L${x+8} ${y-8} L${x+26} ${y} L${x+8} ${y+8} L${x} ${y+26} L${x-8} ${y+8} L${x-26} ${y} L${x-8} ${y-8}Z" fill="${C.mustard}"/>`).join('')}
    <path d="M360 800 C350 700 380 640 440 630 C520 625 560 690 560 800Z" fill="${C.red}"/>
    <ellipse cx="455" cy="590" rx="52" ry="56" fill="${C.hair}"/>
  </g>`,
  balance: () => `<g filter="url(#paint)">
    <path d="M0 950 L1000 950 L1000 1000 L0 1000Z" fill="${C.mustard}"/>
    <rect x="470" y="300" width="60" height="650" fill="${C.brown}"/><path d="M380 950 L620 950 L580 900 L420 900Z" fill="${C.brown}"/>
    <path d="M150 380 L850 300" stroke="${C.ink}" stroke-width="22" stroke-linecap="round"/>
    <path d="M150 380 L80 600 M150 380 L220 600 M850 300 L780 520 M850 300 L920 520" stroke="${C.ink}" stroke-width="6"/>
    <path d="M60 600 L240 600 C230 660 80 660 60 600Z" fill="${C.red}"/>
    <path d="M760 520 L940 520 C930 580 780 580 760 520Z" fill="${C.olive}"/>
    <circle cx="150" cy="560" r="36" fill="${C.black}"/>
    <path d="M820 480 C800 440 860 440 880 480Z" fill="#f6f1e6" stroke="${C.ink}" stroke-width="4"/>
    <circle cx="500" cy="290" r="40" fill="${C.red}"/>
  </g>`,
};

const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
function page(spec){
  const {w,h,lines,by,color=C.ink,handle='@rohitkaperspective',scene,size=118,num} = spec;
  const text = esc(spec.text || (lines||[]).join(' '));
  return `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'FSC';font-weight:500;src:url(data:font/woff2;base64,${font}) format('woff2');}
html,body{margin:0;background:${C.white}}
#c{position:relative;width:${w}px;height:${h}px;background:${C.white};overflow:hidden;font-family:'FSC',sans-serif}
#t{position:absolute;left:62px;width:${spec.tw||930}px;top:${spec.top ?? 64}px;font-size:${size}px;line-height:1.02;font-weight:500;color:${color};letter-spacing:0.005em}
#by{position:absolute;left:66px;font-size:40px;letter-spacing:0.06em;color:${C.red}}
#h{position:absolute;left:0;right:0;bottom:22px;text-align:center;font-size:30px;color:${C.ink};letter-spacing:0.03em}
svg{position:absolute;left:0;top:0}
</style></head><body><div id="c">
<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${FILTER}<g id="sc">${scenes[scene](0,0,'')}</g></svg>
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
    const lay = await p.evaluate((j)=>{
      const t=document.getElementById('t'), by=document.getElementById('by');
      let size=j.size||118; const limit=j.limit||(j.h*0.44);
      for(;size>=60;size-=2){ t.style.fontSize=size+'px'; by.style.top='0px'; const b=t.getBoundingClientRect().bottom; if(b+(j.by?64:0)<=limit) break; }
      const tb=t.getBoundingClientRect().bottom; by.style.top=(tb+12)+'px';
      const top=tb+(j.by?64:0)+16; const bottom=j.h-70; const avail=bottom-top;
      const box = j.scene==='imagination' ? {x0:205,wd:790,y0:0,ht:1010} : {x0:0,wd:1000,y0:0,ht:1000};
      let sc=Math.min(avail/box.ht, (j.w-60)/box.wd);
      const tx=(j.w-box.wd*sc)/2 - box.x0*sc, ty=top - box.y0*sc;
      document.getElementById('sc').setAttribute('transform',`translate(${tx},${ty}) scale(${sc})`);
      return {size,sc:+sc.toFixed(2)};
    }, j);
    console.log(JSON.stringify(lay));
    fs.mkdirSync(path.dirname(path.resolve(j.out)),{recursive:true});
    await p.screenshot({path:j.out,clip:{x:0,y:0,width:j.w,height:j.h}});
    console.log('ok',j.out);
  }
} finally { await browser.close(); }
