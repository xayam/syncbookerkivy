import ftplib
import subprocess

from ftpconfig import HOST, USER, PASSWORD
from src.model.utils import get_app_version


def directory_exists(ftp, folder):
    filelist = []
    ftp.retrlines('LIST', filelist.append)
    for file in filelist:
        if file.split()[-1] == folder and file.upper().startswith('D'):
            return True
    return False


build = "build.bat"
subprocess.call([build], shell=False)

latest = "latest.txt"
version = "v" + get_app_version()

with open(latest, mode="w") as f:
    f.write(version)

print(f"Connecting to server '{HOST}'...")
session = ftplib.FTP(HOST, USER, PASSWORD)

print(f"Creating folder {version}...")
if directory_exists(session, version) is False:
    session.mkd(version)

print(f"Uploading {version}/syncbooker-{version}.exe...")
with open("dist/syncbooker.exe", mode="rb") as f:
    session.storbinary(f"STOR {version}/syncbooker-{version}.exe", f)

print(f"Uploading {version}/createsync-{version}.exe...")
with open("dist/createsync.exe", mode="rb") as f:
    session.storbinary(f"STOR {version}/createsync-{version}.exe", f)

print(f"Uploading latest/{latest}...")
with open(latest, mode="rb") as f:
    session.storbinary(f"STOR latest/{latest}", f)

session.quit()
