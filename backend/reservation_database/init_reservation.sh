#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE ROLE reservation_service LOGIN SUPERUSER PASSWORD 'password';
	CREATE SCHEMA reservation_microservice;
EOSQL
