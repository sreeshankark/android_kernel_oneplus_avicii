# AnyKernel3 Ramdisk Mod Script
# osm0sis @ xda-developers

## AnyKernel setup
# begin properties
properties() { '
kernel.string=NeverSettle Kernel
version.string=
date.string=
maintainer.string=Sreeshankar K
do.devicecheck=1
do.modules=0
do.systemless=0
do.cleanup=1
do.cleanuponabort=0
device.name1=avicii
device.name2=Nord
device.name3=OnePlusNord
device.name4=OnePlus Nord
device.name5=
supported.versions=13, 14
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

if mountpoint -q /data; then
  # Optimize F2FS extension list (@arter97)
  for list_path in $(find /sys/fs/f2fs* -name extension_list); do
    
    ui_print " "
    ui_print "- Optimizing F2FS extension list"
    echo "Updating extension list: $list_path"

    echo "Clearing extension list"

    hot_count="$(grep -n 'hot file extens' $list_path | cut -d':' -f1)"
    list_len="$(cat $list_path | wc -l)"
    cold_count="$((list_len - hot_count))"

    cold_list="$(head -n$((hot_count - 1)) $list_path | grep -v ':')"
    hot_list="$(tail -n$cold_count $list_path)"

    for ext in $cold_list; do
      [ ! -z $ext ] && echo "[c]!$ext" > $list_path
    done

    for ext in $hot_list; do
      [ ! -z $ext ] && echo "[h]!$ext" > $list_path
    done

    echo "Writing new extension list"

    for ext in $(cat $home/f2fs-cold.list | grep -v '#'); do
      [ ! -z $ext ] && echo "[c]$ext" > $list_path
    done

    for ext in $(cat $home/f2fs-hot.list); do
      [ ! -z $ext ] && echo "[h]$ext" > $list_path
    done
  done
fi


#patch fstab for mounting data partition
patch_fstab /vendor/etc/fstab.qcom /data f2fs options "fsync_mode=nobarrier" "fsync_mode=posix,atgc,background_gc=sync"

#patch fstab for system partion
patch_fstab /vendor/etc/fstab.qcom / ext4 options "barrier=1" "nobarrier,i_version"

write_boot;
## end install

