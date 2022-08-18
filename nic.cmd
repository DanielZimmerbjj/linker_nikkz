@echo off
color 02
python.exe C:\python\pythonProject\main.py
TIMEOUT /T 300
cls
start /b nic.cmd
exit