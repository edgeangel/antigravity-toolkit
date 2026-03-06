---
name: ea-reporting-leo
description: Rédige des reportings mensuels de performance digitale (SEA, Social Ads). Utilise ce skill pour créer des bilans mensuels clients avec analyse des performances par levier (Google Ads, Microsoft Ads, META), comparaisons MoM/YoY, et recommandations stratégiques. Ce skill couvre aussi bien les bilans e-commerce (ROAS, CA, ventes) que les bilans orientés acquisition/service (CPA, courses, téléchargements). MCPs utiles : bigquery, google-analytics, google-ads-gms, meta-ads.
---

# Skill Reporting Mensuel — EdgeAngel

Ce skill guide la rédaction de reportings mensuels de performance digitale. Il encode l'ADN, la structure, la tonalité et les patterns analytiques des bilans produits par EdgeAngel, tels qu'observés dans les reportings réels de 4 clients aux profils très différents.

## Quand utiliser ce skill

- Rédaction d'un bilan mensuel de performance pour un client
- Analyse des résultats d'un mois sur les leviers payants (SEA, Social Ads)
- Synthèse des données Google Ads, Microsoft Ads, META
- Préparation d'un email ou d'une présentation de reporting client
- Rédaction de commentaires analytiques à intégrer dans des slides

## Liens avec d'autres skills

- **Contexte client** : si pertinent, consulter `ea-client-context` pour enrichir l'analyse avec le contexte métier du client (KPIs cibles, saisonnalité, historique stratégique). Si aucune fiche n'existe ou n'est à jour, procéder sans.
- **Analyse BigQuery** : pour les requêtes de données, se référer à `ea-analyse-edgeangel` qui documente les pièges de la vue `view_raw_daily_insight`.
- **Brand voice** : le ton du reporting (tutoiement, factuel, directif) est propre à ce skill et peut différer du brand-voice EdgeAngel (destiné au site web). Si le ton s'écarte significativement de l'ADN EdgeAngel, **notifier l'utilisateur** pour arbitrage.

## Principes fondamentaux (ADN du reporting EdgeAngel)

### 1. Chaque chiffre raconte une histoire

Ne **jamais** laisser un chiffre seul. Chaque métrique doit être :
- **Comparée** (MoM + YoY minimum)
- **Contextualisée** (saisonnalité, événement promo, problème technique, marché)
- **Interprétée** (ce que ça signifie stratégiquement : signal positif, point de vigilance, levier d'action)

> Exemple réel : « Les résultats du SEA en termes de ventes restent corrects dans un contexte où l'ensemble des leviers du site enregistrent une baisse de volumes par rapport à l'année dernière (-14% de ventes selon le BO), puisque le recul SEA est très modéré en termes de ventes (-6%) et que nous sommes en légère croissance en termes de CA (+4%). »

### 2. Triple perspective systématique

Pour chaque métrique clé, toujours fournir :
1. **Valeur absolue** (le chiffre brut)
2. **Évolution MoM** (vs mois précédent — dynamique de court terme)
3. **Évolution YoY** (vs même mois N-1 — tendance structurelle)

> Exemple réel : « Le CA atteint 550 563€ (+14% vs octobre, +22% YoY). »

### 3. Honnêteté stratégique

- **Valoriser sans enjoliver** : les réussites sont documentées avec fierté mais toujours par les chiffres
- **Expliquer sans minimiser** : les baisses sont expliquées par des hypothèses concrètes (saisonnalité, concurrence, tracking, stock), jamais esquivées
- **Proposer sans imposer** : les recommandations sont formulées comme des orientations stratégiques, pas des directives

> Exemple réel de contextualisation d'une baisse : « Ce recul s'explique moins par une baisse de performance des campagnes que par un contexte général plus compliqué — saisonnalité creuse + concurrence + achats 42h plus importants. »

### 4. Vision multi-niveaux

L'analyse descend toujours du global vers le granulaire :
```
Site global → Leviers payants (agrégé) → Par levier (Google, MS, Meta) → Par type de campagne → Par produit/marque
```

### 5. Adaptabilité par client

Chaque client a un "vocabulaire métrique" propre selon son business model. Le skill ne produit **pas** un template figé mais un cadre analytique adaptable :

| Type de client | Métriques prioritaires | Focus stratégique |
|---|---|---|
| **E-commerce produit** (ex: Golf One, Cheval Energy) | CA, ventes, ROAS, panier moyen, NC, CA marge | Rentabilité, scaling, mix produit/marque |
| **Service/Booking** (ex: Allocab) | Courses bookées, CPA, NC, ratio NC, marge/course | Acquisition, CPA cible, volume, notoriété |
| **B2B / Formation** (ex: AMJT) | Ventes, CA, NC, CA nouveau client, ratio NC | Croissance, conquête vs fidélisation, attribution |

---

## Structure type du reporting

Le reporting suit la structure ci-dessous. **Adapter les sections selon les leviers actifs et le profil du client.** Certains clients reçoivent des emails rédigés, d'autres des présentations avec commentaires analytiques par slide.

### 1. En-tête & Introduction

**Format email :**
```
Objet : [Agence x Client] Bilan [Leviers] - [mois] [année]

Bonjour [Prénom],
Tu trouveras ci-dessous le reporting de [mois].
```

**Format présentation (PPTX) :**
- Page de couverture : `Accompagnement Marketing Digital — Bilan mensuel [mois] [année]`
- Slide « Récapitulatif des actions menées » (liste à puces concise des actions techniques/opérationnelles du mois)

**Règles communes :**
- Tutoiement systématique
- Phrase d'intro courte (1-2 lignes max)
- Si contexte particulier (vœux, événement, incident technique), l'intégrer naturellement dans l'intro

### 2. Vue d'ensemble globale ��

C'est la section la plus importante. Elle donne le ton du bilan entier. Elle est spécifique au client et au mois — ce n'est **jamais** un simple tableau de chiffres.

**Cheminement de pensée :**

1. **Qualifier le mois en 1 phrase forte** — C'est l'accroche éditoriale. Elle doit transmettre immédiatement si le mois est bon, exceptionnel, en retrait, en transition. Cette phrase donne le "mood" du bilan entier.

2. **Panorama macro** — Métriques clés du site (CA, ventes, panier moyen) avec double comparaison MoM + YoY. Le but : situer le mois dans sa trajectoire.

3. **Interprétation stratégique** — Pourquoi ce résultat ? Saisonnalité, promotion, scaling, problème technique ? Ne jamais laisser le lecteur se poser la question.

4. **Contribution du paid** — Quelle part des résultats vient des leviers payants ? C'est la justification de valeur de l'agence.

5. **Nouveaux clients** — Toujours traité comme un KPI à part : volume, ratio dans le total, évolution. C'est souvent l'enjeu stratégique central.

**Métriques à couvrir selon le type de client :**

| Métrique | E-commerce | Service/Booking | B2B/Formation | Comparaisons |
|---|---|---|---|---|
| CA (€) | ✅ | — | ✅ | MoM + YoY |
| Volume de ventes/achats | ✅ | — | ✅ | MoM + YoY |
| Courses bookées | — | ✅ | — | MoM + YoY |
| Courses réalisées | — | ✅ | — | MoM + YoY |
| ROAS global | ✅ | — | ✅ (si pertinent) | MoM + YoY |
| CPA / CPA nouveau client | Si pertinent | ✅ | ✅ | MoM + YoY |
| Panier moyen (€) / Course moyenne (€) | ✅ | ✅ | — | YoY min |
| Nouveaux clients (volume) | ✅ | ✅ | ✅ | MoM + YoY |
| Part nouveaux clients (%) | ✅ | ✅ | ✅ | YoY min |
| CA marge estimé (€) | Si disponible | — | — | YoY |
| Marge par course/vente | — | Si disponible | — | YoY |
| Investissements médias (€) | ✅ | ✅ | ✅ | MoM + YoY |
| Part paid dans ventes (%) | ✅ | ✅ | ✅ | YoY |

### 3. Focus par levier ��

Une section dédiée par levier actif. Le niveau de détail varie selon l'importance du levier pour le client.

**Structure commune pour chaque levier :**
1. **Résumé en 1-2 phrases** — Bilan net du levier sur le mois
2. **Métriques clés** — Investissements, résultats (CA/ventes ou courses/CPA), ROAS ou CPA, NC
3. **Comparaison MoM et YoY**
4. **Analyse du rôle stratégique** — Qu'apporte ce levier dans la stratégie globale ?
5. **Points d'attention / faits marquants** — Tests, incidents, signaux faibles

**Spécificités par levier :**

#### Google Ads
- Part dans le mix global (% ventes, % CA, % NC)
- Analyse des types de campagnes : Brand vs Conquête vs PMax vs DemandGen
- Stratégie d'enchères et évolution
- Pour le SEA service : distinction courses bookées vs courses réalisées
- Signaux de pression concurrentielle (CPC en hausse, taux d'impression en baisse)

> Exemple réel : « Les canaux payants sont à l'origine de 73% des ventes et du CA (contre seulement 38% l'année dernière), ce qui représente une croissance YoY conséquente (+90% de ventes et +120% de CA) pour des dépenses quasi stables (+7%). »

#### Microsoft Ads
- Toujours positionné comme **complément stratégique** à Google, jamais en concurrent
- Focus sur le rôle de conquête (ratio NC souvent supérieur à Google)
- Analyse du potentiel de scaling
- Comparaison coût d'acquisition vs Google Ads

> Exemple réel : « Scaling important des dépenses aussi bien par rapport à décembre (sous-diffusion) que par rapport à l'année dernière. Les volumes progressent mais le scaling n'est pas encore optimal en termes de CPA, même si le chiffre reste très nettement inférieur à celui de Google et que la marge réalisée est plus importante. »

#### META (Facebook/Instagram)
- Double vision : ROAS régie vs ROAS GA4 (toujours mentionner les deux)
- Analyse par type de campagne : Acquisition, Retargeting, Catégorie/Produit, Notoriété
- Fatigue créative : identifier si les visuels s'essoufflent et recommander un renouvellement
- Meilleurs visuels/formats du mois (vidéo, catalogue, visuels spécifiques)
- Restructuration campagnes (ex: passage aux campagnes ASC — Advantage+ Shopping)

> Exemple réel : « Record historique d'efficacité sans promotions. La campagne de Retargeting affiche un ROAS de 50 (68% du CA Meta). Succès majeur du format vidéo en retargeting et des visuels "Phyto" (ROAS de 45.5). »

#### Campagnes App (si applicable)
- Volume de téléchargements
- Achats in-app (B2C/SMB)
- CPA global et évolution
- Impact estimé sur la croissance organique de l'app

### 4. Analyse par pays / zone géographique (si multi-pays)

Pour chaque zone active :
- Bilan spécifique avec métriques clés (CA, ventes ou courses, ROAS ou CPA)
- Panier moyen / course moyenne par zone
- Part dans le global et évolution
- Dynamique spécifique (phase de scaling, maturité, pression concurrentielle locale)

> Exemple réel (Golf One Espagne) : « SEA ES poursuit sa croissance (+17% vs mars). Responsable de 25% des nouveaux clients. »

### 5. Analyse produits / stock / marques �� (si pertinent)

Cette section est critique pour les clients e-commerce avec un catalogue structuré par marques.

**Approche par niveaux de priorité :**
- **Prio 1** : Marques propres / forte marge → Investissement agressif, ROAS cible plus bas accepté
- **Prio 2** : Top marques distribuées → ROAS cible intermédiaire
- **Prio 3** : Reste du catalogue → ROAS cible élevé (conservateur)

**Éléments à couvrir :**
- Taux de conversion global vs N-1
- Performance par marque/catégorie (vues, ajouts panier, achats)
- Problèmes de stock identifiés et leur impact
- Produits/marques volontairement mis en retrait et la raison

> Exemple réel : « Les produits ESC sont volontairement mis en retrait (-90% de CA YoY) par manque de rentabilité ou ruptures. La focalisation sur les marques Cheval Energy, Audevard et Reverdy est maintenue. »

### 6. Contexte marché / Environnement concurrentiel �� (si pertinent)

Section particulièrement utilisée pour les clients en service/booking, mais applicable à tout client.

**Éléments à couvrir :**
- Volumes de recherche Google sur les requêtes clés (tendance MoM + YoY)
- Évolution des CPC et de la pression concurrentielle
- Événements de marché impactants (grèves, météo, réglementation, saisonnalité)
- Source des données toujours mentionnée

> Exemple réel : « Les principaux mots-clés du secteur (taxi Paris, taxi Marseille…) affichent des décroissances marquées sur un an, de l'ordre de -20% à -30% en volume de requêtes. (Source : données Google Ads sur un panel de 1000+ mots-clés représentatifs) »

### 7. Actions réalisées / en cours ��️

Liste à puces concise, organisée par importance :
- Optimisations techniques (tracking, flux produits, restructuration)
- Gestion des budgets et des stratégies d'enchères
- Tests en cours (AB tests, nouvelles campagnes, nouveaux formats)
- Suivi du calendrier promotionnel
- Problèmes en cours de résolution
- Prochaines actions prévues (mois suivant)

> Exemple réel : « AB Test sur la fonctionnalité AI Max (élargissement des mots-clés/audiences/personnalisation automatiques des annonces/extension d'urls). Suivi des courses done et de la marge, préparation AB test (lancement 10/02). »

### 8. Sections administratives

- **DC/DA** ⚙️ — Enveloppe jours restants, travaux prévus
- **Facturation** �� — Renvoi au dispatch, factures échues
- **Mois en cours** ��️ — Objectif d'investissement, tendances des premiers jours

### 9. Conclusion

```
N'hésite pas à nous contacter pour toute question / commentaire, nous sommes à ta disposition.
Bonne journée.
```

- Mentionner la prochaine visio si prévue
- Rester disponible et ouvert

---

## Guidelines de tonalité et de style

##...