"""Guard against committing credentials again."""
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

# mongodb URI with an inline password that is not an obvious placeholder
MONGO_CRED = re.compile(r"mongodb(?:\+srv)?://[^:/\s\"'<>]+:(?!<)[^@\s\"'<>]+@")
# Pixabay keys look like "<8 digits>-<24+ hex chars>"
PIXABAY_KEY = re.compile(r"\b\d{7,9}-[0-9a-f]{20,}\b")


def tracked_text_files():
    try:
        out = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("git not available")
    for rel in out:
        path = ROOT / rel
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ttf", ".pyc"}:
            continue
        if path.is_file():
            yield rel, path.read_text(encoding="utf-8", errors="ignore")


def test_no_hardcoded_credentials_in_tracked_files():
    offenders = []
    for rel, text in tracked_text_files():
        if rel == "tests/test_no_secrets.py":
            continue
        if MONGO_CRED.search(text) or PIXABAY_KEY.search(text):
            offenders.append(rel)
    assert not offenders, f"credential-looking strings found in: {offenders}"


def test_env_files_are_ignored():
    gitignore = (ROOT / ".gitignore").read_text()
    assert re.search(r"^\.env$", gitignore, re.M)
