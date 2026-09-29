# QwenPaw Sync Repository

Repositório de sincronização para infraestrutura híbrida QwenPaw - AgentScope Platform + RAW.hq + Local

## Arquitetura

Veja [ARCHITECTURE.md](ARCHITECTURE.md) para o diagrama completo e detalhes.

## Status Atual

✅ **Fase 0** - Pré-requisitos globais (Windows, WSL2, Ollama, Git, Node.js, Docker)
✅ **Fase 1** - AgentScope Platform (deploy realizado, APIs testadas)
🔒 **Fase 2** - RAW.hq (BLOQUEADO — token inválido para deploy, investigar depois)
✅ **Fase 3** - Local Bridge (Bridge Python upgraded, Healthcheck, Ollama)
✅ **Fase 3.1** - ngrok configurado (authtoken salvo, pronto)
✅ **Fase 4** - Scripts de orquestração (satellite-ping, sync-github, healthcheck v2)
✅ **Fase 5** - Documentação completa da arquitetura

## Componentes

### Bridge (`qwenpaw-bridge/`)
- Flask proxy com endpoints OpenAI-compatible (`/v1/chat/completions`)
- CORS, auth opcional, logging
- Exposta via ngrok tunnel

### Orchestrator (`qwenpaw-orchestrator/`)
- Healthcheck com suporte a satellites e JSON reports
- Satellite ping script (para VMs Serv00, Sanfeng, MonkeysCloud, Lunes)
- Git sync automático

### Multi-Agente
- Principal (Qwen) → Crítico (Llama) → Síntese (Qwen)
- Veja [MULTI_AGENT_CONFIG.md](MULTI_AGENT_CONFIG.md)

## Documentação

| Documento | Descrição |
|-----------|-----------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Arquitetura completa com diagramas |
| [MULTI_AGENT_CONFIG.md](MULTI_AGENT_CONFIG.md) | Configuração multi-agente |
| [CRON_SCHEDULE.md](CRON_SCHEDULE.md) | Todos os cron jobs |
| [SATELLITE_VMS.md](SATELLITE_VMS.md) | VMs satélite e deploy |
| [NGROK_CONFIG.md](NGROK_CONFIG.md) | Configuração ngrok |
| [FASE_3_LOCAL_BRIDGE.md](FASE_3_LOCAL_BRIDGE.md) | Bridge local |
| [STATUS_RAW_HQ.md](STATUS_RAW_HQ.md) | Status RAW.hq (bloqueado) |
| [API_KEYS_CONFIG.md](API_KEYS_CONFIG.md) | Chaves API |
| [AGENTSCOPE_CONFIG_GUIDE.md](AGENTSCOPE_CONFIG_GUIDE.md) | Guia AgentScope |

## Quick Start

```bash
# Iniciar todos os serviços locais
cd C:\Users\Utilizador\qwenpaw-bridge
.\start-all.bat
```

## Última atualização

2026-08-12 - Infraestrutura completa: bridge v2, healthcheck v2, satellites, docs
