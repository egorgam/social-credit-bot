from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    chat_id = Column(Integer, primary_key=True, nullable=False)
    rank = Column(Integer, nullable=False)
