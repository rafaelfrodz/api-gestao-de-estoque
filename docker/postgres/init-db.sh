#!/bin/bash

set -e

# Create test database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE estoque_test_db;
    GRANT ALL PRIVILEGES ON DATABASE estoque_test_db TO postgres;
EOSQL