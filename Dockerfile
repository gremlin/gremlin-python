FROM alpine:latest
LABEL maintainer="kyle@gremlin.com"

# Runtime arguments
ARG BUILD_DATE
ARG IMAGE_NAME
ARG AWS_IAMAUTH_DOWNLOAD="https://amazon-eks.s3-us-west-2.amazonaws.com/1.14.6/2019-08-22/bin/linux/amd64/aws-iam-authenticator"
ARG GREMLIN_PYTHON_REPO="https://github.com/gremlin/gremlin-python.git"

# Container Labels
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name=$IMAGE_NAME
LABEL org.label-schema.version=$BUILD_VERSION

RUN apk add --no-cache --update \
		ca-certificates git bash openssh go tar gzip python3 openssl curl make

RUN python3 -m ensurepip  && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN pip --no-cache-dir install --upgrade awscli boto3

RUN curl -s -L $AWS_IAMAUTH_DOWNLOAD -o /usr/local/bin/aws-iam-authenticator && chmod 755 /usr/local/bin/aws-iam-authenticator

RUN mkdir -p /opt/gremlin-python

WORKDIR /opt/gremlin-python

# RUN git clone $GREMLIN_PYTHON_REPO .
COPY . .

# uncomment to install the package container wide
# RUN python3 setup.py install

ENTRYPOINT ["/bin/ash"]
CMD ["/bin/ash"]