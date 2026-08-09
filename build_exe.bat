@echo off
REM Build a standalone Windows executable for GCVX_IMS.
REM Run this from Windows (not from this Linux sandbox) after installing
REM the dependencies in requirements.txt.

setlocal

set APP_NAME=GCVX_IMS

echo Installing dependencies...
pip install -r requirements.txt

echo Building %APP_NAME%.exe ...
if exist icon.ico (
    pyinstaller --noconfirm --onefile --windowed --name %APP_NAME% ^
        --icon=icon.ico ^
        --add-data "error.html;." ^
        --add-data "images.png;." ^
        --add-data "icon.ico;." ^
        --add-data "icon.icns;." ^
        main.py
) else (
    pyinstaller --noconfirm --onefile --windowed --name %APP_NAME% ^
        --add-data "error.html;." ^
        --add-data "images.png;." ^
        main.py
)

echo.
echo Done. Find the executable in the "dist" folder as %APP_NAME%.exe
endlocal
pause
