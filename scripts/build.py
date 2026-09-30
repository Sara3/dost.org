"""Build the portable Dost website with Python's standard library."""
from pathlib import Path
from html import escape as e
import json
import zipfile
import hashlib

ROOT = Path(__file__).resolve().parent.parent
REPORTS = json.loads((ROOT / 'content/reports.json').read_text())
GENERATED_PATH = ROOT / 'content/media-generated.json'
GENERATED = json.loads(GENERATED_PATH.read_text()) if GENERATED_PATH.exists() else {}
MEDIA = GENERATED.get('items', []) + json.loads((ROOT / 'content/media.json').read_text())
for year_text, pdf in GENERATED.get('reports', {}).items():
 year = int(year_text)
 record = next((r for r in REPORTS if r['year'] == year), None)
 if record is None:
  record = {'year': year, 'type': 'records'}
  REPORTS.append(record)
 if record['type'] != 'report':
  record.update({'type': 'report', 'label': 'Annual report', 'title': f'{year} annual report',
   'description': f'Dost’s published annual report for {year}.',
   'paragraphs': ['Read the full annual report in the downloadable PDF below.'],
   'note': 'The downloadable document is provided by Dost. Financial figures have not been extracted into this summary.'})
  record.pop('metrics', None)
 record['pdf'] = pdf
REPORTS.sort(key=lambda r: r['year'], reverse=True)
ARCHIVE_RANGE = f'{min(r["year"] for r in REPORTS)}–{max(r["year"] for r in REPORTS)}'
TEAM = json.loads((ROOT / 'content/team.json').read_text())
PROGRAMS = json.loads((ROOT / 'content/programs.json').read_text())
DONATE = 'donate.html'
GIVEBUTTER = 'https://givebutter.com/dostforgood'
GIVEBUTTER_SCRIPT = 'https://widgets.givebutter.com/latest.umd.cjs?acct=IE3iwDtDjUxngJQc&p=other'
CONTACT_EMAIL = 'support@dostforgood.org'
STYLE_VERSION = hashlib.sha256((ROOT / 'assets/site.css').read_bytes()).hexdigest()[:12]
SCRIPT_VERSION = hashlib.sha256((ROOT / 'assets/site.js').read_bytes()).hexdigest()[:12]
ARROW = '<span class="arrow" aria-hidden="true">↗</span>'
ICONS = {
 'heart':'<path d="M20.5 4.6a5.4 5.4 0 0 0-7.6 0L12 5.5l-.9-.9a5.4 5.4 0 0 0-7.6 7.6L12 21l8.5-8.8a5.4 5.4 0 0 0 0-7.6Z"/>',
 'book':'<path d="M3 4h6c2 0 3 1 3 2v15c0-2-2-3-4-3H3V4Zm18 0h-6c-2 0-3 1-3 2v15c0-2 2-3 4-3h5V4Z"/>',
 'check':'<path d="M12 2 3 6v6c0 5 9 10 9 10s9-5 9-10V6l-9-4Z"/><path d="m8 12 3 3 5-6"/>'
}
def icon(name):
 return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+ICONS[name]+'</svg>'
def brand(p=''):
 return f'<a class="brand" href="{p}index.html" aria-label="Dost home"><span class="wordmark">dost</span></a>'
def header(p=''):
 return f'''<a class="skip" href="#main">Skip to content</a>
 <div class="topbar"><div class="container"><span>Supporting families in Afghanistan</span><a href="{p}reports/index.html">Annual reports &amp; records · {ARCHIVE_RANGE} →</a></div></div>
 <header class="header"><div class="container header-inner">{brand(p)}
 <nav class="nav" id="navigation" aria-label="Main navigation"><a href="{p}index.html#work">Our work</a><a href="{p}reports/index.html">Reports &amp; financials</a><a href="{p}index.html#about">About Dost</a><a href="{p}contact.html">Contact</a></nav>
 <a class="button small" href="{p}{DONATE}">Donate {ARROW}</a><button class="menu-toggle" aria-controls="navigation" aria-expanded="false" aria-label="Toggle navigation">Menu</button></div></header>'''
def footer(p=''):
 return f'''<footer class="footer"><div class="container"><div class="footer-main"><div class="footer-brand">{brand(p)}<p>A grassroots commitment to women’s education and families’ basic needs in Afghanistan.</p></div><div><h3>Explore Dost</h3><div class="footer-links"><a href="{p}index.html#work">Our work</a><a href="{p}reports/index.html">Annual reports</a><a href="{p}index.html#about">About &amp; leadership</a><a href="{p}index.html#community">Community gatherings</a></div></div><div><h3>Stay connected</h3><div class="footer-links"><a href="{p}contact.html">Contact the team</a><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><a href="{p}{DONATE}">Donate</a><a href="{p}downloads/dost-report-archive.zip" download>Download report summaries ↓</a><a href="{p}privacy.html">Privacy</a></div></div></div><div class="footer-bottom"><span>© 2026 Dost. A 501(c)(3) nonprofit organization.</span><span>San Francisco · Afghanistan</span></div></div></footer>'''
def cta(p=''):
 return f'''<section class="cta"><div class="container cta-inner"><div><p class="eyebrow">Support our work</p><h2>Help fund essential assistance.</h2><p>Your contribution supports food, medical care and education costs<br>for families in Afghanistan.</p></div><div class="cta-actions"><a class="button light" href="{p}{DONATE}">Give once or monthly {ARROW}</a><a href="https://sadaqiq0.medium.com/eid-gift-2025-5b5ec5480628">Read our latest distribution report ↗</a></div></div></section>'''
def page(title,body,p='',description='Dost is a grassroots nonprofit dedicated to women’s education and basic needs in Afghanistan. Explore our work, local coordination and annual reports.',extra_head=''):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | Dost</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#203f34"><meta property="og:title" content="{e(title)} | Dost"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website"><link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{p}assets/site.css?v={STYLE_VERSION}"><script src="{p}assets/site.js?v={SCRIPT_VERSION}" defer></script>{extra_head}</head><body>{header(p)}{body}{footer(p)}</body></html>'''
def metrics(r):
 return ''.join(f'<div class="stat"><strong>{e(value)}</strong><span>{e(label)}</span></div>' for value,label in r.get('metrics',[]))
def record_sections(record):
 sections=[]
 for section in record.get('sections',[]):
  content=f'<section class="record-section"><h2>{e(section["heading"])}</h2>'
  content+=''.join(f'<p>{e(paragraph)}</p>' for paragraph in section.get('paragraphs',[]))
  if section.get('items'):
   content+='<ul class="record-list">'+''.join(f'<li>{e(item)}</li>' for item in section['items'])+'</ul>'
  if section.get('table'):
   table=section['table']
   content+='<div class="record-table-wrap"><table class="record-table"><caption class="sr-only">'+e(section['heading'])+'</caption><thead><tr>'+''.join(f'<th scope="col">{e(label)}</th>' for label in table['headers'])+'</tr></thead><tbody>'
   for row in table['rows']:
    content+='<tr>'
    for i,cell in enumerate(row):
     content+=f'<th scope="row">{e(cell)}</th>' if i==0 else f'<td>{e(cell)}</td>'
    content+='</tr>'
   content+='</tbody></table></div>'
  sections.append(content+'</section>')
 return ''.join(sections)
def record_sources(record):
 sources=list(record.get('sources',[]))
 if record.get('source'):
  sources.insert(0,{'url':record['source'],'label':record.get('sourceLabel','Read the original report'),'note':('Published '+record.get('sourcePublished',record.get('published',''))) if record.get('sourcePublished') or record.get('published') else ''})
 if not sources:return ''
 return '<section class="record-sources"><h2>Sources &amp; original records</h2>'+''.join(f'<div><a class="text-link" href="{e(source["url"])}">{e(source["label"])} {ARROW}</a>'+ (f'<p>{e(source["note"])}</p>' if source.get('note') else '')+'</div>' for source in sources)+'</section>'
def record_evidence(record,prefix=''):
 evidence=[]
 for item in record.get('evidence',[]):
  src=prefix+item['src']
  evidence.append(f'<details class="record-evidence"><summary>{e(item["title"])} <span aria-hidden="true">＋</span></summary><figure><a href="{e(src)}" target="_blank" rel="noopener noreferrer" aria-label="Open full-size source screenshot in a new tab"><img src="{e(src)}" width="{item["width"]}" height="{item["height"]}" alt="{e(item["alt"])}" loading="lazy"></a><figcaption>{e(item["caption"])}</figcaption></figure></details>')
 return ''.join(evidence)
def profile_content(person,prefix='',heading='h2'):
 name, role, ident = e(person['name']), e(person['role']), person['id']
 paragraphs=''.join(f'<p>{e(paragraph)}</p>' for paragraph in person['paragraphs'])
 duties=''
 if person.get('responsibilities'):
  duties='<h3>Responsibilities</h3><dl class="profile-duties">'+''.join(f'<div><dt>{e(label)}</dt><dd>{e(detail)}</dd></div>' for label,detail in person['responsibilities'])+'</dl>'
 linkedin=f'<a class="text-link" href="{e(person["linkedin"])}" target="_blank" rel="noopener noreferrer">View LinkedIn profile <span aria-hidden="true">↗</span><span class="sr-only"> (opens in a new tab)</span></a>' if person.get('linkedin') else ''
 return f'<div class="profile-header"><img src="{prefix}{e(person["image"])}" width="{person["width"]}" height="{person["height"]}" alt="{name}"><div><p class="eyebrow">The Dost team</p><{heading} id="{ident}-name">{name}</{heading}><p class="profile-role">{role}</p></div></div><div class="profile-body">{paragraphs}{duties}'+(f'<div class="profile-links">{linkedin}</div>' if linkedin else '')+'</div>'
def team_cards():
 cards=[]
 for person in TEAM:
  anchor=f' id="{person["anchor"]}"' if person.get('anchor') else ''
  cards.append(f'<a class="team-person"{anchor} href="team/{person["id"]}.html" data-profile="{person["id"]}" aria-label="Read {e(person["name"])}’s profile"><img src="{e(person["image"])}" width="{person["width"]}" height="{person["height"]}" loading="lazy" alt=""><div class="team-card-copy"><h3>{e(person["name"])}</h3><p>{e(person["role"])}</p><span class="team-read">Read profile <span aria-hidden="true">↗</span></span></div></a>')
 return '<div class="team-grid team-cards">'+''.join(cards)+'</div>'
def team_profiles():
 templates=''.join(f'<template id="profile-{person["id"]}">{profile_content(person)}</template>' for person in TEAM)
 return templates+'<dialog class="profile-dialog" data-profile-dialog><button class="profile-close" type="button" data-profile-close autofocus aria-label="Close profile">Close <span aria-hidden="true">×</span></button><div data-profile-content></div></dialog>'
def row(r,p=''):
 tag_class='tag subtle' if r['type']=='records' else 'tag'
 return f'''<a class="report-row" data-report-type="{r['type']}" href="{p}{r['year']}.html"><span class="year">{r['year']}</span><div><h3>{e(r['title'])}</h3><p>{e(r['description'])}</p></div><span class="{tag_class}">{e(r['label'])}</span>{ARROW}</a>'''
def report_timeline():
 links=[]
 for record in sorted(REPORTS, key=lambda r:r['year']):
  status='Report' if record['type']=='report' else 'Appeal' if record['type']=='campaign' else 'To add'
  if record['label']=='Fundraising update': status='Update'
  status=record.get('timelineLabel',status)
  links.append(f'<a class="record-year record-{record["type"]}" href="reports/{record["year"]}.html" aria-label="{record["year"]}: {status}"><span>{record["year"]}</span><small>{status}</small></a>')
 return f'<div class="record-history"><div class="record-history-intro"><p>Explore all {len(REPORTS)} years · Reports, updates and campaign records</p></div><nav class="record-timeline" aria-label="Annual archive by year">'+''.join(links)+'</nav></div>'
def featured_reports():
 selected=[r for r in REPORTS if r['year'] in (2025,2024)]
 buttons=[]; panels=[]
 for i,r in enumerate(selected):
  year=r['year']; available=r['type'] in ('report','update')
  buttons.append(f'<button type="button" data-report-select="{i}" aria-pressed="{str(i==0).lower()}" aria-controls="annual-card-{year}">{year}</button>')
  date='Published '+r['published'] if r.get('published') else 'PDF available' if r.get('pdf') else 'Retrospective update' if r['type']=='update' else 'Report not yet available'
  status='Yearly update' if r['type']=='update' else 'Published report' if available else 'Awaiting publication'
  title=r['title'] if available else f'The {year} annual record.'
  description=r['description'] if available else 'This report has not yet been added to the public archive. Contact Dost for information about this year’s work.'
  panels.append(f'<article class="report-panel'+(' report-pending' if not available else '')+f'" data-report-year="{year}" id="annual-card-{year}" role="group" aria-roledescription="slide" aria-label="{i+1} of {len(selected)}: {year}, {status.lower()}"><div class="report-panel-year"><p class="eyebrow">{e(r["label"])}</p><span>{year}</span><p>{e(date)}</p></div><div class="report-panel-copy"><p class="report-status">{status}</p><h3>{e(title)}</h3><p>{e(description)}</p><a class="text-link" href="reports/{year}.html">'+(f'Read the {year} update' if r['type']=='update' else f'Read the {year} report' if available else 'View the record status')+' <span aria-hidden="true">↗</span></a></div></article>')
 return '<div class="report-carousel" data-report-carousel role="region" aria-roledescription="carousel" aria-label="Annual reports and records"><div class="report-toolbar" data-report-controls hidden><div class="report-years" role="group" aria-label="Choose a report year">'+''.join(buttons)+'</div><div class="report-arrows"><button type="button" data-report-prev aria-label="Previous report year" disabled>←</button><button type="button" data-report-next aria-label="Next report year">→</button></div></div><div class="report-rail" data-report-rail>'+''.join(panels)+'</div><p class="sr-only" data-report-announcement role="status" aria-live="polite" aria-atomic="true">2025 report. 1 of 2.</p></div>'
def gallery():
 slides, thumbs, fallback = [], [], []
 total=len(MEDIA)
 for i, item in enumerate(MEDIA):
  count, title = f'{i+1} of {total}', e(item['title'])
  year = str(item['year']) if item.get('year') else item['yearNote']
  poster = e(item.get('thumbnail',item.get('poster',item['src'])))
  if item['type'] == 'video':
   visual = f'<video controls playsinline preload="none" poster="{e(item["poster"])}" width="{item["width"]}" height="{item["height"]}" aria-label="{title}" aria-describedby="gallery-caption"><source src="{e(item["src"])}" type="video/mp4">Your browser does not support this video. <a href="{e(item["src"])}">Open the video.</a></video>'
  else:
   responsive=f' srcset="{e(item["thumbnail"])} {item.get("thumbnailWidth",480)}w, {e(item["src"])} {item["width"]}w" sizes="(max-width:760px) 88vw, 900px"' if item.get('thumbnail') and item['width']>item.get('thumbnailWidth',480) else ''
   visual = f'<img src="{e(item["src"])}"{responsive} width="{item["width"]}" height="{item["height"]}" alt="{e(item["alt"])}" loading="lazy" draggable="false">'
  slides.append(f'<figure class="gallery-slide" id="media-slide-{i}" data-gallery-slide data-year-key="{item.get("year") or "undated"}" data-title="{title}" data-caption="{e(item["caption"])}" data-year="{e(year)}" data-poster="{poster}" style="--media-ratio:{item["width"]/item["height"]:.4f}" role="group" aria-roledescription="slide" aria-label="{count}: {title}"'+(' hidden' if i else '')+f'><div class="gallery-mat">{visual}</div></figure>')
  thumbs.append(f'<button class="gallery-thumb" type="button" data-gallery-select="{i}" aria-controls="media-slide-{i}" aria-pressed="{str(i==0).lower()}" aria-label="Show {item["type"]} {count}: {title}"><span class="thumb-image"><img src="{poster}" alt="" width="120" height="76" loading="lazy">'+('<span class="video-badge" aria-hidden="true">▶</span>' if item['type']=='video' else '')+f'</span><span>{e(item["short"])}</span></button>')
  fallback.append(f'<li><a href="{e(item["src"])}">{title}</a> · {e(year)}</li>')
 first=MEDIA[0]
 years=sorted({item['year'] for item in MEDIA if item.get('year')},reverse=True)
 year_filter=('<div class="gallery-year-filter" data-gallery-controls hidden><label for="gallery-year-select">Browse by year</label><select id="gallery-year-select" data-gallery-year-filter><option value="all">All years</option>'+''.join(f'<option value="{year}">{year}</option>' for year in years)+('<option value="undated">Earlier archive · date unconfirmed</option>' if any(not item.get('year') for item in MEDIA) else '')+'</select></div>') if years else ''
 def peek(item,direction):
  return f'<button class="gallery-peek peek-{direction}" type="button" data-gallery-{direction} data-gallery-peek aria-label="View {direction}: {e(item["title"])}" hidden><img src="{e(item.get("poster",item["src"]))}" alt="" draggable="false"><span class="peek-label" aria-hidden="true">{e(item["short"])}</span></button>'
 return f'''<div class="media-gallery" data-gallery role="region" aria-roledescription="carousel" aria-label="Photographs and video from the Dost archive">{year_filter}<div class="gallery-slides">{peek(MEDIA[-1],'prev')}{''.join(slides)}{peek(MEDIA[1],'next')}<div class="gallery-arrows" data-gallery-controls hidden><button type="button" data-gallery-prev aria-label="Previous photograph or video">←</button><button type="button" data-gallery-next aria-label="Next photograph or video">→</button></div></div><div class="gallery-caption-row"><div class="gallery-caption" id="gallery-caption"><p class="gallery-year" data-gallery-year>{e(str(first['year']) if first.get('year') else first['yearNote'])}</p><h3 data-gallery-title>{e(first['title'])}</h3><p data-gallery-caption>{e(first['caption'])}</p></div><div class="gallery-controls" data-gallery-controls hidden><p class="gallery-status" role="status" aria-live="polite" aria-atomic="true"><span data-gallery-counter>01 / {total:02}</span><span class="sr-only" data-gallery-announcement>{e(first['title'])}</span></p></div></div><div class="gallery-thumbnails" data-gallery-controls role="group" aria-label="Choose a photograph or video" hidden>{''.join(thumbs)}</div><noscript><p>Explore the original photographs and video:</p><ul>{''.join(fallback)}</ul></noscript></div>'''
home=(ROOT/'content/home.html').read_text()
for token, value in {
 '{{DONATE}}':DONATE,
 '{{ARCHIVE_ROWS}}':''.join(row(r,'reports/') for r in REPORTS if r['year'] in (2026,2021,2020,2019,2018)),
 '{{GALLERY}}':gallery(),
 '{{REPORT_TIMELINE}}':report_timeline(),
 '{{FEATURED_REPORTS}}':featured_reports(),
 '{{ARCHIVE_RANGE}}':ARCHIVE_RANGE,
 '{{TEAM_CARDS}}':team_cards(),
 '{{TEAM_PROFILES}}':team_profiles(),
 '{{CTA}}':cta(),
}.items():
 home=home.replace(token,value)
(ROOT/'index.html').write_text(page('Women’s education and essential support in Afghanistan',home))
(ROOT/'team').mkdir(exist_ok=True)
for person in TEAM:
 body=f'<main id="main"><article class="container profile-page"><div class="breadcrumbs"><a href="../index.html">Home</a> / <a href="../index.html#team">Our team</a> / {e(person["name"])}</div>{profile_content(person,"../","h1")}<div class="profile-page-back"><a class="text-link" href="../index.html#team">← Back to the team</a></div></article></main>'
 (ROOT/f'team/{person["id"]}.html').write_text(page(person['name'],body,'../',person['paragraphs'][0]))
(ROOT/'programs').mkdir(exist_ok=True)
for program in PROGRAMS:
 paragraphs=''.join(f'<p>{e(paragraph)}</p>' for paragraph in program['paragraphs'])
 body=f'<main id="main"><article class="container article"><section class="page-intro"><div class="breadcrumbs"><a href="../index.html">Home</a> / <a href="../index.html#work">Our work</a> / {e(program["title"])}</div><p class="eyebrow">{e(program["eyebrow"])}</p><h1>{e(program["title"])}</h1><p>{e(program["description"])}</p></section><div class="article-stats">{metrics(program)}</div><div class="article-body"><h2>Opening a path into programming.</h2>{paragraphs}{record_sections(program)}<p class="article-note">{e(program["note"])}</p></div>{record_sources(program)}<div class="actions"><a class="text-link" href="../index.html#work">← Explore our work</a></div></article>{cta("../")}</main>'
 (ROOT/f'programs/{program["id"]}.html').write_text(page(program['title'],body,'../',program['description']))
archive_note='Public distribution reports and fundraising updates are linked to their original sources. The 2024 entry is a retrospective update supplied by Dost about a private friends-and-family campaign, for which no public report was published at the time. Campaigns and fundraising plans are distinguished from completed distributions.'
archive_filters=''.join(f'<button class="filter" data-filter="{kind}" aria-pressed="{str(kind=="all").lower()}">{label}</button>' for kind,label in [('all','All years'),('report','Published reports'),('campaign','Campaigns'),('update','Yearly updates'),('records','Records to add')] if kind=='all' or any(r['type']==kind for r in REPORTS))
archive=f'''<main id="main"><div class="container"><section class="page-intro"><div class="breadcrumbs"><a href="../index.html">Home</a> / Annual reports</div><p class="eyebrow">{ARCHIVE_RANGE} / Public record</p><h1>Reports &amp; distributions.</h1><p>Annual summaries, reported amounts, and links to the original updates. The year shown is the year of the work, which may differ from the publication date.</p></section><div class="archive-controls"><div class="filters" role="group" aria-label="Filter annual records">{archive_filters}</div><a class="text-link" href="../downloads/dost-report-archive.zip" download>Download summaries ↓</a></div><p class="report-count" role="status" aria-live="polite">{len(REPORTS)} years shown</p><div>{''.join(row(r) for r in REPORTS)}</div><p class="archive-notice"><strong>A note on the archive.</strong> {archive_note} Downloads contain local summaries, supplied PDFs and original-source links; full Medium articles are not reproduced.</p><div class="archive-bottom" style="margin-bottom:70px"><p>Looking for an earlier year or a specific record?</p><a class="text-link" href="../contact.html">Contact the team {ARROW}</a></div></div>{cta("../")}</main>'''
(ROOT/'reports/index.html').write_text(page('Annual reports',archive,'../'))
for r in REPORTS:
 metric_block=f'<div class="article-stats">{metrics(r)}</div>' if r.get('metrics') else ''
 paragraphs=''.join(f'<p>{e(x)}</p>' for x in r.get('paragraphs',[r['description']]))
 source=record_sources(r)
 if not source and not r.get('evidence') and r['type']=='records':
  source='<div class="source-box"><p>Have the records for this year?</p><a class="text-link" href="../contact.html">Contact the team ↗</a></div>'
 if r.get('pdf'):
  source=f'<div class="source-box"><p>Annual report · PDF</p><a class="text-link" href="../{e(r["pdf"])}" download>Download the {r["year"]} report ↓</a></div>'+ (source if r.get('source') else '')
 body=f'''<main id="main"><article class="container article"><section class="page-intro"><div class="breadcrumbs"><a href="../index.html">Home</a> / <a href="index.html">Annual reports</a> / {r['year']}</div><p class="eyebrow">{r['year']} / {e(r['label'])}</p><h1>{e(r['title'])}</h1><p>{e(r['description'])}</p></section>{metric_block}<div class="article-body"><h2>{'Report summary' if r['type']=='report' else 'About this record'}</h2>{paragraphs}{record_sections(r)}<p class="article-note">{e(r['note'])}</p></div>{record_evidence(r,'../')}{source}<div class="actions"><button class="button outline" data-print>Print / Save as PDF <span aria-hidden="true">↓</span></button><a class="text-link" href="index.html">Back to all years ←</a></div></article>{cta("../")}</main>'''
 (ROOT/f'reports/{r["year"]}.html').write_text(page(f'{r["year"]} · {r["title"]}',body,'../',r['description']))
contact=f'''<main id="main"><div class="container"><section class="page-intro"><div class="breadcrumbs"><a href="index.html">Home</a> / Contact</div><p class="eyebrow">Contact Dost</p><h1>Questions about the work<br>or your donation?</h1><p>Ask about our reports, get help with a donation receipt, or find a way to get involved.</p></section><div class="contact-grid"><section class="contact-card" aria-labelledby="contact-email-heading"><p class="eyebrow">The Dost team</p><h2 id="contact-email-heading">Get in touch.</h2><a class="contact-email" href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><p>For general inquiries, donation questions, volunteering and partnerships, write to our team.</p><a class="button" href="mailto:{CONTACT_EMAIL}">Email the team {ARROW}</a><p class="contact-hint">This opens your email app. You can also copy the address into your preferred email service.</p></section><div class="contact-copy"><h2>How we can help.</h2><details open><summary>Donation receipts &amp; organization documents</summary><p>Include the donation date and the email address used to donate, or let us know which organization documents you need. Please do not send payment-card details.</p></details><details><summary>Volunteering &amp; partnerships</summary><p>Tell us about your interests, experience and how you would like to help. You can also explore our <a href="index.html#community">past community events</a>.</p></details><details><summary>Questions about an annual report</summary><p>Include the year and the part of the report you are asking about so we can help you find the right information.</p></details><p>For questions about information shared with Dost, see our <a href="privacy.html">privacy information</a> or email the team.</p></div></div></div></main>'''
(ROOT/'contact.html').write_text(page('Contact the team',contact))
privacy=f'''<main id="main"><div class="container privacy"><section class="page-intro"><div class="breadcrumbs"><a href="index.html">Home</a> / Privacy</div><p class="eyebrow">About this website</p><h1>Your information.</h1><p>This page describes the features included in this website.</p></section><h2>Contact messages</h2><p>Contact links open your email app with <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> as the recipient. The website does not collect or submit a contact form. When you send an email, Dost receives your email address and the information you choose to include. Share only what is needed for your question; your email provider’s privacy practices also apply.</p><h2>Donations</h2><p>The donation page embeds a Givebutter form. Givebutter processes donation and payment information entered into that form. You can also open the campaign directly on Givebutter. See <a href="https://givebutter.com/privacy">Givebutter’s privacy policy</a>.</p><h2>Reports and event links</h2><p>Source links include Medium, Facebook, Zeffy, GoFundMe and original project websites; event pages are hosted on Partiful. Those services have their own privacy practices. Source screenshots supplied by Dost are stored locally on this website. The report-summary download contains public summaries and links, without donor lists or private records.</p><h2>Local browsing</h2><p>The donation page loads Givebutter’s widget and related services, which may use cookies and collect information under Givebutter’s privacy policy. Other pages do not load the donation widget or site analytics. The local pages, photographs and report summaries can be viewed without an internet connection. Donations, external pages and sending email require an internet connection.</p><h2>Questions</h2><p>Use our <a href="contact.html">contact page</a> for questions about information shared with Dost.</p></div></main>'''
(ROOT/'privacy.html').write_text(page('Privacy',privacy))

# Load Givebutter only on the dedicated donation page, once per document.
donation=(ROOT/'content/donate.html').read_text().replace('{{GIVEBUTTER}}',GIVEBUTTER).replace('{{CONTACT_EMAIL}}',CONTACT_EMAIL)
widget_script=f'<script async src="{e(GIVEBUTTER_SCRIPT)}"></script>'
(ROOT/'donate.html').write_text(page('Support families in Afghanistan',donation,description='Give once or monthly to support food, medical care and women’s education in Afghanistan. Follow Dost’s annual updates to see how donations are used.',extra_head=widget_script))

(ROOT/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#203f34"/><text x="16" y="49" font-family="Georgia,serif" font-size="54" fill="#f8f7f1">d</text></svg>')
# A self-contained public summary archive, without site navigation or personal records.
summary_css='body{max-width:780px;margin:50px auto;padding:0 24px;font:17px/1.7 system-ui,sans-serif;color:#203f34;background:#f8f7f1}h1,h2{font-family:Georgia,serif;line-height:1.2}h1{font-size:42px}a{color:inherit}li{margin:12px 0}.note{padding:18px;background:#e7ecdf;font-size:14px}footer{border-top:1px solid #d9ded4;margin-top:30px;padding-top:20px;font-size:13px}'
summary_css+='img{max-width:100%;height:auto}figure{margin:18px 0}figcaption{font-size:12px;color:#657067}details{border:1px solid #d9ded4;padding:16px;margin:24px 0}summary{cursor:pointer}table{width:100%;border-collapse:collapse;font-size:14px}th,td{border-bottom:1px solid #d9ded4;padding:12px 8px;text-align:left}th{font-weight:600}.record-sources h2{font-size:24px}.record-sources>div{margin:18px 0}.sr-only{position:absolute;clip:rect(0,0,0,0);width:1px;height:1px;overflow:hidden}'
with zipfile.ZipFile(ROOT/'downloads/dost-report-archive.zip','w',zipfile.ZIP_DEFLATED) as archive_zip:
 links=[]
 for r in REPORTS:
  year=r['year'];links.append(f'<li><a href="{year}/summary.html">{year} — {e(r["title"])}</a> · {e(r["label"])}</li>')
  stats=''.join(f'<li><strong>{e(v)}</strong> — {e(l)}</li>' for v,l in r.get('metrics',[]))
  text=''.join(f'<p>{e(x)}</p>' for x in r.get('paragraphs',[r['description']]))+record_sections(r)
  offline_evidence=[]
  for item in r.get('evidence',[]):
   evidence_name='records/'+Path(item['src']).name
   archive_zip.write(ROOT/item['src'],f'dost-report-archive/{year}/{evidence_name}')
   offline_evidence.append(dict(item,src=evidence_name))
  text+=record_evidence({'evidence':offline_evidence})
  src=record_sources(r)
  if r.get('pdf'):
   archive_zip.write(ROOT/r['pdf'],f'dost-report-archive/{year}/report.pdf')
   src='<p><a href="report.pdf">Download the annual report PDF (available offline)</a></p>'+src
  doc=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dost · {year}</title><style>{summary_css}</style><body><a href="../START-HERE.html">← All years</a><p>DOST / {year} / {e(r["label"])}</p><h1>{e(r["title"])}</h1><ul>{stats}</ul>{text}<p class="note">{e(r["note"])}</p>{src}<footer>Prepared from the linked reports and records supplied by Dost. This is a summary, not the original report. Use your browser’s Print command to save a PDF.</footer></body></html>'
  archive_zip.writestr(f'dost-report-archive/{year}/summary.html',doc)
 archive_zip.writestr('dost-report-archive/START-HERE.html',f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dost report archive</title><style>{summary_css}</style><body><p>DOST / THE PUBLIC RECORD</p><h1>Annual report summaries</h1><p>Open any year below. These summaries work offline; the links to original reports require an internet connection.</p><p class="note">{archive_note} Full Medium articles, receipts and private donor records are not included.</p><ul>{"".join(links)}</ul><footer>Dost · Annual reporting archive.</footer></body></html>')
print(f'Built homepage, archive, {len(REPORTS)} annual pages, {len(PROGRAMS)} program pages, 3 team profiles, contact, privacy, donation page, and offline summary ZIP.')
