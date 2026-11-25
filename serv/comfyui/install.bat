@echo off
setlocal enabledelayedexpansion

rem References
rem --------------------
rem https://docs.comfy.org/installation/manual_install

set "rootpath=%~dp0"
if "%rootpath:~-1%"=="\" set "rootpath=%rootpath:~0,-1%"

if exist "%rootpath%\code\.installed" (
    echo ComfyUI is already installed, skipping ^(%rootpath%\code\.installed exists^).
    exit /b 0
)

set "missing="
where git >nul 2>nul
if errorlevel 1 set "missing=!missing! Git (https://git-scm.com/download/win)"
where python >nul 2>nul
if errorlevel 1 set "missing=!missing! Python 3 (https://www.python.org/downloads/, check 'Add python.exe to PATH' during install)"

if defined missing (
    echo Missing required tools:!missing!
    echo Install them yourself, then re-run this script.
    exit /b 1
)

python -m pip --version >nul 2>nul
if errorlevel 1 (
    echo pip is not available for this Python install. Reinstall Python from
    echo https://www.python.org/downloads/ with pip included, then re-run.
    exit /b 1
)

python -m venv --help >nul 2>nul
if errorlevel 1 (
    echo The "venv" module is not available for this Python install. Reinstall
    echo Python from https://www.python.org/downloads/, then re-run.
    exit /b 1
)

if not exist "%rootpath%\code" (
    echo Cloning ComfyUI ...
    git clone https://github.com/comfyanonymous/ComfyUI.git "%rootpath%\code"
    if errorlevel 1 exit /b 1
)

echo Creating virtual environment ...
python -m venv "%rootpath%\code\.venv"
call "%rootpath%\code\.venv\Scripts\activate.bat"
pip install --upgrade pip wheel
pip install -r "%rootpath%\code\requirements.txt"
call "%rootpath%\code\.venv\Scripts\deactivate.bat"

echo Adding 'comfyui' command to %USERPROFILE%\bin ...
if not exist "%USERPROFILE%\bin" mkdir "%USERPROFILE%\bin"
(
    echo @echo off
    echo "%rootpath%\code\.venv\Scripts\python.exe" "%rootpath%\code\main.py" %%*
) > "%USERPROFILE%\bin\comfyui.bat"

rem Models live centralized under the user profile (shared across any repo
rem clone/host on this machine), one category subfolder at a time, matching
rem ComfyUI's own "code\models\<category>" layout.
set "models_root=%USERPROFILE%\llms\models\comfyui"
if not exist "%models_root%" mkdir "%models_root%"
for /d %%c in ("%rootpath%\code\models\*") do (
    fsutil reparsepoint query "%%c" >nul 2>nul
    if errorlevel 1 (
        set "category=%%~nxc"
        if not exist "%models_root%\!category!" mkdir "%models_root%\!category!"
        robocopy "%%c" "%models_root%\!category!" /E /MOVE >nul
        rmdir "%%c" 2>nul
        mklink /J "%%c" "%models_root%\!category!" >nul
    )
)

rem If this host declares a model list (host\<host>\data\comfyui\models.yml),
rem link it in so "models.py" can read it.
if not exist "%rootpath%\data" mkdir "%rootpath%\data"
if not exist "%rootpath%\data\models" (
    mklink /J "%rootpath%\data\models" "%models_root%" >nul
)
for /d %%h in ("%rootpath%\..\..\host\*") do (
    if exist "%%h\data\comfyui\models.yml" (
        del /f /q "%rootpath%\data\models.yml" 2>nul
        mklink /H "%rootpath%\data\models.yml" "%%h\data\comfyui\models.yml" >nul 2>nul
        if errorlevel 1 copy /Y "%%h\data\comfyui\models.yml" "%rootpath%\data\models.yml" >nul
        goto :models_done
    )
)
:models_done

type nul > "%rootpath%\code\.installed"

echo Done. Start it with:
echo   comfyui --listen 0.0.0.0
echo ^(Make sure %USERPROFILE%\bin is on PATH.^)

endlocal
