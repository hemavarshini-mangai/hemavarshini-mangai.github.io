"""Q1: Core CRUD with validation

Build a FastAPI app with:

A Pydantic model Book with fields: title (str), author (str), price (float), in_stock (bool)
POST /books — accepts a Book in the request body, returns it with status code 201
GET /books/{book_id} — path parameter, returns a book by ID (use an in-memory dict/list as storage)
GET /books?min_price=X — query parameter, returns only books priced ≥ min_price
"""

from fastapi import FastAPI, status
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class ModelBook(BaseModel):
    title: str
    author: str
    price: float
    in_stock: bool

@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: dict):
    return book

@app.get("/books/{book_id}")
def get_user(book_id: int):
    return {"book_id": book_id}

@app.get("/books")
def list_items(category: str , price: int >= min_price):
    return {"category": category}

if __name__ == "__main__":
    uvicorn.run{"app:app", host = "127.0.0.1", port = 8000, reload = True}
