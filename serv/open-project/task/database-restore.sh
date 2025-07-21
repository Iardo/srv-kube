database=1751134974-pgdata.tar.gz

docker-compose stop open-project-web open-project-worker
docker exec -it open-project-database psql -U postgres -c 'drop database openproject;'
docker cp ./backups/$database open-project-database:/
docker exec -it open-project-database psql -U postgres \c openproject \i $database \q
# docker exec -it open-project-database rm $database
docker-compose start seeder
docker-compose start open-project-web open-project-worker
