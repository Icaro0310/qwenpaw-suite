# Scheduling examples / Exemplos de agendamento

## English

No schedule is installed by this repository. Choose intervals based on the
service limits and availability you control.

- `orchestrator/healthcheck.py` runs once with `--once`; without it, the
  process repeats using `CHECK_INTERVAL` (default 3600 seconds).
- `orchestrator/satellite-ping.py --once` performs one round. Use cron or
  Windows Task Scheduler if you want periodic checks.
- `orchestrator/sync-github.py` is dry-run by default. A scheduled mutating
  sync must explicitly include `--apply` (or `--auto`), and will stage all
  changes, commit and push `origin/main` for the selected repository.

Example Linux cron line, after configuring the variables in a protected
service environment:

```cron
*/15 * * * * cd /path/to/qwenpaw-suite && python3 orchestrator/satellite-ping.py --once
```

Do not put API keys, webhook URLs or tunnel tokens directly in a crontab or
tracked file.

## Português (BR)

Este repositório não instala nenhum agendamento. Escolhe intervalos de acordo
com os limites e a disponibilidade dos serviços que controlas.

- `orchestrator/healthcheck.py --once` faz uma verificação; sem essa opção o
  processo repete com `CHECK_INTERVAL` (padrão 3600 segundos).
- `orchestrator/satellite-ping.py --once` executa uma ronda. Usa cron ou Task
  Scheduler do Windows se quiseres verificações periódicas.
- `orchestrator/sync-github.py` é dry-run por omissão. Um sync agendado que
  altera dados precisa incluir explicitamente `--apply` (ou `--auto`), e faz
  stage de todas as alterações, commit e push de `origin/main`.

Exemplo cron Linux, depois de configurares as variáveis num ambiente protegido:

```cron
*/15 * * * * cd /path/to/qwenpaw-suite && python3 orchestrator/satellite-ping.py --once
```

Não coloques API keys, URLs de webhook ou tokens de túnel diretamente no
crontab ou em ficheiros rastreados.
