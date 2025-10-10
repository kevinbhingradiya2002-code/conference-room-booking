#!/usr/bin/env bash
set -e

python3 -m pip install -r requirements.txt
python3 manage.py migrate --noinput
python3 manage.py setup_production
python3 manage.py collectstatic --noinput --clear
