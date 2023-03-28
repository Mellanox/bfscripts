bfscripts
=========

A public collection of useful scripts to help manage the Mellanox BlueField
SoC.

Overview of each file:
- **bfacpievt** Config ACPI daemon to handle AUX power mode.
- **bfbootmgr** Change boot options.
- **bfcfg** Processes a config file passed over the rshim device.
- **bfcpu-freq** Display Arm core frequency.
- **bfdracut** Create an initramfs.
- **bffamily** Display the BlueField family for the particular board.
- **bfgrubcheck** Checks if default grub password needs to be changed.
- **bfhcafw** Utilities for managing ConnectX interfaces on BlueField.
- **bfinst** Simple installation script for both the bootloader and a root file
  system.
- **bfpxe** PXE boot helper script.
- **bfrec** Force update of the bootloader only.
- **bfrshlog** Write message into the rshim logging buffer.
- **bfsbdump** Dump secure boot status information.
- **bfsbkeys** Dump all public keys in ATF.
- **bfsbverify** Read BFB file from file or device and verify RoTPK and CoT.
- **bfver** Print ATF, UEFI and rootfs versions.
- **bfvcheck** Check whether software versions installed match those in current release.
- **bfvcheck.service** Companion service to bfvcheck, runs bfvcheck at boot time.
- **mlx-mkbfb** Builds and extracts BFB files.
- **bfup** Informs that linux is running via rshlog message and gpio pin
