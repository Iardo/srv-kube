# dockerfiles

<blockquote>
DISCLAIMER ⚠

Do not use the content here in production environments.

This is a personal and ever changing repo.

Most of these recipes comes from different parts of the internet, I took the time to bundle the ones that worked for me and compile it here.

Some are work in progress and is not guaranteed for them to work properly.
</blockquote>


## How to use

1. Run `./main.py` without arguments to generate the configurations files
2. To install a service just uncomment the one that you want in the `service-list.yml` and run `./main.sh sync`

The `service-sync.yml` is auto-managed by the application to keep track of the installations, do not make changes to it manually.

## Disable service

Comment out the one that you want disabled in the `service-list.yml` and run `./main.sh sync`, if the services was previously installed then is going to be marked as disabled inside `service-sync.yml` but keeping their directory in intact.

## Clean-up services

If you want to get rid of disabled services directories inside `./installed` run `./main.py clean`.
