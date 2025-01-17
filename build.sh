#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip first
python -m pip install --upgrade pip

# Install numpy first
python -m pip install numpy==1.18.5

# Then install other requirements
python -m pip install -r requirements.txt

# Train the model
python train_model.py
