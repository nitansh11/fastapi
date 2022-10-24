from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# create a database file
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

# create session with engine: it is a instance of a database connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create Base to be used in models

Base = declarative_base()
