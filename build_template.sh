#!/bin/bash

export APP_VERSION="2.10"
export DEBUG=1

rm -rf syncbookerkivy-main

git clone https://github.com/xayam/syncbookerkivy.git

mv syncbookerkivy syncbookerkivy-main

cd ./syncbookerkivy-main

cp ./build_template ../new_build.sh

chmod +x ../new_build.sh

export ANDROIDSDK="$HOME/Documents/SDK"
export ANDROIDNDK="$HOME/Documents/ndk"
export ANDROIDAPI="27"  # Target API version of your application
export NDKAPI="21"  # Minimum supported API version of your application
export ANDROIDNDKVER="r25c"  # Version of the NDK you installed

export TARGET_ARCH="armeabi-v7a"

python3 p4a.py

export TARGET_ARCH="x86_64"

python3 p4a.py

apk_file=$(find . -maxdepth 1 -mindepth 1 -name '*.apk')

echo $apk_file

# ftp_site=
# username=
# passwd=

# ftp -n $ftp_site<<EOF
# quote USER $username
# quote PASS $passwd
# binary
# cd apks
# put ./syncbooker.apk
# quit
# EOF

read -p "Press ENTER for exit..."

