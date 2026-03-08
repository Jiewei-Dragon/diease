from sqlalchemy import Column, Integer, String
from core.db import Base


class TbUser(Base):
    __tablename__ = "tb_user"  # 和原表名保持一致

    ID = Column(Integer, primary_key=True, index=True, comment="用户ID")
    Phone = Column(String(20), unique=True, index=True, comment="手机号")
    Password = Column(String(100), comment="密码")
    # 可添加其他字段（如用户名、创建时间等）