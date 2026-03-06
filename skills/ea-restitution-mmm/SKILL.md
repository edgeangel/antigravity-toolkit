---
name: restitution-mmm
description: Éléments de langage et guide éditorial pour rédiger du contenu de restitution d'analyses MMM ou contribution média. Ton pédagogique, humble, factuel. Destiné à des audiences non-techniques. Basé sur le template EdgeAngel Février 2026.
---

# Éléments de langage — Restitution MMM & Contribution Média

Guide éditorial pour produire du contenu de qualité lors de la restitution d'analyses de contribution média (MMM Meridian, ARIMA_PLUS_XREG, ou toute approche statistique de mesure d'incrémentalité).

---

## 1. Posture Éditoriale

### 1.1 Le principe fondamental

**On présente des faits. Si c'est clair, le client comprend tout seul.**

On ne fait JAMAIS l'interprétation à la place du client. On structure les données de manière limpide, on pose les bons encadrés "Insights", et le client tire ses propres conclusions. C'est plus puissant qu'une slide de recommandations surjouée.

### 1.2 Les 5 règles d'or

| # | Règle | En pratique |
|---|---|---|
| 1 | **Humilité avant tout** | On parle de « signaux », « ordres de grandeur », « tendances ». Jamais de certitudes absolues. |
| 2 | **Les faits parlent d'eux-mêmes** | Un CPIK de 11€ vs 15€ n'a pas besoin de 3 paragraphes pour convaincre. Le chiffre suffit. |
| 3 | **Pas de méthode Coué** | On ne dit pas « excellents résultats » ou « performance exceptionnelle ». On dit « le modèle indique que… ». |
| 4 | **Transparence sur les limites** | On expose les biais, les incertitudes et les questions ouvertes AVANT qu'on nous les pose. |
| 5 | **Pédagogie sans condescendance** | Expliquer simplement, mais ne jamais faire ressentir au client qu'il ne comprend pas. |

### 1.3 Le ton juste

| ✅ Ce qu'on fait | ❌ Ce qu'on ne fait pas |
|---|---|
| « Le modèle suggère que… » | « Le modèle prouve que… » |
| « Les données indiquent un signal sur… » | « On a découvert que… » |
| « L'intervalle de confiance est large, ce qui traduit une incertitude » | « On ne sait pas trop » |
| « Ordre de grandeur : environ X leads » | « Le Social génère exactement 42 884 leads » |
| « Corrélation identifiée, à confirmer par un test » | « Le Social cause directement X conversions » |
| On laisse le client conclure | On conclut à sa place avec emphase |

---

## 2. Vocabulaire Client

### 2.1 Glossaire de traduction

L'audience n'est pas technique. Chaque terme doit être traduit naturellement dans le texte, avec la définition intégrée au fil de la prose — PAS dans un glossaire formel.

| Terme technique | Comment le dire au client |
|---|---|
| MMM (Marketing Mix Modeling) | Analyse statistique de la contribution des investissements publicitaires |
| Baseline / Intercept | Le socle organique — les conversions qui arrivent sans aucune publicité (marque, saisonnalité, bouche-à-oreille) |
| Incrémentalité | Ce que la pub ajoute réellement, au-dessus du trafic naturel |
| CPIK | Coût Par Incrément de KPI — le coût réel pour obtenir un lead (ou une vente) qui **n'aurait pas existé** sans publicité |
| ROI incrémental | Retour sur investissement mesuré uniquement sur les conversions supplémentaires générées par la pub |
| Adstock | Effet mémoire — une pub ne s'arrête pas le jour où elle est diffusée, son impact persiste (de quelques jours pour le Search à plusieurs semaines pour la vidéo) |
| Half-life | Durée au bout de laquelle la moitié de l'effet publicitaire s'est dissipé |
| Intervalle de crédibilité (IC 90%) | Fourchette dans laquelle le vrai chiffre se situe avec 90% de probabilité |
| Hill / Saturation | Rendements décroissants — doubler un budget ne double pas les résultats |
| R² | Score de qualité du modèle — à quel point les prédictions collent à la réalité (100% = parfait) |
| Prior / Posterior | Hypothèse de départ (prior) vs ce que les données nous apprennent (posterior) |
| Convergence MCMC / R-hat | Vérification que le modèle a bien "convergé" vers une solution stable |
| Multicolinéarité | Deux canaux activés en même temps — difficile de séparer leurs effets individuels |
| GQV (Google Query Volume) | Volume de recherches Google dans une zone — sert à capturer l'intention naturelle des internautes |

### 2.2 Mots et expressions à utiliser

**Préférer** :
- « Le modèle identifie un signal… »
- « Les données suggèrent… »
- « L'analyse met en évidence… »
- « On observe une tendance… »
- « En ordre de grandeur… »
- « Le niveau de confiance est [élevé/modéré/à confirmer] »
- « L'intervalle de crédibilité indique que… »
- « Ce résultat est cohérent avec… » (quand triangulation)

**Éviter** :
- « Le modèle prouve… » / « On a prouvé… »
- « Excellents résultats » / « Performance remarquable »
- « Grâce à notre expertise… »
- « Il faut absolument… » / « Vous devez… »
- « Le Social est le meilleur canal » (dire plutôt « le canal le plus efficient sur cette période »)
- Tout superlatif non factuel

---

## 3. Structure Narrative

### 3.1 Arc en 5 actes

Chaque restitution suit cet ordre logique. Le client doit comprendre POURQUOI avant de voir les résultats.

```
ACTE 1 — LE CONSTAT (pourquoi le tracking classique est limité)
ACTE 2 — LA MÉTHODE (ce que le MMM apporte de différent)
ACTE 3 — LE PÉRIMÈTRE (données, dates, canaux, géographies)
ACTE 4 — LES RÉSULTATS (contribution + efficacité)
ACTE 5 — PERSPECTIVES & LIMITES (recul, caveats, prochaines étapes)
```

### 3.2 Acte 1 — Le constat : pourquoi le tracking classique est limité

**Objectif** : Poser le problème AVANT la solution. Le client doit comprendre pourquoi on a besoin de cette analyse.

**Messages clés** :
- Les outils analytics (GA4, pixels) reposent sur le **tracking post-clic** : ils attribuent la conversion au dernier clic identifié
- Ce modèle **sous-estime structurellement** les canaux qui créent la demande sans générer de clic direct (Social, Display, YouTube, TV)
- 4 facteurs aggravants : ITP/Safari (cookies 7j max), parcours fragmentés (multi-touch/multi-device), dépréciation des cookies tiers, consentement RGPD (~60% de visibilité)

**Exemple concret à utiliser** :
> « Un internaute voit une pub Meta le lundi, effectue ensuite une recherche Google le jeudi et convertit. Le tracking attribue **100% au Search**. Meta = 0% de crédit. »

**Encadré "Attribution Post-Clic"** (si slide visuelle) :
- Focalisé sur les dernières interactions
- Invisible sur les impressions (post-view)
- Limité aux environnements trackés
- → Favorise les leviers bas de funnel (intentionnistes)

### 3.3 Acte 2 — La méthode : ce que le MMM apporte

**Messages clés** :
- Approche **statistique, cookie-free** — ne dépend pas du tracking navigateur
- Analyse les **corrélations historiques** entre les variations de dépenses média et les variations de conversions
- Capture les **effets indirects** (post-view) et le **temps long** (adstock)
- Permet de reconstituer la **contribution réelle** de chaque canal, y compris ceux invisibles dans GA4

**Schéma de décomposition** (concept visuel) :
```
Conversions totales observées
├── 🔵 Socle organique (baseline) — tendance + saisonnalité + marque
├── 🟢 Contribution Canal 1 (Search)
├── 🟠 Contribution Canal 2 (Social Ads)
└── 🔴 Résiduel (bruit statistique)
```

**Ce qu'il faut dire sur l'adstock** (en langage simple) :
> « Le modèle tient compte du fait qu'une pub continue d'agir après sa diffusion. Par exemple, un clic Search a un effet quasi-immédiat, tandis qu'une impression Social a un effet qui persiste plusieurs jours voire semaines. »

### 3.4 Acte 3 — Le périmètre

Le périmètre doit être posé clairement et factuellement. Pas de narratif ici, juste des faits.

**Éléments à toujours mentionner** :
- Période analysée (dates début → fin)
- Nombre de semaines / granularité (hebdo)
- Nombre de géographies (si geo-level)
- Canaux média inclus (avec le détail de ce que chacun contient)
- Sources de données (GA4, Google Ads, Meta Ads, etc.)
- Variables de contrôle utilisées (vacances, GQV, concurrence…)
- Toute exclusion notable (ex : « TV non incluse car absence de données régionalisées »)

### 3.5 Acte 4 — Les résultats

#### Bloc A : Contribution au fil du temps

Graphique en aires empilées (stacked area) montrant la décomposition semaine par semaine :
- Baseline en gris
- Chaque canal en couleur distincte
- Ligne réelle superposée (pour montrer que le modèle « colle »)

**Encadré Insights** (à accompagner chaque graphique) :
- Résumer les 2-3 faits saillants en bullet points courts
- Toujours commencer par la baseline : « {X%} du KPI provient du socle organique »
- Puis la répartition média : « Le Search contribue à {Y%}, le Social à {Z%} »

#### Bloc B : Efficacité par canal (le tableau central)

Le CPIK est **le concept central** de la restitution. C'est le KPI le plus parlant pour un non-technique.

**Format du tableau** :

| Canal | CPIK | IC 90% | Persistance (Adstock) | Leads incrémentaux | IC 90% |
|---|---|---|---|---|---|
| Social Ads | **11 €** | [9 – 16 €] | ~5 sem (binomial) | 43K | [30K – 57K] |
| GAds Search | **15 €** | [7 – 42 €] | 2,4 sem (geometric) | 58K | [20K – 114K] |

**Comment commenter ce tableau** :
- Toujours noter quel canal est le plus efficient (CPIK le plus bas)
- Souligner la largeur de l'intervalle de confiance — un IC large = plus d'incertitude
- Expliquer POURQUOI un IC peut être large (ex : « ~30% des clics Search sont drivés par des requêtes de marque captives — le modèle a du mal à distinguer l'incrémental pur du trafic de marque →  d'où une confiance moindre sur le CPIK exact du Search »)

#### Bloc C : Graphique de contribution (horizontal bar)

Graphique en barres horizontales montrant la répartition :
- Baseline : X% (YM€)
- Canal 1 : X% (YM€)
- Canal 2 : X% (YM€)

Chaque barre indique le % ET le montant absolu en € (si revenue_per_kpi disponible).

### 3.6 Acte 5 — Perspectives & Limites

**C'est la slide la plus importante pour la crédibilité.** Un consultant qui pose ses limites avant qu'on les lui demande gagne plus de confiance qu'un vendeur qui affirme tout.

**Message d'ouverture obligatoire** :
> « Le MMM fournit des **ordres de grandeur et des tendances**, pas des chiffres exacts. Il peut comporter des biais car il identifie les corrélations entre les variations sur les dépenses et les résultats… mais **corrélation n'implique pas forcément causalité**. »

**Colonne "Les enseignements"** :
- Intervalles de crédibilité : « Les IC 90% sont plus resserrés pour le Social [9-16€] que pour le Search [7-42€]. Cela traduit une confiance plus élevée du modèle sur le Social. »
- Biais potentiel de marque : « Le modèle peut confondre l'incrémental Search pur avec le trafic de marque captif. »
- Qualité du modèle (R², MAPE) — résumé en 1-2 lignes, détail en annexe

**Colonne "Pour aller plus loin"** :
- Tests d'incrémentalité géographiques (couper les campagnes sur une zone témoin pendant 4-6 semaines)
- Itérations du modèle (ajout de variables, rerun avec plus de données)
- Raffinage des priors si nouvelles informations disponibles

---

## 4. Règles de Rédaction

### 4.1 Encadrés "Insights"

Chaque graphique ou tableau de résultats DOIT être accompagné d'un encadré "Insights" qui synthétise les 2-3 points clés. Ce sont ces encadrés que les gens lisent en premier.

**Format** :
> **Insights**
> - Le Social Ads (37% du budget → 14,4% des leads) affiche un CPIK de 11€, c'est le canal le plus efficient.
> - Le GAds Search est le premier en volume (19,8%) avec un CPIK de 15€.
> - L'intervalle de confiance du Search [7–42€] est beaucoup plus large que celui du Social [9–16€]. Le modèle a du mal à distinguer l'incrémental pur du trafic de marque captif.

**Règles** :
- Max 3 bullet points
- Chaque bullet = 1 fait + 1 donnée chiffrée
- Pas de jugement de valeur, pas de recommandation
- Le dernier bullet peut être une nuance / caveat

### 4.2 Niveaux de confiance

Toujours qualifier les résultats avec un niveau de confiance. Utiliser ces 3 niveaux :

| Niveau | Quand l'utiliser | Formulations |
|---|---|---|
| 🟢 **Signal fort** | IC resserré (ratio < 2x), cohérent avec d'autres sources | « Le modèle identifie un signal fort sur… » |
| 🟡 **Signal modéré** | IC moyen (ratio 2-5x), pas de contradiction flagrante | « Les données suggèrent… avec une incertitude modérée » |
| 🔴 **Signal faible / à confirmer** | IC très large (ratio > 5x), ou incohérence avec d'autres sources | « Le modèle donne une indication, mais la marge d'incertitude est importante — à valider par un test » |

**Le ratio de CI** : largeur IC / médiane. C'est le meilleur indicateur synthétique de confiance.

### 4.3 Formulations de caveat prêtes à l'emploi

À insérer selon le contexte :

**Sur la méthode** :
> « Cette analyse identifie des corrélations statistiques. Corrélation n'implique pas forcément causalité. Pour valider la causalité, des tests d'incrémentalité (de type geo-lift) sont recommandés. »

**Sur le Search / Brand** :
> « Le modèle peut avoir du mal à distinguer l'incrémental pur des requêtes Search de marque "captives" — c'est-à-dire des internautes qui auraient cherché la marque même sans publicité. L'intervalle de confiance large sur ce canal reflète cette incertitude. »

**Sur la baseline** :
> « Le socle organique représente {X%} de l'activité. C'est la force de la marque, la saisonnalité naturelle et l'effet bouche-à-oreille. C'est aussi un indicateur de la solidité du business en dehors de la publicité. »

**Sur les priors** :
> « Le modèle utilise des hypothèses de départ (priors) calibrées sur les benchmarks sectoriels et notre expérience. Les données ajustent ensuite ces hypothèses. Un prior ouvert (comme celui utilisé ici) laisse les données "parler" sans forcer de conclusion. »

**Sur les petits budgets** :
> « Lorsqu'un canal représente un faible pourcentage du budget total, le signal statistique est mécaniquement plus faible. L'intervalle de confiance sera naturellement plus large. »

---

## 5. Annexes Techniques

Les annexes sont réservées aux profils analytiques. Elles ne doivent JAMAIS apparaître dans le corps principal de la restitution.

### 5.1 Qualité du modèle

**Tableau de référence** :

| Métrique | Valeur obtenue | Benchmark | Interprétation client |
|---|---|---|---|
| R² (national) | {X} | > 0.80 | « Le modèle explique {X}% de la variance des conversions — score [excellent/bon/à améliorer]. » |
| MAPE (national) | {X}% | < 15% | « L'erreur moyenne de prédiction est de {X}% au niveau national. » |
| wMAPE | {X}% | < 15% | « L'erreur pondérée par le volume confirme que les prédictions sont fiables là où ça compte. » |
| P(baseline négatif) | {X}% | < 5% | « Il y a {X}% de probabilité que le modèle attribue plus de conversions aux médias qu'il n'en existe — [rassurant/à surveiller]. » |
| R-hat (convergence) | < 1.1 | < 1.1 | « Le modèle a bien convergé vers une solution stable. » |

### 5.2 MAPE geo-level vs national

**Phrase type pour expliquer un MAPE geo élevé** :
> « Le MAPE au niveau géographique individuel est mécaniquement plus élevé (~20-25%) car certaines régions à faible volume amplifient les erreurs relatives. Le wMAPE (pondéré par le volume) est dans les normes (~14-15%), ce qui confirme que les prédictions sont fiables là où les volumes sont significatifs. »

### 5.3 Paramètres du modèle

**Informations à lister en annexe** :
- Framework et version (ex : Meridian v1.5.1)
- Nombre de chaînes MCMC, samples
- Stratégie de prior (type, paramètres)
- Adstock par canal (type + max_lag)
- Variables de contrôle avec population scaling
- Holdout % et seed
- Temps d'exécution

---

## 6. Anti-patterns (ce qu'il faut absolument éviter)

| ❌ Anti-pattern | Pourquoi c'est problématique | ✅ Alternative |
|---|---|---|
| « Le modèle a des résultats excellents » | Jugement de valeur, le client peut douter | « Le R² de 96% indique que le modèle capture bien la dynamique des conversions » |
| « Le Social est clairement le meilleur canal » | Trop affirmatif, ignore les nuances (volume vs efficience) | « Le Social affiche le CPIK le plus bas (11€), ce qui en fait le canal le plus efficient en coût par lead incrémental sur cette période » |
| « Vous devez réallouer votre budget » | Directif, présomptueux | « Les données suggèrent qu'une réallocation pourrait améliorer l'efficience. Un test géographique permettrait de le confirmer. » |
| « Le Search ne marche pas » | Faux et réducteur | « L'intervalle de confiance du Search est large, ce qui reflète la difficulté à isoler l'incrémental pur des requêtes de marque captives. » |
| « Les résultats prouvent que… » | Le modèle ne prouve rien, il identifie des corrélations | « Les résultats indiquent que… » ou « Le modèle met en évidence que… » |
| Donner des chiffres exacts sans IC | Fausse précision, le client risque de les prendre au pied de la lettre | Toujours accompagner d'un IC : « 43K leads [30K – 57K] » |
| Cacher les limites en fin de présentation | Le client les découvre et doute de tout | Les poser en amont, en slide dédiée "Perspectives & Limites" |

---

## 7. Checklist Qualité Avant Livraison

Avant de livrer tout contenu de restitution, vérifier :

- [ ] Chaque résultat chiffré est accompagné d'un intervalle de confiance
- [ ] On parle de « signaux », « ordres de grandeur », « tendances » — jamais de « preuves »
- [ ] La distinction corrélation / causalité est posée explicitement
- [ ] Les limites sont exposées clairement (pas cachées en annexe)
- [ ] Le CPIK est défini en langage simple dès sa première mention
- [ ] Aucun superlatif injustifié (« excellent », « remarquable », « extraordinaire »)
- [ ] Les encadrés Insights contiennent max 3 bullets factuels
- [ ] Chaque canal est qualifié avec un niveau de confiance (fort / modéré / à confirmer)
- [ ] Le ton est factuel, pas commercial — les faits parlent d'eux-mêmes
- [ ] Les annexes techniques sont séparées du corps principal
- [ ] L'exemple concret « internaute voit Meta → recherche Google → convertit » est utilisé pour expliquer le biais post-clic
- [ ] Les prochaines étapes proposées incluent au moins un test d'incrémentalité

---

## 8. Adaptation par type d'analyse

| Type d'analyse | Ajustements de langage |
|---|---|
| **Meridian (MMM bayésien)** | Parler d'intervalles de crédibilité (pas de confiance), de posteriors, de priors. Mentionner les response curves et l'optimisation budgétaire. |
| **ARIMA_PLUS_XREG (BQML)** | Appeler ça « analyse de contribution » — jamais « MMM ». Parler de poids des régresseurs, d'AIC, de décomposition. Pas d'intervalles crédibles (c'est du fréquentiste). |
| **Causal Impact (geo-lift)** | Parler de « test d'incrémentalité » ou « expérimentation ». Ici on peut parler de causalité (c'est un quasi-expérimental). Les termes « groupe test / groupe témoin » sont appropriés. |
| **ARIMA + Contribution (hybride)** | Combiner le vocabulaire des deux premiers. Être clair sur ce qui vient du modèle de séries temporelles vs de l'attribution. |

---

## 9. Références

- Skill `meridian-mmm` — Guide technique complet Meridian
- Skill `expert_bqml_arima_plus_xreg` — Guide technique ARIMA_PLUS_XREG
- [Google Meridian (open-source)](https://github.com/google/meridian)
- [Meridian Documentation](https://developers.google.com/meridian)

> [!TIP]
> Pour approfondir la méthodologie MMM avant une restitution :
> ```
> search_documents("Google Meridian MMM marketing mix modeling bayesian")
> search_documents("BigQuery ML ARIMA_PLUS_XREG contribution analysis")
> ```
