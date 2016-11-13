FROM python:latest

ENV PYTHONUNBUFFERED 1

RUN mkdir /soma_home /app
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["gunicorn"]
CMD ["soma.wsgi_docker:application", "--log-level=info", "--bind=0.0.0.0:8000"]
