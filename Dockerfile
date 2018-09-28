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
    echo "Upgrading pip..." && \
    pip install --upgrade pip && \
    echo "Installing Docker and boto3..." && \
    pip install docker-py && \
    pip install boto3 && \
    \
    echo "Installing Ansible..." && \
    pip install ansible==${ANSIBLE_VERSION} && \
    \
    echo "Cleaning up." && \
    apk del build-dependencies && \
    rm -rf /var/cache/apk/* && \
    \
    echo "Creating folders..." && \
    mkdir -p /etc/ansible /ansible

ENV ANSIBLE_SCP_IF_SSH=y
ENV PATH /ansible/bin:$PATH
ENV PYTHONPATH /ansible/lib
ENV ANSIBLE_ROLES_PATH /ansible/roles
ENV ANSIBLE_LIBRARY /ansible/library
ENV ANSIBLE_SSH_PIPELINING True
ENV ANSIBLE_HOST_KEY_CHECKING false
ENV ANSIBLE_RETRY_FILES_ENABLED false
ENV ANSIBLE_GATHERING smart
ENV ANSIBLE_KEEP_REMOTE_FILES 1

WORKDIR /ansible

ENTRYPOINT ["ansible-playbook", "-i", "/ansible/inventory/ec2.py"]
CMD ["ansible-playbook", "-i", "/ansible/inventory/ec2.py"]
