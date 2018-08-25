#! /usr/bin/env bash

# script from Deni Bertovic
# https://denibertovic.com/posts/handling-permissions-with-docker-volumes/

# Add local user
# Either use the LOCAL_USER_ID if passed in at runtime or
# fallback

if [[ $LOCAL_USER_ID != "" ]]; then
	if [[ $(id -u user 2> /dev/null) != $LOCAL_USER_ID ]]; then
		useradd --shell /bin/bash -u $LOCAL_USER_ID -o -c "" -m user
		export HOME=/home/user
		echo "set -o vi" >> $HOME/.bashrc
	fi

	cmd_prefix="/usr/local/bin/gosu user"
fi

$cmd_prefix mkdir -p "$SOMA_HOME/log"

if [[ "$@" == "" ]]; then
	gunicorn -D soma.wsgi:application --log-level=info --bind=0.0.0.0:8000 \
		--log-file="$SOMA_HOME/log/gunicorn.log"
	pushd /app/client > /dev/null
	$cmd_prefix node /app/client/server.js &
	popd > /dev/null
	$cmd_prefix caddy -conf=/app/Caddyfile
elif [[ "$@" == "devserver" ]]; then
	$cmd_prefix python3 ./manage.py runserver 0.0.0.0:8000 &
	pushd /app/client > /dev/null
	$cmd_prefix npm run start-dev &
	popd > /dev/null
	$cmd_prefix caddy -conf=/app/Caddyfile
else
	$cmd_prefix "$@"
fi
