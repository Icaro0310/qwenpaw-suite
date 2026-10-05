<div align="center">

<img src="assets/banner.svg" alt="qwenpaw-suite" width="100%"/>

</div>

# QwenPaw Suite

> Independent community project; not affiliated with or endorsed by Cognition AI.
> It is an optional local LLM/operations stack, not a Devin installation or a
> requirement for the `devin-*` tools. **If you only run Devin and have no
> local-model stack (no Ollama, no second machine), skip this repository
> entirely — every `devin-*` tool works without it.** It is an add-on for
> operators who already run, or want to run, their own model server.
>
**[Linux](README.linux.md)** · **[Personal Windows](README.windows.md)** · **[Corporate Windows](README.corporate-windows.md)**

Part of the [awesome-devin](https://github.com/Icaro0310/awesome-devin) ecosystem: the curated hub for the devin-* tools.

QwenPaw Suite connects Ollama to OpenAI-compatible clients and provides small
health-check, satellite-ping and Git synchronization utilities. It can run
locally on Windows or Linux. Cloud providers, tunnels and remote servers are
optional integrations configured by each operator; no maintainer account,
server, path or credential is required.

## Components and why they are useful

| Component | What it does | When to use it |
|---|---|---|
| `bridge/bridge.py` | Converts `/v1/chat/completions` requests to Ollama `/api/generate`; also exposes `/api/generate`, `/api/tags`, `/v1/models` and `/health`. | Let a local client that speaks the OpenAI API use a local Ollama model. |
| `orchestrator/healthcheck.py` | Checks Ollama, the bridge, and optional service URLs; writes a JSON report and can send a webhook alert. | Monitor endpoints you configure. |
| `orchestrator/satellite-ping.py` | Pings operator-supplied URLs once or on a timer and optionally posts failures to a webhook. | Keep an external endpoint active or monitor it from a small host. |
| `orchestrator/sync-github.py` | Inspects a selected Git checkout; dry-run by default. With `--apply`/`--auto`, pulls, stages all changes, commits and pushes `origin/main`. | Only when you intentionally want that repository automation. Review the target first. |
| `bridge/start-all.bat` | Windows helper that creates a local virtual environment and runs the local bridge. It does not start a public tunnel. | Quick local bridge start on Windows. |

## Requirements

- Python 3.10 or newer for the Python components.
- Ollama running at `http://localhost:11434` by default, with a model already
  pulled, if you want to generate responses through the bridge.
- Docker Compose is optional for the bridge container.
- `git` is required by `sync-github.py`; `ngrok` or another tunnel is optional
  and is never started automatically.

## Run the bridge locally

The bridge binds to `127.0.0.1:5000` by default. On loopback, an API key is
optional. It does not enable permissive browser CORS unless you configure
`BRIDGE_CORS_ORIGINS`.

**Windows (PowerShell), from the repository root:**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r bridge\requirements.txt -r orchestrator\requirements.txt
$env:OLLAMA_URL = 'http://localhost:11434'
python bridge\bridge.py
```

**Linux, from the repository root:**

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r bridge/requirements.txt -r orchestrator/requirements.txt
export OLLAMA_URL='http://127.0.0.1:11434'
python bridge/bridge.py
```

Check the local service with `curl http://localhost:5000/health`. Test a model:

```bash
curl http://localhost:5000/v1/models
```

To require a bearer key even on loopback, set `BRIDGE_API_KEY` before launch.
Binding to a non-loopback address requires `BRIDGE_API_KEY`; use a private
network/firewall and never expose an unauthenticated Ollama bridge to the
internet. `BRIDGE_CORS_ORIGINS` is a comma-separated allowlist for browser
clients; it is empty by default.

### Docker Compose

The Compose service binds its host port to loopback and requires an API key.
From `bridge/`, set `BRIDGE_API_KEY` in your shell or a local ignored `.env`
file, then run on either OS:

```bash
docker compose up --build
```

The container reaches Ollama through `host.docker.internal`. Set `OLLAMA_URL`
if your Ollama server is elsewhere. Stop the container with `docker compose
down`.

## Run the operations tools

### Health check

`healthcheck.py` checks Ollama and the local bridge, and optionally checks
`PLATFORM_URL`, `RAW_URL` and the satellite URLs. `RAW_URL` is skipped when
unset. Run one check and print the JSON report:

```bash
python orchestrator/healthcheck.py --once
```

Without `--once`, it loops using `CHECK_INTERVAL` (default 3600 seconds),
writes a status report, and can post failures to `WEBHOOK_URL`. This is a
monitor for URLs you configure, not a preconfigured cloud deployment.

### Satellite ping

```bash
PING_TARGETS='https://example.invalid/health' VM_NAME='my-node' \
  python orchestrator/satellite-ping.py --once
```

Set `PING_TARGETS` to comma-separated URLs. `WEBHOOK_URL`, `VM_NAME` and
`PING_INTERVAL` are optional. For periodic use, schedule `--once` with cron or
Task Scheduler; the repository does not install a schedule.

### Git sync — dry-run by default

```bash
python orchestrator/sync-github.py --repo /path/to/your/checkout
```

The default only reads `git status` and writes a local log; it does not change
the checkout or contact the remote. **`--apply` or `--auto` enables mutation:**
it pulls `origin/main`, stages all files with `git add -A`, commits local
changes and pushes to `origin/main`. Use it only on the repository you intend
to sync, after reviewing the working tree. The target is required as `--repo`
or `SYNC_REPO_PATH`; no maintainer path is embedded.

## Configuration reference

| Variable | Component | Purpose |
|---|---|---|
| `OLLAMA_URL` | Bridge/healthcheck | Ollama API base URL; default `http://localhost:11434`. |
| `BRIDGE_HOST` / `BRIDGE_PORT` | Bridge | Listen address and port; defaults `127.0.0.1` and `5000`. |
| `BRIDGE_API_KEY` | Bridge | Bearer key; required when binding outside loopback. |
| `BRIDGE_CORS_ORIGINS` | Bridge | Comma-separated browser-origin allowlist; unset by default. |
| `PLATFORM_URL`, `RAW_URL`, `BRIDGE_URL` | Healthcheck | Optional service health URLs. |
| `CHECK_INTERVAL` | Healthcheck | Poll interval in seconds; default `3600`. |
| `HEALTHCHECK_LOG`, `HEALTHCHECK_REPORT` | Healthcheck | Local log and JSON report paths. |
| `SATELLITE_URLS` | Healthcheck | Comma-separated `name=url` optional satellite endpoints. |
| `PING_TARGETS`, `PING_INTERVAL`, `VM_NAME`, `WEBHOOK_URL` | Satellite ping | Target URLs, interval, label and optional failure webhook. |
| `SYNC_REPO_PATH` | Git sync | Default checkout path when `--repo` is omitted. Required if no `--repo` is passed. |
| `SYNC_LOG` | Git sync | Log file path; default `sync-github.log`. |

Never put API keys, tunnel tokens or webhook URLs in tracked files. Use local
environment variables or an ignored `.env` file, and rotate anything that may
have been committed previously.

## Documentation

| File | Scope |
|---|---|
| [Architecture](ARCHITECTURE.md) | Public component/data-flow overview. |
| [Local bridge](FASE_3_LOCAL_BRIDGE.md) | Bridge setup and endpoints. |
| [API key handling](API_KEYS_CONFIG.md) | Where operator-supplied credentials belong. |
| [AgentScope integration](AGENTSCOPE_CONFIG_GUIDE.md) | Generic OpenAI-compatible endpoint setup. |
| [Multi-agent example](MULTI_AGENT_CONFIG.md) | Optional configuration pattern, not an included orchestrator. |
| [Scheduling](CRON_SCHEDULE.md) | Example schedules; none are installed automatically. |
| [Satellite ping](SATELLITE_VMS.md) | Generic host setup for the ping utility. |
| [Optional tunnel](NGROK_CONFIG.md) | Secure, manually enabled tunneling. |
| [RAW.hq integration](STATUS_RAW_HQ.md) | Optional integration status; no account credentials are included. |

## Platform support

The bridge, healthcheck, satellite ping and sync scripts work on Windows and
Linux. The batch launcher is Windows-only; Linux users run the documented
Python commands or use their own service manager. Remote-provider credentials,
network exposure and scheduling are operator choices, not bundled defaults.

## License

No license file is currently included in this repository. Public visibility
alone does not grant reuse rights; ask the maintainer before redistributing or
integrating the code until a license is selected.
