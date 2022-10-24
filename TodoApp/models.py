from enum import unique
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

# {
#   "email": "nitansh11@gmail.com",
#   "username": "nitansh11",
#   "first_name": "Nitansh",
#   "last_name": "Rastogi",
#   "password": "nitansh11"
# }


# create a table


class Users(Base):
    __tablename__ = "users"  # actual table name in database
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    # created using some encryption which can't be decrypted
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # adding a one-to-many relationship to todos
    todos = relationship("Todos", back_populates="owner")


class Todos(Base):
    __tablename__ = "todos"  # actual table name in database

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="todos")
