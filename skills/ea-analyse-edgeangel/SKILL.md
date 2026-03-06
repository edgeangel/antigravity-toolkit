---
name: ea-analyse-edgeangel
description: "Règles critiques pour analyser les données de performance acquisition EdgeAngel dans BigQuery (vue view_raw_daily_insight). Prévient les erreurs de jointure, d'agrégation et d'interprétation."
---

# Analyse EdgeAngel — Règles Critiques

> **Contexte client** : pour le contexte métier d'un client (stratégie, KPIs cibles, saisonnalité), consulter `ea-client-context` si pertinent.
> **MCP BigQuery** : en cas de problème avec les requêtes, consulter `ea-mcp-usage` pour les subtilités du MCP `bigquery`.

## 🚨 PIÈGE N°1 : La structure multi-platform par campagne

La vue `ia-initiatives.performance_acquisition_control.view_raw_daily_insight` contient **plusieurs lignes par jour par campagne**, issues de sources différentes dans la colonne `platform` :

### Clients Capture V2 (Allocab, Forge Adour, Blue Horse Group, MFI, Boutique 64)

La colonne `platform` = `COALESCE(pt_source, analytics_source)` produit :

| platform | Source | `cost` | `conversions_regie` | `revenue_regie` | `conversions_ga4` | `revenue_ga4` |
|:---|:---|:---|:---|:---|:---|:---|
| `google_ads` | Régie Google | ✅ Valeur | ✅ Valeur | ✅ Valeur | **= 0** | **= 0** |
| `bing_ads` | Régie Bing | ✅ Valeur | ✅ Valeur (souvent 0) | ✅ Valeur | **= 0** | **= 0** |
| `meta` | Régie Meta | ✅ Valeur | ✅ Valeur | ✅ Valeur | **= 0** | **= 0** |
| `google` | GA4 (source=google) | **= NULL** | **= 0** | **= 0** | ✅ Valeur | ✅ Valeur |
| `bing` | GA4 (source=bing) | **= NULL** | **= 0** | **= 0** | ✅ Valeur | ✅ Valeur |
| `fb` | GA4 (source=fb) | **= NULL** | **= 0** | **= 0** | ✅ Valeur | ✅ Valeur |

> **RÈGLE ABSOLUE** : Les métriques régie (cost, conversions_regie, revenue_regie) et les métriques GA4 (conversions_ga4, revenue_ga4) ne sont **JAMAIS sur la même ligne** pour les clients Capture V2. Elles sont sur des lignes `platform` différentes.

### Client Golfone (exception)

Golfone utilise une vue legacy `golfone64-data.capture_ai.analyse_raw_data` où le croisement régie/GA4 est **pré-calculé**. Une même ligne contient cost, conversions_regie ET conversions_ga4. Le `platform` = `link_source` (ex: `google_ads`, `bing_ads`, `meta`).

### Client Citeo (exception)

Citeo n'a **pas de données GA4**. Uniquement des données régie (`pt_source`). Pas de revenue.

---

## 🚨 PIÈGE N°2 : Jointures campagnes entre semaines

### ❌ NE JAMAIS FAIRE

```sql
-- FAUX : jointure many-to-many car une campagne a N lignes platform
FROM (SELECT * FROM campaign_data WHERE period = 'N') curr
FULL OUTER JOIN (SELECT * FROM campaign_data WHERE period = 'N-1') prev
  ON curr.campaign_name = prev.campaign_name
```

Cette jointure crée un **produit cartésien** : si une campagne a 4 lignes `platform` en N et 4 en N-1, on obtient 16 lignes au lieu de 4.

### ✅ TOUJOURS FAIRE

**Option A — Pré-agréger par (campaign_name, platform) puis joindre :**

```sql
FROM (SELECT * FROM campaign_data WHERE period = 'N') curr
FULL OUTER JOIN (SELECT * FROM campaign_data WHERE period = 'N-1') prev
  ON curr.campaign_name = prev.campaign_name
  AND curr.platform = prev.platform
```

**Option B (recommandée) — Agréger en consolidant régie + GA4 :**

```sql
WITH campaign_data AS (
  SELECT
    campaign_name,
    ea_campaign_category,
    CASE 
      WHEN platform IN ('google_ads', 'google') THEN 'Google'
      WHEN platform IN ('bing_ads', 'bing') THEN 'Bing'
      WHEN platform IN ('meta', 'fb', 'ig', 'an') THEN 'Meta'
      ELSE platform
    END AS platform_group,
    period,
    SUM(cost) AS cost,
    SUM(conversions_regie) AS conversions_regie,
    SUM(revenue_regie) AS revenue_regie,
    SUM(conversions_ga4) AS conversions_ga4,
    SUM(revenue_ga4) AS revenue_ga4
  FROM ...
  GROUP BY 1, 2, 3, 4
)
```

En groupant `google_ads` + `google` dans un même `platform_group`, on fusionne les métriques régie et GA4 en une seule ligne (car SUM de 0 + valeur = valeur).

---

## 🚨 PIÈGE N°3 : Agrégation au niveau client

Pour le tableau de synthèse hebdomadaire au niveau client, **PAS de problème** : un simple `GROUP BY client, period` avec `SUM()` fonctionne correctement car :
- `SUM(cost)` ne prend que les lignes régie (les lignes GA4 ont cost = NULL, ignoré par SUM)
- `SUM(conversions_ga4)` ne prend que les lignes GA4 (les lignes régie ont conversions_ga4 = 0)

Le problème ne survient **qu'au drill-down campagne** quand on fait des jointures N vs N-1.

---

## Requête de drill-down correcte (template)

```sql
WITH week_bounds AS (
  SELECT 
    DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 WEEK), WEEK(MONDAY)) AS week_n_start,
    DATE_ADD(DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 WEEK), WEEK(MONDAY)), INTERVAL 6 DAY) AS week_n_end,
    DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 2 WEEK), WEEK(MONDAY)) AS week_n1_start,
    DATE_ADD(DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 2 WEEK), WEEK(MONDAY)), INTERVAL 6 DAY) AS week_n1_end
),
campaign_data AS (
  SELECT 
    v.campaign_name,
    v.ea_campaign_category,
    -- Grouper régie + GA4 dans le même platform_group
    CASE 
      WHEN v.platform IN ('google_ads', 'google') THEN 'Google'
      WHEN v.platform IN ('bing_ads', 'bing') THEN 'Bing'
      WHEN v.platform IN ('meta', 'fb', 'ig', 'an') THEN 'Meta'
      ELSE v.platform
    END AS platform_group,
    CASE 
      WHEN v.date BETWEEN wb.week_n_start AND wb.week_n_end THEN 'N'
      WHEN v.date BETWEEN wb.week_n1_start AND wb.week_n1_end THEN 'N-1'
    END AS period,
    SUM(v.cost) AS cost,
    SUM(v.conversions_regie) AS conversions_regie,
    SUM(v.revenue_regie) AS revenue_regie,
    SUM(v.conversions_ga4) AS conversions_ga4,
    SUM(v.revenue_ga4) AS revenue_ga4
  FROM `ia-initiatives.performance_acquisition_control.view_raw_daily_insight` v
  CROSS JOIN week_bounds wb
  WHERE v.client = '{CLIENT_NAME}'
    AND v.is_managed_campaign = TRUE
    AND v.date BETWEEN wb.week_n1_start AND wb.week_n_end
  GROUP BY 1, 2, 3, 4
)
SELECT 
  COALESCE(curr.campaign_name, prev.campaign_name) AS Campagne,
  COALESCE(curr.ea_campaign_category, prev.ea_campaign_category) AS Categorie,
  COALESCE(curr.platform_group, prev.platform_group) AS Plateforme,
  ROUND(curr.cost) AS Cout_N,
  ROUND(prev.cost) AS Cout_N1,
  ROUND((curr.cost - prev.cost) / NULLIF(prev.cost, 0) * 100, 1) AS Evol_Cout_pct,
  ROUND(curr.conversions_regie, 1) AS Conv_Regie_N,
  ROUND(prev.conversions_regie, 1) AS Conv_Regie_N1,
  ROUND(curr.conversions_ga4, 1) AS Conv_GA4_N,
  ROUND(prev.conversions_ga4, 1) AS Conv_GA4_N1,
  ROUND((curr.conversions_ga4 - prev.conversions_ga4) / NULLIF(prev.conversions_ga4, 0) * 100, 1) AS Evol_Conv_GA4_pct,
  ROUND(SAFE_DIVIDE(curr.revenue_ga4, curr.cost), 2) AS ROAS_GA4_N,
  ROUND(SAFE_DIVIDE(prev.revenue_ga4, prev.cost), 2) AS ROAS_GA4_N1
FROM (SELECT * FROM campaign_data WHERE period = 'N') curr
FULL OUTER JOIN (SELECT * FROM campaign_data WHERE period = 'N-1') prev
  ON curr.campaign_name = prev.campaign_name
  AND curr.platform_group = prev.platform_group
ORDER BY COALESCE(curr.cost, 0) DESC
LIMIT 15
```

---

## Mapping GA4 Property IDs par client

| Client | GA4 Property ID | Nom de la propriété |
|:---|:---|:---|
| Allocab | `152840252` | [01] - Allocab Passenger - Web + App |
| Forge Adour | `434129234` | 01 - www.forgeadour.com |
| Blue Horse Group | `280091548` | 01 - Cheval Energy |
| MFI | `356241191` | 01 - Maformationimmo (MFI) |
| Boutique 64 | `338082520` | 01 - www.64.eu |
| Golfone | `313585219` | 01 - Golf One 64 |
| Citeo | ❌ | Pas d'investigation GA4 (pas de revenue) |

---

## Particularités par client

| Client | Données disponibles | Notes |
|:---|:---|:---|
| **Allocab** | Coût, Conv Régie, Conv GA4, Revenue | Web + App. Les conversions `purchase` GA4 sont attribuées via `analytics_source`. |
| **Forge Adour** | Coût, Conv Régie, Conv GA4, Revenue | E-commerce. Attention aux doublons Meta dans conversions régie. |
| **Blue Horse Group** | Coût, Conv Régie, Conv GA4, Revenue | E-commerce (Cheval Energy). Même remarque doublons Meta. |
| **MFI** | Coût, Conv Régie, Conv GA4, Revenue | E-commerce formation immo. Filtre régie = `%transaction%` uniquement. |
| **Boutique 64** | Coût, Conv Régie, Conv GA4, Revenue | E-commerce mode. Source = `production_v3`. |
| **Golfone FR/ES/BE** | Coût, Conv Régie, Conv GA4, Revenue | ⚠️ Vue legacy pré-croisée. Pas d'impressions/clics. Split pays par nom de campagne. |
| **Citeo** | Coût, Conv Régie UNIQUEMENT | App installs. Pas de GA4, pas de revenue. Ne pas investiguer en GA4. |

---

## Calcul des KPIs

| KPI | Formule | Périmètre |
|:---|:---|:---|
| **ROAS Régie** | `SUM(revenue_regie) / SUM(cost)` | `is_managed_campaign = TRUE` |
| **ROAS GA4 Attribué** | `SUM(revenue_ga4) / SUM(cost)` | `is_managed_campaign = TRUE` |
| **Mix ROAS** | `SUM(revenue_ga4 total) / SUM(cost managed)` | Numérateur = TOUT le trafic, dénominateur = managed only |
| **CPA** | `SUM(cost) / SUM(conversions)` | SAFE_DIVIDE |

> **Attention** : `cost` est NULL (pas 0) sur les lignes GA4. Utiliser `SUM()` qui ignore les NULL, ou `SAFE_DIVIDE`.

---

## Checklist avant analyse

1. [ ] Vérifier si le client est **Capture V2** ou **legacy** (Golfone)
2. [ ] Pour tout drill-down campagne : **toujours grouper par `platform_group`** (ou joindre sur platform)
3. [ ] Ne **jamais** joindre uniquement sur `campaign_name` sans `platform`
4. [ ] Utiliser `SUM()` pour agréger (gère automatiquement les NULL de cost)
5. [ ] Afficher `n/a` et non `0` quand une valeur est NULL
6. [ ] Pour Citeo : ne pas chercher de GA4 ni de revenue
7. [ ] Pour Golfone : les données sont déjà croisées, pas de piège multi-platform
