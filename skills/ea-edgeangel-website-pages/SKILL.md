---
name: ea-edgeangel-website-pages
description: Guide expert pour créer et optimiser les pages transactionnelles du site EdgeAngel (Level 2, Level 3, Solutions). Intègre SEO, GEO, CRO et respecte le brand-voice. Lire ea-edgeangel-brand-voice AVANT ce skill.
---

# EdgeAngel Website — Pages Transactionnelles

> **Prérequis** : Lire le skill `ea-edgeangel-brand-voice` AVANT celui-ci pour le ton et la personnalité.
> **Scope** : Pages services (Level 2, Level 3, Solutions). Pour les Notes d'Expert → skill `ea-edgeangel-content-strategy`.

---

## 1. Architecture du Site

### Hiérarchie des pages

```
Homepage (/)
├── Hub (Level 1)          → /data-foundations, /marketing-activation, /performance-acquisition
│   ├── Level 2            → /data-foundations/web-tracking, /performance-acquisition/seo-geo
│   │   └── Level 3        → /data-foundations/google-analytics, /performance-acquisition/google-ads
│   └── Level 2            → ...
├── Solutions              → /solutions/capture, /solutions/cookie-consent
├── Notes d'Expert         → /notes/...  (→ skill edgeangel-content-strategy)
└── Institutionnel         → /a-propos/agence, /contact, etc.
```

### Fichiers de référence

| Fichier | Rôle |
|---|---|
| `src/data/routes.ts` | **Source de vérité** des URLs, titres et hiérarchie (hubs, level2, level3, other, notes) |
| `src/data/seo-config.ts` | Config SEO globale (siteName, siteUrl, defaultTitle, organization schema) |
| `src/data/teamProfiles.ts` | Profils experts (nom, rôle, bio, avatar) — utilisé pour E-E-A-T |
| `src/data/expertNotes.ts` | Référencement des Notes d'Expert pour les lier aux pages services |
| `src/data/testimonials.ts` | Témoignages clients pour la preuve sociale |

---

## 2. Level 2 — Pages Hub Thématiques

### Rôle
Présenter un **domaine d'expertise** (ex: SEO & GEO, Social Ads, AI Marketing). C'est une page de conviction qui vend une vision, pas un outil.

### Layout & Slots

Utiliser `Level2Layout.astro` avec les slots dans cet ordre :

```astro
<Level2Layout title={...} metaTitle={...} description={...} faq={faqItems}>
    <Level2Hero slot="hero" ... />
    <ServiceList slot="services" ... />
    <ApproachSection slot="approach" ... />       <!-- "Notre conviction" -->
    <Reassurance slot="intro" />
    <ExpertList slot="experts" ... />
    <ToolList slot="tools" ... />
    <Contact slot="contact" showTeamPhoto={false} />
    <FAQ slot="faq" ... />
    <ArticleList slot="notes" articles={articles} />
</Level2Layout>
```

### Contenu obligatoire

| Section | Contenu attendu | Ton |
|---|---|---|
| **Hero** | Titre accrocheur + subtitle + description ~2 phrases denses en faits | Engagé, percutant |
| **Services** (ServiceList) | 3-4 blocs avec title + 4-5 bullet points `<strong>Nom</strong> : Description` | Expert, concret |
| **"Notre conviction"** (ApproachSection) | 2-3 paragraphes de prise de position forte. C'est l'ADN EdgeAngel. | Engagé, tranché |
| **Experts** | Via `getExperts()` depuis `teamProfiles.ts` | Professionnel |
| **Outils** | 4-6 outils avec description orientée "ce qu'on fait avec" | Pragmatique |
| **FAQ** | 5-10 questions (voir guide FAQ ci-dessous) | Naturel, expert |
| **Notes liées** | 2-4 articles via `EXPERT_NOTES` depuis `expertNotes.ts` | — |

### Template de données Level 2

```typescript
// Section approche — voix engagée
const approachContent = {
    title: "Notre conviction : [Titre fort et engagé]",
    content: [
        "Paragraphe 1 : Poser le constat ou la vision...",
        "Paragraphe 2 : Expliquer l'approche EdgeAngel...",
        "Paragraphe 3 : Conclure sur la différenciation...",
    ],
};

// Services — 3-4 blocs
const services = [
    {
        title: "Nom du Service",
        points: [
            "Phrase d'accroche qui pose le besoin ou la conviction.",
            "<strong>Feature 1</strong> : Description orientée bénéfice, pas catalogue.",
            "<strong>Feature 2</strong> : ...",
        ],
    },
];

// Experts — depuis teamProfiles
import { getExperts } from "../../data/teamProfiles";
const experts = getExperts(["prenom1", "prenom2"], "domainKey");

// Articles liés — depuis expertNotes
import { EXPERT_NOTES } from "../../data/expertNotes";
const articles = [EXPERT_NOTES.article1, EXPERT_NOTES.article2];
```

---

## 3. Level 3 — Pages Outil / Technologie

### Rôle
Présenter l'expertise EdgeAngel sur un **outil spécifique** (Google Analytics, Meta Ads, Didomi…). Plus concret et technique que le Level 2.

### Layout & Slots

Utiliser `Level3Layout.astro` :

```astro
<Level3Layout title={...} metaTitle={...} description={...} faq={faqItems}>
    <Level3Hero slot="hero" toolName="..." tagline="..." description="..." logo="..." />
    <ToolIntro slot="intro" title="..." description="..." features={[...]} ... />
    <Certification slot="certification" partners={[...]} />
    <Clients slot="clients" />
    <ToolServicesNav slot="services" title="..." services={services} />
    <Reassurance slot="reassurance" />
    <ExpertList slot="team" ... />
    <Contact slot="cta" showTeamPhoto={false} />
    <ArticleList slot="notes" articles={articles} />
    <FAQ slot="faq" ... />
    <RelatedTools slot="related" currentTool="..." />
</Level3Layout>
```

### Contenu obligatoire

| Section | Contenu attendu |
|---|---|
| **Level3Hero** | `toolName` (nom outil), `tagline` (bénéfice en 1 ligne), `description` (2-3 phrases), `logo` |
| **ToolIntro** | `title`, `description` (1 phrase), `features` (4 bullet points orientés bénéfice business) |
| **Services** (ToolServicesNav) | 2-3 blocs de services avec `title`, `description`, `features[]` |
| **Experts** | 2-3 experts pertinents pour cet outil |
| **FAQ** | 5-7 questions spécifiques à l'outil |
| **RelatedTools** | Composant automatique qui affiche les outils connexes |

### Différence de ton Level 2 vs Level 3

| Aspect | Level 2 | Level 3 |
|---|---|---|
| **Angle** | Vision, conviction, stratégie | Expertise outil, concret, technique |
| **"Notre conviction"** | Oui (obligatoire) | Non (optionnel) |
| **Certification / Partenariat** | Non | Oui (si applicable) |
| **Profondeur technique** | Stratégique | Opérationnel |

---

## 4. Pages Solutions

### Rôle
Présenter un **produit EdgeAngel** (ex: Capture). Page de vente longue avec pricing et business cases.

### Layout
Utiliser `SolutionLayout.astro`. Structure libre (pas de slots imposés sauf hero/services/faq).

### Éléments attendus
- Hero avec proposition de valeur en 1 phrase
- Section "Pourquoi [Produit] ?" avec 3 piliers
- Modules détaillés avec visuels/vidéos
- Business case avec témoignage client (composant `BusinessCase`)
- Pricing transparent
- FAQ

---

## 5. Conventions SEO

### Meta Tags

| Élément | Convention | Exemple |
|---|---|---|
| **title / metaTitle** | `{Sujet} : {Bénéfice} \| EdgeAngel` — 50-60 chars | `Agence Google Analytics : Expertise GA4 Et Migration` |
| **description** | 150-160 chars, inclure "EdgeAngel", bénéfice concret | `Exploitez le potentiel de GA4 avec notre agence google analytics. Migration, configuration, conformité RGPD et formation par nos experts certifiés.` |
| **H1** | Un seul par page, dans le Hero | Via `title` du Hero |
| **Breadcrumbs** | Hérités de `routes.ts` via le layout | Automatique |

### URL
- Toujours en `kebab-case` français
- Structure : `/{hub}/{slug}` pour L2/L3
- Définies dans `src/data/routes.ts` — ne jamais hardcoder

### Maillage interne
- Utiliser `ROUTES.level3.xxx.path` pour les liens internes (jamais de chemin en dur)
- Chaque page L2 doit lier vers ses pages L3 via `ToolList`
- Chaque page L3 doit lier vers son hub parent via breadcrumbs et `RelatedTools`

### Schema JSON-LD
- Géré automatiquement par `SEOHead.astro` → `SchemaJSONLD.astro`
- Les **FAQ** passées en prop `faq` sont automatiquement sérialisées en `FAQPage` schema
- Type `service` par défaut pour toutes les pages L2/L3

---

## 6. Conventions GEO (Generative Engine Optimization)

L'objectif est que le contenu EdgeAngel soit **cité par les moteurs IA** (ChatGPT, Perplexity, Gemini).

### Principes appliqués

| Principe GEO | Application EdgeAngel |
|---|---|
| **Densité de faits** | Hero et intro doivent contenir des faits concrets (pas de fluff marketing) |
| **Réponses directes** | Chaque FAQ commence par une réponse en 1 phrase (extractible par LLM) |
| **Entity Building** | Section "Notre conviction" = contenu citable unique à EdgeAngel |
| **Auteur identifié** | Toujours utiliser `teamProfiles.ts` → `getExperts()` pour nommer les experts |
| **Dates** | Pas de dates dans les pages transactionnelles (contenu evergreen) |
| **Contenu structuré** | Utiliser `<strong>` pour les termes clés dans les listes de services |

### Structure FAQ optimisée GEO

```
Question : [Question naturelle que poserait un utilisateur à ChatGPT]
Réponse :
  → Phrase 1 : Réponse directe (la "citation" que l'IA pourra extraire)
  → Phrases 2-4 : Explication, contexte, nuance
  → Phrase 5 : Preuve EdgeAngel (cas client, certification, pratique interne)
```

**Longueur cible** : 80-150 mots par réponse. Pas plus.

---

## 7. Conventions CRO (Conversion Rate Optimization)

| Élément | Implémentation |
|---|---|
| **CTA principal** | Composant `Contact` en bas de page avec `showTeamPhoto={false}` |
| **CTA secondaires** | Liens vers `/contact` dans le texte (soft CTA) |
| **Preuve sociale** | Composant `Reassurance` (logos clients, certifications, métriques) |
| **Témoignages** | Via `testimonials.ts` et composant `BusinessCase` (pour Solutions) |
| **Experts identifiés** | Photos et bios d'experts = signal de confiance |
| **FAQ** | Lève les objections, rassure, et capte le trafic longue traîne |

---

## 8. Checklist de Validation

Avant de livrer une page transactionnelle, vérifier :

- [ ] **Brand Voice** : Le ton respecte les 5 piliers (pas de jargon vide, pas de promesses sans preuve)
- [ ] **Structure** : Tous les slots du layout sont remplis dans le bon ordre
- [ ] **SEO** : `title` ≤ 60 chars, `description` 150-160 chars, H1 unique, FAQ en schema
- [ ] **GEO** : FAQ avec réponses directes, experts identifiés, contenu dense en faits
- [ ] **CRO** : CTA Contact présent, Reassurance, au moins 1 preuve sociale
- [ ] **Routes** : Page enregistrée dans `routes.ts`, liens internes via `ROUTES`
- [ ] **Données** : Experts via `getExperts()`, articles via `EXPERT_NOTES`
- [ ] **i18n** : Si le site est bilingue, vérifier que la route EN existe dans `routesEn`
