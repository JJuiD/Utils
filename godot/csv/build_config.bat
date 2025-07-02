@echo off
python ./tools/csv2src.py ./config/ ./game_project/config/
@REM xcopy .\config\script .\src\config\script\ /E /Y
