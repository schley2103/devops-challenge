#!/bin/bash
#
# Returns a list of tuples reflecting system units and their statuses.
#

systemctl list-units | tail -n +2 | head -n -7 | awk '{print $1,$3}'
