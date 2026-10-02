# Fase 2 - RAW.hq - Status Atual

## Status: ⏳ BLOQUEADO (Token ainda inválido para deploy)

## Última Tentativa: 2026-08-12

## Conta RAW.hq
- **Email:** `<your-email>` (conta pessoal do maintainer)
- **API Token:** `<RAW_API_TOKEN>`
- **CLI:** `rawhq@0.6.0` instalado globalmente via npm
- **Config:** `C:\Users\Utilizador\.raw\config.json`
- **Variável de ambiente:** `RAW_API_TOKEN` configurada (User scope)
- **Autenticação:** `raw whoami` funciona ✅
- **Deploy:** Falha com "the token you have provided is invalid" ❌

## Diagnóstico Atualizado (2026-08-12)
- Conta criada com sucesso e CLI autenticado
- `raw whoami` reconhece a conta corretamente
- O novo token `<RAW_API_TOKEN>` foi configurado
- Deploy continua a falhar - pode ser necessário:
  1. Verificação de email pendente
  2. Ativação manual da conta no dashboard RAW.hq
  3. Limitação do plano gratuito (free tier pode não estar disponível)

## Ação Necessária
1. **Verificar email** da conta para links de verificação/ativação
2. **Verificar dashboard RAW.hq** em https://app.rawhq.io para status da conta
3. **Contactar suporte RAW.hq** se o problema persistir

## Comandos de Verificação
```bash
# Verificar status da conta
$env:RAW_API_TOKEN = "<RAW_API_TOKEN>"
raw whoami

# Listar servers (se houver algum)
raw ls

# Verificar tipos disponíveis
raw types

# Verificar regiões disponíveis
raw regions

# Tentar deploy novamente
raw deploy --type raw-free --region eu
```

## Especificações da VM Gratuita (raw-free)
- **CPU:** 2 vCPU
- **RAM:** 4 GB
- **Storage:** 40 GB SSD NVMe
- **OS:** Ubuntu 24.04
- **Custo:** $0/mo (grátis)
- **Região:** eu (Alemanha)

## Próximos Passos (Após Deploy Bem-sucedido)

1. **Acessar VM via SSH:** `raw ssh <nome-da-vm>`
2. **Configurar segurança básica** (UFW, fail2ban)
3. **Instalar Docker + Docker Compose**
4. **Deploy QwenPaw completo via Docker**
5. **Configurar backup automático**
6. **Configurar sync com GitHub**

## Alternativas
Se RAW.hq continuar com problemas, considerar:
- **Hoody:** https://hoody.com (máquina gratuita 4GB RAM)
- **Oracle Cloud:** Always Free tier
- **Google Cloud:** Free tier limitado
- **AWS:** Free tier (12 meses)
