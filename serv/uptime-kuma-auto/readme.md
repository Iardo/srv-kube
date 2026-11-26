# AutoKuma

Companion automation agent for `serv/uptime-kuma`. Reads Docker labels (`kuma.<id>.<type>.<setting>: <value>`) off other containers on this host and creates/updates the matching monitors in Uptime Kuma automatically. It has no web UI or port of its own.

## Required setup

It needs a real Uptime Kuma admin account to talk to, there's nothing to generate. Fill these in on the host itself (`.env-secrets.local`), pointing at this host's own `serv/uptime-kuma` instance:
```
UPTIME_KUMA_AUTO_KUMA_URL=http://host.docker.internal:<UPTIME_KUMA_WEB_HTTP>
UPTIME_KUMA_AUTO_KUMA_USER=<an existing Uptime Kuma admin username>
UPTIME_KUMA_AUTO_KUMA_PASS=<that account's real password>
```

Labels usage: https://autokuma.bigboot.dev/dev/autokuma/usage/
