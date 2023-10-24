#!/bin/bash

read -p "Enter exists path for local installation [$HOME/PycharmProjects]:" CURR_DIR
CURR_DIR=${CURR_DIR:-$HOME/PycharmProjects}

read -p "Enter you login on github [xayam]: " NAME_GITHUB
NAME_GITHUB=${NAME_GITHUB:-xayam}

read -p "Enter name you github project [syncbookerkivy]: " NAME_PROJECT
NAME_PROJECT=${NAME_PROJECT:-syncbookerkivy}
GITHUB="https://raw.githubusercontent.com/$NAME_GITHUB/$NAME_PROJECT/main"

read -p "Enter name you aplication [syncbooker]: " NAME_APP
NAME_APP=${NAME_APP:-syncbooker}

cd $CURR_DIR

echo "Installing depends..."
sudo apt install mpg123
sudo apt-get install beep

wget  --quiet --output-document=demon.sh "$GITHUB/demon.sh"
sudo chmod +x demon.sh
wget  --quiet --output-document=build.sh "$GITHUB/build.sh"
sudo chmod +x build.sh
wget  --quiet --output-document=complete.mp3 "$GITHUB/res/complete.mp3"

echo "Testing complete.mp3..."
mpg123 -q complete.mp3

touch latest.txt
echo "\nOptions +Indexes\nIndexOptions NameWidth=*\nIndexOptions FancyIndexing\nIndexOrderDefault Descending Date\n" > .htaccess

echo "Setup options. This require only once."
read -p "Enter URL you http server in format 'http://you.domain.zone': " HTTP_SERVER
read -p "Enter you ftp site for server '$HTTP_SERVER': " FTP_SITE
read -p "Enter ftp user for login on ftp site '$FTP_SITE': " FTP_USER
read -s -p "Enter ftp password for login on ftp site '$FTP_SITE': " FTP_PASSWORD
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

sed -i "s|_NAME_GITHUB_|$NAME_GITHUB|g" demon.sh
sed -i "s|_NAME_PROJECT_|$NAME_PROJECT|g" demon.sh
sed -i "s|_CURR_DIR_|$CURR_DIR|g" demon.sh
sed -i "s|_HTTP_SERVER_|$HTTP_SERVER|g" demon.sh
sed -i "s|_FTP_SITE_|$FTP_SITE|g" demon.sh
sed -i "s|_FTP_USER_|$FTP_USER|g" demon.sh
sed -i "s|_FTP_PASSWORD_|$FTP_PASSWORD|g" demon.sh
sed -i "s|_ANDROIDSDK_|$ANDROIDSDK|g" demon.sh
sed -i "s|_ANDROIDNDK_|$ANDROIDNDK|g" demon.sh
sed -i "s|_ANDROIDAPI_|$ANDROIDAPI|g" demon.sh
sed -i "s|_NDKAPI_|$NDKAPI|g" demon.sh
sed -i "s|_ANDROIDNDKVER_|$ANDROIDNDKVER|g" demon.sh
sed -i "s|_NAME_APP_|$NAME_APP|g" demon.sh
echo "Setup options is completed. All options write to file '$CURR_DIR/demon.sh'"

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

echo "Now demon.sh be waiting while make new commit on githun with new version in config.sh and run script build.py on Windows..."
echo "Running demon.sh"
./demon.sh

read -p "Press ENTER for exit..."
