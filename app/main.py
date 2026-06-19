# app/main.py —— FastAPI 应用入口
# 第1周目标:先让服务能起来,有一个健康检查接口。后面再往上加 LLM 抽取、数据库。
from fastapi import FastAPI

app = FastAPI(
    title="制造业工程/运维知识智能助手",
    version="0.1.0",
)


@app.get("/")
def health():
    """健康检查:用来确认服务正常启动。"""
    return {"status": "ok", "service": "manufacturing-knowledge-assistant"}
