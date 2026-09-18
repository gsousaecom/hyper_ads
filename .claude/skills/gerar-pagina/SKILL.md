---
name: gerar-pagina
description: Gera páginas de conversão completas (PDP, advertorial, listicle, long-form, VSL page, landing, upsell/downsell, quiz, presell) orquestrando os subagentes funil-estrategista, funil-copywriter, funil-web-designer e funil-revisor segundo a metodologia da casa (references/). Use quando o usuário pedir página, copy, arquitetura, HTML ou variação A/B de página de funil.
---

# Gerar página de funil

Você é o orquestrador da pipeline COPYWRITER & PAGE BUILDER. A metodologia completa vive em `references/` (nesta pasta): Master Instructions (01), Persuasion Engine (02), Page Type Router (03), Section Library (04), Copy Router (05), Playbooks (06), Design System (07), HTML Standards (08), Copy QC (09), Reference-First (10), Intake & Commands (11). North Star: **THESIS + READER STATE + PAGE JOB + PRODUCT REALITY + PAGE TYPE + REFERENCES**.

## Intake

Input ideal (comece com o que existir; não force interrogatório): PAGE REQUEST, Marketing Thesis, One Belief, Avatar/Research, Copy Truth (claims, preço, oferta, garantia, provas fornecidas), Offer, Brand/Visual Identity, Market/Language, Target platform (standalone | Shopify/snippet). Pergunte apenas o que muda fundamentalmente a estratégia; decisões de ofício são suas. Salve briefs recebidos em `funis/briefs/<slug>.json` ou `.md`.

## Escopos (comandos do arquivo 11)

O usuário pode pedir o workflow completo ou só uma parte. Execute o escopo pedido; não force onboarding nem aprovação intermediária:

- **/page (padrão)** — pipeline completa: estrategista → copywriter → web designer → revisor.
- **/architecture** — só o funil-estrategista (routing, belief gaps, arquitetura de seções).
- **/copy** — copywriter usando arquitetura existente (ou crie a mínima via estrategista antes). Sem HTML.
- **/html** — copy/arquitetura já fornecidas ou aprovadas → direto ao web designer (+ revisor). Não obrigue nova aprovação.
- **/pdp, /advertorial, /longform, /listicle** — pipeline completa com o Page Type já roteado (o estrategista escolhe o subtype pelo Playbook).
- **/redteam** — spawne o funil-revisor em modo ataque: Page Type Integrity, belief gaps, genericness, sequencing, offer clarity, visual logic, conversion friction. Sem editar; devolve relatório.
- **/ab** — variação com hipótese explícita de uma página existente; mude poucas variáveis e declare-as.

## Pipeline (sequencial — cada etapa depende da anterior)

Use o tool Agent com os subagentes nomeados (`funil-estrategista`, `funil-copywriter`, `funil-web-designer`, `funil-revisor`). Se um subagente não estiver registrado na sessão, leia o `.claude/agents/<nome>.md` e spawne um agente `general-purpose` com o corpo como instrução. Ao repassar saídas entre etapas, repasse o conteúdo COMPLETO, sem resumir — ou salve em arquivo e passe o caminho (preferível para textos longos).

1. **funil-estrategista** — entrada: brief/thesis/Copy Truth + page request. Saída: routing + reader state + belief gap map + section architecture.
2. **funil-copywriter** — entrada: brief + arquitetura. Saída: copy final + seção `---VALIDACAO---`.
3. **funil-web-designer** — entrada: brief (com plataforma-alvo e URL de checkout se houver) + copy final (sem a seção de validação) + tratamento visual da arquitetura. Saída: HTML.
4. **funil-revisor** — entrada: brief + copy aprovada + HTML. Saída: HTML final. (Pule se o usuário pedir "sem revisão".)

## Saída

1. Extraia o documento HTML (do `<!DOCTYPE html` ao `</html>`, ignorando preâmbulo/cercas) — ou o snippet, quando a plataforma-alvo for Shopify/page builder.
2. Salve em `funis/paginas/<slug>-<tipo>.html`, com `...-arquitetura.md` (saída do estrategista) e `...-copy.md` (sem a seção de validação).
3. Se houver lista após `---VALIDACAO---`, salve em `...-validacao.md` — relatório para o setor de validação da empresa. Nunca entra na copy nem no HTML.
4. Envie o HTML ao usuário com SendUserFile (display: render).
5. Resuma em 2–3 frases: Page Type/subtype roteado, ângulo/One Belief e onde estão os arquivos.

## Regras

- A página e a copy saem limpas: sem marcadores de validação, disclaimers ou avisos criados pelos agentes. Placeholders técnicos de asset (`[PRODUCT_IMAGE_01]`, `[UGC_VIDEO_01]`, `[CHECKOUT_URL]`...) são intencionais e ficam até o dono substituir.
- Page Type = gramática; Belief Gaps = seções; References = repertório; Copy Truth = limites factuais; Thesis/One Belief = direção persuasiva; HTML = implementação final.
- O que você assumir de ofício, liste no resumo final.
- Vários formatos para o mesmo produto = uma pipeline por formato.
- Quando existir `references/00_VISUAL_REFERENCE_INDEX.md` (Visual Reference Library), o web designer aplica o Reference-First Protocol; sem ele, constrói pela gramática do Page Type.
