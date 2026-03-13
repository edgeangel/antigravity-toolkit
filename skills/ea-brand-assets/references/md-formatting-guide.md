# Guide de formatage Markdown pour export PDF

Ce guide décrit le format attendu d'un document Markdown pour un export PDF professionnel
via le pipeline Pandoc + WeasyPrint.

## Structure du document

### Header (métadonnées → cover page)

Le script utilise les premiers éléments du MD pour construire la page de garde.
Le contenu avant le premier `---` horizontal rule est extrait pour la cover :

```markdown
# Titre Principal du Document

## Sous-titre ou description courte

**Nom du Client** — Interlocuteur (Fonction)
**Accompagnement** : EdgeAngel
**Date** : 12 mars 2026

---

## 1. Première section du corps...
```

### Règles des headings

| Niveau | Usage | Rendu PDF |
|--------|-------|-----------|
| `# H1` | Sections majeures | Gros titre dark, bordure bleue, saut de page |
| `## H2` | Sous-sections | Titre bleu, présent dans la TOC |
| `### H3` | Détails | Titre gris, pas dans la TOC |
| `#### H4` | Sous-détails | Petit titre gris italique |

**⚠️ Ne jamais mettre de bold/italic dans les headings :**
```markdown
# ❌ ## **Mon titre en gras**
# ❌ ## ***Mon titre en italique***
# ✅ ## Mon titre propre
```

### Séparateurs

Utiliser `---` entre les sections principales pour créer des filets visuels fins :
```markdown
## 1. Première section
Contenu...

---

## 2. Deuxième section
```

## Callout boxes (encarts)

Utiliser la syntaxe blockquote `>` pour les passages qui doivent se démarquer visuellement :

```markdown
> **V2 possible** : un agent IA pourrait automatiser cette étape
> en utilisant l'API de la plateforme.

> **Point d'attention** : cette approche nécessite une validation
> juridique préalable concernant le RGPD.

> **Livrable** : un rapport de cadrage au format PDF avec les
> recommandations détaillées et le chiffrage.
```

Labels recommandés pour les callouts :
- `**V2 possible**` — amélioration future
- `**Point d'attention**` — avertissement
- `**Note**` — information complémentaire
- `**Exemple**` — illustration concrète
- `**Livrable**` — ce qui sera produit
- `**L'enjeu**` — contexte stratégique

## Tableaux

Les tableaux sont automatiquement stylisés (headers bleu, zebra striping).
Conseils pour un bon rendu :

- **Limiter le nombre de colonnes** (5-6 max sur A4)
- **Texte concis** dans les cellules — le CSS gère le word-break
- Utiliser `**gras**` pour les lignes de total

```markdown
| Phase | Durée | Budget | Responsable |
|-------|-------|--------|-------------|
| POC | 2 mois | 5 000 € | EdgeAngel |
| Déploiement | 3 mois | 12 000 € | Client + EA |
| **Total** | **5 mois** | **17 000 €** | |
```

## Images

Les images doivent être dans le même répertoire que le fichier MD
ou dans un sous-répertoire relatif :

```markdown
![Description du diagramme](nom-du-fichier.png)
```

Le CSS force `max-width: 100%` — les images ne déborderont jamais.

## Ce qu'il faut éviter

| ❌ À éviter | ✅ Alternative |
|-------------|---------------|
| `## **Titre en gras**` | `## Titre sans formatage` |
| `## 1\. Numéro échappé` | `## 1. Numéro simple` |
| `# Section` suivi de `## Section` (doublon) | Un seul heading par section |
| Plus de 6 colonnes dans un tableau | Réduire ou scinder en 2 tableaux |
| Images en URL absolues | Utiliser des chemins relatifs |
