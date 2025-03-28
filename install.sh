#!/bin/bash

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then 
    echo "请使用root权限运行此脚本"
    exit 1
fi

# 创建应用目录
mkdir -p /opt/smart-inv
mkdir -p /opt/smart-inv/data
mkdir -p /opt/smart-inv/logs

# 创建系统用户
useradd -r -s /bin/false stock || true

# 设置目录权限
chown -R stock:stock /opt/smart-inv
chmod -R 755 /opt/smart-inv
chmod 777 /opt/smart-inv/logs  # 确保日志目录可写

# 创建虚拟环境
python3 -m venv /opt/smart-inv/venv
source /opt/smart-inv/venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制服务文件
cp stock-analysis.service /etc/systemd/system/

# 重新加载systemd
systemctl daemon-reload

# 启用服务
systemctl enable stock-analysis

# 启动服务
systemctl start stock-analysis

echo "安装完成！"
echo "服务状态："
systemctl status stock-analysis

echo "日志文件位置："
echo "- 应用日志：/opt/smart-inv/logs/app.log"
echo "- 错误日志：/opt/smart-inv/logs/error.log"
echo ""
echo "查看日志的命令："
echo "- 实时查看应用日志：tail -f /opt/smart-inv/logs/app.log"
echo "- 实时查看错误日志：tail -f /opt/smart-inv/logs/error.log"
echo "- 查看系统日志：journalctl -u stock-analysis -f" 