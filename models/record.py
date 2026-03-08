from sqlalchemy import Column, Integer, String, Double
from core.db import Base


class TbRecord(Base):
    __tablename__ = "tb_record"  # 和表名保持一致
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    HeatmapUrl = Column(String(100), comment="热力图路径")
    Confidence = Column(Double(10), comment="置信度")
    DieaseType = Column(Integer, comment="病害索引")
    DieaseName = Column(String(10), comment="病害名称")
    CreateTime = Column(String(10), comment="创建时间")
    # 可添加其他字段（如用户名、创建时间等）