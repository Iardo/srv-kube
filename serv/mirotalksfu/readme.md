# MiroTalk SFU

Video conferencing (WebRTC SFU). Before deploying,
set `SFU_ANNOUNCED_IP` in this host's override of `serv/mirotalksfu/.env`
to this machine's real public IP or domain.
WebRTC clients need it to negotiate media, it can't be left blank.

The 40000-40100 TCP/UDP range is the WebRTC media relay,
published as a fixed range on every host rather than through
the usual per-host port registry (a single port var wouldn't fit a 101-port range).
