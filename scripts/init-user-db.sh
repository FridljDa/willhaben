#!/bin/bash
set -eux

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -a <<-EOSQL
    CREATE USER application_user WITH PASSWORD 'my_pw';
    CREATE DATABASE workshop WITH OWNER application_user;
EOSQL
