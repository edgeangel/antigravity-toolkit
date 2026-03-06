# Cheval Energy — Contexte Client

> **Dernière mise à jour :** Février 2026
> **Site :** [cheval-energy.com](https://www.cheval-energy.com/fr/)

---

## 1. Identité & Business Model

- **Secteur :** E-commerce équin (compléments alimentaires, soins, bien-être du cheval)
- **Type :** E-commerce produit
- **Positionnement :** Spécialiste des produits pour chevaux, avec une gamme propriétaire + distribution multi-marques
- **Particularités :**
  - Possède ses **marques propres** (Cheval Energy = marque mère) et des **marques "maison"** (distributeur exclusif)
  - Distribue également des **marques tierces**
  - Les **taux de marge varient significativement** selon les marques : les plus hautes marges sur les produits propres/maisons

---

## 2. Stratégie Marketing Globale

### Objectif 2026
**Générer de la croissance dans le cadre du budget alloué (310k€ ads).**

La croissance prioritaire est celle de la **marge** (disponible via BigQuery/Capture v2, bien que le calcul soit plus complexe). L'optimisation doit trouver l'équilibre entre trois axes :
1. **Croissance en marge** (priorité n°1) — via la priorisation des marques propres/maisons à forte marge
2. **Croissance en volume d'achats et en CA** (court terme) — pour maintenir un niveau d'activité sain et visible pour le client
3. **Acquisition de nouveaux clients** (moyen terme) — clé pour la croissance durable, pilotée via le ratio NC et le CPA NC

> [!IMPORTANT]
> Le client regarde son **CA Back-Office** — pas le CA GA4. Toute communication de "croissance" doit être cohérente avec ce que le client observe dans son BO. Cf. écart BO/GA4 documenté en §7.

### Principes stratégiques
- **Marge > Volume** : La priorité n°1 est de pousser les marques à forte marge (marques BHG)
- **Ne pas invisibiliser les marques tierces** : Elles génèrent du volume et du CA — elles restent nécessaires pour le chiffre d'affaires global
- **Segmentation fine par ROAS cible** : Les ROAS cibles sont différenciés selon le niveau de marge — plus la marge est haute, plus le ROAS cible est bas (on accepte un coût d'acquisition plus élevé)
- Les campagnes à ROAS cible plus élevé (1200-1400) sont sur des marques à marge plus faible → on exige un retour publicitaire plus strict pour compenser

### KPIs prioritaires
- Marge estimée (via BigQuery)
- CA global et panier moyen
- Volume d'achats
- ROAS par niveau de priorité
- Part des dépenses par catégorie de priorité
- Nouveaux clients (volume + ratio + CPA NC)

---

## 3. Leviers Actifs & Structure de Campagnes

> La structure de campagnes ci-dessous est la **traduction opérationnelle de l'objectif 2026** (§2). Elle a été restructurée en janvier 2026 pour répondre aux enjeux de croissance de la marge dans le budget alloué.

### Google Ads — Structure détaillée (17 campagnes)

> **Note :** Cette structure segmentée a été mise en place **courant janvier 2026**, avec une mise à jour des priorités marques.

La structure repose sur une **segmentation par niveau de marge**, organisée en 4 niveaux de priorité + campagnes complémentaires.

#### Répartition budgétaire cible

| Catégorie | Part des dépenses visée |
|---|---|
| **PRIO 1** — Super marge | ~35% |
| **PRIO 2** — Marques Top Marge | ~20-30% |
| **PRIO 3** — Top marques | ~15-20% |
| **PRIO 4** — Reste du catalogue | ~10% |
| **Autres** (Brand, Acquisition, DemandGen, Autres pays) | ~10-20% |

---

#### 🟢 PRIO 1 — Super marge (Marques maison + dépôt margé)

Les campagnes les plus stratégiques. Marques propres et marques en dépôt avec forte marge.

| Campagne | Type | Marques / Contenu | ROAS cible | Notes |
|---|---|---|---|---|
| FR - Performance - Mixte (ROAS-NC) - PMax - Marque BHG - CE | PMax | **Cheval Energy** (marque mère) | **900** | La plus importante, meilleure marge, la plus connue des marques maisons |
| FR - Performance - Mixte (ROAS-NC) - PMax - Autres Marques BHG | PMax | Phytology Vetcare, Gamme du maréchal, ProbioHorse, Stop Fourbure, Pony Power, Horseflex Care, AromaHorse | **720** | Très forte marge, marques plus spécifiques/niche, parfois moins connues |
| FR - Performance - Mixte (ROAS-NC) - PMax - Marques Dépôt margé | PMax | Reverdy, NAF, TRM | **1000** | Stocks importants à écouler, bonne marge |

**Logique :** ROAS cibles les plus bas → on accepte un coût publicitaire plus élevé car la marge absorbe largement.

---

#### 🟡 PRIO 2 — Marques Top Marge (taux de marge >42%) + Top produits

| Campagne | Type | Marques / Contenu | ROAS cible | Notes |
|---|---|---|---|---|
| FR - Performance - Mixte (ROAS-NC) - PMax - Marques Top Marge | PMax | Natural Innov, Hilton Herbs, Jump'in, Michel Vaillant, NaturaCheval, Keratex, Or Vet, Paskacheval, LPC Labo, Alodis Care, Alliance Équine, Equi-mojo, Waldhausen | **1000** | Seuil de marge >42% |
| FR - Performance - Mixte - PMax (ROAS-NC) - Produits Top Marge - hors BHG | PMax | Divers produits de toutes marques (hors marques maison) avec très bonnes marges | **1200** | Logique produit plutôt que marque |

---

#### 🟠 PRIO 3 — Top marques (mix volume + marge)

| Campagne | Type | Marques / Contenu | ROAS cible | Notes |
|---|---|---|---|---|
| FR - Performance - Mixte (ROAS-NC) - PMax - Top Marques | PMax | Nutragile, Ravene, Equistro, Alodis Care, DRJ, Ekin, Ekkia, Aqua Cheval, Nellumbo, Signs, Ekinat, Harry's Horse, Happy Crackers, First Ekine, David Rossi, Bleu Roy | **1200** | Mix marques volume/marge moyenne + peu de volume/bonne marge |
| FR - Performance - Mixte (ROAS-NC) - Search - Top Produits | Search | Mix de produits best-sellers (sans flux produits) | **1300** | Campagne Search only |
| FR - Performance - Mixte (ROAS-NC) - PMax - Audevard | PMax | **Audevard** | **1400** | Marque la plus vendue du site, gros volume + CA, mais marge limitée |

---

#### 🔴 PRIO 4 — Reste du catalogue

| Campagne | Type | Contenu | ROAS cible | Notes |
|---|---|---|---|---|
| FR - Performance - Mixte (ROAS-NC) - PMax - All Marques | PMax | Reste du catalogue | **1400** | Catch-all |
| FR - Performance - Mixte (ROAS-NC) - Search - Marques | Search | Noms de marques distribuées | **1400** | — |
| FR - Performance - Mixte (ROAS-NC) - PMax No Shopping - Catégories | PMax (sans Shopping) | Catégories produits (search + display) | **1400** | — |
| FR - Performance - Mixte (ROAS-NC) - Search - Catégories | Search | Catégories de produits | **1400** | — |

**Logique PRIO 4 :** ROAS cible le plus élevé → on exige un retour strict car les marges sont plus faibles.

---

#### ⚪ Autres campagnes

| Campagne | Type | Objectif | ROAS cible | Notes |
|---|---|---|---|---|
| FR - Croissance - CA-ROAS - DemandGen | Demand Gen | Haut de funnel / notoriété | — | Acquisition d'audiences froides |
| FR - Performance w/Brand - CA-ROAS - PMax - Tous les Produits | PMax | Remarketing (brand inclus) | **2200** | Vocation remarketing, nom de marque "Cheval Energy" inclus |
| FR - Performance - ACQ-NC - PMax - Tous les Produits | PMax | Acquisition nouveaux clients | **600** | Exclusion de marque, ciblage nouveaux clients uniquement |
| BE-CH - Performance - Mixte (ROAS-NC) - PMax - Tous les produits | PMax | Expansion internationale | **1400** | Belgique, Suisse, Luxembourg |
| FR - Brand - Achats - Search - Cheval Energy | Search | Protection de marque | — | Défense du brand |

---

### Meta Ads — Structure détaillée (4 campagnes)

Les campagnes Meta sont des campagnes de **Croissance** — elles ciblent des audiences plus froides et plus haut dans le funnel que Google/Microsoft. Elles visent soit l'activation de nouvelles audiences (nouveaux clients), soit la génération de CA (y compris via la réactivation de clients existants pas en process d'achat).

| Campagne | Objectif | Attribution | Cible | Focus |
|---|---|---|---|---|
| **CE-EA - Croissance - MémoMarque - Adv - Fil rouge** | Notoriété (mémo de marque) | — | Large | Pas d'objectif de conversion — augmentation de la mémorisation de marque |
| **CE-EA - Croissance - ACQ-NC - Run promo** | Achats nouveaux clients | 7j clic, 1j vue | Prospection | Promos du site, nouveautés — focus acquisition NC |
| **CE-EA - FR - Croissance - CA-ROAS - Catégories** | Achats (CA/ROAS) | 7j clic uniquement | Large (dont clientèle existante) | Attribution plus stricte, post-clic uniquement. Publicités sur les grandes catégories du site (phyto, compléments, etc.) |
| **CE-EA - FR - Croissance - CA-ROAS - Retargeting** | Achats (retargeting) | 7j clic | Visiteurs non-acheteurs récents | Retargeting de visiteurs du site sur des catégories spécifiques |

> [!NOTE]
> **Écart d'attribution régie vs GA4 :** La vision régie Meta mélange post-clic et post-view (attribution plus large), tandis que GA4 est essentiellement post-clic (même si elle modélise en data-driven). GA4 sous-estime donc très largement l'apport de Meta (d'où les ROAS GA4 très faibles : 0,5-0,8 vs ROAS régie 20-50). C'est un biais structurel à avoir en tête pour l'analyse, sans nécessairement le rappeler systématiquement dans chaque bilan.

### Microsoft Ads

La structure Microsoft Ads **ne suit pas la segmentation par marge** appliquée sur Google Ads. Raison : les volumes sur Microsoft sont nettement inférieurs — appliquer la même granularité (PRIO 1-4) risquerait de **sur-segmenter des campagnes à faible volume** et de brider l'algorithme d'enchères, déjà moins performant que celui de Google.

> [!NOTE]
> **Chantier à venir :** Discuter d'une optimisation de la structure Microsoft Ads pour orienter davantage la diffusion vers les produits à meilleure marge, sans casser les performances actuelles (meilleurs ratios NC du portefeuille : 31-35%). Le défi est de trouver un compromis entre segmentation marge et maintien de volumes suffisants pour l'algorithme.

---

## 4. Catalogue & Mix Produits/Marques (Données 2025)

> **Source :** Analyse renta marques 2025 (données annuelles)
> **CA Total 2025 :** 6 441 334 € | **Marge Brute Totale :** 2 642 889 € | **Taux de marge moyen :** 41%

### Performance par groupe stratégique (aligné sur les PRIO Google Ads)

| Groupe stratégique | CA 2025 (€) | Marge (€) | Taux de marge | Lien campagne |
|---|---|---|---|---|
| **PRIO 1 — Marques BHG (CE)** | 1 275 936 | 804 470 | **63%** | PMax Marque BHG - CE |
| **PRIO 1 — Autres BHG** | 358 046 | 199 286 | **56%** | PMax Autres Marques BHG |
| **PRIO 1 — Marques Dépôt margé** | 811 774 | 320 113 | **39%** | PMax Marques Dépôt margé |
| **PRIO 2 — Top Marges >42%** | 622 339 | 290 266 | **47%** | PMax Marques Top Marge |
| **PRIO 3 — Audevard** | 1 196 827 | 368 679 | **31%** | PMax Audevard |
| **PRIO 3 — Top Marques flux** | 805 091 | 243 300 | **30%** | PMax Top Marques |
| **PRIO 4 — Reste marques** | 1 403 639 | 425 716 | **30%** | PMax All Marques + Search |

> **Lecture clé :** Les marques PRIO 1 représentent ~38% du CA mais ~50% de la marge totale. À l'inverse, Audevard représente ~19% du CA mais seulement ~14% de la marge.

### Top 20 marques par contribution marge (2025)

| # | Marque | Code | CA (€) | Marge (€) | Taux | Groupe |
|---|---|---|---|---|---|---|
| 1 | **Cheval Energy** | CE | 1 275 936 | 804 470 | **63%** | PRIO 1 — BHG |
| 2 | Audevard | AU | 1 196 827 | 368 679 | 31% | PRIO 3 |
| 3 | Reverdy | RV | 497 292 | 183 195 | 37% | PRIO 1 — Dépôt |
| 4 | **Phytology Vetcare** | PY | 238 067 | 134 923 | **57%** | PRIO 1 — Autres BHG |
| 5 | Greenpex | GP | 426 606 | 118 030 | 28% | PRIO 4 |
| 6 | TRM | SE | 171 479 | 78 893 | 46% | PRIO 1 — Dépôt |
| 7 | Natural'Innov | IC | 185 904 | 74 217 | 40% | PRIO 2 |
| 8 | NAF | NA | 143 003 | 57 527 | 40% | PRIO 1 — Dépôt |
| 9 | Hilton Herbs | HB | 125 994 | 53 323 | 42% | PRIO 2 |
| 10 | Nutragile | NU | 141 701 | 50 359 | 36% | PRIO 3 |
| 11 | Michel Vaillant | MV | 78 627 | 38 029 | 48% | PRIO 2 |
| 12 | Equistro | VQ | 95 662 | 36 341 | 38% | PRIO 3 |
| 13 | Ravene | RA | 103 286 | 33 082 | 32% | PRIO 3 |
| 14 | Gamme du Maréchal | OM | 55 510 | 28 797 | 52% | PRIO 1 — Autres BHG |
| 15 | Horseflex | HX | 48 496 | 28 480 | 59% | PRIO 1 — Autres BHG |
| 16 | Horsemaster | HM | 120 709 | 27 867 | 23% | PRIO 4 |
| 17 | Pommier | FA | 115 885 | 27 639 | 24% | PRIO 4 |
| 18 | Keratex | KT | 53 217 | 27 015 | 51% | PRIO 2 |
| 19 | Twydil | TW | 75 498 | 23 030 | 31% | PRIO 4 |
| 20 | ESC | ES | 59 418 | 23 021 | 39% | PRIO 4 |

### Marques à très forte marge (>50%)

| Marque | Taux de marge | CA (€) | Groupe |
|---|---|---|---|
| TIMAB Magnesium | **71%** | 10 844 | Niche |
| **Cheval Energy** | **63%** | 1 275 936 | PRIO 1 — BHG |
| **Horseflex** | **59%** | 48 496 | PRIO 1 — Autres BHG |
| AromaHorse Care | **59%** | 1 177 | PRIO 1 — Autres BHG |
| **Phytology Vetcare** | **57%** | 238 067 | PRIO 1 — Autres BHG |
| Waldhausen | **56%** | 19 142 | PRIO 2 |
| Aquacheval | **56%** | 2 856 | PRIO 3 |
| StopFourbure | **55%** | 18 185 | PRIO 1 — Autres BHG |
| Gamme du Maréchal | **52%** | 55 510 | PRIO 1 — Autres BHG |
| Keratex | **51%** | 53 217 | PRIO 2 |

### Marques à faible marge (<30%) — Points de vigilance

| Marque | Taux de marge | CA (€) | Risque |
|---|---|---|---|
| Horsemaster | 23% | 120 709 | Fort volume, faible rentabilité |
| Pommier | 24% | 115 885 | Idem |
| Greenpex | 28% | 426 606 | **Top 5 CA mais marge très basse** — attention au poids dans les dépenses |
| Costalfa France | **7%** | Faible | Marge quasi nulle |

### Problématiques stock et catalogue
- **Reverdy, NAF, TRM** : stocks importants à écouler → ces marques sont poussées en PRIO 1 malgré le fait qu'elles ne soient pas des marques maison
- **ESC** : historiquement mise en retrait (-90% de CA YoY en 2025) par manque de rentabilité ou ruptures
- **Greenpex** : 5ème marque en CA (426k€) mais seulement 28% de marge → surveiller le poids de cette marque dans les dépenses publicitaires
- **Notes concurrentielles internes** : StopFourbure est considéré comme concurrent du best-seller ThinLine ; ProbioHorse comme concurrent du Proferm

---

## 4. Budgets & Objectifs 2026

### Budget annuel (Total Ads, hors frais EA)

| Année | Total Ads | Google Ads | Meta Ads | Microsoft Ads | Évolution YoY |
|---|---|---|---|---|---|
| **2024** | 285k€ | 240k€ | 21,8k€ | 7k€ | — |
| **2025** | 293k€ | 245,5k€ | 30,5k€ | 11,6k€ | +2,8% |
| **2026** | **310k€** | **265,5k€** | **32,5k€** | **12k€** | **+5,8%** |

### Budget mensuel 2026 (Ads uniquement)

| Mois | Google Ads | Meta | Microsoft | **Total** |
|---|---|---|---|---|
| Janvier | 19 000€ | 2 500€ | 1 000€ | **22 500€** |
| Février | 17 500€ | 2 500€ | 1 000€ | **21 000€** |
| Mars | 24 000€ | 3 000€ | 1 000€ | **28 000€** |
| Avril | 23 500€ | 3 000€ | 1 000€ | **27 500€** |
| Mai | 24 000€ | 2 500€ | 1 000€ | **27 500€** |
| Juin | 24 500€ | 3 000€ | 1 000€ | **28 500€** |
| Juillet | 24 500€ | 3 500€ | 1 000€ | **29 000€** |
| Août | 21 000€ | 2 500€ | 1 000€ | **24 500€** |
| Septembre | 22 000€ | 2 500€ | 1 000€ | **25 500€** |
| Octobre | 24 500€ | 2 500€ | 1 000€ | **28 000€** |
| Novembre | 23 000€ | 2 500€ | 1 000€ | **26 500€** |
| Décembre | 18 000€ | 2 500€ | 1 000€ | **21 500€** |

> [!NOTE]
> La répartition par levier est **indicative** — le total ads mensuel est l'enveloppe de référence. Les ajustements entre leviers se font en fonction des performances observées.

### ROAS cibles par levier (vision régie)

| Levier | ROAS cible | Notes |
|---|---|---|
| **CE Google Ads** | 13+ | Hors campagne de marque, noto PMax incluse |
| **CE Meta Ads** | 7 | Vision régie (7j clic) |
| **CE Microsoft Ads** | 5 | Vision régie |

---

## 5. Calendrier Promotionnel & Saisonnalité

### Saisonnalité observée (basée sur les bilans 2025)

| Période | Dynamique | Impact CA | Notes |
|---|---|---|---|
| **Janvier-Février** | Creux saisonnier | Faible (~235-137k€/mois) | Taux de conversion au plus bas, sensibilité aux ruptures de stock |
| **Mars-Avril** | Reprise forte | En hausse (~290-306k€) | Saison des concours équestres, restart du marché |
| **Mai-Juin** | Stabilisation | Stable (~290-306k€) | Soldes d'été (résultats inégaux), montée des marques propres |
| **Juillet-Août** | Creux estival | En baisse (~278k€ et moins) | Trafic -8%, effet soldes quasi inexistant |
| **Septembre-Octobre** | Réaccélération | En hausse (~259-306k€) | Rentrée, Salon Equita Lyon (oct), braderie physique |
| **Novembre** | **Pic annuel** | **Record (~551k€)** | Black Week / Black Friday, mois record historique |
| **Décembre** | Normalisation | ~376k€ | Bonnes ventes Noël, ralentissement fin de mois |

### Événements commerciaux récurrents
- **Black Friday / Black Week** (novembre) : temps fort majeur, x2 sur les volumes
- **Equita Lyon** (octobre) : salon physique avec impact online + boutique
- **Braderie Cheval Energy** (octobre) : ventes record en boutique physique
- **Soldes d'été** (juin-juillet) : impact variable, moins fort qu'attendu en 2025
- **Happy Jeudi Paskacheval** (novembre) : opération marque spécifique, bons résultats
- **Promotions saisonnières** : gale de boue (hiver), confort gastrique (hiver), vermifugation

### Patterns saisonniers produits
- **Hiver** : produits gale de boue, confort gastrique, compléments immunité
- **Printemps** : compléments sportifs, soins des sabots, anti-insectes
- **Été** : soins anti-mouches, hydratation, crèmes solaires
- **Automne** : vermifuges, compléments articulaires, préparation hiver

---

## 7. Données & Tracking

- **BigQuery :** Projet `ia-initiatives` — données Capture v2
- **GA4 :** Propriété `properties/280091548` — "01 - Cheval Energy" (compte Blue Horse Group)
- **Logique de segmentation bilan** :
  - **Pôle "Performance"** (bas de funnel) : Google Ads, Microsoft Ads → focus CA + ROAS
  - **Pôle "Croissance"** (haut/milieu de funnel) : Meta Ads → focus NC + CPA

> [!CAUTION]
> **Bug GA4 item-level (non résolu)** : Les métriques `itemsPurchased` et `itemRevenue` sont **incorrectes au niveau produit**. Dans les paniers multi-produits, un seul item peut absorber l'ensemble des conversions et du revenu de la transaction. Ce bug est en cours de résolution côté dev mais persiste depuis longtemps.
> 
> **Conséquence :** Pour toute analyse produit dans GA4, **seules les métriques `itemsViewed` et `itemsAddedToCart` sont fiables**. Ne pas utiliser `itemsPurchased` ni `itemRevenue` pour des conclusions au niveau individuel produit.

> [!WARNING]
> **Écart BO (Back-Office) vs GA4 sur le CA** : En 2025, GA4 sous-comptait significativement le CA par rapport au BO site. Cet écart a été largement résorbé en 2026, ce qui **gonfle artificiellement les comparaisons YoY GA4**.
>
> | Mois | CA BO (site) | CA GA4 | Écart | Note |
> |---|---|---|---|---|
> | **Jan 2025** | 434k€ | 392k€ | **-9,7%** | GA sous-compte fortement |
> | **Jan 2026** | 418k€ | 407k€ | **-2,6%** | Écart quasi résorbé |
> | **Fév 2025** | 413k€ | 359k€ | **-13,1%** | GA sous-compte très fortement |
> | **Fév 2026** | 415 638€ (HT) | 406 000€ (HT) | **~2,4%** | Écart quasi résorbé. Mollie TTC = 451 683€, Prestashop TTC = 456 253€ |
>
> **Conséquence pour les bilans :** La YoY GA4 montre une croissance (ex: Jan +3,8%) alors que le BO du client montre une décroissance (-3,7%). Le client qui regarde son BO ne comprend pas qu'on parle de croissance. **Toujours caveaté les YoY quand on compare 2026 vs 2025.**

---

## 8. Problématiques Spécifiques

### Problématiques structurelles
- **Pression sur les marges** : le mix marques propres vs marques distribuées est critique pour la rentabilité → toute dérive vers les marques à faible marge impacte directement le résultat
- **Concentration de la marge** : Cheval Energy (CE) seule génère 30% de la marge totale du site (804k€ sur 2,6M€) — forte dépendance à une seule marque
- **Baisse du panier moyen** : tendance observée tout au long de 2025 (~80-84€ vs ~85€ en 2024), liée au pivot vers les produits CE (moins chers mais plus margés)
- **Dépendance au paid** : les leviers payants représentent 60-73% des ventes du site selon les mois, en forte hausse vs 2024 (38%)

### Problématiques opérationnelles (observées en 2025)
- **Ruptures de stock chroniques** : problème majeur en janvier-février 2025, avec perte de 300+ références shopping ; amélioration progressive au S2
- **ESC brand phase-out** : arrêt progressif de la marque ESC (-90% CA YoY) pour manque de rentabilité/ruptures — transition vers les marques BHG
- **Conversion rate fragile** : taux de conversion en recul YoY sur la majeure partie de 2025, amélioré au Q4 grâce à la disponibilité stock
- **Widget "Je découvre" disparu** : module UX redirigeant les utilisateurs depuis les pages en rupture vers d'autres produits — impact négatif sur le trafic organique

### Problématiques par levier
- **Meta Ads** : ROAS GA4 très faible (0,5-0,8) vs ROAS régie très élevé (20-50) → fort écart d'attribution, difficulté à justifier les investissements. Fatigue créative récurrente.
- **Microsoft Ads** : levier sous-exploité mais très efficace en conquête (ratio NC 31-35% vs 23% moyenne) — bug tracking résolu en août 2025
- **Greenpex** : 5ème marque en CA (427k€) mais 28% de marge seulement — surveiller le poids dans les dépenses publicitaires
- **Audevard** : 2ème marque en CA (1,2M€) mais seulement 31% de marge — pilotage strict du ROAS (cible 1400)

---

## 9. Historique des Décisions Stratégiques

| Date | Décision | Détails |
|---|---|---|
| Jan 2025 | Réduction budget retargeting | Haute répétition, faible efficacité |
| Mars 2025 | Scaling agressif (+40% budget) | Rattrapage du sous-investissement de début d'année, capitaliser sur la reprise saisonnière |
| Mars 2025 | Succès DemandGen YouTube | Campagne CE avec ROAS 33, +40k€ de CA |
| Avr 2025 | Lancement Stop'Fourbure Light | ~50 ventes en 1er mois, haute marge |
| Mai 2025 | Début transition ESC → BHG | Arrêt progressif de la marque ESC, focus marques propres |
| Mai 2025 | Lancement Microsoft Ads PMax | Nouvelles campagnes pour diversification |
| Juin 2025 | Pivot budget vers marques BHG | BHG passe à 22% du budget Google Ads |
| Juin 2025 | Approche LTV | Transition vers optimisation LTV (vs ROAS immédiat) |
| Juil 2025 | Création campagnes "Top marge" | Segmentation par seuil de marge >40% |
| Juil 2025 | Campagne acquisition NC dédiée | Ciblage exclusif nouveaux clients |
| Sept 2025 | Réaccélération post-été | +36% budget vs août pour regagner les volumes |
| Sept 2025 | Bug tracking Bing résolu | Impact sur le suivi des conversions Microsoft Ads en août |
| Oct 2025 | Événementiel Meta (Equita Lyon) | Utilisation de Meta pour promouvoir salon physique, record ventes boutique |
| Nov 2025 | **Mois record** | 551k€ CA, 220k€ marge estimée, ROAS 13-18.6, taux de conversion +20% YoY |
| Déc 2025 | 35% budget sur PRIO 1 atteint | Objectif de répartition budgétaire marge atteint |
| Déc 2025 | Nouvelle enveloppe 2025-26 signée | Contrat d'accompagnement renouvelé |
| Jan 2026 | **Restructuration complète Google Ads** | Passage à 17 campagnes segmentées par marge (PRIO 1-4), ROAS cibles différenciés (600-2200) |
| Jan 2026 | 50% budget sur PRIO 1-2 | Augmentation vs 35% au Q4 2025 |
| Jan 2026 | Suivi avancé conversions Bing | Mise en place du tracking enhanced |
| Jan 2026 | Upgrade reporting Capture | Nouveaux graphiques dans l'outil de dashboard |

---

## 10. Rétrospective Performance 2025 (Synthèse des bilans)

### Vue d'ensemble annuelle

| Mois | Dépenses (€) | CA GA4 (€) | ROAS GA4 | NC ratio | Temps fort |
|---|---|---|---|---|---|
| Jan 2025 | 21 677 | 235 618 | 10,9 | 22,6% | Crise stock, -15% ventes |
| Fév 2025 | 15 439 | 137 362 | 8,9 | 24,8% | Creux saisonnier |
| Mars 2025 | 27 038 | 291 501 | 10,8 | 24,1% | Scaling +40%, DemandGen YouTube |
| Avr 2025 | 28 084 | 306 416 | 10,9 | 23,7% | +59% ventes YoY |
| Mai 2025 | 23 609 | 291 765 | 12,4 | 24,1% | Transition ESC→BHG, Bing |
| Juin 2025 | 26 266 | 306 101 | 11,7 | 25,7% | Record NC ratio, pivot BHG |
| Juil 2025 | 24 121 | 277 555 | 11,5 | — | Creux estival |
| Sept 2025 | 28 503 | 258 991 | 9,1 | — | Réaccélération post-été |
| Oct 2025 | 28 831 | 306 000 | 10,6 | 24,4% | Equita Lyon, scaling Bing |
| Nov 2025 | 26 643 | 551 000 | 13,0-18,6 | 23,4% | **Record absolu**, Black Week |
| Déc 2025 | 21 200 | 376 000 | 10,8 | — | Noel, fin d'année |
| Jan 2026 | 23 600 | 407 000 | 11,7-17,3 | — | Restructuration, 50% PRIO 1-2 |

### Grandes tendances 2025

1. **Pivot stratégique vers les marques propres (BHG)** : fil rouge de l'année. De la simple priorisation en début d'année (22% du budget) à une restructuration complète du compte en janvier 2026 (50% sur PRIO 1-2)
2. **Montée en puissance de Microsoft Ads** : d'un levier marginal à un contributeur significatif avec les meilleurs ratios NC (31-35%) et des ROAS solides (13-23)
3. **Meta Ads en difficulté** : ROAS GA4 très faible toute l'année (<1), fort décalage avec l'attribution régie. Utilisation réorientée vers l'événementiel (Equita Lyon) et le retargeting
4. **Stock comme variable clé** : impacte directement le taux de conversion — crise en jan-fév, amélioration progressive, contribution au record de novembre
5. **Acquisition nouveaux clients** : ratio stable autour de 23-25% sur l'année, porté par le paid qui représente 60-73% des ventes
6. **Panier moyen en baisse structurelle** : de ~85€ à ~80-84€, lié au pivot vers les produits CE (moins chers mais plus margés) — compensé par la marge

### Tonalité et exemples narratifs — Section « Campagnes Payantes »

La sous-section « Campagnes Payantes » du bilan doit être rédigée en **paragraphe narratif fluide** (en complément du tableau de données). Elle couvre 3 axes : le budget (contextualisé vs prévisionnel), les volumes payants (ventes, CA, NC) avec leur part dans le total site, et la rentabilité (ROAS). Voici deux exemples de tonalité pour s'inspirer, **sans les reproduire à l'identique** :

> **Janvier 2026 :** « L'investissement publicitaire total s'élève à 23,6k€, en hausse de +9% par rapport à janvier 2025, conformément au prévisionnel et à la tendance de ces derniers mois. Les leviers payants confirment leur rôle de moteur ultra-central en générant 3 075 ventes (+9% YoY), 257k€ de CA (+8%), et 755 nouveaux clients (+19%), soit dans chacun des cas 63% du volume total du site. Le ratio de NC reste élevé (24,5%) et gagne 2 pts par rapport à l'année dernière. Les leviers payants assurent un renouvellement efficace de la base client tout en maintenant une rentabilité globale très saine (ROAS GA global de 10,9). »

> **Février 2026 :** « L'investissement publicitaire total s'élève à 22,6k€ (+17% YoY). Le budget, revu à la hausse en cours de mois pour viser ~23-24k€, a été quasiment atteint. Les leviers payants génèrent 3 065 ventes (+10% YoY), 245k€ de CA (+6%), et 778 nouveaux clients (+27%), soit respectivement 61%, 60% et 65% du volume total du site. Le ratio NC gagne +2,8 pts YoY à 25,4%. La rentabilité reste très saine (ROAS GA4 global de 10,9, identique à janvier). En MoM, les volumes sont quasi stables pour ~1 000€ de budget en moins, confirmant le gain d'efficience de la nouvelle segmentation. »

---

## 11. Contexte Marché & Environnement Concurrentiel

### Filière équine France (Source : IFCE, Annuaire ÉCUS 2025)

| Indicateur | Valeur | Tendance |
|---|---|---|
| **Population équine France** | 995 700 équidés (2024) | 📉 Baisse — **<1M pour la première fois**, projection <800k en 2037 |
| Répartition | 70% selle/poneys, 16% trait/ânes, 14% courses | — |
| **Cavaliers licenciés FFE** | 648 300 (2024) | 📉 Baisse continue mais reste > pré-Covid |
| Établissements équestres | 9 682 | Stable |
| CA filière équine | 6,2 Mds€ (2023, 26 300 entreprises) | — |
| Dépense moyenne / cavalier | 1 000 à 2 500 €/an | 📈 +8-12% sur 3 ans |
| Marché équitation (croissance) | +2-3%/an prévu 2025-2030 | Tiré par le loisir |

> **Impact sur CE :** Le recul du cheptel est un signal de fond négatif (marché adressable en contraction). La hausse de la dépense/cavalier concerne surtout **l'équipement** (sellerie, vêtements techniques) — un segment où CE est **peu présent**. Sur les compléments, la dynamique est différente : la tendance est au **"clean label" / naturel / fabrication française** plutôt qu'à la montée en prix pure. Cette tendance bénéficie directement aux **marques propres BHG** (CE, Phytology, etc.) mais ne profite **pas aux marques tierces à faible marge** — ce qui renforce la pertinence du pivot stratégique vers les marques propres.

### Marché des compléments alimentaires équins (Europe)

| Indicateur | Valeur | Source |
|---|---|---|
| **Taille marché Europe** | 557 M$ (2024) → 755 M$ (2031) | The Insight Partners |
| **CAGR prévu** | **+4,5%/an** (2025-2031) | — |
| Marché mondial (global) | 3,6 Mds$ (2024) → 6,3 Mds$ (2034) | GM Insights |
| CAGR mondial | +5,6%/an | — |
| Canal online (croissance) | **+7,8%/an** à partir de 2025 | GM Insights |

### Tendances consommateurs clés (2025-2026)

1. **Ingrédients "clean" et ciblés** : formules transparentes, actifs brevetés/validés scientifiquement → avantage pour les marques propres CE
2. **Fabrication française / traçabilité** : critère de confiance majeur → CE bien positionné
3. **Solutions naturelles et véganes** : croissance +9,4%/an des compléments véganes en Europe
4. **Approche holistique** : fusion nutrition + bien-être mental → opportunité de développement
5. **E-commerce spécialisé** : **60%+ des acheteurs préfèrent les sites spécialisés** aux généralistes (Amazon, Decathlon) → avantage structurel pour CE
6. **Adaptation saisonnière** : besoins variant selon les saisons (électrolytes été, immunité hiver) — CE couvre déjà bien ce segment

### Environnement concurrentiel e-commerce équin France

| Acteur | Positionnement | Menace pour CE |
|---|---|---|
| **Distri'Horse33** | Compléments naturels fabriqués en France | Direct (même créneau compléments santé) |
| **Kramer Equitation** | Équipement + nutrition, gros catalogue | Indirect (plus équipement que compléments) |
| **Padd** | Équipement équestre, forte marque | Faible (peu de compléments) |
| **Decathlon / Fouganza** | Entrée de gamme accessible | Faible (généraliste, pas spécialisé santé) |
| **Equi-Clic, Equestra** | E-commerce équitation | Indirect |
| **Vétérinaires / pharmacies online** | Vente directe médicaments + compléments | Croissant (confiance vétérinaire) |
| **Amazon / marketplaces** | Volume, prix agressifs | Modéré (40% achètent sur généralistes) |

> **Avantage compétitif CE :** Double positionnement unique — **fabricant** de marques propres à forte marge + **distributeur** spécialisé de marques tierces. La spécialisation pure santé/bien-être cheval est un différenciateur fort face aux concurrents généralistes.

### Signaux faibles à surveiller

- **Baisse structurelle du cheptel** : moins de chevaux = pression long terme sur le marché adressable
- **Prémiumisation** : compense la baisse en volume par une hausse en valeur
- **Réglementation UE** : restrictions sur antibiotiques dans l'alimentation animale → opportunité pour les compléments naturels
- **IA et personnalisation** : 82% des sites e-commerce investissent dans l'IA en 2025

