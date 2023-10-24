#!/bin/bash

read -p "Enter link to you github project [https://github.com/xayam/syncbookerkivy/blob/main]: " GITHUB
GITHUB=${GITHUB:-https://github.com/xayam/syncbookerkivy/blob/main}

read -p "Enter exists path for local installation [$HOME/PycharmProjects]:" CURR_DIR
CURR_DIR=${CURR_DIR:-$HOME/PycharmProjects}

cd $CURR_DIR

echo "Installing depends..."
sudo apt install mpg123
sudo apt-get install beep

wget  --quiet --output-document=demon.sh "$GITHUB/demon.sh"
sudo chmod +x demon.sh
wget  --quiet --output-document=build.sh "$GITHUB/build.sh"
sudo chmod +x build.sh
wget  --quiet --output-document=complete.mp3 "$GITHUB/complete.mp3"

echo "Testing complete.mp3..."
mpg123 -q complete.mp3

touch latest.txt
echo "\nOptions +Indexes\nIndexOptions NameWidth=*\nIndexOptions FancyIndexing\nIndexOrderDefault Descending Date\n" > .htaccess

echo "Setup options. This require only once."
read -p "Enter URL you http server in format 'http[s]://you.domain.zone': " HTTP_SERVER
read -p "Enter you ftp site for server '$HTTP_SERVER': " FTP_SITE
read -p "Enter ftp user for login on ftp site '$FTP_SITE': " FTP_USER
read -p "Enter ftp password for login on ftp site '$FTP_SITE': " FTP_PASSWORD
read -p "Enter path to Android SDK [$HOME/Documents/SDK]: " ANDROIDSDK
ANDROIDSDK=${ANDROIDSDK:-$HOME/Documents/SDK}
read -p "Enter path to Android NDK [$HOME/Documents/ndk]: " ANDROIDNDK
ANDROIDNDK=${ANDROIDNDK:-$HOME/Documents/ndk}
read -p "Enter target API version of your application [27]: " ANDROIDAPI
ANDROIDAPI=${ANDROIDAPI:-27}
read -p "Enter minimum supported API version of your application [21]: " NDKAPI
NDKAPI=${NDKAPI:-21}
read -p "Enter version of the NDK you installed [r25c]: " ANDROIDNDKVER
ANDROIDNDKVER=${ANDROIDNDKVER:-r25c}

cat demon.sh | sed -e "s/{{{HTTP_SERVER}}}/$HTTP_SERVER/" >> demon.sh
cat demon.sh | sed -e "s/{{{FTP_SITE}}}/$FTP_SITE/" >> demon.sh
cat demon.sh | sed -e "s/{{{FTP_USER}}}/$FTP_USER/" >> demon.sh
cat demon.sh | sed -e "s/{{{FTP_PASSWORD}}}/$FTP_PASSWORD/" >> demon.sh
cat demon.sh | sed -e "s/{{{ANDROIDSDK}}}/$ANDROIDSDK/" >> demon.sh
cat demon.sh | sed -e "s/{{{ANDROIDNDK}}}/$ANDROIDNDK/" >> demon.sh
cat demon.sh | sed -e "s/{{{ANDROIDAPI}}}/$ANDROIDAPI/" >> demon.sh
cat demon.sh | sed -e "s/{{{NDKAPI}}}/$NDKAPI/" >> demon.sh
cat demon.sh | sed -e "s/{{{ANDROIDNDKVER}}}/$ANDROIDNDKVER/" >> demon.sh
echo "Setup options is completed."

echo "Connecting to '$FTP_SITE'..."
ftp -n $FTP_SITE<<EOF
quote USER $FTP_USER
quote PASS $FTP_PASSWORD
mkdir "latest"
binary
put latest.txt latest/latest.txt
put .htaccess
quit
EOF

echo "Now demon.sh be waiting while run build.py on Windows OS with new version in file config.sh on yoy github..."
echo "Running demon.sh"
./demon.sh

read -p "Press ENTER for exit..."
