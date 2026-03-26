"""Markdown reporter for CI/PR integration."""

from harness_eval.models import Scorecard, pct_to_grade
from harness_eval.recommender import get_recommendations


def render_markdown(card: Scorecard) -> str:
    """Render scorecard as Markdown string."""
    lines = [
        f"# Harness Eval: Grade {card.grade} ({card.percentage:.0f}%)",
        "",
        "| Dimension | Score | Grade | Details |",
        "|-----------|------:|:-----:|---------|",
    ]
    for d in card.dimensions:
        pct = d.score / d.max_score * 100
        grade = pct_to_grade(pct)
        detail = "; ".join(d.details)
        lines.append(f"| {d.name} | {pct:.0f}% | {grade} | {detail} |")

    recs = get_recommendations(card)
    if recs:
        lines += ["", "## Recommendations", ""]
        for rec in recs:
            dim = rec["dimension"]
            lines.append(f"**{dim} ({rec['current_pct']:.0f}%)**")
            for s in rec["suggestions"]:
                lines.append(f"- {s}")
            lines.append("")

    return "\n".join(lines)
