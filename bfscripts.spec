Summary: Install BlueField scripts
Name: bfscripts
Version: 2.1.0
Release: 10924
License: BSD
Group: base
Packager: Poky <poky@yoctoproject.org>
BuildRequires: systemd-systemctl-native
Requires: /bin/bash
Requires: /bin/sh
Requires: /usr/bin/env
Requires: bash
Requires: mlxbf-bootctl
Requires: mlxbf-bootimages
Requires(post): /bin/bash
Requires(post): /bin/sh
Requires(post): /usr/bin/env
Requires(post): bash
Requires(post): mlxbf-bootctl
Requires(post): mlxbf-bootimages
Requires(preun): /bin/bash
Requires(preun): /bin/sh
Requires(preun): /usr/bin/env
Requires(preun): bash
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
"/opt/mlnx"
"/opt/mellanox/scripts/bfver"
"/opt/mellanox/scripts/bfcpu-freq"
"/opt/mellanox/scripts/bfsbkeys"
"/opt/mellanox/scripts/mlx-mkbfb"
"/opt/mellanox/scripts/bfmisc"
"/opt/mellanox/scripts/bfinst"
"/opt/mellanox/scripts/build-bfb"
"/opt/mellanox/scripts/bfpart"
"/opt/mellanox/scripts/bfpxe"
"/opt/mellanox/scripts/bfvcheck"
"/opt/mellanox/scripts/bffamily"
"/opt/mellanox/scripts/bfdracut"
"/opt/mellanox/scripts/bfrec"
"/opt/mellanox/scripts/bfbootmgr"
"/lib/systemd/system/bfvcheck.service"

