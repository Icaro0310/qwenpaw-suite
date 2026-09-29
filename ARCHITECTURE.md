# Arquitetura QwenPaw - Infraestrutura Completa

## Diagrama

```
+-----------------------------------------------------------------------------+
|                         AGENTSCOPE PLATFORM (Nuvem)                        |
|                    2 vCPU | 4 GB RAM | 1 GB Storage                        |
|                         CEREBRO PRINCIPAL #1                                |
|                                                                              |
|  * QwenPaw rodando 24/7 (mantido acordado por cron 12h)                    |
|  * API Keys Cloud -> PRIORIDADE #1 (DeepSeek, Groq, Gemini, OpenRouter)     |
|  * Multi-agente: Principal (Qwen) + Critico (Llama) + Sintese (Qwen)      |
|  * Skills leves: DuckDuckGo, Browser MCP, Hacker News, GitHub, ArXiv       |
|  * Canais: Telegram Bot + Slack App                                        |
|  * Memoria ReMe (Markdown editavel, pesquisavel, interligado)              |
|  * Cron: heartbeat 12h + daily digest 8h + news scan 14h                     |
|  * 1 GB storage = APENAS configs, skills, knowledge base (poucos KB)   |
|                                                                              |
|  ! Sleep apos 48h inatividade -> cron job mantem acordado                 |
|  ! Limpeza apos 6 meses -> backup periodico para GitHub                   |
+-----------------------------------------------------------------------------+
                                    |
                                    |  Sync via Git (repo qwenpaw-sync)
                                    |  + API REST bridge
                                    v
+-----------------------------------------------------------------------------+
|                              RAW.HQ (VPS Real)                               |
|                    2 vCPU | 4 GB RAM | 40 GB SSD NVMe                        |
|                         CEREBRO PRINCIPAL #2                                |
|                                                                              |
|  * Ubuntu 24.04 LTS (root SSH)                                              |
|  * Docker + Docker Compose                                                  |
|  * QwenPaw completo (Docker)                                                |
|  * Ollama (Docker) com modelos locais                                       |
|  * SearXNG (self-hosted meta-search)                                        |
|  * Nginx reverse proxy + SSL (Let's Encrypt)                                |
|  * Backup automatico                                                         |
|  * Redundancia: se Platform dormir, RAW.hq assume                            |
|  * Zero egress fees -> pode transferir dados livremente                      |
|                                                                              |
|  <-> Sync com Platform: git pull/push do repo qwenpaw-sync                   |
+-----------------------------------------------------------------------------+
                                    |
                                    |  Fallback / Bridge
                                    v
+-----------------------------------------------------------------------------+
|              MAQUINA LOCAL (Windows + WSL + Docker Leve)                      |
|                                                                              |
|  * Ollama ja instalado (fallback 100% offline)                                |
|  * Docker para SERVICOS LEVES APENAS:                                        |
|     - Bridge Python (conecta Platform/RAW.hq ao Ollama local)              |
|     - Healthcheck/orquestrador local                                         |
|     - NAO rodar QwenPaw completo nem Ollama duplicado no Docker local       |
|  * Projetos GitHub Icaro0310                                                |
|  * RAM local preservada ao maximo -- processamento pesado vai para VMs     |
|                                                                              |
|  ! RAM limitada -> Docker local APENAS para bridge e scripts leves         |
+-----------------------------------------------------------------------------+
                                    |
                                    |  Ping de redundancia (cron scripts)
                                    v
+-----------------------------------------------------------------------------+
|                      VMs SATELITE (Ping / Orquestracao)                      |
|                                                                              |
|  * Serv00 (FreeBSD, 520MB RAM) -> script de ping para Platform              |
|  * Sanfeng (1GB RAM) -> script de ping para RAW.hq                         |
|  * MonkeysCloud (1GB RAM, hiberna 30min) -> ping a cada 20min              |
|  * Lunes (128MB RAM) -> script de healthcheck minimo                        |
|                                                                              |
|  ! NENHUMA roda QwenPaw (RAM insuficiente)                               |
|  ! Apenas scripts Python simples: ping, cron, webhook                     |
+-----------------------------------------------------------------------------+
```

## Camadas

### Camada 1: AgentScope Platform (Cérebro #1)
- **Propósito:** Agente AI principal na nuvem, sempre disponível
- **Limitações:** 1GB storage, dorme após 48h sem interação, limpa após 6 meses
- **Mitigação:** Cron jobs de heartbeat (12h), backup periódico para GitHub
- **Processamento:** APIs cloud (DeepSeek, Groq, Gemini) — zero custo de compute local

### Camada 2: RAW.hq (Cérebro #2) — ⏳ BLOQUEADO
- **Propósito:** VPS real com controlo total, redundância se Platform dormir
- **Vantagens:** 40GB SSD, root SSH, Docker, zero egress fees
- **Status:** Deploy bloqueado (token inválido)

### Camada 3: Máquina Local (Fallback)
- **Propósito:** Último recurso offline, bridge para cloud
- **Componentes:** Ollama (2 modelos: llama3.2:1b, qwen2.5-coder:1.5b)
- **Bridge:** Flask proxy (porta 5000) com ngrok tunnel
- **RAM:** ~150MB total para serviços Docker leves

### Camada 4: VMs Satélite (Ping/Orquestração)
- **Propósito:** Manter serviços acordados, healthcheck distribuído
- **Regra:** NENHUMA roda QwenPaw — apenas scripts ping/cron
- **VMs:** Serv00, Sanfeng, MonkeysCloud, Lunes

## Fluxo de Dados

```
User → Telegram/Slack → AgentScope Platform
                              ↓
                    Multi-agente (Principal→Crítico→Síntese)
                              ↓
                    API Cloud (Groq/DeepSeek/Gemini)
                              ↓ (se falhar)
                    Bridge ngrok → Ollama Local
                              ↓
                    Resposta → User
```

## Fallback Chain (APIs)

| Prioridade | Provider     | Modelo                    | Velocidade | Custo |
|-----------|-------------|---------------------------|-----------|-------|
| 1         | Groq        | llama-3.1-8b-instant      | Muito rápida | Free |
| 2         | DeepSeek    | deepseek-chat             | Rápida    | Free tier |
| 3         | Gemini      | gemini-1.5-flash          | Rápida    | Free tier |
| 4         | OpenRouter  | auto                      | Variável  | Free tier |
| 5         | HuggingFace | Llama-3.1-8B-Instruct     | Média     | Free |
| 6         | Cerebras    | llama3.1-70b              | Rápida    | Free tier |
| 7         | Ollama Local| qwen2.5-coder:1.5b        | Lenta     | Free (offline) |

## Cron Schedule

| Job              | Schedule        | Descrição                         |
|-----------------|----------------|-----------------------------------|
| Heartbeat       | `0 */12 * * *` | Keepalive da Platform (12h)       |
| Daily Digest    | `0 8 * * *`    | Briefing matinal (8h)             |
| News Scan       | `0 14 * * *`   | Scan de notícias (14h)            |
| Healthcheck     | `0 * * * *`    | Check local (1h)                  |
| Git Sync        | `0 */6 * * *`  | Sync repo (6h)                    |
| Satellite Ping  | `*/10-30 * * * *` | Ping das VMs satélite          |

## Storage Budget (Platform — 1GB)

| Item                  | Tamanho Estimado |
|----------------------|-----------------|
| Configs & Skills     | ~50 KB          |
| Knowledge Base ReMe  | ~500 KB         |
| Conversation History | ~10 MB (rotated)|
| Logs                 | ~5 MB (rotated) |
| **Total**            | **~15 MB**      |
| **Disponível**       | **~985 MB**     |

## RAM Budget (Local)

| Componente        | RAM     |
|------------------|---------|
| Bridge Docker    | ~100 MB |
| Healthcheck      | ~50 MB  |
| **Total Docker** | **~150 MB** |
| Ollama (nativo)  | Variável (modelo-dependente) |
