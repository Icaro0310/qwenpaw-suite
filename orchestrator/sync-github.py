#!/usr/bin/env python3
"""Sync an explicitly selected Git repository with its ``origin/main`` branch.

Dry-run is the default. ``--apply`` opts into pulling, staging all changes,
committing them and pushing to ``origin main``.
"""
import argparse
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SYNC_REPO_PATH = os.environ.get("SYNC_REPO_PATH")
LOG_FILE = os.environ.get("SYNC_LOG", "sync-github.log")
log = logging.getLogger("sync")


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [SYNC] %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE, encoding="utf-8")],
    )


def run_git(args, cwd):
    """Run a Git command in the selected repository and return its output."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except OSError as error:
        return -1, "", str(error)


def sync(repo_path=None, *, apply=False):
    """Inspect a repo, or explicitly pull/commit/push it with ``apply=True``."""
    selected = repo_path or SYNC_REPO_PATH
    if not selected:
        log.error("Set --repo or SYNC_REPO_PATH; no repository is selected")
        return False
    repo = Path(selected).expanduser()
    if not repo.is_dir():
        log.error("Repository directory does not exist: %s", repo)
        return False

    log.info("Checking repository: %s", repo)
    code, out, err = run_git(["status", "--porcelain"], cwd=repo)
    if code != 0:
        log.error("git status failed: %s", err)
        return False
    has_changes = bool(out.strip())

    if not apply:
        log.info("DRY RUN: no pull, staging, commit or push was performed")
        log.info("Working tree: %s", out or "clean")
        log.info("Pass --apply to perform the sync (stages all changes)")
        return True

    log.info("Pulling origin/main with rebase...")
    code, out, err = run_git(["pull", "--rebase", "origin", "main"], cwd=repo)
    if code != 0:
        log.error("git pull --rebase failed; resolve conflicts manually: %s", err)
        return False
    log.info("Pull result: %s", out)

    if has_changes:
        log.info("Staging all changes in the selected repository...")
        code, out, err = run_git(["add", "-A"], cwd=repo)
        if code != 0:
            log.error("git add failed: %s", err)
            return False

        commit_msg = f"auto-sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        code, out, err = run_git(["commit", "-m", commit_msg], cwd=repo)
        if code != 0 and "nothing to commit" not in (out + err):
            log.error("git commit failed: %s", err)
            return False
        if code == 0:
            log.info("Committed: %s", out)

        log.info("Pushing origin/main...")
        code, out, err = run_git(["push", "origin", "main"], cwd=repo)
        if code != 0:
            log.error("git push failed: %s", err)
            return False
        log.info("Push result: %s", out)
    else:
        log.info("No local changes to stage or push")

    log.info("Sync complete")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default=SYNC_REPO_PATH,
                        help="repository directory (or set SYNC_REPO_PATH)")
    parser.add_argument("--apply", action="store_true",
                        help="pull, stage all changes, commit and push; default is dry-run")
    parser.add_argument("--auto", action="store_true",
                        help="for cron: same mutating behavior as --apply")
    args = parser.parse_args(argv)
    configure_logging()
    success = sync(args.repo, apply=args.apply or args.auto)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
