#!/usr/bin/env python3
"""
QwenPaw Git Sync -- Sincroniza repo qwenpaw-sync automaticamente.
Faz pull, verifica mudanças locais, commit/push se necessário.

Uso:
  python sync-github.py          # Sync interativo
  python sync-github.py --auto   # Sync automático (para cron)

Crontab:
  # Sync a cada 6 horas
  0 */6 * * * cd /path/to/qwenpaw-sync && python3 ../qwenpaw-orchestrator/sync-github.py --auto >> sync.log 2>&1
"""
import os
import sys
import subprocess
import time
import logging
from datetime import datetime

SYNC_REPO = os.environ.get('SYNC_REPO_PATH', r'C:\Users\Utilizador\qwenpaw-sync')
LOG_FILE = os.environ.get('SYNC_LOG', 'sync-github.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [SYNC] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding='utf-8')
    ]
)
log = logging.getLogger('sync')


def run_git(args, cwd=None):
    """Run a git command and return output."""
    cmd = ['git'] + args
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or SYNC_REPO,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, '', 'TIMEOUT'
    except Exception as e:
        return -1, '', str(e)


def sync():
    """Execute full sync cycle."""
    log.info("=" * 50)
    log.info(f"Starting sync: {SYNC_REPO}")
    log.info("=" * 50)

    # 1. Check repo status
    code, out, err = run_git(['status', '--porcelain'])
    if code != 0:
        log.error(f"git status failed: {err}")
        return False

    has_changes = bool(out.strip())
    if has_changes:
        log.info(f"Local changes detected:\n{out}")

    # 2. Pull latest
    log.info("Pulling latest changes...")
    code, out, err = run_git(['pull', '--rebase', 'origin', 'main'])
    if code != 0:
        log.error(f"git pull failed: {err}")
        # Try without rebase
        code, out, err = run_git(['pull', 'origin', 'main'])
        if code != 0:
            log.error(f"git pull (no rebase) also failed: {err}")
            return False
    log.info(f"Pull result: {out}")

    # 3. If local changes, commit and push
    if has_changes:
        log.info("Staging changes...")
        code, out, err = run_git(['add', '-A'])
        if code != 0:
            log.error(f"git add failed: {err}")
            return False

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_msg = f"auto-sync: {timestamp}"
        log.info(f"Committing: {commit_msg}")

        code, out, err = run_git(['commit', '-m', commit_msg])
        if code != 0:
            if 'nothing to commit' in out or 'nothing to commit' in err:
                log.info("Nothing to commit (already clean)")
            else:
                log.error(f"git commit failed: {err}")
                return False
        else:
            log.info(f"Committed: {out}")

        log.info("Pushing to origin...")
        code, out, err = run_git(['push', 'origin', 'main'])
        if code != 0:
            log.error(f"git push failed: {err}")
            return False
        log.info(f"Push result: {out}")
    else:
        log.info("No local changes to push")

    log.info("Sync complete ✓")
    return True


if __name__ == '__main__':
    auto = '--auto' in sys.argv
    success = sync()
    if not success and not auto:
        sys.exit(1)
