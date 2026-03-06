---
name: orchestrateur
description: Orchestrateur agent interne. Point d'entrée pour orienter le LLM vers les bons skills et la bonne logique selon le contexte de la tâche. Consulter EN PREMIER pour toute tâche complexe.
---

# Orchestrateur Agent Interne EdgeAngel

> Point d'entrée central : guide l'agent vers le bon skill et le bon MCP selon la tâche.

---

## 1. Principe

**Lire ce skill EN PREMIER** pour toute tâche complexe impliquant :
- Plusieurs skills potentiels
- Un choix de MCP
- Un workflow multi-étapes

L'orchestrateur ne fait rien lui-même — il **route** vers le bon skill.

---

## 2. Matrice de Routage par Domaine

### 🎯 Ads — Audits & Analyses

| L'utilisateur veut... | Skill(s) à lire | MCP(s) à utiliser |
|---|---|---|
| Audit complet multi-plateforme | `ea-ads` (cadre) → `ea-ads-google` + `ea-ads-meta` | `google-ads-gms` + `meta-ads` + `google-analytics` |
| Audit Google Ads | `ea-ads` → `ea-ads-google` | `google-ads-gms`, `google-analytics` |
| Audit Meta Ads | `ea-ads` → `ea-ads-meta` | `meta-ads` |
| Audit créatif cross-plateforme | `ea-ads-creative` | `meta-ads` (ad library) |
| Audit landing pages | `ea-ads-landing` | Browser (navigation) |
| Veille concurrentielle | `ea-ads-competitor` | `meta-ads` (ad library), `google-ads-gms` (auction insights) |
| Audit Merchant Center / Shopping | `ea-merchant-center` | `merchant-center` |

> [!IMPORTANT]
> **Ordre de lecture pour un audit ads** : `ea-ads` (cadre + scoring) → skill plateforme spécifique → `ea-client-context` (si client connu).

### 🌐 EdgeAngel — Site Web & Contenu

| L'utilisateur veut... | Skill(s) à lire | MCP(s) |
|---|---|---|
| Travailler sur le site EdgeAngel | `ea-edgeangel-website` (routeur) | — |
| Créer/optimiser une page web | `ea-edgeangel-website` → `ea-edgeangel-website-pages` | — |
| Rédiger une Note d'Expert (blog) | `ea-edgeangel-website` → `ea-edgeangel-content-strategy` | — |
| Vérifier le ton / brand voice | `ea-edgeangel-brand-voice` | — |

> [!TIP]
> `ea-edgeangel-website` est lui-même un sous-orchestrateur qui route vers `website-pages` ou `content-strategy`. **Toujours lire `ea-edgeangel-brand-voice` AVANT** de produire du contenu.

### 📊 Reporting & Données Client

| L'utilisateur veut... | Skill(s) à lire | MCP(s) |
|---|---|---|
| Reporting mensuel client | `ea-reporting-leo` + `ea-client-context` | `google-ads-gms`, `meta-ads`, `google-analytics`, `bigquery` |
| Contexte / stratégie d'un client | `ea-client-context` | — |
| Analyse données BigQuery (EdgeAngel) | `ea-analyse-edgeangel` | `bigquery` |
| Requête GAQL Google Ads | `ea-mcp-usage` | `google-ads-gms` |
| Requête Google Analytics | `ea-mcp-usage` | `google-analytics` |

### 📈 Mesure & Modélisation

| L'utilisateur veut... | Skill(s) à lire | MCP(s) |
|---|---|---|
| Analyse contribution média (BQML) | `ea-expert_bqml_arima_plus_xreg` | `bigquery` |
| MMM complet (Meridian) | `ea-meridian-mmm` | `bigquery` |
| Restitution résultats MMM/contribution | `ea-restitution-mmm` | — |

> [!NOTE]
> **Framework de mesure EdgeAngel** :
> 1. **Causal Impact** (geo-lift) → incrémentalité ponctuelle
> 2. **ARIMA_PLUS_XREG** (BQML) → contribution continue, industrialisable
> 3. **Meridian** (bayésien) → MMM complet avec optimisation budgétaire

### 🛠️ Infrastructure & Développement

| L'utilisateur veut... | Skill(s) à lire | MCP(s) |
|---|---|---|
| Créer un agent ADK | `ea-adk-creation` | — |
| Déployer sur Agent Engine | `ea-agent-engine-deploy` | — |
| Déployer sur Cloud Run | `cloudrun-deploy` | — |
| Construire un MCP server | `ea-mcp-builder` | `google-developer-knowledge` |
| Résoudre un bug MCP | `ea-mcp-usage` | `google-developer-knowledge` |
| Containeriser (Docker) | `docker-expert` | — |
| Déboguer un problème complexe | `systematic-debugging` | — |
| Planifier une implémentation | `plan-writing` | — |

---

## 3. Matrice MCP

| MCP | Domaine | Skills associés |
|-----|---------|-----------------|
| `google-ads-gms` | Google Ads (GAQL) | `ea-ads-google`, `ea-ads-competitor`, `ea-reporting-leo` |
| `meta-ads` | Meta Ads (Facebook/Instagram) | `ea-ads-meta`, `ea-ads-creative`, `ea-ads-competitor`, `ea-reporting-leo` |
| `google-analytics` | GA4 | `ea-ads-google`, `ea-reporting-leo` |
| `bigquery` | BigQuery SQL | `ea-analyse-edgeangel`, `ea-expert_bqml_arima_plus_xreg`, `ea-meridian-mmm` |
| `merchant-center` | Google Merchant Center | `ea-merchant-center` |
| `google-developer-knowledge` | Documentation Google | `ea-mcp-builder`, `ea-mcp-usage`, tous les skills techniques |
| `github-mcp-server` | GitHub repos | `ea-adk-creation`, `ea-mcp-builder` |
| `notion-mcp-server` | Notion pages | `ea-reporting-leo` |
| `asana` | Gestion de projet | — (usage direct) |
| `piano-analytics-*` | Piano Analytics | — (usage direct, voir `ea-mcp-usage`) |

---

## 4. Règles de Routage

### Priorités

1. **Toujours lire le skill cible** avant d'agir — chaque skill a ses conventions critiques
2. **Un problème MCP ?** → Lire `ea-mcp-usage` en premier pour les quirks connus
3. **Contexte client disponible ?** → Toujours consulter `ea-client-context` avant un reporting ou audit
4. **Contenu EdgeAngel ?** → Toujours lire `ea-edgeangel-brand-voice` AVANT de rédiger
5. **Audit ads ?** → Toujours passer par `ea-ads` (cadre) avant le skill plateforme

### Escalade Documentation

Si un skill ne suffit pas pour répondre :
```
1. Lire le skill ea-* pertinent
2. Si données insuffisantes → consulter ea-mcp-usage pour les quirks MCP
3. Si doc technique manquante → utiliser google-developer-knowledge :
   search_documents("mot-clé pertinent")
4. Si bug MCP → documenter dans ea-mcp-usage pour enrichir le skill
```

### Incompatibilités

| ❌ Ne PAS faire | ✅ Faire plutôt |
|---|---|
| Mélanger les MCPs cross-domaine dans un même appel | Un MCP par domaine, séquentiellement |
| Produire du contenu EA sans lire brand-voice | Lire `ea-edgeangel-brand-voice` EN PREMIER |
| Lancer un audit ads sans le cadre | Lire `ea-ads` avant le skill plateforme |
| Appeler MMM pour un simple modèle BQML | Utiliser `ea-expert_bqml_arima_plus_xreg` |
| Ignorer le contexte client pour un reporting | Toujours consulter `ea-client-context` |

---

## 5. Arbre de Décision Rapide

```
L'utilisateur demande quoi ?
│
├─ Ads / Performance / Audit ?
│  ├─ Google Ads → ea-ads → ea-ads-google
│  ├─ Meta Ads → ea-ads → ea-ads-meta
│  ├─ Shopping / Merchant → ea-merchant-center
│  ├─ Créa / fatigue → ea-ads-creative
│  ├─ Landing page → ea-ads-landing
│  └─ Concurrents → ea-ads-competitor
│
├─ Site EdgeAngel / Contenu ?
│  ├─ Page web → ea-edgeangel-website → ea-edgeangel-website-pages
│  ├─ Blog / Note → ea-edgeangel-website → ea-edgeangel-content-strategy
│  └─ Brand voice → ea-edgeangel-brand-voice
│
├─ Reporting / Client ?
│  ├─ Reporting mensuel → ea-reporting-leo + ea-client-context
│  ├─ Données BQ → ea-analyse-edgeangel
│  └─ Contexte client → ea-client-context
│
├─ Mesure / Modélisation ?
│  ├─ Contribution média → ea-expert_bqml_arima_plus_xreg
│  ├─ MMM complet → ea-meridian-mmm
│  └─ Restitution → ea-restitution-mmm
│
├─ Technique / Dev ?
│  ├─ Agent ADK → ea-adk-creation
│  ├─ Deploy Agent Engine → ea-agent-engine-deploy
│  ├─ Deploy Cloud Run → cloudrun-deploy
│  ├─ MCP server → ea-mcp-builder
│  ├─ Docker → docker-expert
│  └─ Debug → systematic-debugging
│
└─ MCP qui bug ?
   └─ ea-mcp-usage → google-developer-knowledge
```
