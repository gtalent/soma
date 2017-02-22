#!/bin/bash

# script from Deni Bertovic
# https://denibertovic.com/posts/handling-permissions-with-docker-volumes/

# Add local user
# Either use the LOCAL_USER_ID if passed in at runtime or
# fallback

if [[ $LOCAL_USER_ID == "" ]]; then
	USER_ID=-9001
fi

if [[ $USER_ID != -9001 ]]; then
	if [[ $(id -u user 2> /dev/null) != $USER_ID ]]; then
		useradd --shell /bin/bash -u $USER_ID -o -c "" -m user
		export HOME=/home/user
		echo "set -o vi" >> $HOME/.bashrc
	fi

	exec /usr/local/bin/gosu user "$@"
else
	exec "$@"
fi
