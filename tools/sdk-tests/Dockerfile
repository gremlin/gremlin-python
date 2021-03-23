FROM gremlin/gremlin-python-api:latest
LABEL maintainer="kyle@gremlin.com"

# Runtime arguments
ARG BUILD_DATE
ARG IMAGE_NAME
ARG APP_DIR=/opt/gremlin-python
ARG SRC_DIR=.

# Container Labels
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name=$IMAGE_NAME
LABEL org.label-schema.version=$BUILD_VERSION

WORKDIR ${APP_DIR}
COPY ${SRC_DIR} .
#RUN pip3 install urllib3
#RUN python3 setup.py install
ENTRYPOINT ["/bin/ash"]
CMD ["/bin/ash"]