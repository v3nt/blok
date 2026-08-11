import datetime, html, re

BASE = "/sessions/bold-hopeful-hypatia/mnt/outputs/blok/"
YEAR = 2026
LINKS = {
  "Clapton": "https://classpass.com/studios/blok-clapton-london",
  "Shoreditch": "https://classpass.com/studios/blok-shoreditch-london",
}
COLORS = {
  "Calisthenics": "#7c5cff",
  "Strength (Upper)": "#2e9e5b",
  "Strength (Lower)": "#c77d0a",
  "Strength (Full Body)": "#1f7fd1",
}
CATS = ["Calisthenics", "Strength (Upper)", "Strength (Lower)", "Strength (Full Body)"]

def classify(name):
    u = name.upper()
    if "CALISTHENICS" in u: return "Calisthenics"
    if "UPPER" in u: return "Strength (Upper)"
    if "LOWER" in u: return "Strength (Lower)"
    if "FULL" in u: return "Strength (Full Body)"
    return "Strength (Full Body)"

def mins(t):
    m = re.match(r"(\d+):(\d+)\s*(AM|PM)", t)
    h, mi, ap = int(m.group(1)), int(m.group(2)), m.group(3)
    if ap == "PM" and h != 12: h += 12
    if ap == "AM" and h == 12: h = 0
    return h * 60 + mi

rows = []
loc = None
for line in open(BASE + "data.txt"):
    line = line.rstrip("\n")
    if not line: continue
    if line in ("CLAPTON", "SHOREDITCH"):
        loc = line.title(); continue
    d, t, dur, name, inst, av = line.split("|")
    mon, day = d.split()
    dt = datetime.date(YEAR, 8, int(day))
    cat = classify(name)
    if av == "R":
        avail_txt, avail_flag = "Available (Reserve)", 1
    elif av == "F":
        avail_txt, avail_flag = "Full / Unavailable", 0
    else:
        avail_txt, avail_flag = f"Available ({av} credits)", 1
    rows.append(dict(dt=dt, loc=loc, time=t, dur=dur, name=name, inst=inst,
                     cat=cat, avail=avail_txt, flag=avail_flag, m=mins(t)))

rows.sort(key=lambda r: (r["dt"], r["m"], r["loc"]))

total = len(rows)
n_avail = sum(r["flag"] for r in rows)
cat_counts = {c: sum(1 for r in rows if r["cat"] == c) for c in CATS}
n_work = sum(1 for r in rows if r["dt"].weekday() < 5 and 480 <= r["m"] <= 1045)

d0, d1 = rows[0]["dt"], rows[-1]["dt"]
fmt = lambda d: d.strftime("%a %-d %b %Y")
fmt_short = lambda d: d.strftime("%a %-d %b")
stamp = datetime.datetime.now().strftime("%a %-d %b %Y, %H:%M")

body = []
last = None
for r in rows:
    cls = "day-start" if r["dt"] != last else ""
    last = r["dt"]
    wd = 1 if r["dt"].weekday() < 5 else 0
    col = COLORS[r["cat"]]
    acol = "#1f8a3c" if r["flag"] else "#c0392b"
    body.append(
f'''<tr class="{cls}" data-cat="{r['cat']}" data-avail="{r['flag']}" data-wd="{wd}" data-mins="{r['m']}">
<td>{fmt_short(r['dt'])}</td>
<td><a href="{LINKS[r['loc']]}" target="_blank" rel="noopener">{r['loc']}</a></td>
<td>{r['time']}</td>
<td><span class="pill" style="background:{col}22;color:{col};border:1px solid {col}55;">{html.escape(r['cat'])}</span></td>
<td>{html.escape(r['name'])} <span class="dur">({r['dur']} min)</span></td>
<td>{html.escape(r['inst'])}</td>
<td style="color:{acol};font-weight:600;">{r['avail']}</td>
</tr>''')

typeboxes = "\n".join(
    f'<label class="chk"><input type="checkbox" class="typeFilter" data-cat="{c}" checked> {html.escape(c)} ({cat_counts[c]})</label>'
    for c in CATS)

desc = (f"BLOK Clapton &amp; Shoreditch — upcoming Calisthenics / BLOKStrength schedule for the next 2 weeks "
        f"({fmt(d0)} – {fmt(d1)}), scraped live from ClassPass public studio pages. Filterable by availability, "
        f"class type, and work-hours. Data is a periodic snapshot refreshed by a scheduled task every 3 hours, "
        f"not live-refreshing on open.")

doc = f'''<!DOCTYPE html><script type="application/json" id="cowork-artifact-meta">
{{
  "name": "Blok 2week Schedule",
  "schemaVersion": 1,
  "description": "{desc}"
}}
</script>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>BLOK Clapton &amp; Shoreditch schedule</title>
<style>
  :root {{
    color-scheme: light;
    --bg: #f7f7f8;
    --card: #ffffff;
    --border: #e3e3e6;
    --header-bg: #1a1a1f;
    --header-fg: #f5f5f7;
    --row-alt: #fafafa;
    --row-hover: #eef4ff;
    --text: #1c1c1e;
    --muted: #6b6b70;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    margin: 0;
    padding: 24px;
  }}
  h1 {{
    font-size: 1.4rem;
    font-weight: 700;
    margin: 0 0 4px 0;
  }}
  .stamp {{
    color: var(--muted);
    font-size: 0.85rem;
    margin: 0 0 16px 0;
  }}
  .filterbar {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 14px;
    background: #eeeef0;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 16px;
    margin-bottom: 16px;
    font-size: 0.92rem;
  }}
  .filterbar .sep {{
    width: 1px;
    height: 20px;
    background: #cfcfd2;
  }}
  .filterbar label.chk {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
    white-space: nowrap;
  }}
  .filterbar .typegroup {{
    display: inline-flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }}
  .filterbar .type-label {{
    font-weight: 600;
    color: var(--muted);
  }}
  .count {{
    margin-left: auto;
    color: var(--muted);
    font-variant-numeric: tabular-nums;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    background: var(--card);
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }}
  thead th {{
    position: sticky;
    top: 0;
    background: var(--header-bg);
    color: var(--header-fg);
    text-align: left;
    padding: 10px 12px;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    z-index: 2;
  }}
  tbody td {{
    padding: 9px 12px;
    border-bottom: 1px solid var(--border);
    font-size: 0.9rem;
    vertical-align: middle;
  }}
  tbody td a {{ color: inherit; text-decoration: none; border-bottom: 1px dotted #9a9aa0; }}
  tbody td a:hover {{ color: #1f7fd1; border-bottom-color: #1f7fd1; }}
  tbody tr:nth-child(even) {{
    background: var(--row-alt);
  }}
  tbody tr:hover {{
    background: var(--row-hover);
  }}
  tr.day-start td {{
    border-top: 2px solid #1a1a1f;
  }}
  .pill {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    white-space: nowrap;
  }}
  .dur {{
    color: var(--muted);
    font-size: 0.82rem;
  }}
  tr.hidden {{
    display: none;
  }}
</style>
</head>
<body>
<h1>BLOK Clapton &amp; Shoreditch — upcoming Calisthenics / BLOKStrength</h1>
<p class="stamp">{fmt(d0)} – {fmt(d1)} &middot; {total} classes &middot; snapshot refreshed {stamp} BST (auto-updated every 3 hours)</p>

<div class="filterbar">
  <label class="chk"><input type="checkbox" id="availOnly"> Show available only ({n_avail})</label>
  <div class="sep"></div>
  <div class="typegroup"><span class="type-label">Type</span>
    {typeboxes}
  </div>
  <div class="sep"></div>
  <label class="chk"><input type="checkbox" id="hideWorkHours"> Hide weekday 8:00am&ndash;5:25pm classes ({n_work})</label>
  <div class="count" id="liveCount">showing {total} of {total}</div>
</div>

<table>
<thead>
<tr>
<th>Date</th><th>Location</th><th>Time</th><th>Type</th><th>Class</th><th>Instructor</th><th>Availability</th>
</tr>
</thead>
<tbody id="rows">
{chr(10).join(body)}
</tbody>
</table>

<script>
(function() {{
  const availChk = document.getElementById('availOnly');
  const workChk = document.getElementById('hideWorkHours');
  const typeChks = Array.from(document.querySelectorAll('.typeFilter'));
  const rows = Array.from(document.querySelectorAll('#rows tr'));
  const liveCount = document.getElementById('liveCount');

  function loadState() {{
    try {{
      const a = localStorage.getItem('blokAvailOnly');
      if (a !== null) availChk.checked = a === '1';
      const w = localStorage.getItem('blokHideWorkHours');
      if (w !== null) workChk.checked = w === '1';
      const t = localStorage.getItem('blokTypes');
      if (t !== null) {{
        const set = new Set(JSON.parse(t));
        typeChks.forEach(c => c.checked = set.has(c.dataset.cat));
      }}
    }} catch(e) {{}}
  }}

  function saveState() {{
    localStorage.setItem('blokAvailOnly', availChk.checked ? '1' : '0');
    localStorage.setItem('blokHideWorkHours', workChk.checked ? '1' : '0');
    localStorage.setItem('blokTypes', JSON.stringify(typeChks.filter(c=>c.checked).map(c=>c.dataset.cat)));
  }}

  function applyFilters() {{
    const checkedTypes = new Set(typeChks.filter(c => c.checked).map(c => c.dataset.cat));
    let shown = 0;
    let lastDate = null;
    rows.forEach(r => r.classList.remove('day-start'));
    rows.forEach(row => {{
      const availOk = !availChk.checked || row.dataset.avail === '1';
      const typeOk = checkedTypes.has(row.dataset.cat);
      const mins = parseInt(row.dataset.mins, 10);
      const isWd = row.dataset.wd === '1';
      const inWorkHours = isWd && mins >= 480 && mins <= 1045;
      const workOk = !workChk.checked || !inWorkHours;
      const visible = availOk && typeOk && workOk;
      row.classList.toggle('hidden', !visible);
      if (visible) {{
        shown++;
        const dateCell = row.querySelector('td');
        const dateVal = dateCell ? dateCell.textContent : null;
        if (dateVal !== lastDate) {{
          row.classList.add('day-start');
          lastDate = dateVal;
        }}
      }}
    }});
    liveCount.textContent = `showing ${{shown}} of ${{rows.length}}`;
    saveState();
  }}

  loadState();
  availChk.addEventListener('change', applyFilters);
  workChk.addEventListener('change', applyFilters);
  typeChks.forEach(c => c.addEventListener('change', applyFilters));
  applyFilters();
}})();
</script>
</body>
</html>
'''

open(BASE + "index.html", "w").write(doc)
print("rows", total, "avail", n_avail, "work", n_work, cat_counts, fmt(d0), fmt(d1))
