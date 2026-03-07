---
name: ea-skill-creator
description: >
  Create and evaluate Antigravity skills with structured test cases and grading.
  Use when user says "créer un skill", "nouveau skill", "tester un skill",
  "évaluer un skill", "skill quality", "evals", "améliorer un skill",
  or wants to verify that an existing skill produces correct outputs.
  Also use when the user wants to create test cases for a skill.
---

# EA Skill Creator

Skill pour créer et évaluer des skills Antigravity avec des cas de test structurés et du grading objectif.

## Deux modes d'utilisation

1. **Create** — Créer un nouveau skill depuis zéro avec ses test cases
2. **Evaluate** — Tester un skill existant et produire un rapport de qualité

Identifier le mode depuis le contexte de la conversation. Si l'utilisateur n'est pas clair, demander : "Tu veux créer un nouveau skill ou évaluer un skill existant ?"

---

## Mode Create

### Étape 1 — Capturer l'intention

Extraire du contexte de conversation :
1. **Quoi** : Que doit faire ce skill ? Quel est le livrable ?
2. **Quand** : Quels mots-clés ou contextes doivent le déclencher ?
3. **Format** : Quel format de sortie attendu ? (rapport MD, JSON, artefact...)
4. **MCPs** : Quels MCPs sont nécessaires ? (google-ads-gms, bigquery, notion...)
5. **Liens** : Quels autres skills EA sont liés ? (ea-client-context, ea-ads...)

Si la conversation contient déjà un workflow que l'utilisateur veut capturer, extraire les réponses du contexte. Sinon, poser les questions.

### Étape 2 — Interviewer sur les edge cases

Avant de rédiger, clarifier :
- Quels sont les cas limites ? (pas de données, accès refusé, client inconnu...)
- Y a-t-il des formats d'entrée différents ? (CSV, API, manuel...)
- Quels sont les critères de succès objectifs ?
- Le skill doit-il fonctionner pour plusieurs clients ou un seul ?

### Étape 3 — Rédiger le SKILL.md

Lire `references/skill-anatomy.md` pour les conventions EdgeAngel, puis rédiger :

```yaml
---
name: ea-<nom>
description: >
  <description pushy — inclure ce que fait le skill ET quand l'utiliser>
---
```

Principes de rédaction :
- **Expliquer le pourquoi** derrière chaque instruction, pas juste le quoi
- **Impératif** : "Collecter les données" pas "Il faut collecter les données"
- **< 500 lignes** dans le SKILL.md ; au-delà, externaliser en `references/`
- **Exemples concrets** : inclure des blocs Input/Output
- **Description pushy** : la description doit faire en sorte que le skill se déclenche même quand l'utilisateur ne le nomme pas explicitement

Structure recommandée du SKILL.md :
1. Liens (skills liés, MCPs)
2. Process (étapes numérotées)
3. What to Analyze / What to Do (détail des étapes)
4. Thresholds / Critères (si applicable)
5. Output (format du livrable)
6. Deliverables (liste des artefacts produits)

### Étape 4 — Créer les test cases

Créer `evals/evals.json` avec 3-5 prompts réalistes. Voir `references/schemas.md` pour le format exact.

Chaque prompt doit être :
- **Réaliste** — ce qu'un vrai utilisateur EA taperait
- **Varié** — mélanger formel/informel, cas simples/complexes
- **Avec assertions** — vérifications objectives et mesurables

Exemple de bons prompts :
- ✅ "Fais un audit Google Ads du compte Golfone, j'ai l'impression qu'on gaspille du budget"
- ✅ "Analyse les campagnes PMax de Golfone, est-ce qu'on utilise bien les asset groups ?"
- ❌ "Analyse un compte" (trop vague, pas réaliste)

Pour les assertions, penser en termes de checks **objectifs** :
- Le rapport contient un score numérique entre X et Y
- N sections spécifiques sont présentes
- Au moins N findings sont identifiés
- Le format de sortie est conforme au template

### Étape 5 — Valider la structure

Exécuter le script de validation :
```bash
python ~/.gemini/antigravity/skills/ea-skill-creator/scripts/validate_skill.py <chemin-du-skill>
```

Vérifier que tous les checks passent. Si ce n'est pas le cas, corriger avant de présenter à l'utilisateur.

---

## Mode Evaluate

### Étape 1 — Charger le contexte

1. Lire le SKILL.md du skill cible
2. Lire `evals/evals.json` du skill cible
3. Si pas d'evals.json, en créer un (basculer vers le mode Create, étape 4)
4. Lire `references/eval-patterns.md` pour adapter les patterns d'évaluation au type de skill

### Étape 2 — Exécuter chaque eval

Pour chaque eval dans `evals.json`, séquentiellement :

1. **Lire le skill cible** et comprendre ses instructions
2. **Exécuter le prompt** comme si c'était un utilisateur réel :
   - Appeler les MCPs nécessaires (google-ads-gms, bigquery, etc.)
   - Suivre les instructions du skill étape par étape
   - Produire le livrable attendu (rapport, artefact, etc.)
3. **Sauvegarder le résultat** dans `evals/results/eval-<ID>/output.md`

> **Important** : Exécuter le skill sérieusement, comme si c'était une vraie demande client. Ne pas simuler les appels MCP — les faire réellement si possible. Si impossible (pas d'accès), noter "(SIMULATED)" dans le résultat.

### Étape 3 — Grader

Pour chaque eval, évaluer chaque assertion :

```json
{
  "text": "Le rapport contient un Health Score entre 0 et 100",
  "passed": true,
  "evidence": "Ligne 5 du rapport: 'Google Ads Health Score: 72/100'"
}
```

Règles de grading :
- **Objectif** : chaque check doit être vérifiable factuellement
- **Evidence obligatoire** : citer l'extrait exact du résultat qui prouve pass/fail
- **Programmatique quand possible** : pour les checks structurels (présence de sections, format JSON), écrire un mini-script de vérification plutôt qu'évaluer à l'œil
- **Pas de jugement subjectif** : si une assertion est trop vague pour être graded objectivement, la noter et suggérer une reformulation

### Étape 4 — Analyser les patterns

Après le grading, identifier :
- **Assertions qui fail systématiquement** → instruction manquante ou pas claire dans le skill
- **Assertions qui pass toujours** → possiblement non-discriminantes, à durcir
- **Patterns récurrents** → le skill oublie-t-il systématiquement la même chose ?
- **Suggestions d'amélioration** classées par impact (high/medium/low)

### Étape 5 — Produire le rapport

Écrire `evals/grading.json` (voir `references/schemas.md` pour le format exact) avec :
- Pass rate par eval et global
- Evidence pour chaque assertion
- Suggestions d'amélioration

Présenter un résumé lisible à l'utilisateur :

```
📊 Évaluation de ea-ads-google

Eval 1 (audit Golfone) : 2/3 assertions passed (67%)
  ✅ Health Score présent
  ✅ 6 catégories couvertes
  ❌ Moins de 3 findings identifiés

Eval 2 (PMax analysis) : 3/3 assertions passed (100%)
  ✅ Section PMax Deep Dive
  ✅ Asset groups analysés
  ✅ Audience signals évalués

Pass rate global : 83% (5/6)

💡 Suggestions :
1. [HIGH] Ajouter instruction explicite : "identifier minimum 5 findings"
2. [MED] Préciser le format des findings : statut + description + action
```

---

## Références

- `references/schemas.md` — Schémas JSON pour evals.json et grading.json
- `references/skill-anatomy.md` — Conventions et anatomie d'un bon skill EA
- `references/eval-patterns.md` — Patterns d'évaluation par type de skill
