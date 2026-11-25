# Komodo Periphery: Installation

Install Periphery on a Linux server that you want Komodo to manage.

```text
                    Komodo Core
                         │
                         │ WebSocket
                         │
                         ▼
                ┌─────────────────┐
                │    Periphery    │
                │                 │
                │  Target Server  │
                └────────┬────────┘
                         │
                         ▼
                       Docker
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
           Stack 1    Stack 2    Stack 3
```

## Requirements

- Linux with `systemd`
- Docker installed and running
- `curl` and Python 3
- The server can reach Komodo Core

Install Docker if it's not there yet (Ubuntu, see
[docs.docker.com](https://docs.docker.com/engine/install/ubuntu/) for other distros):

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Post-install (see
[docs.docker.com](https://docs.docker.com/engine/install/linux-postinstall/) for more):
run Docker without `sudo`, and have it start on boot.

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

Verify Docker, no `sudo` needed:

```bash
docker run hello-world
```

There are two ways Core and Periphery can connect, pick one **before** installing:

- **Inbound** (default, use this if the host has a public IP, e.g. a VPS): Core dials
  out to Periphery. Periphery just listens, nothing needs to know about Core.
- **Outbound** (only if the host has no public IP / can't be reached, e.g. behind
  home NAT without port-forwarding): Periphery dials out to Core instead. See
  [Outbound Mode](#outbound-mode-no-public-ip--behind-nat) below instead of the steps
  here.

## 1. Create the Server in Komodo

In Komodo, create a Server matching the name you will use for Periphery, with its
`address` set to `http://<this-host's-public-ip-or-domain>:9120` and `enabled` on
(matches the `[[server]]` block in that host's `komodo-srv.toml`, this repo creates
these from `host/<name>/komodo-srv.toml`: see root [readme.md](../../readme.md)).

No onboarding key needed for inbound mode.

## 2. Install Periphery

Run on the target server, as root:

```bash
sudo su -
curl -sSL https://raw.githubusercontent.com/moghtech/komodo/main/scripts/setup-periphery.py \
  | python3 - --version v2.3.2
```

`--version` must match the Core image tag used in
[serv/komodo/docker-compose.yml](docker-compose.yml) (currently `2.3.2`), otherwise
Core refuses the connection with "Periphery version mismatch". No other flags: this
defaults to inbound mode, listening on port `8120`. Set it to `9120` to match this
repo's convention (every `komodo-srv.toml` address uses `:9120`):

```bash
sudo sed -i 's|^port = 8120|port = 9120|' /etc/komodo/periphery.config.toml
sudo systemctl restart periphery
```

Make sure that port is actually reachable from the internet: open it in the host's
firewall (`ufw allow 9120/tcp` if using `ufw`) and in the cloud provider's firewall /
security group if it has one, separate from the OS firewall.

## 3. Verify Periphery

Check the service:

```bash
systemctl status periphery
ss -tlnp | grep 9120
```

In Komodo, the Server will show a **pending public key** once Core's first connection
attempt reaches Periphery: approve it there (first time only, this is what pins the
connection against MITM). It then shows **Connected**.

## Outbound Mode (no public IP / behind NAT)

Only for a host Core can't dial into directly. Periphery dials Core instead, so Core's
own address needs to be reachable from this host instead of the other way around:
if Core itself is behind home NAT, this usually means forwarding Core's port on the
router and using the home network's public IP or a DynDNS hostname here, not a
LAN-only name.

In Komodo, create a Server matching the name you will use for Periphery, and create
an **Onboarding Key** for it (not needed in inbound mode).

> Do not commit the onboarding key to Git.

Run on the target server, as root:

```bash
sudo su -
curl -sSL https://raw.githubusercontent.com/moghtech/komodo/main/scripts/setup-periphery.py \
  | python3 - \
  --version v2.3.2 \
  --core-address "ws://YOUR-KOMODO-CORE:9120" \
  --connect-as "YOUR-SERVER-NAME" \
  --onboarding-key "YOUR-ONBOARDING-KEY"
```

`--version` must match the Core image tag in
[serv/komodo/docker-compose.yml](docker-compose.yml) (currently `2.3.2`).

Running the script again later (e.g. to fix a typo) does **not** overwrite an
existing config: edit `/etc/komodo/periphery.config.toml` directly instead
(`core_address`, `connect_as`, `onboarding_key` near the top), then:

```bash
sudo systemctl restart periphery
```

Check the logs for the connection attempt:

```bash
journalctl -u periphery -f
```

Periphery should appear as **Connected** in Komodo.

## Migrating from the bundled Core+Periphery

If this host's `docker-compose.yml` used to include `serv/komodo` (its own local
Core+Periphery) before switching to this native install, stop the old containers,
they're not managed by that compose file anymore:

```bash
cd /etc/srv-kube
docker compose -f host/<host-name>/docker-compose.yml down
```

## 4. Verify Docker Access

Periphery (running as root) needs Docker access, already covered by the post-install
step above if Periphery runs as the same user that ran it:

```bash
docker ps
```

## 5. Configuration

The main configuration file is:

```text
/etc/komodo/periphery.config.toml
```

The default Periphery root directory is:

```text
/etc/komodo
```

If using a custom Stack directory, configure:

```text
PERIPHERY_STACK_DIR=/etc/srv-kube
```

After changing the configuration:

```bash
sudo systemctl restart periphery
```

## Troubleshooting

If Periphery is not connecting:

```bash
journalctl -u periphery -f
```

**Inbound mode**: verify Periphery is actually listening, from Periphery's own host:

```bash
ss -tlnp | grep 9120
```

then from Core's host, verify the port is reachable (not refused, not timing out):

```bash
nc -vz THIS-HOST-ADDRESS 9120
```

A refused connection with nothing listening usually means
`/etc/komodo/periphery.config.toml` still has `core_address` set (forces outbound
mode, disabling the inbound listener): see step 2 above.

**Outbound mode**: verify Core's hostname resolves from Periphery's host:

```bash
getent hosts YOUR-KOMODO-CORE
```

and that Core's port is reachable from here:

```bash
nc -vz YOUR-KOMODO-CORE 9120
```