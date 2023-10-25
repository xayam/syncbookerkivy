# SyncBookerKivy

- Sources for Android: https://github.com/xayam/syncbookerkivy
- Sources for Windows x64: https://github.com/xayam/syncbooker
- Telegram chat: https://t.me/syncbooker_chat

# Audio player for

- Synchrone read book
- Synchrone listen two books: russian or english 
- Text book on two language: russian and english
- Catalog audiobooks are included

# Catalog of books:

- Kafka Franz The Metamorphosis
- Kuttner Henry The Ego Machine
- Lewis Carroll Alices Adventures in Wonderland
- Wells Herbert The Time Machine

# Binary and source download

- Last release for Android https://github.com/xayam/syncbookerkivy/releases/latest
- Last release for Windows x64 https://github.com/xayam/syncbooker/releases/latest
- Copies in mail cloud https://cloud.mail.ru/public/rdBB/KHvCjQdaT

# Install and run from sources (on Windows)

- Download sources
- Install python 3.8 - tested only this version
- Create virtual env, run command "python.exe -m venv venv"
- Activate venv, run command "venv/Scripts/activate.bat"
- Upgrade pip, run command "python.exe -m pip install -upgrade pip"
- Install requirements, run command "pip install -r requirements.txt"
- Run main.py with python

# For own build apk (for run this file on Android) 

- Install Ubuntu 22 on VirtualBox
- Run virtual machine with Ubuntu 22
- Install depends: https://python-for-android.readthedocs.io/en/latest/quickstart/ for Ubuntu 22
- Clone git in you project on github
- Copy git in you project on local machine (on Windows)
- Install python 3.8 - tested only this version
- Create virtual env, run command "python.exe -m venv venv"
- Activate venv, run command "venv/Scripts/activate.bat"
- Upgrade pip, run command "python.exe -m pip install -upgrade pip"
- Install requirements, run command "pip install -r requirements.txt"
- run commands in terminal Ubuntu:
   - $ wget --quiet --output-document=setup.sh https://raw.githubusercontent.com/xayam/syncbookerkivy/main/setup.sh
   - $ sudo chmod +x setup.sh 
   - $ ./setup.sh
- Waiting while run daemon.sh, no close terminal
- Commit and push new version in you config.sh on github
- Create file ftpconfig.py with vars HOST, USER, PASSWORD for access to ftp server for uploading exe files
- Run local (on Windows) build.py for create exe files and upload on server with change version in latest/latest.txt
- Wait all complete
- Run .apk with arch 'armeabi-v7a' on Android; 
- Arch 'x86_64' may be run in emulator on Android Studio
