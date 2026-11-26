# Scrypted

Serves its own UI over HTTPS (self-signed) directly on `SCRYPTED_WEB_HTTP`,
visit `https://<host>:<port>/` (not `http://`) even though the port var is named `_HTTP` (it just follows this repo's normal single-role naming).

Runs with `network_mode: host` on purpose, see the comment in `docker-compose.yml` — required for HomeKit/mDNS device discovery to work.
