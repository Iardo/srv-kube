# Self-Hosted Services

Collection of self-hosted services.

---

> **Heads up:** this is my personal repo, with my own hosts and config baked in.
> It's not meant to be generic or reusable out of the box. Use it as a
> reference, not a drop-in. If you want to run it yourself, keep your own
> fork with your own hosts. I make no promises to fix or respond to
> anything, I change this however and whenever suits me.

---

## How it Works

Two ways to deploy a host:
- `./start.py`: local, brings that one host's `docker-compose.yml` up directly.
- Komodo: a web UI that deploys to any host remotely, and auto-redeploys on git push.

Komodo is optional, it's itself just another service in this repo (`serv/komodo`).

Setup, once: pick one host to run Komodo on (include `serv/komodo` in its
`docker-compose.yml`) and bring it up with `./start.py`. That becomes your central
Komodo instance.\
From then on, every other host is deployed and managed from that Komodo's web UI
instead: see [Komodo Notes](#komodo-notes) below for how a host connects to it.

`./start.py` still works on any host at any time, Komodo-managed or not, it's always
there as a plain fallback, not something Komodo locks you out of.

---

## Host Config

Copy `/host/@host-sample` to make a new host, it has:
```
docker-compose.yml  : Which services to install (the "include" list)
.env                : Non-secret overrides (ports, timezone, etc), the ports section is auto-generated
.env-secrets        : One dummy value per secret var, tracked in git, just a reference
.env-secrets.local  : Gitignored, real secret values go here, never wiped by a re-deploy
```

`.env-secrets.local` is what you edit by hand (or over SSH on a VPS) to put real
secret values in.\
Komodo copies `.env-secrets` into `.env-secrets.local` automatically on first deploy,
so the file already exists and is ready to fill in.\
Whatever you set in `.env-secrets.local` always wins over `.env-secrets` for the same
variable.

---

## Adding a New Host

After copying `/host/@host-sample` (above), decide how this host gets deployed: local
/ self-managed, or remote via Periphery.

Either way, there's nothing to configure in Komodo itself afterward: the Resource
Sync (see [Komodo Notes](#komodo-notes) below) picks up this host's folder
automatically, once it's committed.

### Local / Self-managed

A desktop or laptop you run commands on yourself: include `serv/komodo` in its
`docker-compose.yml`, then `./start.py` on it once: it runs its own Core+Periphery
and manages only itself.

### Remote (Periphery)

A VPS, managed from your central Komodo instead of logging into it to deploy:
**normally set up as inbound** (Core dials out to it), which is simplest and needs a
reachable public IP. Only use outbound mode instead if it doesn't have one (e.g.
behind home NAT): that variant is covered separately in
[serv/komodo/readme.md](serv/komodo/readme.md), not here.

#### 1. Create the Server in Komodo

In your central Komodo: create a Server named after this host, `address` set to
`http://<this-host's-public-ip-or-domain>:9120`, enabled.

#### 2. On the VPS: install Docker

[docs.docker.com](https://docs.docker.com/engine/install/) (full apt command for
Ubuntu, plus post-install steps, in [serv/komodo/readme.md](serv/komodo/readme.md)).

#### 3. On the VPS: install Periphery (inbound)

As root:

```bash
curl -sSL https://raw.githubusercontent.com/moghtech/komodo/main/scripts/setup-periphery.py \
  | python3 - --version v2.3.2
sudo sed -i 's|^port = 8120|port = 9120|' /etc/komodo/periphery.config.toml
sudo systemctl restart periphery
```

`--version` must match this repo's Core image tag
([serv/komodo/docker-compose.yml](serv/komodo/docker-compose.yml)), otherwise Core
refuses the connection with "Periphery version mismatch".

#### 4. On the VPS: configure the firewall (ufw)

Open SSH, HTTP/HTTPS (for Caddy), and Periphery's port, then enable. Add the `allow`
rules **before** `enable`, otherwise the `default deny incoming` locks out SSH as soon
as it's active:

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 9120/tcp
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw enable
sudo ufw status verbose
```

Swap `22` for the actual SSH port first if this host doesn't use the default one.

If this host also includes `caddy-ui` (`caddy-ui-frontend`/`caddy-ui-backend`), it never
gets an auto-generated subdomain of its own (`source/caddy.py` deliberately skips the
`caddy` service itself, so a broken caddyfile can't also lock you out of the UI that'd
fix it), so it's reached directly by IP and port instead, both need opening too:
```bash
sudo ufw allow 7002/tcp # CADDY_WEB_UI_HTTP, the frontend
sudo ufw allow 7003/tcp # CADDY_WEB_UI_API, called directly from the browser
```
(Port numbers above are this repo's convention, defaults; use whatever
`CADDY_WEB_UI_HTTP`/`CADDY_WEB_UI_API` actually resolve to in that host's `.env`.)

Also open port `9120` (and `22`/`80`/`443` as needed) in the cloud provider's own
firewall/security group if it has one, separate from the OS firewall above.

Full install details, verification, and troubleshooting:
[serv/komodo/readme.md](serv/komodo/readme.md).

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

### Resource Sync (one-time per Komodo instance)

- Resources → Resource Syncs → New
- Name it anything, e.g. `srv-kube`
- Source: "Files on Server"
- Resource Path: `/mnt/srv-kube-dev/host`
- Check "Include Variables" and "Include User Groups"
- Execute Sync (creates every host's Server/Stack resources)

File detection under that path is recursive, so adding a new host is just committing
its folder under `host/`, nothing to configure here ever again.

### Filling in Real Secrets (first Deploy of a host)

1. Deploy the Stack once from Komodo. It comes up with dummy values,
   `pre_deploy.command` copies `.env-secrets` into `.env-secrets.local` on this
   first run, since it doesn't exist yet.
2. On that host, edit the real values into:
   ```
   /etc/srv-kube/host/<host-name>/.env-secrets.local
   ```
   `/etc/srv-kube` is Komodo's own clone (see above), not your dev clone.
3. Deploy the Stack again from Komodo so the containers pick up the real values.

`.env-secrets.local` is gitignored and never touched by `git checkout -f` /
`git pull --force`, so it survives every deploy after this, you only come back to
it when a secret actually changes.

A database only ever reads its password env var once, to create that user
when its volume is first empty. Changing it in `.env-secrets.local` afterward
doesn't reach the database on its own, nothing re-applies it there, that
service is then locked out of its own database. Safe to do anyway *only* for
a service whose `post_deploy` re-syncs it on every deploy (see
`serv/linkace/task/task-sync-db-password.sh` for the pattern: a separate,
never-rotated root password lets it log in and re-apply the real one
regardless of how many times that's changed since). Any other
database-backed service without that same wiring still gets permanently
locked out the moment its password changes post-deploy.

---

## Komodo Gotchas

### A Resource Sync can't declare itself
A Resource Sync's `resource_path` can't point at a file that declares a
`[[resource_sync]]` for that same sync: it'd try to update its own config while still
running the read that found the change, which always fails as "busy", on every run,
not just the first. This is why the Resource Path above is a plain folder to scan
(`host/`), not a committed config file declaring the sync itself.

### Files on Host nests by the sync's own name
A `Files on Server` sync resolves a *relative* `resource_path` under a folder named
after the sync itself (e.g. `conf/komodo/<sync-name>/`), not the mounted root
directly. Doesn't apply to the absolute path used above, only came up while chasing
the previous gotcha.

### A host's own Periphery can't connect to a remote Core
`serv/komodo`'s bundled Periphery has `PERIPHERY_CORE_ADDRESS` hardcoded to
`ws://komodo-core:9120`, its own bundled Core's internal Docker DNS name. It can't be
pointed at a different, remote Core. For a host managed from elsewhere, don't include
`serv/komodo` there at all, install Periphery natively instead (see
[Adding a New Host](#adding-a-new-host) near the top).

---

## Wildcard Domains (Caddy)

If a host includes `caddy`, `./init.py` writes it a `caddyfile` at `host/<host-name>/caddyfile`.\
If it also includes `dnsmasq`, `./init.py` writes it a `dnsmasq.conf` the same way,
with a wildcard rule so `*.<host-name>` resolves to `127.0.0.1`,
and a `dnsmasq.sh` script that points your machine at it.

Which file actually gets mounted can be overridden per-host,
set `CADDY_CADDYFILE` / `DNSMASQ_CONF` in that host's `.env` to a path
relative to `serv/caddy` / `serv/dnsmasq`.\
Point it somewhere other than
that host's own auto-generated file to stop `./init.py` from touching it.

For those domains to actually resolve on your machine, run that script once,
on the machine, per host that has `dnsmasq` (needs `sudo`):
```
./host/<host-name>/dnsmasq.sh
```
It's rewritten on every `./init.py` run, re-run it if you add a host or the port changes.

---

## GPU-bound Services (llama.cpp, ComfyUI)

The `llama-cpp` and `comfyui` need direct GPU access (CUDA / Apple's Metal API), so on
every host in this repo today they're installed straight onto the machine instead of
through Docker, which means `./start.py` and `./init.py` do **not** cover them.

See [docs/services-gpu-bound.md](docs/services-gpu-bound.md) for full requirements,
setup (Linux/MacOS and Windows), running commands, and editor integrations.

---

## Clean-up

Stopping services doesn't delete their data or config.
Most services store everything under `/serv/<service>/data`, remove it by hand to start fresh.
