#!/usr/bin/env bash
set -e

python3 -m pip install -r requirements.txt
python3 manage.py migrate --noinput
python3 manage.py check_database
python3 manage.py fix_auth
python3 manage.py collectstatic --noinput --clear
