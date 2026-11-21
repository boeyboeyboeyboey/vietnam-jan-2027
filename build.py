import json, base64, html, sys, os
pics = json.load(open(sys.argv[1]))
OUTDIR = sys.argv[2]

def url(lid, p):
    for k, v in {'.J': '.jpeg', '.j': '.jpg'}.items():
        if p.endswith(k): p = p[:-2] + v
    if p.startswith('H:'): p = f"hosting/Hosting-{base64.b64encode(('StaySupplyListing:'+lid).encode()).decode()}/original/{p[2:]}"
    elif p.startswith('I:'): p = f"hosting/Hosting-{lid}/original/{p[2:]}"
    elif p.startswith('M:'): p = f"miso/Hosting-{lid}/original/{p[2:]}"
    return "https://a0.muscache.com/im/pictures/" + p

# Hero photos: Unsplash License (free, no attribution required; credited anyway)
HERO = {
 "hcmc": ("https://images.unsplash.com/photo-1673934149508-318260ef31f2", "Anh Phan", "https://unsplash.com/photos/tyMDpHN7BZk"),
 "danang": ("https://images.unsplash.com/photo-1732827503735-511f7ccd187e", "Yash Parashar", "https://unsplash.com/photos/bLn5N9ldqfA"),
}

# id, name, short, dates, nights, checkin, checkout, accent, note, listings
CITIES = [
 ("hcmc", "Ho Chi Minh City", "HCMC", "4–7 Jan 2027", 3, "2027-01-04", "2027-01-07", "#ff9f7a",
  "Ranked best first. All within 2.5 km of Ben Thanh Market, 3+ bathrooms.", [
  ("HCMC1","27990178","Phoenix's 5BR House","District 1 (Da Kao) · 2.0 km","S$813","S$30","5 bedrooms · 5 baths","4.85★ (238) · Superhost",
   ["Most reviewed, consistently good","Every room has its own bathroom + AC","Host fixes problems fast","Free airport pickup"],
   ["5 floors of stairs, no lift","Weak portable AC in living room","Rooster from ~4:30am","Past ant/cockroach reports (one group moved out, Jan 2024)","5 queen beds, so 4 pairs share"]),
  ("HCMC2","27914684","Le's 6BR House","District 1 (Tan Dinh) · 2.2 km","S$493","S$18","6 bedrooms · 6 baths","4.84★ (79)",
   ["6 rooms, each with own bathroom + TV","Daily towel change","79 reviews, mostly 5★"],
   ["Dated","Ants + mould in a bathroom (Nov 2025)","Leaky shower","No real living room","Dim phone photos"]),
  ("HCMC3","965804095820583217","4BR Duplex + Free Pickup","District 3 · 1.0 km","S$1,040","S$39","4 bedrooms · 4 baths","4.91★ (149) · Guest Favourite · Superhost",
   ["Most reviewed this close to centre","Two living areas (one with projector)","Quiet street, café downstairs","Building rooftop pool + gym","Free airport pickup + SIM"],
   ["Pricey","4 beds for 9 (extra mattress on request)","\"A bit dated\" (2024)","Pickup car only fits 4–7","Building gym equipment broken (Jun 2024)"]),
  ("HCMC4","1311605703773163437","Haina's 5BR House","District 3 · 1.6 km","S$753","S$28","5 bedrooms · 6 beds · 4.5 baths","4.88★ (16) · Superhost",
   ["Enough beds for 9 with little sharing","Living room has AC + TV","Rooftop terrace"],
   ["\"Old house, AC doesn't work well\" (Dec 2024)","Alley + stairs","Only 16 reviews"]),
  ("HCMC5","39342498","Rivergate 6BR Apartments","District 4 · 1.2 km","S$840","S$31","6 bedrooms · 4 baths","4.91★ (70)",
   ["64/70 five-star, none below 4★","Building pool + gym","7-Eleven downstairs, near Bui Vien"],
   ["2+ separate apartments, so the group is split","Building notice against short-term rentals","Host replies only 60% of the time","Traffic noise"]),
  ("HCMC6","1697772649812663470","ZenPetal 5BR House","District 4 · 1.9 km","S$572","S$21","5 bedrooms · 5 beds · 5 baths","5.0★ (6) · Guest Favourite · Superhost",
   ["Close to budget","5 bathrooms","Every review 5★","Street food nearby"],
   ["Small rooms in photos","5 beds, so pairs share","Only 6 reviews","One power cut (Jun 2026, fixed fast)"]),
  ("HCMC7","1731138706065239581","Cozy 5BR/5BA House","District 1 · 1.0 km","S$1,094","S$41","5 bedrooms · 8 beds · 5 baths","5.0★ (8) · Guest Favourite · Superhost",
   ["Most beds + baths this close to centre","New, clean","Every review 5★"],
   ["Priciest","Only 8 reviews","Only 1 bathroom shown in photos","No living-room AC seen","Shophouse alley"]),
  ("HCMC8","1483784188953758037","Cau Kho 3BR House","District 1 (Cau Kho) · 2.2 km","S$473","S$18","3 bedrooms · 6 beds · 3 baths","4.68★ (40)",
   ["Cheapest","Living room has AC + TV","Washer in photos","Rooftop","Responsive host"],
   ["Sewage backup + washer flooded ground floor (Oct 2025)","Only 1 of 3 toilets worked for one group (Oct 2025)","Weak shower pressure (Nov 2025)","4 floors of steep, narrow stairs","Some sleep on sofa beds","Alley, Grab can't reach the door"]),
 ]),
 ("danang", "Da Nang", "Da Nang", "7–11 Jan 2027", 4, "2027-01-07", "2027-01-11", "#6fd6d1",
  "Ranked best first. Private pool + central costs about S$26–31 per person per night.", [
  ("DN1","1500369668192839406","Cam On Pool Villa","1.1 km from Han Market","S$923","S$26","4 bedrooms · 5 beds · 4 baths","4.73★ (33) · private pool ~8–10 m",
   ["Biggest private pool","~1 km to Han Market","Free airport pickup"],
   ["No warm water some evenings, few towels/dishes","Construction + karaoke nearby (Jan 2025)","Dining table seats 6","TV/washer not seen in photos"]),
  ("DN2","1598281711142232998","Luxury 4BR Home","1.9 km from Han Market","S$697","S$19","4 bedrooms · 8 beds · 4.5 baths","5.0★ (10) · Guest Favourite · Superhost",
   ["Under budget","All reviews 5★","Washer + dryer","Rooftop"],
   ["No pool","Only 10 reviews","Living room has a portable cooler, not AC","Construction crane nearby"]),
  ("DN3","1499048958220731670","Da Nang Pool Villa (Olivia)","1.8 km from Han Market","S$1,101","S$31","4 bedrooms · 5 beds · 5 baths","4.94★ (100) · Guest Favourite · Superhost",
   ["Best track record","5 bathrooms","8-seat dining","Free airport pickup"],
   ["Pool is a small plunge pool (~3×2 m)","\"5 rooms\" was 4 + curtained rooftop (May 2025)","4 floors of stairs","Market-alley entrance","Weak water pressure"]),
  ("DN4","1119292625144112269","Han Market Indoor-Pool Villa","0.3 km from Han Market","S$1,049","S$29","4 bedrooms · 4 beds · 4 baths","4.77★ (13) · indoor pool",
   ["Best location","Indoor pool works in rain","No complaints in reviews"],
   ["Some photos look AI-generated, ask for real ones","4 beds for 9","Washer not shown"]),
  ("DN5","1173705612210421870","CAFE HOUSE","1.5 km from Han Market","S$670","S$19","5 bedrooms · 5 beds · 4 baths","4.8★ (56)",
   ["Cheapest","5 bedrooms, all queen beds","Washer + dryer"],
   ["No pool","Repeated bad-smell reports","Cockroach (Nov 2025)","Living room has fan only","Dining table seats 6"]),
 ]),
]

CANC = {'1483784188953758037': 'Free cancel until 30 Dec', '27914684': 'No free cancellation', '1697772649812663470': 'Free cancel until 3 Jan', '1311605703773163437': 'Free cancel until 3 Jan', '27990178': 'Free cancel until 30 Dec', '39342498': 'No free cancellation', '965804095820583217': 'Free cancel until 30 Dec', '1731138706065239581': 'Free cancel until 30 Dec', '1500369668192839406': 'Free cancel until 8 Dec', '1499048958220731670': 'Free cancel until 8 Dec', '1119292625144112269': 'Free cancel until 8 Dec', '1598281711142232998': 'Free cancel until 24 Dec', '1173705612210421870': 'Free cancel until 2 Jan'}
WISH = {"1483784188953758037"}
WISH_OUT = {"hcmc": [
 ("Grand Riverside 4BR, District 4","S$585","1232973284686915745","Only 2 bathrooms and 4 beds for 9. Apr 2026: a bathroom unusable + mould. Jun 2026: host charged a guest for a sheet they say they didn't damage."),
 ("The Echo D1 3BR","S$543","1380356239307975966","Only 2 bathrooms and 4 beds for 9. Nov 2025 1★: \"looked NOTHING like the photos\", dirty."),
]}

def esc(s): return html.escape(s, quote=True)

# Single deliberate night look: deep ink background, soft neon accent per city.
CSS = '''
:root{color-scheme:dark;--bg:#0e1116;--panel:#151a22;--ink:#eef1f5;--mut:#9aa4b2;--rule:#252c37;--plus:#8fe3a8;--minus:#ff9b9b}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 "Be Vietnam Pro",system-ui,sans-serif;font-variant-numeric:tabular-nums}
a{color:inherit}
.hero{position:relative;min-height:340px;display:flex;align-items:flex-end;background:var(--bg) center/cover no-repeat;padding:20px max(16px,env(safe-area-inset-left)) 30px}
.hero::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,17,22,.35) 0%,rgba(14,17,22,.55) 45%,var(--bg) 100%)}
.hero .in{position:relative;width:100%;max-width:880px;margin:0 auto}
.top{position:absolute;z-index:1;top:calc(14px + env(safe-area-inset-top));left:max(16px,env(safe-area-inset-left));right:max(16px,env(safe-area-inset-right));max-width:880px;margin:0 auto;display:flex;justify-content:space-between;font-size:.8rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase}
.top a{text-decoration:none;opacity:.85;background:rgba(14,17,22,.45);padding:6px 10px;border-radius:4px;backdrop-filter:blur(6px)}
.top a:hover{opacity:1}
.hero h1{font-size:clamp(2.6rem,9vw,4.8rem);line-height:.95;margin:0 0 10px;font-weight:800;letter-spacing:-.03em;text-shadow:0 2px 24px rgba(0,0,0,.4)}
.hero .dates{font-size:1.1rem;font-weight:600;color:var(--acc)}
.hero .note{margin:8px 0 0;max-width:60ch;color:#d6dbe3}
.wrap{max-width:880px;margin:0 auto;padding:8px max(16px,env(safe-area-inset-left)) 40px}
.opt{background:var(--panel);border:1px solid var(--rule);border-radius:6px;padding:18px;margin:0 0 18px}
.row{display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:start}
.code{font-weight:800;font-size:1.05rem;letter-spacing:.04em;color:var(--bg);background:var(--acc);padding:6px 10px;border-radius:4px;line-height:1.2}
.row h2{margin:0;font-size:1.2rem;line-height:1.25}
.row h2 a{text-decoration:none;border-bottom:1px solid var(--rule)}.row h2 a:hover{border-color:var(--acc)}
.meta{margin:4px 0 0;color:var(--mut);font-size:.88rem}
.price{text-align:right;border-left:2px solid var(--acc);padding-left:14px;min-width:130px}
.price b{display:block;font-size:2.1rem;line-height:1;font-weight:800;color:var(--acc);letter-spacing:-.02em}
.price span{display:block;font-size:.75rem;color:var(--mut);margin-top:4px}
.price i{display:block;font-style:normal;font-size:.85rem;margin-top:4px}
.price em{display:block;font-style:normal;font-size:.75rem;margin-top:4px}.price em.ok{color:var(--plus)}.price em.no{color:var(--minus)}
.strip{display:flex;gap:4px;overflow-x:auto;margin:16px -18px 4px;padding:0 18px;scroll-snap-type:x proximity}
.strip img{height:230px;width:auto;aspect-ratio:3/2;object-fit:cover;display:block;scroll-snap-align:start;background:var(--rule);border-radius:3px}
.count{font-size:.78rem;color:var(--mut);margin:0 0 12px}
.fa{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.fa h3{margin:0 0 6px;font-size:.75rem;letter-spacing:.1em;text-transform:uppercase}
.for h3{color:var(--plus)}.against h3{color:var(--minus)}
ul{margin:0;padding:0;list-style:none}li{padding:4px 0 4px 18px;position:relative;border-top:1px solid var(--rule);font-size:.95rem}
.for li::before{content:"+";position:absolute;left:2px;color:var(--plus);font-weight:800}
.against li::before{content:"−";position:absolute;left:2px;color:var(--minus);font-weight:800}
span.wish{display:inline-block;margin-left:8px;font-size:.7rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--bg);background:var(--acc);padding:2px 7px;border-radius:3px;vertical-align:middle}
span.wish.top{background:var(--ink);color:var(--bg)}
.wl{border:1px dashed var(--rule);border-radius:6px;padding:14px 18px;margin:0 0 18px}.wl h3{margin:0 0 6px;font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}.wl li{border-top:1px solid var(--rule);padding:6px 0;font-size:.92rem}.wl li::before{content:none}.wl b{color:var(--acc)}
footer{color:var(--mut);font-size:.78rem;padding-top:6px}
footer a{color:var(--mut)}
@media (max-width:620px){.row{grid-template-columns:auto 1fr}.price{grid-column:1/-1;text-align:left;border-left:0;border-top:1px solid var(--rule);padding:10px 0 0;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}.price span,.price i{margin:0}.strip img{height:180px}.fa{grid-template-columns:1fr}.hero{min-height:300px}}
.home{display:grid;grid-template-columns:1fr 1fr;min-height:100vh}
.home a{position:relative;text-decoration:none;padding:40px max(20px,env(safe-area-inset-left));display:flex;flex-direction:column;justify-content:flex-end;gap:6px;background:var(--bg) center/cover no-repeat;overflow:hidden}
.home a::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,17,22,.2),rgba(14,17,22,.85));transition:background .2s}
.home a:hover::before,.home a:focus-visible::before{background:linear-gradient(180deg,rgba(14,17,22,.05),rgba(14,17,22,.75))}
.home a>*{position:relative}
.home h2{font-size:clamp(2.4rem,7vw,4.4rem);line-height:.95;margin:0;font-weight:800;letter-spacing:-.03em}
.home p{margin:0;font-size:1.05rem;font-weight:600;color:var(--acc)}
.home small{color:#d6dbe3;font-size:.95rem}
.home .t{position:fixed;top:0;left:0;right:0;z-index:2;text-align:center;padding:calc(14px + env(safe-area-inset-top)) 0 0;font-weight:700;letter-spacing:.1em;text-transform:uppercase;font-size:.78rem;color:#eef1f5;text-shadow:0 1px 8px rgba(0,0,0,.6)}
.home .cr{position:fixed;bottom:8px;right:12px;z-index:2;font-size:.7rem;color:#c9ced6;text-shadow:0 1px 6px rgba(0,0,0,.7)}
@media (max-width:620px){.home{grid-template-columns:1fr}.home a{min-height:50vh}}
'''

HEAD = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;800&display=swap">
<style>{css}</style></head>'''

TOPTAG = ' <span class="wish top">Top pick</span>'
WISHTAG = ' <span class="wish">On your wishlist</span>'

def wishout(cid, ci, co):
    rows = WISH_OUT.get(cid)
    if not rows: return ""
    li = "".join(f'<li><a href="https://www.airbnb.com.sg/rooms/{lid}?check_in={ci}&check_out={co}&adults=9" target="_blank" rel="noopener">{esc(n)}</a> <b>{p}</b> · {esc(why)}</li>' for n,p,lid,why in rows)
    return f'<section class="wl"><h3>Also on your wishlist, not included</h3><ul>{li}</ul></section>'

def price_from(items): return min(int(i[5][2:]) for i in items)

for idx, (cid, cname, short, dates, nights, ci, co, acc, note, items) in enumerate(CITIES):
    other = CITIES[1-idx]
    himg, hby, hlink = HERO[cid]
    opts = []
    for code, lid, name, loc, tot, pp, rooms, rating, pro, con in items:
        link = f"https://www.airbnb.com.sg/rooms/{lid}?check_in={ci}&check_out={co}&adults=9"
        imgs = ''.join(f'<a href="{esc(url(lid,p))}?im_w=1200" target="_blank" rel="noopener"><img src="{esc(url(lid,p))}?im_w=480" width="345" height="230" loading="lazy" alt="{code} photo {i+1}"></a>' for i,p in enumerate(pics[lid]))
        opts.append(f'''<article class="opt" id="{code.lower()}">
<div class="row"><span class="code">{code}</span>
<div><h2><a href="{link}" target="_blank" rel="noopener">{esc(name)} ↗</a>{WISHTAG if lid in WISH else ""}{TOPTAG if code.endswith("1") and not code[-2].isdigit() else ""}</h2><p class="meta">{esc(loc)}<br>{esc(rooms)} · {esc(rating)}</p></div>
<div class="price"><b>{pp}</b><span>per person / night</span><i>{tot} total · {nights} nights</i><em class="{"no" if CANC[lid].startswith("No") else "ok"}">{CANC[lid]}</em></div></div>
<div class="strip">{imgs}</div><p class="count">{len(pics[lid])} photos · swipe →</p>
<div class="fa"><div class="for"><h3>For</h3><ul>{''.join(f"<li>{esc(x)}</li>" for x in pro)}</ul></div>
<div class="against"><h3>Against</h3><ul>{''.join(f"<li>{esc(x)}</li>" for x in con)}</ul></div></div>
</article>''')
    page = HEAD.format(title=f"{cname} · Jan 2027 stays", css=CSS) + f'''<body style="--acc:{acc}">
<header class="hero" style="background-image:url('{himg}?auto=format&fit=crop&w=1800&q=70')">
<div class="top"><a href="./">← All cities</a><a href="{other[0]}.html">{esc(other[2])} →</a></div><div class="in">
<h1>{esc(cname)}</h1><div class="dates">{dates} · {nights} nights · 9 people</div><p class="note">{esc(note)}</p>
</div></header>
<main class="wrap">{''.join(opts)}{wishout(cid,ci,co)}
<footer>Airbnb totals before tax. Prices and availability checked 22 Nov 2026. Tap a photo for full size, a title to open Airbnb. Header photo: <a href="{hlink}" target="_blank" rel="noopener">{hby} / Unsplash</a>.</footer></main></body></html>'''
    open(os.path.join(OUTDIR, f"{cid}.html"), 'w').write(page)

tiles = ''.join(f'''<a href="{c[0]}.html" style="--acc:{c[7]};background-image:url('{HERO[c[0]][0]}?auto=format&fit=crop&w=1200&q=70')"><h2>{esc(c[1])}</h2><p>{c[3]} · {c[4]} nights</p><small>{len(c[9])} options · from S${price_from(c[9])} per person / night</small></a>''' for c in CITIES)
credit = ' · '.join(f'<a href="{HERO[c[0]][2]}" target="_blank" rel="noopener">{HERO[c[0]][1]}</a>' for c in CITIES)
open(os.path.join(OUTDIR, "index.html"), 'w').write(HEAD.format(title="Vietnam Jan 2027 · stays", css=CSS) + f'<body><div class="home"><div class="t">Vietnam · Jan 2027 · 9 people</div>{tiles}</div><div class="cr">Photos: {credit} / Unsplash</div></body></html>')
print("ok", sum(len(pics[i[1]]) for c in CITIES for i in c[9]))
