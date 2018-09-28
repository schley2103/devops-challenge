#!/usr/bin/python

#
# Returns a list of systemd units and their current state.
#
# The returned data structure is a list of dictionaries each containing two
# keys representing the name of the unit and the current state. For example:
# [
#     {
#         "unit": "docker.socket",
#         "state": "enabled"
#     },
#     {
#         "unit": "docker.service",
#         "state": "enabled"
#     }
# ]
#

from ansible.module_utils.basic import AnsibleModule
import subprocess

def run_module():

    """A "command" argument is required"""
    module_args = dict(
        command = dict(type='str', required=True)
    )

    """Initialize the result as a dictionary."""
    result = dict(changed=False, message='')

    """AnsibleModule handles args and has exit_json()"""
    module = AnsibleModule(module_args, supports_check_mode=True)

    """If invoked in check mode, just return the current state with no mods"""
    if module.check_mode:
        return result

    """Traverse units, build a list of {name, state} dicts as we go."""
    units = list()
    cmd = ['systemctl', 'list-units', '--no-legend']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for line in iter(p.stdout.readline, ''):
        fields = line.strip().split()
        units.append({"unit": fields[0], "state": fields[3]})

    """Return JSON with the unit properties."""
    result['message'] = units
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

