# Defines a container that proxies ansible-playbook.
FROM alpine:3.8

ENV ANSIBLE_VERSION 2.6

ENV PACKAGES \
  bash \
  curl \
  openssh-client \
  sshpass \
  python \
  py-boto \
  py-jinja2 \
  py-paramiko \
  py-setuptools \
  py-pip \
  py-yaml

RUN echo "Adding Build dependencies..." && \
    apk --update add --virtual build-dependencies \
      openssl \
      python-dev && \
    \
    echo "Installing Python..." && \
    apk add --no-cache ${PACKAGES} && \
    pip install docker-py && \
    \
    echo "Installing Ansible..." && \
    pip install ansible==${ANSIBLE_VERSION} && \
    \
    echo "Cleaning up." && \
    apk del build-dependencies && \
    rm -rf /var/cache/apk/* && \
    \
    echo "Adding hosts for convenience..." && \
    mkdir -p /etc/ansible /ansible && \
    echo "[local]" >> /etc/ansible/hosts && \
    echo "localhost" >> /etc/ansible/hosts

ENV PATH /ansible/bin:$PATH
ENV PYTHONPATH /ansible/lib
ENV ANSIBLE_ROLES_PATH /ansible/playbooks/roles
ENV ANSIBLE_LIBRARY /ansible/library
ENV ANSIBLE_SSH_PIPELINING True
ENV ANSIBLE_HOST_KEY_CHECKING false
ENV ANSIBLE_RETRY_FILES_ENABLED false
ENV ANSIBLE_GATHERING smart

WORKDIR /ansible/playbooks

ENTRYPOINT ["ansible-playbook"]

