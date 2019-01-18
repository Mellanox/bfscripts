Summary: Install BlueField scripts
Name: bfscripts
Version: 1.1
Release: r0
License: BSD
Group: base
Packager: Poky <poky@yoctoproject.org>
BuildRequires: systemd-systemctl-native
Requires: /bin/sh
Requires: /usr/bin/env
Requires: mlxbf-bootctl
Requires: mlxbf-bootimages
Requires(post): /bin/sh
Requires(post): /usr/bin/env
Requires(post): mlxbf-bootctl
Requires(post): mlxbf-bootimages
Requires(preun): /bin/sh
Requires(preun): /usr/bin/env
Requires(preun): mlxbf-bootctl
Requires(preun): mlxbf-bootimages

%description
Install BlueField scripts.

%post
# bfscripts - postinst
#!/bin/sh
set -e
OPTS=""

if [ -n "$D" ]; then
    OPTS="--root=$D"
fi

if type systemctl >/dev/null 2>/dev/null; then
	if [ -z "$D" ]; then
		systemctl daemon-reload
	fi

	systemctl $OPTS enable bfvcheck.service

	if [ -z "$D" -a "enable" = "enable" ]; then
		systemctl --no-block restart bfvcheck.service
	fi
fi


%preun
# bfscripts - prerm
#!/bin/sh
if [ "$1" = "0" ] ; then
set -e
OPTS=""

if [ -n "$D" ]; then
    OPTS="--root=$D"
fi

if type systemctl >/dev/null 2>/dev/null; then
	if [ -z "$D" ]; then
		systemctl stop bfvcheck.service
	fi

	systemctl $OPTS disable bfvcheck.service
fi
fi

%files
%defattr(-,-,-,-)
%dir "/lib"
%dir "/opt"
%dir "/lib/systemd"
%dir "/lib/systemd/system"
"/lib/systemd/system/bfvcheck.service"
%dir "/opt/mellanox"
"/opt/mlnx"
%dir "/opt/mellanox/scripts"
"/opt/mellanox/scripts/bfinst"
"/opt/mellanox/scripts/bfrec"
"/opt/mellanox/scripts/bfdracut"
"/opt/mellanox/scripts/build-bfb"
"/opt/mellanox/scripts/bfpart"
"/opt/mellanox/scripts/bfbootmgr"
"/opt/mellanox/scripts/mlx-mkbfb"
"/opt/mellanox/scripts/bfvcheck"
"/opt/mellanox/scripts/bfpxe"
"/opt/mellanox/scripts/bffamily"
"/opt/mellanox/scripts/bfver"
"/opt/mellanox/scripts/bfcpu-freq"

