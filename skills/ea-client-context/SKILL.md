---
name: ea-client-context
description: >
  Base de connaissances contextuelles par client. Contient la stratégie marketing, structure de campagnes,
  objectifs par levier, calendrier promotionnel, saisonnalités et problématiques spécifiques de chaque client.
  Use when user says "contexte client", "fiche client", "stratégie de", "objectifs de",
  "quel client", "info client", "onboarding client". Always read BEFORE ea-reporting-leo for reporting
  and BEFORE ea-ads-google or ea-ads-meta for client-specific audits.
---

# Skill Client Context — EdgeAngel

Ce skill stocke et organise le contexte marketing de chaque client géré par EdgeAngel. Il sert de **mémoire structurée** pour alimenter les bilans mensuels et toute analyse stratégique.

## Quand utiliser ce skill

- **Avant de rédiger un bilan mensuel** (`ea-reporting-leo`) : charger la fiche client pour contextualiser l'analyse
- **Lors d'un audit ou d'une recommandation stratégique** : comprendre les enjeux spécifiques du client
- **Pour vérifier un objectif (ROAS cible, budget, priorité)** : retrouver la référence à jour
- **En onboarding d'un nouveau client** : créer une nouvelle fiche

> **Souplesse** : si aucune fiche n'existe ou n'est à jour pour le client en question, procéder sans et demander à l'utilisateur si nécessaire.

## Liens avec d'autres skills

- **Reporting** : le skill `ea-reporting-leo` référence les fiches clients pour enrichir les bilans mensuels
- **Analyse BigQuery** : le skill `ea-analyse-edgeangel` contient les GA4 Property IDs et les particularités techniques par client (complémentaire à la fiche client qui est orientée business/stratégie)

## Comment utiliser ce skill

1. **Identifier le client** concerné
2. **Lire la fiche client** dans le dossier `clients/` (ex: `clients/cheval-energy.md`)
3. **Intégrer le contexte** dans ton analyse ou ton bilan :
   - Adapter la structure du reporting aux leviers actifs du client
   - Respecter les priorités stratégiques (ex: focus marge vs volume)
   - Contextualiser les résultats avec la saisonnalité et le calendrier promo
   - Mentionner les problématiques spécifiques (stock, tracking, etc.)

## Fiches clients disponibles

| Client | Fichier | Leviers actifs | Dernière MAJ |
|---|---|---|---|
| Cheval Energy | `clients/cheval-energy.md` | Google Ads, Meta Ads | Février 2026 |
| Allocab | `clients/allocab.md` | Google Ads, Microsoft Ads | Mars 2026 |
| Golf One 64 | `clients/golf-one.md` | Google Ads, Meta Ads, Microsoft Ads, Demand Gen | Mars 2026 |
| ETS Global (TOEIC) | `clients/ets-global.md` | Google Ads, Microsoft Ads (suspendu), Meta Ads | Mars 2026 |

---

## Structure d'une fiche client (template)

Chaque fiche client suit la structure ci-dessous. **Toutes les sections ne sont pas obligatoires** — ne remplir que ce qui est pertinent pour le client.

### 1. Identité & Business Model
- Nom du client, URL, secteur d'activité
- Type de business (e-commerce, service, B2B, SaaS…)
- Proposition de valeur / positionnement
- Particularités (marques propres, distribution, multi-pays…)

### 2. Stratégie Marketing Globale
- Objectif principal (volume, marge, acquisition, notoriété…)
- Arbitrages stratégiques clés (ex: marge vs volume, conquête vs fidélisation)
- KPIs prioritaires et cibles

### 3. Leviers Actifs & Structure de Campagnes
Pour chaque levier (Google Ads, Meta Ads, Microsoft Ads, etc.) :
- Nombre et liste des campagnes
- Logique de segmentation (par marque, catégorie, priorité, pays…)
- Objectifs et ROAS/CPA cibles par campagne ou groupe
- Stratégie d'enchères
- Répartition budgétaire cible

### 4. Catalogue & Mix Produits/Marques
- Structure du catalogue (marques propres, distribuées, etc.)
- Hiérarchie de marge par marque/catégorie
- Produits phares / best-sellers
- Problématiques stock

### 5. Calendrier Promotionnel & Saisonnalité
- Périodes de forte/faible activité
- Événements commerciaux récurrents (Black Friday, soldes…)
- Promotions programmées
- Événements sectoriels spécifiques

### 6. Données & Tracking
- Sources de données disponibles (BigQuery, GA4, BO…)
- Propriété GA4 (ID)
- Compte Google Ads (ID)
- Tables BigQuery pertinentes
- Problématiques de tracking connues

### 7. Problématiques Spécifiques
- Contraintes opérationnelles (stock, logistique, saisonnalité de production…)
- Points de vigilance (concurrence, réglementation…)
- Historique récent (restructurations, migrations, incidents…)

### 8. Historique des Décisions Stratégiques
- Changements de structure de campagne (date + motif)
- Évolutions de targets (ROAS, CPA, budget)
- Tests réalisés et résultats
