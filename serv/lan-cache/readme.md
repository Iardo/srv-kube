# LanCache

A transparent cache for game-download/update traffic on a LAN
(Steam, Blizzard, Origin, etc). Only useful if this host IS the LAN's DNS/gateway,
or every client's DNS is pointed at it manually.

Before deploying: set `LANCACHE_IP`/`DNS_BIND_IP` in this host's override
of `serv/lan-cache/.env` to this machine's real LAN IP (not loopback).
Then point client devices' DNS at this host.
