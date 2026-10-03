# Satellite hosts / Hosts satélite

## English

The satellite utility is a generic HTTP pinger; this repository does not name,
provision, or contain credentials for any remote host.

1. Copy or clone this repository on a host you administer.
2. Install Python 3 and `requests` (`python3 -m pip install requests`, or use a
   virtual environment).
3. Set `VM_NAME` and `PING_TARGETS` (`name=url` pairs are used by the
   orchestrator healthcheck; the standalone pinger accepts comma-separated
   URLs). Set `WEBHOOK_URL` only if you want failure notifications.
4. Run `python3 orchestrator/satellite-ping.py --once` and verify its JSON
   result before scheduling it.
5. If periodic execution is needed, use cron/systemd on Linux/BSD or Task
   Scheduler on Windows. Choose a cadence appropriate for your provider.

The utility sends HTTP GET requests to configured endpoints; it does not run
QwenPaw, install a remote agent, or keep a host awake unless the target service
itself treats those requests as activity.

## Português (BR)

O utilitário satélite é um pinger HTTP genérico; este repositório não identifica
nem provisiona hosts remotos e não contém as respetivas credenciais.

1. Copia ou clona o repositório num host que administras.
2. Instala Python 3 e `requests` (`python3 -m pip install requests`, de
   preferência num virtualenv).
3. Define `VM_NAME` e `PING_TARGETS` (o healthcheck aceita pares `name=url`; o
   pinger standalone aceita URLs separados por vírgula). Define `WEBHOOK_URL`
   só se quiseres alertas de falha.
4. Executa `python3 orchestrator/satellite-ping.py --once` e verifica o JSON
   antes de agendar.
5. Se precisares de execução periódica, usa cron/systemd em Linux/BSD ou Task
   Scheduler no Windows. Escolhe uma cadência adequada ao provider.

O utilitário faz pedidos HTTP GET aos endpoints configurados; não instala um
agente remoto nem mantém um host acordado, a menos que o próprio serviço conte
esses pedidos como atividade.
