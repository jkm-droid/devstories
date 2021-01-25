release: python manage.py migrate
web: daphne devstories.asgi:application --port $PORT --bind 0.0.0.0
worker: python manage.py runworker --settings=devstories.settings -v2