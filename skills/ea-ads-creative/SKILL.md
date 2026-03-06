---
name: ea-ads-creative
description: >
  Cross-platform creative quality audit. Détecte la fatigue créative,
  évalue la diversité des formats, définit les cadences de refresh, et produit
  les priorités de production. Ce skill est complémentaire aux audits
  plateforme-spécifiques (ea-ads-google, ea-ads-meta) qui contiennent les
  checks créa détaillés par plateforme. MCPs utiles : meta-ads (ad library
  pour benchmark créa). Use when user says "creative audit", "ad creative",
  "creative fatigue", "ad copy", "ad design", or "creative review".
---

# Audit Créatif Cross-Plateforme

## Liens

- **Cadre global** : `ea-ads` contient les quality gates et scoring transversaux
- **Checks Google** : `ea-ads-google` contient les checks RSA, ad strength, extensions (ne pas répéter ici)
- **Checks Meta** : `ea-ads-meta` contient les checks créa Meta, DCO, Advantage+ (ne pas répéter ici)
- **MCP** : `meta-ads` — `search_ad_library` pour benchmarker les créas concurrentes

> **Ce skill ne duplique pas les checks par plateforme.** Il se concentre sur la vision **cross-plateforme** : fatigue, diversité, cadences, production.

## Process

1. Collecter les données créa de toutes les plateformes actives
2. Charger `ea-ads/references/platform-specs.md` pour les spécifications
3. Charger `ea-ads/references/benchmarks.md` pour les benchmarks CTR/engagement
4. Évaluer la santé créative transversale
5. Identifier les gaps de formats et les créas fatiguées
6. Générer les priorités de production

## Évaluation Cross-Plateforme

> Les checks détaillés par plateforme sont dans `ea-ads-google` et `ea-ads-meta`.
> Ici on évalue la **cohérence globale** :

- Combien de plateformes ont des créas actives ?
- Y a-t-il un déséquilibre (ex: 20 créas Meta mais 2 sur Google) ?
- Les messages clés sont-ils cohérents entre plateformes ?
- Les visuels sont-ils adaptés aux spécificités de chaque plateforme vs. identiques partout ?

## Creative Fatigue Detection

### Signals of Fatigue
| Signal | Threshold | Action |
|--------|-----------|--------|
| CTR declining | >20% over 14 days | Refresh creative |
| Frequency (Meta) | >5.0 prospecting, >12.0 retargeting | New audience or creative |
| Watch time declining (TikTok) | <3s average | New hook needed |
| QS declining (Google) | Drop of 2+ points | Refresh ad copy |
| Engagement rate drop | >30% decline | Full creative overhaul |

### Refresh Cadence by Platform
| Platform | Recommended Refresh |
|----------|-------------------|
| Google Search | Every 8-12 weeks |
| Meta | Every 2-4 weeks |
| LinkedIn | Every 4-6 weeks |
| TikTok | Every 5-7 days (fastest fatigue) |
| Microsoft | Every 8-12 weeks |
| YouTube | Every 4-8 weeks |

## Format Diversity Matrix

Evaluate which formats are active per platform:

| Format | Google | Meta | LinkedIn | TikTok | Microsoft |
|--------|--------|------|----------|--------|-----------|
| Static Image | RSA image ext | ✅ | ✅ | ❌ | Multimedia |
| Video | YouTube, PMax | ✅ | ✅ | ✅ (required) | ❌ |
| Carousel | ❌ | ✅ | ✅ | ❌ | ❌ |
| Collection | ❌ | ✅ | ❌ | ❌ | ❌ |
| Document | ❌ | ❌ | ✅ | ❌ | ❌ |
| Shopping | PMax, Shopping | Catalog | ❌ | Shop | Shopping |

## Universal Creative Best Practices

### Cross-Platform Safe Zone
- 900x1000px usable area works across all vertical placements
- Keep critical elements centered and within safe margins
- Test on mobile devices (75%+ of ad impressions are mobile)

### Ad Copy Principles
- Lead with benefit, not feature
- Include clear CTA (what should they do next?)
- Match ad message to landing page (message match)
- Use numbers and specifics over vague claims
- Test emotional vs rational appeals

### Video Production Standards
- H.264 codec, AAC audio, MP4 container
- Minimum 720p (1080p preferred)
- Subtitles/captions always (accessibility + sound-off viewing)
- Brand mention within first 5s (awareness) or at CTA (performance)

## Output

### Creative Quality Report

```
Cross-Platform Creative Health

Google:     ████████░░  X/X checks passing
Meta:       ██████████  X/X checks passing
LinkedIn:   ███████░░░  X/X checks passing
TikTok:     █████░░░░░  X/X checks passing
Microsoft:  ████████░░  X/X checks passing
```

### Deliverables
- `CREATIVE-AUDIT-REPORT.md` — Per-platform creative assessment
- Fatigue alerts (any creative past refresh cadence)
- Format diversity gaps per platform
- Production priority list (most impactful creative to produce next)
- Quick Wins (format conversions, CTA changes, Spark Ads setup)
