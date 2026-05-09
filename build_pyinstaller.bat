@echo off
chcp 65001 >nul
setlocal

REM ==============================================================
REM  PyInstaller 打包 gui_transcribe.py → 独立 .exe (备用方案)
REM  比 Nuitka 更快, 但 exe 稍大, 启动略慢
REM ==============================================================

echo [0/3] 检查 Python 环境...
python --version || (echo Python not found! && pause && exit /b 1)

echo [1/3] 安装打包依赖...
pip install pyinstaller -q
pip install faster-whisper maliang -q

echo [2/3] 开始 PyInstaller 编译 (预计 1~3 分钟)...

pyinstaller ^
    --name="音频转字幕工具" ^
    --windowed ^
    --onefile ^
    --clean ^
    --add-data="ctranslate2;ctranslate2" ^
    --hidden-import=ctranslate2 ^
    --hidden-import=faster_whisper ^
    --hidden-import=maliang ^
    --hidden-import=maliang.core ^
    --hidden-import=maliang.standard ^
    --hidden-import=maliang.animation ^
    --hidden-import=maliang.color ^
    --hidden-import=maliang.theme ^
    --hidden-import=maliang.toolbox ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --collect-all=maliang ^
    --collect-all=faster_whisper ^
    --collect-all=ctranslate2 ^
    gui_transcribe.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [FAIL] PyInstaller 编译失败!
    pause
    exit /b 1
)

echo.
echo [3/3] 复制输出文件...
if exist "dist\音频转字幕工具.exe" (
    copy /Y "dist\音频转字幕工具.exe" ".\音频转字幕工具.exe" >nul
    echo ==============================================================
    echo   打包成功! 输出: 音频转字幕工具.exe
    echo ==============================================================
) else (
    echo [FAIL] 找不到 dist\音频转字幕工具.exe
)

pause
endlocal
