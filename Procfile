web: python manage.py -c $CONFIG db upgrade; gunicorn 'graygram.app:create_app()' -b 0.0.0.0:$PORT --log-file=-
