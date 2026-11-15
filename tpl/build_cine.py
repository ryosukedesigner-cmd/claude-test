"""Construit un modèle « cinématique » (v105) à partir du modèle v104 d'un métier.

Garde intacts : <head> (SEO, JSON-LD), la couche de vente (#bbr, #bbs, scripts de suivi),
et tous les crochets utilisés par pipeline-cron :
  - <span class="mono" data-slot="logo">  (logo)
  - <p class="lead">                       (accroche personnalisée)
  - premier <div class="cta">              (note Google insérée juste après)
  - section #realisations hidden + figures g1 g2 g4 + <div class="gal rv">
  - <a href="#zone">Zone</a> dans la nav
  - {{SEO_CMP}}, data-phone, data-track, .mbar, .no-phone
Usage : python3 build_cine.py <v104.html> <config.json> <sortie.html>
"""
import json, re, sys


def grab(h, pat, flags=re.S):
    m = re.search(pat, h, flags)
    if not m:
        raise SystemExit(f"motif introuvable : {pat[:60]}")
    return m.group(1) if m.groups() else m.group(0)


def build(v104: str, cfg: dict) -> str:
    A = cfg["assets"]  # URL de base des médias du métier, avec / final
    head_end = v104.index("</head>")
    body_start = v104.index("<body")
    body_tag_end = v104.index(">", body_start) + 1
    sales_start = v104.index('<div id="bbr"')

    site = v104[body_tag_end:sales_start]

    header = grab(site, r'(<header class="hd" id="hd">.*?</header>)')
    eyebrow = grab(site, r'<section class="hero">.*?<span class="eyebrow">(.*?)</span>')
    h1 = grab(site, r"<h1>(.*?)</h1>")
    lead = grab(site, r'(<p class="lead">.*?</p>)')
    cta = grab(site, r'<div class="hero-t">.*?(<div class="cta">.*?</div>)')
    trust = re.findall(r'<div class="trust">(.*?)</div>\s*</div>\s*</section>', site, re.S)[0]
    trust_items = re.findall(r"<span><b>(.*?)</b>(.*?)</span>", trust)
    services = grab(site, r'(<section class="sec" id="services">.*?</section>)')
    serv_h = grab(services, r'(<div class="sec-h rv">.*?</div>\s*<p>.*?</p></div>)')
    cards = re.findall(r'<article class="card rv"><div class="n">(\d+)</div><h3>(.*?)</h3><p>(.*?)</p></article>', services)
    split = grab(site, r'<div class="wrap split">(.*?)</div>\s*</section>')
    split_txt = grab(split, r'<div class="rv">(<span class="eyebrow">.*?</p>)</div>')
    ticks = grab(split, r'(<ul class="ticks">.*?</ul>)')
    real = grab(site, r'(<section class="sec dark" id="realisations" hidden>.*?</section>)')
    steps = re.findall(r'<div class="step rv"><h3>(.*?)</h3><p>(.*?)</p></div>', site)
    steps_h = grab(site, r'<section class="sec">\s*<div class="wrap">\s*<div class="sec-h rv"><div>(<span class="eyebrow">Comment.*?</h2>)</div></div>')
    zone_txt = grab(site, r'<div class="zone-c rv"><div>(.*?)</div>')
    zone_cta = grab(site, r'<div class="zone-c rv">.*?(<div class="cta">.*?</div>)')
    faq = grab(site, r'(<section class="sec" id="faq".*?</section>)')
    final_txt = grab(site, r'<div class="final-c rv">\s*<div>(.*?)</div>')
    final_cta = grab(site, r'<div class="final-c rv">.*?(<div class="cta">.*?</div>)')
    footer = grab(site, r'(<footer class="ft">.*?</footer>)')
    mbar = grab(site, r'(<div class="mbar">.*?</div>)')

    s = cfg["story"]
    lines = "".join(
        f'<p class="cx-l" style="--a:{0.12 + i * 0.2:.2f}">{t}</p>' for i, t in enumerate(s["lines"])
    )
    lines += f'<p class="cx-l cx-l-end" style="--a:{0.12 + len(s["lines"]) * 0.2:.2f}">{s["end"]}</p>'

    marquee_items = "".join(f"<span><b>{b}</b> {t}</span><i>✦</i>" for b, t in trust_items)

    cards_html = "".join(
        f'<article class="cx-card cv" style="--d:{i % 3 * 90}ms"><span class="cx-n">{n}</span><h3>{t}</h3><p>{p}</p></article>'
        for i, (n, t, p) in enumerate(cards)
    )
    steps_html = "".join(
        f'<li class="cv" style="--d:{i * 120}ms"><span>0{i + 1}</span><div><h3>{t}</h3><p>{p}</p></div></li>'
        for i, (t, p) in enumerate(steps)
    )
    ba = cfg["ba"]

    hero_m = A + cfg["img"]["hero_m"]
    hero_d = A + cfg["img"]["hero_d"]
    video = (A + cfg["video"]) if cfg.get("video") else ""

    body = f"""
{header}
<main id="top">
<section class="cx-hero" data-cx="out">
 <div class="cx-media">
  <picture><source media="(min-width:821px)" srcset="{hero_d}"><img class="cx-poster" src="{hero_m}" alt="" fetchpriority="high" decoding="async"></picture>
  {f'<video class="cx-vid" muted loop playsinline preload="none" aria-hidden="true" data-src="{video}"></video>' if video else ''}
 </div>
 <div class="cx-shade"></div>
 <div class="wrap cx-hero-c">
  <span class="cx-kick">{eyebrow}</span>
  <h1>{h1}</h1>
  {lead}
  {cta}
 </div>
 <a class="cx-cue" href="#cx-story" aria-label="Découvrir"><span></span></a>
</section>
<div class="cx-marq" aria-hidden="true"><div>{marquee_items}{marquee_items}</div></div>
<section class="cx-story" id="cx-story" data-cx="pin">
 <div class="cx-pin">
  <img class="cx-bg" src="{A + cfg['img']['story']}" alt="" loading="lazy" decoding="async">
  <div class="cx-veil"></div>
  <div class="wrap cx-lines"><span class="cx-eye">{s['eyebrow']}</span>{lines}</div>
  <div class="cx-bar"><i></i></div>
 </div>
</section>
<section class="sec cx-gest" data-cx="in">
 <div class="wrap cx-gest-c">
  <figure class="cx-reveal"><img src="{A + cfg['img']['gest']}" alt="{cfg['alt']['gest']}" loading="lazy" decoding="async"></figure>
  <div><div class="cv">{split_txt}</div><div class="cv" style="--d:120ms">{ticks}</div></div>
 </div>
</section>
<section class="cx-ba" data-cx="pin">
 <div class="cx-pin cx-ba-pin">
  <div class="wrap cx-ba-h"><span class="eyebrow">{ba['eyebrow']}</span><h2>{ba['title']}</h2></div>
  <div class="cx-ba-f">
   <img src="{A + cfg['img']['before']}" alt="{ba['alt_before']}" loading="lazy" decoding="async">
   <img class="cx-after" src="{A + cfg['img']['after']}" alt="{ba['alt_after']}" loading="lazy" decoding="async">
   <span class="cx-tag cx-tag-b">Avant</span><span class="cx-tag cx-tag-a">Après</span>
   <i class="cx-handle"></i>
  </div>
  <p class="cx-ba-c">{ba['caption']}</p>
 </div>
</section>
<section class="sec cx-serv" id="services">
 <div class="wrap">
  {serv_h.replace('class="sec-h rv"', 'class="sec-h cv"')}
  <div class="cx-cards">{cards_html}</div>
 </div>
</section>
{real}
<section class="sec cx-steps" data-cx="in">
 <div class="wrap cx-steps-c">
  <div class="cv">{steps_h}</div>
  <ol class="cx-tl"><i class="cx-tl-line"></i>{steps_html}</ol>
 </div>
</section>
<section class="cx-zone" id="zone" data-cx="in">
 <img class="cx-zbg" src="{A + cfg['img']['zone']}" alt="" loading="lazy" decoding="async">
 <div class="cx-zveil"></div>
 <div class="wrap cx-zone-c"><div class="cv">{zone_txt}{zone_cta}</div></div>
</section>
{faq}
<section class="cx-final" id="contact" data-cx="in">
 <img class="cx-fbg" src="{hero_d}" alt="" loading="lazy" decoding="async">
 <div class="cx-fveil"></div>
 <div class="wrap cx-final-c cv"><div>{final_txt}</div>{final_cta}</div>
</section>
</main>
{footer}
{mbar}
"""

    body = re.sub(r" ([?!:;»])", "\u00a0\\1", body)
    body = body.replace("« ", "«\u00a0")
    css = CSS
    js = JS
    head = v104[:head_end]
    head = head.replace(
        "family=Inter+Tight:wght@500;600;700&",
        "family=Inter+Tight:wght@500;600;700&family=Fraunces:ital,opsz,wght@1,9..144,500&",
    )
    head += f'<link rel="preload" as="image" href="{hero_m}" media="(max-width:820px)" fetchpriority="high">'
    head += f'<link rel="preload" as="image" href="{hero_d}" media="(min-width:821px)">'
    head += f'<style id="cx-css">{css}</style>'
    out = head + v104[head_end:body_tag_end].replace("<body>", '<body class="cx">') + body + v104[sales_start:]
    out = out.replace("</body>", f"<script data-cx=\"v1\">{js}</script></body>")
    return out


CSS = r"""
:root{--cx-dark:#0d0f12;--cx-cream:#f4f1ea}
.cx{background:var(--bg)}
.cx .rv{opacity:1;transform:none}
/* en-tête transparent sur la scène d'ouverture */
.cx .hd{position:fixed;left:0;right:0;background:transparent;backdrop-filter:none;-webkit-backdrop-filter:none;color:#fff;transition:background .35s,color .35s,border-color .35s}
.cx .hd .brand small{color:rgba(255,255,255,.75)}
.cx .hd .nav a:not(.btn){color:rgba(255,255,255,.85)}
.cx .hd.sc{background:rgba(13,15,18,.72);backdrop-filter:saturate(1.4) blur(16px);-webkit-backdrop-filter:saturate(1.4) blur(16px);border-color:rgba(255,255,255,.08)}
.cx .hd .mono{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.35);backdrop-filter:blur(6px)}
.cx .hd .brand .logo{background:#fff;border-radius:10px;padding:3px}
[data-cx]{--p:1}
/* scène 1 */
.cx-hero{position:relative;height:100svh;min-height:600px;overflow:hidden;background:var(--cx-dark);color:#fff;display:flex;align-items:flex-end}
.cx-media{position:absolute;inset:0;transform:scale(calc(1.02 + var(--p)*.16)) translateY(calc(var(--p)*6%));will-change:transform}
.cx-media img,.cx-media video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.cx-media video{opacity:0;transition:opacity 1.2s ease}.cx-media video.on{opacity:1}
.cx-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,9,11,.55) 0%,rgba(8,9,11,0) 26%,rgba(8,9,11,.15) 48%,rgba(8,9,11,.88) 100%);opacity:calc(.9 + var(--p)*.3)}
.cx-hero-c{position:relative;z-index:2;width:100%;padding-bottom:max(54px,8svh);transform:translateY(calc(var(--p)*-90px));opacity:calc(1 - var(--p)*1.5)}
.cx-kick{display:inline-flex;align-items:center;gap:10px;font-size:12.5px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.82)}
.cx-kick:before{content:"";width:26px;height:1px;background:var(--acc-hi,#fff)}
.cx-hero h1{font-size:clamp(46px,7.4vw,104px);line-height:.98;letter-spacing:-.04em;margin:16px 0 18px;max-width:900px;text-wrap:balance}
.cx-hero h1 em{font-family:Fraunces,Georgia,serif;font-style:italic;font-weight:500;letter-spacing:-.02em;color:var(--acc-hi,#fff)}
.cx-hero .lead{color:rgba(255,255,255,.86);font-size:18px;max-width:580px}
.cx-hero .cta{margin-top:28px}
.cx-hero .btn-s{background:rgba(255,255,255,.12);color:#fff;border-color:rgba(255,255,255,.35);backdrop-filter:blur(8px)}
.cx-hero .bbnote{color:rgba(255,255,255,.9)}
.cx-cue{position:absolute;right:24px;bottom:28px;z-index:3;width:26px;height:42px;border:1.5px solid rgba(255,255,255,.6);border-radius:14px;opacity:calc(1 - var(--p)*4)}
.cx-cue span{position:absolute;left:50%;top:8px;width:3px;height:8px;margin-left:-1.5px;border-radius:2px;background:#fff;animation:cxcue 1.8s infinite}
@keyframes cxcue{0%{transform:translateY(0);opacity:1}80%{transform:translateY(14px);opacity:0}100%{opacity:0}}
.cx-hero-c>*{animation:cxin 1.1s cubic-bezier(.2,.7,.1,1) both}
.cx-hero-c>*:nth-child(2){animation-delay:.12s}.cx-hero-c>*:nth-child(3){animation-delay:.24s}.cx-hero-c>*:nth-child(4){animation-delay:.36s}.cx-hero-c>*:nth-child(5){animation-delay:.48s}
@keyframes cxin{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:none}}
.cx-media img.cx-poster{animation:cxzoom 2.4s cubic-bezier(.2,.7,.1,1) both}
@keyframes cxzoom{from{transform:scale(1.12);filter:brightness(.6)}to{transform:none;filter:none}}
.cx-media:not(:has(video)) img.cx-poster{animation:cxzoom 2.4s cubic-bezier(.2,.7,.1,1) both,cxkb 24s ease-in-out 2.4s infinite alternate}
@keyframes cxkb{from{transform:none}to{transform:scale(1.09) translate(-1.5%,-1%)}}
/* bandeau défilant */
.cx-marq{background:var(--cx-dark);color:#fff;overflow:hidden;border-top:1px solid rgba(255,255,255,.08);padding:16px 0}
.cx-marq>div{display:flex;gap:28px;width:max-content;animation:cxmarq 34s linear infinite;white-space:nowrap;font-size:14.5px;color:rgba(255,255,255,.72)}
.cx-marq b{color:#fff;font-weight:600}.cx-marq i{font-style:normal;color:var(--acc-hi,#fff)}
@keyframes cxmarq{to{transform:translateX(-50%)}}
/* scène 2 : récit épinglé */
.cx-story{height:300svh;background:var(--cx-dark);position:relative}
.cx-pin{position:sticky;top:0;height:100svh;overflow:hidden}
.cx-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scale(calc(1.18 - var(--p)*.16));filter:saturate(calc(.7 + var(--p)*.4))}
.cx-veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,9,11,.35),rgba(8,9,11,.82))}
.cx-lines{position:relative;z-index:2;height:100%;display:flex;flex-direction:column;justify-content:center;gap:6px;color:#fff}
.cx-eye{font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.65);margin-bottom:18px}
.cx-l{--k:clamp(0,calc((var(--p) - var(--a))*7),1);font:700 clamp(34px,5.4vw,72px)/1.04 "Inter Tight",sans-serif;letter-spacing:-.035em;opacity:calc(.08 + var(--k)*.92);transform:translateY(calc((1 - var(--k))*26px));filter:blur(calc((1 - var(--k))*6px))}
.cx-l-end{font:italic 500 clamp(24px,3.4vw,40px)/1.2 Fraunces,Georgia,serif;letter-spacing:-.01em;color:var(--acc-hi,#fff);margin-top:22px;max-width:760px}
.cx-bar{position:absolute;left:24px;right:24px;bottom:30px;height:2px;background:rgba(255,255,255,.15);z-index:2}
.cx-bar i{display:block;height:100%;background:var(--acc-hi,#fff);transform-origin:left;transform:scaleX(var(--p))}
/* scène 3 : le geste */
.cx-gest-c{display:grid;grid-template-columns:1fr 1fr;gap:70px;align-items:center}
.cx-reveal{border-radius:28px;overflow:hidden;aspect-ratio:4/5;clip-path:inset(calc((1 - clamp(0,var(--p)*2.2,1))*14%) round 28px)}
.cx-reveal img{width:100%;height:118%;object-fit:cover;transform:translateY(calc(var(--p)*-14%))}
.cx-gest h2{font-size:clamp(32px,3.8vw,48px);margin:14px 0 18px;text-wrap:balance}
.cx-gest p{color:var(--ink2);font-size:18px;margin-bottom:30px}
/* scène 4 : avant / après */
.cx-ba{height:260svh;background:var(--cx-cream)}
.cx-ba-pin{display:flex;flex-direction:column;justify-content:center;gap:22px;padding:84px 0 30px}
.cx-ba-h h2{font-size:clamp(30px,4vw,52px);margin-top:12px;text-wrap:balance}
.cx-ba-f{--q:clamp(0,calc((var(--p) - .12)*1.45),1);position:relative;margin:0 auto;width:min(calc(100% - 40px),560px,calc((100svh - 300px)*.8));aspect-ratio:4/5;border-radius:24px;overflow:hidden;box-shadow:0 50px 90px -50px rgba(20,23,28,.55);touch-action:pan-y}
.cx-ba-f img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.cx-after{clip-path:inset(0 calc((1 - var(--q))*100%) 0 0)}
.cx-handle{position:absolute;top:0;bottom:0;left:calc(var(--q)*100%);width:2px;margin-left:-1px;background:#fff;box-shadow:0 0 18px rgba(0,0,0,.4)}
.cx-handle:after{content:"‹ ›";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:44px;height:44px;border-radius:50%;background:#fff;color:var(--ink);display:grid;place-items:center;font:700 16px "Inter Tight",sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.25)}
.cx-tag{position:absolute;top:14px;padding:6px 12px;border-radius:999px;font-size:12.5px;font-weight:600;letter-spacing:.04em;background:rgba(13,15,18,.7);color:#fff;backdrop-filter:blur(6px)}
.cx-tag-b{right:14px;opacity:calc(1 - var(--q)*1.4)}.cx-tag-a{left:14px;opacity:calc(var(--q)*1.4 - .2)}
.cx-ba-c{text-align:center;font-size:13px;color:var(--ink3)}
/* services */
.cx-serv{background:var(--bg)}
.cx-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.cx-card{position:relative;padding:34px 30px 30px;border-radius:24px;background:var(--bg2);overflow:hidden;transition:transform .3s,box-shadow .3s}
.cx-card:hover{transform:translateY(-4px);box-shadow:0 30px 60px -36px rgba(20,23,28,.4)}
.cx-n{display:block;font:700 64px/1 "Inter Tight",sans-serif;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1.5px var(--acc);margin-bottom:26px}
.cx-card h3{font-size:22px;margin-bottom:8px}.cx-card p{color:var(--ink2);font-size:15.5px}
/* étapes */
.cx-steps-c{display:grid;grid-template-columns:.9fr 1.1fr;gap:70px}
.cx-steps h2{font-size:clamp(32px,3.8vw,48px);margin-top:14px;text-wrap:balance}
.cx-tl{position:relative;list-style:none;display:grid;gap:34px;padding-left:46px}
.cx-tl:before{content:"";position:absolute;left:14px;top:6px;bottom:6px;width:2px;background:var(--line)}
.cx-tl-line{position:absolute;left:14px;top:6px;bottom:6px;width:2px;background:var(--acc);transform-origin:top;transform:scaleY(clamp(0,calc(var(--p)*1.7 - .25),1))}
.cx-tl li{position:relative}
.cx-tl li>span{position:absolute;left:-46px;top:0;width:30px;height:30px;border-radius:50%;background:var(--bg);border:2px solid var(--acc);color:var(--acc-ink);display:grid;place-items:center;font:700 11px "Inter Tight",sans-serif}
.cx-tl h3{font-size:22px;margin-bottom:6px}.cx-tl p{color:var(--ink2)}
/* zone */
.cx-zone{position:relative;overflow:hidden;color:#fff;min-height:88svh;display:flex;align-items:flex-end;background:var(--cx-dark)}
.cx-zbg{position:absolute;inset:-12% 0;width:100%;height:124%;object-fit:cover;transform:translateY(calc((var(--p) - .5)*-14%))}
.cx-zveil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,9,11,.1),rgba(8,9,11,.82))}
.cx-zone-c{position:relative;z-index:2;padding-bottom:70px;padding-top:120px}
.cx-zone .eyebrow{color:#fff}.cx-zone .eyebrow:before{background:var(--acc-hi,#fff)}
.cx-zone h2{font-size:clamp(34px,4.6vw,60px);margin:14px 0 14px;max-width:760px;text-wrap:balance}
.cx-zone p{color:rgba(255,255,255,.82);max-width:520px;font-size:18px}
.cx-zone .cta{margin-top:26px}
/* final */
.cx-final{position:relative;overflow:hidden;color:#fff;background:var(--cx-dark);padding:140px 0 120px}
.cx-fbg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scale(calc(1.15 - var(--p)*.15));opacity:.55}
.cx-fveil{position:absolute;inset:0;background:radial-gradient(ellipse at 30% 60%,rgba(8,9,11,.4),rgba(8,9,11,.9))}
.cx-final-c{position:relative;z-index:2;display:grid;grid-template-columns:1.3fr 1fr;gap:40px;align-items:end}
.cx-final h2{font-size:clamp(36px,5vw,68px);text-wrap:balance}
.cx-final p{color:rgba(255,255,255,.78);margin-top:16px;font-size:18px}
.cx-final .cta{justify-content:flex-end}
.cx-final .btn-s{background:transparent;color:#fff;border-color:rgba(255,255,255,.4)}
.cx .ft{padding-top:34px}
/* apparitions */
.cv{opacity:0;transform:translateY(34px);transition:opacity .9s cubic-bezier(.2,.7,.1,1) var(--d,0ms),transform .9s cubic-bezier(.2,.7,.1,1) var(--d,0ms)}
.cv.in{opacity:1;transform:none}
html:not(.cx-js) .cv{opacity:1;transform:none}
@media (max-width:980px){
 .cx-gest-c,.cx-steps-c,.cx-final-c{grid-template-columns:1fr;gap:40px}
 .cx-cards{grid-template-columns:1fr 1fr}
 .cx-final .cta{justify-content:flex-start}
}
@media (max-width:640px){
 .cx-hero{min-height:560px}
 .cx-hero h1{font-size:clamp(42px,12.5vw,58px);margin:14px 0 14px}
 .cx-hero .lead{font-size:16px}
 .cx-hero-c{padding-bottom:calc(118px + env(safe-area-inset-bottom))}
 .cx-hero .cta{gap:10px;margin-top:22px}.cx-hero .cta .btn{height:50px}
 .cx-hero .cta .btn-s{display:inline-flex}
 .cx-cue{display:none}
 .cx-story{height:260svh}
 .cx-l{font-size:clamp(32px,10vw,44px)}
 .cx-l-end{font-size:23px}
 .cx-reveal{aspect-ratio:4/5;margin:0 -4px}
 .cx-ba{height:230svh}
 .cx-ba-pin{padding-top:76px;gap:18px}
 .cx-ba-f{width:min(calc(100% - 32px),calc((100svh - 260px)*.8))}
 .cx-cards{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:12px;margin:0 -20px;padding:4px 20px 18px;scrollbar-width:none}
 .cx-cards::-webkit-scrollbar{display:none}
 .cx-card{flex:0 0 78%;scroll-snap-align:center;padding:28px 24px}
 .cx-n{font-size:52px;margin-bottom:18px}
 .cx-zone{min-height:78svh}
 .cx-final{padding:100px 0 90px}
}
@media (prefers-reduced-motion:reduce){
 [data-cx]{--p:1!important}
 .cx-story,.cx-ba{height:auto}.cx-pin{position:relative}
 .cx-marq>div,.cx-hero-c>*,.cx-media img.cx-poster,.cx-media:not(:has(video)) img.cx-poster,.cx-cue span{animation:none}
 .cv{opacity:1;transform:none;transition:none}
}
"""

JS = r"""
(function(){var d=document,R=matchMedia('(prefers-reduced-motion: reduce)').matches;d.documentElement.classList.add('cx-js');
var S=[].slice.call(d.querySelectorAll('[data-cx]')),vh=innerHeight,q=0;
function c(x){return x<0?0:x>1?1:x}
function t(){q=0;for(var i=0;i<S.length;i++){var e=S[i],r=e.getBoundingClientRect(),m=e.getAttribute('data-cx'),p;
 if(r.bottom<-vh||r.top>vh*2)continue;
 if(m==='pin')p=c(-r.top/Math.max(1,e.offsetHeight-vh));else if(m==='out')p=c(-r.top/Math.max(1,r.height));else p=c((vh-r.top)/(vh+r.height));
 e.style.setProperty('--p',p.toFixed(4))}}
function k(){if(!q){q=1;requestAnimationFrame(t)}}
if(!R){addEventListener('scroll',k,{passive:true});addEventListener('resize',function(){vh=innerHeight;k()});t()}
var io='IntersectionObserver'in window?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -10% 0px'}):null;
[].forEach.call(d.querySelectorAll('.cv'),function(e){io?io.observe(e):e.classList.add('in')});
var v=d.querySelector('.cx-vid'),cn=navigator.connection;
if(v&&!R&&innerWidth<=820&&!(cn&&(cn.saveData||/2g/.test(cn.effectiveType||'')))){addEventListener('load',function(){setTimeout(function(){v.src=v.getAttribute('data-src');v.addEventListener('playing',function(){v.classList.add('on')},{once:true});var pr=v.play();pr&&pr.catch&&pr.catch(function(){})},600)});
 if(io){new IntersectionObserver(function(es){es.forEach(function(e){if(!v.src)return;e.isIntersecting?v.play().catch(function(){}):v.pause()})}).observe(v)}}
var f=d.querySelector('.cx-ba-f');if(f){var drag=function(ev){var r=f.getBoundingClientRect(),x=(ev.touches?ev.touches[0].clientX:ev.clientX);f.style.setProperty('--q',c((x-r.left)/r.width).toFixed(3))};f.addEventListener('pointerdown',function(e){drag(e);f.setPointerCapture&&f.setPointerCapture(e.pointerId);f.onpointermove=drag});f.addEventListener('pointerup',function(){f.onpointermove=null})}
})();
"""

if __name__ == "__main__":
    v104 = open(sys.argv[1]).read()
    cfg = json.load(open(sys.argv[2]))
    open(sys.argv[3], "w").write(build(v104, cfg))
    print("ok")
