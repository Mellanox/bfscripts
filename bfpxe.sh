#!/bin/sh

# Copyright (c) 2017, Mellanox Technologies
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.

TMP_MNT=

usage() {
  echo "syntax: bfpxe [-d <rootfs-device>]"
}

#
# Convert netmask to prefix length.
# For example, convert 255.255.255.0 to /24
#
netmask_to_prefix() {
   c=0 x=0$(printf '%o' $(echo "$1" | sed -r 's/[\.]+/ /g'))
   while [ $x -gt 0 ]; do
     c=$(($c+$((x%2))))
     x=$(($x/2))
   done
   echo /$c
}

#
# Create network interfaces.
# Create network configuration if root_device is specified.
#
create_net() {
  bfnet=""
  is_vlan=0
  eval "$1"

  if [ -n "$bfnet" ]; then
    ifname=$(echo $bfnet | cut -d: -f1)
    ifaddr=$(echo $bfnet | cut -d: -f2)
    ifnet=$(echo $bfnet | cut -d: -f3)

    # vlan check
    if [ ! -z $(echo "$ifname" | grep -E ".+\..+") ]; then
      vname=$(echo "$ifname" | cut -d. -f1)
      vid=$(echo "$ifname" | cut -d. -f2)
      if [ -n "$vname" -a -n "$vid" ]; then
        modprobe 8021q
        ip link add link "$vname" name "$ifname" type vlan id "$vid"
        ifconfig "$vname" 0.0.0.0 up
        is_vlan=1
        if [ -n "$TMP_MNT" ]; then
          mkdir -p "$TMP_MNT"/etc/systemd/network 2>/dev/null
          cat  >"$TMP_MNT"/etc/systemd/network/04-${ifname}.netdev <<EOF
[NetDev]
Name = $ifname
Kind = vlan

[VLAN]
Id = $vid
EOF
          cat  >"$TMP_MNT"/etc/systemd/network/05-${ifname}.network <<EOF
[Match]
Name = $ifname

[Network]
EOF
          echo "VLAN=${ifname}" >> "$TMP_MNT"/etc/systemd/network/05-${vname}.network
        fi
      fi
    fi

    # IP address
    if [ "$ifaddr" = "dhcp" ]; then
      ifconfig "$ifname" 0.0.0.0 up
      udhcpc -R -b -A 5 -T 3 -t 10 -i "$ifname"
      if [ -n "$TMP_MNT" ]; then
        sed -i '/Address =/d' "$TMP_MNT"/etc/systemd/network/05-${ifname}.network
        echo "DHCP = ipv4" >> "$TMP_MNT"/etc/systemd/network/05-${ifname}.network
      fi
    else
      ifconfig "$ifname" "$ifaddr" ${ifnet:+netmask $ifnet} up
      if [ -n "$TMP_MNT" ]; then
        sed -i '/DHCP =/d' "$TMP_MNT"/etc/systemd/network/05-${ifname}.network
        echo "Address = ${ifaddr}${ifnet:+$(netmask_to_prefix $ifnet)}" \
          >> "$TMP_MNT"/etc/systemd/network/05-${ifname}.network
      fi
    fi
  fi
}

# Parse the argument.
while getopts ":d:" opt; do
    case $opt in
        d)
            root_device=$OPTARG
            ;;
        \?)
            usage >&2
            exit 1
        ;;
    esac
done

# Mount the root device.
if [ -e "$root_device" ]; then
  TMP_MNT=/tmp/.bfmnt
  mkdir -p $TMP_MNT 2>/dev/null
  mount "$root_device" $TMP_MNT
  if [ ! -d $TMP_MNT/bin ]; then
    umount $TMP_MNT 2>/dev/null
    TMP_MNT=
  else
    # Delete the default static IP address if bfnet is configured.
    tmp=$(cat /proc/cmdline | grep bfnet)
    if [ -n "$tmp" ]; then
      sed -i '/Address =/d' $TMP_MNT/etc/systemd/network/05-tmfifo_net0.network
    fi
  fi
fi

# Parse kernel arguments.
for i in $(cat /proc/cmdline); do
  # Network config.
  if [ $(echo "$i" | cut -c1-6) = "bfnet=" ]; then
    create_net "$i"
  fi

  # Kickstart script.
  if [ $(echo "$i" | cut -c1-5) = "bfks=" ]; then
    eval "$i"
  fi
done

# Unmount the root device.
# It is provided for the kickstart script to install network cofiguration,
# so exit here once it's done.
if [ -n "$TMP_MNT" ]; then
  umount $TMP_MNT 2>/dev/null
  rmdir $TMP_MNT 2>/dev/null
  exit
fi

# Run the kickstart script.
if [ -n "$bfks" ]; then
  cd /tmp; wget "$bfks"
  bfks=$(basename "$bfks")
  if [ -f "$bfks" ]; then
    chmod +x "$bfks"
    ./"$bfks"
  fi
fi
