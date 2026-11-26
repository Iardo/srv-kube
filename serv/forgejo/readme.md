# Forgejo

`FORGEJO_SECRET_KEY` being set makes Forgejo skip the web install wizard
on first boot (`INSTALL_LOCK` is set automatically), but no admin user
exists yet, there is no sign-up form left to create one from.

## First-run setup

Run, on the host, after the stack is up:

```
docker exec -it forgejo-web forgejo admin user create --admin --username <user> --password <password> --email <email>
```
