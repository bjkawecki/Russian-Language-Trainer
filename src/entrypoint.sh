#!/bin/bash

set -e

RUN_MANAGE_PY="python manage.py"

echo "Collecting static files..."
$RUN_MANAGE_PY collectstatic --no-input

echo "Running migrate..."
$RUN_MANAGE_PY migrate --no-input

echo "Checking for superuser..."
$RUN_MANAGE_PY makesuperuser

$RUN_MANAGE_PY make_announcements

echo "Server is ready:"

echo "$@"
exec "$@"
