@echo off

venv\Scripts\python.exe -m PyInstaller syncbooker.spec

venv\Scripts\python.exe -m PyInstaller createsync.spec
