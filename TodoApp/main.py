
from pyexpat import model
from typing import Optional
from xmlrpc.client import boolean
from fastapi import FastAPI, Depends, HTTPException

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

from pydantic import BaseModel, Field

from auth import get_user_exceptions, get_current_user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# used to create a sesstion of database connection and close db whether we get connection or not


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# this class has been created to define data schema for a POST request


class Todo(BaseModel):

    title: str
    description: Optional[str]
    priority: int = Field(
        gt=0, lt=6, description="The priority must be between 1-5")
    complete: boolean

    # todos.db table will get created as soon as we hit this api


@app.get("/")
# db parameter depends on get_db function, now read_all gets executed after get_db
async def read_all(db: Session = Depends(get_db)):
    # returns all records from todos model/table
    return db.query(models.Todos).all()


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exceptions()
    todo_record = db.query(models.Todos).filter(
        models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo_record is not None:
        return todo_record
    else:
        raise http_exception()


# add a todo model record in db
@app.post("/")
async def create_todo(todo: Todo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exceptions()
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")
    db.add(todo_model)  # add a todo_model object to session
    db.commit()  # flush pending changes in the session to database and commit the transaction
    return successful_response(201)


@app.put("/todo/{todo_id}")
async def update_todo(todo_id: int, todo: Todo, user: dict = Depends(get_current_user),  db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exceptions()

    todo_model = db.query(models.Todos)\
        .filter(
        models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo_model is None:
        raise http_exception()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    db.add(todo_model)  # add the updated todo model in db session
    db.commit()  # commit db session to database
    return successful_response(200)


@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):

    if user is None:
        raise get_user_exceptions()

    todo_model = db.query(models.Todos).filter(
        models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo_model is None:
        raise http_exception()
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
    return successful_response(200)


@app.get("/todos/user")
async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exceptions()
    print(user)
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()


def successful_response(status_code: int):
    return {"status": status_code, "transaction": "successful"}


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")
