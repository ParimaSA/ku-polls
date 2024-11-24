#!/bin/sh
# Apply migrations
python ./manage.py migrate

# Apply fixtures
python ./manage.py loaddata data/users.json
python ./manage.py loaddata data/polls-v4.json
python ./manage.py loaddata data/votes-v4.json

# Run the server
python ./manage.py runserver 0.0.0.0:8000