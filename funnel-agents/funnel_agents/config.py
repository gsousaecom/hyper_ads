"""Configuração central do projeto: cliente da API e modelos."""

import anthropic

# Modelo principal usado por todos os agentes.
MODEL = "claude-opus-5"

# Limite de saída por agente. Páginas completas (HTML + copy longa) podem
# ser extensas, então usamos streaming com um teto alto.
MAX_TOKENS = 64000

# Flag beta do fallback server-side: se um pedido for recusado pelos
# classificadores de segurança, a API repete a chamada em um modelo de
# fallback dentro da mesma requisição.
FALLBACK_BETA = "server-side-fallback-2026-07-01"


def get_client() -> anthropic.Anthropic:
    """Cria o cliente. Lê ANTHROPIC_API_KEY (ou perfil `ant auth login`)."""
    return anthropic.Anthropic()
