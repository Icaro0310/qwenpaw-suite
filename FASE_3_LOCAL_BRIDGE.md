# Local bridge setup / Configuração da bridge local

## English

The Flask bridge converts OpenAI-compatible chat requests to Ollama's generate
API. It is useful when an external client can target an OpenAI-style endpoint
but the model should run in your own Ollama environment.

### Windows (PowerShell)

From the repository root:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r bridge\requirements.txt
$env:OLLAMA_URL = 'http://localhost:11434'
python bridge\bridge.py
```

### Linux

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r bridge/requirements.txt
export OLLAMA_URL='http://127.0.0.1:11434'
python bridge/bridge.py
```

The default listener is `127.0.0.1:5000`; no API key is needed for loopback.
When binding to a non-loopback address, set `BRIDGE_API_KEY`. Requests to the
protected endpoints must include `Authorization: Bearer <key>`. CORS is off by
default; browser clients need an explicit `BRIDGE_CORS_ORIGINS` allowlist.

Endpoints:

| Method / path | Purpose | Auth |
|---|---|---|
| `GET /health` | Ollama reachability status | No; response omits the Ollama URL |
| `GET /api/tags` | Ollama model list | Bearer key when configured |
| `POST /api/generate` | Native Ollama prompt | Bearer key when configured |
| `GET /v1/models` | OpenAI-style model list | Bearer key when configured |
| `POST /v1/chat/completions` | OpenAI-compatible chat request | Bearer key when configured |

The Docker Compose setup is in `bridge/`; it binds the host port to loopback
and requires `BRIDGE_API_KEY`. No public tunnel is started automatically.

## Português (BR)

A bridge Flask converte pedidos de chat compatíveis com OpenAI para a API
generate do Ollama. É útil quando um cliente externo aceita endpoint OpenAI,
mas o modelo deve rodar no teu Ollama.

### Windows (PowerShell)

Na raiz do repositório:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r bridge\requirements.txt
$env:OLLAMA_URL = 'http://localhost:11434'
python bridge\bridge.py
```

### Linux

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r bridge/requirements.txt
export OLLAMA_URL='http://127.0.0.1:11434'
python bridge/bridge.py
```

O listener padrão é `127.0.0.1:5000`; em loopback não requer API key. Para bind
fora de loopback, define `BRIDGE_API_KEY`. Os endpoints protegidos exigem
`Authorization: Bearer <key>`. CORS fica desligado por omissão; clientes browser
precisam de uma allowlist explícita em `BRIDGE_CORS_ORIGINS`.

| Método / path | Propósito | Auth |
|---|---|---|
| `GET /health` | Estado de ligação ao Ollama | Não; a resposta omite a URL |
| `GET /api/tags` | Lista de modelos Ollama | Bearer key quando configurada |
| `POST /api/generate` | Prompt na API nativa Ollama | Bearer key quando configurada |
| `GET /v1/models` | Lista de modelos formato OpenAI | Bearer key quando configurada |
| `POST /v1/chat/completions` | Chat compatível com OpenAI | Bearer key quando configurada |

A configuração Docker Compose fica em `bridge/`; a porta do host fica em
loopback e exige `BRIDGE_API_KEY`. Nenhum túnel público é iniciado
automaticamente.
