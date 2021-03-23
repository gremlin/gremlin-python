DOCKER_OWNER=gremlin
DOCKER_NAME=gremlin-python-api-test
DOCKER_IMAGE=$(DOCKER_OWNER)/$(DOCKER_NAME)
BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ')
ENV_VARS=.env
IA_SRC_DIR=$(PWD)/../..
APP_SRC_DIR=python-sdk-root/
APP_DST_DIR=/opt/gremlin-python
TSV=$(shell date -u '+%Y%j.%H')

all: docker-build

docker-build:
	docker build --no-cache=true \
	             --build-arg BUILD_DATE=$(BUILD_DATE) \
	             --build-arg IMAGE_NAME=$(DOCKER_IMAGE) \
	             --build-arg APP_DIR=$(APP_DST_DIR) \
	             --build-arg SRC_DIR=$(APP_SRC_DIR) \
	             -t $(DOCKER_IMAGE):$(TSV) \
	             -t $(DOCKER_IMAGE):latest \
	             .

docker-run:
	@if ! test -f $(ENV_VARS); then touch $(ENV_VARS); fi
	docker run --rm -v ~/.ssh/:/root/.ssh --mount type=bind,source="$(PWD)",target=/opt/gremlin-python \
	--env-file=$(ENV_VARS) --name $(DOCKER_NAME) --entrypoint "/bin/ash" $(DOCKER_IMAGE):latest

docker-run-interactive:
	@if ! test -f $(ENV_VARS); then touch $(ENV_VARS); fi
	docker run -it --rm \
	-v $(IA_SRC_DIR):$(APP_DST_DIR) \
	--env-file=$(ENV_VARS) --name $(DOCKER_NAME) --entrypoint "/bin/ash" $(DOCKER_IMAGE):latest