# Komodo Periphery — Installation

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

Verify Docker:

```bash
docker ps
```

## 1. Create the Server in Komodo

In Komodo, create a Server matching the name you will use for Periphery.

Example:

```text
iardo-iardodev
```

Create an **Onboarding Key** for the server.

> Do not commit the onboarding key to Git.

## 2. Install Periphery

Run on the target server:

```bash
sudo su -
```

Then:

```bash
curl -sSL https://raw.githubusercontent.com/moghtech/komodo/main/scripts/setup-periphery.py \
  | python3 - \
  --core-address "ws://YOUR-KOMODO-CORE:9120" \
  --connect-as "YOUR-SERVER-NAME" \
  --onboarding-key "YOUR-ONBOARDING-KEY"
```

Example:

```bash
curl -sSL https://raw.githubusercontent.com/moghtech/komodo/main/scripts/setup-periphery.py \
  | python3 - \
  --core-address "ws://komodo.home.example:9120" \
  --connect-as "iardo-iardodev" \
  --onboarding-key "O_xxxxxxxxx"
```

## 3. Verify Periphery

Check the service:

```bash
systemctl status periphery
```

Check the logs:

```bash
journalctl -u periphery -f
```

Periphery should appear as **Connected** in Komodo.

## 4. Verify Docker Access

Periphery needs Docker access:

```bash
docker ps
```

If Docker requires `sudo`, add the Periphery user to the Docker group:

```bash
sudo usermod -aG docker "$USER"
```

Log out and back in afterward.

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

Verify that the Core hostname resolves:

```bash
getent hosts YOUR-KOMODO-CORE
```

and that the Core port is reachable:

```bash
nc -vz YOUR-KOMODO-CORE 9120
```