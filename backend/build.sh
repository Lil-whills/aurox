#!/usr/bin/env bash

set -o errexit

# Ensure pip is up-to-date and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run migrations and collect static files
python manage.py migrate --noinput
python manage.py collectstatic --noinput
