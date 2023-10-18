import subprocess

VERSION = "1.10"

ARCH = "armeabi-v7a"
# ARCH = "x86_64"

command = \
    "p4a apk " + \
    "--debug " + \
    "--private=$HOME/PycharmProjects/syncbookerkivy-main " + \
    "--package=com.github.xayam.syncbookerkivy " + \
    "--dist_name=syncbooker " + \
    '--name="SyncBooker" ' + \
    "--wakelock " + \
    "--window " + \
    "--permission android.permission.INTERNET " + \
    "android.permission.READ_EXTERNAL_STORAGE " + \
    "android.permission.WRITE_EXTERNAL_STORAGE " + \
    "android.permission.GLOBAL_SEARCH " + \
    "android.permission.MEDIA_CONTENT_CONTROL " + \
    "android.permission.READ_MEDIA_AUDIO " + \
    "--orientation=landscape " + \
    "--icon=$HOME/PycharmProjects/syncbookerkivy-main/img/icon.png " + \
    "--presplash=$HOME/PycharmProjects/syncbookerkivy-main/img/presplash.png " + \
    "--version=" + VERSION + " " + \
    "--arch=" + ARCH + " " + \
    "--bootstrap=sdl2 " + \
    "--requirements=android,python3,kivy,cython,ffmpeg,libx264,libshine,libvpx," + \
    "av_codecs,ffpyplayer,openssl,ffpyplayer_codecs,setuptools,regex," + \
    "sdl2_image,sdl2_ttf,sdl2_mixer,sdl2"

if __name__ == "__main__":
    subprocess.call([command], shell=True)
