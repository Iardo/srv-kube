# Maddy

Lightweight outbound-only mail relay (SMTP Submission),
for this repo's other services to send transactional mail through.
No web admin UI: everything here is config file + CLI, by design.

## Before first deploy

1. Set `MADDY_HOSTNAME` (this server's mail hostname, e.g. `mx1.example.com`)
   and `MADDY_DOMAIN` (the domain you're sending mail as, e.g. `example.com`)
   in that host's `.env` (Override section).
2. Run `bash serv/maddy/task/task-gen-tls.sh` once,
   it generates a self-signed cert at `./data/tls/`
   (maddy refuses to start without one).
   Fine for internal use by other containers.
   For mail that needs to pass real deliverability checks,
   replace `./data/tls/fullchain.pem`/`privkey.pem` with a real certificate
   instead (e.g. certbot/acme.sh) before relying on this in production.
3. Outside this repo: set an SPF TXT record for `MADDY_DOMAIN`,
   and a PTR record for the host's IP matching `MADDY_HOSTNAME`.
   Both affect whether recipients accept your mail at all.

## First-run setup

1. Start the container once, then create a submission login
   (the username is an email address, used by other services to authenticate):
   ```
   docker exec -it maddy maddy creds create postmaster@<MADDY_DOMAIN>
   ```
2. Read the DKIM public key maddy generated on first start,
   and publish it as a DNS TXT record:
   ```
   docker exec maddy cat /data/dkim_keys/<MADDY_DOMAIN>_default.dns
   ```
   Add it as `default._domainkey.<MADDY_DOMAIN>`
   (the file already gives you the full `v=DKIM1; k=ed25519; p=...` value to paste).
3. Point other services at `maddy:587` for SMTP,
   using the credentials from step 1 (STARTTLS, not implicit TLS).
