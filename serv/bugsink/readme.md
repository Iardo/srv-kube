# Bugsink: First Login

`BUGSINK_CREATE_SUPERUSER` only creates the initial admin account while the
user table is empty. Bugsink refuses to touch it again once any user
exists, so changing that value in `.env-secrets.local` after the first
deploy does nothing — these manual steps are the only way to actually
change the login afterward.

## 1. Log in with the committed dummy

```text
URL:      https://<this host's bugsink domain>
Email:    admin@example.com
Password: admin
```

(Or whatever's currently set in that host's `.env-secrets`/`.env-secrets.local`
under `BUGSINK_CREATE_SUPERUSER`, if it was never the default.)

## 2. Change the email

In the UI: account settings → change the email away from
`admin@example.com` to a real one you control.

## 3. Change the password

The UI has no "change password" field for this. On the VPS:

```bash
docker exec -it bugsink-web bugsink-manage changepassword <the-new-email-from-step-2>
```

Prompts twice for the new password (typing is hidden, that's normal).

Once this is done, the dummy login committed in `.env-secrets` (public,
anyone with this repo can read it) no longer works at all.

## Inviting more users

`SINGLE_USER=false` / `USER_REGISTRATION=CB_ADMINS` (see `.env`) are already
set, so this isn't single-user-only. There's no standalone "create user"
page though: go to **Teams** → pick (or create) a team → **Members** → add
someone by email. If that email has no account yet, this both creates and
invites it.
