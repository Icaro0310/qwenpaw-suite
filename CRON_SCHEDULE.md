# Cron Schedule - Infraestrutura QwenPaw

## AgentScope Platform

| Job | Cron Expression | Hora | Descrição |
|-----|----------------|------|-----------|
| Heartbeat Keepalive | `0 */12 * * *` | 00:00, 12:00 | Mantém Platform acordada (sleep após 48h) |
| Daily Digest | `0 8 * * *` | 08:00 | Briefing matinal: tarefas, notícias, status projetos |
| News Scan | `0 14 * * *` | 14:00 | Scan Hacker News, ArXiv, GitHub trending |

## Máquina Local

| Job | Cron Expression | Intervalo | Descrição |
|-----|----------------|-----------|-----------|
| Healthcheck | `0 * * * *` | 1 hora | Verifica Ollama, Bridge, Platform, Satellites |
| Git Sync | `0 */6 * * *` | 6 horas | Sync automático do repo qwenpaw-sync |

## VMs Satélite

| VM | Cron Expression | Intervalo | Target |
|----|----------------|-----------|--------|
| Serv00 | `*/10 * * * *` | 10 min | AgentScope Platform |
| Sanfeng | `*/10 * * * *` | 10 min | RAW.hq |
| MonkeysCloud | `*/20 * * * *` | 20 min | Platform + RAW.hq |
| Lunes | `*/30 * * * *` | 30 min | Platform |

## Timeline Diária

```
00:00  ▐ Heartbeat keepalive
       │
06:00  ▐ Git sync
       │
08:00  ▐ Daily Digest → Telegram
       │
10:00  │
       │
12:00  ▐ Heartbeat keepalive
       ▐ Git sync
       │
14:00  ▐ News Scan (HN + ArXiv)
       │
18:00  ▐ Git sync
       │
00:00  ▐ Git sync
       ▐ Heartbeat keepalive
```

Satellites pingam continuamente a cada 10-30 min.
Healthcheck local roda a cada hora.
