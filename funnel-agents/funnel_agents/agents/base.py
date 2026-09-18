"""Agente base: encapsula a chamada à API com streaming e fallback."""

from __future__ import annotations

import sys

import anthropic

from ..config import FALLBACK_BETA, MAX_TOKENS, MODEL


class Agent:
    """Um agente especializado com system prompt próprio.

    Cada agente faz uma chamada única e stateless: recebe o contexto
    acumulado da pipeline e devolve seu texto. O orquestrador é quem
    encadeia as saídas.
    """

    name: str = "agente"
    system_prompt: str = ""
    effort: str = "high"

    def __init__(self, client: anthropic.Anthropic):
        self.client = client

    def run(self, user_message: str) -> str:
        print(f"→ [{self.name}] trabalhando...", file=sys.stderr)
        # Streaming evita timeouts em saídas longas; o system prompt fixo
        # é cacheado para baratear execuções repetidas.
        with self.client.beta.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            betas=[FALLBACK_BETA],
            fallbacks="default",
            output_config={"effort": self.effort},
            system=[
                {
                    "type": "text",
                    "text": self.system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            response = stream.get_final_message()

        if response.stop_reason == "refusal":
            detalhe = ""
            if response.stop_details and response.stop_details.explanation:
                detalhe = f" ({response.stop_details.explanation})"
            raise RuntimeError(f"[{self.name}] pedido recusado pela API{detalhe}")
        if response.stop_reason == "max_tokens":
            raise RuntimeError(
                f"[{self.name}] resposta truncada em {MAX_TOKENS} tokens; "
                "aumente MAX_TOKENS em config.py"
            )

        texto = "".join(b.text for b in response.content if b.type == "text")
        if not texto.strip():
            raise RuntimeError(f"[{self.name}] resposta vazia")
        return texto
