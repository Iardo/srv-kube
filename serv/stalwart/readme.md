# Stalwart

Mail server with a built-in web admin UI (SMTP+IMAP+JMAP). Outbound-only here, same posture as `serv/maddy`: no port 25 published, just relaying other services' mail out. See `serv/maddy/readme.md` for the lighter, no-UI option this repo also has.

## Before first deploy

DNS prerequisites, outside this repo: a static public IP, the server's hostname resolving to it, and control over the mail domain's DNS zone (SPF/DKIM/DMARC records get added after the wizard, step 3 below).

## First-run setup

There's no env-var shortcut for the first admin, it's done through Stalwart's own setup wizard:

1. The wizard listens on `STALWART_PANEL` (mapped to the container's 8080), bound to loopback only by design upstream (it has no auth yet at this point). Reach it through an SSH tunnel:
   ```
   ssh -L 8080:127.0.0.1:<STALWART_PANEL> <host>
   ```
   Then open `http://localhost:8080` and complete the wizard (server identity, storage backend, account directory, logging, DNS).
2. Restart the stack once the wizard finishes, it won't start normally until a restart picks up the config it wrote.
3. Sign in at `https://<domain>:<STALWART_WEB_HTTPS>/admin` with the credentials the wizard gave you, and publish the DNS records it shows for the mail domain.
4. Create a submission login from the WebUI (account management), used by other services in this repo to authenticate when sending mail through `stalwart:465`.

If you ever get locked out: set `STALWART_RECOVERY_ADMIN=admin:<password>` as a one-off env var on the container, restart, sign in and promote an account to administrator, then remove the variable and restart again.
Never leave it set.
