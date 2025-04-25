#!/bin/zsh

# 检查是否有权限访问.zshrc
if [ ! -w ~/.zshrc ]; then
    echo "错误：没有写入权限访问 ~/.zshrc 文件"
    echo "请尝试使用以下命令添加权限："
    echo "chmod u+w ~/.zshrc"
    exit 1
fi

# 检查.zshrc文件是否存在
if [ ! -f ~/.zshrc ]; then
    echo "错误：~/.zshrc 文件不存在"
    exit 1
fi

# 删除已存在的函数定义和相关注释
if grep -q "generate_agenda()" ~/.zshrc; then
    echo "正在删除函数定义..."
    # 使用sed删除从注释到函数结束之间的内容
    sed -i '' '/# Custom functions for Smart Agenda/,/^}/d' ~/.zshrc
    # 删除可能存在的空行
    sed -i '' '/^$/N;/\n$/D' ~/.zshrc
    echo "函数已成功从.zshrc中移除。"
else
    echo "未找到需要移除的函数定义。"
fi

# 重新加载zsh配置
source ~/.zshrc

echo "卸载完成！" 