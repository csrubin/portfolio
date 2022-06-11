#!/usr/bin/env bash

# Update environments
conda env export > environment.yml
pip list --format=freeze

# Git operations
read -p "Commit message": message
git add ./*
git commit -m "$message"

# Deploy to Heroku
git push heroku main
heroku open