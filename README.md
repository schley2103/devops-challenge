# DevOps Challenge
A DevOps coding challenge

The goal of this exercise is to demonstrate how I think about and approach problems through code. The solution is be an example of my work and demonstrates community best practices for the tools and languages involved.

## Requirements

Create a containerized Ansible project that provisions a Linux VM running in Amazon Web Services. Once provisioned, the Ansible project should execute a custom Ansible module created for this exercise that returns a list of installed _systemd_ units and their current state.

The returned data structure should be a list of dictionaries each containing two keys representing the name of the unit file and the current state. For example:

[
    {
        "unit": "docker.socket",
        "state": "enabled"
    },
    {
        "unit": "docker.service",
        "state": "enabled"
    }
]

## Other Requirements

- The solution should be delivered as a link to a public GitHub repository containing the project (you are here).
- The project should contain a working Dockerfile that builds the solution.
- The project should have three playbooks:
  - A playbook to provision the VM and any other resources needed
  - A playbook to connect to the VM and return the solution
  - A playbook to delete the VM and any other AWS resources created by the solution.
- The created Linux VM should reside in the default public VPC with a default, dynamically assigned public IP address.
- The playbook that connects to the VM and returns the solution should be runnable multiple times and produce the result without having to provision or deprovision the instance each time.
- The playbook that connects to the VM and returns the solution should continue to work without modification if the public IP address of the Linux VM changes.
- All playbooks should be idempotent and not return false _changed_ responses.
- Forcefully terminating the running Linux VM should automatically create a duplicate instance to replace it
- The custom Ansible module you create for this test must only use functionality present in the Python standard library on the running Linux VM.
- When designing the Docker image, follow best practices to reduce the image size to be as small as is reasonably possible.
- The container should take AWS credentials as its only input.
- The project should require no existing AWS resources other than an AWS account with valid credentials and permissions.
- Using roles and other Ansible best practices for project layout is highly encouraged.
- Throughout the project, pay particular attention to modularizing repetitive code with an eye toward producing the most readable and elegant solution possible.
