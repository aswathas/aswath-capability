#!/usr/bin/env python3
"""Install aswath-capability from this checkout into the live skills directory.

The checkout is the source of truth. This copies it into place, preserves your
personal state (the ledger and anything staged for approval), and rebuilds the
registry so the next session routes against what is actually on disk.

Usage:
    python install.py            # install
    python install.py --check    # show what would change, change nothing
    python install.py --uninstall

Where it installs to:
    ~/.agents/skills/aswath-capability   (and ~/.claude/skills via the symlink)
"""

import argparse
import filecmp
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_NAME = "aswath-capability"
# Files that belong to the person, not the project. Never overwritten.
PERSONAL = {"registry/ledger.json", "registry/staged.json"}
# Generated at install time.
GENERATED = {"registry/skills.json"}


def repo_root():
    return Path(__file__).resolve().parent


def live_dir(home=None):
    home = Path(home) if home else Path.home()
    for base in (home / ".agents" / "skills", home / ".claude" / "skills"):
        if base.parent.is_dir():
            return base / SKILL_NAME
    return home / ".agents" / "skills" / SKILL_NAME


def source_dir():
    return repo_root() / "skill" / SKILL_NAME


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def copy_tree(src, dst, dry=False):
    """Copy src into dst, skipping personal and generated files. Returns a diff report."""
    report = {"updated": [], "added": [], "unchanged": 0, "removed": [], "skipped": []}
    src_files = {str(p.relative_to(src)).replace("\\", "/") for p in src.rglob("*") if p.is_file()}
    dst_files = {str(p.relative_to(dst)).replace("\\", "/") for p in dst.rglob("*") if p.is_file()} \
        if dst.is_dir() else set()

    for rel in sorted(src_files):
        if rel in PERSONAL or rel in GENERATED:
            report["skipped"].append(rel)
            continue
        if "__pycache__" in rel or rel.endswith(".pyc"):
            continue
        s = src / rel
        d = dst / rel
        if d.is_file() and digest(s) == digest(d):
            report["unchanged"] += 1
            continue
        (report["updated"] if d.is_file() else report["added"]).append(rel)
        if not dry:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, d)

    for rel in sorted(dst_files - src_files):
        if rel in PERSONAL or rel in GENERATED:
            continue
        if "__pycache__" in rel:
            continue
        report["removed"].append(rel)
        if not dry:
            try:
                (dst / rel).unlink()
            except OSError:
                pass
    return report


def rebuild_registry(dst):
    script = dst / "scripts" / "build-registry.py"
    if not script.is_file():
        return None
    try:
        r = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, timeout=300)
        return (r.stdout or "").strip()
    except Exception as e:  # noqa: BLE001
        return f"registry rebuild failed: {e}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--home", default=None)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--uninstall", action="store_true")
    ap.add_argument("--no-rebuild", action="store_true")
    args = ap.parse_args()

    src = source_dir()
    dst = live_dir(args.home)
    if not src.is_dir():
        raise SystemExit(f"source skill not found: {src}")

    if args.uninstall:
        if dst.is_dir():
            shutil.rmtree(dst)
            print(f"removed {dst}")
        else:
            print(f"nothing installed at {dst}")
        return 0

    dry = args.check
    if not dry:
        dst.parent.mkdir(parents=True, exist_ok=True)

    report = copy_tree(src, dst, dry=dry)

    if dry:
        print(f"would install -> {dst}")
        for k in ("added", "updated", "removed"):
            for f in report[k]:
                print(f"  {k:<8} {f}")
        print(f"  unchanged: {report['unchanged']}")
        print(f"  preserved (yours): {', '.join(sorted(PERSONAL))}")
        return 0

    print(f"installed -> {dst}")
    print(f"  added {len(report['added'])}, updated {len(report['updated'])}, "
          f"unchanged {report['unchanged']}, removed {len(report['removed'])}")
    if report["skipped"]:
        print(f"  preserved (yours): {', '.join(sorted(report['skipped']))}")

    if not args.no_rebuild:
        out = rebuild_registry(dst)
        if out:
            print("\n".join("  " + l for l in out.splitlines()))
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
