@echo off
chcp 65001 >nul
setlocal

REM ==============================================================
REM  Nuitka 打包 gui_transcribe.py → 独立 .exe
REM  编译器: 自动检测 (MSVC 优先, 已验证 MSVC 14.3 可用)
REM ==============================================================

echo [0/4] 检查 Python 环境...
python --version || (echo Python not found! && pause && exit /b 1)

echo [1/4] 安装打包依赖...
pip install nuitka ordered-set zstandard -q

echo [2/4] 确保应用依赖已安装...
pip install faster-whisper maliang -q

echo [3/4] 开始 Nuitka 编译 (预计 5~15 分钟)...

python -m nuitka ^
    --standalone ^
    --windows-console-mode=disable ^
    --enable-plugin=tk-inter ^
    --include-package=maliang ^
    --include-package=faster_whisper ^
    --include-package=ctranslate2 ^
    --noinclude-data-files="*.py" ^
    --assume-yes-for-downloads ^
    --output-dir=build ^
    gui_transcribe.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [FAIL] 编译失败, 请检查上方错误信息.
    echo.
    echo 常见解决:
    echo   - 若提示找不到编译器, 在 Visual Studio Developer Command Prompt 中运行本脚本
    echo   - 或安装 MinGW64 后加 --mingw64 参数
    pause
    exit /b 1
)

echo.
echo [4/4] 复制输出文件...

if exist "build\gui_transcribe.dist\gui_transcribe.exe" (
    copy /Y "build\gui_transcribe.dist\gui_transcribe.exe" ".\音频转字幕工具.exe"
    echo ==============================================================
    echo   打包成功! 输出: 音频转字幕工具.exe
    echo.
    echo   将此 exe 与音频文件放同一目录即可使用.
    echo   首次运行需下载 Whisper 模型 (~1-4GB).
    echo ==============================================================
) else (
    echo [FAIL] 找不到 build\gui_transcribe.dist\gui_transcribe.exe
)

pause
endlocal
