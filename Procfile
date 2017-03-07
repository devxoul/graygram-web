web: python manage.py -c $CONFIG db upgrade; python manage.py -c $CONFIG db prepare_default_data; gunicorn 'graygram.app:create_app()' -b 0.0.0.0:$PORT --log-file=-
