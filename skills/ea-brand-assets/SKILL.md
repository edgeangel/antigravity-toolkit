---
name: ea-brand-assets
description: >
  Production de livrables Google Docs professionnels EdgeAngel à partir de Markdown.
  Workflow automatisé : import .md dans Drive, conversion Google Doc, branding via script
  Apps Script (styles, header/footer, tableaux, bordures H1), personnalisation header via MCP.
  MCPs : google-drive (create_file, copy_file, write_doc, read_doc).
  Use when user says "export", "créer un doc", "note client", "rapport client",
  "livrable", "document Google Docs", "template EdgeAngel", "Google Doc", "brand".
---

# EA Brand Assets — Export Google Docs EdgeAngel

Production de livrables Google Docs professionnels aux couleurs EdgeAngel, à partir de contenu Markdown.

## Liens

- **Contexte client** : `ea-client-context` pour le contexte du client concerné
- **MCPs** : `google-drive` (create_file, copy_file, write_doc, read_doc, read_file)
- **Script** : Web App Apps Script `applyEdgeAngelBrand` (déployé, URL privée)
- **Config** : `config/template-ids.json` — IDs templates, shared drive, couleurs

---

## Architecture

```
ea-brand-assets/
├── SKILL.md                            # Ce fichier — workflow unique
├── config/template-ids.json            # Registry des templates + brand colors
└── references/md-formatting-guide.md   # Guide formatage Markdown
```

---

## Workflow — 5 étapes

```
Markdown (.md) → Upload Drive (convert) → Google Doc natif
                                            ↓
                 Script brand (web app) ← Appliquer branding EA
                                            ↓
                 MCP write_doc ← Personnaliser header (contexte du contenu)
                                            ↓
                                       Vérification
```

### Étape 1 — Importer le Markdown dans Google Docs

Uploader le fichier .md dans Drive en le convertissant automatiquement en Google Doc natif.
La conversion Google préserve la structure (headings, tableaux, listes) avec un formatage basique.

```
create_file(
  name="<Nom du document>",
  local_path="/chemin/vers/fichier.md",
  convert_to="document",
  parent_folder_id="<DOSSIER_DRIVE>"    # voir config/template-ids.json → shared_drive_id
)
```

> **Pourquoi `convert_to: document`** — Google convertit le Markdown en Doc natif avec
> tables, headings et listes automatiquement reconnus. C'est plus fiable que d'insérer
> le contenu manuellement via l'API.

**Résultat** : un Google Doc brut avec le contenu structuré mais pas brandé.

### Étape 2 — Appliquer le branding EdgeAngel

Appeler le script Apps Script déployé en web app pour appliquer automatiquement :
- ✅ Header (logo EdgeAngel + texte centré)
- ✅ Footer (texte centré)
- ✅ Styles texte (font Inter, couleurs EA sur headings, body, etc.)
- ✅ Tableaux (header Navy + texte blanc, body stylisé)
- ✅ Bordure H1 (trait bleu Pacific sous chaque HEADING_1)
- ✅ Bordure header (trait gris clair sous le header)
- ✅ Marges document (si configurées)

```python
import urllib.request, json

url = "<URL_WEBAPP_APPS_SCRIPT>"
payload = json.dumps({
  "docId": "<DOC_ID>",
  "action": "brand"
}).encode()

req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
resp = urllib.request.build_opener(urllib.request.HTTPRedirectHandler).open(req, timeout=120)
result = json.loads(resp.read().decode())
# result = {"success": true, "docId": "...", "action": "brand"}
```

**Actions disponibles** :

| Action | Rôle |
|--------|------|
| `brand` | Pipeline complet (RECOMMANDÉ) |
| `styles` | Styles texte uniquement |
| `tables` | Formatage tableaux uniquement |
| `borders` | Bordures H1 + header + footer uniquement |
| `header` | Header uniquement (contenu + bordure) |
| `footer` | Footer uniquement (contenu + bordure) |

> **Ce que fait le script en interne** (4 phases) :
> 1. Phase 0 : Supprime les headers "fantômes" DocumentApp (`removeFromParent`)
> 2. Phase 2a : Crée un header/footer officiel via `CreateHeaderRequest` (API REST)
> 3. Phase 1 : Remplit le contenu (logo base64, texte, styles) via DocumentApp
> 4. Phase 2 : Applique les bordures et marges via l'API REST Docs

### Étape 3 — Personnaliser le header

Le script brand met un header générique : **"EdgeAngel — Note Client"**.
Adapter le texte du header au contexte du document (client, sujet, type de livrable).

1. **Récupérer le `headerId`** du header officiel :

```
read_doc(DOC_ID, format="structure")
# ou utiliser l'action debug-headers du script pour obtenir le headerId
```

Le debug retourne par exemple :
```json
{
  "headerKeys": ["kix.85qlgg20p4yq"],
  "documentStyle": { "defaultHeaderId": "kix.85qlgg20p4yq" }
}
```

2. **Lire le contenu actuel du header** pour trouver les index :

L'action `debug-headers` du script retourne la structure du header avec les index.
Le header contient typiquement 2 paragraphes :
- Paragraphe 1 : logo (image inline) — index 0 à ~2
- Paragraphe 2 : texte "EdgeAngel — Note Client" — index ~2 à ~26

3. **Remplacer le texte du header** via le MCP :

```
write_doc(DOC_ID, "replace_all", '{"find": "EdgeAngel — Note Client", "replace": "EdgeAngel — Audit Web Performance Golfone64"}')
```

> **Adapter l'en-tête au contenu** : analyser le titre du document (H1) et le contexte
> client pour générer un en-tête pertinent. Exemples :
> - Audit web perf → "EdgeAngel — Audit Web Performance [Client]"
> - Analyse Meta Ads → "EdgeAngel — Analyse Meta Ads [Client]"
> - Rapport mensuel → "EdgeAngel — Rapport Mensuel [Client] — [Mois Année]"

### Étape 4 — Ajustements optionnels

Selon le contenu du document, ajuster via le MCP `google-drive` :

- **Titre du document** : si le H1 du Markdown n'est pas bon
  ```
  write_doc(DOC_ID, "replace_all", '{"find": "ancien titre", "replace": "nouveau titre"}')
  ```

- **Encadrés / blockquotes** : appliquer le style executive summary sur les paragraphes clés
  ```
  write_doc(DOC_ID, "format_paragraph", '{"start_index": X, "end_index": Y, 
    "border_left": {"color": {"red": 0.086, "green": 0.302, "blue": 0.506}, "width": 3, "padding": 6, "dash_style": "SOLID"},
    "indent_start": 18, "shading_color": {"red": 0.937, "green": 0.965, "blue": 1.0}}')
  ```

- **Listes à puces** : si le Markdown avait des listes non converties
  ```
  write_doc(DOC_ID, "insert_bullets", '{"start_index": X, "end_index": Y}')
  ```

### Étape 5 — Vérification

Vérifier le document final via le MCP (pas de navigateur) :

```
read_doc(DOC_ID, format="structure")
```

**Checklist** :
- [ ] Header présent avec texte personnalisé (pas "Note Client" générique)
- [ ] Footer présent
- [ ] Bordure sous le header (borderBottom dans la structure)
- [ ] Bordures bleues sous les HEADING_1
- [ ] Tableaux formatés (si le MD en contenait)
- [ ] Font Inter sur l'ensemble du document
- [ ] Pas de placeholder `{{...}}` résiduel

Fournir le lien Google Docs au user :
```
https://docs.google.com/document/d/<DOC_ID>/edit
```

> 🚫 **Ne jamais utiliser le sub-agent navigateur** pour tester les Google Docs.

---

## Charte graphique EdgeAngel — Référence rapide

| Token | RGB | Hex | Usage |
|---|---|---|---|
| **Navy** | `(0.047, 0.157, 0.271)` | `#0C2845` | TITLE, H1 texte, table header bg |
| **Pacific** | `(0.086, 0.302, 0.506)` | `#164D81` | H2, H3, bordure H1, blockquote |
| **Slate** | `(0.2, 0.255, 0.333)` | `#334155` | Body text |
| **Grey** | `(0.392, 0.455, 0.545)` | `#64748B` | Subtitle |
| **Ice Blue** | `(0.937, 0.965, 1.0)` | `#EFF7FF` | Blockquote / encadré bg |
| **White** | `(1, 1, 1)` | `#FFFFFF` | Table header texte |
| **Font** | Inter | — | Tout le document |

---

## Mapping Markdown → Google Docs

> **Convention** : les niveaux MD sont décalés d'un cran.
> `# H1` MD = TITLE du document. `## H2` MD = HEADING_1 Docs.

| Élément MD | Style Google Docs | Notes |
|---|---|---|
| `# Titre` | TITLE | bold, Navy |
| Sous-titre | SUBTITLE | italic, Grey |
| `## Section` | HEADING_1 | bold, Navy, borderBottom Pacific |
| `### Sous-section` | HEADING_2 | bold, Pacific, 13pt |
| `#### Détail` | HEADING_3 | bold, Pacific, 11pt |
| Texte | NORMAL_TEXT | Slate, 10pt |
| `> blockquote` | NORMAL_TEXT + encadré | borderLeft Pacific, bg Ice Blue |
| `**text**` | bold | |
| `| table |` | TABLE | header Navy/White via script brand |

---

## Gestion des erreurs

| Erreur | Cause | Solution |
|---|---|---|
| Script retourne `error` | docId invalide ou droits insuffisants | Vérifier que le doc est dans le shared drive |
| Header fantôme (defaultHeaderId: null) | Le script gère ça automatiquement (Phase 0) | Relancer `brand` — Phase 0 supprime le fantôme |
| `Invalid range: start and end index` | Premier paragraphe header (startIndex undefined) | Fix intégré dans le script (fallback `\|\| 0`) |
| Bordure H1 absente | Document pas passé par le script brand | Appeler action `borders` |
| Tableaux non formatés | La conversion MD→Doc ne formate pas | Appeler action `tables` |
| `storageQuotaExceeded` | Doc dans My Drive au lieu du Shared Drive | Vérifier `parent_folder_id` |

---

## Bonnes pratiques

1. **Toujours `brand` d'abord** — le script applique tout d'un coup
2. **Personnaliser le header** — ne jamais laisser "Note Client" générique
3. **`replace_all` pour le texte** — il hérite du formatage existant
4. **Vérifier via `read_doc(structure)`** — pas via le navigateur
5. **Un seul pipeline** — .md → Drive convert → brand → header → vérifie
