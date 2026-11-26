# Dagu

DAG/cron job scheduler, YAML workflow files, no database. Not CI/CD, see `serv/woodpecker` for that. Dagu runs arbitrary scheduled or on-demand jobs, including SSH steps against other hosts, woodpecker only runs pipelines triggered by git events.

## DAGs

Put workflow YAML files under `data/dags/` (mounted at `/var/lib/dagu/dags`), they're picked up automatically. Dagu doesn't ship any example DAGs here, write your own.

## Running jobs over SSH

Dagu's `ssh` executor needs a private key reachable inside the container. Drop one at `data/ssh/id_ed25519` (and `data/ssh/known_hosts` with each target VPS's host key already trusted), it's mounted read-only at `/home/dagu/.ssh`. Both paths already match this repo's gitignore for `serv/**/data/*`, nothing here gets committed.

## Login

Basic auth, username `admin`, password is `DAGU_ADMIN_PASSWORD` from this host's secrets.
