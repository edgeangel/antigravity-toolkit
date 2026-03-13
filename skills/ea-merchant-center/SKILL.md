---
name: ea-merchant-center
description: >
  Audit complet Google Merchant Center — flux produit, issues, performance Shopping.
  Use when user says "Merchant Center", "flux produit", "Shopping", "feed produit",
  "Google Shopping audit", "issues produit". Uses MCP: merchant-center.
---

# Merchant Center Audit Skill

> Méthodologie structurée pour auditer un compte Google Merchant Center et optimiser le flux produit.

> [!IMPORTANT]
> **Documentation fraîche Google** : Pour des informations à jour sur la Merchant API, utiliser le MCP `google-developer-knowledge` :
> ```
> search_documents("Google Merchant Center API product data quality feed optimization")
> search_documents("Merchant API sub-APIs overview")
> ```
> Google propose aussi un [MCP Merchant API devdocs](https://developers.google.com/merchant/api/guides/devdocs-mcp) accessible via endpoint RAG : `https://merchantapi.googleapis.com/devdocs/mcp/`

> [!TIP]
> **Nouveautés Merchant API (2025)** :
> - **Product Studio (ALPHA)** — GenAI pour optimiser titres/descriptions (sub-API dédiée, accès sur demande)
> - **Issue Resolution** — Accès programmatique au diagnostic et aux actions correctives (comme dans l'UI MC)
> - **Order Tracking** — Historique de suivi des commandes pour estimations livraison
> - **clickPotentialRank** normalisé entre 1 et 1000 (le rang le plus bas = le meilleur potentiel de clics)
> - **pageSize max** : passé de 250 à 1000 rows par appel API
> - Support **gRPC** en plus de REST

---

## Quand utiliser cette skill

- L'utilisateur demande un **audit Merchant Center** / Shopping / flux produit
- L'utilisateur veut **diagnostiquer** des problèmes de refus de produits
- L'utilisateur veut **optimiser** la performance de ses produits Shopping
- L'utilisateur veut vérifier la **santé** de son flux produit

---

## Prérequis

- Le MCP `merchant-center` doit être configuré et opérationnel
- L'utilisateur doit fournir (ou avoir configuré dans .env) :
  - Le **Merchant Center Account ID**
  - Un **service account** avec accès à la Merchant API

---

## Méthodologie d'Audit en 6 Étapes

### Étape 1 : Vérification d'accès & Infos compte

**Outil** : `get_account_info`

**Ce qu'on cherche** :
- Le nom du compte et sa configuration de base
- La timezone et la langue configurées
- Confirmer que l'accès API fonctionne

**Si erreur 403/401** → problème de permissions du service account. Vérifier :
- La Merchant API est activée dans le projet GCP
- Le service account a les droits sur le compte Merchant Center

---

### Étape 2 : Snapshot Santé Globale (CRITIQUE)

**Outil** : `get_product_statuses`

**C'est l'étape la plus importante de l'audit.** Elle donne en un appel :
- Le nombre de produits **actifs**, **en attente**, **refusés**, **expirants**
- La liste de toutes les **issues** avec leur sévérité et le nombre de produits impactés
- Le détail par **contexte** (Shopping Ads, Free Listings) et par **pays**

**Analyse attendue** :
| Métrique | Seuil d'alerte | Action |
|---|---|---|
| Taux de refus > 10% | 🔴 Critique | Investiguer les issues DISAPPROVED |
| Taux de pending > 5% | 🟡 Attention | Vérifier les feeds récents |
| Produits expirants > 0 | 🟡 Attention | Rafraîchir le feed |
| Issues DISAPPROVED | 🔴 Toujours traiter | Lister par nombre de produits impactés |

**Format de restitution** :
```
Santé du flux : XX% actifs | XX% refusés | XX% en attente | XX% expirants

Top 5 issues critiques :
1. [DISAPPROVED] missing_gtin — 450 produits affectés
2. [DISAPPROVED] missing_image — 120 produits affectés
...
```

---

### Étape 3 : Issues au Niveau Compte

**Outil** : `list_account_issues`

**Ce qu'on cherche** :
- Violations de politique au niveau du compte entier
- Problèmes de configuration (shipping, tax, etc.)
- Restrictions de destination

> **Important** : Les issues compte affectent TOUS les produits. Les traiter en priorité absolue.

---

### Étape 4 : Diagnostic des Feeds

**Outil** : `list_data_sources`

**Ce qu'on vérifie** :
- Combien de data sources sont configurées
- Type : Primary vs Supplemental
- Méthode d'upload : fetch URL, upload direct, API
- Dernière date de mise à jour réussie

**Red flags** :
- Feed primaire qui n'a pas été mis à jour depuis > 24h
- Pas de feed primaire configuré
- Erreurs de fetch (URL inaccessible)

---

### Étape 5 : Échantillon Qualité Produits

**Outil** : `list_products` (avec max_results=30)

**Analyser un échantillon de produits pour vérifier** :
- **Titre** : Est-il descriptif ? Contient-il la marque, le modèle, les attributs clés ?
- **Description** : Est-elle riche et informative ?
- **Images** : Y a-t-il des images ? Sont-elles de qualité ?
- **Prix** : Le prix est-il cohérent ? Pas de 0€ ou de prix anormaux ?
- **GTIN/EAN** : Le code-barres est-il renseigné ?
- **Disponibilité** : Correspond-elle au stock réel ?
- **Attributs manquants** : color, size, brand, etc.

**Scoring qualité** (sur 10) :
| Critère | Poids | Score |
|---|---|---|
| Titre optimisé | 2 | /2 |
| Description riche | 2 | /2 |
| Images présentes | 1 | /1 |
| GTIN renseigné | 2 | /2 |
| Prix cohérent | 1 | /1 |
| Attributs complets | 2 | /2 |

---

### Étape 6 : Intelligence Compétitive & Canaux

**Outils** : `get_price_competitiveness`, `get_competitive_visibility`, `list_programs`

**Analyse prix** :
- Utiliser `get_price_competitiveness` pour comparer les prix au benchmark marché
- 🔴 > +10% au-dessus du benchmark → prix non compétitif
- 🟢 < -10% en-dessous → bonne opportunité ou vérifier la marge
- 🟡 ±5% → aligné avec le marché

**Analyse visibilité** :
- Utiliser `get_competitive_visibility` pour identifier les concurrents directs
- Regarder le `relative_visibility`, `page_overlap_rate`, `higher_position_rate`
- Identifier les catégories où on est fort/faible vs concurrents

**Analyse canaux** :
- Utiliser `list_programs` pour voir les canaux actifs
- ✅ Shopping Ads, Free Listings → minimum à avoir actif
- 🟡 Free Local Listings → si inventaire magasin disponible
- 🟡 Buy on Google → si pertinent

---

## Phase Optimisation du Flux

> Après le diagnostic, passer en mode **optimisation proactive**.

### Étape 7 : Optimisation des Titres

**Outil** : `generate_text_suggestions`

**Best practices titres** :
- Front-loader : **Marque + Type produit + Attributs clés** (couleur, taille, genre)
- Les 70 premiers caractères sont les plus importants (troncature Shopping)
- Pas de MAJUSCULES, pas de texte promo, pas de prix dans le titre
- Variantes → chaque variante doit avoir un titre unique avec ses attributs

**Processus** :
1. Prendre un échantillon de 5-10 produits avec `list_products`
2. Appeler `generate_text_suggestions` pour chaque avec le titre actuel
3. Comparer les suggestions avec les best practices
4. Proposer un format de titre standardisé

### Étape 8 : Optimisation des Descriptions

**Outil** : `generate_text_suggestions`

**Best practices descriptions** :
- Utiliser les 5 000 caractères disponibles
- Front-loader les keywords importants dans les 180 premiers caractères
- Inclure : bénéfices produit, specs techniques, usage, matériaux
- Pas de HTML, pas de liens, pas de promo

### Étape 9 : Optimisation des Images

**Outil** : `enhance_product_image`

**Best practices images** :
- Minimum **800×800px** (idéal 1200×1200) pour Shopping classique
- **Images YouTube TV** : minimum 1200×1200 sinon warning `image_too_small_for_high_resolution`
- Fond blanc préféré, pas de watermark, pas de texte superposé
- Image = variante exacte (bonne couleur, bonne taille)

**Actions possibles** :
- `upscale` → augmenter la résolution (fix les warnings image_too_small)
- `remove_background` → détourage fond blanc propre
- `generate_background` → fond lifestyle/scène AI

### Étape 10 : Attributs Produit Complets

**Checklist attributs essentiels** :
| Attribut | Obligatoire | Impact SEO Shopping |
|---|---|---|
| `title` | ✅ | ⭐⭐⭐ |
| `description` | ✅ | ⭐⭐ |
| `image_link` | ✅ | ⭐⭐⭐ |
| `price` | ✅ | ⭐⭐⭐ |
| `gtin` | ⭐⭐ (fortement recommandé) | ⭐⭐⭐ |
| `brand` | ✅ | ⭐⭐ |
| `color` | Recommandé (apparel) | ⭐⭐ |
| `size` | Recommandé (apparel) | ⭐⭐ |
| `gender` | Recommandé (apparel) | ⭐ |
| `google_product_category` | Recommandé | ⭐⭐ |
| `product_type` | Recommandé (3+ niveaux) | ⭐⭐ |
| `additional_image_link` | Recommandé | ⭐ |

---

## Format de Restitution Finale

Le rapport d'audit doit contenir :

1. **Executive Summary** (3-4 phrases)
2. **Score de Santé** (% actifs, % refusés, par destination et pays)
3. **Issues Critiques** (classées par impact, avec plan d'action)
4. **Intelligence Compétitive** (positionnement prix, visibilité)
5. **Qualité du Flux** (scoring des attributs, suggestions d'optimisation)
6. **Canaux Actifs** (vs canaux potentiels)
7. **Plan d'Actions Prioritaires** (quick wins → moyen terme → stratégique)

**Ton** : Pragmatique, factuel, orienté action. Pas de jargon inutile.

---

## Erreurs Courantes à Éviter

| Erreur | Correction |
|---|---|
| Ignorer les issues `WARNING` | Elles peuvent devenir `DISAPPROVED` |
| Ne pas vérifier par pays | Un produit peut être actif en FR mais refusé en DE |
| Oublier les Free Listings | Vérifier le contexte `FREE_LISTINGS` en plus de `SHOPPING_ADS` |
| Juger la performance sans volume | Si < 100 impressions, pas significatif |
| Ne pas distinguer feed primaire vs supplemental | Le feed primaire est la source de vérité |
| Optimiser un titre sans contexte | Toujours passer brand + product_type à `generate_text_suggestions` |
| Upscaler toutes les images aveuglément | Trier par issue `image_too_small` d'abord |

---

## Références

- [Merchant API Overview](https://developers.google.com/merchant/api/overview)
- [Merchant API Latest Updates](https://developers.google.com/merchant/api/latest-updates)
- [Product data specification](https://support.google.com/merchants/answer/188494)
- [Merchant API devdocs MCP](https://developers.google.com/merchant/api/guides/devdocs-mcp)
- [Product Studio (ALPHA)](https://developers.google.com/merchant/api/release-notes/rest/product-studio)
- [Issue Resolution sub-API](https://developers.google.com/merchant/api/release-notes/rest/issueresolution)

> [!TIP]
> Pour approfondir un point spécifique pendant un audit :
> ```
> search_documents("Merchant Center product disapproval GTIN requirements")
> search_documents("Google Shopping free listings optimization")
> ```
