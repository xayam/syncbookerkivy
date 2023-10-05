@echo off

powershell -Command "Invoke-WebRequest http://apk.delphima.z8.ru/apks/syncbooker.apk -OutFile syncbooker.apk"

adb.exe install -r syncbooker.apk

adb.exe logcat --clear

adb.exe shell monkey -p com.github.xayam.syncbookerkivy -c android.intent.category.LAUNCHER 1

adb.exe -d logcat com.github.xayam.syncbookerkivy:V > logcat.txt

notepad++.exe logcat.txt

pause