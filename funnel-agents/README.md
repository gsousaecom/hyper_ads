# Funnel Agents

Equipe de agentes de IA (API da Anthropic) que gera **páginas de funil completas** a partir de um brief de produto: advertorial, listicle, quiz interativo, PDP e presell — copy + HTML prontos para publicar.

## Como funciona

Pipeline de 4 agentes especializados, orquestrados em código:

```
Brief (JSON)
   │
   ▼
1. Estrategista  → define o ângulo e a estrutura da página
   ▼
2. Copywriter    → escreve toda a copy, seção por seção
   ▼
3. Web Designer  → gera o HTML/CSS/JS completo (arquivo único, mobile-first)
   ▼
4. Revisor       → QA: português, copy fiel, CTAs corretos, HTML válido
   ▼
output/<produto>-<tipo>.html  (+ plano.md e copy.md)
```

Cada agente usa `claude-opus-5` com streaming, prompt caching no system prompt e fallback automático server-side em caso de recusa.

## Instalação

```bash
cd funnel-agents
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sua-chave"   # ou use `ant auth login`
```

## Uso

```bash
# Gera um advertorial a partir do brief de exemplo
python -m funnel_agents --brief examples/brief_exemplo.json

# Mesmo brief, outro formato de página
python -m funnel_agents --brief examples/brief_exemplo.json --tipo quiz

# Mais rápido/barato: pula o agente revisor
python -m funnel_agents --brief examples/brief_exemplo.json --sem-revisao
```

Saída em `output/`: o HTML final da página, o plano estratégico e a copy em markdown (para editar e regenerar se quiser).

## O brief

Copie `examples/brief_exemplo.json` e preencha com seu produto. Campos: `produto`, `descricao`, `publico_alvo`, `oferta`, `tipo_pagina` (`advertorial` | `listicle` | `quiz` | `pdp` | `presell`), `idioma`, `tom`, `diferenciais`, `objecoes`, `provas_sociais`, `url_checkout`, `observacoes`.

Os agentes têm liberdade criativa para promessas, ângulos, narrativas e provas alinhadas à tese do produto/marca — a página e a copy saem limpas, sem marcadores ou disclaimers. Os elementos de prova criados pelos agentes são listados à parte em `...-validacao.md`, o relatório para o setor de validação da empresa. Quanto melhor o brief, melhor a página.

## Uso como biblioteca

```python
from funnel_agents import Brief, run_pipeline

brief = Brief.from_json("examples/brief_exemplo.json")
resultado = run_pipeline(brief, output_dir="output")
print(resultado.html[:200])
```

## Estrutura

```
funnel-agents/
├── funnel_agents/
│   ├── config.py            # modelo, limites, cliente da API
│   ├── brief.py             # dataclass do brief + tipos de página
│   ├── orchestrator.py      # pipeline e gravação dos artefatos
│   ├── __main__.py          # CLI
│   └── agents/
│       ├── base.py          # chamada à API (streaming, cache, fallback)
│       ├── strategist.py
│       ├── copywriter.py
│       ├── designer.py
│       └── reviewer.py
├── examples/brief_exemplo.json
└── requirements.txt
```

Este diretório é autocontido — pode ser extraído para um repositório próprio sem mudanças.
