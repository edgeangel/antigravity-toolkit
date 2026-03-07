---
name: ea-mcp-usage
description: >
  Guide d'utilisation des MCPs (Model Context Protocol) disponibles. Centralise
  les subtilités, quirks, workarounds et bonnes pratiques de chaque MCP.
  Consulter ce skill quand un MCP ne fonctionne pas comme attendu, quand une
  requête API échoue, ou quand les résultats semblent incohérents. Ce skill
  s'enrichit au fil des usages. MCPs couverts : google-ads-gms, meta-ads,
  google-analytics, bigquery, merchant-center, notion-mcp-server,
  google-developer-knowledge, github-mcp-server.
  Triggers : "MCP error", "API issue", "GAQL", "query fail", "MCP bug",
  "incohérence données".
---

# MCP Usage — Guide & Troubleshooting

Ce skill est une **base de connaissances vivante** sur l'utilisation des MCPs. Il a 3 objectifs :

1. **Capitaliser les subtilités** : quand un MCP a un comportement inattendu, documenter le workaround ici
2. **Remonter les incohérences** : quand un MCP retourne des données incohérentes, **notifier l'utilisateur** avec un diagnostic clair pour améliorer le MCP
3. **Pousser à lire la doc** : quand un MCP résiste, utiliser `google-developer-knowledge` ou `github-mcp-server` pour chercher la doc officielle

## Réflexe debug MCP

Quand un appel MCP échoue ou retourne des résultats inattendus :

```
1. Vérifier les paramètres (types, formats, IDs)
2. Consulter ce skill → section du MCP concerné
3. Si pas de workaround connu → lire la doc via :
   - google-developer-knowledge → search_documents("sujet API")
   - github-mcp-server → get_file_contents (README du MCP)
4. Si incohérence confirmée → NOTIFIER L'UTILISATEUR :
   "⚠️ Incohérence détectée sur le MCP [nom] : [description].
    Ça peut être un bug du MCP ou une limitation de l'API.
    Recommandation : [action]"
```

## Réflexe documentation

Avant de contourner un problème, **toujours chercher la doc** :

| Besoin | Outil | Exemple |
|---|---|---|
| Doc API Google (Ads, Analytics, Merchant, Cloud) | `google-developer-knowledge` → `search_documents` | "Google Ads API campaign bidding" |
| Doc API complète d'une page | `google-developer-knowledge` → `get_document` | Utiliser le `parent` retourné par search |
| Code source du MCP | `github-mcp-server` → `get_file_contents` | Lire le README ou le code source |
| Doc GAQL spécifique | `google-ads-gms` → `get_gaql_doc` | Syntaxe GAQL complète |
| Champs disponibles dans un reporting view | `google-ads-gms` → `get_reporting_view_doc` | Liste des vues et metrics |

---

## Subtilités par MCP

### google-ads-gms

#### Basics

| Subtilité | Détail |
|---|---|
| `customer_id` | Digits uniquement, pas de tirets (ex: `7750228049` pas `775-022-8049`) |
| GAQL date format | `segments.date` au format `'YYYY-MM-DD'` avec quotes simples |
| Métriques incompatibles | Certaines métriques ne peuvent pas être dans la même query (ex: `search_impression_share` + `conversions` dans certains cas) |
| Pas de `LIMIT` sur certaines vues | Certaines vues resource ne supportent pas LIMIT dans GAQL |

#### Architecture MCC EdgeAngel

Le MCC (Manager Customer) principal est **EdgeAngel Consulting** : `7750228049`.

Le token OAuth du MCP est lié à ce MCC. Cela signifie que :
- **Le MCC peut être requêté directement comme `customer_id`** pour lister les sous-comptes
- **Les sous-comptes sont accessibles directement** avec leur propre `customer_id`, sans besoin de `login_customer_id`

#### Hiérarchie de comptes — Pattern de découverte

Pour lister tous les comptes sous le MCC EdgeAngel :

```sql
-- Requêter avec customer_id = 7750228049
SELECT
  customer_client.descriptive_name,
  customer_client.id,
  customer_client.status,
  customer_client.manager
FROM customer_client
WHERE customer_client.status = 'ENABLED'
```

La vue `customer_client` retourne tous les sous-comptes (directs et indirects). Le champ `customer_client.manager` indique si c'est un sous-MCC (`true`) ou un compte publicitaire final (`false`).

**Comptes clients principaux (sous le MCC EdgeAngel) :**

| Client | customer_id | Type |
|---|---|---|
| Golf One 64 (Golfone) | `7751730476` | Compte ads |
| Chauffagiste Izi confort (EDF) | `6893971454` | Compte ads |
| EA pour CITEO | `1595306039` | Compte ads |
| 02 - Kiloutou España | `1002611386` | Compte ads |
| 03 - Kiloutou Polska | `3762274321` | Compte ads |
| 05 - Kiloutou Italia | `7397043900` | Compte ads |
| EdgeAngel - Website | `9123843844` | Compte ads |

#### ⚠️ Bug connu : `login_customer_id`

Le paramètre `login_customer_id` du MCP souffre d'un **bug Pydantic** : la valeur numérique est castée en `int` au lieu d'être gardée en `string`, ce qui provoque une erreur de validation.

```
Error: Input should be a valid string [type=string_type, input_value=7750228049, input_type=int]
```

**Workaround :** ne PAS utiliser `login_customer_id`. Grâce au token OAuth lié au MCC, tous les sous-comptes sont accessibles directement en passant leur `customer_id`. Ce workaround fonctionne pour toute la hiérarchie EdgeAngel.

#### Outils de doc intégrés

**Quand ça galère :** `get_gaql_doc` + `get_reporting_view_doc` + `get_reporting_fields_doc`

### meta-ads

| Subtilité | Détail |
|---|---|
| `account_id` | Sans préfixe `act_` (ex: `2532104420345604`) |
| `date_preset` vs `time_range` | Utiliser l'un OU l'autre, jamais les deux |
| `actions` field | Retourne un tableau d'objets `{action_type, value}`, pas un scalaire |
| Breakdowns limités | Certaines combinaisons de breakdowns sont interdites par l'API |
| `search_ad_library` | Requiert `ad_reached_countries` obligatoire |
| Rate limiting | Pauses possibles sur comptes à gros volume |

**Quand ça galère :** `get_doc("insights")`, `get_doc("execute")`, `get_doc("targeting")`

### google-analytics

| Subtilité | Détail |
|---|---|
| `property_id` | Peut être un nombre ou `properties/XXXXX` |
| Dimensions vs métriques realtime | Les dimensions/métriques realtime sont différentes des standards |
| Custom dimensions | Préfixées `customUser:` ou `customEvent:` |
| Quotas | Attention aux quotas API — `return_property_quota: true` pour monitorer |

### bigquery

| Subtilité | Détail |
|---|---|
| Projet par défaut | `ia-initiatives` — toujours vérifier le projet |
| `execute_sql` | Pas de dry_run par défaut — attention aux queries coûteuses |
| `search_catalog` | Utile pour trouver des tables dont on ne connaît pas le nom exact |
| Forecast | Nécessite timestamp_col + data_col minimum |

**Voir aussi :** `ea-analyse-edgeangel` pour les pièges spécifiques à la vue `view_raw_daily_insight`

### merchant-center

| Subtilité | Détail |
|---|---|
| MCQL | Syntaxe propre (pas du SQL standard) — `get_doc("reports")` pour la doc |
| `product_name` | Format spécifique pour le `get` produit |
| Product Studio | Nécessite `account_id` explicite |

### notion-mcp-server

| Subtilité | Détail |
|---|---|
| `data_source` vs `database` | Les deux termes coexistent — `data_source` est le terme API v2025 |
| Blocks | Pagination max 100 par appel |
| Rich text | Format spécifique avec objets `{text: {content: "..."}}` |

### github-mcp-server

| Subtilité | Détail |
|---|---|
| `push_files` | Peut créer plusieurs fichiers en un seul commit |
| `create_or_update_file` | Requiert le `sha` du fichier existant pour une update |
| Search code | La query `q` suit la syntaxe GitHub search |

---

## Template de remontée d'incohérence

Quand une incohérence est détectée, utiliser ce template pour notifier l'utilisateur :

```
⚠️ INCOHÉRENCE MCP DÉTECTÉE

MCP : [nom du MCP]
Action : [tool appelé]
Paramètres : [params utilisés]
Résultat attendu : [ce qu'on attendait]
Résultat obtenu : [ce qu'on a eu]
Hypothèse : [bug MCP / limitation API / erreur paramètre]
Recommandation : [workaround ou action corrective]
```

Cela permet de constituer un historique pour améliorer les MCPs.
