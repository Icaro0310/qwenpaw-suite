# QwenPaw Sync Repository

Repositório de sincronização para infraestrutura híbrida QwenPaw - AgentScope Platform + RAW.hq + Local

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AGENTSCOPE PLATFORM (Nuvem)                        │
│                    2 vCPU | 4 GB RAM | 1 GB Storage                        │
│                         CEREBRO PRINCIPAL #1                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │  Sync via Git
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              RAW.HQ (VPS Real)                               │
│                    2 vCPU | 4 GB RAM | 40 GB SSD NVMe                        │
│                         CEREBRO PRINCIPAL #2                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │  Fallback / Bridge
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              MAQUINA LOCAL (Windows + WSL + Docker Leve)                      │
│                                                                              │
│  * Ollama local (fallback 100% offline)                                      │
│  * Bridge Python (conecta Platform/RAW.hq ao Ollama local)                  │
│  * Healthcheck/orquestrador local                                             │
│  * RAM preservada (~150MB total para serviços leves)                        │
│  * ngrok tunnel (expõe bridge para internet)                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Estrutura

Este repositório contém:
- Configurações sincronizadas entre AgentScope Platform e RAW.hq
- Base de conhecimento ReMe
- Skills e scripts de orquestração
- Documentação da arquitetura
- Scripts de setup local

## Status Atual

✅ **Fase 0** - Pré-requisitos globais (Windows, WSL2, Ollama, Git, Node.js, Docker)
✅ **Fase 1** - AgentScope Platform (deploy realizado, APIs testadas)
⏳ **Fase 2** - RAW.hq (Conta criada, token novo configurado, deploy a falhar - investigar)
✅ **Fase 3** - Local Bridge (Bridge Python, Healthcheck, Ollama configurado)
✅ **Fase 3.1** - ngrok configurado (authtoken salvo, pronto para expor bridge)

## Status das APIs

### ✅ FUNCIONANDO
- **Groq:** API key válida, testada e funcionando (principal)
- **HuggingFace:** API key válida, acesso a modelos confirmado

### ❌ PROBLEMAS
- **Google Gemini:** API key inválida ou endpoint incorreto (404)
- **OpenRouter:** Requer pagamento/crédito (402)
- **RAW.hq:** Token de deploy inválido (conta funciona mas deploy falha)

## Credenciais e Configuração

### ngrok (✅ Configurado)
- **Authtoken:** Salvo em `ngrok.yml` e variável de ambiente `NGROK_AUTHTOKEN`
- **Config:** `C:\Users\Utilizador\AppData\Local\ngrok\ngrok.yml`

### RAW.hq (⏳ Deploy pendente)
- **API Token:** `<RAW_API_TOKEN>`
- **Email:** `icarogalvao5@gmail.com`
- **CLI:** `rawhq@0.6.0`
- **Variável de ambiente:** `RAW_API_TOKEN` configurada

### Variáveis de Ambiente Configuradas
- `NGROK_AUTHTOKEN` - Token ngrok (User scope)
- `RAW_API_TOKEN` - Token RAW.hq (User scope)

## Documentação por Fase

- [FASE_3_LOCAL_BRIDGE.md](FASE_3_LOCAL_BRIDGE.md) - Configuração local completa (Bridge, Healthcheck, Ollama)
- [NGROK_CONFIG.md](NGROK_CONFIG.md) - Configuração do ngrok tunnel
- [STATUS_RAW_HQ.md](STATUS_RAW_HQ.md) - Status e troubleshooting RAW.hq
- [API_KEYS_CONFIG.md](API_KEYS_CONFIG.md) - Chaves disponíveis e configuração
- [AGENTSCOPE_CONFIG_GUIDE.md](AGENTSCOPE_CONFIG_GUIDE.md) - Guia completo de configuração

## Quick Start (Setup Local)

```bash
# 1. Iniciar Ollama (se não estiver rodando)
ollama serve

# 2. Iniciar Bridge + Healthcheck + ngrok
cd C:\Users\Utilizador\qwenpaw-bridge
.\start-all.bat

# 3. Ou manualmente:
# Bridge
docker-compose up -d

# ngrok (em outro terminal)
.\ngrok.exe http 5000
```

## Próximos Passos

### Imediato
1. ~~Configurar ngrok authtoken~~ ✅
2. ~~Configurar RAW.hq token~~ ✅ (deploy ainda falha)
3. Resolver deploy RAW.hq (verificar email/dashboard)
4. Expor bridge via ngrok e testar acesso externo

### AgentScope Platform
1. Configurar modelos LLM (APIs Free Tier)
2. Configurar canais (Telegram, Slack)
3. Configurar multi-agente personalizado
4. Configurar skills de pesquisa
5. Configurar agendamento (heartbeat)
6. Configurar Git sync

### RAW.hq (Após Deploy)
1. Resolver problema do token de deploy
2. Acessar VM via SSH
3. Configurar Docker + QwenPaw na VM

### Local
1. ~~Configurar ngrok authtoken~~ ✅
2. Expor bridge via `ngrok http 5000`
3. Configurar Ollama-Local-Bridge na Platform com URL do ngrok

## Última atualização

2026-08-12 - ngrok configurado, RAW.hq token atualizado, documentação expandida
