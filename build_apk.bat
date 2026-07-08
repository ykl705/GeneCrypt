@echo off
chcp 65001 > nul
echo ========================================
echo  GeneCrypt APK Builder
echo ========================================

:: Check if Ubuntu WSL is installed
wsl -l -v 2>nul | findstr "Ubuntu" >nul
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Ubuntu WSL not found. Installing...
    wsl --install -d Ubuntu-22.04
    echo [WARN] Please complete the Ubuntu setup (create username/password), then run this script again.
    pause
    exit /b 1
)

:: Check if distro is running
wsl -l -v 2>nul | findstr "Stopped" >nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Starting Ubuntu...
    wsl -d Ubuntu-22.04 -- bash -c "echo 'WSL Ready'"
)

:: Build the APK
echo [INFO] Installing buildozer and dependencies...
wsl -d Ubuntu-22.04 -- bash -c "
    cd /mnt/c/Users/17311/Desktop/abc\ -\ 副本/ && \
    sudo apt update -qq && \
    sudo apt install -y -qq python3-pip python3-dev libncurses5-dev && \
    pip3 install --user --upgrade buildozer cython && \
    export PATH=\$PATH:\$HOME/.local/bin && \
    echo '[INFO] Starting buildozer...' && \
    buildozer android debug 2>&1
"

:: Check result
if exist bin\*.apk (
    echo [SUCCESS] APK built successfully!
    dir bin\*.apk
) else (
    echo [ERROR] Build failed. Check output above.
)
pause
