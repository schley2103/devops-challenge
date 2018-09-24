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

import dbus
import json

# Mass transit.
bus = dbus.SystemBus()

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
        """unit[6] is the path to the unit, used to locate it."""
        unit_proxy = bus.get_object('org.freedesktop.systemd1', unit[6])
        unit_interface = dbus.Interface(unit_proxy,
            'org.freedesktop.systemd1.Unit',)
        properties_interface = dbus.Interface(unit_proxy,
            'org.freedesktop.DBus.Properties')
        return properties_interface.Get(unit_interface.dbus_interface, name)
    except dbus.exceptions.DBusException as error:
        error.get_dbus_name()
        error.get_dbus_message()

def main():
    units = list()
    """Walk units, building a list of {name,state} dictionaries as we go."""
    for unit in list_units():
        id = get_property(unit, "Id")
        state = get_property(unit, "ActiveState")
        dict = {"unit":str(id), "state":str(state)}
        units.append(dict)

    """Print a JSON of the units' properties."""
    print json.dumps(units, sort_keys=False, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    main()

