DOCKER_TAG=artw/jj:latest

.PHONY: docker-build docker-push

all: docker-build docker-push

docker-build:
	docker build . -t $(DOCKER_TAG)

docker-push:
	docker push $(DOCKER_TAG)
