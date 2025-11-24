#!/bin/bash
# 表情符号检查器 - Linux/Mac启动脚本

echo "========================================"
echo "表情符号检查器系统"
echo "========================================"
echo ""

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "[1/4] 创建虚拟环境..."
    python3 -m venv venv
    echo ""
fi

# 激活虚拟环境
echo "[2/4] 激活虚拟环境..."
source venv/bin/activate
echo ""

# 安装/更新依赖
echo "[3/4] 检查依赖包..."
pip install -q -r requirements.txt
echo ""

# 运行环境测试
echo "[4/4] 测试环境配置..."
python test_environment.py
TEST_RESULT=$?
echo ""

# 根据测试结果决定是否启动
if [ $TEST_RESULT -eq 0 ]; then
    echo "========================================"
    echo "启动应用..."
    echo "========================================"
    echo ""
    echo "应用将在 http://localhost:5000 运行"
    echo "按 Ctrl+C 停止服务器"
    echo ""
    python app.py
else
    echo ""
    echo "========================================"
    echo "环境测试失败，请查看上述错误信息"
    echo "========================================"
    echo ""
    read -p "按Enter键退出..."
fi

