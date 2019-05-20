#!/bin/sh -e

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

TMP_DIR=$(mktemp -d)
CURRENT_BFB=$TMP_DIR/"current.bfb"

rm -rf "$TMP_DIR"
# Create a temporary folder for the generated files
mkdir "$TMP_DIR"

# Identify current primary boot partition
DEV_PATH=$(mlxbf-bootctl | grep "primary" | cut -d ' ' -f 2)

# Retrieve default.bfb from the eMMC
mlxbf-bootctl -r "$DEV_PATH" -b "$CURRENT_BFB"

# Find and print the ATF version of current bfb
echo BlueField ATF version: "$(strings "$CURRENT_BFB" | grep -m 1 "(\(release\|debug\))")"

# Find and print the UEFI of current bfb
echo BlueField UEFI version: "$(strings -e l "$CURRENT_BFB" | grep "BlueField" | cut -d':' -f 2)"

# Print boot parameters using mlx-mkbfb
SCRIPTS_DIR="/opt/mlnx/scripts"
if [ -d "$SCRIPTS_DIR" ]; then
	cd "$TMP_DIR"
	$SCRIPTS_DIR/mlx-mkbfb -x "$CURRENT_BFB"
	echo Boot args: "$(cat dump-boot-args-v0)"
	echo Boot desc: "$(cat dump-boot-desc-v0)"
	echo Boot path: "$(cat dump-boot-path-v0)"
	echo Boot ACPI: "$(cat dump-boot-acpi-v0)"
fi

# Print BlueField version number if Yocto version file is present
if [ -e "/etc/bluefield_version" ]; then
	echo BlueField Release Version: "$(cat /etc/bluefield_version)"
else
	echo No Yocto version file present
fi

# Remove temporary directory
rm -rf "$TMP_DIR"
