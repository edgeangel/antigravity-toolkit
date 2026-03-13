---
name: ea-edgeangel-content-strategy
description: >
  Guide expert pour rédiger du contenu à forte valeur ajoutée EdgeAngel (Notes d'Expert, articles de fond).
  Use when user says "Note d'Expert", "article EdgeAngel", "blog EdgeAngel", "rédiger un article",
  "contenu SEO EdgeAngel", "GEO content". Always read ea-edgeangel-brand-voice BEFORE this skill.
---

# EdgeAngel Content Strategy — Notes d'Expert

> **Prérequis** : Lire `ea-edgeangel-brand-voice` AVANT ce skill.
> **Scope** : Notes d'Expert (`src/pages/notes/`). Pour les pages services → skill `ea-edgeangel-website-pages`.

---

## 1. Objectif

Rédiger des **Notes d'Expert** qui positionnent EdgeAngel comme un Tiers de Confiance. L'objectif n'est PAS de vendre une prestation. C'est de **démontrer une expertise pointue, pragmatique et honnête** sur des sujets complexes (Data, Privacy, Tracking, Analytics, AI, Marketing).

Format : articles de fond (~10 min de lecture), très structurés, sourcés.

---

## 2. Structure Obligatoire

Chaque note suit cette structure en 7 parties :

### Part 1 — Frontmatter & Metadata

```astro
---
import ExpertNoteLayout from "../../layouts/ExpertNoteLayout.astro";

export const title = "Titre accrocheur avec mots-clés";
export const description = "Description SEO dense, 150-160 chars";
export const author = "Prénom Nom";
export const pubDate = "YYYY-MM-DD";
export const updatedDate = "YYYY-MM-DD";
export const tags = ["tag1", "tag2"];

const headings = [
    { depth: 2, slug: "contexte", text: "Contexte" },
    { depth: 2, slug: "analyse", text: "Analyse Approfondie" },
    { depth: 2, slug: "avis-edgeangel", text: "💡 L'avis EdgeAngel" },
    { depth: 2, slug: "que-faire", text: "Dis EdgeAngel, du coup que faut-il faire ?" },
    { depth: 2, slug: "sources", text: "Sources" },
];
---
```

**Règles metadata :**
- `title` : accrocheur, inclure les mots-clés cibles
- `description` : résumé dense pour SEO et GEO, 150-160 chars
- `author` : nom complet de l'expert EdgeAngel (doit exister dans `teamProfiles.ts`)
- `tags` : utiliser les catégories de l'article (correspondant aux routes dans `routes.ts`)
- `headings` : déclaration manuelle de la table des matières (profondeur, slug, texte)

### Part 2 — Introduction / Avant-propos

- Pose le contexte en 2-3 paragraphes
- Si sujet légal/RGPD → disclaimer juridique obligatoire :
  > *EdgeAngel n'est pas un cabinet d'avocats. Cette note reflète notre analyse technique et stratégique. Pour un avis juridique, consultez un spécialiste.*
- Inclure `contact@edgeangel.co` pour poursuivre la discussion

### Part 3 — Contexte / Rappel des Faits

- **Quoi ?** Quel événement, quelle mise à jour, quel changement ?
- **Pourquoi maintenant ?** Dates clés, timeline, régulateurs concernés
- Ton factuel. Pas d'opinion ici. Citer les sources.

### Part 4 — Analyse Approfondie (Corps du sujet)

- Développer l'analyse technique, juridique ou stratégique
- Sous-titres `h2`/`h3` clairs et descriptifs
- Listes à puces pour aérer
- Schémas textuels si pertinent (organigrammes, comparaisons)
- **Profondeur attendue** : aller au-delà de l'info disponible sur les docs officielles

### Part 5 — 💡 « L'avis EdgeAngel » *(OBLIGATOIRE)*

> **C'est la section qui fait la différence.** C'est elle que les lecteurs viennent chercher.

- Analyser les forces en présence (ex : UE vs US, Google vs CNIL, Privacy vs Performance)
- Prendre position clairement : « Nous pensons que… », « C'est une opportunité pour… »
- Être rassurant mais réaliste, jamais vendeur de rêve
- Démontrer que EdgeAngel a une opinion fondée et indépendante

### Part 6 — « Dis EdgeAngel, du coup que faut-il faire ? » *(OBLIGATOIRE)*

- Le lecteur veut un **plan d'action concret**
- Scénariser par cas d'usage :
  - *Cas A : Vous avez déjà X…* → Faites Y
  - *Cas B : Vous partez de zéro…* → Faites Z
- Fournir une checklist actionnable
- Terminer par un soft CTA : « EdgeAngel peut vous accompagner sur l'audit / la mise en conformité / … »

### Part 7 — Sources

- Lister les liens officiels (docs Google, textes de loi, communiqués CNIL, RFC)
- Crédibilise l'expertise et signale aux moteurs IA la fiabilité du contenu
- Format : liste à puces avec liens cliquables

---

## 3. Formatage Technique (Astro / Tailwind)

### Classes CSS du design system

| Élément | Classe |
|---|---|
| **H2** | `text-2xl font-bold text-edge-blue mt-12 mb-6 scroll-mt-32` + attribut `id` (slug) |
| **H3** | `text-xl font-bold text-slate-800 mb-3 mt-8` |
| **Paragraphe** | `my-1.5` |
| **Liste à puces** | `list-disc pl-5 mb-6 leading-normal mt-[2px] [&>li]:mb-[2px]` |
| **Liens** | `text-edge-blue hover:underline` |
| **Strong** | `<strong>` standard (pas de classe supplémentaire) |

### Layout

```astro
<ExpertNoteLayout
    title={title}
    description={description}
    headings={headings}
    author={author}
    date={pubDate}
    updatedDate={updatedDate}
    readingTime="10 min de lecture"
>
    <!-- Contenu ici -->
</ExpertNoteLayout>
```

---

## 4. Optimisation GEO

Les Notes d'Expert sont le format le plus susceptible d'être **cité par les moteurs IA**. Optimisations spécifiques :

| Critère GEO | Application |
|---|---|
| **Auteur identifié** | `author` dans le frontmatter + profil dans `teamProfiles.ts` |
| **Date de publication** | `pubDate` et `updatedDate` — les IA privilégient le contenu récent |
| **Sources citées** | Section Sources obligatoire — signal de fiabilité |
| **Réponse directe** | La section "Que faire ?" doit commencer par une réponse sans ambiguïté |
| **Statistiques originales** | Si vous avez des données internes, les inclure (ex: « Sur nos 50+ clients GA4… ») |
| **Définitions claires** | Pour chaque concept technique, donner une définition en 1 phrase au premier usage |
| **Prise de position** | « L'avis EdgeAngel » = contenu unique non reproductible par l'IA |

---

## 5. Checklist Pré-Publication

- [ ] **Structure** : Les 7 sections sont présentes (intro, contexte, analyse, avis, que faire, sources)
- [ ] **Avis EdgeAngel** : Prise de position claire et argumentée (pas vague)
- [ ] **Plan d'action** : Scénarisé par cas d'usage, checklist actionnable, CTA soft
- [ ] **Sources** : Au moins 3 sources officielles citées
- [ ] **Metadata** : `title` ≤ 60 chars, `description` 150-160 chars, `author` valide
- [ ] **Headings** : Table des matières déclarée dans `headings`, slugs cohérents avec les `id`
- [ ] **Brand Voice** : Ton conforme aux 5 piliers (expert, transparent, pédagogue, engagé, direct)
- [ ] **GEO** : Auteur identifié, dates présentes, au moins 1 stat/fait original
- [ ] **Maillage** : Au moins 2 liens internes vers des pages services (L2/L3) via `ROUTES`
