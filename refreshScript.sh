#!/bin/bash

# Change directory to the root of the project
cd /home/pi/projects/LetsHang

# Pull the latest code from the remote repository
git pull origin master

# Gracefully restart gunicorn
#ps ax | grep gunicorn | grep -Eo "^[^0-9]*[0-9]+" | grep -Eo "[0-9]+$" | xargs kill -HUP

# Start the WSGI server
# /home/pi/.local/bin/gunicorn -b 0.0.0.0:8000 things:app
