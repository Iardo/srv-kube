# frp-server

Public-IP side of the `frp-server`/`frp-client` pair. Deploy this to a VPS host, it's what makes a local dev server reachable from the internet, ngrok-style.

`serv/frp-client` is the other half, it runs on the local/dev machine that actually has the web server to share.

## Ports

- `FRP_SERVER_TUNNEL`: where `frpc` (the client) connects in.
- `FRP_SERVER_VHOST_HTTP`: public HTTP entrypoint, this is the port visitors actually hit. Not reverse-proxied through `serv/caddy`, it has to route by whatever subdomain the client proxy picks, not one fixed route.
- `FRP_SERVER_PANEL`: dashboard, unauthenticated by design upstream, bound to loopback only. Reach it through an SSH tunnel:
  ```
  ssh -L 7500:127.0.0.1:<FRP_SERVER_PANEL> <host>
  ```
  Then open `http://localhost:7500`.

## DNS

Point a wildcard record at this host's public IP, e.g. `*.tunnel.yourdomain.com -> <vps-ip>`, so any subdomain `frpc` proxies through resolves here. `subDomainHost` isn't set in `frps.toml` by default, set it yourself if you want `frpc` to pick subdomains instead of full custom domains, see [frp's README](https://github.com/fatedier/frp#dynamic-subdomains).

Visitors reach `http://<whatever-subdomain-or-domain-frpc-set>:<FRP_SERVER_VHOST_HTTP>/`. This repo doesn't automate HTTPS for the tunneled traffic itself, see frp's own docs on `vhostHTTPSPort` if that matters for your use case.

## Setup

1. Deploy this first, `FRP_SERVER_AUTH_TOKEN` gets generated on this host.
2. Copy that same value into `serv/frp-client`'s host, in its `.env-secrets.local`, as `FRP_CLIENT_AUTH_TOKEN`. They must match exactly, or `frpc` fails to authenticate.
