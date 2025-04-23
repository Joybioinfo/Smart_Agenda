import os
from datetime import datetime
import getpass

# 默认设置
DEFAULT_SAVE_DIR = os.path.expanduser("~/Documents/iA Writer/daily_logs")
TEMPLATE_DIR = "./templates"
TEMPLATE_FILE = "daily_log_template.md"

def get_save_dir():
    """获取保存目录，如果环境变量未设置则使用默认值"""
    custom_dir = os.getenv("DAILY_LOG_DIR")
    if custom_dir:
        return os.path.expanduser(custom_dir)
    return DEFAULT_SAVE_DIR

def read_template():
    template_path = os.path.join(TEMPLATE_DIR, TEMPLATE_FILE)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"模板文件不存在: {template_path}")
    
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

def generate_log():
    # 获取保存目录
    save_dir = get_save_dir()
    
    # 确保目录存在
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"创建目录: {save_dir}")
    
    if not os.path.exists(TEMPLATE_DIR):
        os.makedirs(TEMPLATE_DIR)

    # 获取当前日期
    today_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today_str}_work_log.md"
    filepath = os.path.join(save_dir, filename)

    # 检查文件是否已存在
    if os.path.exists(filepath):
        print(f"已存在: {filepath}")
        return

    try:
        # 读取模板
        template = read_template()
        
        # 生成文件
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(template.format(date=today_str))

        print(f"生成成功: {filepath}")
    except Exception as e:
        print(f"生成失败: {str(e)}")

if __name__ == "__main__":
    generate_log()