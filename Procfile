release: python manage.py migrate
web: gunicorn afh_api.wsgi:application --bind 0.0.0.0:$PORT
