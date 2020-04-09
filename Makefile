DOCKER_OWNER=gremlin
DOCKER_NAME=gremlin-python-api
DOCKER_IMAGE=$(DOCKER_OWNER)/$(DOCKER_NAME)

BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ')
ENV_VARS=.env

all: docker-build

install:
	python3 setup.py install

docker-build:
	docker build --no-cache=true \
	             --build-arg BUILD_DATE=$(BUILD_DATE) \
	             --build-arg IMAGE_NAME=$(DOCKER_IMAGE) \
	             -t $(DOCKER_IMAGE):latest \
	             .

docker-run:
	@if ! test -f $(ENV_VARS); then touch $(ENV_VARS); fi
	docker run --rm -v ~/.ssh/:/root/.ssh --mount type=bind,source="$(PWD)",target=/opt/gremlin-python \
	--env-file=$(ENV_VARS) --name $(DOCKER_NAME) --entrypoint "/bin/ash" $(DOCKER_IMAGE):latest

docker-run-interactive:
	@if ! test -f $(ENV_VARS); then touch $(ENV_VARS); fi
	docker run -it --rm -v ~/.ssh/:/root/.ssh --mount type=bind,source="$(PWD)",target=/opt/gremlin-python \
	--env-file=$(ENV_VARS) --name $(DOCKER_NAME) --entrypoint "/bin/ash" $(DOCKER_IMAGE):latest
