# Defines a container that proxies ansible-playbook.
FROM alpine:3.8

ENV ANSIBLE_VERSION 2.6

ENV PACKAGES python py-pip
ENV DEPENDENCIES py-boto py-paramiko

RUN echo "====> Adding Build dependencies..." && \
    apk --update add --virtual build-dependencies $DEPENDENCIES && \
    \
    echo "====> Installing Python..." && \
    apk add --no-cache $PACKAGES && \
    \
    echo "====> Upgrading pip..." && \
    pip install --upgrade pip  && \
    \
    echo "====> Installing ansible..." && \
    pip install ansible==${ANSIBLE_VERSION} && \
    pip install boto3 # Required by the ec2_group module && \
    \
    echo "====> Cleaning up..." && \
    rm -rf /var/cache/apk/* && \
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
