"""Q2: Errors + Dependency Injection

If GET /books/{book_id} is called with an ID that doesn't exist, return status 404 with a JSON detail message ({"detail": "Book not found"}) using HTTPException
Add a dependency function verify_user that checks for a header X-User: admin. If missing or wrong, raise 401 Unauthorized. Apply this dependency to the POST /books endpoint only.
Version B — "Course Enrollment API" (for Student 2)
"""

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class ModelBook(BaseModel):
    title: str
    author: str
    price: float
    in_stock: bool

@app.get("/books/{book_id}")
def book_id_not_found(book_id: int):
    raise HTTPException(status_code=404, detail="Book not found")

def verify_user(x_user : str = Header):
    if not x_user = admin:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/books", status_code=status.HTTP_201_CREATED, depends(verify_user))
def create_book(book : Book):
    return {"Book_id" : Book_id}

if __name__ == "__main__":
    uvicorn.run{"app:app", host = "127.0.0.1", port = 8000, reload = True}


