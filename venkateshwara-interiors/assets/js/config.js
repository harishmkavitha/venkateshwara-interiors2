/* =====================================================================
   VENKATESHWARA INTERIORS — SITE CONFIGURATION
   ---------------------------------------------------------------------
   Edit the values below (or edit config.xlsx and re-export) to reuse
   this website for any client. Every page reads from this object, so
   one change updates the whole site (header, footer, contact, map...).
   ===================================================================== */
window.SITE_CONFIG = {
  /* ---- Brand ---- */
  businessName:   "Venkateshwara Interiors",
  tagline:        "Crafting Soulful Indian Homes",
  shortAbout:     "A premium interior design studio shaping modern Indian homes — from modular kitchens and pooja rooms to complete turnkey interiors, rooted in craft and built to last.",
  establishedYear:"2009",

  /* ---- Contact ---- */
  phone:          "+91 98840 12345",
  phoneRaw:       "919884012345",          /* digits only, for tel: & wa.me */
  whatsapp:       "919884012345",          /* digits only */
  email:          "hello@venkateshwarainteriors.in",
  websiteUrl:     "https://www.venkateshwarainteriors.in",

  /* ---- Address ---- */
  addressLine1:   "No. 24, Sannathi Street, Velachery",
  addressLine2:   "Chennai, Tamil Nadu 600042, India",
  mapEmbed:       "https://www.google.com/maps?q=Velachery,Chennai&output=embed",
  mapLink:        "https://maps.google.com/?q=Velachery,Chennai",

  /* ---- Legal ---- */
  gstin:          "33ABCDE1234F1Z5",
  cin:            "U74999TN2009PTC012345",

  /* ---- Hours ---- */
  hours:          "Mon – Sat: 10:00 AM – 8:00 PM",
  hoursNote:      "Sunday by appointment",

  /* ---- Social (leave blank to hide an icon) ---- */
  social: {
    facebook:  "https://facebook.com/",
    instagram: "https://instagram.com/",
    youtube:   "https://youtube.com/",
    linkedin:  "https://linkedin.com/",
    pinterest: "https://pinterest.com/"
  },
  /* The single icon used in the fixed mobile action bar */
  primarySocial: "instagram",

  /* ---- Trust stats (Home / Why-Choose) ---- */
  stats: [
    { value: 1600, suffix: "+", label: "Homes Designed" },
    { value: 15,   suffix: "+", label: "Years of Craft" },
    { value: 12,   suffix: "",  label: "Interior Specialities" },
    { value: 98,   suffix: "%", label: "Client Referrals" }
  ],

  /* ---- Copyright ---- */
  copyrightName: "Venkateshwara Interiors"
};
