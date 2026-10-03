# Optional tunnel / Túnel opcional

## English

The bridge and Docker Compose bind to loopback by default. No tunnel is started
by the launcher. Prefer a private VPN or SSH tunnel when a remote client needs
to reach the bridge.

If you deliberately use ngrok or another tunnel:

1. Install/configure the tunnel client using its current official instructions.
2. Keep its authentication token in the tunnel client's local config or a
   secret store, never in this repository.
3. Set `BRIDGE_API_KEY` before exposing the bridge. Non-loopback bridge binds
   refuse to start without it.
4. Start a tunnel to the local bridge port and configure the remote client to
   use `Authorization: Bearer <BRIDGE_API_KEY>`.
5. Revoke the tunnel token and bridge key if they are exposed. Remember that
   tunnel URLs and query strings must not be copied into logs or public reports.

A tunnel makes a local service reachable remotely; it does not add TLS/auth to
an unsafe bridge configuration. Use a strong key and restrict allowed network
origins.

## Português (BR)

A bridge e o Docker Compose escutam em loopback por omissão. O launcher não
inicia túnel. Prefere VPN privada ou SSH quando um cliente remoto precisa de
aceder à bridge.

Se decidires usar ngrok ou outro túnel:

1. Instala/configura o cliente do túnel pelas instruções oficiais atuais.
2. Guarda o token no config local do cliente ou num secret manager, nunca neste
   repositório.
3. Define `BRIDGE_API_KEY` antes de expor a bridge. Binds fora de loopback
   recusam iniciar sem essa chave.
4. Inicia o túnel para a porta local e configura o cliente remoto com
   `Authorization: Bearer <BRIDGE_API_KEY>`.
5. Revoga tokens de túnel e bridge se forem expostos. Não copies URLs de túnel
   ou query strings para logs/relatórios públicos.

Um túnel torna o serviço local acessível remotamente; não acrescenta TLS/auth a
uma bridge insegura. Usa uma chave forte e restringe origens de rede.
