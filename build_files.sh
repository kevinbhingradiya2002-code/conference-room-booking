#!/usr/bin/env bash
set -e

echo "Starting build process..."

echo "Installing dependencies..."
python3 -m pip install -r requirements.txt

echo "Running migrations..."
python3 manage.py migrate --noinput

echo "Setting up production data..."
python3 manage.py setup_production

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Build completed successfully!"
