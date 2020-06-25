#!/bin/sh

# This feature is supported only on OCP 3.0 cards

powerconf=/etc/acpi/events/powerconf
powercontrol=/etc/acpi/actions/powercontrol.sh
systemdconf=/etc/systemd/logind.conf

mkdir -p /etc/acpi/events
touch $powerconf
echo \
"event=button/power.*
action=$powercontrol
" > $powerconf

mkdir -p /etc/acpi/actions
touch $powercontrol
echo \
"#!/bin/sh

echo 441 > /sys/class/gpio/export
value=\$(cat /sys/class/gpio/gpio441/value)

echo \$value > /root/log

for i in {1..7}
do
        echo \$value > /sys/devices/system/cpu/cpu\$i/online
done

echo 441 > /sys/class/gpio/unexport
" > $powercontrol

chmod +x $powercontrol

systemctl restart acpid

echo \
"
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.
#
# Entries in this file show the compile time defaults.
# You can change settings by editing this file.
# Defaults can be restored by simply deleting this file.
#
# See logind.conf(5) for details.

[Login]
HandlePowerKey=ignore
" > $systemdconf

echo "Systemd config has been updated. Please reboot for it to take effect."
