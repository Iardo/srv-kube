# Authentik

## First-run admin login

Set the default admin ("akadmin") user's password, only available for a
limited time after the stack's first boot:

```
https://<domain>/if/flow/initial-setup/
```

If that flow already expired, reset it from the server instead:

```
docker exec -it authentik-worker ak changepassword akadmin
```

Then log in normally at:

```
https://<domain>/if/flow/default-authentication-flow/
```
