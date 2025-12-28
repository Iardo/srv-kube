#!/bin/bash

quiet() { "$@" > /dev/null 2>&1; }

fullpath=$(dirname "$0")

source $fullpath/../.env
rm -rf $fullpath/../data/assets/attachment/file/*

# https://stackoverflow.com/a/72665159
# https://github.com/opf/openproject/blob/dev/docs/installation-and-operations/installation/manual/README.md#finish-the-installation-of-openproject
cmd_del_project="\"\
::Projects::ScheduleDeletionService.new(user: User.admin.active.first, model: Project.find('your-scrum-project')).call;\
::Projects::ScheduleDeletionService.new(user: User.admin.active.first, model: Project.find('demo-project')).call;\
\""
echo "Removing: Database entries ..."
quiet docker exec -it open-project-web sh -c "./bin/rails runner $cmd_del_project"

# https://stackoverflow.com/a/5342503
# https://community.openproject.org/topics/4468
cmd_del_entries="\"\
TRUNCATE TABLE attachable_journals, attachment_journals, attachments;\
ALTER SEQUENCE attachments_id_seq RESTART WITH 1;\
ALTER SEQUENCE work_packages_id_seq RESTART WITH 1;\
\""
echo "Removing: Attachments ..."
quiet docker exec -it open-project-database sh -c "PGPASSWORD=$POSTGRESQL_PASS psql -h localhost -U $POSTGRESQL_USER -d $POSTGRESQL_NAME -c $cmd_del_entries"
