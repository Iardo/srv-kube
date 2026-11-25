# Passbolt

Passbolt has no open registration.
The first (admin) user must be created by hand via CLI,
there is no sign-up form on the login page.

## First-run setup

1. On the host, fill in these 3 values in that host's `.env-secrets.local`
   (left empty on purpose, never committed):
   ```
   PASSBOLT_ADMIN_EMAIL=
   PASSBOLT_ADMIN_FIRSTNAME=
   PASSBOLT_ADMIN_LASTNAME=
   ```
2. Run, on that same host:
   ```
   bash serv/passbolt/task/task-create-admin-user.sh
   ```
3. The command prints a one-time setup URL. Open it to set your passphrase
   and install the browser extension, that finishes the account, not the
   regular login page.
