"""CLI entry point for harness-eval."""

import click

from harness_eval.reporters.console import print_scorecard
from harness_eval.scanner import scan


@click.command()
@click.argument(
    "path",
    default=".",
    type=click.Path(exists=True),
)
@click.option(
    "--json", "as_json",
    is_flag=True,
    help="Output as JSON",
)
def main(path: str, as_json: bool) -> None:
    """Evaluate harness engineering quality."""
    card = scan(path)
    if as_json:
        _print_json(card)
    else:
        print_scorecard(card)


def _print_json(card) -> None:
    import json
    data = {
        "project": card.project_path,
        "score_pct": round(card.percentage, 1),
        "dimensions": [
            {
                "name": d.name,
                "score": d.score,
                "max": d.max_score,
                "details": d.details,
            }
            for d in card.dimensions
        ],
    }
    click.echo(json.dumps(data, indent=2))
