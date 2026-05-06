from sqlalchemy import Column, Integer, String, DateTime
from core.db import Base


class TbUser(Base):
    __tablename__ = "tb_user"

    ID = Column(Integer, primary_key=True, index=True, comment="用户ID")
    Phone = Column(String(20), unique=True, index=True, comment="手机号")
    Password = Column(String(100), comment="密码")
    IsAdmin = Column(Integer, default=0, comment="是否管理员：1-管理员，0-普通用户")
    IsBanned = Column(Integer, default=0, comment="是否被封禁：1-封禁，0-正常")
    CreateTime = Column(DateTime, name="create_time", comment="创建时间")
    UpdateTime = Column(DateTime, name="update_time", comment="更新时间")
