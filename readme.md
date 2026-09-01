# Dockerfiles

Collection of docker files for a lot of different services.

---

## How This Works

Two ways to deploy,
`./start.py` (local, one host at a time),
or Komodo (web UI, deploys to any machine, auto-redeploys on git push).

Komodo is optional,
Komodo itself is just another service in this repo.

First time cloning the repo: run `./start.py`, pick a host, install Komodo on it.
From then on, use Komodo for every other host.
You can always fall back to `./start.py` for any host, Komodo or not.

---

## Host Config

Copy `/host/@host-sample` to make a new host, it has:
```
docker-compose.yml  : Which services to install (the "include" list)
.env                : Non-secret overrides (ports, timezone, etc), the ports section is auto-generated
.env-secrets        : One dummy value per secret var, tracked in git, just a reference
.env-secrets.local  : Gitignored, real secret values go here, never wiped by a re-deploy
```

The file `.env-secrets.local` is what you edit by hand (or over SSH on a VPS) to put real values in.\
Komodo copies `.env-secrets` into it automatically the first time, so it's ready to fill in.\
It always wins over `.env-secrets` when both set the same variable.

---

## Scripts

```
./init.py  : One-time setup, generates ports, runs each service's init.sh
./start.py : Docker compose up for a host
./stops.py : Docker compose down for a host (does not remove volumes)
```
Run with no args to pick a host from a list, or `--host=name` to skip the prompt.

Each service can also have a `/task` folder (gen directories, fix permissions, backup, restore).\
Run them from the service's own directory `./task/data-set-permissions.sh`, not from inside `/task`.

---

## Komodo Notes

Komodo clones this repo into its own directory (`/etc/srv-kube`),
separate from wherever you're developing, never point it at your dev clone.
A deploy runs `git checkout -f` + `git pull --force`,
which wipes any uncommitted changes in whatever directory it's pointed at.

Commit and push before every deploy, Komodo only ever sees what's on `origin`.

---

## Wildcard Domains (Caddy)

If a host includes `caddy`, `./init.py` writes it a `caddyfile` at `host/<host-name>/caddyfile`.\
If it also includes `dnsmasq`, `./init.py` writes it a `dnsmasq.conf` the same way,
with a wildcard rule so `*.<host-name>` resolves to `127.0.0.1`.

Which file actually gets mounted can be overridden per-host,
set `CADDY_CADDYFILE` / `DNSMASQ_CONF` in that host's `.env` to a path
relative to `serv/caddy` / `serv/dnsmasq`.\
Point it somewhere other than
that host's own auto-generated file to stop `./init.py` from touching it.

For those domains to actually resolve on your machine, point it at dnsmasq once:
```
sudo mkdir -p /etc/systemd/resolved.conf.d
printf '[Resolve]\nDNS=127.0.0.1:<DNSMASQ_DNS>\nDomains=~<host-name> ~<host-name>\n' | sudo tee /etc/systemd/resolved.conf.d/dnsmasq-wildcards.conf
sudo systemctl restart systemd-resolved
```
This file isn't auto-updated, re-run it if you add a host or the port changes.

---

## Clean-up

Stopping services doesn't delete their data or config.
Most services store everything under `/serv/<service>/data`, remove it by hand to start fresh.
