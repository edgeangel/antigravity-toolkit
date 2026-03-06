---
name: ea-ads
description: >
  Comprehensive paid advertising audit and optimization for any business type.
  Performs full multi-platform audits (Google Ads, Meta Ads), single-platform
  deep analysis, conversion tracking health checks, creative quality assessment,
  and compliance verification. Industry detection for SaaS, e-commerce, local
  service, B2B enterprise, info products, mobile app, real estate, healthcare,
  finance, and agency. MCPs utiles : google-ads-gms, meta-ads, google-analytics.
  Triggers on: "ads", "PPC", "paid advertising", "ad audit", "campaign audit",
  "ROAS", "conversion tracking", "creative fatigue", "bid strategy".
---

# Ads — Cadre Audit & Expertise Paid Advertising

Ce skill est le **cadre transversal** du groupe Ads. Il contient l'expertise métier commune : détection industrie, quality gates, scoring, et la connaissance des skills spécialisés à mobiliser.

## Skills liés

| Besoin | Skill à mobiliser | MCPs |
|---|---|---|
| Audit Google Ads approfondi | `ea-ads-google` | `google-ads-gms`, `google-analytics` |
| Audit Meta Ads approfondi | `ea-ads-meta` | `meta-ads` |
| Audit qualité créa cross-plateforme | `ea-ads-creative` | `meta-ads` (ad library) |
| Audit landing pages post-clic | `ea-ads-landing` | browser (PageSpeed) |
| Veille concurrentielle ads | `ea-ads-competitor` | `meta-ads` (`search_ad_library`) |
| Troubleshooting MCP / quirks API | `ea-mcp-usage` | — |

## Process d'audit multi-plateforme

1. Identifier le client et son contexte (`ea-client-context` si pertinent)
2. Détecter le type de business (voir Industry Detection ci-dessous)
3. Identifier les plateformes actives du client
4. Lancer les analyses par plateforme (ea-ads-google, ea-ads-meta)
5. Compléter avec créa cross-plateforme (ea-ads-creative) et landing pages (ea-ads-landing)
6. Agréger les scores → Ads Health Score global
7. Générer le rapport unifié avec plan d'action priorisé

## Industry Detection

Détecter le type de business à partir des signaux du compte :

| Type | Signaux |
|---|---|
| **SaaS** | trial_start/demo_request events, pricing page targeting, attribution longue |
| **E-commerce** | purchase events, product catalog/feed, Shopping/PMax campaigns |
| **Local Service** | call extensions, location targeting, store visits |
| **B2B Enterprise** | LinkedIn Ads actif, ABM lists, CPA toléré élevé ($50+) |
| **Info Products** | webinar/course funnels, lead gen forms |
| **Mobile App** | app install campaigns, in-app events, deep linking |
| **Real Estate** | listing feeds, landing pages spécifiques, geo-heavy |
| **Healthcare** | HIPAA compliance, healthcare ad policies |
| **Finance** | Special Ad Categories, financial products compliance |
| **Agency** | multiple client accounts, white-label reporting |

## Quality Gates

**Règles dures — ne jamais violer :**

| Règle | Plateforme |
|---|---|
| Jamais de Broad Match sans Smart Bidding | Google |
| 3x Kill Rule : CPA > 3x cible → flag pause | Tous |
| Budget min : Meta ≥ 5x CPA par ad set | Meta |
| Ne jamais recommander d'édits en phase d'apprentissage | Tous |
| Toujours vérifier Special Ad Categories (housing/employment/credit) | Meta, Google |
| Attribution par défaut : 7j clic / 1j vue (Meta), data-driven (Google) | Meta, Google |

## Scoring — Ads Health Score (0-100)

Score par plateforme pondéré par budget share :

```
Aggregate = Sum(Platform_Score × Platform_Budget_Share)
```

### Grading

| Grade | Score | Action |
|---|---|---|
| A | 90-100 | Optimisations mineures uniquement |
| B | 75-89 | Quelques opportunités d'amélioration |
| C | 60-74 | Problèmes notables à traiter |
| D | 40-59 | Problèmes significatifs |
| F | <40 | Intervention urgente requise |

### Priorités

| Niveau | Définition |
|---|---|
| **Critical** | Risque de perte de données/revenu → corriger immédiatement |
| **High** | Impact significatif sur la performance → corriger sous 7 jours |
| **Medium** | Opportunité d'optimisation → corriger sous 30 jours |
| **Low** | Best practice, impact mineur → backlog |

## Fichiers de référence

Chargés à la demande, chemin : `ea-ads/references/`

| Fichier | Contenu |
|---|---|
| `scoring-system.md` | Algorithme de scoring pondéré |
| `benchmarks.md` | Benchmarks industrie par plateforme (CPC, CTR, CVR, ROAS) |
| `bidding-strategies.md` | Arbres de décision bidding par plateforme |
| `budget-allocation.md` | Matrice sélection plateforme, scaling, MER |
| `platform-specs.md` | Spécifications créa par plateforme |
| `conversion-tracking.md` | Pixel, CAPI, EMQ, ttclid |
| `compliance.md` | Réglementation, politiques publicitaires, privacy |
| `google-audit.md` | 74 checks Google Ads |
| `meta-audit.md` | 46 checks Meta Ads |
