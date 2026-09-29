# Configuração Multi-Agente QwenPaw

## Arquitetura Multi-Agente

```
User (Telegram/Slack)
        │
        ▼
┌─────────────────┐
│  QwenPrincipal   │  Agente Principal
│  (Qwen/Groq)    │  Gera resposta técnica completa
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LlamaCritico    │  Agente Crítico
│  (Llama/Groq)   │  Revisa, aponta falhas, sugere melhorias
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  QwenSintese     │  Agente Síntese
│  (Qwen/Groq)    │  Consolida resposta final otimizada
└────────┬────────┘
         │
         ▼
    User (resposta)
```

## Agentes

### 1. QwenPrincipal (Agente Principal)
- **Modelo:** Groq-Free (llama-3.1-8b-instant)
- **Role:** Engenheiro/QA principal
- **System Prompt:**
  > Você é o agente principal de engenharia/QA. Gere respostas técnicas completas, analise código, proponha testes, e identifique bugs. Sempre justifique suas conclusões.
- **Memória:** ReMe enabled
- **Próximo agente:** LlamaCritico

### 2. LlamaCritico (Agente Crítico)
- **Modelo:** Groq-Free (llama-3.1-8b-instant)
- **Role:** Revisor técnico rigoroso
- **System Prompt:**
  > Você é um revisor crítico técnico. Analise a resposta do agente principal, aponte falhas lógicas, erros de código, imprecisões técnicas, e sugira melhorias concretas. Seja direto, rigoroso, mas construtivo.
- **Memória:** ReMe enabled
- **Próximo agente:** QwenSintese

### 3. QwenSintese (Agente Síntese)
- **Modelo:** Groq-Free (llama-3.1-8b-instant)
- **Role:** Consolidador final
- **System Prompt:**
  > Você consolida as respostas do Agente Principal e do Crítico em uma resposta final clara, corrigida e otimizada para o usuário. Elimine redundâncias e mantenha apenas informações verificadas.
- **Memória:** ReMe enabled
- **Output:** User final

## Fallback Chain (Providers)

| # | Provider     | API Key | Status |
|---|-------------|---------|--------|
| 1 | Groq        | <GROQ_API_KEY> | ✅ Funcionando |
| 2 | DeepSeek    | (a configurar) | ⏳ Pendente |
| 3 | Gemini      | `<GEMINI_API_KEY>` | ❌ Erro 404 |
| 4 | OpenRouter  | <OPENROUTER_API_KEY> | ❌ Erro 402 |
| 5 | HuggingFace | <HF_API_TOKEN> | ✅ Funcionando |
| 6 | Cerebras    | <CEREBRAS_API_KEY> | ⏳ Não testado |
| 7 | Ollama Local| (via bridge) | ✅ Disponível |

## Skills

| Skill | Tipo | Descrição | Peso |
|-------|------|-----------|------|
| DuckDuckGo Search | Python | Pesquisa web gratuita | Leve |
| Browser MCP | MCP | Navegação web | Leve |
| Hacker News | API | Feed de notícias tech | Leve |
| GitHub | MCP | Integração repos Icaro0310 | Leve |
| ArXiv | API | Papers acadêmicos | Leve |

## Canais

### Telegram Bot
- Criar via @BotFather
- Configurar token na Platform
- Restringir a chat IDs autorizados

### Slack App
- Criar workspace + app em api.slack.com
- Configurar OAuth scopes (chat:write, im:read)
- Configurar bot token na Platform

## Memória ReMe
- **Formato:** Markdown editável, pesquisável, interligado
- **Storage:** Dentro do 1GB da Platform
- **Auto-index:** Conversas indexadas automaticamente
- **Scroll Context:** 50 turns ativos, arquivo automático

## Cron Jobs (Platform)

| Job | Cron | Descrição |
|-----|------|-----------|
| Heartbeat | 0 */12 * * * | Keepalive (evitar sleep 48h) |
| Daily Digest | 0 8 * * * | Briefing matinal via Telegram |
| News Scan | 0 14 * * * | Scan Hacker News + ArXiv |
