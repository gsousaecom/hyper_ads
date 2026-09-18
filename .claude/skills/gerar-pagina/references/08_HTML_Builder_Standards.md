# HTML BUILDER STANDARDS

## Standalone
Documento completo com doctype, head, responsive meta, semantic HTML, CSS e JS mínimo.

## Snippet / Page Builder / Shopify
Não adicionar html/body/head. Namespacing obrigatório no CSS. Evitar selectors globais, resets agressivos e JS que interfira na plataforma. Respeitar classes/containers existentes quando informados.

## Code Quality
- semantic sections;
- reusable CSS variables;
- mobile-first ou breakpoints claros;
- accessible buttons/links/forms;
- alt text quando asset conhecido;
- lazy loading para mídia abaixo da dobra quando apropriado;
- evitar bibliotecas externas desnecessárias;
- evitar inline JS repetitivo;
- sem URLs/assets inventados.

## Placeholders
Use marcadores explícitos:
`[PRODUCT_IMAGE_01]`, `[UGC_VIDEO_01]`, `[REVIEW_REAL_01]`, `[CHECKOUT_URL]`.

## Preview QA
Quando renderização estiver disponível:
1. render desktop;
2. render mobile;
3. revisar hierarchy, overflow, line length, spacing, media crop, CTA visibility, sticky elements;
4. corrigir;
5. entregar final.

## Performance
Evite imagens enormes, fontes excessivas, scripts supérfluos e layout shift.

## Accessibility
Contraste suficiente, focus states, labels, semantic headings, controles acionáveis por teclado.