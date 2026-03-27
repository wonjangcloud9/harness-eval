"""CLI entry point for harness-eval."""

import sys

import click

from harness_eval.recommender import get_recommendations
from harness_eval.reporters.console import (
    print_recommendations,
    print_scorecard,
)
from harness_eval.scanner import scan


def _resolve_path(path_or_url: str):
    """Resolve a local path or clone a remote repo. Returns (path, cleanup)."""
    from harness_eval.remote import is_remote

    if is_remote(path_or_url):
        from harness_eval.remote import clone_remote

        return clone_remote(path_or_url)
    return None


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    """Evaluate harness engineering quality."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(score)


@main.command()
@click.argument("path", default=".")
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Output as JSON",
)
@click.option(
    "--markdown",
    "as_md",
    is_flag=True,
    help="Output as Markdown",
)
@click.option(
    "--recommend/--no-recommend",
    default=True,
    help="Show improvement recommendations",
)
@click.option(
    "--fail-under",
    type=float,
    default=None,
    help="Exit with code 1 if score is below this percentage",
)
def score(
    path: str,
    as_json: bool,
    as_md: bool,
    recommend: bool,
    fail_under: float | None,
) -> None:
    """Score a project's harness engineering."""
    remote_ctx = _resolve_path(path)
    if remote_ctx is not None:
        with remote_ctx as local_path:
            _run_score(str(local_path), as_json, as_md, recommend, fail_under)
    else:
        _run_score(path, as_json, as_md, recommend, fail_under)


def _run_score(
    path: str,
    as_json: bool,
    as_md: bool,
    recommend: bool,
    fail_under: float | None,
) -> None:
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

    if fail_under is not None and card.percentage < fail_under:
        click.echo(
            f"\nScore {card.percentage:.1f}% is below threshold {fail_under}%",
            err=True,
        )
        sys.exit(1)


@main.command()
@click.argument("paths", nargs=2)
def compare(paths: tuple[str, str]) -> None:
    """Compare harness quality of two projects."""
    from rich.console import Console
    from rich.table import Table

    c = Console()
    cards = []
    for p in paths:
        remote_ctx = _resolve_path(p)
        if remote_ctx is not None:
            with remote_ctx as local_path:
                cards.append(scan(str(local_path)))
        else:
            cards.append(scan(p))
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
    "--interval",
    type=float,
    default=2.0,
    help="Seconds between file checks",
)
def watch(path: str, interval: float) -> None:
    """Watch project for changes and re-score automatically."""
    from pathlib import Path

    from harness_eval.watcher import watch_and_score

    click.echo(f"Watching {path} for harness file changes (Ctrl+C to stop)...")
    try:
        watch_and_score(Path(path), interval=interval)
    except KeyboardInterrupt:
        click.echo("\nStopped watching.")


@main.command()
@click.argument("paths", nargs=-1, required=True)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Output as JSON",
)
def leaderboard(paths: tuple[str, ...], as_json: bool) -> None:
    """Rank multiple projects by harness quality."""
    from rich.console import Console
    from rich.table import Table

    entries = []
    for p in paths:
        remote_ctx = _resolve_path(p)
        if remote_ctx is not None:
            with remote_ctx as local_path:
                card = scan(str(local_path))
        else:
            card = scan(p)
        entries.append({"path": p, "card": card})

    entries.sort(key=lambda e: e["card"].percentage, reverse=True)

    if as_json:
        import json

        data = [
            {
                "rank": i + 1,
                "project": e["path"],
                "grade": e["card"].grade,
                "score_pct": round(e["card"].percentage, 1),
            }
            for i, e in enumerate(entries)
        ]
        click.echo(json.dumps(data, indent=2))
        return

    c = Console()
    table = Table(title="Harness Leaderboard")
    table.add_column("#", style="bold", justify="right")
    table.add_column("Project", style="cyan")
    table.add_column("Grade", justify="center")
    table.add_column("Score", justify="right")

    for i, entry in enumerate(entries):
        card = entry["card"]
        grade_color = {
            "A": "green",
            "B": "blue",
            "C": "yellow",
            "D": "red",
            "F": "bright_red",
        }.get(card.grade, "white")
        table.add_row(
            str(i + 1),
            entry["path"],
            f"[{grade_color}]{card.grade}[/{grade_color}]",
            f"{card.percentage:.0f}%",
        )

    c.print(table)


@main.command()
@click.argument(
    "path",
    default=".",
    type=click.Path(exists=True),
)
@click.option(
    "-o",
    "--output",
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


@main.command()
@click.argument("path", default=".")
@click.option(
    "-o",
    "--output-dir",
    default="benchmarks",
    help="Directory to write benchmark YAML files",
)
@click.option(
    "--max-tasks",
    type=int,
    default=None,
    help="Maximum number of tasks to generate",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Output as JSON instead of YAML files",
)
def generate(path: str, output_dir: str, max_tasks: int | None, as_json: bool) -> None:
    """Generate benchmark tasks from a repo's git history."""
    from pathlib import Path

    remote_ctx = _resolve_path(path)
    if remote_ctx is not None:
        with remote_ctx as local_path:
            _run_generate(local_path, output_dir, max_tasks, as_json)
    else:
        _run_generate(Path(path), output_dir, max_tasks, as_json)


def _run_generate(
    project, output_dir: str, max_tasks: int | None, as_json: bool
) -> None:
    import json
    from pathlib import Path

    import yaml

    from harness_eval.config import load_config
    from harness_eval.generator import generate_tasks

    config = load_config(project)
    if max_tasks is not None:
        config.generate.max_tasks = max_tasks

    tasks = generate_tasks(project, config)

    if not tasks:
        click.echo("No benchmark tasks found. Need fix commits with test changes.")
        return

    if as_json:
        click.echo(json.dumps([t.to_dict() for t in tasks], indent=2))
        return

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for task in tasks:
        task_file = out / f"{task.id}.yaml"
        task_file.write_text(
            yaml.dump(task.to_dict(), default_flow_style=False, allow_unicode=True)
        )

    click.echo(f"Generated {len(tasks)} benchmark task(s) in {out}/")
    for task in tasks:
        diff = "easy" if task.difficulty == "easy" else task.difficulty
        click.echo(f"  [{diff}] {task.id}: {task.description}")


@main.command(name="init")
@click.argument(
    "path",
    default=".",
    type=click.Path(exists=True),
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing files",
)
def init_cmd(path: str, force: bool) -> None:
    """Bootstrap harness engineering files."""
    from pathlib import Path

    from harness_eval.init import init_harness

    created = init_harness(Path(path), force=force)
    if created:
        for f in created:
            click.echo(f"  Created {f}")
        click.echo(f"\n{len(created)} file(s) created.")
    else:
        click.echo("All harness files already exist.")


@main.command(name="run")
@click.argument(
    "repo_path",
    default=".",
    type=click.Path(exists=True),
)
@click.option(
    "-t",
    "--tasks-dir",
    default="benchmarks",
    type=click.Path(exists=True),
    help="Directory containing benchmark YAML tasks",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Output results as JSON",
)
def run_cmd(repo_path: str, tasks_dir: str, as_json: bool) -> None:
    """Run benchmark tasks against a repository."""
    from pathlib import Path

    from harness_eval.runner import run_benchmark

    results = run_benchmark(Path(repo_path), Path(tasks_dir))

    if not results:
        click.echo("No benchmark tasks found.")
        return

    if as_json:
        import json

        data = [
            {"task_id": r.task_id, "passed": r.passed, "error": r.error}
            for r in results
        ]
        click.echo(json.dumps(data, indent=2))
        return

    passed = sum(1 for r in results if r.passed)
    total = len(results)

    for r in results:
        status = "PASS" if r.passed else "FAIL"
        click.echo(f"  [{status}] {r.task_id}")
        if r.error:
            click.echo(f"         {r.error}")

    click.echo(f"\n{passed}/{total} tasks passed ({passed/total*100:.0f}%)")


@main.command()
@click.argument(
    "path",
    default=".",
    type=click.Path(exists=True),
)
def fix(path: str) -> None:
    """Auto-fix common harness issues by creating missing files."""
    from pathlib import Path

    from harness_eval.fixer import fix_harness

    actions = fix_harness(Path(path))
    if actions:
        for action in actions:
            click.echo(f"  {action}")
        click.echo(f"\n{len(actions)} fix(es) applied.")

        card = scan(path)
        click.echo(f"  New score: {card.grade} ({card.percentage:.0f}%)")
    else:
        click.echo("Nothing to fix — all harness files present.")


@main.command()
@click.argument("dimension", required=False)
def explain(dimension: str | None) -> None:
    """Explain what each dimension measures and why it matters."""
    from rich.console import Console
    from rich.markdown import Markdown

    explanations = {
        "context": (
            "## Context Engineering\n"
            "Files like CLAUDE.md, AGENTS.md, .cursorrules tell AI agents "
            "how your project works. Content depth (keywords, structure, "
            "length) determines how well the agent understands your codebase."
        ),
        "scaffolding": (
            "## Scaffolding\n"
            "Tool schemas, architecture docs, and templates give agents "
            "structured access to your project. Without scaffolding, agents "
            "guess instead of following defined patterns."
        ),
        "feedback": (
            "## Feedback Loops\n"
            "CI/CD, linters, and pre-commit hooks catch agent mistakes "
            "early. Agents perform best when they get fast, automated "
            "feedback on their changes."
        ),
        "safety": (
            "## Safety & Guardrails\n"
            "Sandboxes, CODEOWNERS, and secrets protection prevent agents "
            "from causing damage. Essential for running agents with any "
            "level of autonomy."
        ),
        "reproducibility": (
            "## Reproducibility\n"
            "Containers, lockfiles, and pinned dependencies ensure agents "
            "work in the same environment every time. Eliminates "
            "'works on my machine' failures."
        ),
        "docs": (
            "## Documentation\n"
            "README, CONTRIBUTING, API docs, and CHANGELOG help agents "
            "understand project conventions. Well-documented projects "
            "produce higher quality agent output."
        ),
        "entropy": (
            "## Entropy Management\n"
            "Keeps context files focused (<200 lines), removes stale TODOs, "
            "prevents external URL drift, and enforces architecture rules. "
            "Low entropy = high signal for agents."
        ),
    }

    c = Console()
    if dimension:
        key = dimension.lower().split()[0]
        if key in explanations:
            c.print(Markdown(explanations[key]))
        else:
            click.echo(f"Unknown dimension: {dimension}")
            click.echo(f"Available: {', '.join(explanations)}")
    else:
        for text in explanations.values():
            c.print(Markdown(text))
            c.print()


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
