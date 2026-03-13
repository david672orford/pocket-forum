DOCKER_IMAGE=pocket-forum
DOCKER_CONTAINER=$(shell ./docker-options --docker-container)
UID=$(shell ls -ldn instance | cut -d' ' -f3)

all: pull build restart

pull:
	git pull

build-no-cache: BUILD_ARGS=--no-cache
build-no-cache: build
build:
	test -d instance || mkdir instance
	docker build $(BUILD_ARGS) --build-arg uid=$(UID) --tag $(DOCKER_IMAGE) .

shell:
	docker exec -it $(DOCKER_CONTAINER) /bin/sh

start:
	docker run --detach --restart=always $(shell ./docker-options) $(DOCKER_IMAGE)

stop:
	docker stop $(DOCKER_CONTAINER)
	docker rm $(DOCKER_CONTAINER)

restart: stop start

logs:
	docker logs $(DOCKER_CONTAINER) 2>&1

tail:
	docker logs -f $(DOCKER_CONTAINER) 2>&1

