@echo off
chcp 65001 >nul
setlocal

echo ==============================================================
echo   音频转字幕工具 - 环境安装脚本
echo ==============================================================
echo.

echo [1/3] 检查 Python 环境...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] 未找到 Python。请先安装 Python 3.10+:
    echo   https://www.python.org/downloads/
    echo   安装时务必勾选 "Add Python to PATH"
    pause
    exit /b 1
)
python --version
echo.

echo [2/3] 升级 pip...
python -m pip install --upgrade pip -q
echo.

echo [3/3] 安装项目依赖...
pip install faster-whisper maliang --quiet
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] 依赖安装失败!
    pause
    exit /b 1
)
echo.

echo ==============================================================
echo   环境安装完成!
echo.
echo   启动方式:
echo     方式1 (GUI):  python gui_transcribe.py
echo     方式2 (命令行): python transcribe.py
echo     方式3 (打包): build.bat
echo ==============================================================

pause
endlocal
