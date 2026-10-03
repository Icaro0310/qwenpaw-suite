# Architecture / Arquitetura

## English

QwenPaw Suite is a set of independent local-first utilities, not a hosted
service and not an automatic deployment of any cloud account.

```text
OpenAI-compatible client
          │ HTTP /v1/chat/completions
          ▼
bridge/bridge.py ──HTTP──► Ollama (default http://localhost:11434)

orchestrator/healthcheck.py ──► configured health URLs
orchestrator/satellite-ping.py ──► configured ping targets
orchestrator/sync-github.py ──► one explicitly selected Git checkout
```

The bridge runs on loopback by default. A remote bind requires
`BRIDGE_API_KEY`; browser CORS is disabled unless origins are explicitly
allowlisted. A tunnel, cloud provider, healthcheck URL, webhook, or Git sync
target is always configured by the operator.

The suite does **not** ship QwenPaw Platform, Ollama models, provider API keys,
remote hosts, or a multi-agent runtime. The multi-agent document is a pattern
for configuring an external platform, not an executable orchestrator here.

## Português (BR)

QwenPaw Suite é um conjunto de utilitários locais e independentes, não um
serviço hospedado nem um deploy automático de contas cloud.

```text
Cliente compatível com OpenAI
          │ HTTP /v1/chat/completions
          ▼
bridge/bridge.py ──HTTP──► Ollama (padrão http://localhost:11434)

orchestrator/healthcheck.py ──► URLs de healthcheck configuradas
orchestrator/satellite-ping.py ──► destinos de ping configurados
orchestrator/sync-github.py ──► um checkout Git escolhido explicitamente
```

A bridge escuta em loopback por padrão. Bind remoto exige `BRIDGE_API_KEY`; CORS
para browser fica desligado até configurar uma allowlist de origens. Túnel,
provider cloud, URL de healthcheck, webhook e alvo Git são sempre configurados
pelo operador.

A suite **não** inclui QwenPaw Platform, modelos Ollama, API keys de providers,
hosts remotos ou runtime multi-agente. O documento de multi-agente descreve um
padrão de configuração externa, não um orquestrador executável neste repo.
