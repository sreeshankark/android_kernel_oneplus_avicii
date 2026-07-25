import os
import sys
import subprocess
import string
import random

bashfile = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
bashfile = '/tmp/' + bashfile + '.sh'

f = open(bashfile, 'w')
s = """#!/bin/bash

# Telegram Config
TOKEN=$(/usr/bin/env python -c "import os; print(os.environ.get('TOKEN'))")
# (env vars are inherited directly by bash, no need to shell out to python for them)
if [[ "$BUILDTYPE" == "RELEASE" ]];
	then
		CHATID="$CHATID"
		MESSAGEID=0
elif [[ "$BUILDTYPE" == "TEST" ]];
	then
		CHATID="$CHATIDTEST"
		MESSAGEID=0
else
		exit 0;
fi
CHANGELOG=$(/usr/bin/env python -c "import os; print(os.environ.get('CHANGELOG'))")

BOT_MSG_URL="https://api.telegram.org/bot${TOKEN}/sendMessage"
BOT_BUILD_URL="https://api.telegram.org/bot${TOKEN}/sendDocument"
BOT_STICKER_URL="https://api.telegram.org/bot${TOKEN}/sendSticker"
BOT_EDIT_URL="https://api.telegram.org/bot${TOKEN}/editMessageText"

# Build Machine details
cores=$(nproc --all)
os=$(awk '{print $1, $2, $3; exit}' /etc/issue)
time=$(TZ="Asia/Kolkata" date "+%a %b %d %r")

# send msgs to tg and track the ID
tg_post_msg() 
{
  response=$(curl -s -X POST "$BOT_MSG_URL" -d chat_id="$CHATID" -d message_thread_id="$MESSAGEID" -d "disable_web_page_preview=true" -d "parse_mode=html" -d text="$1")
  
  LAST_MSG_ID=$(echo "$response" | jq '.result.message_id')
}

# edit the last message sent by this script execution
tg_edit_msg() 
{
  if [ -z "$LAST_MSG_ID" ] || [ "$LAST_MSG_ID" = "null" ]; then
    echo "No valid LAST_MSG_ID found to edit."
    return 1
  fi
  
  curl -s -X POST "$BOT_EDIT_URL" -d chat_id="$CHATID" -d message_id="$LAST_MSG_ID" -d "disable_web_page_preview=true" -d "parse_mode=html" -d text="$1"
}

tg_edit_msg2()
{
   curl -s -X POST "$BOT_EDIT_URL" -d chat_id="$CHATID" -d message_id="$LAST_MSG_ID2" -d "disable_web_page_preview=true" -d "parse_mode=html" -d text="$1"
}

# send build to tg
tg_post_build()
{
	#Post MD5Checksum alongwith for easeness
	MD5CHECK=$(md5sum "$1" | cut -d' ' -f1)

	#Show the Checksum alongwith caption
	curl --progress-bar -F document=@"$1" "$BOT_BUILD_URL" -F message_thread_id="$MESSAGEID" -F chat_id="$CHATID" -F "disable_web_page_preview=true" -F "parse_mode=Markdown" -F caption="$2 | *MD5 Checksum : *\\`$MD5CHECK\\`"
}

# send a nice sticker ro act as a sperator between builds
tg_post_sticker() {
  curl -s -X POST "$BOT_STICKER_URL" -d chat_id="$CHATID" -d message_thread_id="$MESSAGEID" -d sticker="CAACAgUAAxkBAAEKCfxk3IWJbpyf9AJVzCr7WqNariv-YgACfwoAAiV14VZRQDfFXOn16DAE"
}

kernel_dir="${PWD}"
TC_DIR=$HOME/tc/
CLANG_DIR=$TC_DIR
objdir="${kernel_dir}/out"
kf="$kernel_dir/packaging/kf"
kmu="$kernel_dir/packaging/kmu"
builddir="${kernel_dir}/build"
avbtool=${kernel_dir}/scripts/avb/avbtool.py
ZIMAGE=$kernel_dir/out/arch/arm64/boot/Image.gz-dtb
DTBOIMAGE=$kernel_dir/out/arch/arm64/boot/dtbo.img
version="v4.4"
versioncode="4400"
kernel_version="4.19.325-cip133-st17"
ksu_version="v3.3.0"
ksu_version_code="33214"
build_date="$(date +"%d-%m-%Y")"
kernel_name="NeverSettle-Kernel-$version-avicii"
ksu_apk_name="KernelSU_Next_${ksu_version}_${ksu_version_code}-release.apk"
ksu_apk="https://github.com/KernelSU-Next/KernelSU-Next/releases/download/${ksu_version}/KernelSU_Next_${ksu_version}_${ksu_version_code}-release.apk"
zip_name="$kernel_name-$(date +"%d%m%Y-%H%M").zip"
zip_name_module="KMU_$kernel_name-$(date +"%d%m%Y-%H%M").zip"
sed -i "s/-NeverSettle-Kernel/-NeverSettle-Kernel-v4.4/g" arch/arm64/configs/avicii_defconfig
sed -i 's/CONFIG_LOCALVERSION_AUTO=y/# CONFIG_LOCALVERSION_AUTO is not set/g' arch/arm64/configs/avicii_defconfig

export ARCH=arm64
export SUBARCH=arm64
export CONFIG_FILE="avicii_defconfig avicii_ext.config"
export BRAND_SHOW_FLAG=oneplus
export CCACHE=$(command -v ccache)
export PATH="$CLANG_DIR/bin:$PATH"
export CC="ccache clang"
export CLANG_TRIPLE="aarch64-linux-gnu-"
export CROSS_COMPILE="aarch64-linux-gnu-"
export CROSS_COMPILE_ARM32="arm-linux-gnueabi-"
export LLVM=1
export LLVM_IAS=1
export DTC_EXT=/bin/dtc

#Start off by sending a trigger msg
tg_post_msg "/lock all"
sleep 1s
tg_post_sticker
tg_post_msg "<b>NeverSettle Kernel Build Triggered</b>%0A<b>============================</b>%0A<b>Kernel : </b><code>$kernel_name</code>%0A<b>Machine : </b><code>$os</code>%0A<b>Cores : </b><code>$cores</code>%0A<b>Time : </b><code>$time IST</code>"

# Colors
NC='\\033[0m'
RED='\\033[0;31m'
LRD='\\033[1;31m'
LGR='\\033[1;32m'

tg_post_msg "<code>🧬 Cloning NeverSettle Kernel source...</code>"
sleep 10s
tg_edit_msg "<code>🧬 Cloned NeverSettle Kernel source ✅</code>"
sleep 3s
tg_post_msg "<code>🛠️ Cloning ZyC-Clang (22.0.0)...</code>"
wget https://github.com/ZyCromerZ/Clang/releases/download/22.0.0git-20250920-release/Clang-22.0.0git-20250920.tar.gz
mkdir $TC_DIR && tar -xvf Clang-22.0.0git-20250920.tar.gz -C $TC_DIR && rm -rf Clang-22.0.0git-20250920.tar.gz
tg_edit_msg "<code>🛠️ Cloned ZyC-Clang (22.0.0) ✅</code>"

make_defconfig()
{
    START=$(date +"%s")
    echo -e ${LGR} "########### Generating Defconfig ############${NC}"
    make -s ARCH=arm64 O=out $CONFIG_FILE -j$cores
}
compile()
{
    echo -e ${LGR} "######### Compiling kernel #########${NC}"
    make ARCH=arm64 O=out -j$cores \\
    2>&1 | tee error.log
    tg_edit_msg "<code>🏗️ Built kernel ✅</code>"
    sleep 3s
    tg_edit_msg "<code>🏗️ Building kernel modules...</code>"
    make O=out ARCH=arm64 INSTALL_MOD_PATH=modules_install INSTALL_MOD_STRIP=1 modules_install
    sleep 15s
    tg_edit_msg "<code>🏗️ Built kernel modules ✅</code>"
    sleep 3s
    tg_edit_msg "<code>🏗️ Building dtbo.img...</code>"
    python3 ${avbtool} add_hash_footer --image ${DTBOIMAGE} --partition_size 25165824 --partition_name dtbo
    sleep 10s
    tg_edit_msg "<code>🏗️ Built dtbo.img ✅</code>"
	sleep 2s
}

completion() {
  cd ${objdir}
  if [[ -f ${ZIMAGE} && ${DTBOIMAGE} ]]; then
    tg_edit_msg "<code>⚙️ NeverSettle Kernel $version compiled ✅</code>"
    sleep 5s
    tg_edit_msg "<code>📦 Creating flashable zip...</code>"
    cd $kf
	mv -f $ZIMAGE $DTBOIMAGE $kf
    find . -name "*.zip" -type f
    find . -name "*.zip" -type f -delete
    sed -i "s/version.string=/version.string=$version/g" anykernel.sh
    sed -i "s/date.string=/date.string=$build_date/g" anykernel.sh
    sed -i "s/Based on Linux Kernel KERNEL_VERSION_STRING/Based on Linux Kernel $kernel_version/g" META-INF/com/google/android/update-binary
    sed -i "s/KernelSU-Next version: KSU_VERSION/KernelSU-Next version: $ksu_version/g" META-INF/com/google/android/update-binary
    zip -r $zip_name *
    mv $kf/$zip_name $HOME/$zip_name
    sleep 6s
    tg_edit_msg "<code>📦 Flashable zip created ✅</code>"
    sleep 2s
    tg_edit_msg "<code>📦 Creating kernel modules updater zip...</code>"
    cd $kmu
    mkdir -p $kmu/system/vendor/lib/modules
    find $objdir/modules_install -type f -name "*.ko" -exec mv {} $kmu/system/vendor/lib/modules/ \;
    sed -i "s/name=/name=Kernel modules updater for NeverSettle Kernel/g" $kmu/module.prop
    sed -i "s/version=/version=$version/g" $kmu/module.prop
    sed -i "s/versionCode=/versionCode=$versioncode/g" $kmu/module.prop
    sed -i "s/description=/description=NeverSettle Kernel $version | Build date: $build_date/g" $kmu/module.prop
    zip -r $zip_name_module *
    mv $kmu/$zip_name_module $HOME/$zip_name_module
    sleep 4s
    tg_edit_msg "<code>📦 Kernel modules updater zip created ✅</code>"
    sleep 2s
    tg_edit_msg "<code>🧑‍💼 Downloading KernelSU-Next manager...</code>"
    LAST_MSG_ID2=$LAST_MSG_ID
    curl -sL ${ksu_apk} > $HOME/${ksu_apk_name}
    sleep 6s
    tg_edit_msg2 "<code>🧑‍💼 KernelSU-Next manager downloaded ✅</code>"
    END=$(date +"%s")
    DIFF=$(($END - $START))
	sleep 2s
    tg_edit_msg2 "<code>📤 Initiate file upload...</code>"
    sleep 2s
    tg_edit_msg2 "<code>📤 File upload started ✅</code>"
    sleep 2s
    tg_edit_msg2 "<code>📤 [1/3] Uploading NeverSettle Kernel flashable zip...</code>"
    sleep 6s
    tg_post_build "$HOME/$zip_name" "Build took : $((DIFF / 60)) minute(s) and $((DIFF % 60)) second(s)"
    tg_edit_msg2 "<code>📤 [1/3] NeverSettle Kernel flashable zip uploaded ✅</code>"
    sleep 2s
    tg_edit_msg2 "<code>📤 [2/3] Uploading kernel modules updater zip</code>"
    sleep 4s
    tg_post_build "$HOME/$zip_name_module" "Kernel modules updater (KMU), install this module after flashing the kernel. Use Magisk/KernelSU-Next. Metamodule (eg: Mountify) needed!"
    tg_edit_msg2 "<code>📤 [2/3] Kernel modules updater zip uploaded ✅</code>"
    sleep 2s
    tg_edit_msg2 "<code>📝 Generating changelog...</code>"
    sleep 3s
    tg_post_msg "<b>Changelog ($(date +%d-%m-%Y))</b>%0A<code>$CHANGELOG</code>"
    tg_edit_msg2 "<code>📝 Changelog generated ✅</code>"
    sleep 2s
    tg_edit_msg2 "<code>📤 [3/3] Uploading KernelSU-Next manager apk...</code>"
    sleep 6s
    tg_post_build "$HOME/${ksu_apk_name}" "KernelSU-Next Manager for this build"
    tg_edit_msg2 "<code>📤 [3/3] KernelSU-Next manager apk uploaded ✅</code>"
    sleep 2s
    tg_edit_msg2 "<code>📤 Files uploaded ✅</code>"
    sleep 2s
    tg_edit_msg2 "<code>⚙️ NeverSettle Kernel $version compiled ✅</code>"
    tg_post_msg "<b>😊 Support the developer ❤️</b>%0A<b>UPI:</b> <code>sreeshankar10202-3@okaxis</code>%0A<b>BuyMeACoffee:</b> buymeacoffee.com/sreeshankark"
    sleep 1s
    tg_post_msg "/unlock all"
    curl --upload-file $HOME/$zip_name https://free.keep.sh
    echo
    echo -e ${LGR} "############################################"
    echo -e ${LGR} "######### Compilation suceeded :) ##########"
    echo -e ${LGR} "############################################${NC}"
  else
    tg_post_build "$kernel_dir/error.log" "$CHATID" "Debug Mode Logs"
    tg_post_msg "<code>😭 Compilation failed ❌</code>"
    echo -e ${RED} "############################################"
    echo -e ${RED} "##         Compilation failed :(          ##"
    echo -e ${RED} "############################################${NC}"
  fi
}
make_defconfig
if [ $? -eq 0 ]; then
  tg_post_msg "<code>📝 Generating Defconfig...</code>"
  sleep 3s
  tg_edit_msg "<code>📝 Defconfig generated ✅</code>"
  sleep 4s
  tg_edit_msg "<code>🏗️ Building kernel...</code>"
fi
compile
completion
cd ${kernel_dir}
"""
f.write(s)
f.close()
os.chmod(bashfile, 0o755)
bashcmd = bashfile
for arg in sys.argv[1:]:
    bashcmd += ' ' + arg
subprocess.call(bashcmd, shell=True)
