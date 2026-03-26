"""Rich console reporter for scorecard."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from harness_eval.models import Scorecard

_console = Console()


def print_scorecard(card: Scorecard) -> None:
    """Pretty-print a scorecard to the terminal."""
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

    _console.print(table)
    total_color = _score_color(card.percentage)
    _console.print(
        Panel(
            f"[bold {total_color}]"
            f"{card.percentage:.0f}%"
            f"[/bold {total_color}]",
            title="Overall Score",
        )
    )


def print_recommendations(recs: list[dict]) -> None:
    """Print improvement recommendations."""
    _console.print()
    _console.print("[bold]Recommendations[/bold] (lowest score first):")
    for rec in recs:
        dim = rec["dimension"]
        pct = rec["current_pct"]
        color = _score_color(pct)
        _console.print(
            f"\n  [{color}]{dim} ({pct:.0f}%)[/{color}]"
        )
        for s in rec["suggestions"]:
            _console.print(f"    - {s}")


def _score_color(pct: float) -> str:
    if pct >= 70:
        return "green"
    if pct >= 40:
        return "yellow"
    return "red"
