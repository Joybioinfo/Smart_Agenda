#!/bin/zsh

# 保存当前目录
ORIGINAL_DIR=$(pwd)

# 获取脚本所在目录的绝对路径并切换到该目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 检查是否有权限访问.zshrc
if [ ! -w ~/.zshrc ]; then
    echo "错误：没有写入权限访问 ~/.zshrc 文件"
    echo "请尝试使用以下命令添加权限："
    echo "chmod u+w ~/.zshrc"
    # 返回原目录
    cd "$ORIGINAL_DIR"
    exit 1
fi

# 检查.zshrc文件是否存在
if [ ! -f ~/.zshrc ]; then
    touch ~/.zshrc
fi

# 删除已存在的函数定义和相关注释
if grep -q "generate_agenda()" ~/.zshrc; then
    echo "删除已存在的函数定义..."
    # 使用sed删除从注释到函数结束之间的内容
    sed -i '' '/# Custom functions for Smart Agenda/,/^}/d' ~/.zshrc
    # 删除可能存在的空行
    sed -i '' '/^$/N;/\n$/D' ~/.zshrc
fi

# 添加新的函数定义
echo "\n# Custom functions for Smart Agenda" >> ~/.zshrc
echo "generate_agenda() {" >> ~/.zshrc
echo "    # 保存当前目录" >> ~/.zshrc
echo "    local CURRENT_DIR=\$(pwd)" >> ~/.zshrc
echo "    # 切换到脚本目录" >> ~/.zshrc
echo "    cd \"$SCRIPT_DIR\"" >> ~/.zshrc
echo "    python3 \"$SCRIPT_DIR/agenda_template_generator.py\"" >> ~/.zshrc
echo "    # 返回原目录" >> ~/.zshrc
echo "    cd \"\$CURRENT_DIR\"" >> ~/.zshrc
echo "}" >> ~/.zshrc
echo "函数已成功添加到.zshrc中。"

# 重新加载zsh配置
source ~/.zshrc

echo "安装完成！现在你可以在任何目录下使用 'generate_agenda' 命令了。"

# 返回原目录
cd "$ORIGINAL_DIR" 