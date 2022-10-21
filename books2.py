from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(
        title="Description of the book", max_length=100, min_length=1)
    rating: int = Field(gt=-1, lt=101)  # between 0 and 100 inclusive


BOOKS = []


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    return BOOKS


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x


@app.put("/book/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter-1] = book
            return BOOKS[counter-1]


@app.delete("/book/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter-1]
            return {"message": "Book deleted"}
