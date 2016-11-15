FROM python:latest

ENV PYTHONUNBUFFERED 1

ENV SOMA_HOME /soma_home
RUN mkdir $SOMA_HOME /app
WORKDIR /app
# install requirements first, so unrelated changes
# don't require rerunning this part
ADD requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["gunicorn"]
CMD ["soma.wsgi:application", "--log-level=info", "--bind=0.0.0.0:8000"]
