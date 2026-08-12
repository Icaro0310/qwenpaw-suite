# Configuração ngrok - QwenPaw Bridge

## Status: ✅ CONFIGURADO

## Credenciais

### Authtoken
```
<NGROK_AUTHTOKEN>
```

### Configuração Salva Em
- **Config file:** `C:\Users\Utilizador\AppData\Local\ngrok\ngrok.yml`
- **Variável de ambiente:** `NGROK_AUTHTOKEN` (User scope)

## Configuração Realizada (2026-08-12)

### 1. Authtoken adicionado ao ngrok
```bash
ngrok config add-authtoken <NGROK_AUTHTOKEN>
# ✅ Authtoken saved to configuration file
```

### 2. Variável de ambiente configurada
```powershell
# Sessão atual + persistente (User scope)
$env:NGROK_AUTHTOKEN = "<NGROK_AUTHTOKEN>"
[System.Environment]::SetEnvironmentVariable("NGROK_AUTHTOKEN", "<NGROK_AUTHTOKEN>", "User")
```

### 3. ngrok.yml verificado
```bash
ngrok config check
# ✅ Valid configuration file
```

## Como Usar

### Expor a Bridge (porta 5000)
```bash
cd C:\Users\Utilizador\qwenpaw-bridge
.\ngrok.exe http 5000
```

### URL pública gerada
Após iniciar o ngrok, copiar a URL gerada (ex: `https://abc123.ngrok-free.app`)
e usar como Base URL do Ollama-Local-Bridge na AgentScope Platform.

### Iniciar tudo automaticamente
```bash
C:\Users\Utilizador\qwenpaw-bridge\start-all.bat
```

## Notas
- O plano gratuito do ngrok gera URLs dinâmicas (mudam a cada restart)
- Para URLs fixas, considerar upgrade para plano pago ou usar alternativas (Cloudflare Tunnel)
- A bridge local roda na porta 5000 e proxifica para Ollama em 11434
