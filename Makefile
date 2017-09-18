DEVENV=devenv$(shell pwd | sed 's/\//-/g')
DEVENV_IMAGE=soma-image
ifeq ($(shell docker inspect --format="{{.State.Status}}" ${DEVENV} 2>&1),running)
	ENV_RUN=docker exec --user $(shell id -u ${USER}) ${DEVENV}
endif

build:
	docker build . -t ${DEVENV_IMAGE}
run:
	docker run --rm -i -v $(shell pwd):/usr/src/project \
		-e LOCAL_USER_ID=$(shell id -u ${USER}) \
		-p 2010:2010 \
		-p 2015:2015 \
		-v $(shell pwd)/api_server:/app/api_server \
		-v $(shell pwd)/client:/app/client \
		--name soma \
		-v $(shell pwd)/soma_home:/soma_home \
		-t ${DEVENV_IMAGE}
run-dev:
	docker run --rm -i -v $(shell pwd):/usr/src/project \
		-e LOCAL_USER_ID=$(shell id -u ${USER}) \
		-p 2010:2010 \
		-p 2015:2015 \
		-v $(shell pwd)/api_server:/app/api_server \
		-v $(shell pwd)/client:/app/client \
		-v $(shell pwd)/soma_home:/soma_home \
		--name soma \
		-t ${DEVENV_IMAGE} \
		devserver
migrate:
	${ENV_RUN} ./api_server/manage.py makemigrations
	${ENV_RUN} ./api_server/manage.py migrate

devenv:
	docker run -d -v $(shell pwd):/usr/src/project \
		-e LOCAL_USER_ID=$(shell id -u ${USER}) \
		-v $(shell pwd):/app \
		-v $(shell pwd)/soma_home:/soma_home \
		--restart=always \
		--name ${DEVENV} -t ${DEVENV_IMAGE} bash
devenv-destroy:
	docker rm -f ${DEVENV}
