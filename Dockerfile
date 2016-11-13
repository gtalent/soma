FROM python:latest

ENV PYTHONUNBUFFERED 1

RUN mkdir /soma_home
WORKDIR /soma_home
ADD . /soma_home/
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["gunicorn"]
CMD ["soma.wsgi_docker:application", "--log-level=info", "--bind=0.0.0.0:8000"]
