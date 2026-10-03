# Public components / Componentes públicos

## English

This file lists only the reusable components shipped in this repository. It
contains no personal project portfolio or maintainer deployment inventory.

| Component | Source | Purpose |
|---|---|---|
| Local LLM bridge | `bridge/bridge.py` | Ollama-to-OpenAI-compatible HTTP adapter. |
| Health checker | `orchestrator/healthcheck.py` | Monitors user-configured local and remote endpoints. |
| Satellite pinger | `orchestrator/satellite-ping.py` | Sends HTTP checks to URLs supplied by the operator. |
| Git sync helper | `orchestrator/sync-github.py` | Dry-run Git status by default; opt-in sync/push with `--apply`. |

## Português (BR)

Este ficheiro lista apenas os componentes reutilizáveis deste repositório. Não
inclui portfólio pessoal nem inventário de deploy do maintainer.

| Componente | Código | Propósito |
|---|---|---|
| Bridge LLM local | `bridge/bridge.py` | Adapter HTTP Ollama para API compatível com OpenAI. |
| Healthcheck | `orchestrator/healthcheck.py` | Monitoriza endpoints locais/remotos configurados pelo operador. |
| Ping de satélite | `orchestrator/satellite-ping.py` | Faz verificações HTTP de URLs fornecidos pelo operador. |
| Git sync helper | `orchestrator/sync-github.py` | Dry-run Git por omissão; sync/push opt-in com `--apply`. |
