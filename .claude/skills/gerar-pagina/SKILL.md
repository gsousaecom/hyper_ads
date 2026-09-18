---
name: gerar-pagina
description: Gera uma página de funil completa (advertorial, listicle, quiz, PDP ou presell) orquestrando os subagentes funil-estrategista, funil-copywriter, funil-web-designer e funil-revisor. Use quando o usuário pedir para gerar/criar uma página de funil, advertorial, listicle, quiz, PDP ou presell para um produto.
---

# Gerar página de funil

Você é o orquestrador de uma pipeline de 4 agentes que transforma um brief de produto em uma página de funil pronta (HTML único, mobile-first).

## Entrada

O usuário fornece um brief de uma destas formas:

1. Caminho de um JSON em `funis/briefs/` (formato do `funis/briefs/brief_exemplo.json`);
2. Descrição livre no chat — nesse caso, monte o brief você mesmo com os campos: produto, descricao, publico_alvo, oferta, tipo_pagina (advertorial | listicle | quiz | pdp | presell), idioma, tom, diferenciais, objecoes, provas_sociais, url_checkout, observacoes. Se faltar algo essencial (produto, oferta ou tipo de página), pergunte antes de começar. Salve o brief montado em `funis/briefs/<slug>.json`.

Serialize o brief em texto legível (campo: valor, um por linha) — chamado de BRIEF abaixo.

## Pipeline (sequencial — cada etapa depende da anterior)

Execute cada etapa com o tool Agent, usando o subagente nomeado. Se um subagente não estiver registrado nesta sessão (agentes recém-criados exigem reinício), leia o arquivo `.claude/agents/<nome>.md` correspondente e spawne um agente `general-purpose` passando o corpo do arquivo como instrução, mais a entrada da etapa.

1. **funil-estrategista** — entrada: BRIEF + tipo de página. Saída: PLANO (markdown).
2. **funil-copywriter** — entrada: BRIEF + PLANO. Saída: COPY (markdown).
3. **funil-web-designer** — entrada: BRIEF + COPY. Saída: HTML.
4. **funil-revisor** — entrada: BRIEF + COPY + HTML. Saída: HTML final. (Pule esta etapa se o usuário pedir rapidez com "sem revisão".)

Ao repassar saídas entre etapas, repasse o conteúdo COMPLETO, sem resumir.

## Saída

1. Extraia o documento HTML da resposta final (do `<!DOCTYPE html` ao `</html>`, ignorando qualquer preâmbulo ou cerca de código).
2. Salve em `funis/paginas/<slug-do-produto>-<tipo>.html`; salve também o plano em `...-plano.md` e a copy em `...-copy.md` (sem a seção `---VALIDACAO---`).
3. Se o copywriter devolveu uma lista após `---VALIDACAO---`, salve-a em `...-validacao.md` — é o relatório para o setor de validação da empresa. Ela nunca entra na copy nem no HTML.
4. Envie o HTML ao usuário com SendUserFile (display: render) para pré-visualização.
5. Resuma em 2–3 frases: ângulo escolhido e onde estão os arquivos gerados.

## Regras

- A página e a copy saem limpas: sem marcadores de validação, placeholders de compliance, disclaimers ou avisos criados pelos agentes. A checagem de claims é responsabilidade do setor de validação da empresa, que usa o arquivo `-validacao.md`.
- Não invente campos do brief silenciosamente: o que você assumir, liste no resumo final.
- Vários formatos para o mesmo produto = rodar a pipeline uma vez por formato (o plano e a copy são específicos do formato).
