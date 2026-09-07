# AnyKernel3 Ramdisk Mod Script
# osm0sis @ xda-developers
# Advanced NS Kernel Flasher

## AnyKernel setup
# begin properties
properties() { '
version.string=
clang.version=
date.string=
ksu.version=
kernel.version=
susfs.version=
do.devicecheck=1
do.cleanup=1
do.cleanuponabort=0
device.name1=avicii
device.name2=Nord
device.name3=AC2001
device.name4=AC2003
supported.versions=14 - 17
supported.patchlevels=
'; } # end properties

# shell variables
block=/dev/block/bootdevice/by-name/boot;
is_slot_device=auto;
ramdisk_compression=auto;

## AnyKernel methods (DO NOT CHANGE)
# import patching functions/variables - see for reference
. tools/ak3-core.sh;

## AnyKernel install
dump_boot;

write_boot;
## end install

