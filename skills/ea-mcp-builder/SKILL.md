---
name: mcp-builder
description: MCP (Model Context Protocol) server building principles. Tool design, resource patterns, best practices.
---

# MCP Builder — Guide Expert

> Principes et patterns pour construire des serveurs MCP robustes et déployables.

> [!IMPORTANT]
> Pour la spécification complète du protocole MCP, consulter la documentation officielle via le MCP `google-developer-knowledge` :
> ```
> search_documents("Model Context Protocol MCP server building guide")
> ```
> Ou directement sur [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/getting-started/intro).

---

## 1. MCP Overview

### Qu'est-ce que MCP ?

Model Context Protocol — standard ouvert qui connecte les systèmes IA (LLMs) avec des outils externes et des sources de données. Le serveur MCP expose des **Tools**, **Resources** et **Prompts** que l'IA peut découvrir et invoquer de manière autonome.

### Concepts Clés

| Concept | Purpose | Exemple |
|---------|---------|---------|
| **Tools** | Fonctions que l'IA peut appeler | `execute_query`, `list_products` |
| **Resources** | Données que l'IA peut lire | Config, documentation, templates |
| **Prompts** | Templates de prompt prédéfinis | System instructions, audit workflows |

### Boucle d'Interaction

```
1. USER → Requête en langage naturel
2. LLM → Découvre les outils disponibles (tool discovery)
3. LLM → Invoque le tool MCP approprié
4. MCP Server → Exécute la logique (API, DB, etc.)
5. MCP Server → Retourne données structurées au LLM
6. LLM → Synthétise une réponse humaine
```

---

## 2. Architecture Serveur

### Structure Projet Recommandée (Python)

```
my-mcp-server/
├── src/
│   ├── __init__.py
│   ├── server.py          # Point d'entrée MCP (FastMCP)
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── core.py        # Tools principaux
│   │   └── reports.py     # Tools de reporting
│   ├── services/
│   │   ├── __init__.py
│   │   └── api_client.py  # Client API wrappé
│   └── prompts/
│       └── setup.md       # Prompt de configuration rapide
├── tests/
│   ├── test_tools.py
│   └── test_integration.py
├── Dockerfile             # Multi-stage build
├── requirements.txt
├── pyproject.toml
└── README.md
```

### Transports

| Type | Use | Recommandation |
|------|-----|----------------|
| **Stdio** | Local, développement | ✅ Dev & test rapide |
| **SSE** | ❌ Deprecated (supprimé juin 2025) | Ne PAS utiliser |
| **Streamable HTTP** | ✅ **Standard actuel** — Remote, multi-client | ✅ Production (Cloud Run) |

> [!WARNING]
> **SSE est deprecated.** Utiliser `StreamableHTTPConnectionParams` pour tout nouveau serveur.
> Voir aussi le skill `adk-creation` §5.3 pour l'intégration MCP dans un agent ADK.

### Framework Recommandé : FastMCP (Python)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="my-mcp-server",
    instructions="Description du serveur pour l'IA."
)

@mcp.tool(description="Exécute une requête sur l'API X.")
def execute_query(query: str, limit: int = 50) -> str:
    """Exécute une requête et retourne les résultats formatés.
    
    Args:
        query: La requête à exécuter.
        limit: Nombre maximum de résultats (défaut: 50).
    
    Returns:
        Résultats formatés en JSON.
    """
    # ... logique API ...
    return json.dumps(results, indent=2)
```

---

## 3. Tool Design Principles

### Règles de Conception

| Principe | Description | Exemple |
|----------|-------------|---------|
| **Nom action-oriented** | Verbe + objet | `get_insights`, `list_products`, `create_campaign` |
| **Single purpose** | Un tool = une action | Pas de tool "do_everything" |
| **Input validé** | Schema typé + descriptions | `query: str`, `limit: int = 50` |
| **Output structuré** | JSON prévisible | `{"data": [...], "total": 42}` |
| **Description explicite** | Le LLM choisit les outils par description | Docstring détaillée et précise |

### Pattern : Consolidation d'Outils

> [!TIP]
> **Préférer peu de tools puissants plutôt que beaucoup de tools spécialisés.**
> Le pattern EdgeAngel (Meta Ads, Merchant Center) consolide en 3-4 tools maximum :

```python
# ❌ Mauvais : 12 tools atomiques
@mcp.tool() def get_campaigns(): ...
@mcp.tool() def get_adsets(): ...
@mcp.tool() def get_ads(): ...
# × 12 = cognitive overload pour le LLM

# ✅ Bon : 3-4 tools consolidés avec routing interne
@mcp.tool(description="Execute CRUD operations on Meta Ads entities.")
def execute(entity: str, action: str, params: str = "{}") -> str:
    """
    entity: campaigns, ad_sets, ads, creatives, images, ...
    action: list, get, create, update
    params: JSON string of parameters
    """
    # Router interne vers la bonne logique
```

### Documentation Intégrée : `get_doc`

Pattern recommandé — un tool qui expose la documentation du MCP :

```python
@mcp.tool(description="Get built-in documentation for the MCP.")
def get_doc(topic: str = "overview") -> str:
    """
    Args:
        topic: overview, execute, insights, targeting, ...
    """
    docs = {
        "overview": "# Overview\n...",
        "execute": "# Execute Reference\n...",
    }
    return docs.get(topic, f"Topic '{topic}' not found. Available: {list(docs.keys())}")
```

> [!IMPORTANT]
> Ajouter dans le `get_doc("overview")` un hint vers `google-developer-knowledge` :
> ```
> 💡 Pour approfondir, utiliser le MCP google-developer-knowledge :
> search_documents("Google Merchant Center API product data")
> ```

### Input Schema Design

| Champ | Requis ? | Notes |
|-------|----------|-------|
| Type hints Python | **Oui** | `str`, `int`, `float`, `bool`, `list` |
| Valeurs par défaut | Recommandé | Réduisent la friction (`limit: int = 50`) |
| Docstring Args | **Oui** | Le LLM utilise la docstring pour décider |
| Description param | **Oui** | JSON-friendly, pas d'ambiguïté |

---

## 4. Patterns de Réponse

### Format Standard

```python
# ✅ Réponse structurée
return json.dumps({
    "status": "success",
    "data": results,
    "metadata": {
        "total": len(results),
        "query": original_query
    }
}, indent=2)

# ✅ Réponse d'erreur
return json.dumps({
    "status": "error",
    "error": "Invalid account ID",
    "hint": "Use list(accounts) to see available accounts."
})
```

### Gestion du Volume de Données

> [!CAUTION]
> **Le volume de réponse est critique.** Des réponses trop volumineuses saturent le context window du LLM et dégradent les performances.

| Stratégie | Quand |
|-----------|-------|
| Pagination | Données volumineuses (products, campaigns) |
| Troncature intelligente | Top N résultats + compteur total |
| Agrégation | Métriques résumées plutôt que lignes brutes |
| Format compact | Supprimer les champs vides/null |

```python
# Pattern : troncature avec signal
if len(results) > MAX_RESULTS:
    return json.dumps({
        "data": results[:MAX_RESULTS],
        "truncated": True,
        "total_available": len(results),
        "hint": f"Showing first {MAX_RESULTS}. Use offset parameter for more."
    })
```

---

## 5. Error Handling

### Stratégie de Gestion d'Erreurs

```python
@mcp.tool()
def execute(entity: str, action: str, params: str = "{}") -> str:
    try:
        parsed = json.loads(params)
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON params: {e}"})
    
    try:
        result = _route_action(entity, action, parsed)
        return json.dumps({"status": "success", "data": result})
    except PermissionError:
        return json.dumps({
            "error": "Permission denied",
            "hint": "Check API credentials and account access."
        })
    except Exception as e:
        return json.dumps({
            "error": f"Unexpected error: {type(e).__name__}: {str(e)}",
            "hint": "Check get_doc() for correct parameters."
        })
```

### Règles

- **Ne jamais exposer** de stack traces ou de secrets dans les réponses
- **Toujours fournir** un `hint` actionnable dans les erreurs
- **Logger** les erreurs côté serveur pour le debugging
- **Distinguer** erreurs client (params invalides) et serveur (API down)

---

## 6. Sécurité

### Principes

| Domaine | Règle |
|---------|-------|
| **Credentials** | Variables d'environnement — jamais hardcodées |
| **Input validation** | Valider TOUS les paramètres avant exécution |
| **Rate limiting** | Protéger les APIs sous-jacentes |
| **Read-only par défaut** | Les mutations nécessitent une confirmation explicite |
| **Secrets** | Ne jamais logger ni retourner de tokens/clés |

### Pattern : Credentials via Env

```python
import os

class Config:
    API_TOKEN = os.environ.get("MY_API_TOKEN")
    ACCOUNT_ID = os.environ.get("MY_ACCOUNT_ID")
    
    @classmethod
    def validate(cls):
        missing = [k for k, v in {
            "MY_API_TOKEN": cls.API_TOKEN,
            "MY_ACCOUNT_ID": cls.ACCOUNT_ID,
        }.items() if not v]
        if missing:
            raise ValueError(f"Missing env vars: {', '.join(missing)}")
```

---

## 7. Déploiement Cloud Run

### Dockerfile Multi-stage

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY src/ ./src/
EXPOSE 8080
CMD ["python", "-m", "src.server"]
```

### Point d'Entrée Streamable HTTP

```python
# src/server.py
import uvicorn
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="my-server", instructions="...")

# ... définition des tools ...

if __name__ == "__main__":
    # Mode Streamable HTTP pour Cloud Run
    uvicorn.run(
        mcp.get_asgi_app(),
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
    )
```

### Déploiement

```bash
# Build & push
gcloud builds submit --tag gcr.io/$PROJECT_ID/my-mcp-server

# Deploy
gcloud run deploy my-mcp-server \
  --image gcr.io/$PROJECT_ID/my-mcp-server \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars "MY_API_TOKEN=xxx" \
  --memory 512Mi \
  --min-instances 0 \
  --max-instances 3
```

> [!TIP]
> Pour les détails de déploiement Cloud Run, voir le skill `cloudrun-deploy`.
> Pour la doc officielle : `search_documents("deploy remote MCP server Cloud Run streamable HTTP")`.

---

## 8. Configuration Client

### Antigravity / Gemini CLI

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "@my-org/my-mcp-server"],
      "env": {
        "MY_API_TOKEN": "xxx"
      }
    }
  }
}
```

### Pour un serveur distant (Cloud Run)

```json
{
  "mcpServers": {
    "my-server": {
      "url": "https://my-mcp-server.run.app/mcp"
    }
  }
}
```

---

## 9. Testing

### Catégories de Tests

| Type | Focus | Priorité |
|------|-------|----------|
| **Unit** | Logique métier de chaque tool | ⭐⭐⭐ |
| **Integration** | Serveur complet + API réelles | ⭐⭐ |
| **Contract** | Validation schemas input/output | ⭐⭐ |
| **E2E** | Test via un client MCP réel | ⭐ |

### Pattern Test Unitaire

```python
import pytest
from src.tools.core import execute

def test_execute_list_campaigns():
    result = json.loads(execute("campaigns", "list", '{"account_id": "123"}'))
    assert result["status"] == "success"
    assert isinstance(result["data"], list)

def test_execute_invalid_params():
    result = json.loads(execute("campaigns", "list", "not-json"))
    assert "error" in result
```

---

## 10. Checklist Qualité

### Avant Déploiement

- [ ] Noms de tools action-oriented et sans ambiguïté
- [ ] Schémas d'input complets avec descriptions et types
- [ ] Output JSON structuré et compact
- [ ] Error handling sur tous les chemins d'erreur
- [ ] Validation des inputs utilisateur
- [ ] Credentials via variables d'environnement
- [ ] `get_doc()` tool avec documentation intégrée
- [ ] Hint vers `google-developer-knowledge` dans `get_doc`
- [ ] Tests unitaires sur chaque tool
- [ ] Dockerfile multi-stage optimisé
- [ ] README avec setup rapide et exemples
- [ ] Réponses tronquées si volumineuses (pagination)

### Patterns EdgeAngel Validés

| Pattern | Utilisé dans |
|---------|-------------|
| Consolidation 3-4 tools | Meta Ads, Merchant Center |
| `get_doc()` intégré | Meta Ads, Merchant Center |
| Router `entity/action` | Meta Ads, Merchant Center |
| Hint google-developer-knowledge | Merchant Center |
| Read-only par défaut | Google Ads, Google Analytics |

---

## 11. Références

- [Spécification MCP](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Google Cloud MCP servers](https://cloud.google.com/mcp/overview)
- [Déploiement MCP sur Cloud Run](https://cloud.google.com/run/docs/tutorials/deploy-remote-mcp-server)
- [Google Ads MCP server (officiel)](https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server)
- [Merchant API MCP devdocs](https://developers.google.com/merchant/api/guides/devdocs-mcp)

> [!TIP]
> Pour explorer la doc Google officielle sur MCP et les APIs :
> ```
> search_documents("MCP server Cloud Run deployment")
> search_documents("Google Cloud MCP servers overview")
> ```
