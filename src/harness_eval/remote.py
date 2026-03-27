"""Clone remote repositories to temporary directories."""

import re
import tempfile
from contextlib import contextmanager
from pathlib import Path
from subprocess import CalledProcessError, run

_URL_PATTERNS = [
    re.compile(r"^https?://"),
    re.compile(r"^git@"),
    re.compile(r"^[\w-]+/[\w.-]+$"),  # owner/repo shorthand
]


def is_remote(path_or_url: str) -> bool:
    """Check if the input looks like a remote URL or GitHub shorthand."""
    return any(p.match(path_or_url) for p in _URL_PATTERNS)


def normalize_url(path_or_url: str) -> str:
    """Convert GitHub shorthand to full URL."""
    if re.match(r"^[\w-]+/[\w.-]+$", path_or_url):
        return f"https://github.com/{path_or_url}.git"
    return path_or_url


@contextmanager
def clone_remote(url: str, depth: int = 0):
    """Clone a remote repo to a temp dir and yield its path.

    Args:
        url: Git-cloneable URL or GitHub owner/repo shorthand.
        depth: Shallow clone depth. 0 means full clone (needed for generate).
    """
    full_url = normalize_url(url)
    with tempfile.TemporaryDirectory(prefix="harness-eval-") as tmpdir:
        cmd = ["git", "clone"]
        if depth > 0:
            cmd += ["--depth", str(depth)]
        cmd += [full_url, tmpdir]
        try:
            run(cmd, check=True, capture_output=True, text=True)
        except CalledProcessError as exc:
            raise RuntimeError(
                f"Failed to clone {full_url}: {exc.stderr.strip()}"
            ) from exc
        yield Path(tmpdir)
