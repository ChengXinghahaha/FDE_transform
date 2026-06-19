# test_api.py —— 最小连通性测试:验证环境 + LLM API 是否打通
# 用法见同目录说明;key 从 .env 读取,绝不写死在代码里。
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # 读取同目录下的 .env

api_key = os.getenv("LLM_API_KEY")
base_url = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
model = os.getenv("LLM_MODEL", "deepseek-chat")

if not api_key:
    raise SystemExit("❌ 没找到 LLM_API_KEY,请在同目录建一个 .env 文件并填入你的 key")

client = OpenAI(api_key=api_key, base_url=base_url)

try:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "只回复四个字:连接成功"}],
        timeout=30,
    )
    print("模型返回:", resp.choices[0].message.content)
    print("✅ API 连通正常,环境就绪")
except Exception as e:
    print("❌ 调用失败,排查 key / base_url / model 是否正确")
    print("错误信息:", repr(e))
