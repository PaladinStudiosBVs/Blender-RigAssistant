@echo off
python create_virtualenv.py
call venv\Scripts\activate.bat
venv\Scripts\pip3.exe install fake-bpy-module
pause
