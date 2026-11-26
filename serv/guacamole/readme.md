# Guacamole

## First-run setup

Before the first deploy, run once (idempotent, safe to re-run):

```
bash serv/guacamole/task/task-gen-directories.sh
bash serv/guacamole/task/task-init-db.sh
```

`task-init-db.sh` generates `init/initdb.sql` from the exact pinned image,
read by the database container on its first boot only (empty volume).

## First-run admin login

```
username: guacadmin
password: guacadmin
```

Change it immediately after logging in.
