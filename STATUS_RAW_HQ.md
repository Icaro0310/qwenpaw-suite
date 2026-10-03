# Optional RAW.hq integration / Integração opcional RAW.hq

## English

This public repository does not provision a RAW.hq account, store an account
status, or include deployment credentials. The local bridge and orchestrator
work without RAW.hq.

If you independently use a compatible remote health endpoint, set `RAW_URL` in
the environment where `orchestrator/healthcheck.py` runs. Leave it unset to
report the service as skipped. Keep provider tokens in a secret manager or
ignored local environment file, never in this repository.

## Português (BR)

Este repositório público não provisiona conta RAW.hq, guarda estado de conta
nem inclui credenciais de deploy. A bridge local e o orchestrator funcionam
sem RAW.hq.

Se usares por conta própria um endpoint remoto compatível de healthcheck,
define `RAW_URL` no ambiente onde `orchestrator/healthcheck.py` corre. Deixa-o
vazio para reportar o serviço como ignorado. Guarda tokens no gestor de
segredos ou em ficheiro local ignorado, nunca neste repositório.
