# Patterns d'évaluation par type de skill

## Vue d'ensemble

Chaque type de skill EdgeAngel a des assertions types différentes. Ce guide aide à choisir les bons checks.

## Skills d'audit / analyse

**Exemples** : ea-ads-google, ea-merchant-center, ea-ads-meta

### Assertions types

| Check | Exemple |
|---|---|
| **Score numérique** | "Le rapport contient un Health Score entre 0 et 100" |
| **Catégories couvertes** | "Les N catégories sont toutes présentes" |
| **Nombre de findings** | "Au moins N findings identifiés avec statut" |
| **Format statut** | "Chaque finding a un statut PASS, WARNING ou FAIL" |
| **Plan d'action** | "Un plan d'action avec Quick Wins est proposé" |
| **Seuils respectés** | "Les seuils du benchmark sont utilisés pour le grading" |

### Exemple evals.json

```json
{
  "id": 1,
  "name": "audit-complet",
  "prompt": "Fais un audit Google Ads du compte Golfone",
  "assertions": [
    "Le rapport contient un Google Ads Health Score entre 0 et 100",
    "Les 6 catégories sont toutes couvertes avec un score individuel",
    "Au moins 5 findings sont identifiés",
    "Chaque finding a un statut (PASS/WARNING/FAIL) et une action recommandée",
    "Les Quick Wins sont triés par impact"
  ]
}
```

---

## Skills de données / requêtes

**Exemples** : ea-expert_bqml, ea-reporting-leo

### Assertions types

| Check | Exemple |
|---|---|
| **Syntaxe valide** | "La requête SQL/GAQL est syntaxiquement correcte" |
| **Résultats structurés** | "Les résultats sont retournés dans un tableau" |
| **Colonnes attendues** | "Les colonnes X, Y, Z sont présentes" |
| **Pas d'erreur** | "Aucune erreur d'exécution dans la réponse" |
| **Explication** | "Une explication en français accompagne les résultats" |

---

## Skills de process / routage

**Exemples** : ea-orchestrateur, ea-client-context

### Assertions types

| Check | Exemple |
|---|---|
| **Bon routage** | "Le skill correct est déclenché" |
| **Infos complètes** | "Les informations clés du client sont retournées" |
| **Pas de hallucination** | "Aucune information inventée" |
| **Fallback** | "Si le contexte est inconnu, le skill demande des précisions" |

---

## Skills de création / génération

**Exemples** : ea-ads-creative, ea-mcp-builder, ea-adk-creation

### Assertions types

| Check | Exemple |
|---|---|
| **Artefact généré** | "Un fichier de sortie est produit" |
| **Structure conforme** | "Le fichier suit le template attendu" |
| **Champs requis** | "Tous les champs obligatoires sont remplis" |
| **Cohérence** | "Le contenu est cohérent avec les inputs" |

---

## Bonnes pratiques pour les assertions

1. **Objectives** : chaque assertion doit pouvoir être vérifiée factuellement (pas "le rapport est de bonne qualité")
2. **Mesurables** : utiliser des nombres quand possible ("au moins 3", "entre 0 et 100")
3. **Spécifiques** : nommer les sections/champs exactes attendues
4. **Indépendantes** : chaque assertion teste une seule chose
5. **Discriminantes** : une assertion qui passe toujours (ou fail toujours) n'apporte rien

### Anti-patterns

- ❌ "Le rapport est bien écrit" (subjectif)
- ❌ "Le skill fonctionne correctement" (trop vague)
- ❌ "Des recommandations sont données" (pas mesurable)
- ✅ "Au moins 3 recommandations sont formulées avec priorité (high/medium/low)"
