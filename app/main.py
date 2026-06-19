# app/main.py —— FastAPI 应用入口
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.llm import extract_work_order
from app.db import SessionLocal, WorkOrder, init_db

app = FastAPI(
    title="制造业工程/运维知识智能助手",
    version="0.3.0",
)

# 应用启动时确保表已建好
init_db()


# 每个请求拿一个数据库会话,用完自动关闭(FastAPI 的依赖注入机制)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def serialize(w: WorkOrder) -> dict:
    """把数据库行对象转成可返回的 dict。"""
    return {
        "id": w.id,
        "raw_text": w.raw_text,
        "equipment": w.equipment,
        "symptom": w.symptom,
        "cause": w.cause,
        "action": w.action,
        "parts": w.parts,
    }


@app.get("/")
def health():
    """健康检查。"""
    return {"status": "ok", "service": "manufacturing-knowledge-assistant"}


class ExtractRequest(BaseModel):
    text: str


@app.post("/extract")
def extract(req: ExtractRequest, db: Session = Depends(get_db)):
    """抽取工单结构化字段并存入数据库,返回存好的记录 id。"""
    result = extract_work_order(req.text)
    wo = WorkOrder(
        raw_text=req.text,
        equipment=result.get("equipment"),
        symptom=result.get("symptom"),
        cause=result.get("cause"),
        action=result.get("action"),
        parts=result.get("parts"),
    )
    db.add(wo)
    db.commit()
    db.refresh(wo)  # 拿到数据库分配的自增 id
    return {"id": wo.id, "extracted": result}


@app.get("/work_orders")
def list_work_orders(db: Session = Depends(get_db)):
    """列出所有工单(最新的在前)。"""
    rows = db.query(WorkOrder).order_by(WorkOrder.id.desc()).all()
    return [serialize(w) for w in rows]


@app.get("/work_orders/{wo_id}")
def get_work_order(wo_id: int, db: Session = Depends(get_db)):
    """按 id 查一条工单。"""
    w = db.get(WorkOrder, wo_id)
    if w is None:
        raise HTTPException(status_code=404, detail="未找到该工单")
    return serialize(w)
