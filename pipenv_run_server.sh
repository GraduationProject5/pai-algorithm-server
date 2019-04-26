#/bin/sh
pipenv run python manage.py runserver 0.0.0.0:14000
pipenv run celery -A pai_algorithm worker -l info