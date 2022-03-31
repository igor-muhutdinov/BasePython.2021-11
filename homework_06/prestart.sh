#!/usr/bin/env sh

echo "applying migrations"

flask db upgrade

echo "migrations ok"