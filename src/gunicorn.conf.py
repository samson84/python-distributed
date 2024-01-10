from os import getenv


bind=getenv('GUNICORN_HOST')
workers=1
wsgi_app="src.server:app"