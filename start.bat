@echo off
REM 表情符号检查器 - Windows启动脚本
echo ========================================
echo 表情符号检查器系统
echo ========================================
echo.

REM 检查虚拟环境是否存在
if not exist "venv\" (
    echo [1/4] 创建虚拟环境...
    python -m venv venv
    echo.
)

REM 激活虚拟环境
echo [2/4] 激活虚拟环境...
call venv\Scripts\activate.bat
echo.

REM 安装/更新依赖
echo [3/4] 检查依赖包...
pip install -q -r requirements.txt
echo.

REM 运行环境测试
echo [4/4] 测试环境配置...
python test_environment.py
echo.

REM 根据测试结果决定是否启动
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo 启动应用...
    echo ========================================
    echo.
    echo 应用将在 http://localhost:5000 运行
    echo 按 Ctrl+C 停止服务器
    echo.
    python app.py
) else (
    echo.
    echo ========================================
    echo 环境测试失败，请查看上述错误信息
    echo ========================================
    echo.
    pause
)

