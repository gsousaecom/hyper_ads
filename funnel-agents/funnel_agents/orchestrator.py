"""Orquestrador: encadeia os agentes e salva os artefatos."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from .agents.copywriter import Copywriter
from .agents.designer import Designer
from .agents.reviewer import Reviewer
from .agents.strategist import Strategist
from .brief import Brief
from .config import get_client


@dataclass
class Result:
    plano: str
    copy: str
    html: str
    output_dir: Path


def _extract_html(texto: str) -> str:
    """Isola o documento HTML, tolerando cercas de código ou preâmbulo."""
    match = re.search(r"<!DOCTYPE html.*?</html>", texto, re.IGNORECASE | re.DOTALL)
    return match.group(0) if match else texto.strip()


def run_pipeline(brief: Brief, output_dir: str | Path, revisar: bool = True) -> Result:
    """Executa Estrategista → Copywriter → Web Designer (→ Revisor)."""
    client = get_client()
    brief_text = brief.to_prompt()

    estrategista = Strategist(client)
    plano = estrategista.run(estrategista.build_input(brief_text, brief.tipo_pagina))

    copywriter = Copywriter(client)
    copy_raw = copywriter.run(copywriter.build_input(brief_text, plano))
    # A lista pós ---VALIDACAO--- vai para o setor de validação; nunca entra na página.
    copy_final, _, validacao = copy_raw.partition("---VALIDACAO---")
    copy_final = copy_final.strip()
    validacao = validacao.strip()

    designer = Designer(client)
    html = _extract_html(designer.run(designer.build_input(brief_text, copy_final)))

    if revisar:
        revisor = Reviewer(client)
        html = _extract_html(revisor.run(revisor.build_input(brief_text, copy_final, html)))

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", brief.produto.lower()).strip("-") or "pagina"
    base = f"{slug}-{brief.tipo_pagina}"
    (out / f"{base}-plano.md").write_text(plano, encoding="utf-8")
    (out / f"{base}-copy.md").write_text(copy_final, encoding="utf-8")
    if validacao:
        (out / f"{base}-validacao.md").write_text(validacao + "\n", encoding="utf-8")
    html_path = out / f"{base}.html"
    html_path.write_text(html, encoding="utf-8")

    print(f"✔ Página gerada: {html_path}", file=sys.stderr)
    return Result(plano=plano, copy=copy_final, html=html, output_dir=out)
