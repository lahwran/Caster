@echo off
echo Runnig DNS/DPI from Dragonfly CLI with Natlink.
timeout /t 20
set currentpath=%~dp0

TITLE Caster: Status Window
c:\python27\python.exe -m dragonfly load --engine natlink _*.py --no-recobs-messages

pause 1