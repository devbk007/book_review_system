import time

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/book", response_model=schemas.BookResponse)
def create_book(book: schemas.BookBase, db:Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exist")
    else:
        return crud.create_book(db=db, book=book)

@app.get("/book/", response_model=List[schemas.Book])
def get_books(db: Session = Depends(get_db)):
    books = crud.get_books(db)
    return books

@app.get("/book/{book_id}", response_model=schemas.Book)
def get_book(book_id:int, db:Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db=db, id = book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        return db_book

@app.put("/book/{book_id}", response_model=schemas.BookResponse)
def update_book(book: schemas.BookBase, book_id:int, db:Session = Depends(get_db)):
    db_book = crud.update_book_by_id(db=db, id=book_id, book=book)
    if db_book is None :
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        return db_book

@app.delete("/book/{book_id}")
def delete_book(book_id:int, db:Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    elif db_book=="IntegrityError":
        raise HTTPException(status_code=400, detail="Unable to delete review due to integrity constraints")
    else:
        return status.HTTP_204_NO_CONTENT

@app.post("/review", response_model=schemas.Review)
def create_review(review: schemas.ReviewBase, db:Session = Depends(get_db)):
    review = crud.create_review(db=db, review=review)
    if review is None:
        raise HTTPException(status_code=404, detail="Book id does not exist")
    else:
        return review

@app.get("/review/", response_model=List[schemas.Review])
def get_reviews(db: Session = Depends(get_db)):
    reviews = crud.get_reviews(db)
    for review in reviews:
        print("Review ID:", review.id)
        print("Book ID:", review.book_id)
        print("Book Review:", review.book_review)
        print("Rating:", review.rating)
        print("-------------------")
    return reviews

@app.get("/review/{review_id}", response_model=schemas.Review)
def get_review(review_id:int, db:Session = Depends(get_db)):
    db_review = crud.get_review(db, review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    else:
        return db_review

@app.put("/review/{review_id}", response_model=schemas.Review)
def update_review(review:schemas.ReviewBase ,review_id:int, db:Session = Depends(get_db)):
    db_review = crud.update_review(db, review_id, review=review)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    else:
        return db_review

@app.delete("/review/{review_id}")
def delete_review(review_id:int, db:Session = Depends(get_db)):
    db_review = crud.delete_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    elif db_review=="IntegrityError":
        raise HTTPException(status_code=400, detail="Unable to delete review due to integrity constraints")
    else:
        return status.HTTP_204_NO_CONTENT