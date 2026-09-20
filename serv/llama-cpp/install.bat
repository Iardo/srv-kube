@echo off
setlocal enabledelayedexpansion

rem References
rem --------------------
rem https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md

rem NOTE:
rem Run this from a "Developer Command Prompt for VS" (or after calling
rem vcvarsall.bat), otherwise "cl" (the MSVC compiler) won't be on PATH.

set "rootpath=%~dp0"
if "%rootpath:~-1%"=="\" set "rootpath=%rootpath:~0,-1%"

if exist "%rootpath%\code\.installed" (
    echo llama.cpp is already installed, skipping ^(%rootpath%\code\.installed exists^).
    exit /b 0
)

set "missing="
where git >nul 2>nul
if errorlevel 1 set "missing=!missing! Git (https://git-scm.com/download/win)"
where cmake >nul 2>nul
if errorlevel 1 set "missing=!missing! CMake (https://cmake.org/download/)"
where cl >nul 2>nul
if errorlevel 1 set "missing=!missing! MSVC C/C++ build tools (the 'Desktop development with C++' workload from https://visualstudio.microsoft.com/downloads/, run this script from a 'Developer Command Prompt for VS')"

if defined missing (
    echo Missing required tools:!missing!
    echo Install them yourself, then re-run this script.
    exit /b 1
)

if not exist "%rootpath%\code" (
    echo Cloning llama.cpp ...
    git clone https://github.com/ggml-org/llama.cpp "%rootpath%\code"
    if errorlevel 1 exit /b 1
)

rem NOTE:
rem GPU offload needs the CUDA toolkit (nvcc), not just the driver.
rem There is no root-free / unattended way to install it on Windows,
rem so just detect it and print a manual command instead of attempting it blindly.
set "cuda_flag="
where nvidia-smi >nul 2>nul
if not errorlevel 1 (
    nvidia-smi >nul 2>nul
    if not errorlevel 1 (
        echo NVIDIA GPU detected.
        where nvcc >nul 2>nul
        if errorlevel 1 (
            echo CUDA toolkit ^(nvcc^) not found. Building CPU-only for now.
            echo To enable GPU offload, install the CUDA Toolkit yourself, then re-run this install:
            echo   https://developer.nvidia.com/cuda-downloads
        ) else (
            set "cuda_flag=-DGGML_CUDA=ON"
        )
    ) else (
        echo No NVIDIA GPU detected, building CPU-only.
    )
) else (
    echo No NVIDIA GPU detected, building CPU-only.
)

echo Building llama.cpp ...
rem LLAMA_CURL=OFF drops the libcurl dependency, which is only needed for
rem the "-hf" auto-download flag; this setup places models by hand.
cmake -B "%rootpath%\code\build" -S "%rootpath%\code" -DLLAMA_CURL=OFF %cuda_flag%
if errorlevel 1 exit /b 1
cmake --build "%rootpath%\code\build" --config Release -j %NUMBER_OF_PROCESSORS%
if errorlevel 1 exit /b 1

echo Linking llama-server/llama-cli/llama into %USERPROFILE%\bin ...
if not exist "%USERPROFILE%\bin" mkdir "%USERPROFILE%\bin"
for %%b in (llama-server llama-cli llama) do (
    if exist "%rootpath%\code\build\bin\Release\%%b.exe" (
        del /f /q "%USERPROFILE%\bin\%%b.exe" 2>nul
        mklink /H "%USERPROFILE%\bin\%%b.exe" "%rootpath%\code\build\bin\Release\%%b.exe" >nul 2>nul
        if errorlevel 1 copy /Y "%rootpath%\code\build\bin\Release\%%b.exe" "%USERPROFILE%\bin\%%b.exe" >nul
    )
)

rem Models live centralized under the user profile,
rem junctioned in at the path other tooling expects.
set "models_dir=%USERPROFILE%\llms\models\llamacpp"
if not exist "%models_dir%" mkdir "%models_dir%"
if not exist "%rootpath%\data" mkdir "%rootpath%\data"
if not exist "%rootpath%\data\models" (
    mklink /J "%rootpath%\data\models" "%models_dir%" >nul
)

rem If this host declares a model list (host\<host>\data\llama-cpp\models.yml),
rem link it in so "models.py" can read it.
for /d %%h in ("%rootpath%\..\..\host\*") do (
    if exist "%%h\data\llama-cpp\models.yml" (
        del /f /q "%rootpath%\data\models.yml" 2>nul
        mklink /H "%rootpath%\data\models.yml" "%%h\data\llama-cpp\models.yml" >nul 2>nul
        if errorlevel 1 copy /Y "%%h\data\llama-cpp\models.yml" "%rootpath%\data\models.yml" >nul
        goto :models_done
    )
)
:models_done

type nul > "%rootpath%\code\.installed"

echo Done. Place your .gguf model(s^) under %models_dir% and start the server with:
echo(
echo Text-only:
echo   llama-server --model %models_dir%\^<model^>.gguf --host 0.0.0.0 --port 8080
echo(
echo With GPU offload and vision/file input ^(needs the model's own --mmproj file, some models ship one^):
echo   llama-server --model %models_dir%\^<model^>.gguf --mmproj %models_dir%\^<model-mmproj^>.gguf --n-gpu-layers 999 --host 0.0.0.0 --port 8080
echo(
echo ^(Make sure %USERPROFILE%\bin is on PATH.^)

endlocal
