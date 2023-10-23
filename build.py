import ftplib
import subprocess

from ..ftpconfig import HOST, USER, PASSWORD
from src.model.utils import get_app_version

build_syncbooker = "venv/Scripts/python.exe -m PyInstaller syncbooker.spec"
build_createsync = "venv/Scripts/python.exe -m PyInstaller createsync.spec"

subprocess.call([build_syncbooker], shell=True)
subprocess.call([build_createsync], shell=True)

latest = "latest.txt"
version = "v" + get_app_version()

with open(latest, mode="w") as f:
    f.write(version)

session = ftplib.FTP(HOST, USER, PASSWORD)

session.mkd(version)

with open("dist/syncbooker.exe", mode="rb") as f:
    session.storbinary(f"STOR {version}/syncbooker-{version}.exe", f)

with open("dist/createsync.exe", mode="rb") as f:
    session.storbinary(f"STOR {version}/createsync-{version}.exe", f)

with open(latest, mode="rb") as f:
    session.storbinary(f"STOR latest/{latest}", f)

session.quit()
