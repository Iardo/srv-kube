# sist2

File indexer/search tool. It has no config to generate, just a one-time manual setup.

## Before first deploy

Replace `./data-host` in `docker-compose.yml` with the real host path you want indexed, mounted read-only. Add more directories as extra volumes the same way.

## First-run setup

1. Open the panel at `http://<host>:<SIST2_PANEL>`. Never expose this port publicly, it has no login of its own.
2. Create a new index job pointing at `/host`, or whichever mount path you used, with the SQLite search backend (no separate database needed).
3. Run the job. Once it finishes, sist2-admin starts the real search frontend on port 4090 (`SIST2_WEB_HTTP`), the one safe to put behind Caddy.
