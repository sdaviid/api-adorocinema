from sqlalchemy import(
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.types import(
    Date,
    Boolean,
    Time,
    DateTime,
    Text
)
from sqlalchemy.orm import(
    relationship,
    backref
)
from app.models.base import ModelBase
from app.core.database import Base
from datetime import datetime



class Title(ModelBase, Base):
    __tablename__ = "title"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())


    @classmethod
    def add(cls, session, info):
        title = Title()
        title.name = info
        session.add(title)
        session.commit()
        session.refresh(title)
        return Title.find_by_id(session=session, id=title.id)
