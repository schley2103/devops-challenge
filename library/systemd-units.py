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
# The heart of this is a call to org.freedesktop.systemd1.Manager.ListUnits(),
# which returns an array of currently loaded units. Note that units may be
# known by multiple names at the same name, and hence there might be more unit
# names loaded than actual units behind them. The Id and ActiveState properties
# on each element of the returned array are of interest here.
#

from ansible.module_utils.basic import AnsibleModule
import dbus
#import json

# Mass transit.
bus = dbus.SystemBus()


def main():
    run_module()


def run_module():
    """No args this module, required for the AnsibleModule constructor"""
    module_args = dict(
        name=dict(type='str', required=False),
        new=dict(type='bool', required=False, default=False)
    )

    """Initialize the result as a dictionary."""
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    """AnsibleModule has exit_json."""
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result['original_message'] = module.params['name']

    """Walk units, building a list of {name,state} dictionaries as we go."""
    
    units = list()
    try:
        for unit in list_units():
            id = get_property(unit, "Id")
            state = get_property(unit, "ActiveState")
            units.append({"unit": str(id), "state": str(state)})
    except dbus.exceptions.DBusException as error:
        error.get_dbus_name()
        error.get_dbus_message()
    result['message'] = units

    """Return JSON with the unit properties."""
# Try using a dict with Id as the index.
# Try converting the JSON to a str(), then returning it.
#    print json.dumps(units, sort_keys=False, indent=4, separators=(',', ': '))
    module.exit_json(**result)


def list_units():
    """A proxy to the Manager interface."""
    proxy = bus.get_object('org.freedesktop.systemd1',
                           '/org/freedesktop/systemd1')

    """ The Manager interface."""
    manager_interface = dbus.Interface(proxy,
                                       'org.freedesktop.systemd1.Manager')

    try:
        return manager_interface.ListUnits()
    except dbus.exceptions.DBusException as error:
        error.get_dbus_name()
        error.get_dbus_message()


def get_property(unit, name):
    """Fetch the property for the given unit, name."""
    try:
        """unit[6] is the unit path, used to locate it."""
        unit_proxy = bus.get_object('org.freedesktop.systemd1', unit[6])
        unit_interface = dbus.Interface(unit_proxy,
                                        'org.freedesktop.systemd1.Unit',)
        properties_interface = dbus.Interface(unit_proxy,
                                              'org.freedesktop.DBus.Properties'
                                              )
        return properties_interface.Get(unit_interface.dbus_interface, name)
    except dbus.exceptions.DBusException as error:
        error.get_dbus_name()
        error.get_dbus_message()


if __name__ == '__main__':
    main()

