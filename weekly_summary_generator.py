import os
from datetime import datetime, timedelta
import openai
from pathlib import Path

# 配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OBSIDIAN_VAULT_PATH = os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/My Vault")
WEEKLY_SUMMARY_DIR = "Weekly_Summaries"
LOG_DIR = os.path.expanduser("~/Library/Mobile Documents/27N4MQEA55~pro~writer/Documents/daily_logs")

def get_week_dates():
    """获取当前周的日期范围"""
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

def read_daily_logs(start_date, end_date):
    """读取指定日期范围内的日志文件"""
    logs = []
    current_date = start_date
    while current_date <= end_date:
        log_file = os.path.join(LOG_DIR, f"{current_date.strftime('%Y-%m-%d')}_work_log.md")
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                logs.append(f.read())
        current_date += timedelta(days=1)
    return logs

def generate_summary(logs):
    """使用 OpenAI API 生成周总结"""
    if not OPENAI_API_KEY:
        raise ValueError("请设置 OPENAI_API_KEY 环境变量")

    openai.api_key = OPENAI_API_KEY
    
    # 构建提示词
    prompt = f"""请根据以下一周的工作日志，生成一份周总结报告。报告应包含：
1. 本周主要成就
2. 遇到的问题及解决方案
3. 下周计划
4. 个人成长与反思

工作日志内容：
{chr(10).join(logs)}"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个专业的工作总结助手，擅长从日常日志中提取关键信息并生成结构化的总结报告。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    return response.choices[0].message.content

def save_summary(summary, start_date):
    """保存周总结到 Obsidian Vault"""
    # 确保目录存在
    summary_dir = os.path.join(OBSIDIAN_VAULT_PATH, WEEKLY_SUMMARY_DIR)
    os.makedirs(summary_dir, exist_ok=True)
    
    # 生成文件名
    filename = f"周总结_{start_date.strftime('%Y-%m-%d')}.md"
    filepath = os.path.join(summary_dir, filename)
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    return filepath

def main():
    try:
        # 获取本周日期范围
        start_date, end_date = get_week_dates()
        
        # 读取日志
        logs = read_daily_logs(start_date, end_date)
        if not logs:
            print("本周没有找到任何日志文件")
            return
        
        # 生成总结
        print("正在生成周总结...")
        summary = generate_summary(logs)
        
        # 保存总结
        filepath = save_summary(summary, start_date)
        print(f"周总结已保存到: {filepath}")
        
    except Exception as e:
        print(f"生成周总结时出错: {str(e)}")

if __name__ == "__main__":
    main() 