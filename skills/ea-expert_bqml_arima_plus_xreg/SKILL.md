---
name: ea-expert_bqml_arima_plus_xreg
description: >
  Guide expert ARIMA_PLUS_XREG dans BigQuery ML — contribution média et MMM simplifié.
  Use when user says "BQML", "ARIMA", "contribution média", "forecast", "prévision",
  "time series", "BigQuery ML". Uses MCP: bigquery. For full MMM: ea-meridian-mmm.
---

# SKILL.md : Expertise Modélisation ARIMA_PLUS_XREG (BigQuery ML)

> [!IMPORTANT]
> **Documentation BigQuery ML à jour** : Utiliser le MCP `google-developer-knowledge` pour la doc officielle :
> ```
> search_documents("BigQuery ML ARIMA_PLUS_XREG time series forecasting external regressors")
> search_documents("ML.EXPLAIN_FORECAST BigQuery decomposition")
> search_documents("ML.ARIMA_COEFFICIENTS weights external regressors")
> ```

> [!TIP]
> **Alternative TimesFM** : BigQuery ML propose désormais un modèle **TimesFM** (foundation model) avec la fonction `AI.FORECAST` (Preview).
> TimesFM est un modèle pré-entraîné qui ne nécessite pas de créer/gérer son propre modèle.
> **Pour l'analyse de contribution média**, ARIMA_PLUS_XREG reste supérieur car il fournit les poids des régresseurs (ML.ARIMA_COEFFICIENTS) et la décomposition (ML.EXPLAIN_FORECAST).

## 1. Méta-données de la Compétence

- **Nom** : `expert_bqml_arima_plus_xreg`
- **Domaine** : Machine Learning, Séries Temporelles, Prévision Multivariée, Analyse de Contribution Média.
- **Description** : Capacité à concevoir, entraîner, évaluer, expliquer et valider des modèles de prévision de séries temporelles multivariées utilisant ARIMA_PLUS_XREG dans BigQuery ML. Focus particulier sur l'application marketing : mesure de la contribution des canaux média aux conversions/ventes.
- **Niveau d'expertise** : Avancé / Architecte de données.
- **Contexte EdgeAngel** : Ce modèle est la **Méthode 2** de notre framework de mesure publicitaire (après Causal Impact, avant Meridian). Il sert à produire une analyse de contribution média continue et industrialisable, directement dans BigQuery.

---

## 2. Définition et Architecture Technique

### Qu'est-ce que ARIMA_PLUS_XREG ?

`ARIMA_PLUS_XREG` est un modèle de prévision de séries temporelles multivariées intégré à BigQuery ML. Contrairement au modèle univarié `ARIMA_PLUS` qui ne se base que sur l'historique de la valeur cible, `ARIMA_PLUS_XREG` permet d'intégrer des **régresseurs externes** (variables exogènes) pour affiner la prévision.

### ⚠️ Ce que ce modèle EST et ce qu'il N'EST PAS

| Ce que c'est | Ce que ce n'est PAS |
|---|---|
| Un modèle de séries temporelles avec régresseurs linéaires | Un Marketing Mix Model bayésien (comme Meridian, Robyn, PyMC-Marketing) |
| Capable d'isoler la contribution relative de variables externes | Capable de modéliser la saturation (rendements décroissants) nativement |
| Utile pour un diagnostic/monitoring de contribution média | Un outil d'optimisation budgétaire avec intervalles de crédibilité |
| Industrialisable en SQL pur dans BigQuery | Un modèle causal au sens strict (corrélation ≠ causalité) |

**Règle de communication client** : Toujours présenter les résultats comme une "analyse de contribution" ou un "diagnostic média", jamais comme un "MMM" au sens académique du terme. Le vrai MMM viendra avec Meridian (Phase 3).

### Pipeline de Modélisation

Le modèle exécute un pipeline de prétraitement et de décomposition en 5 étapes :

1. **Prétraitement automatique** :
   - Inférence de la fréquence des données (quotidienne, hebdomadaire, etc.).
   - Gestion des intervalles irréguliers et des timestamps dupliqués (moyenne).
   - Interpolation des données manquantes (interpolation linéaire locale).
   - Détection et nettoyage des pics et creux (outliers) aberrants.
   - Ajustement des changements de niveau brutaux (step changes).
2. **Effets Calendaires** : Détection et ajustement des effets liés aux jours fériés. *Efficace uniquement si la série couvre au moins un cycle annuel complet.*
3. **Décomposition STL** : *Seasonal and Trend decomposition using Loess* pour isoler les motifs saisonniers multiples.
4. **Régression Linéaire (Composante XREG)** : Estimation de l'impact des variables externes via régression Ridge (L2 régularisable). C'est cette composante qui nous intéresse pour l'analyse de contribution.
5. **Modélisation de la Tendance (ARIMA)** : La tendance résiduelle est modélisée via `auto.ARIMA` en minimisant l'AIC.

**Implication clé** : Le modèle sépare automatiquement la baseline organique (tendance + saisonalité + jours fériés) de l'effet des régresseurs (média, prix, etc.). C'est cette séparation qui permet l'analyse de contribution.

---

## 3. Syntaxe SQL et Configuration (`CREATE MODEL`)

### Syntaxe de base

```sql
CREATE OR REPLACE MODEL `project.dataset.model_name`
OPTIONS(
  MODEL_TYPE = 'ARIMA_PLUS_XREG',
  TIME_SERIES_TIMESTAMP_COL = 'date_column',
  TIME_SERIES_DATA_COL = 'target_metric',
  TIME_SERIES_ID_COL = 'id_column',
  AUTO_ARIMA = TRUE,
  DATA_FREQUENCY = 'AUTO_FREQUENCY',
  HOLIDAY_REGION = 'FR'
  -- NOTE : DECOMPOSE_TIME_SERIES n'est PAS supporté pour ARIMA_PLUS_XREG
  -- L'explicabilité se fait via ML.EXPLAIN_FORECAST directement
) AS
SELECT
  date_column,
  target_metric,
  feature_1,
  feature_2,
  id_column
FROM `project.dataset.training_data`;
```

### Options Critiques à Maîtriser

| Option | Valeur recommandée | Notes |
|---|---|---|
| `AUTO_ARIMA` | `TRUE` | Laisser BigQuery optimiser les hyperparamètres (p,d,q). Passer à `FALSE` uniquement si on veut forcer un modèle spécifique. |
| `HOLIDAY_REGION` | `'FR'` | Adapter au pays du client. Accepte un array pour multi-pays : `['FR', 'BE']`. |
| `DECOMPOSE_TIME_SERIES` | `TRUE` | ⚠️ **Non supporté pour ARIMA_PLUS_XREG** (uniquement pour ARIMA_PLUS). ML.EXPLAIN_FORECAST fonctionne sans cette option pour les modèles XREG. |
| `L2_REG` | Voir ci-dessous | Régularisation Ridge sur les régresseurs. **La valeur dépend de l'objectif** — voir le guide détaillé ci-dessous. |

**Guide L2_REG pour l'analyse de contribution média** :

| Objectif | L2_REG recommandé | Pourquoi |
|---|---|---|
| Prévision (forecast) | `0.1` à `1.0` | Faible régularisation, priorité au fit |
| Attribution/décomposition (stacked area) | **`5` à `20`** (sweet spot : `10`) | Force les poids à baisser → attributions réalistes, baseline positive |
| Exploration / multicolinéarité forte | `50` à `100` | Forte régularisation, poids très faibles |

> **Apprentissage clé (Pigier/MBway, fév. 2026)** : Sans L2 ou avec L2 faible, les attributions (poids × feature) dépassent souvent le total de conversions réelles quand le média est always-on. Le trend ARIMA compense en devenant très négatif → baseline négative (absurde). Avec L2=10, les attributions restent dans les bornes du model fit et la baseline reste positive. Le fit se dégrade légèrement mais la décomposition devient exploitable pour un stacked area chart.
| `AUTO_ARIMA_MAX_ORDER` | `5` (défaut) | Réduire à `3` pour accélérer l'entraînement sur de gros volumes. Impact marginal sur la précision. |
| `HORIZON` | Adapter | Spécifier l'horizon ici optimise les performances de `ML.FORECAST`. Ex : `30` pour prévision mensuelle. |
| `TIME_SERIES_ID_COL` | Optionnel | Pour prévision multi-séries (ex : par magasin, par pays). Jusqu'à 100M de séries simultanées. |

---

## 4. Cycle de Vie et Fonctions Associées

### A. Évaluation (`ML.ARIMA_EVALUATE`)

Retourne les métriques de précision pour tous les modèles candidats testés lors de l'auto-ARIMA.

```sql
SELECT *
FROM ML.ARIMA_EVALUATE(MODEL `project.dataset.model_name`)
ORDER BY AIC ASC  -- Le meilleur modèle est celui avec l'AIC le plus bas
```

**Métriques clés** : AIC, log-likelihood, variance. Le premier résultat (AIC le plus bas) est le modèle sélectionné automatiquement.

**Astuce validation** : Comparer les métriques du modèle XREG avec un modèle ARIMA_PLUS simple (sans régresseurs). Si XREG n'améliore pas significativement l'AIC, les régresseurs n'apportent pas de valeur prédictive → remettre en question la qualité des données média ou le choix des variables.

### B. Inspection des Coefficients (`ML.ARIMA_COEFFICIENTS`)

**Fonction la plus importante pour l'analyse de contribution média.**

```sql
SELECT *
FROM ML.ARIMA_COEFFICIENTS(MODEL `project.dataset.model_name`)
```

Retourne :
- **`processed_input`** : Nom de la variable (régresseur).
- **`weight`** : Poids numérique de chaque régresseur (pour variables numériques).
- **`category_weights`** : Poids par catégorie (pour variables catégorielles).
- Les coefficients ARIMA (`ar_coefficients`, `ma_coefficients`, `intercept_or_drift`).

**Interprétation des poids en contexte marketing** :
- Les poids sont calculés après standardisation → **ils sont comparables entre eux** pour évaluer l'importance relative de chaque canal.
- Un poids de 0.25 sur `adstock_social` et 0.10 sur `adstock_display` signifie que le Social Ads a ~2.5x plus d'influence que le Display sur les conversions, toutes choses égales par ailleurs.
- **Les poids sont linéaires** : le modèle suppose que doubler le spend double l'effet. C'est une approximation (voir section 6.2 sur la transformation log pour mitiger).

### C. Prévision (`ML.FORECAST`)

Génère les valeurs futures. **Contrainte XREG** : il faut fournir les valeurs futures des régresseurs.

```sql
SELECT *
FROM ML.FORECAST(
  MODEL `project.dataset.model_name`,
  STRUCT(30 AS horizon, 0.90 AS confidence_level),
  (SELECT date, spend_sea, spend_social FROM `dataset.future_media_plan`)
)
```

En contexte marketing, les régresseurs futurs sont souvent **contrôlables** (budgets planifiés) → c'est un use case idéal pour le "what-if analysis" : "Que se passe-t-il si je double le budget Social Ads le mois prochain ?"

### D. Explicabilité (`ML.EXPLAIN_FORECAST`)

**Fonction la plus puissante pour le reporting client.** Décompose chaque prévision en ses composants additifs :

```sql
SELECT
  forecast_timestamp,
  forecast_value,
  trend,
  seasonal_period_yearly,
  seasonal_period_weekly,
  holiday_effect,
  step_changes,
  attribution_adstock_sea_brand,
  attribution_adstock_social,
  attribution_adstock_display,
  attribution_adstock_youtube,
  residual
FROM ML.EXPLAIN_FORECAST(
  MODEL `project.dataset.model_name`,
  STRUCT(30 AS horizon, 0.90 AS confidence_level),
  (SELECT * FROM `dataset.future_media_plan`)
)
```

**Structure de la décomposition** :

```
Valeur Prédite = Tendance
               + Saisonnalité (annuelle + hebdomadaire + ...)
               + Effet Jours Fériés
               + Attribution_Canal_1
               + Attribution_Canal_2
               + ...
               + Attribution_Canal_N
               + Résiduel (bruit)
```

**Comment transformer en insight client** :
1. Calculer `baseline = tendance + saisonnalité + jours_fériés`
2. Calculer `contribution_media = SUM(attribution_canal_1 ... N)`
3. Pourcentage de contribution par canal = `attribution_canal_X / (baseline + contribution_media)`
4. Présenter sous forme de stacked bar chart dans Looker Studio

### E. Détection d'Anomalies (`ML.DETECT_ANOMALIES`)

Identifie les points aberrants en comparant la valeur réelle à l'intervalle de prédiction.

```sql
SELECT *
FROM ML.DETECT_ANOMALIES(
  MODEL `project.dataset.model_name`,
  STRUCT(0.95 AS anomaly_prob_threshold),
  (SELECT * FROM `dataset.recent_data` WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
)
```

**Use case marketing** : détecter des chutes ou pics inexpliqués de conversions. Si le modèle flag une anomalie et qu'aucun régresseur ne l'explique, investiguer des facteurs externes (panne site, action concurrentielle, événement saisonnier non modélisé).

---

## 5. Limitations Techniques & Pièges

### 5.1 Dilemme des Régresseurs Futurs

Le piège classique : utiliser des features dont on ne connaît pas le futur (météo à J+30, actions concurrents).

**Solutions** :
- Si les régresseurs sont contrôlables (budgets média, promotions planifiées) → pas de problème, c'est du scenario planning.
- Si les régresseurs ne sont pas connus → les prévoir d'abord avec un ARIMA_PLUS simple, puis injecter dans le XREG (architecture en cascade).
- Si les régresseurs sont purement exploratoires (analyser le passé, pas prévoir) → `ML.ARIMA_COEFFICIENTS` et `ML.EXPLAIN_FORECAST` sur l'historique suffisent, pas besoin de forecast.

### 5.2 Limites de Données

| Contrainte | Valeur |
|---|---|
| Minimum de points par série | 3 |
| Maximum de points (input) | 1 000 000 par série |
| Maximum de points (forecast) | 10 000 |
| Cardinalité max features catégorielles | 10 000 valeurs distinctes |
| Données recommandées pour bon résultat | **1 an minimum, 2 ans idéal** (pour capturer la saisonnalité) |

### 5.3 Imputation des NULLs dans les Features

BigQuery ML impute automatiquement les NULLs par la **moyenne globale** de la colonne.

**Risque critique** : en contexte multi-séries (plusieurs magasins/pays), la moyenne globale d'une feature "spend_social" mélange des marchés très différents.

**Best practice** : toujours imputer soi-même avant le `CREATE MODEL` :

```sql
-- Imputation par 0 pour les dépenses média (pas de dépense = 0, pas NULL)
COALESCE(spend_social, 0) AS spend_social,
-- Imputation par carry-forward pour les prix
LAST_VALUE(price IGNORE NULLS) OVER (ORDER BY date) AS price
```

### 5.4 Performance & Coûts

- Les modèles ARIMA sont compute-intensive. Le nombre de modèles candidats testés = `AUTO_ARIMA_MAX_ORDER`, et le coût est multiplié par ce nombre.
- Pour de gros volumes : utiliser `TIME_SERIES_LENGTH_FRACTION` pour n'entraîner la tendance que sur la queue de la série (ex : derniers 50%).
- **Le modèle NE PEUT PAS être exporté** hors BigQuery. Tout le cycle de vie reste en SQL.

---

## 6. Application Marketing : Analyse de Contribution Média

### 6.1 Prérequis : la transformation Adstock

**ARIMA_PLUS_XREG ne gère pas l'adstock nativement.** Il faut transformer les données média AVANT de les injecter dans le modèle. L'adstock modélise le fait que l'impact d'une pub ne se limite pas au moment de l'exposition : une partie de l'effet "déborde" sur les périodes suivantes.

#### Formule géométrique (simple, recommandée)

```
Adstock(t) = Spend(t) + λ × Adstock(t-1)
```

Où `λ` (lambda) est le taux de rétention, entre 0 et 1.

#### Valeurs de référence par canal

| Canal | λ suggéré | Half-life | Justification |
|---|---|---|---|
| Search Ads (Brand) | 0.0 – 0.1 | < 1 jour | Intention forte, conversion immédiate |
| Search Ads (Générique) | 0.1 – 0.3 | 1-2 jours | Phase de considération |
| Social Ads (Performance) | 0.3 – 0.5 | 2-5 jours | Exposition passive, effet retardé |
| Display / Programmatique | 0.3 – 0.5 | 2-5 jours | Awareness, faible clic |
| YouTube / Vidéo | 0.5 – 0.8 | 1-3 semaines | Mémorisation forte, branding |
| TV | 0.7 – 0.9 | 2-6 semaines | Branding long terme |

Half-life = ln(0.5) / ln(λ). Exemple : λ=0.5 → half-life ≈ 1 période.

#### Grid Search : trouver le λ optimal par canal (OBLIGATOIRE)

**Ne jamais appliquer un λ "par défaut" sans vérification empirique.** Les valeurs ci-dessus sont des points de départ. L'approche recommandée est de tester une grille de λ et de mesurer la corrélation (Pearson) entre l'adstock transformé et la variable cible (conversions).

**Méthode** : pour chaque λ candidat, calculer l'adstock puis la corrélation avec les conversions. Le λ qui maximise `CORR(conversions, LOG(adstock + 1))` est le meilleur candidat.

```sql
-- ═══════════════════════════════════════════════════════
-- GRID SEARCH λ OPTIMAL — Template réutilisable
-- Adapter : table source, colonne spend, filtre école
-- ═══════════════════════════════════════════════════════
CREATE TEMP FUNCTION adstock_geo(spend ARRAY<FLOAT64>, lambda FLOAT64)
RETURNS ARRAY<FLOAT64>
LANGUAGE js AS r"""
  let result = []; let prev = 0;
  for (let i = 0; i < spend.length; i++) {
    prev = spend[i] + lambda * prev;
    result.push(prev);
  }
  return result;
""";

WITH daily AS (
  SELECT date, conversions, cost_social, cost_google_ads
  FROM `project.dataset.prep_daily_all_ecoles`
  WHERE ecole = 'NOM_ECOLE'  -- ← Adapter
  ORDER BY date
),
arrayed AS (
  SELECT
    ARRAY_AGG(conversions ORDER BY date) AS conv_arr,
    ARRAY_AGG(cost_social ORDER BY date) AS social_arr,
    ARRAY_AGG(cost_google_ads ORDER BY date) AS gads_arr,
    ARRAY_AGG(date ORDER BY date) AS dates
  FROM daily
),
lambdas AS (
  SELECT lambda
  FROM UNNEST([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]) AS lambda
),
grid AS (
  SELECT
    l.lambda,
    adstock_geo(a.social_arr, l.lambda) AS adstocked_social,
    adstock_geo(a.gads_arr, l.lambda) AS adstocked_gads,
    a.conv_arr, a.dates
  FROM arrayed a CROSS JOIN lambdas l
),
unnested AS (
  SELECT
    g.lambda,
    g.conv_arr[OFFSET(i)] AS conversions,
    g.adstocked_social[OFFSET(i)] AS adstock_social,
    g.adstocked_gads[OFFSET(i)] AS adstock_gads
  FROM grid g, UNNEST(GENERATE_ARRAY(0, ARRAY_LENGTH(g.dates) - 1)) AS i
)
SELECT
  lambda,
  ROUND(CORR(conversions, adstock_social), 4) AS corr_social_raw,
  ROUND(CORR(conversions, LOG(adstock_social + 1)), 4) AS corr_social_log,
  ROUND(CORR(conversions, adstock_gads), 4) AS corr_gads_raw,
  ROUND(CORR(conversions, LOG(adstock_gads + 1)), 4) AS corr_gads_log
FROM unnested
GROUP BY lambda
ORDER BY lambda;
```

**Interprétation** :
- Choisir le λ qui maximise `corr_*_log` (corrélation sur échelle log, plus robuste).
- Si la corrélation est plate quel que soit λ (ex : Social Ads ~0.26 partout), le canal a un effet diffus/haut de funnel → garder le λ théorique.
- Si le λ optimal diffère fortement entre écoles pour un même canal, envisager un λ par école.
- Corrélation > 0.5 = bon signal. Entre 0.2-0.5 = signal présent mais bruité. < 0.2 = signal faible.

#### Implémentation SQL dans BigQuery

```sql
-- UDF JavaScript pour le calcul récursif de l'adstock
CREATE TEMP FUNCTION adstock_geo(spend ARRAY<FLOAT64>, lambda FLOAT64)
RETURNS ARRAY<FLOAT64>
LANGUAGE js AS r"""
  let result = [];
  let prev = 0;
  for (let i = 0; i < spend.length; i++) {
    prev = spend[i] + lambda * prev;
    result.push(prev);
  }
  return result;
""";

-- Application de l'adstock à chaque canal
CREATE OR REPLACE TABLE `project.dataset.media_adstocked` AS
WITH ordered AS (
  SELECT
    date,
    conversions,
    revenue,
    spend_sea_brand,
    spend_sea_generic,
    spend_social,
    spend_display,
    spend_youtube
  FROM `project.dataset.daily_media_data`
  ORDER BY date
),
arrayed AS (
  SELECT
    ARRAY_AGG(date ORDER BY date) AS dates,
    ARRAY_AGG(conversions ORDER BY date) AS conversions_arr,
    ARRAY_AGG(revenue ORDER BY date) AS revenue_arr,
    ARRAY_AGG(spend_sea_brand ORDER BY date) AS sea_brand_arr,
    ARRAY_AGG(spend_sea_generic ORDER BY date) AS sea_generic_arr,
    ARRAY_AGG(spend_social ORDER BY date) AS social_arr,
    ARRAY_AGG(spend_display ORDER BY date) AS display_arr,
    ARRAY_AGG(spend_youtube ORDER BY date) AS youtube_arr
  FROM ordered
),
transformed AS (
  SELECT
    dates,
    conversions_arr,
    revenue_arr,
    adstock_geo(sea_brand_arr, 0.1) AS adstock_sea_brand,
    adstock_geo(sea_generic_arr, 0.25) AS adstock_sea_generic,
    adstock_geo(social_arr, 0.4) AS adstock_social,
    adstock_geo(display_arr, 0.4) AS adstock_display,
    adstock_geo(youtube_arr, 0.7) AS adstock_youtube
  FROM arrayed
)
SELECT
  dates[OFFSET(i)] AS date,
  conversions_arr[OFFSET(i)] AS conversions,
  revenue_arr[OFFSET(i)] AS revenue,
  adstock_sea_brand[OFFSET(i)] AS adstock_sea_brand,
  adstock_sea_generic[OFFSET(i)] AS adstock_sea_generic,
  adstock_social[OFFSET(i)] AS adstock_social,
  adstock_display[OFFSET(i)] AS adstock_display,
  adstock_youtube[OFFSET(i)] AS adstock_youtube
FROM transformed, UNNEST(GENERATE_ARRAY(0, ARRAY_LENGTH(dates) - 1)) AS i;
```

### 6.2 Transformation log pour simuler la saturation

ARIMA_PLUS_XREG suppose une relation linéaire entre régresseurs et cible. En réalité, les rendements sont décroissants (doubler le budget ne double pas les conversions). Un hack simple :

```sql
-- Appliquer log(x+1) sur les dépenses adstockées AVANT le modèle
SELECT
  date,
  conversions,
  LOG(adstock_social + 1) AS log_adstock_social,
  LOG(adstock_display + 1) AS log_adstock_display,
  LOG(adstock_youtube + 1) AS log_adstock_youtube,
  -- ⚠️ PAS de LOG pour les canaux intent (Search/GAds)
  adstock_sea_brand AS adstock_sea_brand,
  adstock_sea_generic AS adstock_sea_generic
FROM `project.dataset.media_adstocked`
```

**Pourquoi ça marche** : `log(x)` écrase les grandes valeurs et amplifie les petites. Le coefficient linéaire du modèle s'applique alors sur une échelle log, ce qui produit un effet de rendements décroissants dans l'espace original. Ce n'est pas aussi flexible qu'une vraie fonction de saturation (Hill curve), mais c'est une bonne approximation pour un modèle SQL-only.

#### Quand utiliser LOG vs RAW par type de canal

| Type de canal | Exemples | LOG ? | Raison |
|---|---|---|---|
| **Awareness** (haut de funnel) | Social Ads, Display, YouTube, TV | **✅ OUI** | Rendements décroissants (saturation d'impression) |
| **Intent** (bas de funnel) | Google Ads Search, SEA Brand/Générique | **❌ NON** | Relation quasi-linéaire (+ budget → + clics sur requêtes existantes → + conversions) |

**Pourquoi PAS de LOG sur les canaux intent :**
1. **Relation linéaire** : Search capte l'intention existante. Plus de budget = plus de requêtes couvertes = plus de conversions, sans saturation marquée dans la plage de budget habituelle.
2. **Compression du signal** : si le budget GAds est quasi-constant (CV < 25%, type "always-on"), le LOG compresse encore la variance déjà faible → le modèle ne voit plus le signal.
3. **CPA plus interprétable** : sans LOG, CPA_marginal = `(1-λ) / weight` → directement comparable au CPA GA4 last-click. Avec LOG, CPA_marginal dépend du niveau de spend → moins intuitif.

**Quand ne PAS utiliser log (même pour awareness)** : si les dépenses sont très faibles ou très sporadiques (beaucoup de 0), le log n'ajoute pas de valeur. Dans ce cas, garder les valeurs brutes adstockées.

### 6.3 Workflow complet : de la donnée brute au reporting

```
┌──────────────────────────────────────────────────────────────────┐
│  ÉTAPE 1 : Données brutes dans BigQuery (via Capture)           │
│  - Table daily_media_data : date, conversions, spend par canal  │
│  - Source : connecteurs Capture (GA4, Google Ads, Meta, etc.)   │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  ÉTAPE 2 : Transformation Adstock + Log                         │
│  - Appliquer adstock géométrique par canal (λ par canal)        │
│  - Appliquer log(x+1) sur les dépenses adstockées              │
│  - Résultat : table media_adstocked_log                         │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  ÉTAPE 3 : Entraînement du modèle                               │
│  - CREATE MODEL ARIMA_PLUS_XREG                                 │
│  - Variables : adstock par canal + contrôles (prix, promo)      │
│  - Options : HOLIDAY_REGION='FR', L2_REG=10                    │
│  - NB: Pas de log transform si objectif = décomposition         │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  ÉTAPE 4 : Validation (voir Section 8)                          │
│  - ML.ARIMA_COEFFICIENTS → vérifier signes et stabilité         │
│  - Comparer XREG vs ARIMA_PLUS simple                           │
│  - Sanity checks business                                       │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  ÉTAPE 5 : Reporting                                            │
│  - ML.EXPLAIN_FORECAST → décomposition par composant            │
│  - Calculer % contribution par canal                            │
│  - Visualiser dans Looker Studio (stacked bar chart)            │
└──────────────────────────────────────────────────────────────────┘
```

### 6.4 Template SQL complet pour analyse de contribution média

```sql
-- ═══════════════════════════════════════════════════════
-- ÉTAPE 1 : ADSTOCK + LOG TRANSFORM
-- ═══════════════════════════════════════════════════════

CREATE TEMP FUNCTION adstock_geo(spend ARRAY<FLOAT64>, lambda FLOAT64)
RETURNS ARRAY<FLOAT64>
LANGUAGE js AS r"""
  let result = []; let prev = 0;
  for (let i = 0; i < spend.length; i++) {
    prev = spend[i] + lambda * prev;
    result.push(prev);
  }
  return result;
""";

CREATE OR REPLACE TABLE `project.dataset.media_ready` AS
WITH arrayed AS (
  SELECT
    ARRAY_AGG(date ORDER BY date) AS dates,
    ARRAY_AGG(conversions ORDER BY date) AS conv,
    ARRAY_AGG(COALESCE(spend_sea_brand, 0) ORDER BY date) AS sea_brand,
    ARRAY_AGG(COALESCE(spend_sea_generic, 0) ORDER BY date) AS sea_generic,
    ARRAY_AGG(COALESCE(spend_social, 0) ORDER BY date) AS social,
    ARRAY_AGG(COALESCE(spend_display, 0) ORDER BY date) AS display,
    ARRAY_AGG(COALESCE(spend_youtube, 0) ORDER BY date) AS youtube
  FROM `project.dataset.daily_media_data`
),
transformed AS (
  SELECT dates, conv,
    adstock_geo(sea_brand, 0.1) AS as_sea_brand,
    adstock_geo(sea_generic, 0.25) AS as_sea_generic,
    adstock_geo(social, 0.4) AS as_social,
    adstock_geo(display, 0.4) AS as_display,
    adstock_geo(youtube, 0.7) AS as_youtube
  FROM arrayed
)
SELECT
  dates[OFFSET(i)] AS date,
  conv[OFFSET(i)] AS conversions,
  LOG(as_sea_brand[OFFSET(i)] + 1) AS log_as_sea_brand,
  LOG(as_sea_generic[OFFSET(i)] + 1) AS log_as_sea_generic,
  LOG(as_social[OFFSET(i)] + 1) AS log_as_social,
  LOG(as_display[OFFSET(i)] + 1) AS log_as_display,
  LOG(as_youtube[OFFSET(i)] + 1) AS log_as_youtube
FROM transformed, UNNEST(GENERATE_ARRAY(0, ARRAY_LENGTH(dates) - 1)) AS i;

-- ═══════════════════════════════════════════════════════
-- ÉTAPE 2 : ENTRAÎNEMENT DU MODÈLE
-- ═══════════════════════════════════════════════════════

CREATE OR REPLACE MODEL `project.dataset.media_contribution_v1`
OPTIONS(
  MODEL_TYPE = 'ARIMA_PLUS_XREG',
  TIME_SERIES_TIMESTAMP_COL = 'date',
  TIME_SERIES_DATA_COL = 'conversions',
  AUTO_ARIMA = TRUE,
  DATA_FREQUENCY = 'DAILY',
  HOLIDAY_REGION = 'FR',
  -- NB: DECOMPOSE_TIME_SERIES n'est PAS supporté pour ARIMA_PLUS_XREG
  L2_REG = 10  -- Régularisation Ridge pour attribution exploitable (baseline positive)
) AS
SELECT
  date, conversions,
  log_as_sea_brand,
  log_as_sea_generic,
  log_as_social,
  log_as_display,
  log_as_youtube
FROM `project.dataset.media_ready`
WHERE date BETWEEN '2024-01-01' AND '2025-12-31';

-- ═══════════════════════════════════════════════════════
-- ÉTAPE 3 : ÉVALUATION
-- ═══════════════════════════════════════════════════════

-- 3a. Métriques du modèle
SELECT * FROM ML.ARIMA_EVALUATE(MODEL `project.dataset.media_contribution_v1`);

-- 3b. Coefficients des régresseurs (LA requête clé)
SELECT
  processed_input AS canal,
  weight AS poids,
  CASE
    WHEN weight > 0 THEN '✅ Contribution positive'
    WHEN weight < 0 THEN '🚩 Contribution NÉGATIVE — à investiguer'
    ELSE '⚪ Aucun effet détecté'
  END AS diagnostic
FROM ML.ARIMA_COEFFICIENTS(MODEL `project.dataset.media_contribution_v1`)
WHERE processed_input IS NOT NULL
  AND processed_input != '__INTERCEPT__'
ORDER BY ABS(weight) DESC;

-- ═══════════════════════════════════════════════════════
-- ÉTAPE 4 : EXPLICABILITÉ ET CONTRIBUTION
-- ═══════════════════════════════════════════════════════

-- Décomposition de l'historique récent (pas de forecast ici, juste l'explication)
SELECT
  forecast_timestamp AS date,
  forecast_value AS conversions_predites,
  trend + COALESCE(seasonal_period_yearly, 0)
       + COALESCE(seasonal_period_weekly, 0)
       + COALESCE(holiday_effect, 0)
       + COALESCE(step_changes, 0) AS baseline_organique,
  COALESCE(attribution_log_as_sea_brand, 0) AS contrib_sea_brand,
  COALESCE(attribution_log_as_sea_generic, 0) AS contrib_sea_generic,
  COALESCE(attribution_log_as_social, 0) AS contrib_social,
  COALESCE(attribution_log_as_display, 0) AS contrib_display,
  COALESCE(attribution_log_as_youtube, 0) AS contrib_youtube,
  -- Contribution totale média
  COALESCE(attribution_log_as_sea_brand, 0)
  + COALESCE(attribution_log_as_sea_generic, 0)
  + COALESCE(attribution_log_as_social, 0)
  + COALESCE(attribution_log_as_display, 0)
  + COALESCE(attribution_log_as_youtube, 0) AS contrib_media_total
FROM ML.EXPLAIN_FORECAST(
  MODEL `project.dataset.media_contribution_v1`,
  STRUCT(30 AS horizon, 0.90 AS confidence_level),
  (SELECT * FROM `project.dataset.future_media_plan`)
);
```

### 6.5 Calcul du CPA marginal (avec correction adstock)

**⚠️ CRITIQUE : toujours prendre en compte l'effet carry-over de l'adstock dans le calcul du CPA.**

Le modèle utilise `log(adstock + 1)` comme feature. Le CPA marginal représente le coût d'**une conversion supplémentaire** au niveau de dépense actuel.

#### Formule

```
CPA_marginal = (mean_adstock + 1) × (1 - λ) / weight
```

Où :
- `mean_adstock` = moyenne de l'adstock sur la période d'entraînement
- `λ` = taux de rétention adstock du canal
- `weight` = coefficient du régresseur (depuis `ML.ARIMA_COEFFICIENTS`)

#### Pourquoi le facteur `(1 - λ)` ?

1€ dépensé en semaine `t` génère de l'adstock pendant **plusieurs semaines** :
- Semaine `t` : effet = 1
- Semaine `t+1` : effet = λ
- Semaine `t+2` : effet = λ²
- **Total cumulé** = 1 + λ + λ² + ... = **1 / (1 - λ)**

Sans ce correctif, le CPA est **surestimé par un facteur 1/(1-λ)** :

| λ | Multiplicateur | Erreur si oublié |
|---|---|---|
| 0.0 | ×1 | Aucune |
| 0.3 | ×1.4 | CPA 40% trop haut |
| 0.5 | ×2 | CPA 2× trop haut |
| 0.8 | ×5 | CPA 5× trop haut |
| 0.9 | ×10 | CPA 10× trop haut |

#### Template SQL

```sql
-- CPA marginal corrigé par canal
SELECT ecole,
  ROUND((AVG(adstock_social) + 1) * (1 - 0.9) / weight_social, 2) AS cpa_marginal_social,
  ROUND((AVG(adstock_gads) + 1) * (1 - 0.3) / weight_gads, 2) AS cpa_marginal_gads
FROM `project.dataset.prep_weekly`
```

#### Triangulation obligatoire

Toujours comparer le CPA marginal modélisé au CPA moyen GA4 last-click :
- Si CPA_modèle **< CPA_GA4** → cohérent (le modèle capte l'effet incrémental)
- Si CPA_modèle **≈ CPA_GA4** → plausible pour les canaux bas de funnel (Search Brand)
- Si CPA_modèle **>> CPA_GA4 (>3×)** → signal faible, investigation nécessaire :
  - Vérifier la variance du spend (budget "always-on" = signal trop faible)
  - Vérifier la corrélation LOG(adstock) vs conversions
  - Envisager de retirer le canal du modèle

---

## 7. Fonctions Utilitaires Complémentaires

### Détection d'anomalies sur données récentes

```sql
SELECT
  date_column,
  target_metric AS valeur_reelle,
  lower_bound, upper_bound,
  is_anomaly,
  anomaly_probability
FROM ML.DETECT_ANOMALIES(
  MODEL `project.dataset.media_contribution_v1`,
  STRUCT(0.95 AS anomaly_prob_threshold),
  (SELECT * FROM `dataset.recent_data` WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY))
)
WHERE is_anomaly = TRUE
ORDER BY anomaly_probability DESC;
```

**Use case** : alerting automatique dans un dashboard Looker Studio. Si une anomalie est détectée et qu'aucun changement média ne l'explique → investiguer (panne tracking, action concurrentielle, événement externe).

---

## 8. Validation & Sanity Checks (Section Critique)

Un modèle peut avoir un bon AIC mais produire des résultats absurdes. **Ne jamais livrer des résultats sans passer ces checks.**

### 8.1 Checks automatisables (SQL)

```sql
-- CHECK 1 : Aucun canal média ne doit avoir un poids négatif
SELECT processed_input, weight
FROM ML.ARIMA_COEFFICIENTS(MODEL `project.dataset.media_contribution_v1`)
WHERE processed_input LIKE '%log_as_%' AND weight < 0;
-- Si résultat non vide → PROBLÈME. Causes possibles :
--   • Multicolinéarité forte entre canaux
--   • Données erronées (spend inversé, dates décalées)
--   • Canal corrélé à une baisse saisonnière

-- CHECK 2 : Le modèle XREG est meilleur que ARIMA_PLUS simple
-- (Créer un modèle ARIMA_PLUS simple sur les mêmes données et comparer les AIC)

-- CHECK 3 : Les contributions ne dépassent pas 100% du total
-- (Vérifier dans ML.EXPLAIN_FORECAST que la somme des attributions
--  ne dépasse pas la valeur prédite de manière absurde)
```

### 8.2 Checks manuels (jugement business)

| Check | Question à poser | Red flag |
|---|---|---|
| **Sens des signes** | Les canaux média ont-ils un poids positif ? Les prix un poids négatif ? | Un canal payant avec poids négatif = problème de données ou de multicolinéarité |
| **Proportionnalité** | Un canal à 5% du budget a-t-il une contribution plausible ? | Si un petit canal se voit attribuer >30% de la contribution → suspect |
| **Stabilité temporelle** | Les poids changent-ils radicalement si on entraîne sur une autre période ? | Coefficients qui s'inversent d'une période à l'autre = modèle instable |
| **Cohérence avec GA4** | La contribution du SEA Brand est-elle cohérente avec les conversions GA4 last-click ? | Le SEA Brand devrait être similaire dans les deux visions (car c'est du bas de funnel) |
| **Cohérence avec les régies** | La contribution du Social Ads est-elle plus élevée que dans GA4 ? | Si le modèle montre MOINS que GA4 pour le Social → problème (GA4 sous-estime le Social, pas l'inverse) |
| **Cohérence avec Causal Impact** | Si un test CI a montré +30% d'impact Social, le modèle est-il dans le même ordre de grandeur ? | Contradiction forte entre CI et BQML → l'un des deux est faux, investiguer |

### 8.3 Test de stabilité par fenêtre glissante

Pour vérifier que les coefficients sont robustes, entraîner le modèle sur 3+ fenêtres temporelles :

```sql
-- Fenêtre 1 : Jan 2024 - Déc 2024
-- Fenêtre 2 : Avr 2024 - Mar 2025
-- Fenêtre 3 : Jul 2024 - Jun 2025
-- Comparer les poids des régresseurs entre les 3 modèles
-- Si les poids sont stables (même ordre de grandeur, même signe) → modèle robuste
-- Si les poids oscillent fortement → données insuffisantes ou multicolinéarité
```

### 8.4 Règle d'or de la triangulation

**Ne jamais se fier à un seul signal.** Toujours croiser :
1. **ML.ARIMA_COEFFICIENTS** → contribution modélisée
2. **Vision GA4** → attribution mesurée (biaisée mais utile pour le bas de funnel)
3. **Vision régie** → données platform (biaisées mais utile pour le haut de funnel)
4. **Causal Impact** → validation ponctuelle de l'incrémentalité

Si les 4 signaux convergent → confiance élevée.
Si 1 signal diverge → investiguer ce signal.
Si le modèle BQML contredit les 3 autres → le modèle est probablement faux.

---

## 9. Tips pour l'Agent / le Consultant

- Si l'utilisateur demande une prévision "sans effort", vérifier s'il a les données futures des features. Sinon, rediriger vers `ARIMA_PLUS` simple.
- Si l'utilisateur se plaint de prévisions plates, vérifier la cardinalité des features et la variance des données historiques.
- Si les coefficients sont tous proches de zéro, les régresseurs n'apportent rien → problème de qualité des données ou granularité insuffisante (passer de mensuel à hebdo, de hebdo à daily).
- **Ne jamais dire "MMM"** en présentant les résultats de ce modèle au client. Dire "analyse de contribution" ou "diagnostic média".
- Pour un client qui veut un vrai MMM avec optimisation budgétaire et intervalles de crédibilité → rediriger vers Meridian (Phase 3 du framework EdgeAngel).
- Toujours commencer par un modèle simple (2-3 canaux principaux) avant d'ajouter tous les canaux. Ajouter de la complexité progressivement et vérifier que chaque ajout améliore le modèle (AIC plus bas).

---

## 10. Références

- [CREATE MODEL ARIMA_PLUS_XREG](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series)
- [ML.FORECAST](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast)
- [ML.EXPLAIN_FORECAST](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast)
- [ML.ARIMA_COEFFICIENTS](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-coefficients)
- [ML.DETECT_ANOMALIES](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-detect-anomalies)
- [Tutorial : Single time-series forecasting](https://cloud.google.com/bigquery/docs/arima-plus-xreg-single-time-series-forecasting-tutorial)
- [Tutorial : Multiple time-series forecasting](https://cloud.google.com/bigquery/docs/arima-plus-xreg-multiple-time-series-forecasting-tutorial)
- [Tutorial : Anomaly detection](https://cloud.google.com/bigquery/docs/time-series-anomaly-detection-tutorial)
- [Limitations](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series#limitations)
- [TimesFM / AI.FORECAST (Preview)](https://cloud.google.com/bigquery/docs/timesfm-model)
- [Article : ARIMA_PLUS in BigQuery (arXiv)](https://arxiv.org/abs/2510.24452)

> [!TIP]
> Pour explorer plus de documentation BigQuery ML :
> ```
> search_documents("BigQuery ML time series forecasting end-to-end journey")
> search_documents("BigQuery ML ARIMA_PLUS large-scale time series")
> ```

