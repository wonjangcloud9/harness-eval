"""Rich console reporter for scorecard."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from harness_eval.models import Scorecard


def print_scorecard(card: Scorecard) -> None:
    """Pretty-print a scorecard to the terminal."""
    console = Console()
    table = Table(title="Harness Engineering Scorecard")
    table.add_column("Dimension", style="cyan")
    table.add_column("Score", justify="right")
    table.add_column("Details", style="dim")

    for d in card.dimensions:
        pct = d.score / d.max_score * 100
        color = _score_color(pct)
        table.add_row(
            d.name,
            f"[{color}]{pct:.0f}%[/{color}]",
            "; ".join(d.details),
        )

    console.print(table)
    total_color = _score_color(card.percentage)
    console.print(
        Panel(
            f"[bold {total_color}]"
            f"{card.percentage:.0f}%"
            f"[/bold {total_color}]",
            title="Overall Score",
        )
    )


def _score_color(pct: float) -> str:
    if pct >= 70:
        return "green"
    if pct >= 40:
        return "yellow"
    return "red"
