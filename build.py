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

# id, name, short, dates, nights, checkin, checkout, theme colour, note, listings
CITIES = [
 ("hcmc", "Ho Chi Minh City", "HCMC", "4–7 Jan 2027", 3, "2027-01-04", "2027-01-07", "#b4361f",
  "No private-pool villa near D1 at this budget. The nearest are 7–8 km out.", [
  ("S1","27990178","Phoenix's 5BR House","D1 (Da Kao) · 2.0 km","S$814","S$30","5 bedrooms · 5 baths","4.85★ (238) · Superhost",
   ["Most reviewed, consistently good","Every room has its own bathroom + AC","Host fixes problems fast","Free airport pickup"],
   ["5 floors of stairs, no lift","Weak portable AC in living room","Rooster from ~4:30am","Past ant/cockroach reports (one group moved out, Jan 2024)","5 queen beds, so 4 pairs share"]),
  ("S2","27914684","Le's 6BR House","D1 (Tan Dinh) · 2.2 km","S$493","S$18","6 bedrooms · 6 baths","4.84★ (79)",
   ["Only pick under budget","6 rooms, each with own bathroom + TV","Daily towel change"],
   ["Dated","Ants + mould in a bathroom (Nov 2025)","Leaky shower","No real living room","Dim phone photos"]),
  ("S3","1311605703773163437","Haina's 5BR House","D3 · 1.6 km","S$753","S$28","5 bedrooms · 6 beds · 4.5 baths","4.88★ (16) · Superhost",
   ["Enough beds for 9 with little sharing","Living room has AC + TV","Rooftop terrace"],
   ["\"Old house, AC doesn't work well\" (Dec 2024)","Alley + stairs","Only 16 reviews"]),
  ("S4","39342498","Rivergate 6BR Apartments","D4 · 1.2 km","S$841","S$31","6 bedrooms · 4 baths","4.91★ (70)",
   ["64/70 five-star, none below 4★","Building pool + gym","7-Eleven downstairs, near Bui Vien"],
   ["2+ separate apartments, so the group is split","Building notice against short-term rentals","Host replies only 60% of the time","Traffic noise"]),
 ]),
 ("danang", "Da Nang", "Da Nang", "7–11 Jan 2027", 4, "2027-01-07", "2027-01-11", "#0d6f8c",
  "Private pool + central is possible here, at about S$26–31 per person per night.", [
  ("D1","1500369668192839406","Cam On Pool Villa","1.1 km from Han Market","S$925","S$26","4 bedrooms · 5 beds · 4 baths","4.73★ (33) · private pool ~8–10 m",
   ["Biggest private pool","~1 km to Han Market","Free airport pickup"],
   ["No warm water some evenings, few towels/dishes","Construction + karaoke nearby (Jan 2025)","Dining table seats 6","TV/washer not seen in photos"]),
  ("D2","1499048958220731670","Da Nang Pool Villa (Olivia)","1.8 km from Han Market","S$1,102","S$31","4 bedrooms · 5 beds · 5 baths","4.94★ (100) · Guest Favourite · Superhost",
   ["Best track record","5 bathrooms","8-seat dining","Free airport pickup"],
   ["Pool is a small plunge pool (~3×2 m)","\"5 rooms\" was 4 + curtained rooftop (May 2025)","4 floors of stairs","Market-alley entrance","Weak water pressure"]),
  ("D3","1119292625144112269","Han Market Indoor-Pool Villa","0.3 km from Han Market","S$1,050","S$29","4 bedrooms · 4 beds · 4 baths","4.77★ (13) · indoor pool",
   ["Best location","Indoor pool works in rain","No complaints in reviews"],
   ["Some photos look AI-generated, ask for real ones","4 beds for 9","Washer not shown"]),
  ("D4","1598281711142232998","Luxury 4BR Home","1.9 km from Han Market","S$698","S$19","4 bedrooms · 8 beds · 4.5 baths","5.0★ (10) · Guest Favourite · Superhost",
   ["Under budget","All reviews 5★","Washer + dryer","Rooftop"],
   ["No pool","Only 10 reviews","Living room has a portable cooler, not AC","Construction crane nearby"]),
  ("D5","1173705612210421870","CAFE HOUSE","1.5 km from Han Market","S$671","S$19","5 bedrooms · 5 beds · 4 baths","4.8★ (56)",
   ["Cheapest","5 bedrooms, all queen beds","Washer + dryer"],
   ["No pool","Repeated bad-smell reports","Cockroach (Nov 2025)","Living room has fan only","Dining table seats 6"]),
 ]),
]

def esc(s): return html.escape(s, quote=True)

CSS = '''
:root{--paper:#f4f2ee;--ink:#1b1a18;--mut:#6b6760;--rule:#d9d4cc;--plus:#2f7a3f;--minus:#b4361f;--surface:#fffdf9}
@media (prefers-color-scheme:dark){:root{--paper:#151413;--ink:#efece6;--mut:#a39d93;--rule:#33302c;--plus:#7cc98a;--minus:#f08a76;--surface:#1d1b19}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 "Be Vietnam Pro",system-ui,sans-serif;font-variant-numeric:tabular-nums}
a{color:inherit}
.band{background:var(--city);color:#fff;padding:20px max(16px,env(safe-area-inset-left)) 28px}
.band .in,.wrap{max-width:880px;margin:0 auto}
.top{display:flex;justify-content:space-between;align-items:center;gap:12px;font-size:.85rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase}
.top a{text-decoration:none;opacity:.85}.top a:hover{opacity:1;text-decoration:underline}
.band h1{font-size:clamp(2.6rem,9vw,4.6rem);line-height:.95;margin:22px 0 10px;font-weight:800;letter-spacing:-.03em}
.band .dates{font-size:1.15rem;font-weight:600}
.band .note{margin:10px 0 0;max-width:60ch;opacity:.92}
.wrap{padding:8px max(16px,env(safe-area-inset-left)) 40px}
.opt{border-bottom:2px solid var(--ink);padding:26px 0}
.opt:last-of-type{border-bottom:0}
.row{display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:start}
.code{font-weight:800;font-size:1.5rem;color:var(--city);border:2.5px solid var(--city);padding:2px 9px;line-height:1.2}
.row h2{margin:0;font-size:1.25rem;line-height:1.25}
.row h2 a{text-decoration:none;border-bottom:2px solid var(--rule)}.row h2 a:hover{border-color:var(--city)}
.meta{margin:4px 0 0;color:var(--mut);font-size:.9rem}
.price{background:var(--city);color:#fff;padding:8px 12px;text-align:right;min-width:128px}
.price b{display:block;font-size:2rem;line-height:1;font-weight:800;letter-spacing:-.02em}
.price span{display:block;font-size:.72rem;opacity:.9;margin-top:3px}
.price i{display:block;font-style:normal;font-size:.8rem;margin-top:6px;padding-top:6px;border-top:1px solid rgba(255,255,255,.35)}
.strip{display:flex;gap:4px;overflow-x:auto;margin:16px 0 4px;scroll-snap-type:x proximity}
.strip img{height:230px;width:auto;display:block;scroll-snap-align:start;background:var(--rule)}
.count{font-size:.78rem;color:var(--mut);margin:0 0 14px}
.fa{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.fa h3{margin:0 0 6px;font-size:.78rem;letter-spacing:.08em;text-transform:uppercase}
.for h3{color:var(--plus)}.against h3{color:var(--minus)}
ul{margin:0;padding:0;list-style:none}li{padding:3px 0 3px 18px;position:relative;border-top:1px solid var(--rule)}
.for li::before{content:"+";position:absolute;left:2px;color:var(--plus);font-weight:800}
.against li::before{content:"−";position:absolute;left:2px;color:var(--minus);font-weight:800}
footer{color:var(--mut);font-size:.8rem;border-top:1px solid var(--rule);padding-top:12px}
@media (max-width:620px){.row{grid-template-columns:auto 1fr}.price{grid-column:1/-1;text-align:left;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}.price i{border:0;margin:0;padding:0}.strip img{height:180px}.fa{grid-template-columns:1fr}}
.home{display:grid;grid-template-columns:1fr 1fr;min-height:100vh}
.home a{background:var(--c);color:#fff;text-decoration:none;padding:40px max(20px,env(safe-area-inset-left));display:flex;flex-direction:column;justify-content:flex-end;gap:8px}
.home a:hover h2{text-decoration:underline}
.home h2{font-size:clamp(2.4rem,7vw,4.4rem);line-height:.95;margin:0;font-weight:800;letter-spacing:-.03em}
.home p{margin:0;font-size:1.05rem;font-weight:600}
.home small{opacity:.85;font-size:.95rem}
.home .t{position:fixed;top:16px;left:0;right:0;text-align:center;color:#fff;font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:.8rem;mix-blend-mode:difference}
@media (max-width:620px){.home{grid-template-columns:1fr}.home a{min-height:50vh}}
'''

HEAD = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;800&display=swap">
<style>{css}</style></head>'''

def price_from(items): return min(int(i[5][2:]) for i in items)

for idx, (cid, cname, short, dates, nights, ci, co, col, note, items) in enumerate(CITIES):
    other = CITIES[1-idx]
    opts = []
    for code, lid, name, loc, tot, pp, rooms, rating, pro, con in items:
        link = f"https://www.airbnb.com.sg/rooms/{lid}?check_in={ci}&check_out={co}&adults=9"
        imgs = ''.join(f'<a href="{esc(url(lid,p))}?im_w=1200" target="_blank" rel="noopener"><img src="{esc(url(lid,p))}?im_w=480" loading="lazy" alt="{code} photo {i+1}"></a>' for i,p in enumerate(pics[lid]))
        opts.append(f'''<article class="opt" id="{code.lower()}">
<div class="row"><span class="code">{code}</span>
<div><h2><a href="{link}" target="_blank" rel="noopener">{esc(name)} ↗</a></h2><p class="meta">{esc(loc)}<br>{esc(rooms)} · {esc(rating)}</p></div>
<div class="price"><b>{pp}</b><span>per person / night</span><i>{tot} total · {nights} nights</i></div></div>
<div class="strip">{imgs}</div><p class="count">{len(pics[lid])} photos · swipe →</p>
<div class="fa"><div class="for"><h3>For</h3><ul>{''.join(f"<li>{esc(x)}</li>" for x in pro)}</ul></div>
<div class="against"><h3>Against</h3><ul>{''.join(f"<li>{esc(x)}</li>" for x in con)}</ul></div></div>
</article>''')
    page = HEAD.format(title=f"{cname} · Jan 2027 stays", css=CSS) + f'''<body style="--city:{col}">
<header class="band"><div class="in">
<div class="top"><a href="./">← All cities</a><a href="{other[0]}.html">{esc(other[2])} →</a></div>
<h1>{esc(cname)}</h1><div class="dates">{dates} · {nights} nights · 9 people</div><p class="note">{esc(note)}</p>
</div></header>
<main class="wrap">{''.join(opts)}
<footer>Airbnb totals before tax, checked 21 Nov 2026. Tap a photo for full size, a title to open Airbnb.</footer></main></body></html>'''
    open(os.path.join(OUTDIR, f"{cid}.html"), 'w').write(page)

tiles = ''.join(f'''<a href="{c[0]}.html" style="--c:{c[7]}"><h2>{esc(c[1])}</h2><p>{c[3]} · {c[4]} nights</p><small>{len(c[9])} options · from S${price_from(c[9])} per person / night</small></a>''' for c in CITIES)
open(os.path.join(OUTDIR, "index.html"), 'w').write(HEAD.format(title="Vietnam Jan 2027 · stays", css=CSS) + f'<body><div class="home"><div class="t">Vietnam · Jan 2027 · 9 people</div>{tiles}</div></body></html>')
print("ok", sum(len(pics[i[1]]) for c in CITIES for i in c[9]))
