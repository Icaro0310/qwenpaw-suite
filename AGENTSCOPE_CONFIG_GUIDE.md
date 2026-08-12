# Guia de Configuração - AgentScope Platform

## Teste de APIs - Resultados

### ✅ APIs FUNCIONANDO

#### 1. Groq (PRINCIPAL - MELHOR PERFORMANCE)
- **Status:** ✅ FUNCIONANDO
- **API Key:** `<GROQ_API_KEY>`
- **Modelo testado:** `llama-3.1-8b-instant`
- **Resposta:** Sucesso completo
- **Velocidade:** Muito rápida (13ms total)
- **Prioridade:** #1 (principal)

#### 2. HuggingFace
- **Status:** ✅ FUNCIONANDO
- **API Key:** `<HF_API_TOKEN>`
- **Teste:** Listagem de modelos - Sucesso
- **Prioridade:** #3 (alternativa)

### ❌ APIs COM PROBLEMAS

#### 3. Google Gemini
- **Status:** ❌ ERRO 404
- **API Key:** `<GEMINI_API_KEY>`
- **Problema:** Endpoint inválido ou chave expirada
- **Ação:** Verificar API key no Google AI Studio

#### 4. OpenRouter
- **Status:** ❌ ERRO 402 (Pagamento necessário)
- **API Key:** `<OPENROUTER_API_KEY>`
- **Problema:** Sem crédito ou modelo pago
- **Ação:** Adicionar crédito ou usar modelos gratuitos

---

## Configuração Recomendada para AgentScope Platform

### Provider 1: Groq-Free (PRINCIPAL)
**Configuration → Models → Add Provider**

```
Name: Groq-Free
Type: OpenAI-compatible
API Key: <GROQ_API_KEY>
Model: llama-3.1-8b-instant
Base URL: https://api.groq.com/openai/v1
```

**Modelos alternativos Groq:**
- `llama-3.1-70b-versatile` (maior capacidade)
- `mixtral-8x7b-32768` (mixtral)
- `gemma-7b-it` (Google Gemma via Groq)

### Provider 2: HuggingFace-Free (ALTERNATIVA)
**Configuration → Models → Add Provider**

```
Name: HuggingFace-Free
Type: OpenAI-compatible (ou HuggingFace se disponível)
API Key: <HF_API_TOKEN>
Model: meta-llama/Llama-3.1-8B-Instruct
Base URL: https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct
```

### Provider 3: Ollama-Local-Bridge (FALLBACK OFFLINE)
**Configuration → Models → Add Provider**

```
Name: Ollama-Local-Bridge
Type: Ollama
Base URL: https://<ngrok-url> (configurar após ngrok)
Model: llama3.2:1b
```

---

## Ordem de Fallback Sugerida

1. **Groq-Free** (principal - alta velocidade)
2. **HuggingFace-Free** (alternativa - modelos diversos)
3. **Ollama-Local-Bridge** (fallback offline local)

---

## Configuração de Memória e Contexto

### ReMe (Memory)
**Configuration → Memory → ReMe**

```
[x] Enable ReMe
Storage Path: /app/workspace/knowledge
[x] Auto-index conversations
Embedding Model: Deixar em branco (usar Groq)
[x] Auto-memory enabled
```

### Scroll Context
**Configuration → Context → Scroll Context**

```
Max turns in active context: 50
[x] Auto-archive older turns
[x] Archive to ReMe
```

---

## Configuração de Canais

### Telegram (Principal)
**Channels → Telegram**

1. Criar bot via @BotFather
2. Copiar token
3. Console → Channels → Telegram

```
Bot Token: <seu-token-do-botfather>
Allowed Users: <seu-chat-id>
[x] Enable
```

### Slack (Secundário)
**Channels → Slack**

1. Criar workspace em https://slack.com/create
2. Criar app em https://api.slack.com/apps
3. Configurar OAuth scopes

```
Bot Token: xoxb-<seu-token>
Workspace: <seu-workspace>
[x] Enable
```

---

## Configuração de Multi-Agente

### Agente Principal - "QwenPrincipal"
**Agent Management → New Agent**

```
Name: QwenPrincipal
Model: Groq-Free
System Prompt: "Você é o agente principal de engenharia/QA. Gere respostas técnicas completas, analise código, proponha testes, e identifique bugs. Sempre justifique suas conclusões."
Memory: ReMe enabled
Collaboration → Next Agent: LlamaCritico
```

### Agente Crítico - "LlamaCritico"
**Agent Management → New Agent**

```
Name: LlamaCritico
Model: Groq-Free (llama-3.1-8b-instant)
System Prompt: "Você é um revisor crítico técnico. Analise a resposta do agente principal, aponte falhas lógicas, erros de código, imprecisões técnicas, e sugira melhorias concretas. Seja direto, rigoroso, mas construtivo."
Memory: ReMe enabled
Collaboration → Next Agent: QwenSintese
```

### Agente Síntese - "QwenSintese"
**Agent Management → New Agent**

```
Name: QwenSintese
Model: Groq-Free
System Prompt: "Você consolida as respostas do Agente Principal e do Crítico em uma resposta final clara, corrigida e otimizada para o usuário. Elimine redundâncias e mantenha apenas informações verificadas."
Memory: ReMe enabled
Collaboration → Final Output: User
```

---

## Configuração de Skills

### Skill 1: DuckDuckGo Search
**Skills → Create Skill**

```
Name: duckduckgo-search
Type: Python
Script: (usar web_search tool já disponível)
```

### Skill 2: GitHub Integration
**Skills → Create Skill**

```
Name: github-integration
Type: MCP
Server: github-icaro
Command: npx -y @modelcontextprotocol/server-github
Env: GITHUB_PERSONAL_ACCESS_TOKEN=<seu-token-github>
```

---

## Configuração de Agendamento

### Heartbeat - Daily Brief
**Heartbeat → New**

```
Name: Daily-Engineering-Brief
Schedule: 0 8 * * * (8h da manhã)
Question: "Resuma: (1) minhas tarefas pendentes, (2) top 5 notícias de tecnologia, (3) status dos meus projetos GitHub"
Send to: Telegram
```

### Keepalive - Platform
**Cron Jobs → New**

```
Name: keepalive-platform
Schedule: 0 */12 * * * (a cada 12 horas)
Command: ask "System keepalive check -- timestamp $(date)"
```

---

## Troubleshooting

### Se Groq falhar:
1. Verificar API key no dashboard Groq
2. Verificar limite de rate limit
3. Alternar para HuggingFace

### Se HuggingFace falhar:
1. Verificar permissões da API key
2. Usar modelo diferente
3. Alternar para Ollama local

### Se Gemini/OpenRouter não funcionarem:
1. Google: Regenerar API key em https://aistudio.google.com/app/apikey
2. OpenRouter: Adicionar crédito em https://openrouter.ai/credits

---

## Teste Final

Após configurar todos os providers, testar:

1. **Console Chat:** Enviar mensagem simples
2. **Verificar logs:** Verificar qual provider foi usado
3. **Testar fallback:** Desativar Groq e testar HuggingFace
4. **Testar Telegram:** Enviar mensagem do bot
5. **Testar Slack:** Enviar mensagem do app

---

## Notas de Segurança

⚠️ **IMPORTANTE:**
- As chaves API estão documentadas neste arquivo
- Para produção, usar variáveis de ambiente
- Nunca commitar secrets no Git
- Rotacionar chaves periodicamente
- Monitorar uso e custos

## Próximos Passos

1. Configurar Groq como provider principal
2. Configurar HuggingFace como alternativa
3. Configurar Telegram/Slack bots
4. Configurar multi-agente
5. Testar fallback chain
6. Configurar agendamento
