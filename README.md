# GPAC MCP Server

Ce dépôt contient un serveur MCP permettant d'interroger la documentation GPAC.

## Construction de l'image Docker

```bash
docker build -t gpac-mcp-server -f RAG/backend/DockerFile RAG/backend
```

## Lancement du conteneur

```bash
docker run -p 8000:8000 gpac-mcp-server
```

Le serveur sera alors disponible sur `http://localhost:8000` (ou l'adresse de
votre machine). Configurez Claude Desktop pour utiliser cette URL afin de
contacter l'instance MCP sans devoir la lancer manuellement à chaque fois.

