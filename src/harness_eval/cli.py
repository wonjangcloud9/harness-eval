"""CLI entry point for harness-eval."""

import click

from harness_eval.recommender import get_recommendations
from harness_eval.reporters.console import (
    print_recommendations,
    print_scorecard,
)
from harness_eval.scanner import scan


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    """Evaluate harness engineering quality."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(score)


@main.command()
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
@click.option(
    "--markdown", "as_md",
    is_flag=True,
    help="Output as Markdown",
)
@click.option(
    "--recommend/--no-recommend",
    default=True,
    help="Show improvement recommendations",
)
def score(
    path: str,
    as_json: bool,
    as_md: bool,
    recommend: bool,
) -> None:
    """Score a project's harness engineering."""
    card = scan(path)
    if as_json:
        _print_json(card)
    elif as_md:
        from harness_eval.reporters.markdown import render_markdown
        click.echo(render_markdown(card))
    else:
        print_scorecard(card)
        if recommend:
            recs = get_recommendations(card)
            if recs:
                print_recommendations(recs)


@main.command()
@click.argument(
    "paths",
    nargs=2,
    type=click.Path(exists=True),
)
def compare(paths: tuple[str, str]) -> None:
    """Compare harness quality of two projects."""
    from rich.console import Console
    from rich.table import Table

    c = Console()
    cards = [scan(p) for p in paths]
    table = Table(title="Harness Comparison")
    table.add_column("Dimension", style="cyan")
    table.add_column(paths[0], justify="right")
    table.add_column(paths[1], justify="right")
    table.add_column("Delta", justify="right")

    for d0, d1 in zip(cards[0].dimensions, cards[1].dimensions):
        p0 = d0.score / d0.max_score * 100
        p1 = d1.score / d1.max_score * 100
        delta = p1 - p0
        sign = "+" if delta > 0 else ""
        color = "green" if delta > 0 else ("red" if delta < 0 else "dim")
        table.add_row(
            d0.name,
            f"{p0:.0f}%",
            f"{p1:.0f}%",
            f"[{color}]{sign}{delta:.0f}%[/{color}]",
        )

    c.print(table)
    delta_total = cards[1].percentage - cards[0].percentage
    sign = "+" if delta_total > 0 else ""
    c.print(
        f"\nOverall: {cards[0].grade} ({cards[0].percentage:.0f}%) "
        f"vs {cards[1].grade} ({cards[1].percentage:.0f}%) "
        f"[{'green' if delta_total > 0 else 'red'}]"
        f"({sign}{delta_total:.0f}%)[/]"
    )


@main.command()
@click.argument(
    "path",
    default=".",
    type=click.Path(exists=True),
)
@click.option(
    "-o", "--output",
    type=click.Path(),
    help="Write SVG badge to file",
)
def badge(path: str, output: str | None) -> None:
    """Generate an SVG score badge."""
    from harness_eval.reporters.badge import render_badge
    card = scan(path)
    svg = render_badge(card)
    if output:
        from pathlib import Path
        Path(output).write_text(svg)
        click.echo(f"Badge written to {output}")
    else:
        click.echo(svg)


def _print_json(card) -> None:
    import json
    data = {
        "project": card.project_path,
        "grade": card.grade,
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
