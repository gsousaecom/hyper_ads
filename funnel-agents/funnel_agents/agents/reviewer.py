"""Agente Revisor: QA final do HTML gerado."""

from .base import Agent


class Reviewer(Agent):
    name = "revisor"
    effort = "medium"
    system_prompt = (
        "Você é um revisor de QA de páginas de funil. Você recebe o brief, a "
        "copy aprovada e o HTML gerado, e devolve o HTML FINAL corrigido.\n\n"
        "Verifique e corrija diretamente no código:\n"
        "- Erros de português e de digitação.\n"
        "- Copy faltando ou trocada em relação à copy aprovada.\n"
        "- Links de CTA que não apontam para a URL de checkout do brief.\n"
        "- HTML/JS quebrado (tags não fechadas, quiz que não avança).\n"
        "- Coerência com a tese do produto/marca: promessas e narrativas "
        "criadas pelos agentes são permitidas, mas devem estar alinhadas ao "
        "brief e não contradizer as observações dele.\n"
        "- Depoimentos, números ou estudos que não estão no brief devem "
        "carregar o marcador [VALIDAR: ...] visível; adicione o marcador "
        "onde faltar em vez de remover a prova.\n\n"
        "Responda APENAS com o código HTML final, começando em "
        "<!DOCTYPE html> e terminando em </html>. Se nada precisar mudar, "
        "devolva o HTML recebido na íntegra."
    )

    def build_input(self, brief_text: str, copy_final: str, html: str) -> str:
        return (
            f"BRIEF DO PRODUTO:\n{brief_text}\n\n"
            f"COPY APROVADA:\n{copy_final}\n\n"
            f"HTML GERADO:\n{html}\n\n"
            "Revise e devolva o HTML final."
        )
