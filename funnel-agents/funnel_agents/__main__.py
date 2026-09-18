"""CLI: python -m funnel_agents --brief examples/brief_exemplo.json"""

import argparse
import sys

from .brief import PAGE_TYPES, Brief
from .orchestrator import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="funnel_agents",
        description="Gera páginas de funil (advertorial, listicle, quiz, PDP, presell) com agentes de IA.",
    )
    parser.add_argument("--brief", required=True, help="Caminho do brief em JSON")
    parser.add_argument(
        "--tipo",
        choices=PAGE_TYPES,
        help="Sobrescreve o tipo_pagina do brief",
    )
    parser.add_argument("-o", "--output", default="output", help="Pasta de saída (padrão: output/)")
    parser.add_argument(
        "--sem-revisao",
        action="store_true",
        help="Pula o agente revisor (mais rápido e barato)",
    )
    args = parser.parse_args()

    brief = Brief.from_json(args.brief)
    if args.tipo:
        brief.tipo_pagina = args.tipo

    try:
        run_pipeline(brief, args.output, revisar=not args.sem_revisao)
    except Exception as exc:  # noqa: BLE001 - CLI: mostrar erro legível
        print(f"Erro: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
