# Anatomie d'un bon skill EdgeAngel

## Structure de fichiers

```
ea-<nom>/
├── SKILL.md              # Instructions principales (requis)
├── evals/                # Test cases (optionnel, créé par ea-skill-creator)
│   ├── evals.json        # Cas de test avec assertions
│   ├── grading.json      # Résultats du dernier eval
│   └── results/          # Outputs des exécutions
├── references/           # Docs chargées à la demande (optionnel)
│   ├── benchmarks.md
│   └── checklist.md
├── scripts/              # Scripts exécutables (optionnel)
└── assets/               # Templates, fichiers statiques (optionnel)
```

## Frontmatter YAML

```yaml
---
name: ea-<nom>
description: >
  <Ce que fait le skill>. MCPs utiles : <liste>.
  Use when user says "<triggers>".
---
```

### Règles pour `name`
- Préfixe `ea-` pour tous les skills EdgeAngel
- Minuscules, tirets pour séparer les mots
- Exemples : `ea-ads-google`, `ea-merchant-center`, `ea-mcp-usage`

### Règles pour `description`
- **Pushy** : le skill doit se déclencher même quand l'utilisateur ne le nomme pas
- Inclure les **MCPs utiles** pour que l'agent sache quels outils utiliser
- Inclure des **triggers explicites** : "Use when user says..."
- < 300 caractères idéal, < 500 max

Exemple pushy :
```
❌ "Analyse Google Ads"
✅ "Google Ads deep analysis covering Search, PMax, Display, YouTube.
    Use when user says 'Google Ads', 'PPC', 'search ads', 'PMax',
    or 'Google campaign'."
```

## Structure du SKILL.md

### Sections recommandées

1. **Liens** — Skills EA liés et MCPs nécessaires
2. **Process** — Étapes numérotées du workflow principal
3. **What to Analyze / What to Do** — Détail par catégorie
4. **Thresholds / Critères** — Seuils Pass/Warning/Fail (si audit)
5. **Output** — Format exact du livrable
6. **Deliverables** — Liste des artefacts produits

### Principes de rédaction

- **Impératif** : "Collecter les données via MCP" pas "Il faut collecter"
- **Expliquer le pourquoi** : chaque instruction doit avoir une raison
- **< 500 lignes** dans le SKILL.md — externaliser le reste en `references/`
- **Exemples concrets** : inclure des blocs Input/Output
- **Tables pour les seuils** : plus lisible qu'une liste

### Liens inter-skills

```markdown
## Liens
- **Cadre global** : `ea-ads` contient les quality gates transversaux
- **Contexte client** : `ea-client-context` si pertinent
- **MCPs** : `google-ads-gms` (GAQL queries), `google-analytics` (attribution)
```

## Conventions EdgeAngel

- **Langue** : SKILL.md en anglais ou français, au choix (mais cohérent)
- **Output** : les rapports livrables sont en français par défaut
- **MCPs** : toujours lister les MCPs dans le frontmatter ET dans les liens
- **Clients** : utiliser `ea-client-context` pour charger le contexte client
- **Orchestrateur** : pour qu'un skill soit routable, sa description doit contenir les bons triggers
