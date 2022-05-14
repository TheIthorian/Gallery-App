@echo off
cmd /k "cd /d %~dp0\react & npm install & cd /d %~dp0\src & py -m venv ./venv & cd /d %~dp0\src\venv\Scripts & activate & pip install -r ../../requirements.txt & pip install flask-mysql"