---
name: ea-analyse-olivier
description: >
  Framework complet d'analyse de performance acquisition selon la méthode Olivier / EdgeAngel.
  Couvre le cadrage, le workflow d'investigation (4 phases), les angles d'analyse, le mindset,
  ET le profil utilisateur d'Olivier (préférences, style de travail, patterns de décision).
  Use when user says "analyser la performance", "baisse de performance",
  "ROAS", "conversion drop", "audit performance", "pourquoi les conversions baissent",
  "diagnostic performance", "analyse acquisition", "pourquoi ça baisse",
  "comparer les périodes", "qu'est-ce qui se passe sur le compte",
  "profil olivier", "préférences", "comment olivier travaille".
  Always read ea-client-context for known clients. Uses MCPs: bigquery, google-analytics,
  google-ads-gms, meta-ads, merchant-center.
---

# Analyse de Performance Acquisition — Méthode Olivier / EdgeAngel

> **Skills liés** : `ea-analyse-edgeangel` (règles techniques BQ), `ea-client-context` (contexte client)
> **MCPs utiles** : `bigquery`, `google-analytics`, `google-ads-gms`, `meta-ads`, `merchant-center`
> **Patterns détaillés** : `references/analysis-patterns.md`

---

## 1. Environnement d'analyse

Avant toute analyse, préparer l'environnement de travail dans le workspace :

1. **Vérifier la workspace rule** : s'assurer que le fichier `{workspace}/.agents/rules/analyse-workspace.md` existe. S'il n'existe pas, le créer avec le contenu ci-dessous. Cette rule garantit la continuité et l'historisation entre les conversations.

    ```markdown
    ---
    trigger: always_on
    ---

    # Règles du Workspace Analyses

    ## Continuité et historisation

    À chaque nouvelle conversation d'analyse :

    1. **Identifier le client** concerné et son répertoire dans le workspace (`{nom-client}/`).
    2. **Charger le document de cadrage** (`{client}/cadrage_analyse.md`) pour récupérer le contexte, périmètre et IDs techniques.
    3. **Charger le dernier journal d'analyse** (`{client}/journal_analyse_YYYY-MM-DD.md`) pour reprendre le fil.
    4. Si aucun journal n'existe pour la date du jour, **en créer un nouveau**.

    ## Journal d'analyse

    - **Documenter toutes les avancées** dans le journal du jour pour conserver la mémoire des constats, hypothèses et conclusions même si la fenêtre de contexte est dépassée.
    - Chaque étape DOIT être datée et résumée.
    - Les requêtes SQL clés doivent être sauvegardées avec leurs résultats.

    ## Document de cadrage

    - Le `cadrage_analyse.md` est le document de référence durable pour une analyse client.
    - Il contient : contexte business, périmètre, IDs techniques, axes d'analyse, questions clés.
    - Il peut être enrichi au fil de l'analyse mais ne doit jamais être tronqué.

    ## Skills EdgeAngel

    - Utiliser les skills EdgeAngel disponibles en fonction du contexte de l'analyse.
    ```

2. **Identifier le client** et son répertoire (`{workspace}/{client}/`). Créer le répertoire si inexistant.
3. **Charger le document de cadrage** (`{client}/cadrage_analyse.md`). S'il n'existe pas, en créer un à partir du template ci-dessous.
4. **Charger le dernier journal d'analyse** (`{client}/journal_analyse_YYYY-MM-DD.md`). S'il n'en existe pas pour la date du jour, en créer un nouveau.
5. **Charger les skills EA pertinents** en fonction du contexte (BQ, Google Ads, Meta, Merchant Center, etc.).

### Template cadrage minimal

```markdown
# Cadrage Analyse — {Client}

## Contexte client
- **Client** : ...
- **Activité** : ...

## IDs techniques
| Plateforme | ID |
|---|---|
| ... | ... |

## Périmètre
- Période : ...
- Source de vérité : ...

## Question / Problématique
...

## Axes d'analyse
...
```

---

## 2. Cadrage de l'analyse

Poser les bases **avant de lancer la moindre requête**. Documenter dans le `cadrage_analyse.md`.

| Élément | Pourquoi |
|---|---|
| **Comptes et IDs** | Stocker les property ID, account ID, vues BQ pour ne pas les rechercher à chaque fois |
| **Outils / MCPs** | Définir quels MCPs utiliser (BQ, GA4, Google Ads, Meta, Merchant Center) |
| **Période** | N vs N-1, + mois adjacents pour le contexte de tendance |
| **Question formulée** | Formuler explicitement ce qu'on cherche à comprendre |
| **Source de vérité** | GA4, régie, back-office ? Poser d'entrée pour éviter les ambiguïtés |
| **Biais connus** | Modélisation GA4, attribution post-view, saisonnalité — les documenter |

**Validation** : sauf si l'utilisateur demande une analyse rapide, valider le cadrage avec lui avant de commencer. Même pour une analyse rapide, stocker les infos dans le cadrage.

---

## 3. Angles d'analyse et pistes

Avant de plonger dans les données :

1. **Recueillir les hypothèses de l'utilisateur** — il a souvent une intuition sur la cause.
2. **Proposer des pistes complémentaires** basées sur le contexte : saisonnalité, changements de setup, prix, concurrence, météo, stock.
3. **Prioriser les angles** — du plus probable au moins probable.
4. **Documenter** dans le cadrage la liste des angles retenus.

Voir `references/analysis-patterns.md` pour la bibliothèque de patterns d'analyse disponibles.

---

## 4. Workflow d'analyse

Workflow par défaut en 4 phases. **Modulable** selon la demande — adapter la profondeur au besoin.

### Phase 0 — Cadre

- Périmètre, définitions, sources, auteur
- Rappel des biais de mesure
- Question posée explicitement

### Phase 1 — Constat et problématique

Illustrer la problématique avec des **chiffres concrets** :

- **Tableau comparatif** : budget, conversions, CA, ROAS — N vs N-1
- **Graphique temporel** (hebdo ou quotidien) pour visualiser le point de bascule
- Identifier **où** et **quand** la variation se produit

> L'objectif de la Phase 1 est que n'importe quel lecteur comprenne le problème en 30 secondes.

### Phase 2 — Analyse

Dérouler les **angles principaux** répondant à la question, un par un :

- Avancer **angle par angle**, pas tout en même temps
- Chaque angle = une hypothèse + les données pour la valider ou l'invalider
- Donner la possibilité à l'utilisateur d'intervenir entre les angles
- Documenter chaque étape dans le journal d'analyse

### Phase 3 — Prise de hauteur

L'étape la plus importante et la plus souvent oubliée :

- **Vérifier la cohérence** : est-ce que les conclusions des différents angles convergent ?
- **Chercher ce qu'on n'a pas vu** : y a-t-il une piste qu'on n'a pas explorée ?
- **Analyser la période suivante** : si la tendance s'inverse sans changement → facteur contextuel confirmé
- **Lister les points à clarifier** avec le client

---

## 5. Exemples et spécifications d'analyse

Fiches condensées des analyses types les plus courantes. Pour les patterns avancés détaillés, voir `references/analysis-patterns.md`.

### Brand vs Non-Brand (SEA)

- Séparer les requêtes marque / générique / concurrents
- Le trafic brand est un indicateur de **demande** (pas de performance média)
- Si le brand chute, tout le reste est secondaire
- Attention PMax : utiliser `campaign_search_term_insight` (pas `search_term_view`)
- Identifier la cannibalisation : quel % du budget est consommé par la marque ?

### Mix funnel (Haut vs Bas de funnel)

- Comparer la répartition budgétaire entre campagnes Performance (bas) et Croissance (haut)
- Les campagnes haut de funnel ont un ROAS direct structurellement plus faible (post-view dominant, GA4 last-click aveugle)
- Un shift de budget Performance → Croissance fait mécaniquement baisser le ROAS global
- **Ne jamais juger une campagne haut de funnel sur le ROAS GA4 last-click**

### Variation produit entre 2 périodes

- Comparer les ventes par produit / catégorie entre N et N-1
- Identifier les shifts de mix produit (ex : accessoires vs machines)
- Calculer le prix unitaire réel : `itemRevenue / itemsPurchased` (event `purchase`)
- Un volume de ventes en hausse avec un CA plat = dégradation du mix produit (AOV en baisse)

### Waterfall GA4 (décomposition de la variation)

Décomposer la variation de CA en 3 facteurs multiplicatifs :

```
CA = Sessions × Taux de conversion × Panier moyen
```

- Si les sessions augmentent mais le taux de conversion baisse → trafic plus froid (dilution)
- Si le taux de conversion est stable mais le panier baisse → shift de mix produit
- Si les sessions baissent → problème de demande ou de budget

### Détection d'anomalie

- Tracer les KPIs en **quotidien ou hebdo** pour repérer les cassures
- Identifier la date exacte du point de bascule
- Corréler avec les changements de setup (campagnes activées/pausées, budgets modifiés)
- Si aucun changement de setup et la performance remonte → cause externe (saison, marché)

### Contexte météo et macro

- **Rechercher sur internet** les événements macro pouvant expliquer une variation : météo, actualité, événements sectoriels, jours fériés
- Pour les produits outdoor/saisonniers : la météo drive l'**intérêt** (température) mais la pluie bloque l'**activation** (achat)
- Comparer avec Google Trends pour valider la tendance de marché

### Prix et concurrence

- Vérifier les variations de prix du client (promos actives N-1 absentes en N ?)
- Utiliser le MCP `merchant-center` pour le **benchmark prix concurrent** (`price_competitiveness_product_view`)
- Un écart de prix de +25% vs benchmark peut transformer le site en showroom
- Les revendeurs (Darty, Boulanger, etc.) avec un prix inférieur captent la conversion

### Stock

- Vérifier si des produits phares sont en rupture → baisse mécanique du CA
- Sources possibles : events GA4 spécifiques (si implémentés), données client, contexte métier
- Signal GA4 indirect : hausse des vues produit sans add-to-cart = friction potentielle (rupture ou prix)

### Tunnel de conversion

Analyser le funnel complet :

```
view_item → add_to_cart → begin_checkout → purchase
```

- Calculer les taux de passage entre chaque étape
- Comparer N vs N-1 pour identifier **où** les utilisateurs décrochent
- Si `add_to_cart → purchase` est stable mais `view_item → add_to_cart` chute → problème d'offre/prix, pas de checkout
- Attention : certains sites n'implémentent pas `begin_checkout` (one-page checkout)

---

## 6. Mindset

### Principes non-négociables

- **Humilité** : « hypothèse la plus probable », « à valider avec le client ». On ne connaît pas tout le contexte. Pas de termes alarmistes ni d'emphase.
- **Factuel** : chaque assertion est appuyée par un chiffre. Pas de blabla sans preuve.
- **Pas de recommandation** si l'utilisateur ne l'a pas demandé. L'analyse est un diagnostic, pas une prescription.
- **Cohérence** : le livrable raconte une histoire logique, pas une collection de data points déconnectés.
- **Phrases qui ont du sens** : relire chaque conclusion et vérifier qu'elle apporte une info nouvelle.

### Ne pas être naïf

L'analyse de performance publicitaire est complexe car elle dépend de multiples facteurs interconnectés :

- **Type de campagne** : une campagne de génération de demande (haut de funnel) sera structurellement moins bien trackée en last-click qu'une campagne de captation (bas de funnel). Le ROAS direct n'a pas la même signification.
- **Audience** : conquérir un nouveau client coûte plus cher que reconvertir un client existant. Un ROAS en baisse peut refléter une acquisition saine.
- **Marge et LTV** : le ROAS brut ne tient compte ni de la marge produit ni de la valeur vie du client. Un ROAS de 3 peut être excellent ou catastrophique selon le secteur.
- **Attribution** : chaque source (GA4, régie Google, régie Meta) a raison dans son référentiel. Les écarts sont structurels, pas des bugs.
- **Le budget ne crée pas la demande — il la capte.** Doubler le budget en basse saison produit des rendements décroissants, pas un doublement des résultats.

Pour autant, les métriques comme le ROAS restent **indispensables** pour :
- Détecter les cassures de performance
- Piloter les campagnes au quotidien
- Avoir une vision mix média comparable

Le mindset : **utiliser les métriques comme des signaux, pas comme des verdicts.**

### Toujours chercher le N-1 atypique

Quand on dit « la performance baisse vs N-1 », la première question est : **est-ce que N-1 était normal ?** Un ROAS anormalement élevé peut s'expliquer par des concurrents en rupture de stock, une promo ponctuelle, ou un événement exceptionnel. Si N-1 est l'anomalie, la « baisse » est un retour à la normale.

### Connect the dots

Ne jamais analyser une métrique isolément. Croiser systématiquement : budget × saisonnalité × prix × concurrence × météo × stock × historique promo.

### Analyse ≠ Recommandation

Dans la phase d'analyse, rester sur le diagnostic pur. Proposer des actions uniquement si l'utilisateur le demande explicitement. Un diagnostic prématuré mène à des solutions naïves.

---

## Checklist avant livraison

- [ ] Le périmètre est clairement défini dans le cadrage
- [ ] Les biais de mesure sont documentés
- [ ] Le constat est illustré (tableau + graphique)
- [ ] Chaque angle est appuyé par des données
- [ ] La cohérence globale est vérifiée (Phase 3)
- [ ] Les points à clarifier avec le client sont listés
- [ ] Le journal d'analyse est à jour
- [ ] Le ton est factuel, humble, sans emphase

---

## 7. Profil Utilisateur — Olivier Chubilleau

> Enrichissement continu — proposer une mise à jour après chaque conversation significative.

### Identité & Rôle
- **Fondateur & CEO** d'EdgeAngel — double casquette stratège data + expert technique
- **Équipe** : petite structure agile (Olivier = Stratégie/IA/Tech, Paul = Business/Sales)

### Style de Travail
- Sessions longues et intenses (1-2h) > micro-tâches. Souvent le soir/week-end.
- Réponses directes et structurées — pas de superflu. Proactivité > passivité.
- Décide vite une fois la bonne information obtenue.
- Valorise la **scalabilité** : "est-ce que ça tient dans 6 mois ?"
- Itère sur du concret plutôt que de théoriser longtemps.
- Langue : **français** (technique OK en anglais).

### Préférences Techniques
- **Stack principale** : BigQuery, Google Ads API, Meta Ads API, GA4, Merchant Center
- **No-code** : Notion (reporting), Asana (gestion projet), Slack (comm)
- **Dev** : Python, SQL, Astro (site web), Docker
- **Philosophie** : open-source quand possible, Google Cloud en infrastructure

### Patterns Observés

> Format : `[Date] Pattern observé`

- `[2026-03-09]` Quand il explore un nouveau sujet, il veut d'abord un **benchmark exhaustif** avant de choisir
- `[2026-03-09]` Pense "système" : chaque outil doit s'intégrer dans l'écosystème global, pas être un silo
- `[2026-03-09]` Investit fortement dans l'infrastructure invisible (KIs, skills, rules) — levier multiplicateur
- `[2026-03-08]` Lors des sessions nocturnes, plus exploratoire et orienté R&D
- `[2026-03-08]` Teste systématiquement les limites d'un outil avant de l'adopter

