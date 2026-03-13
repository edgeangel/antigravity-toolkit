---
name: ea-webperf-audit
description: >
  Audit complet de web performance d'un site web. Utilise l'API CrUX (données terrain)
  et l'API PageSpeed Insights (données labo/breakdown) pour produire un diagnostic fiable.
  Génère un rapport synthétique pour les décideurs et un rapport technique détaillé.
  Use when user says "audit webperf", "web performance", "Core Web Vitals", 
  "CWV", "PageSpeed", "LCP", "INP", "CLS", "analyse performance site".
---

# Audit Web Performance

## Liens

- **MCPs** : `bigquery` (CrUX historique), `google-developer-knowledge` (doc Google officielle)
- **Skills liés** : `ea-client-context` (contexte client)
- **APIs externes** : CrUX API (`chromeuxreport.googleapis.com`), PageSpeed Insights API v5 (`pagespeedonline.googleapis.com`)
- **Projet GCP** : `ia-initiatives` — clés API déjà provisionnées

## Philosophie

La web performance est un sujet complexe qui demande de la nuance. **Pas de vision naïve ni simpliste.**

### Enjeux clés à garder en tête

1. **Données terrain ≠ données labo** — Les scores PageSpeed/Lighthouse (labo) simulent un smartphone lent avec throttling CPU 4x et réseau 4G. Les vrais utilisateurs ont souvent de meilleures conditions. Les données CrUX (terrain) reflètent l'expérience réelle et sont celles que Google utilise pour le ranking SEO.

2. **Un score Lighthouse n'est pas un verdict** — Un score de 60/100 ne signifie pas que le site est "lent". Il faut regarder les métriques individuelles (LCP, INP, CLS) et les comparer aux seuils Google, pas uniquement au score agrégé.

3. **Les CWV sont relatifs au contexte** — Un e-commerce chargé en JS aura des CWV différents d'un blog statique. Il faut comparer à des sites du même secteur, pas à une norme abstraite.

4. **L'optimisation est un arbitrage** — Chaque choix technique a des trade-offs : un CMP (Didomi, Axeptio…) ajoute du JS mais est légalement obligatoire. GTM ajoute du poids mais est essentiel au tracking. L'enjeu est l'équilibre, pas l'élimination.

5. **Le TTFB est souvent le premier levier** — Avant de blâmer les scripts tiers, vérifier le temps de réponse serveur. Si le TTFB est mauvais, aucune optimisation front ne compensera.

6. **La saisonnalité existe** — Les CWV fluctuent selon le trafic, le type de visiteurs, les mises à jour du site. Une dégradation ponctuelle n'est pas forcément un problème.

---

## Workflow d'audit

### Phase 1 — Collecte des données (ne pas analyser à ce stade)

Récupérer les données brutes des 3 sources dans l'ordre :

#### 1.1 API CrUX (données terrain temps réel)

```bash
# Prérequis : API Chrome UX Report activée sur le projet GCP
# gcloud services enable chromeuxreport.googleapis.com --project=<PROJECT_ID>
# Clé API existante ou nouvelle : 
# gcloud services api-keys create --display-name="CrUX API Key" --api-target=service=chromeuxreport.googleapis.com

# Snapshot 28 derniers jours — Mobile
curl -s -X POST 'https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=<API_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{"origin":"https://<SITE>","formFactor":"PHONE"}'

# Snapshot 28 derniers jours — Desktop
curl -s -X POST 'https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=<API_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{"origin":"https://<SITE>","formFactor":"DESKTOP"}'

# Historique hebdomadaire (~6 mois)
curl -s -X POST 'https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord?key=<API_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{"origin":"https://<SITE>","formFactor":"PHONE","metrics":["largest_contentful_paint","cumulative_layout_shift","interaction_to_next_paint","first_contentful_paint","experimental_time_to_first_byte","round_trip_time","largest_contentful_paint_image_time_to_first_byte","largest_contentful_paint_image_resource_load_delay","largest_contentful_paint_image_resource_load_duration","largest_contentful_paint_image_element_render_delay","largest_contentful_paint_resource_type","navigation_types"]}'
```

**Données à extraire** : LCP, INP, CLS, FCP, TTFB, RTT + breakdown LCP (img TTFB, load delay, load duration, render delay) + resource type (text/image) + historique hebdomadaire.

#### 1.2 API PageSpeed Insights v5 (données labo + breakdown par script)

```bash
# Prérequis : API PageSpeed activée sur le projet GCP
# gcloud services enable pagespeedonline.googleapis.com --project=<PROJECT_ID>
# Clé API : gcloud services api-keys create --display-name="PageSpeed API Key" --api-target=service=pagespeedonline.googleapis.com

# Audit mobile (prend ~30-60 secondes)
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://<SITE>&strategy=mobile&category=performance&key=<API_KEY>" -o /tmp/pagespeed_result.json
```

**Données à extraire du JSON** :
- `lighthouseResult.categories.performance.score` → score global
- `lighthouseResult.audits.bootup-time.details.items` → **CPU par script** (total, scripting, parse)
- `lighthouseResult.audits.third-party-summary.details.items` → résumé tiers par entité (transferSize, blockingTime, mainThreadTime)
- `lighthouseResult.audits.mainthread-work-breakdown.details.items` → répartition main thread
- `lighthouseResult.audits.render-blocking-resources.details.items` → ressources bloquantes
- `lighthouseResult.audits.network-requests.details.items` → waterfall complet

#### 1.3 BigQuery CrUX (optionnel — historique long terme)

```sql
SELECT
  yyyymm, device,
  p75_lcp AS lcp_p75_ms,
  p75_fcp AS fcp_p75_ms,
  p75_cls AS cls_p75,
  p75_ttfb AS ttfb_p75_ms
FROM `chrome-ux-report.materialized.device_summary`
WHERE origin = 'https://<SITE>'
ORDER BY yyyymm DESC, device
```

Plus de colonnes disponibles : `p75_fid`, `p75_inp`, fractions good/needs_imp/poor pour chaque métrique.

### Phase 2 — Analyse et diagnostic

**Maintenant** analyser les données collectées, dans cet ordre :

#### 2.1 Verdict CWV (terrain)

Comparer les p75 CrUX API aux seuils Google :

| Métrique | BON | MOYEN | MAUVAIS |
|---|---|---|---|
| LCP | ≤ 2 500 ms | ≤ 4 000 ms | > 4 000 ms |
| INP | ≤ 200 ms | ≤ 500 ms | > 500 ms |
| CLS | ≤ 0,1 | ≤ 0,25 | > 0,25 |

Si les 3 sont dans la zone "BON" → **les CWV passent**. C'est la source de vérité pour Google.

**Important** : FCP et TTFB ne sont PAS des CWV officiels mais sont des indicateurs utiles pour diagnostiquer les causes.

#### 2.2 Tendances historiques

Utiliser l'API History / BigQuery pour identifier :
- Tendance générale (amélioration, dégradation, stable ?)
- Points d'inflexion (corrélation avec des déploiements, changements de config ?)
- Saisonnalité (variations normales ?)

#### 2.3 Décomposition du LCP

Le LCP se décompose en 4 phases :
1. **TTFB** — Temps de réponse serveur (infra/backend)
2. **Resource load delay** — Temps avant que le navigateur commence à charger la ressource LCP
3. **Resource load duration** — Temps de téléchargement de la ressource LCP
4. **Element render delay** — Temps entre le chargement de la ressource et son rendu à l'écran

Identifier quelle phase est le bottleneck principal.

#### 2.4 Breakdown par script tiers (PageSpeed)

Du bootup-time, calculer :
- Part de chaque script dans le budget JS total
- Total CPU des scripts tiers vs code applicatif
- Blocking time par entité (si disponible dans third-party-summary)

#### 2.5 Écart labo vs terrain

Expliquer systématiquement l'écart entre Lighthouse et CrUX :
- Lighthouse utilise un throttling CPU 4x + réseau 4G simulé
- Les vrais utilisateurs ont de meilleures conditions (en général)
- Le cache navigateur aide les visiteurs récurrents
- **Les données CrUX sont la source de vérité pour le SEO Google**

---

## Livrables

### Livrable 1 — Synthèse client (non-initiés)

**Ton** : direct, factuel, pas de jargon inutile. Écrire en "tu". Pas de ton IA.

Structure :
1. **Comment on mesure** — 2-3 phrases sur la méthode (données terrain vs labo)
2. **Résultat** — Tableau simple des 3 CWV avec verdict BON/MOYEN/MAUVAIS
3. **Impact des scripts tiers** — Tableau comparatif "qui prend quoi" avec pourcentages
4. **Recommandations** — Ce qu'on peut faire, ce qui dépend du client
5. **Proposition de suite** — Offre d'accompagnement si pertinent

### Livrable 2 — Rapport technique détaillé

Structure :
1. **CrUX API** — Tableau complet des métriques terrain (p75 + distribution good/needs/poor)
2. **CrUX BigQuery** — Historique mensuel avec tendances
3. **CrUX History API** — Évolution hebdomadaire avec breakdown LCP
4. **PageSpeed Insights** — Bootup-time par script, main thread breakdown, third-party summary
5. **Conformité implémentation CMP** — Si CMP audité, tableau de vérification vs recos éditeur
6. **Méthodologie** — Sources, APIs, clés API, commandes utilisées (reproductibilité)

### Livrable 3 — Google Doc client (format EA)

→ **Utiliser le skill `ea-brand-assets`** pour convertir le rapport Markdown en Google Doc brandé EdgeAngel.

Le livrable Markdown (Livrable 1) sert d'input. Le skill `ea-brand-assets` gère :
- La copie du template agence EA (header, footer, styles)
- La conversion Markdown → Google Docs API (titres, listes, tableaux, gras/italique)
- L'insertion et le formatage des tableaux (protocole bottom-to-top)

**Tableaux attendus dans le livrable Google Doc** :

| # | Tableau | Taille | Description |
|---|---------|--------|-------------|
| 1 | CWV Seuils | 5×3 | Métrique, Valeur p75, Seuil Google |
| 2 | Matrice multi-pages | N×6 | Page, Score PSI, LCP, TBT, CLS, Verdict |
| 3 | CrUX Mobile | N×5 | Métrique, p75, %Bon, %Moyen, %Mauvais |
| 4 | CrUX Desktop | N×5 | Idem mobile |
| 5 | Patterns transversaux | N×4 | Problème, Impact CPU, Pages, Solution |
| 6 | Décomposition LCP | 5×4 | Phase, Durée, %LCP, Diagnostic |
| 7 | Recommandations | N×5 | #, Action, Impact, Complexité, Responsable |

---

## Recommandations types par cause

| Cause identifiée | Recommandation | Priorité |
|---|---|---|
| **TTFB serveur élevé** (> 800ms) | Optimiser le serveur (cache applicatif, CDN, upgrade hébergement) | Critique — c'est souvent le 1er levier |
| **LCP img render delay élevé** | Précharger l'image LCP (`<link rel="preload">`), réduire le JS bloquant | Haute |
| **LCP img load delay élevé** | Vérifier que l'image LCP n'est pas lazy-loaded, précharger via preload | Haute |
| **CLS > 0.1** | Dimensionner les éléments (attributs width/height, réserver l'espace pub/bandeau) | Haute |
| **INP > 200ms** | Réduire les long tasks JS, fractionner le code, utiliser `requestIdleCallback` | Moyenne |
| **Scripts tiers lourds** | Évaluer le rapport bénéfice/coût de chaque script, charger en `defer`/`async` | Moyenne |
| **Pas de CDN** | Implémenter un CDN (Cloudflare, Fastly, Cloud CDN) | Haute si TTFB élevé |

---

## Prérequis techniques

### APIs à activer (projet GCP)

```bash
gcloud services enable chromeuxreport.googleapis.com --project=<PROJECT_ID>
gcloud services enable pagespeedonline.googleapis.com --project=<PROJECT_ID>
```

### Clés API

Créer des clés restreintes par service :
```bash
gcloud services api-keys create --display-name="CrUX API Key" \
  --api-target=service=chromeuxreport.googleapis.com --project=<PROJECT_ID>

gcloud services api-keys create --display-name="PageSpeed API Key" \
  --api-target=service=pagespeedonline.googleapis.com --project=<PROJECT_ID>
```

### Clés existantes (projet ia-initiatives)

Les clés API sont stockées dans les variables d'environnement suivantes (ne jamais les hardcoder) :

```bash
export CRUX_API_KEY="<récupérer depuis Google Cloud Console>"
export PAGESPEED_API_KEY="<récupérer depuis Google Cloud Console>"
```

Récupérer les clés : [Google Cloud Console → API Keys](https://console.cloud.google.com/apis/credentials?project=ia-initiatives)

### Parsing des résultats

Pour parser le JSON PageSpeed, utiliser Python avec `python3 -c "import json; ..."` ou un script dédié. Les clés principales sont documentées dans la section 1.2 ci-dessus.

---

## Notes métier

- **Le score Lighthouse n'est qu'un indicateur** — Ne jamais utiliser le score seul comme verdict. Toujours croiser avec les données terrain CrUX.
- **Les CMPs sont légalement obligatoires** — Impossible de recommander la suppression de Didomi/Axeptio. L'enjeu est de vérifier que l'implémentation est optimale.
- **Le tracking est un prérequis business** — GTM + GA4 + pixels ads ont un coût en JS, mais leur suppression n'est pas une option. L'enjeu est le séquençage et le chargement conditionnel au consentement.
- **Pandoc** — Pour livrer en .docx au client : `pandoc <fichier>.md -o <fichier>.docx`
