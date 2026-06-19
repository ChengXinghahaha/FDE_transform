# app/llm.py —— 封装"调大模型做信息抽取"的逻辑
# 单独放一个文件:接口层(main.py)不关心怎么调模型,只管要结果。
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL", "https://api.deepseek.com"),
)
MODEL = os.getenv("LLM_MODEL", "deepseek-chat")

# 告诉模型:它的角色、要抽哪些字段、必须只输出 JSON
SYSTEM_PROMPT = """你是制造业设备维修工单的信息抽取助手。
从用户给的工单文本里抽取结构化字段,只输出一个 JSON 对象,不要任何多余文字或解释。
需要抽取的字段:
- equipment: 设备名称(字符串)
- symptom:   故障现象(字符串)
- cause:     故障原因(字符串)
- action:    处理措施(字符串)
- parts:     涉及的零件名称(字符串数组)
原文里没有的字段,字符串填 null,数组填 []。"""


def extract_work_order(text: str) -> dict:
    """把一段工单文本抽取成结构化 dict。"""
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0,  # 抽取任务要稳定,温度设 0
        response_format={"type": "json_object"},  # 强制返回 JSON
        timeout=30,
    )
    content = resp.choices[0].message.content
    return json.loads(content)  # 把 JSON 字符串转成 Python dict
