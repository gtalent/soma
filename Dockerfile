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

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "soma.wsgi:application", "--log-level=info", "--bind=0.0.0.0:8000"]
