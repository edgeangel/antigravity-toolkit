# Schémas JSON — EA Skill Creator

## evals.json

Fichier de test cases pour un skill. Placé dans `<skill>/evals/evals.json`.

```json
{
  "skill_name": "ea-ads-google",
  "evals": [
    {
      "id": 1,
      "name": "audit-complet-golfone",
      "prompt": "Fais un audit Google Ads du compte Golfone",
      "expected_output": "Un rapport GOOGLE-ADS-REPORT.md avec Health Score et findings",
      "assertions": [
        "Le rapport contient un Google Ads Health Score entre 0 et 100",
        "Les 6 catégories (Conversion Tracking, Wasted Spend, Account Structure, Keywords, Ads, Settings) sont couvertes",
        "Au moins 3 findings sont identifiés avec statut PASS, WARNING ou FAIL",
        "Un plan d'action est proposé avec des Quick Wins"
      ],
      "files": []
    },
    {
      "id": 2,
      "name": "analyse-pmax",
      "prompt": "Analyse les campagnes PMax de Golfone, est-ce qu'on utilise bien les asset groups ?",
      "expected_output": "Analyse PMax avec section asset groups et audience signals",
      "assertions": [
        "Une section PMax Deep Dive est présente",
        "Les asset groups sont analysés (diversité text/images/video)",
        "Les audience signals sont évalués",
        "Des recommandations PMax spécifiques sont formulées"
      ],
      "files": []
    }
  ]
}
```

### Champs

| Champ | Type | Requis | Description |
|---|---|---|---|
| `skill_name` | string | ✅ | Nom du skill évalué |
| `evals` | array | ✅ | Liste des cas de test |
| `evals[].id` | number | ✅ | Identifiant unique de l'eval |
| `evals[].name` | string | ✅ | Nom descriptif (slug) |
| `evals[].prompt` | string | ✅ | Le prompt utilisateur à tester |
| `evals[].expected_output` | string | ✅ | Description du résultat attendu |
| `evals[].assertions` | string[] | ✅ | Checks objectifs à vérifier |
| `evals[].files` | string[] | ❌ | Fichiers d'entrée nécessaires |

---

## grading.json

Résultat du grading. Produit par le mode Evaluate dans `<skill>/evals/grading.json`.

```json
{
  "skill_name": "ea-ads-google",
  "evaluated_at": "2026-03-07T15:30:00+01:00",
  "results": [
    {
      "eval_id": 1,
      "eval_name": "audit-complet-golfone",
      "expectations": [
        {
          "text": "Le rapport contient un Google Ads Health Score entre 0 et 100",
          "passed": true,
          "evidence": "Ligne 5: 'Google Ads Health Score: 72/100 (Grade: C+)'"
        },
        {
          "text": "Les 6 catégories sont couvertes",
          "passed": true,
          "evidence": "Sections trouvées: Conversion Tracking, Wasted Spend, Account Structure, Keywords, Ads, Settings"
        },
        {
          "text": "Au moins 3 findings identifiés",
          "passed": false,
          "evidence": "Seulement 2 findings avec statut explicite trouvés"
        }
      ],
      "pass_rate": 0.67
    }
  ],
  "summary": {
    "total_evals": 2,
    "total_assertions": 8,
    "passed_assertions": 6,
    "avg_pass_rate": 0.75
  },
  "suggestions": [
    {
      "priority": "high",
      "text": "Ajouter une instruction explicite pour lister minimum 5 findings avec statut"
    },
    {
      "priority": "medium",
      "text": "Préciser le format attendu des findings : [STATUT] Description + Action recommandée"
    }
  ]
}
```

### Champs grading

| Champ | Type | Description |
|---|---|---|
| `expectations[].text` | string | Description du check |
| `expectations[].passed` | boolean | Résultat pass/fail |
| `expectations[].evidence` | string | Extrait concret prouvant le résultat |
| `pass_rate` | number | Ratio 0-1 d'assertions passées par eval |
| `suggestions[].priority` | string | high / medium / low |
| `suggestions[].text` | string | Suggestion d'amélioration |

> **Important** : les champs `text`, `passed`, `evidence` sont les noms exacts à utiliser. Ne pas utiliser `name`/`met`/`details` ou d'autres variants.
