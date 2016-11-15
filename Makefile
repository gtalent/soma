build:
	docker build . -t soma-image
run:
	docker run -i --rm -p 80:8000 -v $(shell pwd)/soma_home:/soma_home -v $(shell pwd):/app --name soma -t soma-image
