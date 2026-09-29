# VMs Satélite - Configuração e Deploy

## Visão Geral

As VMs satélite NÃO rodam QwenPaw (RAM insuficiente). Servem apenas para:
- Ping de keepalive (manter Platform/RAW.hq acordados)
- Healthcheck distribuído
- Webhook de notificação

Script utilizado: `satellite-ping.py` (do repo qwenpaw-orchestrator)

---

## VM 1: Serv00

| Spec | Valor |
|------|-------|
| OS | FreeBSD |
| RAM | 520 MB |
| Função | Ping para AgentScope Platform |
| Schedule | `*/10 * * * *` (cada 10 min) |

### Deploy
```bash
# SSH para Serv00
ssh user@serv00.example.com

# Instalar dependências
pip install requests

# Copiar script
scp satellite-ping.py user@serv00.example.com:~/

# Configurar variáveis
export VM_NAME=serv00
export PING_TARGETS=https://platform.agentscope.io/api/health
export PING_INTERVAL=600

# Crontab
crontab -e
# Adicionar:
*/10 * * * * cd ~ && VM_NAME=serv00 PING_TARGETS=https://platform.agentscope.io/api/health python3 satellite-ping.py --once >> ping.log 2>&1
```

---

## VM 2: Sanfeng

| Spec | Valor |
|------|-------|
| RAM | 1 GB |
| Função | Ping para RAW.hq |
| Schedule | `*/10 * * * *` (cada 10 min) |

### Deploy
```bash
ssh user@sanfeng.example.com
pip install requests
# Copiar satellite-ping.py

# Crontab
*/10 * * * * cd ~ && VM_NAME=sanfeng PING_TARGETS=http://raw-hq-ip:8080/health python3 satellite-ping.py --once >> ping.log 2>&1
```

---

## VM 3: MonkeysCloud

| Spec | Valor |
|------|-------|
| RAM | 1 GB |
| Hibernação | Após 30 min inatividade |
| Função | Ping dual (Platform + RAW.hq) |
| Schedule | `*/20 * * * *` (cada 20 min — antes dos 30min de hibernação) |

### Deploy
```bash
ssh user@monkeyscloud.example.com
pip install requests

# Crontab — a cada 20min para evitar hibernação
*/20 * * * * cd ~ && VM_NAME=monkeyscloud PING_TARGETS=https://platform.agentscope.io/api/health,http://raw-hq-ip:8080/health python3 satellite-ping.py --once >> ping.log 2>&1
```

---

## VM 4: Lunes

| Spec | Valor |
|------|-------|
| RAM | 128 MB |
| Função | Healthcheck mínimo |
| Schedule | `*/30 * * * *` (cada 30 min) |

### Deploy
```bash
ssh user@lunes.example.com
pip install requests

# Script mínimo (128MB RAM = muito limitado)
*/30 * * * * cd ~ && VM_NAME=lunes PING_TARGETS=https://platform.agentscope.io/api/health python3 satellite-ping.py --once >> ping.log 2>&1
```

---

## Notas

- **Nenhuma VM satélite roda QwenPaw** (RAM insuficiente)
- Apenas scripts Python simples: ping, cron, webhook
- Dependência única: `requests` (instalável via pip)
- Logs rotativos recomendados para VMs com pouco storage
- URLs dos targets serão atualizadas quando os serviços estiverem configurados
