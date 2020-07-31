%global debug_package %{nil}

Summary: Utility scripts for managing Mellanox BlueField hardware
Name: mlxbf-bfscripts
Version: 3.0.0~beta1
URL: https://github.com/Mellanox/bfscripts
Release: 1%{?dist}
License: BSD

BuildArch: noarch

Source: %{name}-%{version}.tar.gz

BuildRequires: systemd
BuildRequires: python3-devel
BuildRequires: /usr/bin/pathfix.py

Requires: mlxbf-bootctl
# Note: mlxbf-bootimages is provided by mlxbf-aarch64-firmware on Fedora.
Requires: mlxbf-bootimages
Requires: bash
Requires: python
Requires: grub2-tools
Requires: dosfstools
Requires: e2fsprogs
Requires: efibootmgr
Requires: pciutils
Requires: util-linux
Requires: binutils

%description
Useful scripts for managing Mellanox BlueField hardware.

%prep
%setup -q
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" mlx-mkbfb

%build
exit 0

%install
%global installdir %{buildroot}%{_bindir}
%global man1dir %{buildroot}%{_mandir}/man1
%global man8dir %{buildroot}%{_mandir}/man8
mkdir -p %{installdir}
%{__install} -d %{man1dir}
%{__install} -d %{man8dir}

%{__install} bfbootmgr        %{installdir}
%{__install} man/bfbootmgr.8  %{man8dir}
%{__install} bfcfg            %{installdir}
%{__install} man/bfcfg.8      %{man8dir}
%{__install} bfcpu-freq       %{installdir}
%{__install} man/bfcpu-freq.8 %{man8dir}
%{__install} bfdracut         %{installdir}
%{__install} man/bfdracut.8   %{man8dir}
%{__install} bffamily         %{installdir}
%{__install} man/bffamily.8   %{man8dir}
%{__install} bfinst           %{installdir}
%{__install} man/bfinst.8     %{man8dir}
%{__install} bfpxe            %{installdir}
%{__install} man/bfpxe.8      %{man8dir}
%{__install} bfrec            %{installdir}
%{__install} man/bfrec.8      %{man8dir}
%{__install} bfsbkeys         %{installdir}
%{__install} man/bfsbkeys.8   %{man8dir}
%{__install} bfvcheck         %{installdir}
%{__install} man/bfvcheck.8   %{man8dir}
%{__install} bfver            %{installdir}
%{__install} man/bfver.8      %{man8dir}
%{__install} bfauxpwr         %{installdir}
%{__install} man/bfauxpwr.8   %{man8dir}

%{__install} mlx-mkbfb       %{installdir}
%{__install} man/mlx-mkbfb.1 %{man1dir}

mkdir -p %{buildroot}%{_unitdir}/
install bfvcheck.service %{buildroot}%{_unitdir}/

%post
systemctl enable bfvcheck.service
systemctl daemon-reload
systemctl start bfvcheck.service >/dev/null 2>&1

%preun
systemctl stop bfvcheck.service >/dev/null 2>&1
systemctl disable bfvcheck.service
systemctl daemon-reload

%files
%license LICENSE
/usr/bin/bf*
/usr/bin/mlx-mkbfb
%attr(644, root, root) %{_mandir}/man1/*
%attr(644, root, root) %{_mandir}/man8/*
%attr(644, root, root) %{_unitdir}/bfvcheck.service

%doc README.md

%changelog
* Wed Jul 1 2020 Spencer Lingard <spencer@nvidia.com> - 3.0.0~beta1-1
Initial packaging.
