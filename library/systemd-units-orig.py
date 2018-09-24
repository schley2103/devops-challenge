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

# The D-Bus bus.
bus = dbus.SystemBus()

# A proxy to the Manager interface.
proxy = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')

# The Manager interface.
manager_interface = dbus.Interface(proxy, 'org.freedesktop.systemd1.Manager')

# Fetch each unit, building a list of dictionaries of name and state as we go.
units = list()
try:
    for unit in manager_interface.ListUnits():
        """unit[6] is the path to the unit, used to locate it"""
        uproxy = bus.get_object('org.freedesktop.systemd1', unit[6])
        unit_interface = dbus.Interface(uproxy,
            'org.freedesktop.systemd1.Unit',)
        properties_interface = dbus.Interface(uproxy,
            'org.freedesktop.DBus.Properties')
        id = str(properties_interface.Get(unit_interface.dbus_interface, "Id"))
        state = str(properties_interface.Get(unit_interface.dbus_interface,
            "ActiveState"))
        dict = {"unit":id, "state":state}
        units.append(dict)
except dbus.exceptions.DBusException as error:
    error.get_dbus_name()
    error.get_dbus_message()

# Output as JSON, pretty printed.
print json.dumps(units, skipkeys=True, sort_keys=False, default=None, indent=4)
