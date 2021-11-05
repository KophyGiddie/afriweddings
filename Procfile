release: python manage.py migrate
web: gunicorn afriweddings.wsgi
worker: celery -A  afriweddings worker -B -l info --without-gossip --without-mingle --without-heartbeat
