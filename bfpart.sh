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

# Build partition on the eMMC.

set -e

usage ()
{
    echo "syntax: bfpart [-b MB]"
}

boot_size=350

while getopts ":b:" opt; do
    case $opt in
        b)
            boot_size=$OPTARG
            ;;
        \?)
            usage >&2
            exit 1
        ;;
    esac
done

start_reserved=2048    # sectors required for label before first partition
end_reserved=34        # sectors required after last partition

disk_size=$(fdisk -l /dev/mmcblk0 | grep "Disk /dev/mmcblk0:" | awk '{print $5}')
disk_size=$((disk_size / 1024 / 1024))
disk_start=$start_reserved
boot_start=$disk_start
boot_end=$((boot_size * 1024 * 1024 / 512 - 1))
boot_sectors=$((boot_end - boot_start + 1))

root_start=$((boot_end + 1))
disk_sectors=$((disk_size * 1024 * 1024 / 512))
root_end=$((disk_sectors - end_reserved - 1))
root_sectors=$((root_end - root_start + 1))
disk_end=$root_end

cat > /tmp/disk.sfdisk <<EOF
label: gpt
label-id: 35C59B93-2752-492B-A244-62D1BD611793
device: /dev/mmcblk0
unit: sectors
first-lba: $disk_start
last-lba: $disk_end

gpt.dat1 : start=$boot_start, size=$boot_sectors, type=C12A7328-F81F-11D2-BA4B-00A0C93EC93B, uuid=3DCADB7E-BCCC-4897-A766-3C070EDD7C25
gpt.dat2 : start=$root_start, size=$root_sectors, type=0FC63DAF-8483-4772-8E79-3D69D8477DE4, uuid=9E61E8B5-EC9C-4299-8A0B-1B42E3DBD4AC
EOF

dd if=/dev/zero of=/dev/mmcblk0 bs=512 count=1

sfdisk /dev/mmcblk0 < /tmp/disk.sfdisk
