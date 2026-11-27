# Kaneo

Project management app (tasks/boards).

## File uploads (optional)

Needs `serv/silo` deployed on the same host, as Kaneo's S3-compatible storage backend. Without it, uploads just show "Upload not configured" in the UI, everything else still works.

Setup:
1. Add `serv/silo` to this host's include list.
2. Set `SILO_DOMAIN` and `SILO_CORS_ORIGIN` in this host's `.env` (Override section). `SILO_DOMAIN` must match Caddy's own auto-generated route for `serv/silo` (always `silo.<CADDY_DOMAIN>`, e.g. `silo.iardo.dev`), not a freely chosen name, Caddy has no way to serve a different one. `SILO_CORS_ORIGIN` must be this service's own public origin, e.g. `https://kaneo.iardo.dev`.
3. Deploy, then follow `serv/silo/readme.md`'s first-run steps (bucket, policy, dedicated access key).
4. Fill in `KANEO_S3_BUCKET`, `KANEO_S3_ACCESS_KEY_ID`, `KANEO_S3_SECRET_ACCESS_KEY` in this host's `.env-secrets.local` with the values from step 3, then redeploy Kaneo.
