#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Train the model
python train_model.py
