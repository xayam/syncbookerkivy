#!/bin/bash

printf '\a'

rm -rf $NAME_PROJECT

git clone "https://github.com/$NAME_GITHUB/$NAME_PROJECT.git"

cd $NAME_PROJECT

chmod +x config.sh

source config.sh

export TARGET_PLATFORM="armeabi-v7a"

p4a clean_all

python3 p4a.py

apk_file1="$NAME_APP-$TARGET_PLATFORM-debug-$APP_VERSION.apk"

ftp -n $FTP_SITE<<EOF
quote USER $FTP_USER
quote PASS $FTP_PASSWORD
mkdir "v$APP_VERSION"
cd "v$APP_VERSION"
binary
put $apk_file1 $apk_file1
quit
EOF

printf '\a'

export TARGET_PLATFORM="x86_64"

p4a clean_all

python3 p4a.py

apk_file2="$NAME_APP-$TARGET_PLATFORM-debug-$APP_VERSION.apk"

echo "v$APP_VERSION" > ../latest.txt

ftp -n $FTP_SITE<<EOF
quote USER $FTP_USER
quote PASS $FTP_PASSWORD
mkdir "v$APP_VERSION"
cd "v$APP_VERSION"
binary
put $apk_file2 $apk_file2
cd ../latest
put ../latest.txt latest.txt
quit
EOF

echo ""
echo "$HTTP_SERVER/latest"
echo ""

printf '\a'
