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
- Install python 3.7-3.10 (tested only version 3.10)
- Create virtual env, run command "python.exe -m venv venv"
- Activate venv, run command "venv/Scripts/activate.bat"
- Upgrade pip, run command "python.exe -m pip install -upgrade pip"
- Install requirements, run command "pip install -r requirements.txt"
- Install Graphviz with set path env, installer by link https://graphviz.org/download/
- For create project scheme app.svg run commands "cd src" and "pyan3 **/*.py --uses --no-defines --colored --grouped --annotated --svg > app.svg"
- Run main.py with python

# For own build apk (for run this file on Android)

- Install Ubuntu 22 on VirtualBox
- Run virtual machine with Ubuntu 22
- Install depends: https://python-for-android.readthedocs.io/en/latest/quickstart/ for Ubuntu 22
- Download build-template.sh
- Copy build-template.sh in new file, run command "cp ./build-template.sh ./build.sh"
- Edit file build.sh: 
  - add path to SDK and NDK 
  - add own vars 'ftp_site', 'username', and 'passwd'
- Run terminal in folder with file build.sh
- You must mark the file as executable, run command "chmod +x build.sh"
- Run ./build.sh as program for create apk-file
- Run .apk on Android
