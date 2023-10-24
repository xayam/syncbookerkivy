#!/bin/bash

export CURR_DIR="{{{CURR_DIR}}}"
export HTTP_SERVER="{{{HTTP_SERVER}}}"
export FTP_SITE="{{{FTP_SITE}}}"
export FTP_USER="{{{FTP_USER}}}"
export FTP_PASSWORD="{{{FTP_PASSWORD}}}"
export COMPLETE_LOOP=20
export ANDROIDSDK="{{{ANDROIDSDK}}}"
export ANDROIDNDK="{{{ANDROIDNDK}}}"
export ANDROIDAPI="{{{ANDROIDAPI}}}"  # Target API version of your application
export NDKAPI="{{{NDKAPI}}}"  # Minimum supported API version of your application
export ANDROIDNDKVER="{{{ANDROIDNDKVER}}}"  # Version of the NDK you installed

cd $CURR_DIR

while true; do

wget  --quiet --output-document=latest_new.txt "$HTTP_SERVER/latest/latest.txt"

OLD_VERSION=$(<latest.txt)
NEW_VERSION=$(<latest_new.txt)

if cmp latest_new.txt latest.txt
then
    echo "Remote version $NEW_VERSION equal local version $OLD_VERSION"
else
    echo "Find new version $NEW_VERSION"
    ./build.sh
    rm $CURR_DIR/latest_new.txt
    for ((i=1;i<=$COMPLETE_LOOP;i++)); do
        mpg123 -q complete.mp3
    done
fi

sleep 10s

done

read -p "Press ENTER for exit..."
