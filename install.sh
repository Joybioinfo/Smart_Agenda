#!/bin/zsh

# 获取当前脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 检查是否有权限访问.zshrc
if [ ! -w ~/.zshrc ]; then
    echo "错误：没有写入权限访问 ~/.zshrc 文件"
    echo "请尝试使用以下命令添加权限："
    echo "chmod u+w ~/.zshrc"
    exit 1
fi

# 检查.zshrc文件是否存在
if [ ! -f ~/.zshrc ]; then
    touch ~/.zshrc
fi

# 检查是否已经存在该函数
if grep -q "generate_agenda()" ~/.zshrc; then
    echo "函数已经存在于.zshrc中，跳过添加。"
else
    # 添加函数到.zshrc的自定义函数区域
    echo "\n# Custom functions for Smart Agenda" >> ~/.zshrc
    echo "generate_agenda() {" >> ~/.zshrc
    echo "    python3 $SCRIPT_DIR/agenda_template_generator.py" >> ~/.zshrc
    echo "}" >> ~/.zshrc
    echo "函数已成功添加到.zshrc中。"
fi

# 重新加载zsh配置
source ~/.zshrc

echo "安装完成！现在你可以在任何目录下使用 'generate_agenda' 命令了。" 