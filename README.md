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
└─────────────────────────────────────────────────────────────────────────────┘
```

## Estrutura

Este repositório contém:
- Configurações sincronizadas entre AgentScope Platform e RAW.hq
- Base de conhecimento ReMe
- Skills e scripts de orquestração
- Documentação da arquitetura
- Scripts de setup local

## Documentação por Fase

- [FASE_3_LOCAL_BRIDGE.md](FASE_3_LOCAL_BRIDGE.md) - Configuração local completa (Bridge, Healthcheck, Ollama)

## Status Atual

✅ **Fase 0** - Pré-requisitos globais (Windows, WSL2, Ollama, Git, Node.js, Docker)
✅ **Fase 1** - AgentScope Platform (deploy realizado, config web pendente)
⏳ **Fase 2** - RAW.hq (CLI instalado, auth manual pendente)
✅ **Fase 3** - Local Bridge (Bridge Python, Healthcheck, Ollama configurado)

## Próximos Passos (Ação Manual)

### AgentScope Platform
1. Configurar modelos LLM (APIs Free Tier)
2. Configurar canais (Telegram, Slack)
3. Configurar multi-agente personalizado
4. Configurar skills de pesquisa
5. Configurar agendamento (heartbeat)
6. Configurar Git sync

### RAW.hq
1. Executar `raw init` para criar conta
2. Deploy VM gratuita: `raw deploy --type raw-free --region eu`
3. Configurar Docker + QwenPaw na VM

### Local
1. Configurar ngrok authtoken
2. Expor bridge via ngrok
3. Configurar Ollama-Local-Bridge na Platform

## Última atualização

2026-08-12 - Fase 3 (Local Bridge) completa
