"""Brief do produto: a entrada da pipeline de agentes."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

# Tipos de página de funil suportados.
PAGE_TYPES = ("advertorial", "listicle", "quiz", "pdp", "presell")


@dataclass
class Brief:
    produto: str
    descricao: str
    publico_alvo: str
    oferta: str
    tipo_pagina: str = "advertorial"
    idioma: str = "pt-BR"
    tom: str = "conversacional e persuasivo"
    diferenciais: list[str] = field(default_factory=list)
    objecoes: list[str] = field(default_factory=list)
    provas_sociais: list[str] = field(default_factory=list)
    url_checkout: str = "#"
    observacoes: str = ""

    def __post_init__(self) -> None:
        if self.tipo_pagina not in PAGE_TYPES:
            raise ValueError(
                f"tipo_pagina '{self.tipo_pagina}' inválido. Use um de: {', '.join(PAGE_TYPES)}"
            )

    @classmethod
    def from_json(cls, path: str | Path) -> "Brief":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(**data)

    def to_prompt(self) -> str:
        """Serializa o brief em texto para os prompts dos agentes."""
        linhas = [
            f"Produto: {self.produto}",
            f"Descrição: {self.descricao}",
            f"Público-alvo: {self.publico_alvo}",
            f"Oferta: {self.oferta}",
            f"Tipo de página: {self.tipo_pagina}",
            f"Idioma: {self.idioma}",
            f"Tom de voz: {self.tom}",
            f"URL do checkout/CTA: {self.url_checkout}",
        ]
        if self.diferenciais:
            linhas.append("Diferenciais: " + "; ".join(self.diferenciais))
        if self.objecoes:
            linhas.append("Objeções comuns: " + "; ".join(self.objecoes))
        if self.provas_sociais:
            linhas.append("Provas sociais: " + "; ".join(self.provas_sociais))
        if self.observacoes:
            linhas.append(f"Observações: {self.observacoes}")
        return "\n".join(linhas)
