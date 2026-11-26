# Astral

GitHub-stars organizer. Builds locally from source (see docker-compose.yml),
no official image exists upstream.

## Before first deploy

1. Create a GitHub OAuth app at https://github.com/settings/developers.
   Callback URL:
   - with a domain: `http://<domain>/auth/github/callback`
   - without one yet: `http://localhost:<ASTRAL_WEB_HTTP>/auth/github/callback`
2. On the host, fill in these 2 values in that host's `.env-secrets.local`
   (left empty on purpose, never committed):
   ```
   ASTRAL_GITHUB_CLIENT_ID=
   ASTRAL_GITHUB_CLIENT_SECRET=
   ```
