from db import *
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    telegram_id = Column(Integer)


class ToDoList(Base):
    __tablename__ = "todolist"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    description = Column(String)
    done = Column(Boolean)
    user = relationship("User", back_populates="todolist")


User.todolist = relationship("ToDoList", order_by=ToDoList.id, back_populates="user")

Base.metadata.create_all(engine)
