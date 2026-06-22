#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Venkateshwara Interiors — static HTML page generator.
Produces every page with consistent <head>, chrome placeholders and scripts.
Header / footer / action-bar are injected at runtime by assets/js/site.js,
so pages only carry their own <main> content.
"""
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = "assets/images/"

# ---------------------------------------------------------------- head/scaffold
def head(title, desc, page, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#0E2A2B">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{IMG}1.svg">
<link rel="icon" type="image/svg+xml" href="{IMG}favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Marcellus&family=Mukta:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{extra}</head>
<body data-page="{page}">
<header class="site-header"></header>
<main>
"""

FOOT = """</main>
<footer class="site-footer"></footer>
<script src="assets/js/config.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
<script src="assets/js/site.js"></script>
</body>
</html>
"""

def write(name, body_html, title, desc, extra=""):
    page = head(title, desc, name, extra) + body_html + FOOT
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote", name, f"({len(page)//1024} KB)")

# ---------------------------------------------------------------- small helpers
def ornament():
    return ('<div class="ornament reveal"><svg viewBox="0 0 24 24">'
            '<path d="M12 2l2.4 5.6L20 8l-4 4 1 6-5-3-5 3 1-6-4-4 5.6-.4z"/></svg></div>')

def eyebrow(t, center=False):
    c = " center" if center else ""
    return f'<span class="eyebrow{c}">{t}</span>'

def crumb(*parts):
    out = ['<a href="index.html">Home</a>']
    for i, (label, href) in enumerate(parts):
        out.append('<span class="sep">/</span>')
        out.append(f'<a href="{href}">{label}</a>' if href else f'<span>{label}</span>')
    return '<div class="crumb">' + "".join(out) + '</div>'

def banner(title, lead, img, *crumbs):
    return f"""<section class="banner">
  <div class="banner-art"><img src="{IMG}{img}.svg" alt="{html.escape(title)}"></div>
  <div class="geo-bg"></div>
  <div class="container reveal">
    <h1>{title}</h1>
    <p class="lead" style="color:#dfe7e2">{lead}</p>
    {crumb(*crumbs)}
  </div>
</section>"""

# feather-ish inline icons for feature blocks
FIC = {
 "ruler":'<path d="M3 8l13 13 5-5L8 3z"/><path d="M7 7l2 2M11 11l2 2M15 15l2 2"/>',
 "gem":'<path d="M6 3h12l3 6-9 12L3 9z"/><path d="M3 9h18M9 3l-3 6 6 12 6-12-3-6"/>',
 "leaf":'<path d="M4 20s1-9 9-13c5-2 7-2 7-2s0 2-2 7c-4 8-13 9-13 9z"/><path d="M4 20c4-4 7-6 10-7"/>',
 "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "shield":'<path d="M12 3l8 3v6c0 5-4 8-8 9-4-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 "spark":'<path d="M12 3v6M12 15v6M3 12h6M15 12h6"/><path d="M6 6l3 3M15 15l3 3M18 6l-3 3M9 15l-3 3"/>',
 "home":'<path d="M3 11l9-8 9 8M5 10v10h14V10"/>',
 "users":'<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3 3-5 6-5s6 2 6 5"/><path d="M16 6a3 3 0 0 1 0 6M21 20c0-2-1.5-4-4-4.5"/>',
 "palette":'<path d="M12 3a9 9 0 1 0 0 18c1 0 2-1 2-2 0-1.5-1-2-1-3s1-2 2-2h2a4 4 0 0 0 4-4c0-3.5-4-7-9-7z"/><circle cx="7.5" cy="11" r="1"/><circle cx="11" cy="7" r="1"/><circle cx="15.5" cy="8" r="1"/>',
 "cube":'<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M12 3v9l8 4.5M12 12L4 16.5"/>',
 "check":'<path d="M5 13l4 4L19 7"/>',
 "phone":'<path d="M5 4h4l1.5 5-2 1.5a12 12 0 0 0 5 5l1.5-2 5 1.5V20a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1z"/>',
}
def feat(icon, title, text, delay=0):
    d = f' data-delay="{delay}"' if delay else ""
    return f"""<div class="feat reveal r-zoom"{d}>
  <div class="ic"><svg viewBox="0 0 24 24">{FIC.get(icon, FIC['gem'])}</svg></div>
  <h3>{title}</h3><p>{text}</p></div>"""

def tickitem(t):
    return ('<li><svg class="ck" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>'
            f'<span>{t}</span></li>')

def step(no, title, text, delay=0):
    d = f' data-delay="{delay}"' if delay else ""
    return f'<div class="step reveal"{d}><div class="no">{no:02d}</div><h3>{title}</h3><p>{text}</p></div>'

def quote(text, name, role, av, stars=5, delay=0):
    d = f' data-delay="{delay}"' if delay else ""
    return f"""<div class="quote reveal"{d}>
  <div class="stars">{'★'*stars}{'☆'*(5-stars)}</div>
  <div class="qm">&ldquo;</div><p>{text}</p>
  <div class="who"><div class="av">{av}</div><div><b>{name}</b><span>{role}</span></div></div></div>"""

def acc(q, a, open_=False):
    o = " open" if open_ else ""
    return f"""<div class="acc{o}"><div class="acc-q">{q}<span class="pm"></span></div>
  <div class="acc-a"{' style="max-height:400px"' if open_ else ''}><p>{a}</p></div></div>"""

def lbimg(img, cap, cat=None):
    c = f' data-cat="{cat}"' if cat else ""
    return f"""<a class="m-item reveal" href="#"{c} data-lb="{IMG}{img}.svg" data-cap="{html.escape(cap)}">
  <img src="{IMG}{img}.svg" alt="{html.escape(cap)}" loading="lazy">
  <div class="m-cap">{cap}</div></a>"""

print("helpers ready")

# =====================================================================
# HOME
# =====================================================================
SERVICE_CARDS = [
    ("Modular Kitchen", "service-modular-kitchen.html", 3, "Ergonomic, easy-clean modular kitchens with smart storage and premium finishes."),
    ("False Ceiling", "service-false-ceiling.html", 4, "Layered POP & gypsum ceilings with cove lighting that transforms every room."),
    ("Living Room", "service-living-room.html", 5, "Statement living spaces — TV units, accent walls and warm Indian textures."),
    ("Bedroom", "service-bedroom.html", 6, "Restful master & guest bedrooms with wardrobes, panelling and mood lighting."),
    ("Pooja Room", "service-pooja-room.html", 7, "Serene, vastu-aligned mandirs in teak, marble and brass — the heart of the home."),
    ("Study Room", "service-study-room.html", 8, "Focused work-from-home and study corners with smart shelving and ergonomics."),
    ("TV Showcase", "service-tv-showcase.html", 9, "Floating consoles and showcase units that anchor your entertainment wall."),
    ("Dining Room", "service-dining-room.html", 10, "Inviting dining zones with crockery units, panelling and feature lighting."),
    ("Cupboards & Wardrobes", "service-cupboards-wardrobes.html", 11, "Sliding & openable wardrobes engineered to the millimetre for your space."),
    ("Kids Room", "service-kids-room.html", 12, "Playful, safe and clever rooms that grow with your child."),
    ("Toilet & Bathroom", "service-toilet-bathroom.html", 13, "Spa-like bathrooms with quality fittings, waterproofing and elegant tiling."),
    ("Commercial", "service-commercial.html", 14, "Offices, retail and hospitality interiors that work as hard as you do."),
]

def home():
    cards = "\n".join(
        f"""<a class="card reveal" data-delay="{(i%3)+1}" href="{href}">
  <div class="ph"><span class="tag">{str(i+1).zfill(2)}</span><img src="{IMG}{img}.svg" alt="{name} interiors" loading="lazy"></div>
  <div class="body"><h3>{name} Interiors</h3><p>{desc}</p>
  <span class="more">Explore <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div></a>"""
        for i, (name, href, img, desc) in enumerate(SERVICE_CARDS))

    feats = "\n".join([
        feat("palette", "Bespoke Indian Design", "Every layout is drawn around your family, your rituals and the way light moves through your home — never a copy-paste template.", 1),
        feat("cube", "Turnkey Execution", "From civil and false ceiling to the final cushion, we hand you a finished home. One team, one accountable point of contact.", 2),
        feat("gem", "Premium, Honest Materials", "BWP/BWR ply, branded laminates, soft-close hardware and quartz tops — specified in writing, no surprises on site.", 3),
        feat("clock", "On-Time, On-Budget", "Detailed 3D sign-off and a day-wise schedule mean you move in when we promise, at the price we quote.", 4),
        feat("leaf", "Vastu-Friendly Planning", "Pooja placement, kitchen orientation and entrances planned with respect for tradition — without compromising on modern living.", 5),
        feat("shield", "Warranty & After-Care", "Up to 10-year warranty on modular cabinetry and a responsive service team long after handover.", 6),
    ])

    steps = "\n".join([
        step(1, "Consult & Measure", "We listen to how you live, capture an exact site survey and set a clear budget band.", 1),
        step(2, "Design & 3D Walkthrough", "Mood boards, material samples and photoreal 3D views until every corner feels right.", 2),
        step(3, "Production & Build", "Factory-made modular units and disciplined on-site work under daily supervision.", 3),
        step(4, "Styling & Handover", "Lighting, décor and a spotless deep-clean — we hand over the keys to a home, not a site.", 4),
    ])

    quotes = "\n".join([
        quote("They reimagined our 2BHK in Velachery beautifully. The modular kitchen is a dream to cook in and the pooja room brings the whole family together.", "Lakshmi &amp; Suresh", "Velachery, Chennai", "L", 5, 1),
        quote("Professional from day one. The 3D views matched the final result almost exactly, and they finished a week early. Highly recommended.", "Arjun Menon", "OMR, Chennai", "A", 5, 2),
        quote("We did our whole villa interiors with them. Honest pricing, premium materials and a team that genuinely cares about detailing.", "Priya Nair", "ECR, Chennai", "P", 5, 3),
    ])

    return f"""
<section class="hero">
  <div class="hero-art"><img src="{IMG}1.svg" alt="Luxury Indian living room interior"></div>
  <div class="geo-bg"></div>
  <div class="container">
    <div class="hero-inner reveal">
      {eyebrow("Premium Interior Design Studio")}
      <h1>Interiors that feel <span class="gold">like home</span>, crafted for India.</h1>
      <p class="lead">From modular kitchens and serene pooja rooms to complete turnkey homes — <span data-cfg="businessName">Venkateshwara Interiors</span> blends timeless Indian warmth with modern, liveable design.</p>
      <div class="hero-cta">
        <a class="btn btn-gold" href="contact.html">Book a Free Consultation <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
        <a class="btn btn-ghost" href="gallery-images.html">View Our Work</a>
      </div>
    </div>
  </div>
  <a class="scroll-cue" href="#intro" aria-label="Scroll down"><span></span></a>
</section>

<section class="section" id="intro">
  <div class="geo-bg faint"></div>
  <div class="container">
    <div class="split">
      <div class="split-media reveal r-left">
        <img src="{IMG}2.svg" alt="About Venkateshwara Interiors">
        <span class="frame-line"></span>
        <span class="media-badge">Since <span data-cfg="establishedYear">2009</span></span>
      </div>
      <div class="reveal r-right">
        {eyebrow("Who We Are")}
        <h2>A design studio rooted in craft, built for modern Indian living.</h2>
        <p class="lead">We are a full-service interior design and turnkey execution studio. For over a decade we have shaped homes and workspaces that are equal parts beautiful and practical — designed around real families, real budgets and real life.</p>
        <ul class="ticks">
          {tickitem("End-to-end design &amp; execution under one roof")}
          {tickitem("Transparent, itemised quotations — no hidden costs")}
          {tickitem("In-house factory for precision modular furniture")}
          {tickitem("Vastu-sensitive, family-first space planning")}
        </ul>
        <a class="btn btn-gold" href="about.html">More About Us <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
      </div>
    </div>
  </div>
</section>

<section class="section dark cta-band" style="padding-block:clamp(48px,6vw,80px)">
  <div class="banner-art"><img src="{IMG}28.svg" alt="" style="width:100%;height:100%;object-fit:cover;opacity:.18"></div>
  <div class="geo-bg"></div>
  <div class="container">
    <div class="stats">
      <div class="stat reveal"><div class="num" data-count="1600" data-suffix="+">0</div><div class="lbl">Homes Designed</div></div>
      <div class="stat reveal" data-delay="1"><div class="num" data-count="15" data-suffix="+">0</div><div class="lbl">Years of Craft</div></div>
      <div class="stat reveal" data-delay="2"><div class="num" data-count="12">0</div><div class="lbl">Interior Specialities</div></div>
      <div class="stat reveal" data-delay="3"><div class="num" data-count="98" data-suffix="%">0</div><div class="lbl">Client Referrals</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="geo-bg faint"></div>
  <div class="container">
    <div class="center" style="max-width:760px;margin-inline:auto">
      {ornament()}{eyebrow("What We Do", True)}
      <h2 class="reveal">Twelve specialities. One seamless home.</h2>
      <p class="lead reveal">Pick a single room or hand us the whole house — our specialists cover every interior surface, fitting and finish your home needs.</p>
    </div>
    <div class="grid g3" style="margin-top:48px">
      {cards}
    </div>
  </div>
</section>

<section class="section dark">
  <div class="geo-bg"></div>
  <div class="container">
    <div class="center" style="max-width:720px;margin-inline:auto">
      {eyebrow("Why Choose Us", True)}
      <h2 class="reveal">The difference is in the detailing.</h2>
      <p class="lead reveal">Anyone can fit a kitchen. We obsess over the things you feel every day — the soft-close drawer, the glare-free light, the handle that sits just right.</p>
    </div>
    <div class="grid g3" style="margin-top:48px">{feats}</div>
  </div>
</section>

<section class="section">
  <div class="geo-bg faint"></div>
  <div class="container">
    <div class="center" style="max-width:720px;margin-inline:auto">
      {ornament()}{eyebrow("How It Works", True)}
      <h2 class="reveal">A calm, four-step journey to your new home.</h2>
    </div>
    <div class="steps" style="margin-top:52px">{steps}</div>
  </div>
</section>

<section class="section dark">
  <div class="banner-art"><img src="{IMG}30.svg" alt="" style="width:100%;height:100%;object-fit:cover;opacity:.14"></div>
  <div class="geo-bg"></div>
  <div class="container">
    <div class="center" style="max-width:720px;margin-inline:auto">
      {eyebrow("Loved By Families", True)}
      <h2 class="reveal">Homes we&rsquo;ve made, in their own words.</h2>
    </div>
    <div class="grid g3" style="margin-top:48px">{quotes}</div>
  </div>
</section>

<section class="section cta-band dark" style="background:var(--teal)">
  <div class="geo-bg"></div>
  <div class="container center">
    <h2 class="reveal" style="color:var(--ivory);max-width:18ch;margin-inline:auto">Ready to design a home you&rsquo;ll love coming back to?</h2>
    <p class="lead reveal" style="margin-inline:auto">Book a free, no-obligation consultation. We&rsquo;ll visit, measure and share ideas — the first conversation is always on us.</p>
    <div class="hero-cta reveal" style="justify-content:center;margin-top:8px">
      <a class="btn btn-gold" href="contact.html">Get a Free Quote</a>
      <a class="btn btn-ghost" data-cfg-href="phoneRaw" href="#">Call <span data-cfg="phone">+91 98840 12345</span></a>
    </div>
  </div>
</section>
"""

print("home() defined")

# =====================================================================
# ABOUT
# =====================================================================
def about():
    feats = "\n".join([
        feat("gem","Our Mission","To make thoughtful, high-quality interior design accessible to every Indian family — delivered honestly, on time and built to last.",1),
        feat("spark","Our Vision","To be South India&rsquo;s most trusted home interiors studio, known for craft, integrity and homes that feel personal.",2),
        feat("home","Our Values","Listen first. Quote honestly. Build cleanly. Stand behind our work long after the keys change hands.",3),
    ])
    steps = "\n".join([
        step(1,"Discovery","A relaxed conversation about your family, lifestyle, budget and the feeling you want at home.",1),
        step(2,"Design","Space planning, material palettes and photoreal 3D walkthroughs refined until you love every view.",2),
        step(3,"Build","Factory-made modular units and supervised on-site work, with regular updates and clean handovers.",3),
        step(4,"Care","Styling, handover and a warranty-backed service team that stays with you for years.",4),
    ])
    return f"""
{banner("About Venkateshwara Interiors", "Craft, honesty and a deep love for the way Indian families live — that is what we build on, every single project.", 2, ("About Us","about.html"))}

<section class="section">
  <div class="geo-bg faint"></div>
  <div class="container">
    <div class="split">
      <div class="reveal r-left">
        {eyebrow("Our Story")}
        <h2>From a small studio to a thousand happy homes.</h2>
        <p class="lead">What began as a two-person design practice has grown into a full turnkey interiors studio — but our belief has never changed: a home should be designed around the people who live in it.</p>
        <p>We started by designing modular kitchens for families in our neighbourhood. Word travelled, because we did three things well — we listened, we quoted honestly, and we finished what we started. Today our in-house design and production teams deliver complete homes, villas and commercial spaces across the city, with the same hands-on care we began with.</p>
        <ul class="ticks">
          {tickitem("Established <span data-cfg='establishedYear'>2009</span> &mdash; over a decade of detailing")}
          {tickitem("In-house design studio &amp; modular production unit")}
          {tickitem("Dedicated project manager on every home")}
          {tickitem("Hundreds of referrals &mdash; our best marketing")}
        </ul>
      </div>
      <div class="split-media reveal r-right">
        <img src="{IMG}29.svg" alt="Our design process">
        <span class="frame-line"></span>
        <span class="media-badge">Design &middot; Build &middot; Care</span>
      </div>
    </div>
  </div>
</section>

<section class="section dark cta-band" style="padding-block:clamp(48px,6vw,80px)">
  <div class="geo-bg"></div>
  <div class="container">
    <div class="stats">
      <div class="stat reveal"><div class="num" data-count="1600" data-suffix="+">0</div><div class="lbl">Homes Designed</div></div>
      <div class="stat reveal" data-delay="1"><div class="num" data-count="15" data-suffix="+">0</div><div class="lbl">Years of Craft</div></div>
      <div class="stat reveal" data-delay="2"><div class="num" data-count="60" data-suffix="+">0</div><div class="lbl">Skilled Craftspeople</div></div>
      <div class="stat reveal" data-delay="3"><div class="num" data-count="98" data-suffix="%">0</div><div class="lbl">Client Referrals</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="geo-bg faint"></div>
  <div class="container">
    <div class="center" style="max-width:720px;margin-inline:auto">
      {ornament()}{eyebrow("What Drives Us", True)}
      <h2 class="reveal">Beautiful homes, built on principles.</h2>
    </div>
    <div class="grid g3" style="margin-top:48px">{feats}</div>
  </div>
</section>

<section class="section dark">
  <div class="geo-bg"></div>
  <div class="container">
    <div class="center" style="max-width:720px;margin-inline:auto">
      {eyebrow("How We Work", True)}
      <h2 class="reveal">A process designed to keep you relaxed.</h2>
      <p class="lead reveal">No jargon, no surprises — just clear stages, regular updates and a finished home you can be proud of.</p>
    </div>
    <div class="steps" style="margin-top:52px">{steps}</div>
  </div>
</section>

<section class="section cta-band dark" style="background:var(--teal)">
  <div class="geo-bg"></div>
  <div class="container center">
    <h2 class="reveal" style="color:var(--ivory)">Let&rsquo;s design your story next.</h2>
    <p class="lead reveal" style="margin-inline:auto">Tell us about your home and your budget. We&rsquo;ll show you what&rsquo;s possible — beautifully.</p>
    <a class="btn btn-gold reveal" href="contact.html">Start Your Project</a>
  </div>
</section>
"""

# =====================================================================
# SERVICES OVERVIEW
# =====================================================================
def services():
    cards = "\n".join(
        f"""<a class="card reveal" data-delay="{(i%3)+1}" href="{href}">
  <div class="ph"><span class="tag">{str(i+1).zfill(2)}</span><img src="{IMG}{img}.svg" alt="{name} interiors" loading="lazy"></div>
  <div class="body"><h3>{name} Interiors</h3><p>{desc}</p>
  <span class="more">View Service <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div></a>"""
        for i, (name, href, img, desc) in enumerate(SERVICE_CARDS))
    return f"""
{banner("Our Interior Services", "Twelve dedicated specialities, one accountable team — choose a single room or hand us the whole home.", 5, ("Services","services.html"))}

<section class="section">
  <div class="geo-bg faint"></div>
  <div class="container">
    <div class="center" style="max-width:760px;margin-inline:auto">
      {ornament()}{eyebrow("Full-Service Interiors", True)}
      <h2 class="reveal">Everything your home needs, under one roof.</h2>
      <p class="lead reveal">From the kitchen you cook in to the pooja room you pray in, each speciality below is handled by a focused team — designed, manufactured and installed to the same exacting standard.</p>
    </div>
    <div class="grid g3" style="margin-top:48px">{cards}</div>
  </div>
</section>

<section class="section cta-band dark" style="background:var(--teal)">
  <div class="geo-bg"></div>
  <div class="container center">
    <h2 class="reveal" style="color:var(--ivory)">Not sure where to start?</h2>
    <p class="lead reveal" style="margin-inline:auto">Book a free consultation and we&rsquo;ll help you prioritise — room by room or a complete turnkey plan.</p>
    <a class="btn btn-gold reveal" href="contact.html">Talk To A Designer</a>
  </div>
</section>
"""

print("about/services defined")

# =====================================================================
# SERVICE PAGE DATA (tailored, original copy per speciality)
# =====================================================================
SERVICE_PAGES = {
 "service-modular-kitchen.html": dict(
   name="Modular Kitchen", img=3, gallery=[3,16,10],
   lead="Hard-working, easy-clean and beautiful — modular kitchens engineered around the way Indian families really cook.",
   intro="A great Indian kitchen has to survive daily tadka, monsoon humidity and a busy joint family — and still look stunning. We design modular kitchens that balance heavy-duty function with finishes you&rsquo;ll be proud to show off, from compact 2BHK galleys to sprawling island kitchens.",
   benefits=["Moisture-resistant BWP plywood carcass built for Indian conditions","Smart corner units, tall pantry &amp; built-in waste solutions","Soft-close hinges &amp; channels from trusted hardware brands","Quartz / granite counters with anti-stain treatment","Designed around the work-triangle for effortless cooking","Chimney, hob &amp; appliance integration planned in advance"],
   feats=[("cube","Layout That Works","L-shaped, parallel, U or island — we plan the layout around your cooking style, not a catalogue."),("gem","Premium Finishes","Acrylic, laminate, PU or membrane shutters in finishes that wipe clean and resist oil."),("shield","10-Year Warranty","Confidence built in — our modular cabinetry carries up to a decade of warranty.")],
   faq=[("How long does a modular kitchen take?","Most kitchens are designed, manufactured and installed within 4&ndash;6 weeks of final 3D sign-off, depending on size and finish."),("Can you work with my existing plumbing and electrical points?","Yes. We survey existing points and either design around them or relocate them as part of the scope, planned upfront so there are no surprises."),("What is the difference between acrylic and laminate shutters?","Acrylic gives a high-gloss, seamless mirror finish; laminate is more budget-friendly and extremely durable. We&rsquo;ll show you samples of both against your lighting.")]),

 "service-false-ceiling.html": dict(
   name="False Ceiling", img=4, gallery=[4,21,5],
   lead="Layered ceilings and cove lighting that add depth, hide the clutter and completely change how a room feels.",
   intro="The ceiling is the one surface everyone forgets and everyone notices. Our gypsum and POP false ceilings conceal wiring and ducting, soften harsh light and create the warm, layered glow that makes a room feel finished and luxurious.",
   benefits=["Branded gypsum board &amp; POP with clean, crack-resistant finishes","Concealed cove, profile and spot lighting design","Conceals AC ducting, wiring and structural beams","Improved acoustics and a cooler-feeling room","Moisture-resistant boards for kitchens &amp; bathrooms","Designed to complement your furniture and theme"],
   feats=[("spark","Lighting By Design","We design the ceiling and the lighting together, so coves, spots and pendants land exactly where they should."),("palette","Clean Detailing","Crisp lines, neat corners and seamless joints — the difference between a ceiling that looks built-in and one that looks bolted-on."),("leaf","Cooler Rooms","A well-planned false ceiling traps heat and improves AC efficiency, a real benefit in our climate.")],
   faq=[("Will a false ceiling reduce my room height too much?","A typical drop is just 4&ndash;6 inches. For low rooms we use peripheral or floating designs that keep the centre open and airy."),("Is gypsum or POP better?","Gypsum is factory-made, faster and cleaner to install; POP allows more custom curves. We&rsquo;ll recommend based on your design and timeline."),("Does it require much maintenance?","Very little. A good false ceiling lasts years; we use quality boards and proper framing so there&rsquo;s no sagging or cracking.")]),

 "service-living-room.html": dict(
   name="Living Room", img=5, gallery=[5,17,1],
   lead="The room where your home makes its first impression — designed to be warm, social and unmistakably yours.",
   intro="Your living room hosts everything — festivals, guests, lazy Sundays and late-night chats. We design living spaces that feel generous and welcoming, anchored by a stunning TV unit or accent wall and layered with the textures, colour and light that make a house feel like home.",
   benefits=["Feature TV units, panelling &amp; accent walls","Layered lighting — ambient, task and accent","Custom seating layouts for family and guests","Display, storage and console units that hide clutter","Curtains, rugs and décor styled to tie it together","Designs that flex from everyday to festival-ready"],
   feats=[("palette","A Focal Point","Every great living room has a hero — a panelled TV wall, a textured backdrop or a statement console. We design yours."),("home","Made For Gathering","Seating and circulation planned so conversation flows and guests never feel cramped."),("gem","Layered Warmth","Wood, fabric, brass and greenery combined for that warm, collected Indian-luxe feel.")],
   faq=[("Can you design around my existing sofa and TV?","Absolutely. We can build the scheme around pieces you love and replace or restyle only what&rsquo;s needed."),("Do you handle the lighting and false ceiling too?","Yes — living rooms are best designed as a whole, so ceiling, lighting, units and décor all come together in one plan."),("How do I make a small living room feel bigger?","Smart mirrors, lighter palettes, floating units and the right lighting do wonders. We specialise in making compact city homes feel spacious.")]),

 "service-bedroom.html": dict(
   name="Bedroom", img=6, gallery=[6,18,12],
   lead="A calm, clutter-free retreat — wardrobes, panelling and soft lighting designed for genuine rest.",
   intro="Your bedroom should be the quietest, most restful room in the house. We design serene master and guest bedrooms with generous wardrobes, gentle headboard panelling and warm, dimmable lighting — storage-rich but never busy.",
   benefits=["Spacious sliding or openable wardrobes","Upholstered headboards &amp; wall panelling","Bedside, reading and ambient lighting","Dressing units, lofts and hidden storage","Soothing, sleep-friendly colour palettes","Optional study or vanity nooks"],
   feats=[("cube","Storage, Solved","Floor-to-ceiling wardrobes and clever lofts mean a place for everything and a tidy room every morning."),("leaf","Restful By Design","Soft palettes, warm lighting and uncluttered surfaces designed to help you switch off."),("gem","Quiet Luxury","Fluted panels, fabric headboards and brass accents for a hotel-suite feel at home.")],
   faq=[("Sliding or openable wardrobe — which is better?","Sliding wardrobes save floor space and look sleek; openable wardrobes give full access and slightly more internal storage. We&rsquo;ll suggest based on your room width."),("Can you include a dressing area?","Yes — dressers, mirror units and even compact walk-in zones can be worked in, space permitting."),("Do you design kids&rsquo; and guest bedrooms too?","We do. Each bedroom is tailored to who uses it — see our dedicated Kids Room service for the little ones.")]),

 "service-pooja-room.html": dict(
   name="Pooja Room", img=7, gallery=[7,20,2],
   lead="The spiritual heart of your home — serene, vastu-aligned mandirs crafted in teak, marble and brass.",
   intro="A pooja room deserves more care than any other corner of the home. We design tranquil, vastu-sensitive mandirs — from elegant niche units in apartments to dedicated prayer rooms — using teak, marble, brass and considered lighting to create a space that feels truly sacred.",
   benefits=["Vastu-aligned placement and orientation","Teak, marble &amp; brass detailing with carved accents","Concealed storage for lamps, books and samagri","Soft, warm lighting and ventilation for diyas","Compact niche designs for apartments","Easy-to-clean, durable finishes"],
   feats=[("leaf","Vastu-Sensitive","Placement, door direction and seating planned with respect for tradition and your family&rsquo;s practices."),("gem","Sacred Craft","Hand-detailed jaali, carved columns and brass inlays that elevate daily prayer."),("spark","Gentle Light","Warm, glare-free lighting and proper ventilation designed for diyas and aarti.")],
   faq=[("Where should the pooja room ideally be placed?","The north-east is traditionally preferred, with the idols facing west so you face east while praying. We adapt this to your home&rsquo;s layout sensibly."),("Can you design a pooja unit for a small apartment?","Yes — wall-mounted niches and slim corner mandirs give a complete, sacred feel even in compact homes."),("What materials are best for a pooja room?","Teak and marble age beautifully and are easy to maintain; brass adds traditional warmth. We&rsquo;ll balance tradition with upkeep.")]),

 "service-study-room.html": dict(
   name="Study Room", img=8, gallery=[8,24,11],
   lead="Focused, ergonomic study and work-from-home spaces that make concentration come easily.",
   intro="Whether it&rsquo;s a child&rsquo;s study, a home office or a quiet reading corner, a well-designed study changes how productive you feel. We create ergonomic, well-lit work zones with smart shelving and cable management — calm spaces built for deep focus.",
   benefits=["Ergonomic desks at the right working height","Open and closed shelving for books &amp; files","Glare-free, eye-friendly task lighting","Concealed cable management for a clean desk","Pin-up boards, drawers and storage built in","Compact designs that fit into bedrooms or nooks"],
   feats=[("spark","Built For Focus","Quiet placement, good light and tidy storage — the conditions that make concentration effortless."),("cube","Smart Storage","Shelves, drawers and cabinets sized for books, files and devices, so the desk stays clear."),("clock","Work-From-Home Ready","Proper ergonomics and cable management for long, comfortable working days.")],
   faq=[("Can you fit a study into an existing bedroom?","Yes — a slim desk-and-shelf combination or a fold-away unit can create a full study without crowding the room."),("Do you design for dual use, like study plus guest room?","We do. Murphy beds, fold-down desks and modular units let one room do two jobs gracefully."),("What lighting is best for a study?","A combination of soft ambient light and a focused, glare-free task lamp protects the eyes during long hours.")]),

 "service-tv-showcase.html": dict(
   name="TV Showcase", img=9, gallery=[9,22,5],
   lead="Floating consoles and showcase units that turn a blank wall into the centrepiece of your living space.",
   intro="The TV wall is where every eye in the room lands. We design floating consoles, panelled backdrops and integrated showcase units that hide the wiring, display what you love and give your living room a confident, finished focal point.",
   benefits=["Floating &amp; wall-mounted console designs","Panelled or textured TV backdrop walls","Concealed wiring and device storage","Integrated display niches with accent lighting","Combination units with bookshelves &amp; bar","Finishes coordinated with your living room theme"],
   feats=[("palette","Statement Wall","A fluted, stone or veneer backdrop that frames your TV and lifts the whole room."),("cube","Clutter Hidden","Set-top boxes, consoles and a tangle of wires — all tucked neatly out of sight."),("spark","Accent Lighting","Backlighting and niche spots that make the unit glow after dark.")],
   faq=[("Can you hide all the cables and devices?","Yes — concealed conduits and ventilated cabinets keep wires and gadgets completely out of view while staying accessible."),("Can the unit double as storage?","Definitely. We often combine the TV unit with drawers, display niches, bookshelves or a small bar."),("Will it suit a wall-mounted TV?","Whether wall-mounted or on a console, we design the backdrop and unit to suit your screen size and seating distance.")]),

 "service-dining-room.html": dict(
   name="Dining Room", img=10, gallery=[10,19,3],
   lead="Inviting dining zones with crockery units and feature lighting — where the family actually gathers.",
   intro="Meals are where the day comes together. We design warm, inviting dining areas — whether a dedicated room or a smart open-plan zone — complete with crockery and display units, panelled backdrops and a statement light that draws everyone to the table.",
   benefits=["Crockery, display &amp; storage units","Panelled or textured feature walls","Statement pendant &amp; cove lighting","Space-smart layouts for open-plan homes","Mirror and partition designs to define the zone","Durable, easy-clean surfaces"],
   feats=[("home","A Place To Gather","Layouts that seat the whole family comfortably and keep serving easy."),("gem","Display &amp; Store","Crockery units and sideboards that show off your best and hide the rest."),("spark","Light The Table","A well-chosen pendant over the table instantly makes a dining area feel special.")],
   faq=[("I have an open kitchen-dining space — can you define the dining zone?","Yes — a change in ceiling, lighting, a rug or a slim partition can beautifully separate dining from the kitchen and living areas."),("Can you design around my existing dining table?","Of course. We build the crockery units, backdrop and lighting to complement a table you already love."),("What&rsquo;s a good lighting choice for dining?","A statement pendant at the right height over the table, supported by soft ambient ceiling light, is our go-to recipe.")]),

 "service-cupboards-wardrobes.html": dict(
   name="Cupboards & Wardrobes", img=11, gallery=[11,23,6],
   lead="Sliding and openable wardrobes engineered to the millimetre — maximum storage, minimum fuss.",
   intro="Good storage is invisible — it just makes life tidier. We design and manufacture sliding and openable wardrobes and cupboards that use every inch of your space intelligently, with internal layouts planned around exactly what you own.",
   benefits=["Sliding &amp; openable wardrobe systems","Custom internals — shelves, drawers, hanging, lofts","Mirror, laminate, acrylic &amp; veneer shutters","Soft-close, anti-rust premium hardware","Moisture-resistant ply for long life","Floor-to-ceiling designs that maximise storage"],
   feats=[("cube","Every Inch Used","Internal layouts planned around your wardrobe — saree drawers, hanging zones, accessory trays and more."),("shield","Built To Last","Quality ply, branded channels and soft-close hardware mean drawers that glide for years."),("palette","Your Finish","Sleek sliding glass, warm veneer or budget-friendly laminate — finished to match your room.")],
   faq=[("How much storage can I get in a sliding wardrobe?","A great deal — we design the internals (drawers, shelves, hanging rods, lofts) precisely around your belongings to maximise usable space."),("Are wardrobes made on-site or in a factory?","We manufacture in our factory for precision and finish, then install on-site cleanly — far better quality than fully site-made carpentry."),("Can you add mirrors and lighting?","Yes — mirror shutters, internal sensor lights and dressing zones can all be built in.")]),

 "service-kids-room.html": dict(
   name="Kids Room", img=12, gallery=[12,25,6],
   lead="Playful, safe and clever rooms that spark imagination today and grow with your child tomorrow.",
   intro="Children&rsquo;s rooms need to do a lot — sleep, study, play and storage — and change as they grow. We design fun, safe and surprisingly practical kids&rsquo; rooms with rounded edges, non-toxic finishes and smart, flexible storage that adapts over the years.",
   benefits=["Rounded edges and child-safe, non-toxic finishes","Bunk, loft and space-saving bed options","Study desks that grow with your child","Loads of toy, book and clothes storage","Playful themes, colours and wall graphics","Flexible designs that adapt as they grow"],
   feats=[("shield","Safe &amp; Sound","Rounded corners, sturdy fixings and low-VOC finishes designed with little ones in mind."),("cube","Clever Storage","Beds with drawers, loft units and toy stores that keep the chaos beautifully contained."),("spark","Room To Grow","Modular pieces and timeless bases that adapt from toddler to teenager.")],
   faq=[("Are the materials used safe for children?","Yes — we use low-VOC, child-safe finishes, rounded edges and secure fittings throughout kids&rsquo; rooms."),("Can the room adapt as my child grows?","We design with growth in mind — adjustable desks, modular storage and timeless bases that just need restyling later, not rebuilding."),("Can you do a shared room for two children?","Absolutely — bunk beds, twin study zones and divided storage make shared rooms work smoothly.")]),

 "service-toilet-bathroom.html": dict(
   name="Toilet & Bathroom", img=13, gallery=[13,26,4],
   lead="Spa-like bathrooms with quality fittings, sound waterproofing and elegant, easy-clean tiling.",
   intro="A well-designed bathroom is a small daily luxury. We create clean, modern toilets and spa-like bathrooms with quality sanitaryware, dependable waterproofing, smart storage and tiling that&rsquo;s as practical as it is beautiful.",
   benefits=["Reliable waterproofing done right","Branded sanitaryware &amp; CP fittings","Elegant, slip-resistant tiling layouts","Vanity units with concealed storage","Glass partitions and shower enclosures","Good ventilation and task lighting"],
   feats=[("shield","Waterproofing First","The part you never see matters most — we get the membrane and slopes right so leaks never start."),("gem","Spa Feel","Considered tiling, niche shelves and warm lighting turn a daily routine into a small luxury."),("cube","Smart Storage","Vanity units and mirror cabinets keep essentials handy and counters clear.")],
   faq=[("How important is waterproofing, really?","It&rsquo;s the single most important step. We use proven membranes and correct floor slopes so you never face seepage or damage later."),("Can you renovate a bathroom without a full demolition?","In many cases, yes — surface renovations and refits are possible. We&rsquo;ll assess and recommend the least disruptive route."),("Do you provide the sanitaryware and fittings?","We can supply and install branded sanitaryware and CP fittings, or work with pieces you&rsquo;ve chosen — your call.")]),

 "service-commercial.html": dict(
   name="Commercial", img=14, gallery=[14,27,9],
   lead="Offices, retail and hospitality interiors that look sharp, work hard and reflect your brand.",
   intro="Your space is your brand&rsquo;s first handshake. We design and execute commercial interiors — offices, clinics, showrooms, retail and hospitality — that balance brand identity, staff wellbeing and practical, durable function, delivered on tight commercial timelines.",
   benefits=["Office, retail, clinic &amp; hospitality fit-outs","Brand-aligned design and signage","Durable, high-traffic materials and finishes","Efficient space planning &amp; workstations","Reception, cabin and meeting room design","Project delivery on commercial timelines"],
   feats=[("users","Brand In Space","Interiors that tell your brand story the moment someone walks in."),("shield","Built For Traffic","Hard-wearing finishes and detailing that look good after years of daily use."),("clock","On Schedule","We understand downtime costs money — disciplined planning keeps fit-outs on time.")],
   faq=[("Can you work outside business hours to avoid downtime?","Yes — for live retail and offices we plan phased and after-hours work to minimise disruption to your operations."),("Do you handle electrical, networking and HVAC coordination?","We coordinate the full fit-out including services, working with your consultants or ours to deliver a turnkey space."),("Can the design reflect our brand guidelines?","Absolutely — we design to your brand palette, materials and signage so the space feels unmistakably yours.")]),
}

def service_page(fname, d):
    name = d["name"]
    benefits = "\n".join(tickitem(b) for b in d["benefits"])
    feats = "\n".join(feat(ic, t, x, i+1) for i,(ic,t,x) in enumerate(d["feats"]))
    faqs = "\n".join(acc(q, a, i==0) for i,(q,a) in enumerate(d["faq"]))
    g = d["gallery"]
    gal = "\n".join(
        f"""<a class="m-item reveal" data-delay="{i+1}" href="#" data-lb="{IMG}{n}.svg" data-cap="{name} Interiors &mdash; design {n}">
  <img src="{IMG}{n}.svg" alt="{name} interior design {n}" loading="lazy">
  <div class="m-cap">{name} &middot; {str(n).zfill(2)}</div></a>"""
        for i, n in enumerate(g))
    steps = "\n".join([
        step(1,"Consultation","We understand your needs, space and budget, and capture exact measurements.",1),
        step(2,"3D Design","Detailed drawings, material samples and a photoreal 3D walkthrough for your approval.",2),
        step(3,"Manufacture &amp; Build","Factory-made units and supervised installation, finished cleanly and on schedule.",3),
        step(4,"Handover &amp; Care","Styling, a final check and a warranty-backed service team that stays with you.",4),
    ])
    return f"""
{banner(name + " Interiors", d['lead'], d['img'], ("Services","services.html"), (name, fname))}

<section class="section">
  <div class="geo-bg faint"></div>
  <div class="container">
    <div class="split">
      <div class="split-media reveal r-left">
        <img src="{IMG}{d['img']}.svg" alt="{name} interior design">
        <span class="frame-line"></span>
        <span class="media-badge">{name}</span>
      </div>
      <div class="reveal r-right">
        {eyebrow(name + " Interiors")}
        <h2>{name} interiors, designed around you.</h2>
        <p class="lead">{d['intro']}</p>
        <ul class="ticks">{benefits}</ul>
        <a class="btn btn-gold" href="contact.html">Get a Free Quote <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
      </div>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="geo-bg"></div>
  <div class="container">
    <div class="center" style="max-width:680px;margin-inline:auto">
      {eyebrow("Why Our " + name, True)}
      <h2 class="reveal">Built well, finished beautifully.</h2>
    </div>
    <div class="grid g3" style="margin-top:48px">{feats}</div>
  </div>
</section>

<section class="section">
  <div class="geo-bg faint"></div>
  <div class="container">
    <div class="center" style="max-width:680px;margin-inline:auto">
      {ornament()}{eyebrow("Recent Work", True)}
      <h2 class="reveal">A glimpse of our {name.lower()} projects.</h2>
    </div>
    <div class="masonry" style="margin-top:44px;columns:3">{gal}</div>
  </div>
</section>

<section class="section dark">
  <div class="geo-bg"></div>
  <div class="container">
    <div class="center" style="max-width:680px;margin-inline:auto">
      {eyebrow("How We Deliver", True)}
      <h2 class="reveal">From first idea to final handover.</h2>
    </div>
    <div class="steps" style="margin-top:52px">{steps}</div>
  </div>
</section>

<section class="section">
  <div class="geo-bg faint"></div>
  <div class="container" style="max-width:840px">
    <div class="center">{eyebrow("Good To Know", True)}<h2 class="reveal">{name} &mdash; your questions, answered.</h2></div>
    <div style="margin-top:40px">{faqs}</div>
  </div>
</section>

<section class="section cta-band dark" style="background:var(--teal)">
  <div class="geo-bg"></div>
  <div class="container center">
    <h2 class="reveal" style="color:var(--ivory)">Let&rsquo;s plan your {name.lower()}.</h2>
    <p class="lead reveal" style="margin-inline:auto">Share your space and budget — we&rsquo;ll come back with ideas, materials and a transparent quote.</p>
    <div class="hero-cta reveal" style="justify-content:center">
      <a class="btn btn-gold" href="contact.html">Book Free Consultation</a>
      <a class="btn btn-ghost" data-cfg-href="phoneRaw" href="#">Call Us</a>
    </div>
  </div>
</section>
"""

print("service pages defined:", len(SERVICE_PAGES))

# =====================================================================
# IMAGE GALLERY  (masonry + filters)
# =====================================================================
GAL_ITEMS = [
 (16,"Modular Kitchen in Acrylic Finish","kitchen"),
 (3,"Island Kitchen with Breakfast Counter","kitchen"),
 (17,"Warm Family Living Room","living"),
 (5,"Living Room with Fluted TV Wall","living"),
 (1,"Open-Plan Living &amp; Lounge","living"),
 (18,"Serene Master Bedroom","bedroom"),
 (6,"Bedroom with Upholstered Headboard","bedroom"),
 (19,"Elegant Dining with Crockery Unit","dining"),
 (10,"Dining Zone with Pendant Lighting","dining"),
 (20,"Teak &amp; Marble Pooja Room","pooja"),
 (7,"Carved Mandir with Brass Accents","pooja"),
 (21,"Layered False Ceiling with Cove Light","ceiling"),
 (4,"Living Room False Ceiling Detail","ceiling"),
 (22,"Floating TV Showcase Unit","tv"),
 (9,"Panelled Entertainment Wall","tv"),
 (23,"Sliding Wardrobe in Veneer","wardrobe"),
 (11,"Floor-to-Ceiling Wardrobe","wardrobe"),
 (24,"Home Study with Open Shelving","study"),
 (8,"Work-From-Home Corner","study"),
 (25,"Playful Kids Bedroom","kids"),
 (12,"Bunk Bed Kids Room","kids"),
 (26,"Spa-Style Bathroom","bath"),
 (13,"Modern Toilet with Vanity","bath"),
 (27,"Contemporary Office Reception","commercial"),
 (14,"Retail Showroom Interior","commercial"),
 (28,"Turnkey Apartment Handover","living"),
 (29,"Design Studio Moodboard","living"),
 (2,"Villa Interior Overview","living"),
]
GAL_FILTERS = [("All","all"),("Kitchen","kitchen"),("Living","living"),("Bedroom","bedroom"),
 ("Dining","dining"),("Pooja","pooja"),("Ceiling","ceiling"),("TV Unit","tv"),
 ("Wardrobe","wardrobe"),("Study","study"),("Kids","kids"),("Bath","bath"),("Commercial","commercial")]

def gallery_images():
    pills = "\n".join(
        f'<button class="pill{" active" if f==1 and i==0 else ""}" data-filter="{slug}">{label}</button>'
        for i,(label,slug) in enumerate(GAL_FILTERS) for f in [1])
    items = "\n".join(
        f"""<a class="m-item reveal" href="#" data-cat="{cat}" data-lb="{IMG}{n}.svg" data-cap="{cap}">
  <img src="{IMG}{n}.svg" alt="{cap}" loading="lazy">
  <div class="m-cap">{cap} &middot; {str(n).zfill(2)}</div></a>"""
        for n,cap,cat in GAL_ITEMS)
    return f"""
{banner("Image Gallery", "A walk through real rooms we&rsquo;ve designed — filter by space to find inspiration for yours.", 17, ("Gallery","gallery-images.html"), ("Image Gallery","gallery-images.html"))}

<section class="section">
  <div class="geo-bg faint"></div>
  <div class="container">
    <div class="center" style="max-width:720px;margin-inline:auto">
      {ornament()}{eyebrow("Our Portfolio", True)}
      <h2 class="reveal">Browse our interior gallery.</h2>
      <p class="lead reveal">Every image is numbered to match its file in the gallery folder, so a design you love is easy to reference when you talk to us.</p>
    </div>
    <div class="filters reveal" data-filter-group data-target="#galGrid" style="margin-top:36px">{pills}</div>
    <div class="masonry" id="galGrid">{items}</div>
  </div>
</section>

<section class="section cta-band dark" style="background:var(--teal)">
  <div class="geo-bg"></div>
  <div class="container center">
    <h2 class="reveal" style="color:var(--ivory)">See something you love?</h2>
    <p class="lead reveal" style="margin-inline:auto">Tell us the image number and we&rsquo;ll recreate the look, tailored to your home and budget.</p>
    <a class="btn btn-gold reveal" href="contact.html">Enquire Now</a>
  </div>
</section>
"""

# =====================================================================
# VIDEO GALLERY
# =====================================================================
VIDEOS = [
 (31,"Modular Kitchen Reveal","Kitchen Walkthrough"),
 (32,"Living Room Transformation","Living Space"),
 (33,"Master Bedroom Tour","Bedroom Tour"),
 (34,"Pooja Room Craft Story","Pooja Room"),
 (35,"False Ceiling &amp; Lighting","Ceiling &amp; Light"),
 (36,"Commercial Fit-Out Timelapse","Commercial"),
]
def gallery_videos():
    cards = "\n".join(
        f"""<div class="vcard reveal" data-delay="{(i%3)+1}" data-lb="assets/videos/{n}.mp4" data-type="video" data-cap="{title}">
  <img src="{IMG}{n}.svg" alt="{title} video poster" loading="lazy">
  <span class="play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>
  <div class="vmeta"><span>{tag}</span><h3>{title}</h3></div></div>"""
        for i,(n,title,tag) in enumerate(VIDEOS))
    return f"""
{banner("Video Gallery", "Step inside our projects — short walkthroughs and reveal films of homes we&rsquo;ve brought to life.", 32, ("Gallery","gallery-images.html"), ("Video Gallery","gallery-videos.html"))}

<section class="section">
  <div class="geo-bg faint"></div>
  <div class="container">
    <div class="center" style="max-width:720px;margin-inline:auto">
      {ornament()}{eyebrow("Watch Our Work", True)}
      <h2 class="reveal">Project films &amp; walkthroughs.</h2>
      <p class="lead reveal">Poster thumbnails are numbered to match their video files. Drop your own <strong>.mp4</strong> clips into <code>assets/videos/</code> using the same numbers and they&rsquo;ll play instantly.</p>
    </div>
    <div class="vgrid" style="margin-top:44px">{cards}</div>
  </div>
</section>

<section class="section cta-band dark" style="background:var(--teal)">
  <div class="geo-bg"></div>
  <div class="container center">
    <h2 class="reveal" style="color:var(--ivory)">Want a film like this for your home?</h2>
    <p class="lead reveal" style="margin-inline:auto">Every turnkey project can be captured start to finish. Let&rsquo;s create yours.</p>
    <a class="btn btn-gold reveal" href="contact.html">Start Your Project</a>
  </div>
</section>
"""

print("galleries defined")

# =====================================================================
# CONTACT
# =====================================================================
def contact():
    svc_opts = "\n".join(f'<option>{n} Interiors</option>' for n,_,_,_ in SERVICE_CARDS)
    return f"""
{banner("Contact Us", "Tell us about your home — we&rsquo;d love to hear from you. The first consultation is always free.", 15, ("Contact Us","contact.html"))}

<section class="section">
  <div class="geo-bg faint"></div>
  <div class="container">
    <div class="split">
      <div class="reveal r-left">
        {eyebrow("Send An Enquiry")}
        <h2>Let&rsquo;s start the conversation.</h2>
        <p class="lead">Fill in a few details and our design team will get back to you within one working day with ideas and next steps.</p>
        <div class="form-card" style="margin-top:8px">
          <form data-stub>
            <div class="form-grid">
              <div class="field"><label>Your Name</label><input type="text" name="name" placeholder="Full name" required></div>
              <div class="field"><label>Phone</label><input type="tel" name="phone" placeholder="Mobile number" required></div>
            </div>
            <div class="form-grid">
              <div class="field"><label>Email</label><input type="email" name="email" placeholder="you@email.com"></div>
              <div class="field"><label>Interested In</label><select name="service"><option>Complete Home / Turnkey</option>{svc_opts}</select></div>
            </div>
            <div class="field"><label>Tell us about your project</label><textarea name="message" placeholder="Property type, location, rooms, approximate budget, timeline..."></textarea></div>
            <button class="btn btn-gold" type="submit" style="width:100%;justify-content:center">Submit Enquiry</button>
            <p class="form-note">By submitting, you agree to be contacted about your enquiry. We respect your privacy.</p>
          </form>
        </div>
      </div>
      <div class="reveal r-right">
        {eyebrow("Reach Us Directly")}
        <h2>Visit, call or message.</h2>
        <div class="cinfo" style="margin-top:18px">
          <div class="row"><span class="ic"><svg viewBox="0 0 24 24" stroke="currentColor" fill="none"><path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></svg></span>
            <div><b>Studio Address</b><p data-cfg="addressLine1">No. 24, Sannathi Street, Velachery</p><p data-cfg="addressLine2">Chennai, Tamil Nadu 600042, India</p></div></div>
          <div class="row"><span class="ic"><svg viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.24 11 11 0 0 0 3.5.56 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11 11 0 0 0 .56 3.5 1 1 0 0 1-.25 1z" fill="currentColor"/></svg></span>
            <div><b>Phone</b><a data-cfg="phone" data-cfg-href="phoneRaw" href="#">+91 98840 12345</a></div></div>
          <div class="row"><span class="ic"><svg viewBox="0 0 24 24" stroke="currentColor" fill="none"><path d="M3 6h18v12H3z"/><path d="M3 7l9 6 9-6"/></svg></span>
            <div><b>Email</b><a data-cfg="email" href="#">hello@venkateshwarainteriors.in</a></div></div>
          <div class="row"><span class="ic"><svg viewBox="0 0 24 24" stroke="currentColor" fill="none"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></span>
            <div><b>Working Hours</b><p data-cfg="hours">Mon &ndash; Sat: 10:00 AM &ndash; 8:00 PM</p><p data-cfg="hoursNote">Sunday by appointment</p></div></div>
          <div class="row"><span class="ic"><svg viewBox="0 0 24 24" stroke="currentColor" fill="none"><path d="M4 7h16v13H4z"/><path d="M4 7l2-3h12l2 3M9 11h6"/></svg></span>
            <div><b>GSTIN</b><p data-cfg="gstin">33ABCDE1234F1Z5</p></div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section tight">
  <div class="container">
    <div class="map-embed reveal"><iframe data-cfg-src="mapEmbed" src="https://www.google.com/maps?q=Velachery,Chennai&output=embed" loading="lazy" title="Location map" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  </div>
</section>

<section class="section cta-band dark" style="background:var(--teal)">
  <div class="geo-bg"></div>
  <div class="container center">
    <h2 class="reveal" style="color:var(--ivory)">Prefer to talk it through?</h2>
    <p class="lead reveal" style="margin-inline:auto">Call or WhatsApp us directly — we&rsquo;re happy to answer questions before you commit to anything.</p>
    <a class="btn btn-gold reveal" data-cfg-href="phoneRaw" href="#">Call <span data-cfg="phone">+91 98840 12345</span></a>
  </div>
</section>
"""

# =====================================================================
# LEGAL — Privacy & Terms
# =====================================================================
def legal_privacy():
    return f"""
{banner("Privacy Policy", "How we collect, use and protect the information you share with us.", 15, ("Privacy Policy","privacy.html"))}
<section class="section"><div class="geo-bg faint"></div><div class="container"><div class="prose reveal">
  <p class="lead">This Privacy Policy explains how <strong data-cfg="businessName">Venkateshwara Interiors</strong> (&ldquo;we&rdquo;, &ldquo;us&rdquo;) collects and handles your personal information when you use our website or services.</p>
  <h2>Information We Collect</h2>
  <p>We collect information you voluntarily provide through enquiry forms, calls or messages — typically your name, phone number, email address, property location and project requirements. We may also collect basic, non-identifying analytics about how visitors use our website.</p>
  <h2>How We Use Your Information</h2>
  <ul>
    <li>To respond to your enquiries and provide design consultations and quotes.</li>
    <li>To plan, communicate about and deliver your interior project.</li>
    <li>To send relevant updates about our services, only where you have agreed.</li>
    <li>To improve our website and the quality of our services.</li>
  </ul>
  <h2>Sharing Of Information</h2>
  <p>We do not sell your personal information. We may share necessary details with trusted partners and vendors strictly to execute your project, and with authorities where required by law.</p>
  <h2>Data Security</h2>
  <p>We take reasonable technical and organisational measures to protect your information against unauthorised access, alteration or disclosure. No method of transmission over the internet is fully secure, however, and we cannot guarantee absolute security.</p>
  <h2>Your Rights</h2>
  <p>You may request access to, correction of, or deletion of the personal information we hold about you, and you may opt out of marketing communications at any time by contacting us.</p>
  <h2>Cookies</h2>
  <p>Our website may use basic cookies to improve your browsing experience and understand site usage. You can control cookies through your browser settings.</p>
  <h2>Contact Us</h2>
  <p>For any privacy-related questions or requests, contact us at <a data-cfg="email" href="#">hello@venkateshwarainteriors.in</a> or call <a data-cfg="phone" data-cfg-href="phoneRaw" href="#">+91 98840 12345</a>.</p>
  <p class="form-note">This policy may be updated from time to time. Please review it periodically for any changes.</p>
</div></div></section>
"""

def legal_terms():
    return f"""
{banner("Terms &amp; Conditions", "The terms that govern the use of our website and services.", 15, ("Terms &amp; Conditions","terms.html"))}
<section class="section"><div class="geo-bg faint"></div><div class="container"><div class="prose reveal">
  <p class="lead">These Terms &amp; Conditions govern your use of the website and the services provided by <strong data-cfg="businessName">Venkateshwara Interiors</strong>. By using our website or engaging our services, you agree to these terms.</p>
  <h2>Services</h2>
  <p>We provide interior design and turnkey execution services. All designs, quotations and timelines shared are indicative until confirmed in a signed work order. The final scope, materials and pricing are those set out in your agreed quotation.</p>
  <h2>Quotations &amp; Payments</h2>
  <ul>
    <li>Quotations are valid for the period stated within them and are subject to site conditions.</li>
    <li>Payments follow the milestone schedule agreed in your work order.</li>
    <li>Any change in scope after approval may affect pricing and timelines, communicated in advance.</li>
  </ul>
  <h2>Project Execution</h2>
  <p>We commit to delivering work to the agreed specification and standard. Timelines may be affected by factors beyond our control, including site readiness, third-party approvals and material availability, which we will communicate promptly.</p>
  <h2>Warranty</h2>
  <p>Workmanship and modular products carry the warranty stated in your agreement. Warranty excludes damage from misuse, water ingress beyond our scope, or unauthorised alterations.</p>
  <h2>Intellectual Property</h2>
  <p>All designs, drawings, 3D visualisations and content created by us remain our intellectual property unless otherwise agreed in writing. Website content may not be reproduced without permission.</p>
  <h2>Limitation Of Liability</h2>
  <p>To the extent permitted by law, our liability is limited to the value of the services provided. We are not liable for indirect or consequential losses.</p>
  <h2>Governing Law</h2>
  <p>These terms are governed by the laws of India, and any disputes are subject to the jurisdiction of the courts at our registered place of business.</p>
  <h2>Contact Us</h2>
  <p>Questions about these terms? Email <a data-cfg="email" href="#">hello@venkateshwarainteriors.in</a> or call <a data-cfg="phone" data-cfg-href="phoneRaw" href="#">+91 98840 12345</a>. GSTIN: <span data-cfg="gstin">33ABCDE1234F1Z5</span>.</p>
</div></div></section>
"""

# =====================================================================
# SITEMAP
# =====================================================================
def sitemap():
    main = [("Home","index.html"),("About Us","about.html"),("Services","services.html"),
            ("Image Gallery","gallery-images.html"),("Video Gallery","gallery-videos.html"),
            ("Contact Us","contact.html")]
    legal = [("Privacy Policy","privacy.html"),("Terms &amp; Conditions","terms.html"),("Sitemap","sitemap.html")]
    def col(title, items):
        lis = "\n".join(f'<li><a href="{h}">{l}</a></li>' for l,h in items)
        return f'<div class="sm-col reveal"><h3>{title}</h3><ul>{lis}</ul></div>'
    svc_items = [(n,h) for n,h,_,_ in SERVICE_CARDS]
    return f"""
{banner("Sitemap", "Every page on our website, in one place.", 2, ("Sitemap","sitemap.html"))}
<section class="section"><div class="geo-bg faint"></div><div class="container">
  <div class="sm-grid">
    {col("Main Pages", main)}
    {col("Our Services", [(n+" Interiors", h) for n,h in svc_items])}
    {col("Legal &amp; More", legal)}
  </div>
</div></section>
"""

# =====================================================================
# 404
# =====================================================================
def notfound():
    return f"""
<section class="banner" style="min-height:70vh;display:flex;align-items:center">
  <div class="banner-art"><img src="{IMG}2.svg" alt=""></div>
  <div class="geo-bg"></div>
  <div class="container reveal center" style="margin-inline:auto">
    <div class="eyebrow center">Error 404</div>
    <h1 style="font-size:clamp(3rem,10vw,6rem)">This room doesn&rsquo;t exist.</h1>
    <p class="lead" style="color:#dfe7e2;margin-inline:auto">The page you&rsquo;re looking for may have moved or never existed. Let&rsquo;s get you back home.</p>
    <div class="hero-cta" style="justify-content:center;margin-top:10px">
      <a class="btn btn-gold" href="index.html">Back to Home</a>
      <a class="btn btn-ghost" href="contact.html">Contact Us</a>
    </div>
  </div>
</section>
"""

print("contact/legal/sitemap/404 defined")

# =====================================================================
# GENERATE EVERYTHING
# =====================================================================
if __name__ == "__main__":
    write("index.html", home(),
          "Venkateshwara Interiors | Premium Interior Designers in Chennai",
          "Venkateshwara Interiors designs soulful, modern Indian homes — modular kitchens, pooja rooms, false ceilings, wardrobes and complete turnkey interiors.")
    write("about.html", about(),
          "About Us | Venkateshwara Interiors",
          "A decade of craft and honest, family-first interior design. Learn the story, mission and values behind Venkateshwara Interiors.")
    write("services.html", services(),
          "Interior Design Services | Venkateshwara Interiors",
          "Twelve dedicated interior specialities — modular kitchens, false ceilings, bedrooms, pooja rooms, wardrobes, commercial fit-outs and more.")
    for fname, d in SERVICE_PAGES.items():
        write(fname, service_page(fname, d),
              f"{d['name']} Interiors | Venkateshwara Interiors",
              f"{d['name']} interior design by Venkateshwara Interiors — {d['lead']}")
    write("gallery-images.html", gallery_images(),
          "Image Gallery | Venkateshwara Interiors",
          "Browse our interior design portfolio — modular kitchens, living rooms, bedrooms, pooja rooms and more, filterable by space.")
    write("gallery-videos.html", gallery_videos(),
          "Video Gallery | Venkateshwara Interiors",
          "Watch project walkthroughs and reveal films of homes designed and built by Venkateshwara Interiors.")
    write("contact.html", contact(),
          "Contact Us | Venkateshwara Interiors",
          "Get in touch with Venkateshwara Interiors for a free interior design consultation. Call, email or visit our studio.")
    write("privacy.html", legal_privacy(),
          "Privacy Policy | Venkateshwara Interiors",
          "How Venkateshwara Interiors collects, uses and protects your personal information.")
    write("terms.html", legal_terms(),
          "Terms & Conditions | Venkateshwara Interiors",
          "The terms and conditions governing the use of the Venkateshwara Interiors website and services.")
    write("sitemap.html", sitemap(),
          "Sitemap | Venkateshwara Interiors",
          "All pages on the Venkateshwara Interiors website in one place.")
    write("404.html", notfound(),
          "Page Not Found | Venkateshwara Interiors",
          "The page you are looking for could not be found.")
    print("\nALL PAGES GENERATED.")
