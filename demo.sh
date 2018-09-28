#!/bin/bash
#
# Driver script for the Modus demo.
#
# My setup:
#   I have ec2.py installed under inventory/.
#   A Dockerfile defines my ansible-playbook executable.
#   Required by ec2.py: EC2 API credentials in the environment.
#   Inventory manages EC2 machines based on the "modus" group and tag.
#

# Build a Docker image to run ansible-playbook.
docker build . -t ansible-playbook

# Verify that the image built.
docker run --rm -it -v $(pwd) ansible-playbook --version

# Provision a CentOS host on EC2.
# Note: my EC2 credentials are in my local environment. Set your own.
docker run\
 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID\
 -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\
 --rm -it -v $(pwd):/ansible ansible-playbook provision-ec2.yml

# Just checking...
inventory/ec2.py --list --profile default --refresh-cache | grep ec2_state.*running
if [ $? == 0 ]
then
  echo "Instance is running"
fi
ansible -i inventory/ec2.py -u centos all -m ping

# Run the systemd-units playbook.
docker run\
 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID\
 -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\
 --rm -it -v $(pwd):/ansible ansible-playbook systemd-units.yml

# Do it again to check idempotency.
docker run\
 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID\
 -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\
 --rm -it -v $(pwd):/ansible ansible-playbook systemd-units.yml

# Alternative systemctl, using only the Python standard library.
docker run\
 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID\
 -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\
 --rm -it -v $(pwd):/ansible ansible-playbook systemctl.yml

# Tear it all down.
docker run\
 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID\
 -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\
 --rm -it -v $(pwd):/ansible ansible-playbook terminate-ec2.yml

#
# Helpers:
#
# docker run --rm -it -v $(pwd):/ansible ansible-playbook wait.yml
# cid=$(docker ps | tail -1 | cut -f1 -d' ')
# docker exec -it $cid /bin/bash
#

#
# Footnote: what I have learned:
#
# How to manage dynamic inventory in Ansible.
# How to package ansible-playbook as a Docker image.
# Systemd and parts of the D-Bus API.
# A bunch of Python tricks.
# About Ansible roles.

