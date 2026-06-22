#!/usr/bin/env python3
"""
Generates room-specific SVG interior illustrations for Venkateshwara Interiors.
Each image is named 1.svg, 2.svg ... and carries a faint matching watermark.
Indian-luxe palette: peacock teal base, brass gold, ivory, kumkum maroon.
"""
import os, math, random

OUT = os.path.join(os.path.dirname(__file__), "assets", "images")
os.makedirs(OUT, exist_ok=True)

W, H = 1600, 1000

# ---- Palette helpers -------------------------------------------------------
PAL = {
    "teal":    "#0E2A2B",
    "teal2":   "#143C3D",
    "teal3":   "#1C5152",
    "brass":   "#C9A24B",
    "brass2":  "#E3C77A",
    "gold_dk": "#9A7A2E",
    "ivory":   "#F6F1E7",
    "ivory2":  "#EAE2D2",
    "kumkum":  "#7C2D34",
    "kumkum2": "#9E3B43",
    "ink":     "#14201F",
    "wood":    "#5A3A28",
    "wood2":   "#7A5234",
    "sage":    "#7E8C6A",
    "plum":    "#4A2740",
    "blush":   "#D8B9A6",
}

def defs(seed):
    """Common gradient / pattern defs, unique ids per image via seed."""
    s = seed
    return f'''
  <defs>
    <linearGradient id="wall{s}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{{wall_top}}"/>
      <stop offset="1" stop-color="{{wall_bot}}"/>
    </linearGradient>
    <linearGradient id="floor{s}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{{floor_top}}"/>
      <stop offset="1" stop-color="{{floor_bot}}"/>
    </linearGradient>
    <linearGradient id="brass{s}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{PAL['brass2']}"/>
      <stop offset="0.5" stop-color="{PAL['brass']}"/>
      <stop offset="1" stop-color="{PAL['gold_dk']}"/>
    </linearGradient>
    <radialGradient id="glow{s}" cx="0.5" cy="0.45" r="0.55">
      <stop offset="0" stop-color="#FFF6DD" stop-opacity="0.55"/>
      <stop offset="0.45" stop-color="#FFF6DD" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#FFF6DD" stop-opacity="0"/>
    </radialGradient>
    <pattern id="jaali{s}" width="56" height="56" patternUnits="userSpaceOnUse" patternTransform="rotate(0)">
      <rect width="56" height="56" fill="none"/>
      <path d="M28 2 L54 28 L28 54 L2 28 Z" fill="none" stroke="{PAL['brass']}" stroke-opacity="0.5" stroke-width="1.4"/>
      <circle cx="28" cy="28" r="6" fill="none" stroke="{PAL['brass']}" stroke-opacity="0.4" stroke-width="1.2"/>
      <path d="M28 14 L42 28 L28 42 L14 28 Z" fill="none" stroke="{PAL['brass']}" stroke-opacity="0.3" stroke-width="1"/>
    </pattern>
    <filter id="soft{s}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
  </defs>'''

def watermark(num):
    """Mild watermark whose text matches the filename number."""
    return f'''
  <g opacity="0.16" font-family="Georgia, 'Times New Roman', serif">
    <text x="{W-40}" y="{H-46}" text-anchor="end" font-size="190" font-weight="700"
          fill="#FFFFFF" opacity="0.5">{num}</text>
  </g>
  <g opacity="0.5" font-family="Georgia, serif">
    <rect x="36" y="{H-58}" width="234" height="36" rx="18" fill="#000000" opacity="0.22"/>
    <text x="52" y="{H-33}" font-size="19" letter-spacing="3" fill="#F6F1E7">VENKATESHWARA &#8226; {num}</text>
  </g>'''

def vignette():
    return f'''
  <rect x="0" y="0" width="{W}" height="{H}" fill="url(#vig)"/>'''

VIG_DEF = f'''
    <radialGradient id="vig" cx="0.5" cy="0.45" r="0.75">
      <stop offset="0.6" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.28"/>
    </radialGradient>'''

def frame(num, body, walls, jaali=True, glow_xy=None, seed=None):
    seed = seed if seed is not None else num
    d = defs(seed).format(**walls)
    # inject vignette gradient into defs
    d = d.replace("</defs>", VIG_DEF + "\n  </defs>")
    glow = ""
    if glow_xy:
        for (gx, gy, gr) in glow_xy:
            gr = gr * 0.62
            glow += f'<ellipse cx="{gx}" cy="{gy}" rx="{gr:.0f}" ry="{gr*0.7:.0f}" fill="url(#glow{seed})" opacity="0.7"/>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Interior illustration {num}">
{d}
  <rect width="{W}" height="{H}" fill="url(#wall{seed})"/>
{body}
{glow}
{vignette()}
{watermark(num)}
</svg>'''
    return svg

def rect(x,y,w,h,fill,rx=0,extra=""):
    return f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" fill="{fill}" {extra}/>'

def floor(seed, y, top, bot, persp=True):
    # simple floor band with subtle perspective lines
    s = f'<rect x="0" y="{y}" width="{W}" height="{H-y}" fill="url(#floor{seed})"/>'
    if persp:
        cx = W/2
        for i in range(-6,7):
            x1 = cx + i*120
            x2 = cx + i*420
            s += f'<line x1="{x1:.0f}" y1="{y}" x2="{x2:.0f}" y2="{H}" stroke="#000000" stroke-opacity="0.06" stroke-width="2"/>'
    return s

def jaali_panel(seed, x, y, w, h, op=1.0):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PAL["teal"]}" opacity="0.0"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#jaali{seed})" opacity="{op}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="url(#brass{seed})" stroke-width="4"/>')

def brass_line(x1,y1,x2,y2,seed,w=4):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="url(#brass{seed})" stroke-width="{w}"/>'

def pendant(seed, x, y, drop=120, r=26):
    return (f'<line x1="{x}" y1="0" x2="{x}" y2="{y}" stroke="{PAL["gold_dk"]}" stroke-width="3"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*0.7}" fill="url(#brass{seed})"/>'
            f'<ellipse cx="{x}" cy="{y+6}" rx="{r*0.7}" ry="{r*0.5}" fill="#FFF3CF" opacity="0.8"/>')

def plant(x, yb, h=150):
    s = f'<rect x="{x-26}" y="{yb-46}" width="52" height="58" rx="8" fill="{PAL["kumkum"]}"/>'
    s += f'<rect x="{x-26}" y="{yb-46}" width="52" height="14" rx="6" fill="{PAL["kumkum2"]}"/>'
    for a in range(-3,4):
        ang = a*16
        lx = x + math.sin(math.radians(ang))*70
        ly = yb-46-h + abs(a)*10
        s += f'<path d="M{x} {yb-46} Q {x+a*30} {yb-46-h*0.7} {lx:.0f} {ly:.0f}" stroke="{PAL["sage"]}" stroke-width="9" fill="none" stroke-linecap="round"/>'
    return s

def rug(seed, cx, y, w, h, fill):
    return (f'<ellipse cx="{cx}" cy="{y}" rx="{w/2}" ry="{h/2}" fill="{fill}" opacity="0.9"/>'
            f'<ellipse cx="{cx}" cy="{y}" rx="{w/2-22}" ry="{h/2-16}" fill="none" stroke="url(#brass{seed})" stroke-width="3" opacity="0.7"/>')

def art_frame(seed, x, y, w, h, fill):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="url(#brass{seed})" stroke-width="6"/>')

# ---------------------------------------------------------------------------
# Scene builders. Each returns (body_svg, walls_dict, glow_list)
# ---------------------------------------------------------------------------

def scene_living(num, accent=PAL["kumkum"], wood=PAL["wood2"]):
    s = num
    walls = dict(wall_top=PAL["teal2"], wall_bot=PAL["teal"], floor_top=PAL["wood2"], floor_bot=PAL["wood"])
    b = floor(s, 660, PAL["wood2"], PAL["wood"])
    b += jaali_panel(s, 980, 120, 360, 430, 0.9)
    b += art_frame(s, 250, 150, 300, 360, PAL["teal3"])
    b += f'<path d="M270 480 Q400 220 530 480 Z" fill="{accent}" opacity="0.55"/>'
    b += pendant(s, 760, 150, r=34)
    # sofa
    b += rug(s, 700, 800, 760, 150, PAL["kumkum2"])
    b += rect(360, 560, 540, 150, accent, rx=26)
    b += rect(360, 520, 540, 90, PAL["kumkum2"], rx=26)
    for cx in (430, 560, 690, 820):
        b += rect(cx-46, 470, 92, 92, PAL["brass2"], rx=16, extra='opacity="0.92"')
    b += rect(330, 560, 60, 170, wood, rx=14)
    b += rect(870, 560, 60, 170, wood, rx=14)
    # coffee table
    b += rect(560, 720, 220, 70, wood, rx=10)
    b += brass_line(560,792,560,860,s,8)+brass_line(776,792,776,860,s,8)
    b += plant(1180, 760, 200)
    b += plant(150, 760, 180)
    return b, walls, [(760,260,300)]

def scene_kitchen(num):
    s=num
    walls=dict(wall_top="#16413F", wall_bot=PAL["teal"], floor_top="#3C3A36", floor_bot="#24221F")
    b = floor(s, 690, "#3C3A36", "#24221F")
    # upper cabinets
    for i in range(5):
        x=160+i*260
        b += rect(x,120,230,170, PAL["ivory2"], rx=8, extra='opacity="0.96"')
        b += rect(x+14,134,202,142, PAL["ivory"], rx=4)
        b += f'<circle cx="{x+200}" cy="205" r="6" fill="url(#brass{s})"/>'
    # backsplash jaali
    b += jaali_panel(s, 160, 300, 1290, 70, 0.7)
    # counter
    b += rect(130, 372, 1340, 36, PAL["ink"], rx=6)
    b += rect(130, 372, 1340, 10, PAL["brass"], rx=4, extra='opacity="0.5"')
    # island
    b += rect(470, 560, 650, 300, "#2C6E63", rx=10)
    b += rect(470, 536, 650, 40, PAL["ink"], rx=8)
    for i in range(5):
        x=510+i*120
        b += rect(x,576,84,260, "#23564E", rx=6)
        b += f'<circle cx="{x+72}" cy="706" r="6" fill="url(#brass{s})"/>'
    # base cabinets sides
    b += rect(130, 410, 320, 280, "#23564E", rx=8)
    b += rect(1150, 410, 320, 280, "#23564E", rx=8)
    # pendants over island
    b += pendant(s, 640, 150, r=30)+pendant(s, 800, 150, r=30)+pendant(s, 960, 150, r=30)
    # sink / tap
    b += f'<path d="M300 372 q0 -60 40 -60" stroke="url(#brass{s})" stroke-width="9" fill="none"/>'
    return b, walls, [(800,300,360)]

def scene_false_ceiling(num):
    s=num
    walls=dict(wall_top=PAL["teal2"], wall_bot=PAL["teal"], floor_top=PAL["wood2"], floor_bot=PAL["wood"])
    b = floor(s, 720, PAL["wood2"], PAL["wood"])
    # layered ceiling coves
    b += rect(0,0,W,150, "#103534")
    b += rect(120,90,W-240,150, "#16403E", rx=14)
    b += rect(260,150,W-520,130, "#1C5150", rx=14)
    # cove lights
    for i in range(9):
        x=170+i*150
        b += f'<circle cx="{x}" cy="120" r="10" fill="#FFF3CF"/><circle cx="{x}" cy="120" r="22" fill="url(#glow{s})"/>'
    # central chandelier
    b += pendant(s, 800, 250, r=60)
    for a in range(-3,4):
        b += pendant(s, 800+a*70, 250+abs(a)*8, drop=250+abs(a)*6, r=12)
    # subtle furniture below
    b += rect(420, 560, 760, 150, PAL["kumkum"], rx=24)
    b += rect(420, 520, 760, 80, PAL["kumkum2"], rx=24)
    b += art_frame(s, 1240, 300, 250, 280, PAL["teal3"])
    return b, walls, [(800,260,420)]

def scene_bedroom(num):
    s=num
    walls=dict(wall_top="#173A45", wall_bot="#0E2A2B", floor_top=PAL["wood2"], floor_bot=PAL["wood"])
    b=floor(s,700,PAL["wood2"],PAL["wood"])
    # headboard jaali
    b += jaali_panel(s, 470, 180, 660, 320, 0.85)
    b += rect(470, 180, 660, 60, PAL["plum"], rx=10)
    # bed
    b += rug(s, 800, 880, 980, 150, PAL["kumkum2"])
    b += rect(420, 560, 760, 230, "#3A2A4A", rx=18)   # base
    b += rect(440, 500, 720, 130, PAL["ivory2"], rx=18) # mattress/duvet
    b += rect(440, 480, 720, 70, PAL["ivory"], rx=18)
    for cx in (560, 720, 880, 1040):
        b += rect(cx-60, 470, 120, 70, PAL["blush"], rx=14)
    # side tables + lamps
    for x in (360, 1180):
        b += rect(x-50, 560, 100, 150, PAL["wood"], rx=10)
        b += f'<rect x="{x-18}" y="490" width="36" height="80" fill="url(#brass{s})"/>'
        b += f'<path d="M{x-44} 490 L{x+44} 490 L{x+30} 440 L{x-30} 440 Z" fill="{PAL["brass2"]}" opacity="0.9"/>'
        b += f'<circle cx="{x}" cy="470" r="40" fill="url(#glow{s})"/>'
    return b, walls, [(560,470,170),(1180,470,170)]

def scene_pooja(num):
    s=num
    walls=dict(wall_top="#1B4140", wall_bot="#0E2A2B", floor_top="#6A4A30", floor_bot="#4A3220")
    b=floor(s,720,"#6A4A30","#4A3220")
    # arched temple mandir
    cx=800
    b += f'<path d="M540 720 L540 360 Q540 150 800 150 Q1060 150 1060 360 L1060 720 Z" fill="{PAL["wood"]}"/>'
    b += f'<path d="M560 700 L560 370 Q560 175 800 175 Q1040 175 1040 370 L1040 700 Z" fill="{PAL["wood2"]}"/>'
    # gopuram tiers
    for i,wd in enumerate([300,240,180,120]):
        yy=150-i*0  # base
    b += f'<path d="M620 175 Q800 60 980 175 Z" fill="url(#brass{s})"/>'
    b += f'<path d="M660 130 Q800 50 940 130 Z" fill="{PAL["brass2"]}"/>'
    b += f'<circle cx="{cx}" cy="60" r="16" fill="url(#brass{s})"/>'
    # jaali side panels
    b += jaali_panel(s, 300, 280, 200, 430, 0.8)
    b += jaali_panel(s, 1100, 280, 200, 430, 0.8)
    # inner glow + deity silhouette
    b += f'<rect x="610" y="300" width="380" height="360" fill="#2A1B12"/>'
    b += f'<ellipse cx="{cx}" cy="470" rx="150" ry="170" fill="url(#glow{s})"/>'
    b += f'<path d="M{cx} 360 q-60 0 -60 90 q0 110 60 150 q60 -40 60 -150 q0 -90 -60 -90 Z" fill="{PAL["brass"]}" opacity="0.85"/>'
    b += f'<circle cx="{cx}" cy="410" r="34" fill="{PAL["brass2"]}"/>'
    # diya lamps
    for x in (700, 900):
        b += f'<path d="M{x-26} 650 q26 24 52 0 Z" fill="url(#brass{s})"/>'
        b += f'<path d="M{x} 612 q-10 22 0 36 q10 -14 0 -36" fill="#FFB347"/>'
        b += f'<circle cx="{x}" cy="620" r="26" fill="url(#glow{s})"/>'
    # rangoli on floor
    b += f'<g transform="translate({cx},820)">'
    for a in range(12):
        ang=a*30
        b += f'<ellipse cx="0" cy="0" rx="120" ry="34" fill="none" stroke="{PAL["brass"]}" stroke-opacity="0.5" stroke-width="3" transform="rotate({ang})"/>'
    b += '</g>'
    return b, walls, [(cx,470,260)]

def scene_study(num):
    s=num
    walls=dict(wall_top=PAL["teal2"], wall_bot=PAL["teal"], floor_top="#5A4632", floor_bot="#3C2E20")
    b=floor(s,700,"#5A4632","#3C2E20")
    # bookshelf wall
    b += rect(120,120,560,560, PAL["wood"], rx=8)
    for r in range(4):
        yy=160+r*135
        b += rect(140, yy, 520, 16, PAL["wood2"])
        for c in range(10):
            bx=150+c*52+random.randint(-2,2)
            bh=random.randint(70,110)
            col=random.choice([PAL["kumkum"],PAL["brass"],PAL["teal3"],PAL["ivory2"],PAL["plum"],PAL["sage"]])
            b += rect(bx, yy-bh, 34, bh, col, rx=2)
    # jaali panel
    b += jaali_panel(s, 1000, 150, 420, 420, 0.85)
    # desk
    b += rect(760, 560, 620, 50, PAL["ink"], rx=8)
    b += rect(780, 610, 40, 150, PAL["wood2"])
    b += rect(1320, 610, 40, 150, PAL["wood2"])
    # chair
    b += rect(980, 600, 160, 60, PAL["kumkum"], rx=10)
    b += rect(980, 470, 160, 150, PAL["kumkum2"], rx=16)
    # desk lamp + laptop
    b += f'<rect x="820" y="510" width="120" height="80" rx="6" fill="{PAL["teal3"]}"/>'
    b += f'<path d="M1240 560 l0 -90 l60 -20" stroke="url(#brass{s})" stroke-width="8" fill="none"/><circle cx="1300" cy="448" r="20" fill="url(#glow{s})"/>'
    return b, walls, [(1300,450,150)]

def scene_tv(num):
    s=num
    walls=dict(wall_top="#16413F", wall_bot=PAL["teal"], floor_top="#5A4632", floor_bot="#3C2E20")
    b=floor(s,720,"#5A4632","#3C2E20")
    # paneled feature wall
    b += rect(140,100,1320,560, "#103937", rx=8)
    for i in range(7):
        x=180+i*186
        b += rect(x,130,150,500, "#15433F", rx=6)
        b += rect(x,130,150,500, "none", rx=6, extra=f'stroke="url(#brass{s})" stroke-width="2" opacity="0.5"')
    # tv
    b += rect(520,200,560,320, "#05100F", rx=10)
    b += rect(520,200,560,320, "none", rx=10, extra=f'stroke="url(#brass{s})" stroke-width="6"')
    b += f'<rect x="540" y="220" width="520" height="280" rx="6" fill="#0B2B2A"/>'
    # backlight
    b += f'<rect x="500" y="180" width="600" height="360" rx="14" fill="url(#glow{s})" opacity="0.5"/>'
    # console with jaali doors
    b += rect(360,560,880,150, PAL["wood"], rx=10)
    b += jaali_panel(s, 380, 580, 380, 110, 0.7)
    b += jaali_panel(s, 840, 580, 380, 110, 0.7)
    # decor
    b += rect(1300,360,30,300, PAL["wood2"])
    b += plant(220, 690, 180)
    b += art_frame(s, 1180, 230, 0, 0, "none")
    return b, walls, [(800,360,300)]

def scene_dining(num):
    s=num
    walls=dict(wall_top=PAL["teal2"], wall_bot=PAL["teal"], floor_top=PAL["wood2"], floor_bot=PAL["wood"])
    b=floor(s,700,PAL["wood2"],PAL["wood"])
    b += jaali_panel(s, 1040, 140, 400, 440, 0.85)
    b += art_frame(s, 220, 170, 360, 300, PAL["teal3"])
    b += f'<circle cx="400" cy="320" r="90" fill="{PAL["kumkum"]}" opacity="0.5"/>'
    # chandelier row
    for x in (600,800,1000):
        b += pendant(s, x, 170, r=26)
    # table
    b += f'<ellipse cx="800" cy="700" rx="430" ry="120" fill="{PAL["wood"]}"/>'
    b += f'<ellipse cx="800" cy="676" rx="430" ry="120" fill="{PAL["wood2"]}"/>'
    b += f'<ellipse cx="800" cy="668" rx="380" ry="96" fill="{PAL["ivory2"]}" opacity="0.55"/>'
    # chairs
    for i,x in enumerate([470,640,800,960,1130]):
        b += rect(x-46, 560, 92, 60, PAL["kumkum"], rx=10)
        b += rect(x-46, 430, 92, 150, PAL["kumkum2"], rx=14)
    # centerpiece
    b += f'<rect x="760" y="600" width="80" height="60" rx="8" fill="url(#brass{s})"/>'
    b += plant(800, 660, 110)
    return b, walls, [(800,300,360)]

def scene_wardrobe(num):
    s=num
    walls=dict(wall_top="#173A45", wall_bot="#0E2A2B", floor_top="#5A4632", floor_bot="#3C2E20")
    b=floor(s,720,"#5A4632","#3C2E20")
    # wardrobe run
    b += rect(140,120,1320,600, PAL["wood"], rx=8)
    for i in range(6):
        x=160+i*218
        b += rect(x,140,200,560, "#6A5238" if i%2 else "#7A5E40", rx=6)
        b += rect(x,140,200,560, "none", rx=6, extra=f'stroke="url(#brass{s})" stroke-width="2" opacity="0.5"')
        b += f'<rect x="{x+92}" y="320" width="16" height="160" rx="8" fill="url(#brass{s})"/>'
    # one open door showing rail + clothes
    ox=160+2*218
    b += rect(ox,140,200,560, "#2A2620", rx=6)
    b += rect(ox+16,170,168,16, PAL["brass"])
    for c in range(5):
        cx=ox+34+c*32
        col=random.choice([PAL["kumkum"],PAL["teal3"],PAL["ivory2"],PAL["plum"],PAL["sage"]])
        b += rect(cx,186,22,170, col, rx=6)
    # mirror + bench
    b += rect(1500-0,0,0,0,"none")
    b += rect(620,560,360,30, PAL["ink"], rx=8)
    b += rect(700,590,40,120, PAL["wood2"])+rect(860,590,40,120, PAL["wood2"])
    b += pendant(s, 800, 150, r=24)
    return b, walls, [(ox+100,400,200)]

def scene_kids(num):
    s=num
    walls=dict(wall_top="#1E5A66", wall_bot="#143C46", floor_top="#6A5238", floor_bot="#4A3826")
    b=floor(s,700,"#6A5238","#4A3826")
    # playful wall: clouds + stars (geometry)
    for (x,y,r) in [(300,200,70),(420,230,50),(1200,180,60),(1320,210,46)]:
        b += f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*0.7}" fill="{PAL["ivory"]}" opacity="0.85"/>'
    for _ in range(16):
        x=random.randint(120,1480); y=random.randint(120,420)
        b += f'<path d="M{x} {y-9} l3 7 7 0 -6 5 3 8 -7 -5 -7 5 3 -8 -6 -5 7 0 Z" fill="{PAL["brass2"]}" opacity="0.8"/>'
    # bunk bed
    b += rect(220,300,520,420, PAL["wood2"], rx=14)
    b += rect(240,330,480,120, PAL["kumkum"], rx=12)
    b += rect(240,560,480,120, PAL["teal3"], rx=12)
    for cx in (320,420):
        b += rect(cx-40,300,80,150,"none",rx=6,extra=f'stroke="url(#brass{s})" stroke-width="8"')
    # toy shelf
    b += rect(900,360,460,360, PAL["ivory2"], rx=12)
    for r in range(3):
        yy=410+r*110
        b += rect(920, yy, 420, 14, PAL["wood2"])
        for c in range(5):
            bx=930+c*82
            col=random.choice([PAL["kumkum"],PAL["brass"],PAL["teal3"],PAL["plum"],PAL["sage"]])
            b += f'<circle cx="{bx+20}" cy="{yy-26}" r="24" fill="{col}"/>'
    b += pendant(s, 800, 150, r=26)
    return b, walls, [(480,420,220)]

def scene_bath(num):
    s=num
    walls=dict(wall_top="#1B4A4C", wall_bot=PAL["teal"], floor_top="#46555A", floor_bot="#2E3A3E")
    b=floor(s,720,"#46555A","#2E3A3E")
    # marble wall panels
    for i in range(6):
        x=140+i*210
        b += rect(x,110,196,560, "#1F5557" if i%2 else "#236063", rx=6)
        b += f'<path d="M{x+20} 160 q60 80 150 40" stroke="#FFFFFF" stroke-opacity="0.1" stroke-width="3" fill="none"/>'
    b += jaali_panel(s, 1240, 150, 220, 460, 0.6)
    # vanity
    b += rect(220,520,520,40, PAL["ink"], rx=8)
    b += rect(240,560,480,150, PAL["wood"], rx=8)
    b += f'<ellipse cx="480" cy="520" rx="120" ry="26" fill="{PAL["ivory"]}"/>'
    b += f'<path d="M480 510 q0 -70 0 -90" stroke="url(#brass{s})" stroke-width="9" fill="none"/>'
    # round mirror
    b += f'<circle cx="480" cy="320" r="120" fill="#0B2B2A"/><circle cx="480" cy="320" r="120" fill="none" stroke="url(#brass{s})" stroke-width="8"/>'
    b += f'<circle cx="480" cy="320" r="120" fill="url(#glow{s})" opacity="0.4"/>'
    # freestanding tub
    b += f'<ellipse cx="1080" cy="650" rx="240" ry="80" fill="{PAL["ivory"]}"/>'
    b += f'<ellipse cx="1080" cy="630" rx="240" ry="80" fill="{PAL["ivory2"]}"/>'
    b += f'<ellipse cx="1080" cy="624" rx="200" ry="60" fill="#9DBFC0"/>'
    return b, walls, [(480,320,200),(1080,520,240)]

def scene_commercial(num):
    s=num
    walls=dict(wall_top="#16413F", wall_bot=PAL["teal"], floor_top="#3A4A4C", floor_bot="#222E2F")
    b=floor(s,700,"#3A4A4C","#222E2F")
    # glass facade grid
    for i in range(8):
        x=120+i*170
        b += rect(x,100,150,560, "#14403E", rx=4, extra='opacity="0.7"')
        b += rect(x,100,150,560, "none", rx=4, extra=f'stroke="url(#brass{s})" stroke-width="2" opacity="0.4"')
    # reception desk
    b += rect(420,520,760,200, "#0F3433", rx=12)
    b += rect(420,500,760,40, PAL["ink"], rx=10)
    b += jaali_panel(s, 460, 540, 680, 150, 0.6)
    # brass logo wall
    b += rect(560,200,480,220, "#0C2C2B", rx=10)
    b += f'<text x="800" y="340" text-anchor="middle" font-family="Georgia, serif" font-size="88" fill="url(#brass{s})" opacity="0.9">&#10070;</text>'
    # linear pendants
    for x in (560,800,1040):
        b += f'<rect x="{x-90}" y="150" width="180" height="14" rx="7" fill="url(#brass{s})"/>'
        b += f'<rect x="{x-90}" y="164" width="180" height="6" fill="#FFF3CF" opacity="0.7"/>'
    b += plant(220, 690, 200)+plant(1360, 690, 200)
    return b, walls, [(800,300,400)]

def scene_about(num):
    # designer / consultation scene with moodboard
    s=num
    walls=dict(wall_top=PAL["teal2"], wall_bot=PAL["teal"], floor_top="#5A4632", floor_bot="#3C2E20")
    b=floor(s,720,"#5A4632","#3C2E20")
    # moodboard wall
    b += rect(140,120,720,520, "#103937", rx=10)
    cols=[PAL["kumkum"],PAL["brass"],PAL["teal3"],PAL["ivory2"],PAL["plum"],PAL["blush"],PAL["sage"],PAL["wood2"]]
    random.shuffle(cols)
    k=0
    for r in range(3):
        for c in range(4):
            x=170+c*168; y=150+r*162
            b += art_frame(s, x, y, 150, 140, cols[k%len(cols)]); k+=1
    # large table with plans
    b += rect(940,560,520,40, PAL["ink"], rx=8)
    b += rect(960,600,40,150, PAL["wood2"])+rect(1400,600,40,150, PAL["wood2"])
    b += rect(1000,520,400,46, PAL["ivory"], rx=4)
    b += f'<path d="M1010 543 h380 M1010 530 h280 M1010 556 h320" stroke="{PAL["teal"]}" stroke-opacity="0.5" stroke-width="2"/>'
    # samples
    for i,col in enumerate([PAL["kumkum"],PAL["brass"],PAL["sage"],PAL["plum"]]):
        b += rect(1040+i*70, 470, 56, 56, col, rx=6)
    b += pendant(s, 1200, 150, r=28)
    return b, walls, [(500,360,300),(1200,470,200)]

def scene_contact(num):
    # showroom / storefront
    s=num
    walls=dict(wall_top="#16413F", wall_bot=PAL["teal"], floor_top="#3A4A4C", floor_bot="#222E2F")
    b=floor(s,720,"#3A4A4C","#222E2F")
    b += rect(120,120,1360,560, "#0F3433", rx=10)
    b += jaali_panel(s, 150, 150, 1300, 500, 0.35)
    # signage
    b += rect(440,210,720,140, "#0B2B2A", rx=12)
    b += f'<text x="800" y="300" text-anchor="middle" font-family="Georgia, serif" font-size="60" letter-spacing="4" fill="url(#brass{s})">SHOWROOM</text>'
    # entrance arch
    b += f'<path d="M620 720 L620 470 Q620 380 800 380 Q980 380 980 470 L980 720 Z" fill="#0A2625"/>'
    b += f'<path d="M620 470 Q620 380 800 380 Q980 380 980 470" fill="none" stroke="url(#brass{s})" stroke-width="8"/>'
    b += f'<ellipse cx="800" cy="560" rx="120" ry="150" fill="url(#glow{s})"/>'
    b += pendant(s, 800, 200, r=22)
    b += plant(250, 690, 200)+plant(1350, 690, 200)
    return b, walls, [(800,420,300)]

# Pattern-only geometric background (for CSS use, full bleed jaali)
def geometric_bg():
    s="bg"
    d=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">
  <defs>
    <linearGradient id="bgg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{PAL['teal']}"/>
      <stop offset="1" stop-color="#091F20"/>
    </linearGradient>
    <pattern id="j" width="80" height="80" patternUnits="userSpaceOnUse">
      <path d="M40 4 L76 40 L40 76 L4 40 Z" fill="none" stroke="{PAL['brass']}" stroke-opacity="0.18" stroke-width="1.4"/>
      <path d="M40 20 L60 40 L40 60 L20 40 Z" fill="none" stroke="{PAL['brass']}" stroke-opacity="0.12" stroke-width="1.2"/>
      <circle cx="40" cy="40" r="3" fill="{PAL['brass']}" fill-opacity="0.16"/>
      <circle cx="0" cy="0" r="3" fill="{PAL['brass']}" fill-opacity="0.12"/>
      <circle cx="80" cy="80" r="3" fill="{PAL['brass']}" fill-opacity="0.12"/>
    </pattern>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bgg)"/>
  <rect width="{W}" height="{H}" fill="url(#j)"/>
</svg>'''
    return d

# ---------------------------------------------------------------------------
# Build the catalogue. Image number -> scene
# ---------------------------------------------------------------------------
random.seed(7)

CATALOG = {
    1:  ("living",     scene_living),       # Home hero
    2:  ("about",      scene_about),        # About hero
    3:  ("kitchen",    scene_kitchen),      # Modular Kitchen
    4:  ("ceiling",    scene_false_ceiling),# False Ceiling
    5:  ("living",     scene_living),       # Living Room
    6:  ("bedroom",    scene_bedroom),      # Bedroom
    7:  ("pooja",      scene_pooja),        # Pooja Room
    8:  ("study",      scene_study),        # Study Room
    9:  ("tv",         scene_tv),           # TV Showcase
    10: ("dining",     scene_dining),       # Dining Room
    11: ("wardrobe",   scene_wardrobe),     # Cupboards & Wardrobes
    12: ("kids",       scene_kids),         # Kids Room
    13: ("bath",       scene_bath),         # Toilet/Bathroom
    14: ("commercial", scene_commercial),   # Commercial
    15: ("contact",    scene_contact),      # Contact hero
    # gallery extras / section images (variations)
    16: ("kitchen",    scene_kitchen),
    17: ("living",     scene_living),
    18: ("bedroom",    scene_bedroom),
    19: ("dining",     scene_dining),
    20: ("pooja",      scene_pooja),
    21: ("ceiling",    scene_false_ceiling),
    22: ("tv",         scene_tv),
    23: ("wardrobe",   scene_wardrobe),
    24: ("study",      scene_study),
    25: ("kids",       scene_kids),
    26: ("bath",       scene_bath),
    27: ("commercial", scene_commercial),
    28: ("living",     scene_living),       # CTA / why-choose
    29: ("about",      scene_about),        # process
    30: ("dining",     scene_dining),       # testimonial backdrop
    # video posters reuse scenes 31-36
    31: ("kitchen",    scene_kitchen),
    32: ("living",     scene_living),
    33: ("bedroom",    scene_bedroom),
    34: ("pooja",      scene_pooja),
    35: ("ceiling",    scene_false_ceiling),
    36: ("commercial", scene_commercial),
}

# vary accents per number so repeats look different
ACCENTS = [PAL["kumkum"], PAL["plum"], PAL["teal3"], PAL["sage"], PAL["kumkum2"]]

count=0
for num,(name,fn) in CATALOG.items():
    random.seed(num*13+1)
    body, walls, glow = fn(num)
    svg = frame(num, body, walls, glow_xy=glow, seed=num)
    with open(os.path.join(OUT, f"{num}.svg"), "w") as f:
        f.write(svg)
    count+=1

# geometric background
with open(os.path.join(OUT, "geometric.svg"), "w") as f:
    f.write(geometric_bg())

print(f"Generated {count} room images + geometric.svg")
print("Files:", sorted(os.listdir(OUT)))
