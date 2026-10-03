#!/usr/bin/env python3
"""
QwenPaw Healthcheck -- Monitora todos os serviços da infraestrutura.
Verifica: Ollama, Bridge, AgentScope Platform, RAW.hq, Satellites.
Gera relatório JSON e logs.
"""
import os
import sys
import time
import json
import logging
import requests
from datetime import datetime, timezone
from urllib.parse import urlsplit, urlunsplit

# --- Config ---
PLATFORM_URL = os.environ.get('PLATFORM_URL', '')
RAW_URL = os.environ.get('RAW_URL', '')
BRIDGE_URL = os.environ.get('BRIDGE_URL', 'http://127.0.0.1:5000/health')
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://127.0.0.1:11434/api/tags')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', '')
CHECK_INTERVAL = int(os.environ.get('CHECK_INTERVAL', '3600'))
LOG_FILE = os.environ.get('HEALTHCHECK_LOG', 'qwenpaw-health.log')
REPORT_FILE = os.environ.get('HEALTHCHECK_REPORT', 'qwenpaw-status.json')


def _satellite_targets(value):
    targets = {}
    for item in value.split(','):
        name, separator, url = item.partition('=')
        if separator and name.strip() and url.strip():
            targets[name.strip()] = url.strip()
    return targets


SATELLITES = _satellite_targets(os.environ.get('SATELLITE_URLS', ''))


def _safe_url(url):
    parts = urlsplit(url)
    host = parts.hostname or ''
    try:
        if parts.port:
            host = f"{host}:{parts.port}"
    except ValueError:
        pass
    return urlunsplit((parts.scheme, host, parts.path, '', ''))

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
log = logging.getLogger('healthcheck')

# Also log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
log.addHandler(console)


def ping(url, name, timeout=10):
    """Ping a service and return a report with URL credentials/query removed."""
    if not url:
        return {"name": name, "status": "skipped", "url": "", "ms": 0}
    safe_url = _safe_url(url)
    try:
        start = time.time()
        r = requests.get(url, timeout=timeout)
        elapsed = round((time.time() - start) * 1000)
        status = "ok" if r.status_code == 200 else f"error_{r.status_code}"
        log.info(f"{name}: {status} ({elapsed}ms)")
        return {"name": name, "status": status, "url": safe_url, "ms": elapsed, "code": r.status_code}
    except requests.exceptions.Timeout:
        log.warning(f"{name}: TIMEOUT")
        return {"name": name, "status": "timeout", "url": safe_url, "ms": timeout * 1000}
    except requests.exceptions.ConnectionError:
        log.error(f"{name}: CONNECTION_REFUSED")
        return {"name": name, "status": "down", "url": safe_url, "ms": 0}
    except Exception as e:
        log.error(f"{name}: FAILED - {type(e).__name__}")
        return {"name": name, "status": "error", "url": safe_url, "ms": 0, "error": type(e).__name__}


def generate_report(results):
    """Generate JSON status report."""
    now = datetime.now(timezone.utc).isoformat()
    all_ok = all(r['status'] in ('ok', 'skipped') for r in results)

    report = {
        "timestamp": now,
        "overall": "healthy" if all_ok else "degraded",
        "services": results,
        "alerts": []
    }

    # Detect critical issues
    for r in results:
        if r['status'] == 'down' and r['name'] in ('AgentScope Platform', 'Bridge'):
            report['alerts'].append(f"CRITICAL: {r['name']} is DOWN")
        elif r['status'] == 'timeout':
            report['alerts'].append(f"WARNING: {r['name']} timed out")

    return report


def send_webhook(report):
    """Send report to webhook (Telegram, Slack, etc.)."""
    if not WEBHOOK_URL:
        return
    try:
        requests.post(WEBHOOK_URL, json=report, timeout=10)
        log.info("Webhook notification sent")
    except Exception as e:
        log.error(f"Webhook failed: {type(e).__name__}")


def save_report(report):
    """Save latest report to the configured JSON file."""
    report_file = REPORT_FILE
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    log.info(f"Report saved to {report_file}")


def run_checks():
    """Run all health checks and generate report."""
    results = []

    # Core services
    results.append(ping(OLLAMA_URL, "Ollama Local"))
    results.append(ping(BRIDGE_URL, "Bridge"))
    results.append(ping(PLATFORM_URL, "AgentScope Platform"))

    # RAW.hq (bloqueado por enquanto)
    if RAW_URL:
        results.append(ping(RAW_URL, "RAW.hq"))
    else:
        results.append({"name": "RAW.hq", "status": "blocked", "url": "", "ms": 0})

    # Satellite VMs
    for name, url in SATELLITES.items():
        results.append(ping(url, f"Satellite-{name}"))

    report = generate_report(results)
    save_report(report)

    # Send alerts if degraded
    if report['overall'] != 'healthy':
        send_webhook(report)

    return report


def main():
    log.info("=" * 60)
    log.info("QwenPaw Healthcheck Starting")
    log.info(f"Check interval: {CHECK_INTERVAL}s")
    log.info(f"Log file: {LOG_FILE}")
    log.info("=" * 60)

    while True:
        log.info(f"\n--- Check at {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
        report = run_checks()

        # Print summary
        log.info(f"Overall: {report['overall']}")
        for alert in report.get('alerts', []):
            log.warning(alert)

        log.info(f"Next check in {CHECK_INTERVAL}s...")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # Single check mode
        report = run_checks()
        print(json.dumps(report, indent=2))
    else:
        main()
