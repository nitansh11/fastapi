from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# create a sqlite database file
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
# create a postgres database file
# POSTGRESQL_DATABASE_URL = "postgresql://postgres:12345678@localhost/TodoApplicationDatabase"
# create a mysql database file
MYSQL_DATABASE_URL = "mysql+pymysql://root:12345678@127.0.0.1:3306/todoapp"


# create engine for sqlite
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
#                        "check_same_thread": False})
# create engine for mysql and postgres
engine = create_engine(MYSQL_DATABASE_URL)

# create session with engine: it is a instance of a database connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create Base to be used in models

Base = declarative_base()
