#!/bin/bash
echo "SELECT 'CREATE DATABASE paymentsdb' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'paymentsdb')\gexec" | psql
