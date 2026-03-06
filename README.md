# 📚 Antigravity Toolkit — EdgeAngel

Boîte à outils centralisée pour [Antigravity](https://www.google.com/antigravity) chez EdgeAngel.

> **Companion repo de [mcp-registry](https://github.com/edgeangel/mcp-registry)** : les MCPs connectent l'IA aux données, le Toolkit lui donne l'expertise pour les exploiter.

---

## Contenu du repo

| Dossier | Description | Statut |
|---------|-------------|--------|
| [`skills/`](./skills/) | Expertise métier packagée — audits, analyses, guidelines | ✅ 22 skills |
| `workflows/` | Procédures step-by-step réutilisables | 🔜 À venir |
| `prompts/` | Templates de prompts prêts à l'emploi | 🔜 À venir |

---

## Qu'est-ce qu'un Skill ?

Un **Skill** est un fichier de connaissances (Markdown) que l'IA d'Antigravity lit automatiquement quand la tâche le nécessite. Il contient :

- **L'expertise métier** : frameworks d'audit, checklists, scoring, bonnes pratiques
- **Les conventions** : vocabulaire, ton, workflow EdgeAngel
- **Le contexte** : données clients, saisonnalités, objectifs
- **Les liens** : vers les MCPs pertinents et la documentation Google

> 💡 Là où un MCP donne accès aux données (Google Ads, Meta, BigQuery…), le Skill dit à l'IA **comment les interpréter**.

---

## Catalogue des Skills

### 🎯 Ads — Audits & Analyses

> *Origine : skills ads open-source, optimisés et enrichis par EdgeAngel.*

| Skill | Description | MCPs utilisés |
|-------|-------------|---------------|
| `ea-ads` | Cadre transversal audit ads. Industry detection, quality gates, scoring. | — |
| `ea-ads-google` | Deep analysis Google Ads — 74 checks (Search, PMax, Display, YouTube, Demand Gen). | `google-ads-gms`, `google-analytics` |
| `ea-ads-meta` | Deep analysis Meta Ads — 46 checks (Pixel/CAPI, créas, structure, audiences). | `meta-ads` |
| `ea-ads-creative` | Audit créatif cross-plateforme. Fatigue créative, diversité formats. | `meta-ads` |
| `ea-ads-landing` | Audit landing pages post-clic. Message match, vitesse, mobile, CRO. | Browser |
| `ea-ads-competitor` | Veille concurrentielle : Ad Library Meta, Auction Insights Google. | `meta-ads`, `google-ads-gms` |
| `ea-merchant-center` | Audit Google Merchant Center. Product Studio, Issue Resolution. | `merchant-center` |

### 🌐 EdgeAngel — Site Web & Contenu

> *Créés par EdgeAngel. Notre ADN éditorial.*

| Skill | Description |
|-------|-------------|
| `ea-edgeangel-brand-voice` | ADN et identité éditoriale EdgeAngel. **Lire AVANT tout contenu.** |
| `ea-edgeangel-website` | Orchestrateur site web. Route vers pages ou contenu. |
| `ea-edgeangel-website-pages` | Guide pages transactionnelles. SEO, GEO, CRO. |
| `ea-edgeangel-content-strategy` | Guide rédaction Notes d'Expert (blog). |

### 📊 Reporting & Données Client

> *Créés par EdgeAngel. Framework reporting et contexte client.*

| Skill | Description | MCPs utilisés |
|-------|-------------|---------------|
| `ea-reporting-leo` | Reportings mensuels client. Template, indicateurs, narratif. | `google-ads-gms`, `meta-ads`, `google-analytics`, `notion` |
| `ea-client-context` | Fiches contextuelles par client : stratégie, objectifs, saisonnalités. | — |
| `ea-analyse-edgeangel` | Règles critiques pour l'analyse BigQuery. | `bigquery` |

### 📈 Mesure & Modélisation

> *Créés par EdgeAngel. Framework de mesure publicitaire.*

| Skill | Description | MCPs utilisés |
|-------|-------------|---------------|
| `ea-expert_bqml_arima_plus_xreg` | Guide ARIMA_PLUS_XREG dans BigQuery ML. Contribution média. | `bigquery` |
| `ea-meridian-mmm` | Guide complet Google Meridian (MMM bayésien). | `bigquery` |
| `ea-restitution-mmm` | Éléments de langage restitution MMM/contribution. | — |

### 🛠️ Infrastructure & Développement

> *Créés par EdgeAngel. Guides pour construire et déployer.*

| Skill | Description |
|-------|-------------|
| `ea-orchestrateur` | **Routeur central.** Matrice de décision skill/MCP. Lire EN PREMIER. |
| `ea-mcp-usage` | Subtilités et quirks de chaque MCP. Troubleshooting. |
| `ea-mcp-builder` | Guide construction de serveur MCP (Python/FastMCP, Cloud Run). |
| `ea-adk-creation` | Guide création agent ADK from scratch. |
| `ea-agent-engine-deploy` | Guide déploiement Vertex AI Agent Engine. |

---

## Installation dans Antigravity

### Étape 1 : Cloner le repo

```bash
git clone https://github.com/edgeangel/antigravity-toolkit.git /tmp/antigravity-toolkit
```

### Étape 2 : Copier les skills

```bash
cp -r /tmp/antigravity-toolkit/skills/ea-* ~/.gemini/antigravity/skills/
```

### Étape 3 : Vérifier

Dans Antigravity, demandez :

```
Quels skills EdgeAngel sont disponibles ?
```

### Mise à jour

```bash
cd /tmp/antigravity-toolkit && git pull
cp -r skills/ea-* ~/.gemini/antigravity/skills/
```

---

## ⚠️ Règles importantes

### ❌ Ne PAS modifier les skills `ea-*`

Les skills `ea-*` sont maintenus par l'équipe EdgeAngel. **Ne modifiez pas** les fichiers directement — vos modifications seraient écrasées à la prochaine mise à jour.

### ✅ Créer vos propres skills

Créez vos skills personnels avec un **préfixe personnel** (ex: `leo-`, `cam-`) :

```bash
mkdir ~/.gemini/antigravity/skills/leo-mon-skill/
cat > ~/.gemini/antigravity/skills/leo-mon-skill/SKILL.md << 'EOF'
---
name: leo-mon-skill
description: Mon skill personnalisé pour [usage].
---
# Mon Skill
[Contenu...]
EOF
```

### 💬 Partager vos feedbacks

Votre retour est **essentiel**. Utilisez les [Issues GitHub](https://github.com/edgeangel/antigravity-toolkit/issues) pour :

1. 🐛 **Signaler un problème** : résultats incorrects ou incomplets
2. 💡 **Proposer une amélioration** : checklist manquante, convention ambiguë
3. 🆕 **Demander un nouveau skill** : domaine non couvert, workflow récurrent

---

## Liens utiles

| Ressource | Lien |
|-----------|------|
| **MCP Registry** | [github.com/edgeangel/mcp-registry](https://github.com/edgeangel/mcp-registry) |
| **Antigravity** | [google.com/antigravity](https://www.google.com/antigravity) |
| **Contact** | Olivier Chubilleau — [Issues](https://github.com/edgeangel/antigravity-toolkit/issues) |
