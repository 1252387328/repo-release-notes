#!/usr/bin/env python3
"""Generate a Markdown release-note draft from local Git commit subjects, grouped by conventional commit type."""

import argparse
import re
import subprocess
from pathlib import Path


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.strip() or "Git command failed")
    return result.stdout


def resolve(repo, ref):
    if ref.startswith("-"):
        raise ValueError("Git references cannot begin with '-'")
    return git(repo, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}").strip()


def notes(repo, since, until):
    end = resolve(repo, until)
    revision = resolve(repo, since) + ".." + end if since else end
    log = git(repo, "log", "--format=%h%x09%s", revision, "--")
    groups = {"Features": [], "Fixes": [], "Documentation": [], "Maintenance": []}
    for line in log.splitlines():
        sha, subject = line.split("\t", 1)
        match = re.match(r"(\w+)(?:\([^)]*\))?!?:\s*(.*)", subject)
        kind, message = match.groups() if match else ("other", subject)
        group = {"feat": "Features", "fix": "Fixes", "docs": "Documentation"}.get(kind, "Maintenance")
        groups[group].append(f"- {message} ({sha})")
    sections = ["# Release notes", "Draft generated from commit subjects. Review before publishing."]
    for group, entries in groups.items():
        if entries:
            sections.extend([f"## {group}", "\n".join(entries)])
    if not any(groups.values()):
        sections.append("No commits in the selected range.")
    return "\n\n".join(sections) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=Path("."))
    p.add_argument("--since", help="Exclusive starting Git reference")
    p.add_argument("--until", default="HEAD", help="Inclusive ending Git reference")
    a = p.parse_args()
    try:
        print(notes(a.repo, a.since, a.until), end="")
    except (OSError, ValueError) as exc:
        p.exit(2, f"Git error: {exc}\n")


if __name__ == "__main__":
    main()
