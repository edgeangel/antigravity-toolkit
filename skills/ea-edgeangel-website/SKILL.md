---
name: ea-edgeangel-website
description: Orchestrateur des skills EdgeAngel. Point d'entrée pour tout travail sur le site ou le contenu EdgeAngel. Redirige vers le bon skill selon la tâche.
---

# EdgeAngel — Skill Orchestrateur

> Ce skill est le **point d'entrée**. Il ne contient pas de règles de rédaction — il redirige vers le bon skill.

---

## Architecture des Skills

```
ea-edgeangel-website (ce fichier)
│
├── ea-edgeangel-brand-voice       → ADN, ton, personnalité, vocabulaire
│                                     LIRE EN PREMIER, TOUJOURS
│
├── ea-edgeangel-website-pages     → Pages transactionnelles (Level 2, Level 3, Solutions)
│                                     SEO, GEO, CRO intégrés + templates Astro
│
└── ea-edgeangel-content-strategy  → Notes d'Expert (articles de fond)
                                      Structure 7 parties + optimisation GEO
```

---

## Matrice de Décision

| Tâche demandée | Skill à lire |
|---|---|
| Créer ou modifier une **page Level 2** (hub thématique) | `ea-edgeangel-brand-voice` → puis `ea-edgeangel-website-pages` §2 |
| Créer ou modifier une **page Level 3** (page outil) | `ea-edgeangel-brand-voice` → puis `ea-edgeangel-website-pages` §3 |
| Créer ou modifier une **page Solution** (Capture, etc.) | `ea-edgeangel-brand-voice` → puis `ea-edgeangel-website-pages` §4 |
| Rédiger les **FAQ** d'une page | `ea-edgeangel-brand-voice` → puis `ea-edgeangel-website-pages` §6 |
| Rédiger une **Note d'Expert** (article de fond) | `ea-edgeangel-brand-voice` → puis `ea-edgeangel-content-strategy` |
| Optimiser le **SEO** d'une page existante | `ea-edgeangel-website-pages` §5 |
| Optimiser le **GEO** d'une page existante | `ea-edgeangel-website-pages` §6 |
| Vérifier le **ton / brand voice** d'un contenu | `ea-edgeangel-brand-voice` uniquement |
| Choisir le bon **vocabulaire** | `brand-voice` §3 |
| Comprendre l'**architecture du site** | `ea-edgeangel-website-pages` §1 |

---

## Règle Fondamentale

**Toujours lire `ea-edgeangel-brand-voice` avant les 2 autres skills.** Le brand voice est la source de vérité pour le ton, la personnalité et le vocabulaire. Les skills `website` et `content-strategy` en dépendent.

---

## Fichiers Clés du Projet

| Fichier | Rôle |
|---|---|
| `src/data/routes.ts` | Source de vérité des URLs et de la hiérarchie des pages |
| `src/data/seo-config.ts` | Configuration SEO globale |
| `src/data/teamProfiles.ts` | Profils experts (E-E-A-T) |
| `src/data/expertNotes.ts` | Référencement des Notes d'Expert |
| `src/layouts/Level2Layout.astro` | Layout des pages hub (8 slots) |
| `src/layouts/Level3Layout.astro` | Layout des pages outil (10 slots) |
| `src/layouts/SolutionLayout.astro` | Layout des pages solution |
| `src/layouts/ExpertNoteLayout.astro` | Layout des Notes d'Expert |
| `.agents/workflows/add-new-page.md` | Workflow pour ajouter une nouvelle page (si disponible) |
