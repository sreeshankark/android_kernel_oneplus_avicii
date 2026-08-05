import os
import sys
import subprocess
import string
import random

bashfile = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
bashfile = '/tmp/' + bashfile + '.sh'

f = open(bashfile, 'w')
s = """#!/bin/bash

# Build Machine details
cores=$(nproc --all)
os=$(awk '{print $1, $2, $3; exit}' /etc/issue)
time=$(TZ="Asia/Kolkata" date "+%a %b %d %r")

kernel_dir="${PWD}"
TC_DIR=$HOME/tc/
CLANG_DIR=$TC_DIR
objdir="${kernel_dir}/out"
kf="$kernel_dir/packaging"
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


# Colors
NC='\\033[0m'
RED='\\033[0;31m'
LRD='\\033[1;31m'
LGR='\\033[1;32m'

echo -e ${LGR} "NeverSettle Kernel Build Triggered"${NC}
echo "Kernel: $kernel_name | Machine: $os | Cores: $cores | Time: $time IST"

if [ ! -d "$TC_DIR" ]; then
    echo -e ${LGR} "🛠️ Downloading ZyC-Clang (22.0.0)..."${NC}
    mkdir -p $TC_DIR
    wget https://github.com/ZyCromerZ/Clang/releases/download/22.0.0git-20250920-release/Clang-22.0.0git-20250920.tar.gz
    tar -xvf Clang-22.0.0git-20250920.tar.gz -C $TC_DIR && rm -rf Clang-22.0.0git-20250920.tar.gz
fi

make_defconfig()
{
    START=$(date +"%s")
    echo -e ${LGR} "########### Generating Defconfig ############"${NC}
    make -s ARCH=arm64 O=out $CONFIG_FILE -j$cores
}

compile()
{
    echo -e ${LGR} "######### Compiling kernel #########"${NC}
    make ARCH=arm64 O=out -j$cores 2>&1 | tee error.log
    echo -e ${LGR} "🏗️ Building kernel modules..."${NC}
    make O=out ARCH=arm64 INSTALL_MOD_PATH=modules_install INSTALL_MOD_STRIP=1 modules_install
    echo -e ${LGR} "🏗️ Building dtbo.img..."${NC}
    python3 ${avbtool} add_hash_footer --image ${DTBOIMAGE} --partition_size 25165824 --partition_name dtbo
}

completion() {
  cd ${objdir}
  if [[ -f ${ZIMAGE} && -f ${DTBOIMAGE} ]]; then
    echo -e ${LGR} "⚙️ NeverSettle Kernel $version compiled successfully ✅"${NC}
    echo -e ${LGR} "📦 Creating flashable zip..."${NC}
    cd $kf
    mv -f $ZIMAGE $DTBOIMAGE $kf
    sed -i "s/version.string=/version.string=$version/g" anykernel.sh
    sed -i "s/date.string=/date.string=$build_date/g" anykernel.sh
    sed -i "s/kernel.version=/kernel.version=$kernel_version/g" anykernel.sh
    sed -i "s/ksu.version=/ksu.version=$ksu_version/g" anykernel.sh
    mkdir -p $kf/modules/kmu-nsk/system/vendor/lib/modules
    find $objdir/modules_install -type f -name "*.ko" -exec mv {} $kf/modules/kmu-nsk/system/vendor/lib/modules/ \;
    sed -i "s/name=/name=NeverSettle KMU (Kernel Modules Updater)/g" $kf/modules/kmu-nsk/module.prop
    sed -i "s/version=/version=$version/g" $kf/modules/kmu-nsk/module.prop
    sed -i "s/versionCode=/versionCode=$versioncode/g" $kf/modules/kmu-nsk/module.prop
    sed -i "s/description=/description=NeverSettle Kernel $version | Build date: $build_date/g" $kf/modules/kmu-nsk/module.prop
    zip -r $zip_name *
    mv $kf/$zip_name $HOME/$zip_name
    echo -e ${LGR} "📦 Flashable zip created at $HOME/$zip_name ✅"${NC}
    md5sum "$HOME/$zip_name" > $HOME/checksums.txt
    CHANGELOG_TEXT="${CHANGELOG:-* No Changelog provided}"
    echo -e "NeverSettle Kernel $version Changelog ($build_date)\n=========================================\n$CHANGELOG_TEXT" > $HOME/changelog.txt
    echo -e ${LGR} "📝 Generated changelog.txt and checksums.txt ✅"${NC}
    echo -e ${LGR} "🧑‍💼 Downloading KernelSU-Next manager..."${NC}
    curl -sL ${ksu_apk} > $HOME/${ksu_apk_name}
    END=$(date +"%s")
    DIFF=$(($END - $START))
    echo -e ${LGR} "Build took : $((DIFF / 60)) minute(s) and $((DIFF % 60)) second(s)"${NC}
    curl --upload-file $HOME/$zip_name https://free.keep.sh
    echo
    echo -e ${LGR} "############################################"${NC}
    echo -e ${LGR} "######### Compilation succeeded :) ##########"${NC}
    echo -e ${LGR} "############################################"${NC}
  else
    echo -e ${RED} "😭 Compilation failed ❌"${NC}
    echo -e ${RED} "############################################"${NC}
    echo -e ${RED} "##         Compilation failed :(          ##"${NC}
    echo -e ${RED} "############################################"${NC}
  fi
}

make_defconfig
if [ $? -eq 0 ]; then
  echo -e ${LGR} "📝 Defconfig generated successfully ✅"${NC}
  echo -e ${LGR} "🏗️ Building kernel..."${NC}
  compile
  completion
fi
cd ${kernel_dir}
"""
f.write(s)
f.close()
os.chmod(bashfile, 0o755)
bashcmd = bashfile
for arg in sys.argv[1:]:
    bashcmd += ' ' + arg
subprocess.call(bashcmd, shell=True)
