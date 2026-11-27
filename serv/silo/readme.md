# Silo

S3-compatible object storage (a maintained MinIO fork). Used here as Kaneo's file/image upload backend, see `serv/kaneo/readme.md` for the connection steps.

## Before first deploy

Set `SILO_CORS_ORIGIN` in this host's `.env` (Override section) to Kaneo's exact public origin, e.g. `https://kaneo.iardo.dev`. It must match scheme and port exactly, or browser uploads get rejected by CORS.

## Admin console

Bound to loopback only, unauthenticated until you sign in. Reach it through an SSH tunnel:
```
ssh -L 9001:127.0.0.1:<SILO_PANEL> <host>
```
Then open `http://localhost:9001` and sign in with `silo-admin` / the generated `SILO_ROOT_PASSWORD`.

## First-run setup

1. Create a private bucket (any name, e.g. `kaneo-uploads`). Leave anonymous access disabled.
2. Create a policy scoped to that bucket, allowing `s3:GetBucketLocation`, `s3:ListBucket`, `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject` on it.
3. Create a dedicated user (not the root admin) and attach that policy, then generate an access key for it.
4. Fill in `KANEO_S3_BUCKET`, `KANEO_S3_ACCESS_KEY_ID`, `KANEO_S3_SECRET_ACCESS_KEY` in Kaneo's host secrets with those values, see `serv/kaneo/readme.md`.
