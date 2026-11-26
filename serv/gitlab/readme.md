# GitLab

Heavy, all-in-one image (bundles its own nginx, Postgres, Redis, Gitaly,
Sidekiq, Puma). Official minimum is 4 CPU / 4GB RAM, 8GB+ recommended.
Check the host has real headroom before including this.

First boot takes several minutes (internal `gitlab-ctl reconfigure`).

## First-run admin login

`GITLAB_ROOT_PASSWORD` only sets the "root" user's password on first boot
(empty `/etc/gitlab` volume). Log in as `root` with that password at:

```
http://<domain>/users/sign_in
```

If it's already past first boot, reset it instead:

```
docker exec -it gitlab-web gitlab-rails runner "user = User.find_by(username: 'root'); user.password = 'newpassword'; user.password_confirmation = 'newpassword'; user.save!"
```
