bfscripts
=========

A public collection of useful scripts to help manage the Mellanox BlueField
SoC.

Overview of each file:
- **bfacpievt** Config ACPI daemon to handle AUX power mode. ***(Not supported on BlueField-4.)***
- **bfbootmgr** Change boot options.
- **bfcfg** Processes a config file passed over the rshim device.
- **bfcpu-freq** Display Arm core frequency.
- **bfdracut** Create an initramfs. ***(Not supported on BlueField-4.)***
- **bffamily** Display the BlueField family for the particular board.
- **bfgrubcheck** Checks if default grub password needs to be changed.
- **bfhcafw** Utilities for managing ConnectX interfaces on BlueField. ***(Not supported on BlueField-4.)***
- **bfinst** Simple installation script for both the bootloader and a root file
  system. ***(Not supported on BlueField-4.)***
- **bfperf_pmc** Tool for collecting memory statistics. ***(Not supported on BlueField-4.)***
- **bfpxe** PXE boot helper script.
- **bfrec** Force update of the bootloader only. ***(Not supported on BlueField-4.)***
- **bfrshlog** Write message into the rshim logging buffer. ***(Not supported on BlueField-4.)***
- **bfsbdump** Dump secure boot status information.
- **bfsbkeys** Dump all public keys in ATF. ***(Not supported on BlueField-4.)***
- **bfsbverify** Read BFB file from file or device and verify RoTPK and CoT.
- **bftraining_results** Read DDR5 training parameters from ACPI.
- **bfver** Print ATF, UEFI and rootfs versions. ***(Not supported on BlueField-4.)***
- **bfvcheck** Check whether software versions installed match those in current release. ***(Not supported on BlueField-4.)***
- **bfvcheck.service** Companion service to bfvcheck, runs bfvcheck at boot time.
- **mlx-mkbfb** Builds and extracts BFB files.
- **bfup** Informs that linux is running via rshlog message and gpio pin
- **bfup.services** Companion service to bfup, runs bfup at boot time.
