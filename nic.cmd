@echo off
color 02
python.exe C:\python\pythonProject\parser.py
TIMEOUT /T 300
cls
start /b nic.cmd
exit