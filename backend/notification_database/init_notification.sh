#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE ROLE notification_service LOGIN SUPERUSER PASSWORD 'password';
    CREATE SCHEMA notification_microservice;
EOSQL
