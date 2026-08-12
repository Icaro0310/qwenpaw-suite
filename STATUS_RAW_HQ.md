# Fase 2 - RAW.hq - Status Atual

## Status: ⏳ BLOQUEADO (Ação Manual Necessária)

## Problema
O deploy da VM gratuita falhou com erro: "the token you have provided is invalid"

## Diagnóstico
- Conta RAW.hq criada com sucesso: `icarogalvao5@gmail.com`
- CLI autenticado corretamente
- Token configurado no arquivo: `C:\Users\Utilizador\.raw\config.json`
- Sistema enviou NOVO TOKEN para o email (token anterior parece sem permissão de deploy)

## Ação Necessária
1. **Verificar email** `icarogalvao5@gmail.com` para o novo token RAW.hq
2. **Atualizar token** no arquivo de configuração ou re-executar `raw init`
3. **Tentar deploy novamente**: `raw deploy --type raw-free --region eu`

## Comandos para Continuar

### Após obter novo token:
```bash
# Opção 1: Re-autenticar
raw logout
echo "icarogalvao5@gmail.com" | raw init

# Opção 2: Atualizar token manualmente
# Editar C:\Users\Utilizador\.raw\config.json
# Substituir "apiToken" pelo novo token do email

# Deploy
raw deploy --type raw-free --region eu
```

## Comandos de Verificação
```bash
# Verificar status da conta
raw whoami

# Listar servers (se houver algum)
raw ls

# Verificar tipos disponíveis
raw types

# Verificar regiões disponíveis
raw regions
```

## Especificações da VM Gratuita (raw-free)
- **CPU:** 2 vCPU
- **RAM:** 4 GB
- **Storage:** 40 GB SSD
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
