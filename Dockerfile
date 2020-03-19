FROM alpine:latest
LABEL maintainer="kyle@gremlin.com"


# Runtime arguments
ARG BUILD_DATE
ARG IMAGE_NAME
ARG KUBECTL_VERSION="v1.16.1"
ARG KUBECTL_DOWNLOAD="https://storage.googleapis.com/kubernetes-release/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl"
ARG HELM_DOWNLOAD="https://raw.githubusercontent.com/helm/helm/master/scripts/get"
ARG EKSCTL_DOWNLOAD="https://github.com/weaveworks/eksctl/releases/download/latest_release/eksctl_Linux_amd64.tar.gz"
ARG AWS_IAMAUTH_DOWNLOAD="https://amazon-eks.s3-us-west-2.amazonaws.com/1.14.6/2019-08-22/bin/linux/amd64/aws-iam-authenticator"

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

RUN pip --no-cache-dir install --upgrade awscli bitly_api boto3 datadog jinja2 kubernetes==9.0.1

RUN curl $HELM_DOWNLOAD | bash

RUN curl --silent --location $EKSCTL_DOWNLOAD | tar xz -C /usr/local/bin && chmod 755 /usr/local/bin/eksctl

RUN curl -s -L $AWS_IAMAUTH_DOWNLOAD -o /usr/local/bin/aws-iam-authenticator && chmod 755 /usr/local/bin/aws-iam-authenticator

RUN echo $KUBECTL_DOWNLOAD
RUN curl -s -L $KUBECTL_DOWNLOAD -o /usr/bin/kubectl && chmod 755 /usr/bin/kubectl

RUN mkdir -p /opt/gremlin-python
#ADD src /opt/bootcamp
#
#RUN chmod 755 /opt/bootcamp/bootcamp.py

ENTRYPOINT ["python3", "/opt/bootcamp/bootcamp.py", "-x"]
CMD ["make build"]