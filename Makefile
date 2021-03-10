DOCKER_OWNER=gremlin
DOCKER_NAME=gremlin-python-api
DOCKER_IMAGE=$(DOCKER_OWNER)/$(DOCKER_NAME)

BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ')
ENV_VARS=.env

all: docker-build

install:
	python3 setup.py install

package:
	python3 setup.py sdist bdist_wheel

test:
	python3 $(PWD)/tests/test_all.py

lint:
	python3 -m black $(PWD)/gremlinapi
	python3 -m black $(PWD)/tests

pypi-test: export TWINE_PASSWORD=$(PYPI_TEST)
pypi-test: package
	python3 -m twine upload --non-interactive --config-file ${HOME}/.pypirc --repository testpypi dist/*

pypi-prod: export TWINE_PASSWORD=$(PYPI_PROD)
pypi-prod: package
	python3 -m twine upload --non-interactive --config-file ${HOME}/.pypirc dist/*

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
