"""funnel_agents: equipe de agentes de IA que gera páginas de funil."""

from .brief import Brief
from .orchestrator import Result, run_pipeline

__all__ = ["Brief", "Result", "run_pipeline"]
