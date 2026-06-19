# app/db.py —— 数据库连接与数据表定义
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

# 数据库地址从环境变量读,默认用本地 SQLite 文件 app.db。
# 第2周换 PostgreSQL 时,只要把 .env 里的 DATABASE_URL 改成 postgresql://... 即可,代码不用动。
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# SQLite 在 FastAPI 多线程下需要这个参数;换成 PostgreSQL 时不需要。
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class WorkOrder(Base):
    """一条维修工单对应数据库里的一行。"""
    __tablename__ = "work_orders"

    id = Column(Integer, primary_key=True, index=True)
    raw_text = Column(Text)               # 原始工单文本
    equipment = Column(String, nullable=True)  # 设备名称
    symptom = Column(Text, nullable=True)      # 故障现象
    cause = Column(Text, nullable=True)        # 故障原因
    action = Column(Text, nullable=True)       # 处理措施
    parts = Column(JSON, nullable=True)        # 涉及零件(数组,SQLite 里存成 JSON)


def init_db():
    """建表(表已存在则跳过)。"""
    Base.metadata.create_all(bind=engine)
