FROM python:latest

###############################################################################
# Allow running without root

RUN apt-get install -y curl
RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture)" && \
    curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture).asc" && \
    gpg --verify /usr/local/bin/gosu.asc && \
    rm /usr/local/bin/gosu.asc && \
    chmod +x /usr/local/bin/gosu
ADD docker/entrypoint.sh /

ENV PYTHONUNBUFFERED 1

ENV SOMA_HOME /soma_home
RUN mkdir -p $SOMA_HOME /app/api_server
WORKDIR /app
# install requirements first, so unrelated changes
# don't require rerunning this part
ADD api_server/requirements.txt /app/api_server/
RUN pip install -r api_server/requirements.txt
ADD api_server /app/api_server

WORKDIR /app/api_server
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "soma.wsgi:application", "--log-level=info", "--bind=0.0.0.0:8000"]
