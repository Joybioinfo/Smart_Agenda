import os
from datetime import datetime

# 设置保存目录（可修改为你常用的笔记路径）
SAVE_DIR = "./daily_logs"

# 模板内容
TEMPLATE = """# 工作日志 - {date}

## 🎯 今天的目标
- 

## ✅ 今天做了什么
- 

## 💡 思考与发现
- 

## 🧱 遇到的问题
- 

## 🔜 明天的计划
- 
"""

def generate_log():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    today_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today_str}_work_log.md"
    filepath = os.path.join(SAVE_DIR, filename)

    if os.path.exists(filepath):
        print(f"已存在: {filepath}")
        return

    with open(filepath, "w") as f:
        f.write(TEMPLATE.format(date=today_str))

    print(f"生成成功: {filepath}")

if __name__ == "__main__":
    generate_log()