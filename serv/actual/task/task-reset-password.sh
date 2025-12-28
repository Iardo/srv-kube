# NOTE: Resetting Actual login password
# https://actualbudget.org/docs/troubleshooting/reset_password
docker exec -it actual /bin/sh node /app/src/scripts/reset-password.js
