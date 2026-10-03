# Multi-agent pattern / Padrão multi-agente

## English

This repository does not implement a multi-agent runtime. The bridge is a
single-model HTTP adapter; orchestration, role prompts and model selection
belong to the external client or platform.

A generic optional pattern is:

1. **Primary:** produces a draft answer or plan.
2. **Reviewer:** checks the draft against a rubric and returns issues only.
3. **Synthesizer:** combines the draft and review into the final response.

Keep each role's instructions separate, set timeouts and output limits, and
configure provider credentials in the platform's secret manager. Do not assume
that a model named in an old example is available or still has a free tier.

## Português (BR)

Este repositório não implementa um runtime multi-agente. A bridge é um adapter
HTTP para um único modelo; orquestração, prompts de papéis e escolha de modelos
ficam no cliente ou plataforma externa.

Um padrão genérico opcional:

1. **Principal:** produz um rascunho ou plano.
2. **Revisor:** verifica o rascunho com uma rubrica e devolve apenas problemas.
3. **Síntese:** combina o rascunho e a revisão na resposta final.

Mantém as instruções de cada papel separadas, configura timeouts e limites de
saída, e guarda credenciais no gestor de segredos da plataforma. Não assumes
que um modelo citado em exemplo antigo esteja disponível ou continue gratuito.
