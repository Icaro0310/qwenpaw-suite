<div align="center">

<img src="assets/banner.svg" alt="qwenpaw-suite" width="100%"/>

</div>

# QwenPaw Suite

> Projeto comunitário independente; sem afiliação ou endosso da Cognition AI.
> É uma stack opcional de LLM local/operações, não é uma instalação do Devin nem
> requisito dos utilitários `devin-*`. **Se só corres Devin e não tens stack de
> modelos locais (sem Ollama, sem segunda máquina), podes ignorar este
> repositório por completo — todas as ferramentas `devin-*` funcionam sem
> ele.** É um add-on para quem já corre, ou quer correr, o seu próprio
> servidor de modelos.
>
> **[English](README.md)** · Português (BR)

QwenPaw Suite liga Ollama a clientes compatíveis com a API OpenAI e fornece
utilitários leves de healthcheck, ping de satélites e sincronização Git. Pode
rodar localmente em Windows ou Linux. Providers cloud, túneis e servidores
remotos são integrações opcionais configuradas por cada operador; não é
necessária conta, servidor, path ou credencial do maintainer.

## Componentes e utilidade

| Componente | O que faz | Quando usar |
|---|---|---|
| `bridge/bridge.py` | Converte pedidos `/v1/chat/completions` para Ollama `/api/generate`; também expõe `/api/generate`, `/api/tags`, `/v1/models` e `/health`. | Usar um modelo Ollama local com um cliente que fala a API OpenAI. |
| `orchestrator/healthcheck.py` | Verifica Ollama, bridge e URLs opcionais; grava relatório JSON e pode enviar alerta via webhook. | Monitorar endpoints que configurares. |
| `orchestrator/satellite-ping.py` | Testa URLs configuradas uma vez ou em intervalo e pode enviar falhas para um webhook. | Manter um endpoint externo ativo ou monitorá-lo de um host pequeno. |
| `orchestrator/sync-github.py` | Inspeciona um checkout Git indicado; por omissão faz dry-run. Com `--apply`/`--auto`, faz pull, stage de todas as alterações, commit e push de `origin/main`. | Só quando quiseres explicitamente essa automação no repo selecionado. |
| `bridge/start-all.bat` | Helper Windows que cria um venv local e executa a bridge local. Não abre túnel público. | Início rápido da bridge local no Windows. |

## Requisitos

- Python 3.10 ou superior para os componentes Python.
- Ollama em `http://localhost:11434` por omissão e um modelo já descarregado,
  se quiseres gerar respostas pela bridge.
- Docker Compose é opcional para o container da bridge.
- `git` é necessário para `sync-github.py`; ngrok/outro túnel é opcional e
  nunca é iniciado automaticamente.

## Executar a bridge localmente

A bridge escuta em `127.0.0.1:5000` por omissão. Em loopback, a API key é
opcional. CORS permissivo para browser fica desligado, a menos que configures
`BRIDGE_CORS_ORIGINS`.

**Windows (PowerShell), a partir da raiz do repo:**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r bridge\requirements.txt -r orchestrator\requirements.txt
$env:OLLAMA_URL = 'http://localhost:11434'
python bridge\bridge.py
```

**Linux, a partir da raiz do repo:**

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r bridge/requirements.txt -r orchestrator/requirements.txt
export OLLAMA_URL='http://127.0.0.1:11434'
python bridge/bridge.py
```

Verifica o serviço com `curl http://localhost:5000/health`. Testa a lista de
modelos com:

```bash
curl http://localhost:5000/v1/models
```

Para exigir bearer key também em loopback, define `BRIDGE_API_KEY`. Um bind
fora de loopback exige `BRIDGE_API_KEY`; usa rede/firewall privados e nunca
exponhas uma bridge Ollama sem autenticação na internet. `BRIDGE_CORS_ORIGINS`
é uma allowlist de origens separadas por vírgulas; por omissão está vazia.

### Docker Compose

O serviço Compose limita a porta do host a loopback e exige API key. Em
`bridge/`, define `BRIDGE_API_KEY` no shell ou num `.env` local ignorado pelo
Git, e executa em qualquer um dos dois SO:

```bash
docker compose up --build
```

O container alcança o Ollama via `host.docker.internal`. Define `OLLAMA_URL`
se o teu servidor Ollama estiver noutro endereço. Para parar:
`docker compose down`.

## Executar as ferramentas de operações

### Healthcheck

`healthcheck.py` verifica Ollama e a bridge; também verifica
`PLATFORM_URL`, `RAW_URL` e URLs de satélites quando configuradas. `RAW_URL`
é ignorada se estiver vazia. Executa uma verificação e imprime JSON:

```bash
python orchestrator/healthcheck.py --once
```

Sem `--once`, repete segundo `CHECK_INTERVAL` (3600 segundos por omissão),
grava relatório e pode enviar falhas para `WEBHOOK_URL`. É um monitor das URLs
que configurares, não um deploy cloud pré-configurado.

### Ping de satélite

```bash
PING_TARGETS='https://example.invalid/health' VM_NAME='my-node' \
  python orchestrator/satellite-ping.py --once
```

Define `PING_TARGETS` com URLs separados por vírgula. `WEBHOOK_URL`, `VM_NAME`
e `PING_INTERVAL` são opcionais. Para repetição, agenda `--once` com cron ou
Task Scheduler; o repositório não instala um agendamento.

### Git sync — dry-run por omissão

```bash
python orchestrator/sync-github.py --repo /caminho/para/o/teu/checkout
```

A execução padrão só lê `git status` e grava um log local; não altera o
checkout nem contacta o remote. **`--apply` ou `--auto` ativa alterações:**
faz pull de `origin/main`, stage de todos os ficheiros, commit das alterações
e push para `origin/main`. Usa apenas no repo pretendido e depois de rever o
working tree. O destino é obrigatório por `--repo` ou `SYNC_REPO_PATH`; não há
path do maintainer embutido.

## Referência de configuração

| Variável | Componente | Propósito |
|---|---|---|
| `OLLAMA_URL` | Bridge/healthcheck | URL base da API Ollama; default `http://localhost:11434`. |
| `BRIDGE_HOST` / `BRIDGE_PORT` | Bridge | Endereço e porta de escuta; defaults `127.0.0.1` e `5000`. |
| `BRIDGE_API_KEY` | Bridge | Bearer key; obrigatória se o bind sair de loopback. |
| `BRIDGE_CORS_ORIGINS` | Bridge | Allowlist de origens browser separadas por vírgula; vazia por omissão. |
| `PLATFORM_URL`, `RAW_URL`, `BRIDGE_URL` | Healthcheck | URLs opcionais de healthcheck. |
| `CHECK_INTERVAL` | Healthcheck | Intervalo em segundos; default `3600`. |
| `HEALTHCHECK_LOG`, `HEALTHCHECK_REPORT` | Healthcheck | Paths do log local e relatório JSON. |
| `SATELLITE_URLS` | Healthcheck | URLs opcionais `nome=url`, separadas por vírgula. |
| `PING_TARGETS`, `PING_INTERVAL`, `VM_NAME`, `WEBHOOK_URL` | Ping de satélite | URLs destino, intervalo, rótulo e webhook opcional. |
| `SYNC_REPO_PATH` | Git sync | Checkout padrão quando `--repo` não é passado; obrigatório sem `--repo`. |
| `SYNC_LOG` | Git sync | Path do log; default `sync-github.log`. |

Nunca coloques API keys, tokens de túnel ou URLs de webhook em ficheiros
rastreados. Usa variáveis de ambiente ou `.env` ignorado pelo Git; roda
credenciais que tenham sido commitadas anteriormente.

## Documentação

| Ficheiro | Âmbito |
|---|---|
| [Arquitetura](ARCHITECTURE.md) | Visão pública dos componentes e fluxo de dados. |
| [Bridge local](FASE_3_LOCAL_BRIDGE.md) | Instalação e endpoints da bridge. |
| [Configuração de API keys](API_KEYS_CONFIG.md) | Onde configurar credenciais do operador. |
| [Integração AgentScope](AGENTSCOPE_CONFIG_GUIDE.md) | Configuração genérica de endpoint compatível com OpenAI. |
| [Exemplo multi-agente](MULTI_AGENT_CONFIG.md) | Padrão opcional, não é um orquestrador incluído. |
| [Agendamento](CRON_SCHEDULE.md) | Exemplos; nenhum job é instalado automaticamente. |
| [Ping de satélites](SATELLITE_VMS.md) | Configuração genérica de hosts para a ferramenta de ping. |
| [Túnel opcional](NGROK_CONFIG.md) | Túnel manual com configuração segura. |
| [Integração RAW.hq](STATUS_RAW_HQ.md) | Estado genérico da integração; sem credenciais de conta. |

## Suporte de plataformas

Bridge, healthcheck, satellite ping e sync funcionam em Windows e Linux. O
launcher `.bat` é apenas Windows; em Linux executa os comandos Python ou usa o
gestor de serviços escolhido. Credenciais de providers remotos, exposição de
rede e agendamento são decisões do operador, não defaults incluídos.

## Licença

Este repositório ainda não contém um ficheiro de licença. A visibilidade
pública, por si só, não concede direitos de reutilização; consulta o maintainer
antes de redistribuir ou integrar o código até ser escolhida uma licença.
