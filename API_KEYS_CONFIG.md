# API keys and secret handling / API keys e gestão de segredos

## English

This repository contains configuration **names**, not provider credentials.
Never commit real API keys, bearer tokens, webhook URLs with embedded secrets,
or tunnel authentication tokens. Use environment variables or an ignored local
`.env` file with owner-only permissions.

| Variable | Component | Secret? | Purpose |
|---|---|---:|---|
| `BRIDGE_API_KEY` | Bridge | Yes | Bearer key for protected bridge endpoints; required for non-loopback binds and Docker Compose. |
| `OLLAMA_URL` | Bridge/healthcheck | No by itself | Ollama API base URL; default is loopback. Avoid putting credentials in its URL. |
| `BRIDGE_HOST`, `BRIDGE_PORT` | Bridge | No | Listener address and port; default `127.0.0.1:5000`. |
| `BRIDGE_CORS_ORIGINS` | Bridge | No | Explicit comma-separated browser origin allowlist. |
| `WEBHOOK_URL` | Healthcheck/satellite ping | Usually yes | Notification endpoint; protect it like a credential. |
| `PLATFORM_URL`, `RAW_URL`, `BRIDGE_URL` | Healthcheck | No by itself | Optional health-check targets. |
| `SATELLITE_URLS`, `PING_TARGETS` | Healthcheck/satellite ping | No by itself | Operator-supplied URLs to check. |
| `SYNC_REPO_PATH` | Git sync | No | Local checkout path; no maintainer path is embedded. |

For Docker Compose, set `BRIDGE_API_KEY` in the environment or in an ignored
local `bridge/.env` file before `docker compose up`. For AgentScope or another
remote client, enter the same bearer key in that client's secret store; do not
paste it into a tracked JSON/YAML file.

If a key was committed or included in a public report, revoke and rotate it at
its provider. Deleting it from the latest file does not erase Git history.

## Português (BR)

Este repositório contém **nomes** de configuração, não credenciais de
providers. Nunca comites API keys reais, bearer tokens, URLs de webhook com
segredo embutido ou tokens de túnel. Usa variáveis de ambiente ou um `.env`
local ignorado pelo Git e com permissões apenas do utilizador.

| Variável | Componente | Segredo? | Propósito |
|---|---|---:|---|
| `BRIDGE_API_KEY` | Bridge | Sim | Bearer key dos endpoints protegidos; obrigatória fora de loopback e no Docker Compose. |
| `OLLAMA_URL` | Bridge/healthcheck | Não por si só | URL base da API Ollama; padrão em loopback. Evita credenciais na URL. |
| `BRIDGE_HOST`, `BRIDGE_PORT` | Bridge | Não | Endereço/porta; padrão `127.0.0.1:5000`. |
| `BRIDGE_CORS_ORIGINS` | Bridge | Não | Allowlist explícita de origens browser separadas por vírgula. |
| `WEBHOOK_URL` | Healthcheck/satellite ping | Geralmente sim | Endpoint de notificação; protege como credencial. |
| `PLATFORM_URL`, `RAW_URL`, `BRIDGE_URL` | Healthcheck | Não por si só | Destinos opcionais de healthcheck. |
| `SATELLITE_URLS`, `PING_TARGETS` | Healthcheck/satellite ping | Não por si só | URLs configuradas pelo operador. |
| `SYNC_REPO_PATH` | Git sync | Não | Caminho do checkout local; não há path do maintainer embutido. |

Para Docker Compose, define `BRIDGE_API_KEY` no ambiente ou num `bridge/.env`
ignorado antes de `docker compose up`. No AgentScope ou noutro cliente remoto,
guarda a bearer key no gestor de segredos/configuração do cliente; não a
coloques em JSON/YAML rastreados.

Se uma chave foi commitada ou incluída num relatório público, revoga e roda a
chave no provider. Apagá-la do ficheiro atual não remove o histórico Git.
