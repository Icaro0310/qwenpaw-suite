#!/usr/bin/env python3
"""
QwenPaw Satellite Ping -- Script leve para VMs satélite.
Mantém AgentScope Platform e RAW.hq acordados via HTTP ping.

Deploy:
  - Copiar este ficheiro para a VM satélite
  - pip install requests (único dependency)
  - Configurar variáveis de ambiente
  - Adicionar ao crontab

Variáveis de ambiente:
  PING_TARGETS   - URLs separadas por vírgula (ex: https://platform.agentscope.io/api/health)
  PING_INTERVAL  - Intervalo em segundos (default: 600 = 10min)
  WEBHOOK_URL    - URL para notificação de falha (opcional)
  VM_NAME        - Nome desta VM para identificação

Cron example (replace the URL and schedule with your own service):
  */10 * * * * cd /path/to/qwenpaw-suite && python3 orchestrator/satellite-ping.py --once >> ping.log 2>&1
"""
import os
import sys
import time
import json
import logging
from urllib.parse import urlsplit, urlunsplit
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    print("ERRO: 'requests' não instalado. Execute: pip install requests")
    sys.exit(1)

# --- Config ---
VM_NAME = os.environ.get('VM_NAME', 'satellite-unknown')
PING_INTERVAL = int(os.environ.get('PING_INTERVAL', '600'))
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', '')

PING_TARGETS = os.environ.get('PING_TARGETS', '').split(',')


def safe_url(url):
    parts = urlsplit(url)
    host = parts.hostname or ''
    try:
        if parts.port:
            host = f"{host}:{parts.port}"
    except ValueError:
        pass
    return urlunsplit((parts.scheme, host, parts.path, '', ''))


logging.basicConfig(
    level=logging.INFO,
    format=f'%(asctime)s [{VM_NAME}] %(message)s'
)
log = logging.getLogger('satellite')


def ping_target(url, timeout=15):
    """Ping a configured URL; logs/reports omit credentials and query strings."""
    url = url.strip()
    if not url:
        return None
    display_url = safe_url(url)
    try:
        start = time.time()
        r = requests.get(url, timeout=timeout, headers={'User-Agent': f'QwenPaw-Satellite/{VM_NAME}'})
        elapsed = round((time.time() - start) * 1000)
        status = 'ok' if r.status_code == 200 else f'error_{r.status_code}'
        log.info(f"PING {display_url} -> {status} ({elapsed}ms)")
        return {'url': display_url, 'status': status, 'ms': elapsed, 'code': r.status_code}
    except requests.exceptions.Timeout:
        log.warning(f"PING {display_url} -> TIMEOUT")
        return {'url': display_url, 'status': 'timeout', 'ms': timeout * 1000}
    except requests.exceptions.ConnectionError:
        log.error(f"PING {display_url} -> DOWN")
        return {'url': display_url, 'status': 'down', 'ms': 0}
    except Exception as error:
        log.error(f"PING {display_url} -> ERROR: {type(error).__name__}")
        return {'url': display_url, 'status': 'error', 'ms': 0, 'error': type(error).__name__}


def notify_failure(results):
    """Send failure notification via webhook."""
    if not WEBHOOK_URL:
        return
    failed = [r for r in results if r and r['status'] not in ('ok',)]
    if not failed:
        return
    payload = {
        'text': f"⚠️ [{VM_NAME}] Ping failures detected:\n" +
                "\n".join(f"  - {r['url']}: {r['status']}" for r in failed),
        'vm': VM_NAME,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'failures': failed
    }
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except Exception:
        pass


def run_once():
    """Run a single round of pings."""
    results = []
    for target in PING_TARGETS:
        result = ping_target(target)
        if result:
            results.append(result)
    notify_failure(results)
    return results


def main():
    log.info(f"Satellite ping starting: {VM_NAME}")
    log.info(f"Targets: {PING_TARGETS}")
    log.info(f"Interval: {PING_INTERVAL}s")

    while True:
        run_once()
        time.sleep(PING_INTERVAL)


if __name__ == '__main__':
    if '--once' in sys.argv:
        results = run_once()
        print(json.dumps(results, indent=2))
    else:
        main()
