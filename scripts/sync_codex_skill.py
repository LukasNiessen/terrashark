#!/usr/bin/env python3
"""Build or verify the Codex-packaged skill from the canonical root skill."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_SKILL = REPO_ROOT / "SKILL.md"
SOURCE_REFERENCES = REPO_ROOT / "references"
TARGET_SKILL_ROOT = REPO_ROOT / "skills" / "terrashark"
TARGET_SKILL = TARGET_SKILL_ROOT / "SKILL.md"
TARGET_REFERENCES = TARGET_SKILL_ROOT / "references"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synchronize the Codex skill package with the canonical root files."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify synchronization without changing files.",
    )
    return parser.parse_args()


def compare_trees(source: Path, target: Path) -> list[str]:
    differences: list[str] = []
    comparison = filecmp.dircmp(source, target)

    differences.extend(str(source / name) for name in comparison.left_only)
    differences.extend(str(target / name) for name in comparison.right_only)
    differences.extend(str(source / name) for name in comparison.diff_files)
    differences.extend(str(source / name) for name in comparison.funny_files)

    for name, child in comparison.subdirs.items():
        differences.extend(compare_trees(source / name, target / name))

    return differences


def check() -> int:
    differences: list[str] = []

    if not TARGET_SKILL.is_file():
        differences.append(str(TARGET_SKILL))
    elif not filecmp.cmp(SOURCE_SKILL, TARGET_SKILL, shallow=False):
        differences.append(str(TARGET_SKILL))

    if not TARGET_REFERENCES.is_dir():
        differences.append(str(TARGET_REFERENCES))
    else:
        differences.extend(compare_trees(SOURCE_REFERENCES, TARGET_REFERENCES))

    if differences:
        print("Codex skill package is out of sync:", file=sys.stderr)
        for path in sorted(set(differences)):
            print(f"- {path}", file=sys.stderr)
        print(
            "Run `python3 scripts/sync_codex_skill.py` and commit the result.",
            file=sys.stderr,
        )
        return 1

    print("Codex skill package is in sync")
    return 0


def sync() -> int:
    TARGET_SKILL_ROOT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_SKILL, TARGET_SKILL)

    if TARGET_REFERENCES.exists():
        shutil.rmtree(TARGET_REFERENCES)
    shutil.copytree(SOURCE_REFERENCES, TARGET_REFERENCES)

    print(f"Synchronized Codex skill package at {TARGET_SKILL_ROOT}")
    return 0


def main() -> int:
    args = parse_args()
    return check() if args.check else sync()


if __name__ == "__main__":
    raise SystemExit(main())
