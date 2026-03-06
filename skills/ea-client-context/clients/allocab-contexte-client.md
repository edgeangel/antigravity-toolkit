# Allocab — Contexte Client

> **Dernière mise à jour :** Mars 2026
> **Site :** [allocab.com](https://www.allocab.com/)

---

## 1. Identité & Business Model

- **Secteur :** Transport VTC / Taxi
- **Type :** Service de réservation de courses (marketplace)
- **Positionnement :** Plateforme de réservation de VTC/taxi à tarif fixe, couverture nationale France, focus gares et aéroports
- **Particularités :**
  - **Web + App** (iOS & Android) — propriété GA4 unique couvrant les deux
  - **Multi-segments** : B2C (particuliers), SMB Travel (PME/agences), B2B (hôtels, entreprises)
  - **Modèle de revenus** : commission sur chaque course réalisée (pas e-commerce)
  - Promesses clés : tarif fixe, course garantie, planification, couverture nationale
  - Accroche prix historique "dès 9€" (disparue du site lors de la refonte oct 2025, remplacée par min ~15€)

---

## 2. Stratégie Marketing Globale

### Vision données
**La vision GA4 est la vision cible** pour mesurer les performances. Toutes les analyses de performance doivent se baser prioritairement sur les données GA4 (courses bookées, revenue, nouveaux clients).

### Objectif principal
**Maximiser le volume de courses bookées à un CPA fixé (~17€ toutes campagnes confondues)**, en vision GA4.

### Objectif secondaire (presque aussi important)
**Maximiser la part de nouveaux clients** dans le total des courses. Le repeat est la base d'une croissance pérenne et de la marge future. Un ratio NC élevé (>65-70%) témoigne d'une acquisition efficace qui alimente la croissance organique à terme.

### Évolution du pilotage

| Période | Pilotage | Objectif principal | Notes |
|---|---|---|---|
| Avant mars 2025 | **ROAS cible** | Rentabilité "instantanée" | Trop impacté par la course moyenne |
| Mars 2025 → | **CPA cible** (courses bookées) | Volume de courses à CPA fixé | LTV-based, plus adapté à Allocab |
| Jan 2026 → (test) | **Courses done + Marge** | Rentabilité réelle du business | En test — on remonte les données de marge et de courses effectivement réalisées. Pilotage encore majoritairement à la course bookée + volume |

> [!NOTE]
> **Depuis janvier 2026**, les données de **marge** et de **courses done** (effectivement réalisées) sont remontées. Ce sont les objectifs cibles à terme pour un pilotage au plus près de la réalité du business. Mais c'est encore en phase de test : on pilote encore principalement à la **course bookée** et on cherche du **volume**.

### KPIs prioritaires (par ordre d'importance)
1. **Volume de courses bookées** — objectif n°1, on veut du volume (vision GA4)
2. **CPA course bookée** — cible ~17€ toutes campagnes confondues (vision GA4)
3. **Part de nouveaux clients** (% dans le total des courses) — objectif secondaire quasi prioritaire, proxy de croissance pérenne
4. **Volume de nouveaux clients** — croissance de la base
5. **Course moyenne** (€) — proxy d'attractivité et de mix trajets
6. **Courses réalisées (done)** — indicateur de qualité opérationnelle (taux de réalisation ~76-85%). Métrique cible à terme.
7. **Marge** — indicateur business ultime. En cours de remontée depuis jan 2026.
8. **ROAS** — suivi complémentaire (piloté par le CPA, pas l'inverse)

### CPA cibles (évolution)
| Période | CPA cible | Périmètre | Source |
|---|---|---|---|
| Jan-Fév 2025 | ~37€ NC | Nouveau client uniquement | LTV historique 12 mois |
| Mar-Mai 2025 | ~23-25€ NC | Nouveau client uniquement | Objectif de réduction |
| Juin-Déc 2025 | ~20-25€ NC | Nouveau client uniquement | Résultats mois d'été |
| Jan 2026+ | **~17-18,5€** | **Toutes campagnes confondues** | Recalcul post-MEP (voir ci-dessous) |

> [!IMPORTANT]
> **MEP du 15 janvier 2026 — Résultats de l'analyse d'impact** :
>
> La MEP a modifié le tracking e-commerce de sorte que certains achats remontent désormais avec 2 items au lieu de 1. Contrairement à l'hypothèse initiale, **le ratio items/purchase n'a pas doublé** :
>
> | Indicateur | Pré-MEP (1 déc → 14 jan) | Post-MEP (15 jan → 2 mar) | Variation |
> |---|---|---|---|
> | Ratio items / purchase | **0.927** | **1.007** | **+8.6%** |
> | Jours avec items > purchases | 0 / 45 jours | 26 / 47 jours (55%) | — |
> | Revenu moyen / transaction | 44,62€ | 50,21€ | **+12.5%** |
>
> **Facteur d'ajustement** : 1.007 ÷ 0.927 = **×1.086**
> **CPA cible ajusté** : 17€ × 1.086 = **~18,5€** (conservateur — le revenu par transaction justifierait ~19€)
>
> Le CPA cible opérationnel reste fixé autour de **~17€** pour garder de la marge de sécurité, mais les résultats jusqu'à ~18,5€ restent dans la zone acceptable.

---

## 3. Leviers Actifs & Structure de Campagnes

### Google Ads — Structure détaillée

La structure repose sur une segmentation par **type de campagne** (conquête vs marque vs app) et par **géographie/requête**.

#### Campagnes de conquête (Search + PMax) — ~99% des dépenses

| Campagne | Type | Focus | CPA cible | Notes |
|---|---|---|---|---|
| EA - Performance - PMax - tCPA - FR | PMax | Acquisition générique FR | CPA cible | Campagne majeure (~50% des dépenses), flux dynamique |
| EA - Performance - Search - Taxi - Top villes - tCPA - FR | Search | Lyon, Rennes, Bordeaux, Marseille, Nantes, Montpellier, Toulouse, Lille | CPA cible | Groupes d'annonces par ville |
| EA - Performance - Search - Taxi Paris/IdF - tCPA - FR | Search | Paris et Île-de-France (Aéroport, Gares, Top villes IDF) | CPA cible | — |
| EA - Performance - Search - Taxi Paris/IdF - tCPA - EN | Search | Paris/IDF version anglophone | CPA cible | Touristes internationaux |
| EA - Performance - Search - Taxi - France/Top villes - tCPA - EN | Search | Top villes version anglophone | CPA cible | — |
| EA - Performance - Search - Taxi - Générique - tCPA - FR | Search | Requêtes taxi génériques | CPA cible | — |
| EA - Performance - Search - VTC - Générique - tCPA - FR | Search | Requêtes VTC génériques | CPA cible | — |
| EA - Performance - Search - Concurrents - Uber - Générique - tCPA - FR | Search | Requêtes concurrents (Uber) | CPA cible | — |
| EA - Performance - Search - Concurrents - tCPA - FR | Search | Autres concurrents | CPA cible | — |

#### Campagne marque

| Campagne | Type | Focus | Stratégie | Notes |
|---|---|---|---|---|
| EA - Brand - Search - ROAS - Marque Allocab | Search | Requête "Allocab" | ROAS cible | ~1% des dépenses, CPA NC ~3-5€, proxy de notoriété |

**Effet notoriété** : La campagne de marque capte de la demande générée par les campagnes de conquête. Dans ~30% des cas, la conversion finale sur la marque est issue d'un premier contact via une campagne de conquête (données chemins de conversion Google Ads, nov 2025). Le ratio NC sur la marque (20-28%) est lui aussi un indicateur de l'impact des campagnes de conquête.

#### Campagnes App

| Campagne | Type | Focus | Lancement | Notes |
|---|---|---|---|---|
| EA - Performance - Achats - App - iOS - tCPA - FR | App | Achats in-app iOS | Oct 2025 | CPA ~15€, objectif achats (+ téléchargements secondaires) |
| EA - Performance - Achats - App - Android - tCPA - FR | App | Achats in-app Android | Oct 2025 | CPA ~15€, objectif achats (+ téléchargements secondaires) |

> [!IMPORTANT]
> **L'App est un axe de croissance stratégique majeur** :
> - Croissance des achats in-app (B2C/SMB) de +40-84% YoY depuis le lancement des campagnes App
> - Les concurrents (Uber, Bolt) captent l'essentiel de la croissance du marché via leurs apps, ce qui explique en partie la baisse des recherches Google
> - Les campagnes App actuelles ne sont **pas au maximum de leur potentiel** — accélération prévue Q2 2026
> - Être fort sur la partie App est **essentiel pour atteindre des objectifs de croissance soutenue** à moyen terme

#### Campagne DemandGen / YouTube — Élargissement d'audience

| Campagne | Type | Focus | Notes |
|---|---|---|---|
| EA - Croissance - Demand Gen - tCPA - FR | DemandGen / YouTube | Élargissement d'audience, haut de funnel | Levier utilisé pour toucher des audiences au-delà du Search et élargir la diffusion |

> La campagne DemandGen/YouTube tire le ROAS conquête vers le bas mais contribue à élargir la base d'audience touchée et à améliorer les performances globales (effet indirect sur la marque et le trafic direct).

#### Tests et chantiers en cours (2026)

| Chantier | Description | Statut | Horizon |
|---|---|---|---|
| AB Test ROAS Marge | Test de pilotage au ROAS marge plutôt qu'au CPA (lancement 10/02/2026) | En cours | Court terme |
| AB Test AI Max | Élargissement mots-clés/audiences/personnalisation automatique | En cours depuis nov 2025 | Court terme |
| YouTube/DemandGen | Élargissement d'audience via YouTube | Actif | En cours |
| **Accélération App** | Scaling des campagnes App iOS + Android, maximiser le potentiel | **Planifié Q2 2026** | Moyen terme |
| Pilotage courses done / marge | Passage progressif du pilotage à la course bookée vers la course réalisée + marge | En test depuis jan 2026 | Moyen terme |

---

### Microsoft Ads — Structure détaillée

Restructuration complète en mars 2025 (calquée sur la structure Google Ads). Levier complémentaire à Google avec CPA et rentabilité historiquement meilleurs.

| Campagne | Type | Focus |
|---|---|---|
| EA - Performance - Search - Taxi - Générique - tCPA - FR | Search | Requêtes taxi génériques |
| EA - Performance - Search - Taxi - Top villes - tCPA - FR | Search | Top villes |
| EA - Performance - Search - Taxi Paris/IdF - tCPA - FR | Search | Paris/IDF |
| EA - Performance - Search - Campagne Dynamique DSA - tCPA - FR | DSA | Annonces dynamiques |
| EA - Performance - PMax - tCPA - FR | PMax | Performance Max |

> [!NOTE]
> **Tracking courses/NC** : le tracking des courses réalisées et des nouveaux clients sur Microsoft Ads n'a été pleinement opérationnel qu'à partir de **septembre 2025**. Avant cette date, le pilotage se faisait principalement via les sign-ups régie et les purchases GA4.

---

### Meta Ads — En pause

Les campagnes Meta ont été **mises en veille en novembre 2024** (campagne B2C) et **octobre 2024** (campagne B2B Hôtels) après des résultats insuffisants :
- Campagne New Client B2C : faible ratio de NC (27%), convertissait surtout sur des clients existants
- Campagne SMB Travel : 30 NC pour un CPA de 49€, résultats modestes
- Campagne Lead B2B Hôtels : 25 leads pour un CPL de 32€, impossible de qualifier les leads

> Réactivation possible conditionnée à la mise à jour des assets visuels par Allocab et à la création d'une campagne DemandGen/YouTube sur Google Ads.

---

## 4. Budgets & Objectifs

### Budget mensuel (évolution observée)

| Période | Google Ads | Microsoft Ads | Total SEA | Notes |
|---|---|---|---|---|
| Jan 2025 | 26k€ | 0,9k€ | ~27k€ | Réduction post-Q4 2024 |
| Fév 2025 | 28,5k€ | 0,8k€ | ~29k€ | Scaling progressif |
| Mars 2025 | 33,5k€ | 0,9k€ | ~34k€ | Passage CPA cible |
| Avr 2025 | 30k€ | — | ~30k€ | Ralentissement (CPA resserré) |
| Mai 2025 | ~30k€ | — | ~30k€ | Avant ajustement prix (27/05) |
| **Juin 2025** | **96,5k€** | **1,3k€** | **~98k€** | **Pic record** (grève taxis + ajustement prix) |
| Juil 2025 | 45k€ | 0,9k€ | ~46k€ | Retour à la normale |
| Août 2025 | 41,5k€ | 0,9k€ | ~42k€ | Creux estival modéré |
| Sept 2025 | 47,5k€ | 1,1k€ | ~49k€ | Scaling Q4 |
| Oct 2025 | 30,5k€ | 1,5k€ | ~32k€ | Incident site 8-13 oct |
| Nov 2025 | 42k€ | 1,8k€ | ~44k€ | Reprise post-incident |
| Déc 2025 | 55k€ | 0,9k€ | ~56k€ | 2ème meilleur mois |
| Jan 2026 | 54k€ | 2,5k€ | ~57k€ | Scaling Bing massif |

> **Objectif budgétaire 2026** : Target de dépenses mensuelles de **~56k€/mois** (Google Ads + Microsoft Ads). Ce montant correspond au palier atteint en décembre 2025 et janvier 2026, qui combine volume et rentabilité satisfaisants.

---

## 5. Calendrier Promotionnel & Saisonnalité

### Saisonnalité observée (basée sur les bilans 2025)

| Période | Dynamique | Impact volume | Notes |
|---|---|---|---|
| **Janvier-Février** | Période creuse | Modéré | Réduction des investissements, CPA NC plus élevés |
| **Mars-Avril** | Reprise saisonnière | En hausse | Retour de la demande, saisonnalité printemps |
| **Mai-Juin** | **Pic annuel** | **Record** | Juin = mois le plus actif. Grève taxis + ajustement prix en 2025 |
| **Juillet-Août** | Haute saison maintenue | Élevé | Saisonnalité estivale (voyages, aéroports) |
| **Septembre** | Réaccélération rentrée | Élevé | Retour des déplacements pro + scaling |
| **Octobre-Q4** | Creux saisonnier | En baisse | Q4 = demande historiquement la plus faible |
| **Novembre-Décembre** | Variable | Variable | Dépend du contexte (scaling réussi en déc 2025) |

### Événements impactants

- **Grèves des taxis** : impact massif et immédiat sur les volumes de recherche et les conversions (mai 2025)
- **Épisodes météo** (neige) : impact négatif sur les courses réalisées (jan 2026, taux de réalisation sous la moyenne)
- **Refonte site** (oct 2025) : nouvelle charte graphique, changement des messages marketing
- **Ajustement prix** (27 mai 2025) : amélioration de la compétitivité, multiplication des volumes quotidiens par 3-4

### Contexte marché — Intelligence sectorielle

#### Paradoxe central : marché en croissance, recherches en baisse

Il est essentiel de distinguer deux réalités qui coexistent :

**Le marché VTC/taxi en France est en croissance** :
- **CA total taxis + VTC** : ~6,4 Mds€ en 2024 (source Xerfi)
- **CA VTC** : >2 Mds€ en 2024 (+60% depuis 2019)
- **Courses VTC** : >100 millions en 2024, soit **+16% vs 2023** (source ARPE)
- **Chauffeurs VTC actifs** : ~78 000 début 2025 (+9% vs 2023)
- **Prévisions marché ride-hailing France** : ~2,6 Mds$ en 2025, CAGR +9% jusqu'à 2031 (source Mordor Intelligence)

**Mais les recherches Google sur les mots-clés taxi/VTC sont en décroissance structurelle** :
- **YoY 2025 vs 2024** : -8% à -20% en volume de recherche global
- **Top requêtes** ("taxi Paris", "taxi Marseille", etc.) : -20% à -30% YoY
- Décroissance continue depuis 2023
- **Source** : données Google Ads sur un panel de 1000+ mots-clés représentatifs

> [!WARNING]
> **Implication pour Allocab** : Le marché grossit mais les recherches Google rétrécissent. Cela signifie que la croissance du marché est tirée par les **apps et le trafic direct** (Uber, Bolt) plutôt que par la recherche Google. Pour Allocab, qui dépend fortement du Search (~61% du CA via Google Ads), la pression sur les volumes de recherche est un enjeu structurel : il faut capter une **part croissante d'un gâteau de recherche qui rétrécit**, tout en diversifiant vers l'App et d'autres canaux.

#### Paysage concurrentiel

| Acteur | Part de marché VTC France | Positionnement |
|---|---|---|
| **Uber** | 70-80% | Leader dominant, offre diversifiée (UberX, Comfort, XL, Green) |
| **Bolt** | ~20% | Challenger principal, tarifs agressifs, commissions chauffeurs plus basses |
| **Heetch** | ~5-10% | Acteur français, forte présence banlieue et nuit |
| **Allocab** | Niche | Tarif fixe, planification, couverture nationale, multi-segments |
| Autres | <5% | Free Now, Le Cab, indépendants, coopératives émergentes |

**Concurrence sur le Search** :
- Uber domine les requêtes (campagnes Search massives + notoriété organique)
- **taxi-reza** apparaît de plus en plus sur la marque Allocab
- La concurrence Uber est directement ciblée via des campagnes "Concurrents - Uber - Générique"

#### Dynamiques structurelles du secteur

1. **Concentration Île-de-France** : 81% des courses VTC se font en IDF → justifie les campagnes Paris/IDF dédiées
2. **Crise du secteur taxi traditionnel** : ~200 entreprises de taxi fermées fin 2024. Causes : télétravail, restrictions budgétaires entreprises, réduction des courses médicales par l'Assurance maladie en 2025
3. **Revenus chauffeurs en baisse** : revenu horaire brut ajusté en recul chez Uber (-5%), Bolt (-10%), Heetch (-19%) entre 2021 et 2024 (source ARPE) → pression sur l'offre de chauffeurs
4. **Électrification des flottes** : objectif 60% de VTC électriques/hybrides d'ici 2030, subventions EV et zones Crit'Air accélèrent la transition
5. **Migration vers les apps** : les grands acteurs (Uber, Bolt) captent la croissance via leurs apps natives, réduisant mécaniquement la part du Search dans le parcours de réservation

#### Risque réglementaire — Directive Travailleurs de Plateforme

> [!CAUTION]
> **Directive UE 2024/2831** : transposition obligatoire avant le **2 décembre 2026**. Instaure une présomption de salariat pour les travailleurs de plateformes. Pourrait impacter les coûts main-d'œuvre de +20-30% pour les plateformes et potentiellement augmenter les tarifs. Uber France fait déjà face à un redressement URSSAF de 1,7 Md€. Si les grands acteurs augmentent leurs prix, cela pourrait **bénéficier à Allocab** en modèle tarif fixe.

#### Implications stratégiques pour les bilans

Dans les bilans, toujours contextualiser :
1. **Volume de recherche ≠ taille du marché** : le marché grandit mais le Search rétrécit → la croissance d'Allocab sur le Search est d'autant plus notable
2. **Grèves de taxis** : créent des pics de demande ponctuels mais mesurables (mai 2025 : volumes x3-4)
3. **Saisonnalité** : été = pic, Q4 = creux, mais janvier peut être fort (déplacements pro)
4. **Comparaisons YoY** : toujours rappeler le scaling massif des investissements (x2 à x6 vs 2024) pour contextualiser les hausses de volumes

---

## 6. Données & Tracking

### Sources de données

| Source | Identifiant | Contenu | Notes |
|---|---|---|---|
| **BigQuery** | `ia-initiatives.performance_acquisition_control.view_client_allocab` | Données journalières : régie (coût, impressions, clics, conversions, revenue) ET GA4 (conversions, revenue, nouveaux clients) | Table unique avec 2 types de lignes (voir ci-dessous) |
| **GA4** | Propriété `152840252` | "[01] - Allocab Passenger - Web + App" | Fuseau Europe/Paris, devise EUR. Utiliser via l'API GA4 MCP pour des dimensions custom non disponibles en BigQuery (ride_type, departure_department, pro_perso, etc.) |

### Structure BigQuery — Double jeu de lignes

> [!IMPORTANT]
> La table `view_client_allocab` contient **deux types de lignes qui ne se mélangent jamais** :

| Type de ligne | `platform` | Coût | Conversions régie | Conversions GA4 | NC GA4 |
|---|---|---|---|---|---|
| **Lignes régie** | `google_ads`, `bing_ads` | ✅ renseigné | ✅ renseigné | ❌ 0 | ❌ 0 |
| **Lignes GA4** | `google`, `bing`, `(direct)`, `google-play`, etc. | ❌ null | ❌ 0 | ✅ renseigné | ✅ renseigné |

**Colonnes disponibles** :
- `date`, `platform`, `campaign_name`, `link_environnement` (Web, App iOS, App Android, other)
- `campaign_name` : résolu par fallback `COALESCE(link_campaign_name, pt_campaign_name, analytics_campaign_name)` — peut expliquer des noms différents entre régie et GA4
- `cost`, `impressions`, `clicks` — **lignes régie uniquement**
- `conversions_regie`, `revenue_regie` — **lignes régie uniquement** (détail par plateforme ci-dessous)
- `conversions_ga4` — event `purchase` filtré sur `analytics_account_type IN ('b2c', 'smb', 'other_b2b')` — **lignes GA4 uniquement**
- `revenue_ga4` — revenue des mêmes events purchase B2C/SMB/other_b2b — **lignes GA4 uniquement**
- `new_customer_ga4` — event **`first_open`** (première ouverture de l'app = nouveau client VTC) — **lignes GA4 uniquement**
- `new_customer_regie` — toujours à 0 (pas de signal régie nouveau client)

**Détail des conversions régie par plateforme** :
- **Meta** : `omni_purchase` (`pt_conversion`)
- **Google Ads** : `Purchase B2C|SMB - Pixel GAds - EA` via REGEXP (`pt_conversion_all`, exclut "New client") + `iOS purchase` + `Android purchase`
- **Bing Ads** : `(not set)` uniquement depuis le `2025-11-01` (`pt_conversion_all`)

**Comment requêter :**
- **Pour les KPIs régie** (coût, CPA, ROAS régie) : filtrer `WHERE platform IN ('google_ads', 'bing_ads')`
- **Pour les KPIs GA4** (courses bookées, NC, revenue GA4) : filtrer `WHERE platform NOT IN ('google_ads', 'bing_ads')` ou `WHERE conversions_ga4 > 0`
- **Pour croiser** (CPA NC = coût régie / NC GA4) : agréger séparément puis diviser
- **Pour segmenter par campagne GA4** : la colonne `campaign_name` sur les lignes GA4 contient le nom de campagne GA4 (ex: "EA - Performance - PMax - tCPA - FR", "(direct)", "(organic)")

---

## 7. Problématiques Spécifiques

### Problématiques structurelles
- **Recherches Google en décroissance** : -20/30% de volume de recherche YoY sur les requêtes taxi/VTC (malgré un marché VTC en croissance en volume de courses) — pression continue sur la diffusion Search
- **Migration des parcours vers les apps** : les grands acteurs (Uber, Bolt) captent la croissance via leurs apps, réduisant le pool de recherche Google — d'où l'importance des campagnes App pour Allocab
- **Baisse de la course moyenne** : de ~55€ début 2025 à ~44-47€ fin 2025 (~-8€ YoY), liée à l'acquisition de nouveaux clients sur des courses plus courtes
- **Dépendance au paid** : Google Ads représente ~61% du CA (vs 50% en 2024), le paid au global ~70%+
- **Taux de courses réalisées** : ~76-85% des courses bookées sont effectivement réalisées. Variable selon météo et contexte (épisode neigeux etc.)
- **Concurrence croissante** : Uber domine (70-80% du marché VTC France), Bolt et Heetch en croissance, taxi-reza apparaît sur la marque Allocab

### Incidents et problèmes de tracking (2025)
- **Avr-Mai 2025** : Perte de tracking (remontée conversions sous-estimée de ~20% pendant 1 mois)
- **Oct 2025** : Incident site (8-13 oct) ayant bloqué les conversions "Nouveaux Clients" → CPA explosé >70€, ralentissement algorithmique → impact sur tout octobre
- **Nov 2025** : MEP site a modifié le séquençage dataLayer (GTM après footer, déclenchement Didomi incorrect) → perte de données GA4 sur les 10-12 premiers jours
- **Août 2025** : Bug tracking Bing (résolu en septembre)

### Points de vigilance récurrents
- La **campagne PMax** (~50% des dépenses) montre parfois des instabilités de diffusion inexpliquées
- Les **comparaisons YoY** sont biaisées par le très fort scaling (dépenses x2 à x6 vs 2024) — toujours contextualiser
- Le **tracking NC sur Microsoft Ads** n'est pleinement opérationnel que depuis septembre 2025

---

## 8. Historique des Décisions Stratégiques

| Date | Décision | Détails |
|---|---|---|
| Jan 2025 | Création campagnes Top Villes FR + Paris IDF | 8 groupes d'annonces par ville + Paris/Aéroport/Gares/IDF |
| Jan 2025 | Réorganisation campagnes App | Retour objectif téléchargements, réduction budget App |
| Jan-Fév 2025 | Présentation stratégie ROAS → CPA NC | Slide dédiée dans les bilans, calcul LTV en cours |
| Mars 2025 | **Passage au CPA cible** | AB test puis bascule complète au CPA cible sur toute la conquête (25/03) |
| Mars 2025 | Restructuration complète Microsoft Ads | Nouvelles campagnes, structure calquée sur Google, focus conquête |
| Avr 2025 | Premier mois complet CPA cible | CPA NC se rapproche de l'objectif (~25€ vs 30€ début d'année) |
| Mai 2025 | Ajustement prix Allocab (27/05) | Compétitivité accrue, volumes multipliés par 3-4 |
| Juin 2025 | **Mois record** (96k€ dépenses) | Grève taxis + prix ajustés = scaling exceptionnel |
| Juil-Août 2025 | Travail préparatoire App tracking | Linking Tools, SKAN/ATT, SDK Adjust, Capture Insight LTV |
| Sept 2025 | Tracking courses Bing opérationnel | Pilotage plus précis + scaling possible |
| Oct 2025 | Lancement campagnes App iOS & Android | Objectif achats in-app, CPA ~15€ |
| Oct 2025 | AB Test AI Max | Élargissement mots-clés/audiences sur 1 campagne search |
| Oct 2025 | **Incident site** (8-13 oct) | Refonte site, perte conversions NC, impact algo |
| Oct 2025 | Capture Insight Attribution - LTV | Suivi des courses done et de la marge |
| Nov 2025 | MEP site + correctifs tracking | Problème séquençage dataLayer, perte données GA4 10-12 premiers jours |
| Nov 2025 | Extension AB Test AI Max | Sur campagnes supplémentaires |
| Nov 2025 | MAJ assets visuels + textuels | Alignement nouvelle charte graphique |
| Déc 2025 | Pivot stratégie ROAS cible marge | Préparation restructuration |
| Déc 2025 | Test enchères Microsoft Ads | Passage CPC optimisé → CPA cible sur certaines campagnes |
| Jan 2026 | MAJ visuels PMax | Nouveaux assets |
| Jan 2026 | **MEP 15/01 : 2 items/event** | Impact sur le tracking e-commerce GA4, recalcul CPA cible |
| Fév 2026 | **AB Test ROAS Marge** | Lancement 10/02, test de pilotage au ROAS marge plutôt qu'au CPA |
| Fév 2026 | Préparation campagne YouTube/DemandGen | En cours |

---

## 9. Rétrospective Performance 2025-2026 (Synthèse des bilans)

### Vue d'ensemble (Google Ads)

| Mois | Dépenses (€) | Courses Bookées | CPA Course | CPA NC (€) | Ratio NC | Course Moy. (€) | ROAS | Temps fort |
|---|---|---|---|---|---|---|---|---|
| Jan 2025 | 26 069 | 1 539 | — | 30,5 | 56% | 51 | 3,0 | Création top villes, scaling vs 2024 |
| Fév 2025 | 28 476 | 1 492 | — | 32 | 60% | 57 | 2,8 | Pivot CPA annoncé |
| Mars 2025 | 33 517 | 1 777 | — | 31 | 61% | 51,5 | 2,6 | Passage CPA cible, restructuration Bing |
| Avr 2025 | 29 773 | 1 534 | — | ~25 (corrigé) | 69% | — | 2,5 | Perte tracking, CPA NC en amélioration |
| Mai 2025 | ~30k | — | — | ~22 (corrigé) | — | — | — | Ajustement prix 27/05, grève taxis |
| **Juin 2025** | **96 478** | **5 573** | — | **23** | **74%** | **44** | **2,5** | **Record — scaling exceptionnel** |
| Juil 2025 | 45 079 | 3 143 | 14,3 | 20,5 | 70% | 47 | 3,0 | Excellents CPA, records battus |
| Août 2025 | 41 496 | 2 705 | 15,3 | 21,9 | 70% | 47 | 3,1 | Creux estival modéré |
| Sept 2025 | 47 539 | 2 908 | 16,3 | 25 | 66% | 45 | 2,8 | Marché -20/30%, scaling +61% YoY |
| Oct 2025 | 30 449 | 1 871 | 16,3 | 22 | 75% | — | 2,8 | Incident site, volumes impactés |
| Nov 2025 | 42 132 | 2 242 | 18,8 | 26 | 71% | — | 2,2 | Tracking perturbé, perte données GA4 |
| Déc 2025 | 55 194 | 3 452 | 16 | 22 | 71% | 45 | — | 2ème meilleur mois, scaling réussi |
| Jan 2026 | 54 026 | 3 381 | 16 | 24 | 67% | 44 | — | Scaling massif vs Y-1 (+113% courses) |

### Vue d'ensemble (Microsoft Ads)

| Mois | Dépenses (€) | Courses Bookées | CPA Course | Nvx Clients | CPA NC | ROAS | Notes |
|---|---|---|---|---|---|---|---|
| Mars 2025 | 936 | 278 | — | — | — | — | Restructuration complète |
| Juin 2025 | 1 312 | 399 | 3,3 | — | — | 15,7 | Pivot conquête (98,5% dép.) |
| Juil 2025 | 865 | 284 | 3 | — | — | 15,6 | CPA/ROAS > Google |
| Août 2025 | 943 | 217 | 4,3 | — | — | 11,1 | — |
| Sept 2025 | 1 097 | 321 | 3,4 | — | — | 15,9 | Tracking courses opérationnel |
| Oct 2025 | 1 497 | 245 | 6 | — | — | 8 | Incident site |
| Nov 2025 | 1 848 | 234 | — | 176 | 10,5 | 5,4 | Scaling +80%, NC tracking ✅ |
| Déc 2025 | 925 | 217 | — | 120 | 8 | — | Sous-diffusion non volontaire |
| Jan 2026 | 2 448 | 280 | 8,7 | 170 | 14 | — | Scaling massif (+164%) |

### Grandes tendances 2025

1. **Pivot CPA réussi** : transition ROAS → CPA cible effectuée sans dégradation majeure, avec amélioration progressive du CPA NC (de 32€ à 20-22€)
2. **Scaling massif** : dépenses Google Ads multipliées par 2 à 6 vs 2024 selon les mois, avec des volumes de courses et de NC qui ont suivi proportionnellement
3. **Microsoft Ads comme levier de conquête premium** : CPA et ROAS systématiquement meilleurs que Google Ads, ratio NC majoritaire (60-75%)
4. **App comme axe de croissance** : +40-84% achats in-app YoY depuis le lancement des campagnes App
5. **Marque en progression** : les campagnes de conquête alimentent mécaniquement la notoriété de marque (+15-25% de NC sur la campagne brand, ratio NC passé de 13% à 25-28%)
6. **Course moyenne en baisse structurelle** : de 55€ à 44-47€, lié à l'acquisition de NC sur des courses plus courtes — compensé par le volume
7. **Résilience malgré la décroissance du Search** : croissance forte des volumes et de la base client malgré -20/30% de recherches Google YoY — dans un marché VTC globalement en croissance (+16% de courses en 2024)
