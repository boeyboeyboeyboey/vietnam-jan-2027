import json, base64, html, sys
pics = json.load(open(sys.argv[1]))
OUT = sys.argv[2]

def url(lid, p):
    ext = {'.J': '.jpeg', '.j': '.jpg'}
    for k, v in ext.items():
        if p.endswith(k): p = p[:-2] + v
    if p.startswith('H:'): p = f"hosting/Hosting-{base64.b64encode(('StaySupplyListing:'+lid).encode()).decode()}/original/{p[2:]}"
    elif p.startswith('I:'): p = f"hosting/Hosting-{lid}/original/{p[2:]}"
    elif p.startswith('M:'): p = f"miso/Hosting-{lid}/original/{p[2:]}"
    return "https://a0.muscache.com/im/pictures/" + p

CITIES = [
 ("saigon", "Ho Chi Minh City", "4–7 Jan · 3 nights", "2027-01-04", "2027-01-07",
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
 ("danang", "Da Nang", "7–11 Jan · 4 nights", "2027-01-07", "2027-01-11",
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
  ("D4","1598281711142232998","Luxury 4BR Home (no pool)","1.9 km from Han Market","S$698","S$19","4 bedrooms · 8 beds · 4.5 baths","5.0★ (10) · Guest Favourite · Superhost",
   ["Under budget","All reviews 5★","Washer + dryer","Rooftop"],
   ["No pool","Only 10 reviews","Living room has a portable cooler, not AC","Construction crane nearby"]),
  ("D5","1173705612210421870","CAFE HOUSE (no pool)","1.5 km from Han Market","S$671","S$19","5 bedrooms · 5 beds · 4 baths","4.8★ (56)",
   ["Cheapest","5 bedrooms, all queen beds","Washer + dryer"],
   ["Repeated bad-smell reports","Cockroach (Nov 2025)","Living room has fan only","Dining table seats 6"]),
 ]),
]

def esc(s): return html.escape(s, quote=True)

cards = []
nav = []
for cid, cname, dates, ci, co, note, items in CITIES:
    nav.append(f'<a href="#{cid}">{esc(cname)}</a>')
    out = [f'<section id="{cid}"><h2>{esc(cname)} <span>{esc(dates)}</span></h2><p class="note">{esc(note)}</p>']
    for code, lid, name, loc, tot, pp, rooms, rating, pro, con in items:
        link = f"https://www.airbnb.com.sg/rooms/{lid}?check_in={ci}&check_out={co}&adults=9"
        imgs = ''.join(f'<a href="{esc(url(lid,p))}" target="_blank" rel="noopener"><img src="{esc(url(lid,p))}?im_w=480" loading="lazy" alt=""></a>' for p in pics[lid])
        out.append(f'''<article>
<div class="head"><span class="code">{code}</span><div class="t"><h3><a href="{link}" target="_blank" rel="noopener">{esc(name)} ↗</a></h3>
<p class="meta">{esc(loc)} · {esc(rooms)} · {esc(rating)}</p></div>
<div class="price"><b>{pp}</b><small>/person/night</small><small>{tot} total</small></div></div>
<div class="strip">{imgs}</div><p class="count">{len(pics[lid])} photos · scroll →</p>
<div class="pc"><ul class="pro">{''.join(f"<li>{esc(x)}</li>" for x in pro)}</ul><ul class="con">{''.join(f"<li>{esc(x)}</li>" for x in con)}</ul></div>
</article>''')
    out.append('</section>')
    cards.append('\n'.join(out))

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vietnam Jan 2027 Stays</title><meta name="robots" content="noindex">
<style>
:root{{--bg:#f6f7f5;--card:#fff;--fg:#17201d;--mut:#5f6b66;--line:#dde3df;--acc:#0f6e5c;--good:#1d7a4f;--bad:#b3261e}}
@media (prefers-color-scheme:dark){{:root{{--bg:#111715;--card:#19211e;--fg:#e7ece9;--mut:#9aa8a1;--line:#2a3531;--acc:#5cc7ad;--good:#6fd39c;--bad:#f08a80}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}}
main{{max-width:900px;margin:0 auto;padding:16px}}
nav{{position:sticky;top:0;background:var(--bg);display:flex;gap:8px;padding:10px 0;z-index:2;border-bottom:1px solid var(--line)}}
nav a{{padding:6px 14px;border-radius:99px;background:var(--card);border:1px solid var(--line);color:var(--fg);text-decoration:none;font-weight:600}}
h1{{font-size:1.4rem;margin:8px 0 0}}h2{{margin:28px 0 4px;font-size:1.3rem}}h2 span{{font-weight:400;color:var(--mut);font-size:.95rem}}
.note{{margin:0 0 14px;color:var(--mut)}}
article{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:0 0 16px}}
.head{{display:flex;gap:12px;align-items:flex-start}}.t{{flex:1;min-width:0}}
.code{{background:var(--acc);color:var(--card);font-weight:800;border-radius:8px;padding:6px 10px;font-size:1.1rem}}
h3{{margin:0;font-size:1.1rem}}h3 a{{color:var(--fg)}}.meta{{margin:2px 0 0;color:var(--mut);font-size:.88rem}}
.price{{text-align:right;white-space:nowrap}}.price b{{font-size:1.3rem;display:block}}.price small{{display:block;color:var(--mut);font-size:.75rem}}
.strip{{display:flex;gap:6px;overflow-x:auto;margin:12px -14px 0;padding:0 14px;scroll-snap-type:x proximity}}
.strip img{{height:200px;width:auto;border-radius:8px;display:block;scroll-snap-align:start;background:var(--line)}}
.count{{margin:4px 0 8px;font-size:.75rem;color:var(--mut)}}
.pc{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}ul{{margin:0;padding-left:0;list-style:none}}li{{padding-left:20px;position:relative;margin:2px 0}}
.pro li::before{{content:"+";position:absolute;left:4px;color:var(--good);font-weight:800}}.con li::before{{content:"–";position:absolute;left:4px;color:var(--bad);font-weight:800}}
section{{scroll-margin-top:56px}}footer{{color:var(--mut);font-size:.8rem;padding:8px 0 24px}}
@media (max-width:600px){{.pc{{grid-template-columns:1fr}}.strip img{{height:160px}}.head{{flex-wrap:wrap}}.price{{text-align:left;width:100%}}}}
</style></head><body><main>
<h1>Vietnam Jan 2027 · 9 pax · vote by code</h1>
<nav>{''.join(nav)}</nav>
{''.join(cards)}
<footer>Airbnb totals before tax, checked 21 Nov 2026. Tap a photo for full size, tap a title to open on Airbnb.</footer>
</main></body></html>'''
open(OUT, 'w').write(page)
print(len(page), sum(len(pics[i[1]]) for c in CITIES for i in c[6]))
