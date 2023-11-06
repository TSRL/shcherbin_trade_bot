#!/bin/bash
sleep 5 # waiting for database to be up, could be done properly with a management command, but that would increase complexity
python manage.py migrate --noinput &&
gunicorn --workers=1 --timeout=3000 --bind=0.0.0.0:8989 --name=trade_bot trade_bot.wsgi:application