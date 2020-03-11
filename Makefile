DOCKER_OWNER=gremlin
DOCKER_NAME=gremlin-python-api
DOCKER_IMAGE=$(DOCKER_OWNER)/$(DOCKER_NAME)

MAJOR_VERSION_FILE=docker-build-major-version.txt
MINOR_VERSION_FILE=docker-build-minor-version.txt
BUILD_VERSION_FILE=docker-build-version.txt
BUILD_VERSION=$(shell cat $(MAJOR_VERSION_FILE)).$(shell cat $(MINOR_VERSION_FILE))
BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ')

KUBECTL_VERSION=$(shell curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)

ENV_VARS=env.vars

all: docker-build #docker-push

docker-build: $(MINOR_VERSION_FILE)
	BUILD_VERSION=$(shell cat $(MAJOR_VERSION_FILE)).$(shell cat $(MINOR_VERSION_FILE))
	docker build --no-cache=true \
	             --build-arg BUILD_DATE=$(BUILD_DATE) \
	             --build-arg IMAGE_NAME=$(DOCKER_IMAGE) \
	             --build-arg KUBECTL_VERSION=$(KUBECTL_VERSION) \
	             -t $(DOCKER_IMAGE):$(BUILD_VERSION) \
	             -t $(DOCKER_IMAGE):latest \
	             .
	echo ${BUILD_VERSION} > $(BUILD_VERSION_FILE)

docker-push:
	docker push $(DOCKER_IMAGE):$(BUILD_VERSION)
	docker push $(DOCKER_IMAGE):latest

docker-run:
	@if ! test -f $(ENV_VARS); then touch $(ENV_VARS); fi
	docker run --rm -v ~/.ssh/:/root/.ssh --mount type=bind,source="$(PWD)",target=/opt/gremlin-python \
	--env-file=env.vars --name $(DOCKER_NAME) --entrypoint "/bin/ash" $(DOCKER_IMAGE):latest

docker-run-interactive:
	@if ! test -f $(ENV_VARS); then touch $(ENV_VARS); fi
	docker run -it --rm -v ~/.ssh/:/root/.ssh --mount type=bind,source="$(PWD)",target=/opt/gremlin-python \
	--env-file=env.vars --name $(DOCKER_NAME) --entrypoint "/bin/ash" $(DOCKER_IMAGE):latest

$(MAJOR_VERSION_FILE):
	@if ! test -f $(MAJOR_VERSION_FILE); then echo 0 > $(MAJOR_VERSION_FILE); fi
	@echo $$(($$(shell cat $(MAJOR_VERSION_FILE)) + 1)) > $(MAJOR_VERSION_FILE)
	@echo $$(($$(shell cat $(MAJOR_VERSION_FILE)).$(shell cat $(MINOR_VERSION_FILE)))) > $(BUILD_VERSION_FILE)

$(MINOR_VERSION_FILE):
	@if ! test -f $(MINOR_VERSION_FILE); then echo 0 > $(MINOR_VERSION_FILE); fi
	@echo $$(($$(shell cat $(MINOR_VERSION_FILE)) + 1)) > $(MINOR_VERSION_FILE)
	@echo $$(($$(shell cat $(MAJOR_VERSION_FILE)).$(shell cat $(MINOR_VERSION_FILE)))) > $(BUILD_VERSION_FILE)
