"""SVG badge generator for harness-eval scores."""

from harness_eval.models import Scorecard

_COLORS = {
    "A": "#4c1",
    "B": "#97ca00",
    "C": "#dfb317",
    "D": "#fe7d37",
    "F": "#e05d44",
}

_TEMPLATE = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="160" height="20">'
    '<linearGradient id="b" x2="0" y2="100%">'
    '<stop offset="0" stop-color="#bbb" stop-opacity=".1"/>'
    '<stop offset="1" stop-opacity=".1"/>'
    "</linearGradient>"
    '<mask id="a"><rect width="160" height="20" rx="3" fill="#fff"/></mask>'
    '<g mask="url(#a)">'
    '<rect width="100" height="20" fill="#555"/>'
    '<rect x="100" width="60" height="20" fill="{color}"/>'
    '<rect width="160" height="20" fill="url(#b)"/>'
    "</g>"
    '<g fill="#fff" text-anchor="middle" font-family="sans-serif" font-size="11">'
    '<text x="50" y="15" fill="#010101" fill-opacity=".3">harness-eval</text>'
    '<text x="50" y="14">harness-eval</text>'
    '<text x="130" y="15" fill="#010101" fill-opacity=".3">{grade} {pct}%</text>'
    '<text x="130" y="14">{grade} {pct}%</text>'
    "</g></svg>"
)


def render_badge(card: Scorecard) -> str:
    """Generate SVG badge string."""
    return _TEMPLATE.format(
        color=_COLORS.get(card.grade, "#9f9f9f"),
        grade=card.grade,
        pct=f"{card.percentage:.0f}",
    )
