# NOTE: Once the container is running create your first admin user:
# https://github.com/passbolt/passbolt_docker?tab=readme-ov-file#start-passbolt-instance

docker exec -i -u root passbolt-web su -s /bin/bash www-data -c "/usr/share/php/passbolt/bin/cake passbolt register_user -u admin@admin.com -f admin -l admin -r admin"
