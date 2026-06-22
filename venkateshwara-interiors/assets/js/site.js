/* =====================================================================
   VENKATESHWARA INTERIORS — site engine
   Builds shared chrome (header, nav, footer, action bar) from SITE_CONFIG
   and wires every interaction (reveal, tilt, lightbox, accordion, etc.)
   ===================================================================== */
(function(){
  "use strict";
  const C = window.SITE_CONFIG || {};
  const base = (window.PATH_BASE || "");           // "" for root pages, "" here since flat
  const A = base + "assets/";

  /* ---------- Site map (single source for nav + footer + sitemap) ----- */
  const SERVICES = [
    ["Modular Kitchen Interiors","service-modular-kitchen.html"],
    ["False Ceiling Interiors","service-false-ceiling.html"],
    ["Living Room Interiors","service-living-room.html"],
    ["Bedroom Interiors","service-bedroom.html"],
    ["Pooja Room Interiors","service-pooja-room.html"],
    ["Study Room Interiors","service-study-room.html"],
    ["TV Showcase Interiors","service-tv-showcase.html"],
    ["Dining Room Interiors","service-dining-room.html"],
    ["Cupboards & Wardrobes","service-cupboards-wardrobes.html"],
    ["Kids Room Interiors","service-kids-room.html"],
    ["Toilet Bathroom Interiors","service-toilet-bathroom.html"],
    ["Commercial Interiors","service-commercial.html"]
  ];
  const NAV = [
    ["Home","index.html"],
    ["About Us","about.html"],
    ["Services","services.html", SERVICES, true],
    ["Gallery","gallery-images.html", [["Image Gallery","gallery-images.html"],["Video Gallery","gallery-videos.html"]]],
    ["Contact Us","contact.html", [["Privacy Policy","privacy.html"],["Terms & Conditions","terms.html"],["Sitemap","sitemap.html"]]]
  ];
  window.SITE_SERVICES = SERVICES;
  window.SITE_NAV = NAV;

  const current = document.body.getAttribute("data-page") || "";

  /* ---------- SVG icon set ---------- */
  const I = {
    phone:'<svg viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.24 11 11 0 0 0 3.5.56 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11 11 0 0 0 .56 3.5 1 1 0 0 1-.25 1z"/></svg>',
    mail:'<svg viewBox="0 0 24 24"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm1.4 2L12 12l7.6-5H4.4zM20 8.3l-8 5.2-8-5.2V17h16V8.3z"/></svg>',
    pin:'<svg viewBox="0 0 24 24" stroke="currentColor" fill="none"><path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>',
    clock:'<svg viewBox="0 0 24 24" stroke="currentColor" fill="none"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    wa:'<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15l-1.3 4.8 4.9-1.3A10 10 0 1 0 12 2zm5.8 14.2c-.25.7-1.4 1.3-1.9 1.4-.5.1-1.1.1-1.8-.1-.4-.1-1-.3-1.7-.6-2.9-1.3-4.8-4.3-5-4.5-.1-.2-1.2-1.5-1.2-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.1.1.3 0 .5l-.4.5-.3.3c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.6-.1l.7-.9c.2-.3.4-.2.7-.1l2 .9c.3.1.5.2.6.3.1.2.1.9-.1 1.5z"/></svg>',
    fb:'<svg viewBox="0 0 24 24"><path d="M13.5 22v-8h2.7l.4-3.1h-3.1V8.9c0-.9.25-1.5 1.5-1.5h1.6V4.6c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.5-4 4.1v2.3H7.8V14h2.4v8z"/></svg>',
    ig:'<svg viewBox="0 0 24 24"><path d="M12 2c2.7 0 3 0 4.1.06 1.1.05 1.8.24 2.5.5.7.27 1.2.63 1.8 1.2.57.57.93 1.1 1.2 1.8.26.66.45 1.4.5 2.5C22.2 9 22.2 9.3 22.2 12s0 3-.06 4.1c-.05 1.1-.24 1.8-.5 2.5a4.9 4.9 0 0 1-1.2 1.8 4.9 4.9 0 0 1-1.8 1.2c-.66.26-1.4.45-2.5.5-1.1.06-1.4.06-4.1.06s-3 0-4.1-.06c-1.1-.05-1.8-.24-2.5-.5a4.9 4.9 0 0 1-1.8-1.2 4.9 4.9 0 0 1-1.2-1.8c-.26-.66-.45-1.4-.5-2.5C2.1 15 2.1 14.7 2.1 12s0-3 .06-4.1c.05-1.1.24-1.8.5-2.5a4.9 4.9 0 0 1 1.2-1.8A4.9 4.9 0 0 1 5.6 2.4c.66-.26 1.4-.45 2.5-.5C9.2 2 9.5 2 12 2zm0 1.8c-2.7 0-3 0-4 .06-1 .04-1.5.2-1.9.35-.5.18-.8.4-1.2.76-.36.36-.58.7-.76 1.2-.15.4-.3.9-.35 1.9-.05 1-.06 1.3-.06 4s0 3 .06 4c.04 1 .2 1.5.35 1.9.18.5.4.8.76 1.2.36.36.7.58 1.2.76.4.15.9.3 1.9.35 1 .05 1.3.06 4 .06s3 0 4-.06c1-.04 1.5-.2 1.9-.35.5-.18.8-.4 1.2-.76.36-.36.58-.7.76-1.2.15-.4.3-.9.35-1.9.05-1 .06-1.3.06-4s0-3-.06-4c-.04-1-.2-1.5-.35-1.9a3.2 3.2 0 0 0-.76-1.2 3.2 3.2 0 0 0-1.2-.76c-.4-.15-.9-.3-1.9-.35-1-.05-1.3-.06-4-.06zM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm0 1.8a3.2 3.2 0 1 0 0 6.4 3.2 3.2 0 0 0 0-6.4zM17.4 5.6a1.2 1.2 0 1 1 0 2.4 1.2 1.2 0 0 1 0-2.4z"/></svg>',
    yt:'<svg viewBox="0 0 24 24"><path d="M23 7.5a3 3 0 0 0-2.1-2.1C19 4.9 12 4.9 12 4.9s-7 0-8.9.5A3 3 0 0 0 1 7.5 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.5a3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 23.5 12 31 31 0 0 0 23 7.5zM9.8 15.3V8.7l5.7 3.3z"/></svg>',
    li:'<svg viewBox="0 0 24 24"><path d="M4.98 3.5A2.5 2.5 0 1 1 0 3.5a2.5 2.5 0 0 1 4.98 0zM.5 8.5h4V24h-4zM8.5 8.5h3.8v2.1h.05c.53-1 1.83-2.1 3.77-2.1 4 0 4.78 2.65 4.78 6.1V24h-4v-6.6c0-1.57-.03-3.6-2.2-3.6-2.2 0-2.53 1.72-2.53 3.5V24h-4z"/></svg>',
    pin2:'<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-3.6 19.3c-.08-.8-.16-2 .03-2.9l1.2-5s-.3-.6-.3-1.5c0-1.4.8-2.45 1.8-2.45.86 0 1.27.64 1.27 1.4 0 .86-.55 2.14-.83 3.33-.24 1 .5 1.8 1.48 1.8 1.78 0 3.14-1.87 3.14-4.57 0-2.4-1.72-4.07-4.17-4.07-2.84 0-4.5 2.13-4.5 4.33 0 .86.33 1.78.74 2.28a.3.3 0 0 1 .07.28l-.28 1.15c-.04.18-.15.22-.34.13-1.25-.58-2-2.4-2-3.87 0-3.15 2.29-6.05 6.6-6.05 3.47 0 6.16 2.47 6.16 5.77 0 3.45-2.17 6.22-5.19 6.22-1 0-1.95-.52-2.27-1.14l-.62 2.36c-.22.86-.83 1.94-1.24 2.6A10 10 0 1 0 12 2z"/></svg>',
    arrow:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    up:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M6 15l6-6 6 6"/></svg>',
    play:'<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>',
    home:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 11l9-8 9 8M5 10v10h14V10"/></svg>',
    map:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2zM9 4v14M15 6v14"/></svg>'
  };
  const socialIcon = {facebook:I.fb,instagram:I.ig,youtube:I.yt,linkedin:I.li,pinterest:I.pin2};

  /* ---------- Helpers ---------- */
  const e = s => s==null?"":String(s);
  const telHref = "tel:+" + e(C.phoneRaw);
  const waHref = "https://wa.me/" + e(C.whatsapp) + "?text=" + encodeURIComponent("Hello "+e(C.businessName)+", I'd like to know more about your interior design services.");
  const firstSocialKey = C.primarySocial || "instagram";
  const firstSocialUrl = (C.social||{})[firstSocialKey] || Object.values(C.social||{})[0] || "#";

  function navItem(item){
    const [label,href,sub,mega] = item;
    const isCur = (href===current) || (sub && sub.some(s=>s[1]===current)) ? "current" : "";
    if(sub){
      const subli = sub.map(s=>`<li><a href="${s[1]}">${s[0]}</a></li>`).join("");
      return `<li class="has-sub ${isCur}"><a href="${href}">${label}<i class="caret"></i></a>
        <ul class="submenu ${mega?'mega':''}">${subli}</ul></li>`;
    }
    return `<li class="${isCur}"><a href="${href}">${label}</a></li>`;
  }

  /* ---------- TOP BAR + HEADER ---------- */
  function buildHeader(){
    const socials = Object.entries(C.social||{}).filter(([k,v])=>v).map(([k,v])=>
      `<a href="${v}" target="_blank" rel="noopener" aria-label="${k}">${socialIcon[k]||I.ig}</a>`).join("");
    const topbar = `<div class="topbar"><div class="container">
        <div class="tb-left">
          <a class="tb-item" href="${telHref}">${I.phone}<span>${e(C.phone)}</span></a>
          <a class="tb-item" href="mailto:${e(C.email)}">${I.mail}<span>${e(C.email)}</span></a>
          <span class="tb-item">${I.clock}<span>${e(C.hours)}</span></span>
        </div>
        <div class="tb-social">${socials}</div>
      </div></div>`;
    const navList = NAV.map(navItem).join("");
    const header = `${topbar}
      <div class="nav-wrap"><div class="container"><div class="nav-row">
        <a href="index.html" class="brand" aria-label="${e(C.businessName)} home">
          <img class="brand-logo" src="${A}images/logo.svg" alt="${e(C.businessName)} logo">
        </a>
        <nav class="main-nav" aria-label="Primary"><ul>${navList}</ul></nav>
        <div class="header-cta">
          <a class="btn btn-gold" href="contact.html">Get Free Quote ${I.arrow}</a>
          <button class="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
        </div>
      </div></div></div>`;
    const el = document.querySelector(".site-header");
    el.innerHTML = header;

    /* mobile drawer */
    const mdrawer = document.createElement("nav");
    mdrawer.className="mobile-nav";mdrawer.setAttribute("aria-label","Mobile");
    mdrawer.innerHTML = `<img class="m-logo" src="${A}images/logo.svg" alt="${e(C.businessName)}">
      <ul>${NAV.map(([label,href,sub])=>{
        if(sub){return `<li><div class="m-toggle"><a href="${href}">${label}</a><span class="pl">+</span></div>
          <ul class="m-sub">${sub.map(s=>`<li><a href="${s[1]}">${s[0]}</a></li>`).join("")}</ul></li>`;}
        return `<li><a href="${href}">${label}</a></li>`;
      }).join("")}</ul>
      <a class="btn btn-gold" style="margin-top:20px;width:100%;justify-content:center" href="contact.html">Get Free Quote</a>`;
    document.body.appendChild(mdrawer);
    const scrim=document.createElement("div");scrim.className="scrim";document.body.appendChild(scrim);

    const burger=el.querySelector(".burger");
    const closeDrawer=()=>{mdrawer.classList.remove("open");scrim.classList.remove("open");burger.classList.remove("open");burger.setAttribute("aria-expanded","false")};
    burger.addEventListener("click",()=>{
      const open=mdrawer.classList.toggle("open");scrim.classList.toggle("open",open);
      burger.classList.toggle("open",open);burger.setAttribute("aria-expanded",open);
    });
    scrim.addEventListener("click",closeDrawer);
    mdrawer.querySelectorAll(".m-toggle").forEach(t=>{
      t.querySelector(".pl").addEventListener("click",ev=>{ev.preventDefault();
        t.classList.toggle("open");t.nextElementSibling.classList.toggle("open");});
    });
    mdrawer.querySelectorAll("a").forEach(a=>a.addEventListener("click",closeDrawer));

    /* scrolled state */
    const onScroll=()=>el.classList.toggle("scrolled",window.scrollY>30);
    onScroll();window.addEventListener("scroll",onScroll,{passive:true});
  }

  /* ---------- FOOTER ---------- */
  function buildFooter(){
    const f=document.querySelector(".site-footer");if(!f)return;
    const quick=[["Home","index.html"],["About Us","about.html"],["Services","services.html"],
      ["Gallery","gallery-images.html"],["Contact Us","contact.html"],["Sitemap","sitemap.html"]];
    const svc=SERVICES.slice(0,7);
    const socials=Object.entries(C.social||{}).filter(([k,v])=>v).map(([k,v])=>
      `<a href="${v}" target="_blank" rel="noopener" aria-label="${k}">${socialIcon[k]||I.ig}</a>`).join("");
    f.innerHTML=`<div class="geo-bg"></div><div class="container">
      <div class="f-top">
        <div class="f-about reveal">
          <img class="f-logo" src="${A}images/logo.svg" alt="${e(C.businessName)}">
          <p>${e(C.shortAbout)}</p>
          <div class="f-social">${socials}</div>
        </div>
        <div class="f-col reveal" data-delay="1"><h4>Quick Links</h4><ul>
          ${quick.map(q=>`<li><a href="${q[1]}">${q[0]}</a></li>`).join("")}</ul></div>
        <div class="f-col reveal" data-delay="2"><h4>Our Services</h4><ul>
          ${svc.map(s=>`<li><a href="${s[1]}">${s[0].replace(' Interiors','')}</a></li>`).join("")}</ul></div>
        <div class="f-col f-contact reveal" data-delay="3"><h4>Get In Touch</h4>
          <div class="ci">${I.pin}<span>${e(C.addressLine1)}<br>${e(C.addressLine2)}</span></div>
          <div class="ci">${I.phone.replace('fill="currentColor"','')}<a href="${telHref}">${e(C.phone)}</a></div>
          <div class="ci">${I.mail.replace('<path','<path fill="none" stroke="currentColor" stroke-width="0.0001" ').slice(0,0)||I.mail}<a href="mailto:${e(C.email)}">${e(C.email)}</a></div>
          <div class="ci">${I.clock}<span>${e(C.hours)}<br>${e(C.hoursNote)}</span></div>
          <p class="gst-tag" style="margin-top:8px">GSTIN: ${e(C.gstin)}</p>
        </div>
      </div>
      <div class="f-bottom">
        <span>© <span id="yr"></span> ${e(C.copyrightName)}. All Rights Reserved.</span>
        <div class="legal">
          <a href="privacy.html">Privacy Policy</a>
          <a href="terms.html">Terms &amp; Conditions</a>
          <a href="sitemap.html">Sitemap</a>
        </div>
      </div>
    </div>`;
    const yr=f.querySelector("#yr");if(yr)yr.textContent=new Date().getFullYear();
  }

  /* ---------- FIXED ACTION BAR (mobile) ---------- */
  function buildActionBar(){
    const bar=document.createElement("div");bar.className="action-bar";
    bar.innerHTML=`<ul>
      <li><a class="ab-home" href="index.html"><span class="ab-ic">${I.home}</span>Home</a></li>
      <li><a class="ab-call" href="${telHref}"><span class="ab-ic">${I.phone}</span>Call</a></li>
      <li><a class="ab-map" href="${e(C.mapLink)}" target="_blank" rel="noopener"><span class="ab-ic">${I.map}</span>Map</a></li>
      <li><a class="ab-wa" href="${waHref}" target="_blank" rel="noopener"><span class="ab-ic">${I.wa}</span>WhatsApp</a></li>
      <li><a class="ab-soc" href="${firstSocialUrl}" target="_blank" rel="noopener"><span class="ab-ic">${socialIcon[firstSocialKey]||I.ig}</span>Social</a></li>
    </ul>`;
    document.body.appendChild(bar);
  }

  /* ---------- BACK TO TOP ---------- */
  function buildToTop(){
    const b=document.createElement("button");b.className="to-top";b.setAttribute("aria-label","Back to top");
    b.innerHTML=I.up;document.body.appendChild(b);
    b.addEventListener("click",()=>window.scrollTo({top:0,behavior:"smooth"}));
    window.addEventListener("scroll",()=>b.classList.toggle("show",window.scrollY>600),{passive:true});
  }

  /* ---------- PRELOADER ---------- */
  function preloader(){
    const p=document.createElement("div");p.className="preloader";
    p.innerHTML=`<svg class="pl-mark" viewBox="0 0 120 132">
        <circle cx="58" cy="62" r="50" fill="none" stroke="#C9A24B" stroke-width="2.5"/>
        <path d="M34 100 L34 62 Q34 30 58 30 Q82 30 82 62 L82 100" fill="none" stroke="#E3C77A" stroke-width="3.4" stroke-linecap="round"/>
        <path d="M42 46 L58 88 L74 46" fill="none" stroke="#E3C77A" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <div class="pl-text"><div class="nm">${e(C.businessName)}</div><div class="sub">Interiors</div></div>`;
    document.body.appendChild(p);
    window.addEventListener("load",()=>setTimeout(()=>p.classList.add("done"),550));
    setTimeout(()=>p.classList.add("done"),3500); // safety
  }

  /* ---------- REVEAL / COUNTERS / TILT / ACCORDION / LIGHTBOX ---------- */
  function reveals(){
    const els=document.querySelectorAll(".reveal");
    if(!("IntersectionObserver" in window)){els.forEach(x=>x.classList.add("in"));return;}
    const io=new IntersectionObserver((ents)=>{
      ents.forEach(en=>{if(en.isIntersecting){en.target.classList.add("in");io.unobserve(en.target);}});
    },{threshold:.14,rootMargin:"0px 0px -40px 0px"});
    els.forEach(x=>io.observe(x));
  }
  function counters(){
    const nums=document.querySelectorAll("[data-count]");if(!nums.length)return;
    const io=new IntersectionObserver(ents=>{ents.forEach(en=>{
      if(!en.isIntersecting)return;io.unobserve(en.target);
      const el=en.target,target=+el.getAttribute("data-count"),suf=el.getAttribute("data-suffix")||"";
      let s=0;const dur=1600,t0=performance.now();
      const tick=t=>{const p=Math.min((t-t0)/dur,1);const ease=1-Math.pow(1-p,3);
        el.textContent=Math.round(target*ease).toLocaleString('en-IN')+suf;
        if(p<1)requestAnimationFrame(tick);};requestAnimationFrame(tick);
    });},{threshold:.4});
    nums.forEach(n=>io.observe(n));
  }
  function tilt(){
    if(window.matchMedia("(hover:none)").matches)return;
    document.querySelectorAll(".tilt,.card.tiltable,.feat.tiltable").forEach(card=>{
      card.addEventListener("mousemove",ev=>{
        const r=card.getBoundingClientRect();
        const x=(ev.clientX-r.left)/r.width-.5,y=(ev.clientY-r.top)/r.height-.5;
        card.style.transform=`perspective(900px) rotateY(${x*7}deg) rotateX(${-y*7}deg) translateY(-6px)`;
      });
      card.addEventListener("mouseleave",()=>card.style.transform="");
    });
  }
  function accordion(){
    document.querySelectorAll(".acc-q").forEach(q=>q.addEventListener("click",()=>{
      const acc=q.closest(".acc"),a=acc.querySelector(".acc-a"),open=acc.classList.toggle("open");
      a.style.maxHeight=open?a.scrollHeight+"px":null;
    }));
  }
  function filters(){
    document.querySelectorAll("[data-filter-group]").forEach(group=>{
      const pills=group.querySelectorAll(".pill");
      const targetSel=group.getAttribute("data-target");
      const items=document.querySelectorAll(targetSel+" [data-cat]");
      pills.forEach(p=>p.addEventListener("click",()=>{
        pills.forEach(x=>x.classList.remove("active"));p.classList.add("active");
        const f=p.getAttribute("data-filter");
        items.forEach(it=>{
          const show=f==="all"||it.getAttribute("data-cat")===f;
          it.style.display=show?"":"none";
        });
      }));
    });
  }
  function lightbox(){
    const triggers=[...document.querySelectorAll("[data-lb]")];if(!triggers.length)return;
    const lb=document.createElement("div");lb.className="lightbox";
    lb.innerHTML=`<button class="lb-close" aria-label="Close">${I.up.replace('M6 15l6-6 6 6','M6 6l12 12M18 6L6 18')}</button>
      <button class="lb-nav lb-prev" aria-label="Previous"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M15 6l-6 6 6 6"/></svg></button>
      <button class="lb-nav lb-next" aria-label="Next"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 6l6 6-6 6"/></svg></button>
      <div class="lb-stage"><div class="lb-media"></div><div class="lb-cap"></div></div>`;
    document.body.appendChild(lb);
    const media=lb.querySelector(".lb-media"),cap=lb.querySelector(".lb-cap");let idx=0;
    const show=i=>{idx=(i+triggers.length)%triggers.length;const t=triggers[idx];
      const type=t.getAttribute("data-type")||"image";const src=t.getAttribute("data-lb");
      const c=t.getAttribute("data-cap")||"";
      media.innerHTML = type==="video"
        ? `<video src="${src}" controls autoplay playsinline></video>`
        : `<img src="${src}" alt="${c}">`;
      cap.textContent=c;};
    const open=i=>{show(i);lb.classList.add("open");document.body.style.overflow="hidden";};
    const close=()=>{lb.classList.remove("open");media.innerHTML="";document.body.style.overflow="";};
    triggers.forEach((t,i)=>t.addEventListener("click",e=>{e.preventDefault();open(i);}));
    lb.querySelector(".lb-close").addEventListener("click",close);
    lb.querySelector(".lb-prev").addEventListener("click",()=>show(idx-1));
    lb.querySelector(".lb-next").addEventListener("click",()=>show(idx+1));
    lb.addEventListener("click",e=>{if(e.target===lb)close();});
    document.addEventListener("keydown",e=>{if(!lb.classList.contains("open"))return;
      if(e.key==="Escape")close();if(e.key==="ArrowLeft")show(idx-1);if(e.key==="ArrowRight")show(idx+1);});
  }
  function formStub(){
    document.querySelectorAll("form[data-stub]").forEach(f=>f.addEventListener("submit",ev=>{
      ev.preventDefault();const note=f.querySelector(".form-result")||(()=>{
        const n=document.createElement("p");n.className="form-result";f.appendChild(n);return n;})();
      note.style.cssText="margin-top:14px;color:#1C5152;font-weight:600";
      note.textContent="Thank you! Your enquiry has been noted. Our design team will contact you shortly.";
      f.reset();
    }));
  }

  /* ---------- Token replacement: any [data-cfg="key"] gets text ------- */
  function fillTokens(){
    document.querySelectorAll("[data-cfg]").forEach(el=>{
      const k=el.getAttribute("data-cfg");const v=k.split('.').reduce((o,p)=>o&&o[p],C);
      if(v!=null)el.textContent=v;
    });
    document.querySelectorAll("[data-cfg-href]").forEach(el=>{
      const k=el.getAttribute("data-cfg-href");let v=k.split('.').reduce((o,p)=>o&&o[p],C);
      if(k==="phoneRaw")v=telHref;if(k==="whatsapp")v=waHref;if(v!=null)el.setAttribute("href",v);
    });
    document.querySelectorAll("[data-cfg-src]").forEach(el=>{
      const k=el.getAttribute("data-cfg-src");const v=k.split('.').reduce((o,p)=>o&&o[p],C);
      if(v!=null)el.setAttribute("src",v);
    });
  }

  /* ---------- Optional: override from config.xlsx if hosted ----------- */
  function tryExcel(){
    if(location.protocol==="file:")return;            // fetch blocked locally
    if(typeof XLSX==="undefined")return;
    fetch("config.xlsx").then(r=>r.ok?r.arrayBuffer():Promise.reject()).then(buf=>{
      const wb=XLSX.read(buf,{type:"array"});
      const sh=wb.Sheets["Settings"];if(!sh)return;
      const rows=XLSX.utils.sheet_to_json(sh,{header:1});
      rows.forEach(r=>{const key=(r[0]||"").toString().trim();const val=r[1];
        if(key&&val!=null&&key in C){C[key]=val;}});
      // re-render chrome with overrides
      fillTokens();
    }).catch(()=>{});
  }

  /* ---------- Boot ---------- */
  document.addEventListener("DOMContentLoaded",()=>{
    preloader();buildHeader();buildFooter();buildActionBar();buildToTop();
    fillTokens();reveals();counters();tilt();accordion();filters();lightbox();formStub();
    tryExcel();
  });
})();
