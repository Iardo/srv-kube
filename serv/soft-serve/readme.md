# Soft Serve

## First-run admin access

Set `SOFT_SERVE_INITIAL_ADMIN_KEYS` in this host's `.env-secrets.local` to your own SSH public key (`authorized_keys` format, space-separated for more than one) before the first deploy. That key becomes the server's admin, read only once on first boot of an empty data volume.

Clone/push over SSH on the published `SOFT_SERVE_SSH` port, e.g.:
```
git clone ssh://git@<host>:<SOFT_SERVE_SSH>/repo-name
```
