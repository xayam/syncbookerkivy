@echo off

powershell -Command "Invoke-WebRequest http://apk.delphima.z8.ru/latest/latest.txt -OutFile latest.txt"
set /p VERSION=<latest.txt
set APK=syncbooker-armeabi-v7a-debug-%VERSION%.apk
echo %APK%
REM powershell -Command "Invoke-WebRequest http://apk.delphima.z8.ru/%VERSION%/%APK% -OutFile %APK%"

adb.exe install -r %APK%
adb.exe logcat --clear
adb.exe shell monkey -p com.github.xayam.syncbookerkivy -c android.intent.category.LAUNCHER 1
adb.exe -d logcat com.github.xayam.syncbookerkivy:V > logcat.txt
notepad++.exe logcat.txt

pause
