# frp-client

Local/dev-machine side of the `frp-server`/`frp-client` pair. Deploy this on whatever machine has the web server you want to share, it dials out to `serv/frp-server` on a VPS and gets you a public URL for it, ngrok-style.

`serv/frp-server` is the other half, it must be deployed first.

## Setup

1. Deploy `serv/frp-server` first, note its host's public IP/domain and the port it published for `FRP_SERVER_TUNNEL`.
2. On this host's `.env-secrets.local`, set:
   - `FRP_CLIENT_SERVER_ADDR`: `serv/frp-server`'s host, IP or domain.
   - `FRP_CLIENT_SERVER_PORT`: whatever port it published for `FRP_SERVER_TUNNEL`.
   - `FRP_CLIENT_AUTH_TOKEN`: the exact same value as `serv/frp-server`'s `FRP_SERVER_AUTH_TOKEN`.
3. Add a `[[proxies]]` block to `frpc.toml` for each local port you want to share, see the commented example already in that file. Restart the container after editing it.
4. The resulting URL is `http://<subdomain-or-domain>:<FRP_SERVER_VHOST_HTTP>/`, see `serv/frp-server/readme.md` for the DNS side of that.

This container uses `network_mode: host` on purpose, `localPort` in a proxy block points at a port on this machine directly (e.g. a local dev server on `:3000`), not at another container.
