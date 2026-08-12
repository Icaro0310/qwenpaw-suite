# Configuração de APIs para AgentScope Platform

## APIs Disponíveis (do arquivo .env)

### Groq (LLM de alta velocidade)
- **API Key:** `<GROQ_API_KEY>`
- **Modelos:** Llama 3.1, Mixtral, etc.
- **Base URL:** `https://api.groq.com/openai/v1`
- **Provider Name:** `Groq-Free`

### Google Gemini
- **API Key:** `<GEMINI_API_KEY>`
- **Modelos:** Gemini 1.5 Flash, Pro
- **Provider Name:** `Gemini-Free`

### HuggingFace
- **API Key:** `<HF_API_TOKEN>`
- **Modelos:** Vários modelos open-source
- **Provider Name:** `HuggingFace-Free`

### Cloudflare
- **API Key:** `<CLOUDFLARE_API_TOKEN>`
- **Uso:** Workers, Pages, DNS
- **Provider Name:** `Cloudflare-Free`

### Cerebras
- **API Key:** `<CEREBRAS_API_KEY>`
- **Modelos:** Cerebras LLMs
- **Provider Name:** `Cerebras-Free`

### OpenRouter
- **API Key:** `<OPENROUTER_API_KEY>`
- **Modelos:** Vários modelos via OpenRouter
- **Base URL:** `https://openrouter.ai/api/v1`
- **Provider Name:** `OpenRouter-Free`

## Ordem de Prioridade Sugerida (Fallback Chain)

1. **Groq-Free** (mais rápido, modelos Llama 3.1)
2. **Gemini-Free** (Google, boa qualidade)
3. **OpenRouter-Free** (diversos modelos)
4. **Cerebras-Free** (alta performance)
5. **HuggingFace-Free** (modelos open-source)
6. **Ollama-Local-Bridge** (fallback offline local)

## Configuração na AgentScope Platform

Para cada provider, navegar para:
**Configuration → Models → Add Provider**

### Groq Configuration
```
Name: Groq-Free
Type: OpenAI-compatible
API Key: <GROQ_API_KEY>
Model: llama-3.1-8b-instant
Base URL: https://api.groq.com/openai/v1
```

### Gemini Configuration
```
Name: Gemini-Free
Type: Gemini
API Key: <GEMINI_API_KEY>
Model: gemini-1.5-flash
```

### OpenRouter Configuration
```
Name: OpenRouter-Free
Type: OpenAI-compatible
API Key: <OPENROUTER_API_KEY>
Model: openrouter/auto
Base URL: https://openrouter.ai/api/v1
```

### Cerebras Configuration
```
Name: Cerebras-Free
Type: OpenAI-compatible
API Key: <CEREBRAS_API_KEY>
Model: llama3.1-70b
Base URL: https://api.cerebras.ai/v1
```

## Notas de Segurança

⚠️ **IMPORTANTE:** Estas chaves foram expostas neste arquivo. Para produção:
1. Revogar chaves expostas
2. Gerar novas chaves
3. Nunca commitar secrets no Git
4. Usar variáveis de ambiente ou secrets manager

## Teste de Conexão

Após configurar na Platform, testar cada provider:
```bash
# Teste via curl (substituir pela API key real)
curl -X POST https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer <GROQ_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": "Hello"}]}'
```
