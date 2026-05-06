from sqlalchemy import Column, Integer, String, Float
from core.db import Base


class TbRecord(Base):
    __tablename__ = "tb_record"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    UserId = Column(Integer, comment="用户ID")
    OriginMapUrl = Column(String(255), comment="原图路径")
    HeatmapUrl = Column(String(255), comment="热力图路径")
    Confidence = Column(Float, comment="置信度")
    DieaseType = Column(Integer, comment="病害索引")
    DieaseName = Column(String(50), comment="病害名称")
    CreateTime = Column(String(20), comment="创建时间")
