@echo off
cmd /k "cd /d %~dp0\react & npm install & cd /d %~dp0\src & py virtualenv ./venv & cd /d %~dp0\src\venv\Scripts & activate & pip install requirements.txt & exit"