
from typing import Optional
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

BOOKS = {
    "book_1": {"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams"},
    "book_2": {"title": "The Restaurant at the End of the Universe", "author": "Douglas Adams"},
    "book_3": {"title": "Life, the Universe and Everything", "author": "Douglas Adams"},
    "book_4": {"title": "So Long, and Thanks for All the Fish", "author": "Douglas Adams"},
    "book_5": {"title": "Mostly Harmless", "author": "Douglas Adams"}
}


# enum using class
class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"


@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS


@app.get("/books/mybook")
async def read_favorite_book():
    return BOOKS["book_1"]


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    # logic to read a book
    for book in BOOKS:
        if BOOKS[book].get("title") == book_title:
            return BOOKS[book]
    return {"error": "Book not found"}


@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction": direction_name, "sub": "Up"}
    if direction_name == DirectionName.south:
        return {"Direction": direction_name, "sub": "Down"}
    if direction_name == DirectionName.east:
        return {"Direction": direction_name, "sub": "Right"}
    if direction_name == DirectionName.west:
        return {"Direction": direction_name, "sub": "Left"}


@app.get("/{book_name}")
async def read_book(book_name: str):
    return BOOKS[book_name]


# create book

@app.post("/")
async def create_book(book_title, book_author):
    current_book_id = 1
    if len(BOOKS) > 0:
        for book in BOOKS:
            book_id = int(book.split("_")[1])
            if book_id >= current_book_id:
                current_book_id += 1
    BOOKS[f"book_{current_book_id}"] = {
        "title": book_title, "author": book_author}
    return BOOKS[f"book_{current_book_id}"]


@app.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    book_information = {"title": book_title, "author": book_author}
    BOOKS[book_name] = book_information
    return BOOKS[book_name]


@app.delete("/{book_name}")
async def delete_book(book_name: str):
    del BOOKS[book_name]
    return f"{book_name} deleted"
