# Projetos Pessoais — Ícaro Galvão

Mapa dos projetos pessoais ativos. Referenciado por ferramentas internas e pelo ecossistema Devin.

---

## 🐾 PetSaas — PetCare Micro-SaaS
- **Repo:** [Icaro0310/PetSaas](https://github.com/Icaro0310/PetSaas) (public)
- **Stack:** Flutter (Dart), Supabase, Firebase, Material 3
- **Estado:** ativo — MVP com 11 fases, app mobile para gestão de pets (saúde, vacinas, agenda)
- **Infra:** Supabase (auth, DB, edge functions), Firebase (crashlytics, messaging)
- **Notas:** `AGENTS.md` + skills `saas-*`; modo 100% local via `--local`; i18n pt-BR

## 🏝️ living-island — Ilha Viva 2.5D
- **Repo:** privado (local: `~/living-island`)
- **Stack:** Phaser 3 (JS), Tiled, Express + Socket.io (servidor)
- **Conceito:** ilha procedural viva com render 2.5D; 70+ scripts de geração/validação de assets
- **Branch ativa:** `spatial-2.5d`
- **Reuso técnico:** shader walker, asset-pipeline Tiled, QA de spritesheets

## 🗡️ wilson-reborn — RPG Maker MZ "Wilson" 2.5D
- **Repo:** fork privado (local: `~/wilson-reborn`)
- **Stack:** JavaScript, RPG Maker MZ
- **Conceito:** port do legado SceneWorld para rendering pipeline 2.5D
- **Reuso técnico:** partição de sprites, viewport tests, system-upgrade Jest

## 🤖 Devin Ecosystem — Powerups para Devin Desktop
- **Hub privado:** [Icaro0310/devin-powerups](https://github.com/Icaro0310/devin-powerups)
- **Projetos públicos:**
  - `devin-internals-spec` — mapa dos stores internos do Devin (sessions.db, acp-messages, state.vscdb) + detetor de schema
  - `devin-redact` — scanner de segredos para sessões Devin exportadas
- **Conceito:** um repo por projeto, sessão Devin isolada por repo (ACP), docs EN + pt-BR
- **Roadmap:** Wave 0 ✅ → Wave 1 (`devin-history`, `devin-doctor`, `devin-pm`) → Waves 2–4

## 🐌 qwenpaw-sync — Este repo
- **Stack:** Python 3, FastAPI, Docker Compose, ngrok, RAW.hq
- **Conceito:** orquestrador multi-agente local (QwenPaw) com bridge para VMs satélite
- **Componentes:**
  - `bridge/` — serviço FastAPI + Docker
  - `orchestrator/` — healthcheck, sync-github (cron 6h), satellite-ping
- **Config docs:** `API_KEYS_CONFIG`, `NGROK_CONFIG`, `CRON_SCHEDULE`, `MULTI_AGENT_CONFIG`, `AGENTSCOPE_CONFIG_GUIDE`

## 📚 Arquivo de estudo (repos removidos)
- `unyleya_projeto_cicd` + `azure-voting-app` — pipeline CI/CD académica (Azure DevOps, AKS, Redis voting app)
- `MobEAD` — mobilidade EAD (sonar configs)
- Knowledge extraído para Obsidian/memória antes da remoção.

---

*Mantido por Devin (maintainer). Última revisão: 2026-09-29*
