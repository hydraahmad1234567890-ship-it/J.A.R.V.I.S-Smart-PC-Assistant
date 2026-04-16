@echo off
REM J.A.R.V.I.S. Mark IV - Silent Boot
echo 🤖 J.A.R.V.I.S. is waking up in the background...
cd /d "%~dp0"
start /min python server.py
exit
