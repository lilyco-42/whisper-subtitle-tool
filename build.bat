@echo off
chcp 65001 >nul
setlocal

REM ==============================================================
REM  Nuitka 打包 gui_transcribe.py → 独立 .exe
REM  需要: MSVC 或 MinGW (gcc), Python 3.10+
REM ==============================================================

echo [0/4] 检查 Python 环境...
python --version || (echo Python not found! && pause && exit /b 1)

echo [1/4] 安装打包依赖...
pip install nuitka ordered-set zstandard -q

echo [2/4] 确保应用依赖已安装...
pip install faster-whisper maliang -q

echo [3/4] 开始 Nuitka 编译 (预计 5~15 分钟)...
echo     使用 GCC-MinGW64 编译器...

python -m nuitka ^
    --mingw64 ^
    --standalone ^
    --windows-console-mode=disable ^
    --enable-plugin=tk-inter ^
    --include-package=maliang ^
    --include-package=faster_whisper ^
    --include-package=ctranslate2 ^
    --include-package-data-dir=ctranslate2=ctranslate2 ^
    --mingw64 ^
    --assume-yes-for-downloads ^
    --output-dir=build ^
    gui_transcribe.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [FAIL] 编译失败, 请检查上方错误信息。
    echo 可尝试:
    echo   1. 使用 MSVC: 在 Visual Studio Developer Command Prompt 中运行
    echo   2. 去掉 --mingw64 使用系统默认编译器
    pause
    exit /b 1
)

echo.
echo [4/4] 复制输出文件...

REM 复制 exe 到当前目录
if exist "build\gui_transcribe.dist\gui_transcribe.exe" (
    copy /Y "build\gui_transcribe.dist\gui_transcribe.exe" ".\音频转字幕工具.exe"
    echo ==============================================================
    echo   打包成功! 输出文件: 音频转字幕工具.exe
    echo.
    echo   运行时请将此 exe 与音频文件放在同一目录,
    echo   或直接双击启动后在界面内刷新文件列表。
    echo.
    echo   注意: 首次启动需下载 Whisper 模型 (~1-4GB),
    echo   模型将缓存在 %%USERPROFILE%%/.cache/huggingface 下。
    echo ==============================================================
) else (
    echo [FAIL] 找不到 build\gui_transcribe.dist\gui_transcribe.exe
)

pause
endlocal
