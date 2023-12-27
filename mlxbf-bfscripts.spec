%global debug_package %{nil}

Summary: Utility scripts for managing Mellanox BlueField hardware
Name: mlxbf-bfscripts
Version: 3.6.0
URL: https://github.com/Mellanox/bfscripts
Release: 1%{?dist}
License: BSD

BuildArch: noarch

Source: mlxbf-bfscripts-%{version}.tar.gz

BuildRequires: systemd-rpm-macros
BuildRequires: python3-devel
BuildRequires: /usr/bin/pathfix.py

Requires: mlxbf-bootctl
# Note: mlxbf-bootimages is provided by mlxbf-aarch64-firmware on Fedora.
Requires: mlxbf-bootimages
Requires: bash
Requires: python3
Requires: grub2-tools
Requires: dosfstools
Requires: e2fsprogs
Requires: efibootmgr
Requires: pciutils
Requires: util-linux
Requires: binutils
Requires: systemd
Requires: gzip

%description
Useful scripts for managing Mellanox BlueField hardware.

%prep
%setup
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" mlx-mkbfb

%build
exit 0

%install
%global installdir %{buildroot}%{_bindir}
%global man1dir %{buildroot}%{_mandir}/man1
%global man8dir %{buildroot}%{_mandir}/man8
mkdir -p %{installdir}
install -p -d %{man1dir}
install -p -d %{man8dir}

install -p bfbootmgr         %{installdir}
install -p man/bfbootmgr.8   %{man8dir}
install -p bfcfg             %{installdir}
install -p man/bfcfg.8       %{man8dir}
install -p bfcpu-freq        %{installdir}
install -p man/bfcpu-freq.8  %{man8dir}
install -p bfdracut          %{installdir}
install -p man/bfdracut.8    %{man8dir}
install -p bffamily          %{installdir}
install -p man/bffamily.8    %{man8dir}
install -p bfgrubcheck       %{installdir}
install -p man/bfgrubcheck.8 %{man8dir}
install -p bfinst            %{installdir}
install -p man/bfinst.8      %{man8dir}
install -p bfpxe             %{installdir}
install -p man/bfpxe.8       %{man8dir}
install -p bfrec             %{installdir}
install -p man/bfrec.8       %{man8dir}
install -p bfrshlog          %{installdir}
install -p man/bfrshlog.8    %{man8dir}
install -p bfsbdump          %{installdir}
install -p man/bfsbdump.8    %{man8dir}
install -p bfsbkeys          %{installdir}
install -p man/bfsbkeys.8    %{man8dir}
install -p bfsbverify        %{installdir}
install -p man/bfsbverify.8  %{man8dir}
install -p bfvcheck          %{installdir}
install -p man/bfvcheck.8    %{man8dir}
install -p bfver             %{installdir}
install -p man/bfver.8       %{man8dir}
install -p bfacpievt         %{installdir}
install -p man/bfacpievt.8   %{man8dir}
install -p bfgrubcheck       %{installdir}
install -p man/bfgrubcheck.8 %{man8dir}
install -p bfhcafw           %{installdir}
install -p man/bfhcafw.8     %{man8dir}
install -p bfup              %{installdir}
install -p man/bfup.8        %{man8dir}
install -p mlx-mkbfb       %{installdir}
install -p man/mlx-mkbfb.1 %{man1dir}
install -p bftraining_results %{installdir}
install -p man/bftraining_results.8 %{man8dir}

install -p -d %{buildroot}%{_unitdir}
install -p bfvcheck.service %{buildroot}%{_unitdir}/
install -p bfup.service %{buildroot}%{_unitdir}/

install -p -d %{buildroot}%{_presetdir}
install -p 80-bfvcheck.preset %{buildroot}%{_presetdir}/
install -p 80-bfup.preset %{buildroot}%{_presetdir}/

# Install tweak for fwupd on BlueField
%global fwupdquirkdir %{buildroot}%{_datadir}/fwupd/quirks.d
install -p -d %{fwupdquirkdir}
install -p mlx-uefi.quirk %{fwupdquirkdir}/

%post
%systemd_post bfvcheck.service
%systemd_post bfup.service

%preun
%systemd_preun bfvcheck.service
%systemd_preun bfup.service

%postun
%systemd_postun bfvcheck.service
%systemd_postun bfup.service

%files
%license LICENSE
%{_bindir}/bf*
%{_bindir}/mlx-mkbfb
%attr(644, root, root) %{_mandir}/man1/*
%attr(644, root, root) %{_mandir}/man8/*
%attr(644, root, root) %{_unitdir}/bfvcheck.service
%attr(644, root, root) %{_unitdir}/bfup.service
%attr(644, root, root) %{_presetdir}/80-bfvcheck.preset
%attr(644, root, root) %{_presetdir}/80-bfup.preset
%attr(644, root, root) %{_datadir}/fwupd/quirks.d/mlx-uefi.quirk

%doc README.md

%changelog
* Thu May 20 2021 Spencer Lingard <spencer@nvidia.com> - 3.6.0-1
- Update version number to 3.6.0-1

* Fri Jul 24 2020 Spencer Lingard <Spencer@nvidia.com> - 3.0.0~beta1-3
- Add -p to all install invocations
- Change __install macro to just install
- Add autogenerated comment to Source to tell how to obtain sources

* Tue Jul 21 2020 Spencer Lingard <spencer@nvidia.com> - 3.0.0~beta1-2
- Use systemd macros for unit setup
- Use preset file instead of enabling service manually
- Fix Requires/BuildRequires

* Wed Jul 1 2020 Spencer Lingard <spencer@nvidia.com> - 3.0.0~beta1-1
Initial packaging.
