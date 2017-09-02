FROM debian:stretch

###############################################################################
# Allow running without root

RUN apt-get update
RUN apt-get install -y curl python3-pip
RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture)" && \
    curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture).asc" && \
    gpg --verify /usr/local/bin/gosu.asc && \
    rm /usr/local/bin/gosu.asc && \
    chmod +x /usr/local/bin/gosu

# install Caddy
RUN curl -o caddy.tar.gz https://caddyserver.com/download/linux/amd64
RUN tar xf caddy.tar.gz caddy
RUN mv caddy /usr/local/bin/caddy
RUN rm caddy.tar.gz

ENV PYTHONUNBUFFERED 1

ENV SOMA_HOME /soma_home
RUN mkdir -p $SOMA_HOME /app/api_server
WORKDIR /app
# install requirements first, so unrelated changes
# don't require rerunning this part
ADD api_server/requirements.txt /app/api_server/
RUN apt-get install -y python3-cairocffi libpango1.0
RUN pip3 install -r api_server/requirements.txt
ADD api_server /app/api_server
ADD client/build /app/client

WORKDIR /app/api_server
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput

ADD docker/Caddyfile /app/

EXPOSE 2010
EXPOSE 2015

ADD docker/entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
