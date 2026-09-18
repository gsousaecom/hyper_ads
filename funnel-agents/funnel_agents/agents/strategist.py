"""Agente Estrategista: define o ângulo e a estrutura da página."""

from .base import Agent

ESTRUTURAS = {
    "advertorial": (
        "Advertorial (matéria editorial que vende): manchete jornalística, "
        "história/descoberta, mecanismo do problema, apresentação da solução, "
        "provas, depoimentos, oferta e CTA repetido."
    ),
    "listicle": (
        "Listicle ('X motivos pelos quais...'): título numerado chamativo, "
        "introdução curta com gancho, itens numerados que constroem desejo, "
        "sendo o último item a oferta com CTA."
    ),
    "quiz": (
        "Quiz interativo: promessa de resultado personalizado, 4 a 7 perguntas "
        "de múltipla escolha que qualificam e engajam, tela de 'analisando "
        "respostas' e página de resultado que recomenda o produto com CTA."
    ),
    "pdp": (
        "PDP (página de produto): título com benefício, galeria/descrição do "
        "produto, bullets de benefícios, provas sociais, garantia, FAQ com "
        "respostas a objeções e bloco de compra com CTA fixo."
    ),
    "presell": (
        "Presell/bridge page: página curta de aquecimento entre o anúncio e a "
        "oferta — gancho forte, 3 a 5 blocos de convencimento e um único CTA."
    ),
}


class Strategist(Agent):
    name = "estrategista"
    effort = "high"
    system_prompt = (
        "Você é um estrategista sênior de funis de resposta direta para "
        "e-commerce. Sua função é transformar um brief de produto em um plano "
        "de página claro para o copywriter e o web designer executarem.\n\n"
        "Entregue, em markdown:\n"
        "1. **Ângulo principal** — a grande ideia da página e por que ela "
        "funciona para esse público.\n"
        "2. **Estrutura seção a seção** — cada seção com objetivo, conteúdo "
        "esperado e gatilhos de persuasão usados.\n"
        "3. **Diretrizes de conversão** — posicionamento de CTAs, tratamento "
        "das objeções do brief e uso das provas sociais.\n\n"
        "Seja específico para o produto do brief; nada de plano genérico. "
        "Não escreva a copy final — isso é papel do copywriter."
    )

    def build_input(self, brief_text: str, tipo_pagina: str) -> str:
        return (
            f"BRIEF DO PRODUTO:\n{brief_text}\n\n"
            f"FORMATO DA PÁGINA: {ESTRUTURAS[tipo_pagina]}\n\n"
            "Monte o plano estratégico dessa página."
        )
