@echo off
cmd /k "cd /d %~dp0\src\venv\Scripts & activate & cd /d %~dp0\src & py main.py"