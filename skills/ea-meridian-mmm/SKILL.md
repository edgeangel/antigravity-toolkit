---
name: meridian-mmm
description: Guide expert pour Google Meridian, framework open-source de Marketing Mix Modeling (MMM) basé sur l'inférence causale bayésienne. Utiliser quand l'assistant doit aider à installer, configurer, exécuter ou interpréter un modèle Meridian — incluant la préparation des données, le paramétrage des priors, l'exécution MCMC, les diagnostics, l'optimisation budgétaire et la planification de scénarios. Couvre aussi l'intégration avec BigQuery, Google Ads, YouTube R&F, GQV et le Meridian Scenario Planner.
---

# Google Meridian — Marketing Mix Modeling

Framework MMM open-source de Google basé sur l'inférence causale bayésienne. Mesure l'impact causal du marketing, estime le ROI par canal et optimise l'allocation budgétaire.

**Repo** : https://github.com/google/meridian
**Docs** : https://developers.google.com/meridian
**Discord** : https://discord.gg/PU7Prfjc8U

---

## 1. Concepts Fondamentaux

### Ce que Meridian résout

| Question business | Sortie Meridian |
|---|---|
| Quel ROI par canal ? | ROI + intervalles crédibles bayésiens |
| Où sont les rendements décroissants ? | Courbes de réponse (response curves) |
| Comment réallouer le budget ? | Optimisation budgétaire (fixed/flexible) |
| Quel est l'impact incrémental ? | Incremental outcome par canal |
| À quelle fréquence diffuser ? | Optimal frequency (si données R&F) |

### Architecture du modèle

Meridian est un **modèle hiérarchique bayésien géo-level** avec :

- **Adstock** : Effet différé des médias (décroissance géométrique ou binomiale)
- **Hill function** : Saturation / rendements décroissants
- **Intercepts time-varying** : Trend et saisonnalité via knots (splines)
- **Effets aléatoires géo** : Hétérogénéité régionale (coefficients τ_g, β_gm)
- **Priors bayésiens** : Injection de connaissance métier (ROI, mROI, contribution)
- **MCMC via NUTS** : Échantillonnage complet des distributions postérieures

**Équation principale (simplifiée)** :

```
y_gt = μ_t + τ_g
     + Σ γ_gi · z_gti           (variables de contrôle)
     + Σ β_gm · Hill(Adstock(x)) (médias payants)
     + Σ β_gom · Hill(Adstock(x)) (médias organiques)
     + Σ β_grf · Adstock(r · Hill(f)) (reach & frequency)
     + ε_gt
```

### Fonctions de transformation

**Adstock** (effet différé) :
- `geometric` (défaut) : w(s;α) = α^s, α ∈ [0,1]
- `binomial` : w(s;α*) = (1 - s/(1+L))^α*, décroissance plus flexible
- Paramètre `max_lag` : durée max de l'effet (défaut = 8 périodes)

**Hill** (saturation) :
- Hill(q, ec, slope) = (1 + (q/ec)^(-slope))^(-1)
- `ec` : point de demi-saturation
- `slope` : pente (=1 concave, >1 forme en S)
- `hill_before_adstock` : ordre des transformations (défaut = False → Adstock puis Hill)

---

## 2. Installation & Prérequis

### Environnement requis

- **Python** : 3.11, 3.12 ou 3.13 (obligatoire — 3.14 trop récent)
- **GPU** : Recommandé (T4, V100, A100) — réduit le temps de ~3x
- **RAM** : 16 GB minimum testé
- **Environnement idéal** : Google Colab Pro+ avec GPU

### Installation

```bash
# GPU (Linux) — recommandé
pip install --upgrade 'google-meridian[and-cuda]'

# CPU uniquement (macOS / pas de GPU)
pip install --upgrade 'google-meridian'

# Colab avec schéma
pip install --upgrade 'google-meridian[colab,and-cuda,schema]'

# Depuis GitHub (dernière version non publiée)
pip install --upgrade git+https://github.com/google/meridian.git

# Vérification
python3 -c "import meridian; print(meridian.__version__)"
```

### ⚠️ Setup macOS Apple Silicon (M1/M2/M3/M4)

> **CRITIQUE** : Meridian deadlock sur macOS ARM sans ces fixes.

1. **`TF_USE_LEGACY_KERAS=1`** : TFP (TensorFlow Probability) est **incompatible avec Keras 3** (défaut dans TF ≥2.16). Il FAUT forcer Keras 2 via cette variable d'environnement.
2. **Importer TensorFlow AVANT pandas** : Sur macOS Sonoma+, importer pandas avant TF cause un freeze silencieux.
3. **Commande de lancement** : Toujours préfixer avec `TF_USE_LEGACY_KERAS=1`.

```bash
# Installer Python 3.12 si nécessaire
brew install python@3.12
python3.12 -m venv .venv-meridian
source .venv-meridian/bin/activate
pip install --upgrade pip
pip install google-meridian

# Lancer un script Meridian sur macOS
TF_USE_LEGACY_KERAS=1 .venv-meridian/bin/python3 script.py
```

### Imports principaux

> **IMPORTANT** : Sur macOS, importer TensorFlow **AVANT** pandas/numpy.

```python
# ====== ENV VARS — en tout premier ======
import os
os.environ['TF_USE_LEGACY_KERAS'] = '1'    # OBLIGATOIRE pour TFP
os.environ['TF_XLA_FLAGS'] = '--tf_xla_auto_jit=0'  # Optionnel, évite warnings XLA
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'    # Réduit le bruit dans les logs

# ====== TF en premier (macOS fix) ======
import tensorflow as tf
tf.config.optimizer.set_jit(False)  # Optionnel, désactive XLA JIT

# ====== Puis les autres ======
import numpy as np
import pandas as pd
import tensorflow_probability as tfp
import xarray as xr
import arviz as az

from meridian import constants
from meridian.data import load
from meridian.model import model, spec, prior_distribution
from meridian.analysis import analyzer, optimizer, visualizer
```

---

## 3. Données d'entrée (InputData)

### Formats supportés

| Format | Loader | Usage |
|--------|--------|-------|
| CSV | `CsvDataLoader` | Le plus courant |
| DataFrame pandas | `DataFrameDataLoader` | Données en mémoire |
| xarray Dataset | `XrDatasetDataLoader` | Format natif Meridian |

### Variables requises et optionnelles

| Variable | Dimensions | Obligatoire | Description |
|----------|-----------|-------------|-------------|
| `kpi` | (n_geos, n_times) | ✅ | Variable dépendante (ventes, conversions, revenue) |
| `kpi_type` | string | ✅ | `'revenue'` ou `'non-revenue'` |
| `population` | (n_geos,) | ✅ géo | Population par zone (scaling) |
| `media` | (n_geos, n_media_times, n_channels) | ✅¹ | Impressions, clics ou spend |
| `media_spend` | (n_geos, n_media_times, n_channels) | ✅¹ | Dépenses médias |
| `reach` | (n_geos, n_media_times, n_rf_channels) | ✅² | Couverture unique |
| `frequency` | (n_geos, n_media_times, n_rf_channels) | ✅² | Fréquence moyenne |
| `rf_spend` | (n_geos, n_media_times, n_rf_channels) | ✅² | Dépenses R&F |
| `controls` | (n_geos, n_times, n_controls) | ⚡ Recommandé | Variables de contrôle (GQV, météo, etc.) |
| `revenue_per_kpi` | (n_geos, n_times) | Optionnel | Conversion KPI → revenu |

> [!IMPORTANT]
> **`revenue_per_kpi` se passe via `CoordToColumns(revenue_per_kpi='col_name')` dans `CsvDataLoader`, PAS dans `ModelSpec`.**
> Pour un LTV constant (ex: 220€/NC), ajouter une colonne constante au CSV :
> ```python
> df['revenue_per_kpi'] = 220.0
> df.to_csv(csv_path, index=False)
> loader = load.CsvDataLoader(
>     coord_to_columns=load.CoordToColumns(revenue_per_kpi='revenue_per_kpi', ...)
> )
> ```
| `organic_media` | (n_geos, n_media_times, n_organic) | Optionnel | Médias sans spend (SEO, social organique) |
| `non_media_treatments` | (n_geos, n_times, n_non_media) | Optionnel | Prix, promos, événements |

¹ Requis pour canaux avec impressions. ² Requis pour canaux avec reach/frequency.
Un canal est soit media/media_spend, soit reach/frequency/rf_spend — jamais les deux.

### Bonnes pratiques données

- **Granularité géo** : Recommandée (DMA, régions, départements) — plus informative que national
- **Granularité temporelle** : Hebdomadaire recommandé
- **Historique minimum** : 2 ans hebdo (géo) / 3 ans (national) / 3 ans mensuel
- **Format date** : `yyyy-mm-dd`
- **Exclure les geos** avec très faible volume d'observations
- **GQV (Google Query Volume)** : Fortement recommandé comme variable de contrôle (réduit le biais)

### Les 4 types de variables d'input (CRITIQUE)

Meridian distingue **4 types de variables** avec des rôles très différents. Ce n'est **PAS** juste `media` et `controls`. Ne pas les confondre sous peine de perdre de l'information causale.

| Type | Champ `InputData` | Intervenable ? | Adstock + Hill ? | ROI calculé ? | Contribution % ? | Exemple |
|------|-------------------|----------------|------------------|---------------|-------------------|---------|
| **Paid Media** | `media` + `media_spend` | ✅ | ✅ | ✅ | ✅ | Google Ads, Social Ads |
| **Organic Media** | `organic_media` | ✅ | ✅ | ❌ (pas de coût) | ✅ | Newsletter, posts sociaux organiques, SEO |
| **Non-Media Treatment** | `non_media_treatments` | ✅ | ❌ | ❌ | ✅ | Promos, prix, Black Friday, soldes |
| **Control** | `controls` | ❌ | ❌ | ❌ | ❌ | GQV, météo, indicateurs macro |

**Critère de décision (doc Google)** :
- *"If you can intervene and change a variable's value (price, promo), it's a **non-media treatment**."*
- *"If it's outside the control of the advertiser (economic indicators, demographics), it's a **control**."*

**Conséquence clé** : Les `non_media_treatments` apparaissent dans le **waterfall de contribution** et ont un **incremental outcome** calculé. Les `controls` sont absorbés dans la baseline — pas de contribution affichée.

> **Décision soldes/BF/Noël** : Si l'annonceur lance activement une promo soldes → `non_media_treatments`. Si c'est juste un flag calendaire national sans action spécifique → `controls`.

### Taxonomie causale des variables de contrôle (Confounders vs Predictors)

Les variables dans `controls` se classent en 3 sous-types selon leur rôle causal :

| Sous-type | Cause sur dépenses média ? | Cause sur KPI ? | Effet dans le modèle | Faut-il l'inclure ? |
|-----------|---------------------------|-----------------|----------------------|---------------------|
| **Confounder** | ✅ Oui | ✅ Oui | **Débiaiser** l'estimation causale | ✅ **Oui, indispensable** |
| **Predictor** | ❌ Non | ✅ Oui | **Réduire la variance** (bruit) | ✅ Oui si fort prédicteur, sinon risque d'overfitting |
| **Mediator** | ❌ (causé PAR le média) | ✅ Oui | ⛔ **Biaise les résultats** | ❌ **Jamais en control** |

**Exemples concrets** :
- **GQV generic** ("golf") → 🔴 Confounder : la demande sectorielle cause les dépenses Search ET les ventes
- **Température** (pour vente de glaces) → 🟢 Predictor : influence les ventes mais pas les budgets pub
- **GQV brand** ("Golfone 64") → 🟠 Mediator potentiel : le Social génère des recherches brand → conversions → "vol" d'attribution

**Recommandations officielles Google** :
1. ✅ Inclure les confounders (débiaiser)
2. ⛔ Exclure les mediators (éviter le biais)
3. ✅ Inclure les predictors forts (réduire variance)
4. ⚠️ Ne pas inclure trop de variables juste pour la prédiction → risque d'overfitting et de biais de spécification

**Pour identifier les confounders**, poser ces questions aux marketing managers :
1. Comment avez-vous décidé le budget total annuel/trimestriel ?
2. Comment avez-vous réparti entre canaux ?
3. Comment avez-vous choisi les semaines hautes/basses ?
4. Y a-t-il des pics de spend liés à des événements ?
5. Quelles sources de données corrèlent le plus avec vos décisions budgétaires ?

> **Note technique** : Côté code Meridian, il n'y a aucune distinction technique entre confounder et predictor. Tout passe dans le même array `controls[]` et est traité comme `γ_gi · z_gti` dans l'équation. La distinction est **conceptuelle et méthodologique** — elle guide le choix de quoi inclure/exclure.

### ⚠️ ALERTE : Variables de contrôle dans un modèle Géo-level (Endogénéité)

Si vous utilisez un modèle **geo-level**, faites extrêmement attention aux variables de contrôle (ex: `concurrence`, `vacances`, `parcoursup`, `promotions`).

**Le problème :**
Par défaut, Meridian applique un "population scaling" (division par la population) sur le KPI et les variables médias pour les comparer, mais **PAS sur les contrôles**.
Si vous fournissez une simple variable binaire nationale (ex: `vacances = 1` pour toutes les régions la même semaine), Meridian va estimer un coefficient d'impact absolu (`gamma`) spécifique pour chaque région, et va ensuite les regrouper ("shrinker") vers une moyenne commune via son prior hiérarchique.
Or, l'impact absolu en nombre de conversions d'un événement national est *mécaniquement* beaucoup plus fort dans une grande région (ex: IDF) que dans une petite (ex: Corse). Forcer ces effets absolus à se regrouper autour de la même moyenne créée un biais massif d'**endogénéité**. Le modèle risque de compenser en écrasant la baseline globale (probabilité de baseline négative qui explose) ou en sur-attribuant aux médias.

**La solution :**
1. **Contrôles dont l'impact global est proportionnel à la population** (ex: variables binaires d'événements 0/1, requêtes Google totales, volume impressions concurrents) :
   👉 Il **FAUT** utiliser le scaling de population. Dans `ModelSpec()`, passez `control_population_scaling_id=[True, ...]` pour ces variables. Meridian divisera la variable par la population ("per capita"). Le modèle estimera alors un effet *per capita* qui, lui, est comparable d'une région à l'autre et peut légitimement être "shrinké" proprement.
2. **Contrôles indépendants de la taille de la région** (ex: température météo, taux de chômage en %) : 
   👉 Ne pas utiliser le population scaling (laisser `False`).

### ⚠️ ALERTE : Google Query Volume (GQV) — Brand vs Generic (CRITIQUE)

**GQV = proxy de demande organique/sectorielle** via Google Trends. Fortement recommandé par Google Meridian.

#### Quel GQV utiliser ?

| Type | Exemple | Rôle dans le modèle | Quand l'utiliser |
|------|---------|---------------------|-----------------|
| **Generic (catégorie)** | "golf", "clubs de golf" | **Confondeur** — capte la saisonnalité sectorielle, tendances marché | ✅ **TOUJOURS recommandé** |
| **Brand** | "Golfone 64", "MBway" | **Médiateur** — absorbe l'effet des campagnes awareness | ⚠️ Avec précaution |

#### Règle d'or :
- **Site e-commerce ads-driven avec Social/awareness** → **GQV GENERIC uniquement**
  - Mettre le GQV brand casserait l'attribution du Social → le modèle croirait que les conversions viennent de la "demande brand organique" alors que c'est le Social qui la crée
- **Marque à forte notoriété naturelle (éducation, automobile)** → GQV brand + generic séparés
  - La notoriété pré-existante est un confondeur qu'il FAUT contrôler

#### Configuration technique :
- Google Trends retourne des **dates le dimanche** → la prep table Meridian attend des **lundis**
  → Faire `DATE_ADD(gqv.date, INTERVAL 1 DAY)` dans le JOIN
- `control_population_scaling_id` : mettre `False` pour GQV (c'est déjà un index 0-100, pas un volume absolu)
- Source : `pytrends` (pip install pytrends) — requête `geo='FR'` au niveau national, pas par région
  - Le GQV generic représente la saisonnalité sectorielle, uniforme géographiquement

#### ⚠️ Trade-off Biais de Médiation
Si le Paid Social génère de la notoriété → recherches Google → conversions :
- GQV **generic** : safe, ne capture pas cet effet indirect du Social
- GQV **brand** : dangereux, "vole" l'attribution du Social. Le CPA Social monte mécaniquement.
- **Verdict** : mieux vaut un Social légèrement sous-évalué qu'un modèle entier biaisé

### Chargement CSV — Exemple complet

```python
from meridian.data import load

# 1. Mapper les colonnes du CSV aux variables Meridian
coord_to_columns = load.CoordToColumns(
    time='date',
    geo='geo',
    kpi='revenue',
    population='population',
    controls=['gqv_brand', 'holiday_flag', 'temperature'],
    media=['impressions_tv', 'impressions_social', 'impressions_display'],
    media_spend=['spend_tv', 'spend_social', 'spend_display'],
    # Optionnel : reach & frequency pour YouTube
    # reach=['yt_reach'],
    # frequency=['yt_frequency'],
    # rf_spend=['yt_spend'],
)

# 2. Mapper les variables média aux noms de canaux
media_to_channel = {
    'impressions_tv': 'TV',
    'impressions_social': 'Social',
    'impressions_display': 'Display',
}
media_spend_to_channel = {
    'spend_tv': 'TV',
    'spend_social': 'Social',
    'spend_display': 'Display',
}

# 3. Charger
loader = load.CsvDataLoader(
    csv_path='/path/to/data.csv',
    kpi_type='revenue',
    coord_to_columns=coord_to_columns,
    media_to_channel=media_to_channel,
    media_spend_to_channel=media_spend_to_channel,
)
data = loader.load()
```

---

## 4. Configuration du Modèle (ModelSpec)

### Paramètres par défaut complets

```python
from meridian.model import spec, prior_distribution

model_spec = spec.ModelSpec(
    # Priors
    prior=prior_distribution.PriorDistribution(),
    
    # Distribution des effets média
    media_effects_dist='log_normal',      # 'log_normal' ou 'normal'
    
    # Transformations média
    hill_before_adstock=False,            # Adstock → Hill (défaut)
    max_lag=8,                            # Durée max carry-over
    adstock_decay_spec='geometric',       # 'geometric', 'binomial', ou dict per-channel
    
    # Types de priors par canal
    media_prior_type='roi',               # 'roi', 'mroi', 'coefficient'
    rf_prior_type='roi',                  # idem pour R&F
    organic_media_prior_type='contribution',
    organic_rf_prior_type='contribution',
    non_media_treatments_prior_type='contribution',
    
    # Calibration
    roi_calibration_period=None,          # Sous-ensemble de données pour calibration
    rf_roi_calibration_period=None,
    
    # Trend & saisonnalité
    knots=None,                           # Auto: T knots (géo) ou 1 (national)
    enable_aks=False,                     # Adaptive Knot Selection (⚠️ RECOMMANDÉ: True pour geo-level)
    
    # Géo
    baseline_geo=None,                    # Auto: plus grande population
    unique_sigma_for_each_geo=False,
    
    # Validation
    holdout_id=None,                      # Train/test split
    control_population_scaling_id=None,
)
```

### Configurer les Priors ROI

```python
import tensorflow_probability as tfp
from meridian import constants

# Prior ROI identique pour tous les canaux
roi_mu, roi_sigma = 0.2, 0.9
prior = prior_distribution.PriorDistribution(
    roi_m=tfp.distributions.LogNormal(roi_mu, roi_sigma, name=constants.ROI_M)
)

# Prior ROI personnalisé par canal
build_args = data.get_paid_media_channels_argument_builder()
roi_m = build_args(
    TV=(0.5, 0.5),        # LogNormal(mu=0.5, sigma=0.5)
    Social=(0.3, 0.7),
    Display=(0.1, 0.9),
    Search=(0.4, 0.6),
)
prior = prior_distribution.PriorDistribution(roi_m=roi_m)

model_spec = spec.ModelSpec(prior=prior, enable_aks=True)
```

### Priors par défaut (clés)

| Paramètre | Distribution par défaut | Notes |
|-----------|------------------------|-------|
| ROI média | LogNormal(0.2, 0.9) | Moyenne ~1.83, médiane 1.22, 80% CI [0.5, 6.0], 95% CI [0.25, 9], 99% < 10 |
| α (adstock) | Uniform(0, 1) | Non-informatif — personnalisable si on connaît le taux de decay |
| ec (half-saturation) | TruncatedNormal(0.8, 0.8, 0.1, 10) | ec=1 → saturation au médian des impressions non-nulles |
| knot_values | Normal(0, 5) | Non-informatif — flexibilité temporelle |
| tau_g (geo effects) | Normal(0, 5) | Non-informatif — différences géographiques |
| gamma_c (controls) | Normal(0, 5) | Non-informatif — large éventail de contrôles possibles |
| slope (Hill) | **Deterministic(1)** | ⚠️ **FIXÉ à 1** → courbe toujours concave. **Recommandé : `LogNormal(0, 0.5)` pour rendre appris** (median=1, P95≈2.3, permet S-curves upper-funnel) |
| slope_rf | LogNormal+Shift | Optimal freq ~2.1, CI [1, 4.4] |

> [!WARNING]
> [!CAUTION]
> **Ne PAS forcer `slope_m=LogNormal(0, 0.5)` sans données suffisantes.** Ce paramètre ajoute un degré de liberté que le modèle peine à estimer simultanément avec `ec_m` et `roi_m`. Sur des datasets petits/moyens (< 200 semaines, < 10 geos), cela cause une **non-convergence systématique** (R-hat > 10¹⁹ observé sur Golfone). Le défaut `Deterministic(1)` (concave) est safe et fonctionne bien en pratique.
>
> **Quand considérer un slope learnable :**
> - Dataset large (200+ semaines, 20+ geos)
> - Canaux upper-funnel avec évidence claire de S-curve
> - Prior très serré : `slope_m = LogNormal(0, 0.3)` max
> - Toujours valider la convergence R-hat après
>
> ```python
> # UNIQUEMENT si dataset suffisamment grand
> slope_m_prior = tfd.LogNormal(loc=0.0, scale=0.3, name=constants.SLOPE_M)
> custom_prior = prior_distribution.PriorDistribution(
>     roi_m=roi_m_prior,
>     slope_m=slope_m_prior,
> )
> ```

### Choix du type de prior

| Type | Utilisable pour | Quand l'utiliser |
|------|----------------|------------------|
| `roi` | Médias payants | Données d'expériences, benchmarks ROI |
| `mroi` | Médias payants | Régulariser l'optimisation budgétaire |
| `contribution` | Tous (organic, non-media) | Intuition sur la part de contribution |
| `coefficient` | Tous | Approche traditionnelle (moins intuitif) |

### Helpers de construction de priors

```python
from meridian.model import prior_distribution

# Construire un LogNormal à partir de la mean/std d'une expérience
lognormal_dist = prior_distribution.lognormal_dist_from_mean_std(
    mean=[1.0, 3.0],  # Point estimates
    std=[0.3, 2.0],   # Standard errors
)
prior = prior_distribution.PriorDistribution(roi_m=lognormal_dist)

# Construire un LogNormal à partir d'un intervalle de confiance
lognormal_dist = prior_distribution.lognormal_dist_from_range(
    low=[0.1, 0.5],
    high=[2.0, 10.0],
    mass_percent=0.95,  # 95% de la masse dans [low, high]
)
prior = prior_distribution.PriorDistribution(roi_m=lognormal_dist)

# Mixer des familles de distributions (LogNormal + HalfNormal)
distributions = [
    tfp.distributions.LogNormal([0.2, 0.2, 0.2], [0.9, 0.9, 0.9]),
    tfp.distributions.HalfNormal(5),  # 4e canal avec HalfNormal
]
roi_m_prior = prior_distribution.IndependentMultivariateDistribution(distributions)
prior = prior_distribution.PriorDistribution(roi_m=roi_m_prior)
```

> **Note** : `IndependentMultivariateDistribution` ralentit légèrement le sampling. Préférer varier les paramètres dans la même famille si possible.

### Adstock decay par canal

```python
# Différencier adstock par canal (awareness vs performance)
model_spec = spec.ModelSpec(
    adstock_decay_spec={
        'Social Ads': 'binomial',   # Awareness — effet distribué (pic puis retombe)
        'Google Ads': 'geometric',  # Performance — décroissance monotone rapide
    },
    max_lag=8,  # GLOBAL uniquement (int) — pas de dict per-channel
)
```

> [!IMPORTANT]
> **`max_lag` est un paramètre GLOBAL (int), pas per-channel.** La syntaxe `max_lag={'canal': N}` n'existe PAS dans l'API ModelSpec. La doc recommande 4-20 pour un mix geometric+binomial.
> Pour brider la durée d'effet du Search spécifiquement, utiliser un **prior d'Alpha** restrictif (ex: `Beta(1, 3)`) plutôt que max_lag.

> [!WARNING]
> **DANGER ADSTOCK & PRIOR-POSTERIOR SHIFT** : 
> Un modèle mal spécifié ou manquant de Baseline peut tricher. Si vous inspectez le `results.json` ou l'interface de résultats et que vous voyez un **Adstock Alpha > 0.9** pour un levier "Performance" comme le Search... c'est que le modèle utilise le lissage infini du Search pour dessiner sa propre baseline organique annuelle.
> *Symptôme* : Alpha = 0.98 -> Half-Life = 51 semaines. Un clic Search dure 1 an. C'est faux.
> *Remède* : Forcer un Prior d'Alpha avec `Beta(1, 3)` pour interdire au canal de tricher temporellement. Complémentairement, garder `max_lag` bas (4-8).

| Type | Forme | Quand l'utiliser |
|------|-------|------------------|
| `geometric` | Décroissance monotone (α^s) | Performance, search, direct response |
| `binomial` | Pic puis retombe (∝ C(L,s) α^s (1-α)^(L-s)) | Awareness, branding, social, TV |

### 3 approches pour KPI non-revenue (leads, conversions)

| Approche | Quand | Code clé |
|----------|-------|----------|
| **Total Media Contribution Prior** | Intuition sur % total du KPI venant du media | `roi_mean = p_mean * kpi / np.sum(cost)` |
| **IKPC (Incremental KPI Per Cost)** | Intuition sur le coût/KPI par canal | `roi_m = LogNormal([0.5, 0.6], [0.5, 0.5])` |
| **Channel Contribution** | Intuition sur la part de chaque canal | `contribution_m = Beta([1, 5], [99, 95])` |

> **⚠️** : Pour IKPC, il faut définir un prior raisonnable pour **chaque** canal. Le défaut ne fonctionne pas sans `revenue_per_kpi`.

> **⚠️** : Pour Channel Contribution, il faut passer `media_prior_type='contribution'` dans ModelSpec — cela s'applique à **tous** les canaux media.

---

## 5. Exécution du Modèle

### Workflow standard (API v1.5.x)

```python
from meridian.model import model

# 1. Initialiser le modèle
mmm = model.Meridian(input_data=data, model_spec=model_spec)

# 2. EDA — via eda_engine (pas de methode run_eda())
# Les checks EDA sont accessible via la propriété eda_outcomes
try:
    outcomes = mmm.eda_outcomes
    for o in outcomes: print(o)
except Exception as e:
    print(f"EDA skip: {e}")

# 3. Échantillonner le prior
# API v1.5.x: sample_prior(n_draws, seed=None)
mmm.sample_prior(n_draws=500)

# 4. Échantillonner le posterior (MCMC — étape principale)
# API v1.5.x: sample_posterior(n_chains, n_adapt, n_burnin, n_keep, ...)
# ⚠️ Recommandations getting-started (Google, février 2026):
#   n_chains=10, n_adapt=2000, n_burnin=500, n_keep=1000
mmm.sample_posterior(
    n_chains=10,         # Nombre de chaînes MCMC (getting-started = 10)
    n_adapt=2000,        # Steps d'adaptation NUTS (getting-started = 2000)
    n_burnin=500,        # Steps de warmup à jeter
    n_keep=1000,         # Samples à garder (post-burnin)
)

# 5. Sauvegarder le modèle
model.save_mmm(mmm, '/path/to/model.pkl')

# 6. Recharger plus tard
mmm = model.load_mmm('/path/to/model.pkl')
```

> **Note** : `run_eda()` n'existe pas dans v1.5.x. EDA est via `mmm.eda_engine` / `mmm.eda_outcomes`.

### Temps d'exécution indicatifs

| Config | GPU T4 | CPU macOS ARM (M-series) |
|--------|--------|-----|
| 50 geos, 104 semaines, 6 canaux, 10ch | ~15-30 min | ~1-2h |
| 4 geos, 137 semaines, 3 canaux, 10ch | ~3-5 min | **~3 min** |
| National, 154 semaines, 2 canaux, 4ch | ~5 min | **~36 secondes** |
| National, 156 semaines, 6 canaux, 4ch | ~5-10 min | ~5-10 min |

---

## 6. Diagnostics du Modèle

### Checks de convergence

```python
from meridian.analysis import visualizer

# Diagnostics
diag = visualizer.ModelDiagnostics(mmm)

# R-hat boxplots (convergence MCMC)
diag.plot_rhat_boxplot()    # Cible : R-hat < 1.1 (strict) ou < 1.3 (exploratoire)

# Comparaison prior vs posterior
diag.plot_prior_and_posterior_distribution()
```

> **Note** : Les plots retournent des **objets Altair** (LayerChart, FacetChart), pas Matplotlib.
> Pour sauvegarder : `chart.save('plot.html')` (interactif) — pas `.savefig()`.

### Critères de qualité

| Métrique | Cible | Action si hors cible |
|----------|-------|---------------------|
| R-hat | < 1.1 (production), < 1.3 (exploration) | Augmenter num_warmup/num_samples |
| ESS (Effective Sample Size) | > 500 par chaîne | Augmenter num_samples |
| Divergences | < 1% | Revoir priors, max_lag, knots |
| R² | > 0.8 (géo agrégé) | Ajouter controls, revoir spec |
| MAPE | < 15% | Ajuster modèle |
| P(baseline négatif) | < 5% (posterior) | Resserrer priors, contribution prior, ajouter contrôles |
| Bayesian PPP | ∈ [0.05, 0.95] | Si hors : misspecification du modèle |

### ModelReviewer — Quality Checks automatisés (Step 3 Getting-Started)

```python
# Import correct (v1.5.1+) :
from meridian.analysis.review import reviewer

# Lancer tous les checks :
result = reviewer.ModelReviewer(mmm).run()
print(result)  # ReviewSummary avec Overall Status + 6 checks
```

#### ⚠️ OOM sur Mac local (10 chains × 1000 draws)
Le `ModelReviewer.run()` nécessite beaucoup de RAM car il :
1. Crée un `Analyzer(model_context, inference_data)` 
2. Lance `BayesianPPPCheck` qui recalcule des prédictions sur tous les draws

**Sur Mac ARM avec 10 chains** → le process est **killed par OOM** pendant le Baseline/BayesianPPP check.

**Solutions** :
- **Cloud (Colab/Vertex AI)** : recommandé pour 10+ chains
- **Local** : réduire à 4 chains pour les quality checks, ou faire les checks manuellement :

```python
# Version lightweight si OOM :
from meridian.analysis.review import checks, configs
from meridian.analysis import analyzer as analyzer_module

analyzer = analyzer_module.Analyzer(
    model_context=mmm.model_context,
    inference_data=mmm.inference_data,
)

# Convergence (léger, toujours OK local)
conv = checks.ConvergenceCheck(mmm, analyzer, configs.ConvergenceConfig())
print(conv.run())  # PASS si R-hat < 1.2
```

Checks disponibles (6 total) :
| Check | Statut | Description |
|-------|--------|-------------|
| **Convergence** (R-hat) | PASS si tous < 1.2 | Toujours exécutable local |
| **Negative Baseline** | PASS si P < 1% | Nécessite posterior predictive (RAM++) |
| **Bayesian PPP** | PASS si ∈ [0.05, 0.95] | Nécessite posterior predictive (RAM++) |
| **Goodness of Fit** | PASS si R² > 0.7 | MAPE, wMAPE, R² |
| **Prior-Posterior Shift** | PASS si shift modéré | Uniquement si ROI priors customs |
| **ROI Consistency** | PASS si ROI plausible | Uniquement si ROI priors customs |

> **Note** : Prior-Posterior Shift et ROI Consistency ne s'appliquent qu'avec des priors ROI.

### Model Fit

```python
fit = visualizer.ModelFit(mmm)

# Expected vs Actual (graphique principal — retourne un Altair chart)
chart = fit.plot_model_fit()
chart.save('model_fit.html')   # Sauvegarde interactive
```

### Baseline Assessment

```python
a = analyzer.Analyzer(mmm)

# P(baseline négatif) sur le posterior
neg_prob = a.negative_baseline_probability()
print(f"P(neg baseline) = {float(neg_prob):.2%}")  # Doit être < 5%

# P(contribution totale > 100%) sur le PRIOR (avant posterior)
mmm.sample_prior(500)
a_prior = analyzer.Analyzer(mmm)
outcome = np.array(mmm.kpi)
if mmm.revenue_per_kpi is not None:
    outcome = outcome * np.array(mmm.revenue_per_kpi)
total_outcome = float(np.sum(outcome))
prior_inc = np.array(a_prior.incremental_outcome(use_posterior=False))
total_contrib = np.sum(prior_inc, -1) / total_outcome
print(f"P(contrib > 100%) = {np.mean(total_contrib > 1):.2%}")  # Doit être < 5%
```

Si baseline négatif :
1. Utiliser **contribution priors** ou **Total Media Contribution Prior**
2. Vérifier que le 90e percentile ROI d'un canal n'implique pas > 100% de contribution
3. Ajouter des **contrôles de qualité** (GQV, variables macro)
4. Augmenter les **knots** si la saisonnalité n'est pas bien captée

### Holdout observations (train/test split)

```python
import numpy as np

# Créer un holdout balanced ~10% des observations
rng = np.random.default_rng(42)
holdout_id = rng.random(data.kpi.shape) < 0.10

model_spec = spec.ModelSpec(
    holdout_id=holdout_id,
    ...
)
```

> **IMPORTANT** :
> - Le holdout doit être **équilibré** à travers geos ET temps
> - **NE PAS** retirer de gros blocs continus en fin de période (Meridian ≠ forecasting)
> - Les données media du holdout sont **toujours utilisées** (pour l'adstock)
> - Seul le KPI du holdout est ignoré pendant le training
> - Utiliser le **même holdout** pour comparer des versions du modèle

---

## 7. Résultats & Analyse

### Métriques clés

```python
from meridian.analysis import analyzer

a = analyzer.Analyzer(mmm)

# ROI par canal (posterior)
roi = a.roi()                    # shape: (chains, draws, channels)
roi_mean = np.mean(roi, axis=(0,1))

# ROI marginal (mROI)
mroi = a.marginal_roi()

# Outcome incrémental
inc = a.incremental_outcome()

# Courbes de réponse
response = a.response_curves()
```

### Visualisations (v1.5.x — Altair)

> **IMPORTANT** : Tous les plots Meridian retournent des **objets Altair**, pas Matplotlib.
> Utiliser `.save('fichier.html')` pour exporter en HTML interactif.

```python
# Media summary
media_viz = visualizer.MediaSummary(mmm)

# ROI avec intervalles crédibles
media_viz.plot_roi_bar_chart().save('roi_bar.html')

# Spend vs Contribution
media_viz.plot_spend_vs_contribution().save('spend_vs_contribution.html')

# Contribution waterfall
media_viz.plot_contribution_waterfall_chart().save('waterfall.html')

# Contribution pie chart
media_viz.plot_contribution_pie_chart().save('pie.html')

# CPIK (Coût par KPI Incrémental)
media_viz.plot_cpik().save('cpik.html')

# ROI vs mROI
media_viz.plot_roi_vs_mroi().save('roi_vs_mroi.html')

# Channel contribution area (stacked area dans le temps)
media_viz.plot_channel_contribution_area_chart().save('contribution_area.html')

# Channel contribution bump chart
media_viz.plot_channel_contribution_bump_chart().save('bump.html')

# ROI vs Effectiveness
media_viz.plot_roi_vs_effectiveness().save('roi_vs_eff.html')
```

### Rapport HTML complet (2 pages)

```python
# Rapport modèle (2 pages avec tous les graphiques)
from meridian.analysis import summarizer
s = summarizer.Summarizer(mmm)
s.output_model_results_summary(
    'summary_report.html',
    '/output/path/',
    start_date='2023-01-01',
    end_date='2025-12-31',
)
```

> **Note** : Le rapport HTML est autonome (contient CSS + Altair inline). Ouvrir avec `open fichier.html`.

---

## 8. Optimisation Budgétaire

### Scénario Budget Fixe (défaut)

Maximise le ROI pour un budget donné.

```python
from meridian.analysis import optimizer

budget_opt = optimizer.BudgetOptimizer(mmm)

# Défaut : budget historique, allocation historique
opt_results = budget_opt.optimize()

# Personnalisé
opt_results = budget_opt.optimize(
    selected_times=('2024-01-01', '2024-12-31'),
    budget=1_000_000,
    pct_of_spend={
        'TV': 0.3, 'Social': 0.25, 'Display': 0.2,
        'Search': 0.15, 'YouTube': 0.1,
    },
    spend_constraint_lower=0.3,   # Min -30% par canal
    spend_constraint_upper=0.5,   # Max +50% par canal
)
```

### Scénario Budget Flexible — Target ROI

Maximise le revenu incrémental tout en maintenant un ROI minimum.

```python
opt_results = budget_opt.optimize(
    fixed_budget=False,
    target_roi=2.0,
    spend_constraint_lower=0.5,
    spend_constraint_upper=0.5,
)
```

### Scénario Budget Flexible — Target mROI

Détermine le budget max par canal pour un mROI cible.

```python
opt_results = budget_opt.optimize(
    fixed_budget=False,
    target_mroi=1.0,
    spend_constraint_lower=0.5,
    spend_constraint_upper=0.5,
)
```

### Fréquence optimale (si R&F)

```python
opt_results = budget_opt.optimize(
    use_optimal_frequency=True,
    max_frequency=10.0,
)
```

### Export des résultats

```python
# Rapport HTML optimisation (2 pages)
opt_results.output_optimization_summary('optimization_report.html', '/output/')

# Summary metrics programmatique
summary = opt_results.summary_metrics
# Contient : spend optimisé, ROI, mROI, incremental outcome par canal
```

---

## 9. Planification de Scénarios (Scenario Planning)

Pour tester des hypothèses futures différentes de l'historique.

### Cas d'usage

| Scénario | Solution |
|----------|----------|
| Le CPM a changé | Fournir `new_data` avec nouveau spend |
| Nouveau canal lancé | Ajouter le canal dans new_data |
| Revenue per KPI différent | Mettre à jour `revenue_per_kpi` |
| Flighting pattern différent | Modifier la distribution temporelle |

```python
# Exemple : coût par impression différent pour l'année prochaine
import copy

new_data = copy.deepcopy(data)
# Modifier les données de spend ou media dans new_data...

opt_results = budget_opt.optimize(
    new_data=new_data,
    start_date='2025-01-01',
    end_date='2025-12-31',
)
```

### Meridian Scenario Planner (UI interactive)

Dashboard Looker Studio interactif connecté au modèle. Permet aux non-techniques de :
- Tester des scénarios budget fixe / flexible
- Ajuster les contraintes par canal
- Visualiser ROI, mROI, courbes de réponse
- Exporter les résultats

Doc : https://developers.google.com/meridian/docs/scenario-planning/meridian-scenario-planner

---

## 10. Google MMM Data Platform

### Données disponibles

| Donnée | Source | Usage Meridian |
|--------|--------|---------------|
| **Impressions, clics, spend** | Google Ads, DV360 | `media`, `media_spend` |
| **YouTube Reach & Frequency** | Google Ads + DV360 (dédupliqué) | `reach`, `frequency`, `rf_spend` |
| **Google Query Volume (GQV)** | Recherche Google | `controls` (variable de confusion) |

### Accès

1. Demander l'accès : https://forms.gle/k6rxQC4WLC4RzFmz6
2. Réponse sous 3 jours ouvrés
3. Livraison vers Google Cloud, S3 ou SFTP
4. Granularité : national ou régional (selon pays)
5. Fréquence : ponctuel, mensuel ou trimestriel

### GQV — Points clés

- Données **indexées** (pas de volumes bruts) — n'impacte pas le modèle (variable de contrôle)
- Contient termes **brand** et **generic** basés sur les Keyword Graph Entities
- **Fortement recommandé** : réduit le biais d'estimation en contrôlant la demande naturelle
- Pas impacté par les AI Overviews (mesure les requêtes, pas les résultats)

---

## 11. Intégration BigQuery & Cortex

### Google Cloud Cortex Framework

Pipeline automatisé pour préparer les données Meridian depuis :
- **Cross Media & Product Connected Insights** (Google Ads, DV360)
- **SAP/Oracle EBS** pour les données de ventes
- **BYOD** (Bring Your Own Data)

Vue principale : `CrossMediaSalesInsightsWeeklyAgg`

### Architecture Cortex for Meridian

```
Cloud Storage
├── /configuration     → cortex_meridian_config.json
├── /models           → Modèles sauvegardés
├── /notebooks        → Notebook principal (Colab Enterprise)
├── /reporting        → Rapports HTML
├── /csv              → Résultats CSV
└── /notebook-run-logs → Logs d'exécution
```

---

## 12. Unified Schema (Protocol Buffers)

Schéma standardisé framework-agnostique pour :
- Représenter inputs/outputs MMM (Meridian, Robyn, etc.)
- Sérialiser modèles et résultats (protobuf)
- Alimenter dashboards (Scenario Planner)
- Versionner et partager entre équipes

Structure : `MmmKernel` → `MarketingDataPoint` → KPI, média, contrôles, R&F, non-média

---

## 13. Debugging & Troubleshooting

### Problèmes courants

| Symptôme | Cause probable | Solution |
|----------|---------------|----------|
| **Deadlock/freeze macOS ARM** à model init | Keras 3 incompatible avec TFP | `TF_USE_LEGACY_KERAS=1` (**CRITIQUE**) |
| **Freeze silencieux macOS Sonoma** | Import pandas avant TF | Importer `tensorflow` AVANT `pandas` |
| "Compiled cluster using XLA" puis freeze | XLA graph tracing deadlock | `TF_USE_LEGACY_KERAS=1` + importer TF en premier |
| R-hat > 1.3 | Convergence insuffisante | ↑ n_burnin, ↑ n_keep, simplifier modèle |
| ROI négatif | Prior trop large ou données aberrantes | Revoir priors, vérifier données |
| ROI irréaliste (>10) | Prior non-informatif + signal faible | Calibrer avec expériences, resserrer priors |
| OOM (Out of Memory) | Trop de geos × times × canaux | Réduire geos, utiliser GPU, batch |
| mROI >> ROI | Canal sous-saturé | Normal — opportunité d'investir plus |
| mROI << ROI | Canal sur-saturé | Réallouer budget vers canaux à haut mROI |
| Baseline trop haut/bas | Knots mal configurés | Activer `enable_aks=True`, ajuster knots |
| Pas assez de données (national) | Trop de paramètres vs observations | Combiner canaux, réduire knots, ≥15 data points/effet |
| Knots trop nombreux (national) | AKS agressif | Tuner `base_penalty=np.geomspace(10,200,100)`, `max_internal_knots=10` |
| **Baseline négatif (non-revenue)** | **Over-attribution media avec KPI volume** | **⚠️ Voir section 13bis ci-dessous — Total Media Contribution Prior** |
| Contribution > 100% par canal | Prior `contribution` Beta(1,99) trop permissif | Utiliser Total Media Contribution Prior (roi custom) |
| Effet différé non capturé | max_lag trop court | ↑ max_lag, tester binomial decay |
| `.savefig()` error sur plot | Meridian utilise Altair, pas Matplotlib | Utiliser `.save('file.html')` au lieu de `.savefig()` |
| `run_eda()` not found | API changée en v1.5.x | Utiliser `mmm.eda_outcomes` directement |
| `num_chains` error sur `sample_prior` | API v1.5.x différente | `sample_prior(n_draws=500)` (pas num_chains) |

### Workflow de debugging

1. **EDA** : `mmm.eda_outcomes` — vérifier les warnings
2. **Prior predictive check** : `mmm.sample_prior(n_draws=500)` → distributions cohérentes ?
3. **Convergence** : R-hat, ESS, divergences
4. **Model fit** : R², MAPE, expected vs actual
5. **Prior vs Posterior** : Les données informent-elles le modèle ?
6. **Holdout** : Performance out-of-sample via `holdout_id`
7. **Sensibilité** : Tester différents priors et configs

### Évaluation du R² holdout (validation hors-échantillon)

> [!NOTE]
> **Un R² holdout = 0.50 est normal et acceptable** pour un MMM geo-level bayésien.
> La doc Meridian confirme : "Trouver un degré de régularisation approprié peut être un processus itératif qui implique de vérifier l'ajustement hors échantillon."

| Contexte | Ordre de grandeur attendu |
|---|---|
| R² in-sample (train) | 0.90 – 0.98 |
| R² holdout (test) | **0.40 – 0.70** |
| R² All Data | 0.90 – 0.96 |

**Pourquoi le holdout est plus bas :**
- Holdout random (10%) = observations isolées sans contexte temporel voisin
- Peu de geos (4) = faible puissance de validation croisée
- La saisonnalité forte crée du bruit si une semaine de fêtes tombe en holdout

**Quand s'inquiéter :**
- R² holdout < 0 → modèle pire que la moyenne (revoir priors, données)
- wMAPE holdout > 50% → large écart systématique
- R² in-sample - R² holdout > 0.5 → overfitting probable → ↓ knots, resserrer priors

### Guide `max_lag` (revue doc officielle Mars 2026)

| Adstock type | Plage recommandée | Défaut | Notes |
|---|---|---|---|
| **Geometric** | **2 – 10** | 8 | Effet court terme, décroissance monotone. max_lag plus petit = moins de variance |
| **Binomial** | **4 – 20** | 8 | Effet étalé (courbe en cloche). Peut nécessiter max_lag plus élevé |

> `max_lag` est un **int global** (pas de dict par canal). Pour brider un canal spécifique → prior Alpha restrictif (ex: Beta(2,5) pour forcer un decay rapide).

### Guide AKS (Automatic Knot Selection)

L'AKS est recommandé pour le geo-level. Il utilise une régression pénalisée avec élimination progressive des knots, optimisée par AIC. La pénalité s'adapte au nombre de geos (plus de geos = plus de knots).

```python
# AKS par défaut (recommandé)
model_spec = spec.ModelSpec(enable_aks=True)

# AKS custom (si trop/pas assez de knots)
model_spec = spec.ModelSpec(
    enable_aks=True,
    knots_num=10,  # max knots à considérer
)
```

### Prior alpha custom (adstock decay)

Par défaut, alpha est `Uniform(0,1)` (non-informatif). Si on connaît le comportement du canal :

```python
import tensorflow_probability as tfp
tfd = tfp.distributions

# Alpha restrictif pour Search (decay rapide)
alpha_search = tfd.Beta(2.0, 5.0)  # favorise α faible (decay rapide)

# Alpha permissif pour TV/Video (decay lent)
alpha_tv = tfd.Beta(5.0, 2.0)  # favorise α élevé (decay lent)
```

---

## 13bis. KPI Non-Revenue (Conversions / Volume) — GUIDE CRITIQUE

> **⚠️ PIÈGE MAJEUR** : Modéliser un KPI non-monétaire (conversions, leads, new clients) avec les priors par défaut de Meridian produit quasi-systématiquement un **baseline négatif** et des contributions > 100% par canal. C'est un problème documenté (GitHub #430, #419, #791).

### Pourquoi ça échoue avec les priors par défaut

| Approche testée | Résultat | Pourquoi |
|---|---|---|
| `non_revenue` + `revenue_per_kpi` mal calibré | Baseline = -651K | ROI prior attend des € mais reçoit des KPI units |
| `revenue` KPI + conversion ratio | Ne modélise pas le volume | Approximation, pas un vrai modèle client |
| `contribution` prior Beta(1,99) | Total media = 1027% | Beta(1,99) ne contraint pas assez la somme des contributions |
| `non_revenue` sans `revenue_per_kpi` | Baseline = -115K | Auto-calibration ROI insuffisante pour le volume |

### ✅ Solution : Total Media Contribution Prior

Documentation officielle : https://developers.google.com/meridian/docs/advanced-modeling/unknown-revenue-kpi-custom

Principe : calculer un **prior ROI commun** (LogNormal) tel que la contribution totale des médias ait une moyenne et un écart-type cibles.

```python
import numpy as np
import tensorflow_probability as tfp
tfd = tfp.distributions

# Paramètres business — à ajuster par client
p_mean = 0.3   # 30% du KPI vient du paid media
p_sd = 0.15    # ±15 points de pourcentage

revenue_per_kpi = 220.0  # valeur monétaire par unité de KPI
total_kpi = df['new_clients_ga4'].sum()  # KPI total
kpi_revenue = total_kpi * revenue_per_kpi  # en unités monétaires

# Spend total par canal
spend_cols = ['spend_channel1', 'spend_channel2', ...]
cost = np.array([df[c].sum() for c in spend_cols])

# Formule Google : dériver LogNormal à partir de p_mean/p_sd
roi_mean = p_mean * kpi_revenue / np.sum(cost)
roi_sd = p_sd * kpi_revenue / np.sqrt(np.sum(np.power(cost, 2)))

lognormal_sigma = np.sqrt(np.log(roi_sd**2 / roi_mean**2 + 1))
lognormal_mu = np.log(roi_mean * np.exp(-lognormal_sigma**2 / 2))

roi_prior = tfd.LogNormal(
    np.float32(lognormal_mu),
    np.float32(lognormal_sigma),
)
```

### Diagnostics Prior OBLIGATOIRES

Avant de lancer le posterior, toujours vérifier :

```python
mmm.sample_prior(n_draws=500)
a = analyzer.Analyzer(mmm)

# 1. P(baseline négatif) — doit être < 5%
neg_prob = a.negative_baseline_probability(use_posterior=False)
print(f"Prior P(neg baseline) = {float(neg_prob):.2%}")

# 2. P(contribution totale > 100%) — doit être < 5%
outcome = np.array(mmm.kpi)
if mmm.revenue_per_kpi is not None:
    outcome = outcome * np.array(mmm.revenue_per_kpi)
total_outcome = float(np.sum(outcome))
prior_inc = np.array(a.incremental_outcome(use_posterior=False))
total_contrib = np.sum(prior_inc, -1) / total_outcome
print(f"Prior P(contrib > 100%) = {np.mean(total_contrib > 1):.2%}")
print(f"Prior mean contrib = {np.mean(total_contrib):.2%}")
```

Si ces checks échouent : ajuster `p_mean` ou `p_sd` et recalculer le prior.

### 🔬 Grid Search Prior — Sélection optimale de p_mean/p_sd

> **Technique validée** : au lieu de deviner p_mean/p_sd, lancer un **grid search MCMC léger** (4 chains × 500 samples, ~1.5 min/scénario) avec une grille de combinaisons, puis comparer les résultats pour choisir le meilleur compromis.

#### Méthodologie

1. **Définir une grille** de 6-10 scénarios p_mean × p_sd
2. **Exécuter un MCMC court** pour chaque (4 chains, n_adapt=1000, n_burnin=250, n_keep=500)
3. **Extraire les métriques** : baseline%, ROI par canal, P(neg baseline), CI width
4. **Comparer** et choisir le scénario optimal

```python
# Grille recommandée
SCENARIOS = [
    (0.40, 0.20),  # conservateur
    (0.45, 0.20),
    (0.50, 0.20),
    (0.55, 0.20),  # modéré
    (0.60, 0.20),
    (0.65, 0.20),  # agressif
    (0.55, 0.15),  # modéré + CI tight
    (0.60, 0.15),  # agressif + CI tight
]

for p_mean, p_sd in SCENARIOS:
    # 1. Calculer le prior LogNormal
    roi_mean = p_mean * total_revenue / np.sum(cost)
    roi_sd = p_sd * total_revenue / np.sqrt(np.sum(np.power(cost, 2)))
    lognormal_sigma = np.sqrt(np.log(roi_sd**2 / roi_mean**2 + 1))
    lognormal_mu = np.log(roi_mean * np.exp(-lognormal_sigma**2 / 2))
    
    # 2. Construire le modèle avec ce prior
    roi_prior = tfd.LogNormal(loc=..., scale=..., name=constants.ROI_M)
    # ... (model spec, mmm = model.Meridian(...))
    
    # 3. MCMC léger (4 chains × 500 = ~1.5 min)
    mmm.sample_posterior(n_chains=4, n_adapt=1000, n_burnin=250, n_keep=500)
    
    # 4. Extraire résultats
    a = analyzer.Analyzer(mmm)
    inc = np.array(a.incremental_outcome())
    baseline = total_revenue - float(np.mean(np.sum(inc, axis=-1)))
    neg_prob = float(a.negative_baseline_probability())
```

#### Critères de sélection

| Critère | Seuil | Priorité |
|---|---|---|
| **P(neg baseline)** | < 1% | 🔴 Éliminatoire |
| **Baseline cohérent** | Revenue baseline > NC baseline | 🔴 Éliminatoire |
| **CI width** | P95/P5 ratio < 5x | 🟡 Souhaitable |
| **ROI réaliste** | 1 < ROI < 10 pour tous les canaux | 🟡 Souhaitable |
| **P(contrib > 100%)** | < 5% (prior) | 🟢 Informatif (revenue only) |

#### Findings Golfone FR NC (8 scénarios)

- **p_sd** a **peu d'impact sur la baseline**, mais **réduit les CI** (0.15 → CI ~30% plus serrés)
- **p_mean** contrôle linéairement la baseline (~3% de baseline par +0.05 de p_mean)
- Les **ROI sont très stables** entre scénarios (±0.5 de variation) → le modèle est robuste
- Le grid search converge en **~12 min total** (8 × 1.5 min)

> [!TIP]
> **Appliquer le p_mean/p_sd optimal du Revenue au NC du même marché** plutôt que de gridsearcher les deux. Le NC est un sous-ensemble du Revenue, donc la dépendance média est similaire.

### Exemple complet — Golfone New Clients

```python
# KPI = new_clients_ga4 (93/sem avg, 12362 total sur 133 sem)
# revenue_per_kpi = 220€/client
# 5 canaux : GAds Brand, GAds Croissance, GAds Perf, Meta, Bing
# Total spend = 227,532€
# p_mean=0.3, p_sd=0.15

# Résultat du calcul :
# roi_mean = 3.586, roi_sd = 2.540
# LogNormal(mu=1.074, sigma=0.638)

# Prior checks :
# P(neg baseline) = 0.80% ✅
# P(contrib > 100%) = 0.40% ✅
# Mean total contrib = 32.18% ✅

# Résultats finaux :
# Baseline = 8,022 clients (64.9%)
# Total media = 4,340 clients (35.1%)
# CPNC global = 52€
# P(neg baseline) posterior = 0.00%
```

### Checklist non-revenue

- [ ] Définir `revenue_per_kpi` (valeur monétaire unitaire du KPI)
- [ ] Choisir `p_mean` (contribution media cible : 20-40% typique)
- [ ] Calculer le prior LogNormal via la formule Google
- [ ] Vérifier P(neg baseline) < 5% sur le prior
- [ ] Vérifier P(contrib > 100%) < 5% sur le prior
- [ ] Après posterior : vérifier baseline positif et cohérent
- [ ] Interpréter les résultats en CPNC plutôt qu'en ROI €/€

### ⚠️ Calibrage des priors — Pièges & Best Practices

> **CRITIQUE** : Un sigma LogNormal trop élevé est la cause #1 d'intervalles de confiance inutilisables. Le sigma contrôle directement la largeur des posteriors.

#### Valeurs de référence sigma LogNormal

| Source | sigma | Ratio P95/P5 | Contexte |
|---|---|---|---|
| **Meridian default** ROI prior | **0.9** | ~19x | `LogNormal(0.2, 0.9)` — weakly informative |
| **National eCommerce** tuto | **0.5** | ~5x | `LogNormal(0.1, 0.5)` |
| **SKILL Golfone** (5 canaux) | **0.638** | ~8x | p_mean=0.30, p_sd=0.15 |
| **Production target** | **0.5–0.9** | 5–19x | CIs exploitables pour décision |
| ❌ **Pigier V4** (bug) | **2.04** | ~820x | p_sd=0.20 + adj_factor=2.0x |

**Formule de vérification rapide** : `ratio_P95_P5 = exp(2 × 1.645 × sigma)`

```python
# Vérifier AVANT de lancer le posterior
sigma = lognormal_sigma  # ou adjusted_sigma si applicable
ratio = np.exp(2 * 1.645 * sigma)
print(f"Prior P95/P5 ratio: {ratio:.1f}x")
# Si ratio > 30x → prior trop vague, resserrer p_sd
# Si ratio < 3x → prior trop informatif, risque de biais
```

#### ❌ Ne JAMAIS appliquer de facteur multiplicatif sur sigma

```python
# ❌ INTERDIT — non documenté dans Meridian, gonfle le sigma exponentiellement
adjusted_sigma = lognormal_sigma_base * 2.0  # JAMAIS

# ✅ CORRECT — utiliser le sigma directement issu de la formule p_mean/p_sd
sigma_arr = np.array([lognormal_sigma] * n_channels, dtype=np.float32)
```

L'`adjustment_factor` sur sigma n'a **aucune base dans la documentation Meridian**. Pour différencier les canaux, utiliser des priors par canal via `IndependentMultivariateDistribution` avec des mu/sigma distincts basés sur des benchmarks.

#### Grille p_mean / p_sd recommandée

| Contexte | p_mean | p_sd | CV | Sigma ~résultant | Usage |
|---|---|---|---|---|---|
| **Très conservateur** (peu de canaux, pas de données) | 0.20 | 0.15 | 75% | 0.65–0.80 | Secteur éducation, 2 canaux, national |
| **Standard** (intuition métier modérée) | 0.30 | 0.15 | 50% | 0.45–0.65 | 3-5 canaux, benchmarks disponibles |
| **Informatif** (expériences passées, lift tests) | 0.30–0.40 | 0.10 | 25–33% | 0.30–0.45 | Post-calibration avec données expérimentales |
| **Meridian default** (contribution prior) | 0.40 | 0.20 | 50% | 0.45–0.55 | Défaut documenté Google |

> **Règle d'or** : `p_sd ≤ p_mean` (CV ≤ 100%). Si CV > 100%, le prior est trop vague et les CIs seront inutilisables sur un setup mono-géo.

#### Checklist avant lancement

- [ ] Calculer sigma LogNormal et vérifier qu'il est **< 1.0**
- [ ] Calculer le ratio P95/P5 et vérifier qu'il est **< 30x**
- [ ] **Aucun** adjustment_factor sur sigma
- [ ] Vérifier P(neg baseline) < 5% sur le prior
- [ ] Vérifier P(contrib > 100%) < 5% sur le prior

### ⚠️ Calcul CPIK — Piège de Jensen

> **CRITIQUE** : `CPIK = spend / mean(incremental)` ≠ `median(spend / incremental_par_draw)`. Le premier est **biaisé** (inégalité de Jensen : E[1/X] ≠ 1/E[X]).

```python
# ❌ BIAISÉ — ne PAS utiliser pour le CPIK
cpl_biased = total_spend / np.mean(inc_leads)

# ✅ CORRECT — calculer CPIK par draw puis prendre median + percentiles
# C'est ce que fait le Summarizer Meridian (chart CPIK)
cpik_draws = total_spend / np.maximum(inc_leads_per_draw, 1e-6)
cpik_median = np.percentile(cpik_draws, 50)     # Point estimate
cpik_5, cpik_95 = np.percentile(cpik_draws, [5, 95])  # 90% CI
```

**Conséquence** : Le CPIK médian sera toujours **plus élevé** que spend/mean(inc) car les draws avec peu d'incrémental produisent des CPIK très élevés qui tirent la médiane vers le haut. Pour le ROI (qui est direct, pas inversé), les deux méthodes donnent des résultats proches.

---

## 10. Modèle Spatial (Geo-Level) : Pièges & Bonnes Pratiques

Le passage d'un modèle National à un modèle Geo-Level éclaté (ex: 12 régions) introduit une variance locale forte (petites régions = données bruitées). Meridian peut doper mathématiquement certains paramètres pour étouffer ce bruit, au détriment de la vérité métier.

### Piège 1 : "Fake Baseline" et Adstock infini sur le Search
Dans un modèle Geo, Meridian déteste la variance régionale inexpliquée. S'il trouve un canal "pull" continu tout au long de l'année (ex: Google Search) très corrélé à la taille de la région, il aura tendance à **lisser l'Adstock à l'extrême (Alpha > 0.95, demi-vie de 50 semaines)**.
- **Symptôme** : La Baseline organique chute sous les 30%, et le Search capture >50% de la contribution.
- **Solution ("Hard Constraint")** :
  1. Utiliser un `max_lag` global bas (4-8) et un **Prior d'Alpha restrictif** (ex: `Beta(1, 3)`) pour les canaux Search/Performance. Note : `max_lag` est un int global, pas configurable per-channel.
  2. Resserrer le prior `Total Media Contribution` (ex: `p_mean=0.15` au lieu de `0.25`) pour forcer le modèle à chercher l'organique.

### Piège 2 : L'Oubli du "Population Scaling"
À l'échelle nationale, une variable binaire `is_holiday` fonctionne bien. En Geo-Level, appliquer un coefficient "National" sur une région qui pèse 2% de la population va détruire l'attribution (le Baseline s'effondre pour absorber l'asymétrie).
- **Critique** : TOUTES les variables de contrôle qui ne sont pas des ratios/index doivent passer par le **Population Scaling**.
- **Implémentation** : 
  Dans `ModelSpec`, utiliser un array booléen numpy (ex: `True` pour les Vacances, `False` pour le GQV qui est déjà un index 0-100).
  ```python
  # ✅ Obligatoire en Geo-Level
  model_spec = spec.ModelSpec(
      control_population_scaling_id=np.array([True, True, False]),
      ...
  )
  ```

### Piège 3 : Retirer les "micro-canaux" bruyants
En Geo-Level, un canal avec très peu d'investissement (ex: YouTube Video à 8k€ sur 3 ans) éclaté sur 12 régions devient du pur bruit statistique. Le modèle peut lui attribuer un ROI aberrant (ex: 60) juste pour ajuster la variance d'une ou deux petites régions.
- **Règle d'or** : Regrouper (Meta + Snapchat = Social) ou exclure totalement les micro-canaux en Geo-Level. Ne garder que les signaux statistiques forts.

### Piège 4 : Mesurer l'impact des Contrôles (gamma_c)
Meridian traite les variables de contrôle comme des régresseurs log-linéaires (`gamma_c`). Pour mesurer leur impact métier (ex: "Le GQV génère +59% de conversions organiques") :
```python
# Extraction depuis l'objet inference_data
gamma_c = mmm.inference_data.posterior['gamma_c'].values
mean_gamma_c = np.mean(gamma_c, axis=(0,1))

# Impact % sur les ventes = exp(coefficient) - 1
idx_gqv = 5
impact_gqv = np.exp(mean_gamma_c[idx_gqv]) - 1
print(f"Impact de la variable de contrôle {idx_gqv} : {impact_gqv:+.1%}")
```

---

## 14. Migration depuis LightweightMMM

Guide officiel : https://developers.google.com/meridian/docs/migrate

Principales différences :
- Meridian utilise `InputData` + `ModelSpec` (vs dictionnaire LMMM)
- ROI comme paramètre natif (vs dérivé)
- Support R&F, organic media, non-media treatments
- GPU natif via TensorFlow Probability
- Optimiseur intégré avec scenario planning

---

## 15. Checklist Projet Meridian

### Phase 1 — Prémodélisation
- [ ] Collecter ≥ 2 ans de données hebdomadaires géo-level (ou 3 ans national)
- [ ] Demander accès MMM Data Platform (GQV + YouTube R&F)
- [ ] Préparer CSV avec colonnes : geo, time, kpi, population, media, spend, controls
- [ ] Effectuer EDA : corrélations, saisonnalité, outliers, VIF, données manquantes
- [ ] Décider kpi_type ('revenue' vs 'non-revenue')
- [ ] **Data needs** : vérifier ratio data points / effets (≥15 pour national, ≥8 pour géo)
- [ ] **Non-revenue** : choisir approche prior (Total Media Contrib, IKPC, ou Channel Contrib)

### Phase 2 — Modélisation
- [ ] Installer Meridian (GPU recommandé)
- [ ] Charger données via CsvDataLoader
- [ ] Configurer ModelSpec (priors, max_lag, knots, adstock_decay_spec)
- [ ] **Adstock par canal** : geometric (perf) vs binomial (awareness)
- [ ] Calibrer priors ROI avec expériences si disponibles (helpers `lognormal_dist_from_*`)
- [ ] Exécuter sample_prior() — vérifier P(neg baseline) < 5%, P(contrib > 100%) < 5%
- [ ] Exécuter sample_posterior() — 4 chaînes, 2000 samples
- [ ] Vérifier convergence (R-hat < 1.1)
- [ ] **Holdout** : définir holdout_id identique pour comparer les versions

### Phase 3 — Post-modélisation
- [ ] **ModelReviewer** : `from meridian.analysis.review import reviewer` → `reviewer.ModelReviewer(mmm).run()` → PASS/REVIEW/FAIL (⚠️ OOM si 10 chains local)
- [ ] Évaluer model fit (R², MAPE, expected vs actual)
- [ ] **Baseline** : vérifier positivité et saisonnalité attendue
- [ ] Analyser ROI, mROI, contribution par canal
- [ ] Examiner courbes de réponse et saturation
- [ ] Exécuter optimisation budget (fixed + flexible)
- [ ] Générer rapports HTML
- [ ] Sauvegarder modèle (.pkl)
- [ ] Planifier refresh (trimestriel recommandé)

---

## 16. Références & Papiers

| Papier | Sujet |
|--------|-------|
| Jin et al. 2017 | Geo-level Bayesian Hierarchical MMM |
| Sun et al. 2017 | Bayesian Methods for Media Mix Modeling |
| Zhang et al. 2023 | Incorporating Reach and Frequency Data |
| Ng et al. 2021 | Trend and Seasonality Modeling |
| Chan & Perry | Media Mix Model Calibration With Bayesian Priors |
| GeoX | Trimmed Match pour expériences géo |

---

## 17. Quick Reference — Code Patterns

### Pattern complet minimal

```python
# ====== ENV VARS (OBLIGATOIRE sur macOS) ======
import os
os.environ['TF_USE_LEGACY_KERAS'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import tensorflow as tf  # AVANT pandas !
import numpy as np
import pandas as pd

from meridian.data import load
from meridian.model import model, spec, prior_distribution
from meridian.analysis import optimizer, visualizer, summarizer
import tensorflow_probability as tfp
from meridian import constants

# 1. DATA
loader = load.CsvDataLoader(
    csv_path='data.csv',
    kpi_type='revenue',
    coord_to_columns=load.CoordToColumns(
        time='week', geo='region', kpi='sales',
        population='pop',
        media=['imp_tv', 'imp_social'],
        media_spend=['spend_tv', 'spend_social'],
        controls=['gqv'],
    ),
    media_to_channel={'imp_tv': 'TV', 'imp_social': 'Social'},
    media_spend_to_channel={'spend_tv': 'TV', 'spend_social': 'Social'},
)
data = loader.load()

# 2. MODEL
prior = prior_distribution.PriorDistribution(
    roi_m=tfp.distributions.LogNormal(0.2, 0.9, name=constants.ROI_M)
)
model_spec = spec.ModelSpec(prior=prior, enable_aks=True)
mmm = model.Meridian(input_data=data, model_spec=model_spec)

# 3. FIT (API v1.5.x)
mmm.sample_prior(n_draws=500)
mmm.sample_posterior(n_chains=10, n_adapt=2000, n_burnin=500, n_keep=1000)

# 4. DIAGNOSE (retourne des Altair charts)
diag = visualizer.ModelDiagnostics(mmm)
diag.plot_rhat_boxplot().save('rhat.html')

# 5. ANALYZE (Altair charts)
media = visualizer.MediaSummary(mmm)
media.plot_roi_bar_chart().save('roi.html')
media.plot_contribution_waterfall_chart().save('waterfall.html')

# 6. RAPPORT HTML (2 pages)
s = summarizer.Summarizer(mmm)
s.output_model_results_summary('report.html', './', start_date='2023-01-01', end_date='2025-12-31')

# 7. OPTIMIZE
budget_opt = optimizer.BudgetOptimizer(mmm)
opt = budget_opt.optimize()
opt.output_optimization_summary('optim.html', './')

# 8. SAVE
model.save_mmm(mmm, 'meridian_model.pkl')
```

---

## Références & Documentation Fraîche

- [Meridian GitHub](https://github.com/google/meridian)
- [Meridian User Guide](https://developers.google.com/meridian/docs/basics/user-guide)
- [Meridian Data Requirements](https://developers.google.com/meridian/docs/basics/data-requirements)
- [Meridian Prior Selection](https://developers.google.com/meridian/docs/advanced-modeling/set-prior)
- [Meridian Scenario Planner](https://developers.google.com/meridian/docs/optimization/scenario-planner)
- [Google Query Volume (GQV)](https://developers.google.com/meridian/docs/data-prep/collect-gqv)
- [Meridian Colab Notebooks](https://github.com/google/meridian/tree/main/notebooks)

> [!TIP]
> Pour explorer la documentation Meridian à jour :
> ```
> search_documents("Google Meridian MMM marketing mix modeling installation")
> search_documents("Meridian data requirements media geo time series")
> search_documents("Meridian budget optimization scenario planner")
> search_documents("Meridian prior selection ROI adstock hill function")
> ```
