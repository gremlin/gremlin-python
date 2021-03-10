FROM gremlin/gremlin-python-api:latest
LABEL maintainer="kyle@gremlin.com"

# Runtime arguments
ARG BUILD_DATE
ARG IMAGE_NAME
ARG APP_DIR=/opt/gremlin-python
ARG SRC_DIR=../..
ARG GREMLIN_PYTHON_REPO="https://github.com/gremlin/gremlin-python.git"

# Container Labels
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name=$IMAGE_NAME
LABEL org.label-schema.version=$BUILD_VERSION
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

# RUN git clone $GREMLIN_PYTHON_REPO .

COPY ${SRC_DIR} ./

# uncomment to install the package container wide
# RUN python3 setup.py install

ENTRYPOINT ["/bin/ash"]
CMD ["/bin/ash"]