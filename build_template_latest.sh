#!/bin/bash

# sudo apt-get install beep

printf '\a'

rm -rf syncbookerkivy-main

git clone https://github.com/xayam/syncbookerkivy.git

mv syncbookerkivy syncbookerkivy-main

cd ./syncbookerkivy-main

chmod +x config.sh

source config.sh

ftp_site=
username=
passwd=

export ANDROIDSDK="$HOME/Documents/SDK"
export ANDROIDNDK="$HOME/Documents/ndk"
export ANDROIDAPI="27"  # Target API version of your application
export NDKAPI="21"  # Minimum supported API version of your application
export ANDROIDNDKVER="r25c"  # Version of the NDK you installed

export TARGET_PLATFORM="armeabi-v7a"
export TARGET_PLATFORM1="$TARGET_PLATFORM"

p4a clean_all

python3 p4a.py

apk_file1="syncbooker-$TARGET_PLATFORM-debug-$APP_VERSION.apk"

printf '\a'

export TARGET_PLATFORM="x86_64"
export TARGET_PLATFORM2="$TARGET_PLATFORM"

p4a clean_all

python3 p4a.py

apk_file2="syncbooker-$TARGET_PLATFORM-debug-$APP_VERSION.apk"

ftp -n $ftp_site<<EOF
quote USER $username
quote PASS $passwd
binary
cd apks
put $apk_file1 $TARGET_PLATFORM1/$apk_file1
put $apk_file2 $TARGET_PLATFORM2/$apk_file2
put $apk_file1 ./syncbooker.apk
quit
EOF

echo ""
echo "http://apk.delphima.z8.ru/apks/$TARGET_PLATFORM2/$apk_file2"
echo ""

printf '\a'

read -p "Press ENTER for exit..."

