FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN pip install -r req.txt

CMD python manage.py migrate \
    && python manage.py shell -c "from users.models import MyUser; MyUser.objects.filter(username='admin').delete() or MyUser.objects.create_superuser('admin', 'admin@gmail.com', 'admin')" \
    && python manage.py runserver 0.0.0.0:8000
    