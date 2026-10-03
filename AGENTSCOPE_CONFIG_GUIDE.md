# AgentScope-compatible bridge configuration / Configuração compatível com AgentScope

## English

The bridge exposes an OpenAI-compatible API. Configure an external client only
after the local bridge is running and reachable over a trusted network.

- Base URL: `http://<bridge-host>:5000/v1`
- Model: use an ID returned by `GET /v1/models` (for example, the Ollama model name).
- If `BRIDGE_API_KEY` is set, send `Authorization: Bearer <key>` through the
  client's secret store.
- `POST /v1/chat/completions` accepts the OpenAI chat `model`, `messages`,
  `temperature` and `max_tokens` fields.

Local smoke test:

```bash
curl http://127.0.0.1:5000/v1/models
curl http://127.0.0.1:5000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <bridge-key-if-configured>' \
  -d '{"model":"<model-id>","messages":[{"role":"user","content":"Reply with OK"}]}'
```

Provider credentials for AgentScope are configured in AgentScope itself and
are not part of this repository. The bridge uses the Ollama URL you configure;
it does not provide, validate or store cloud-provider API keys.

## Português (BR)

A bridge expõe uma API compatível com OpenAI. Configura o cliente externo só
depois de a bridge local estar ativa e acessível numa rede confiável.

- Base URL: `http://<host-da-bridge>:5000/v1`
- Modelo: usa um ID devolvido por `GET /v1/models` (por exemplo, o nome do
  modelo Ollama).
- Se `BRIDGE_API_KEY` estiver definida, envia
  `Authorization: Bearer <key>` pelo gestor de segredos do cliente.
- `POST /v1/chat/completions` aceita os campos OpenAI `model`, `messages`,
  `temperature` e `max_tokens`.

Teste local:

```bash
curl http://127.0.0.1:5000/v1/models
curl http://127.0.0.1:5000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <bridge-key-if-configured>' \
  -d '{"model":"<model-id>","messages":[{"role":"user","content":"Responde OK"}]}'
```

Credenciais de providers cloud são configuradas no próprio AgentScope e não
fazem parte deste repositório. A bridge usa a URL Ollama que configurares; não
fornece, valida nem guarda API keys de providers.
