build:
	docker build . -t soma-image
run:
	docker run -i --rm -p 80:8000 -v $(shell pwd):/code --name soma -t soma-image
