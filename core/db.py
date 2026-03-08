# core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 创建 MySQL 引擎（移除 SQLite 的 connect_args）
engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 模型基类
Base = declarative_base()

# 依赖注入：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()