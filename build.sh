#!/usr/bin/env bash
# exit on error
set -o errexit

# Update system and install build dependencies
apt-get update
apt-get install -y build-essential python3-dev

# Install Python dependencies
python -m pip install --upgrade pip
python -m pip install wheel setuptools
python -m pip install --no-cache-dir -r requirements.txt
