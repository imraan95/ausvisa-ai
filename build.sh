#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install --upgrade pip
pip install wheel
pip install --no-cache-dir -r requirements.txt
