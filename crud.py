from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models, schemas


def get_book_by_title(db: Session, title: str):
    return db.query(models.Book).filter(models.Book.title == title).first()

def get_book_by_id(db: Session, id:int):
    return db.query(models.Book).get(id)

def create_book(db:Session, book:schemas.BookBase):
    db_book = models.Book(title = book.title, author=book.author, publication_year=book.publication_year)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session):
    return db.query(models.Book).all()

def delete_book(db:Session, id:int):
    db_book = db.query(models.Book).get(id)
    try:
        if db_book:
            db.delete(db_book)
            db.commit()
            return True
        return False
    except IntegrityError:
        db.rollback()
        return "IntegrityError"

def update_book_by_id(db:Session, id:int, book:schemas.BookBase):
    db_book = db.query(models.Book).get(id)
    if db_book:
        db_book.title = book.title
        db_book.author = book.author
        db_book.publication_year = book.publication_year
        db.commit()
        db.refresh(db_book)
        return db_book
    return None

def get_review(db: Session, id: int):
    return db.query(models.Review).filter(models.Review.id == id).first()

def get_reviews(db: Session):
    return db.query(models.Review).all()

def delete_review(db:Session, id:int):
    db_review = db.query(models.Review).get(id)
    try:
        if db_review:
            db.delete(db_review)
            db.commit()
            return True
        return False
    except IntegrityError:
        db.rollback()
        return "IntegrityError"

def update_review(db:Session, id:int, review:schemas.ReviewBase):
    db_review = db.query(models.Review).get(id)
    if db_review:
        db_review.book_review = review.book_review
        db_review.rating = review.rating
        db.commit()
        db.refresh(db_review)
        return db_review
    return None

def create_review(db:Session, review:schemas.ReviewBase):
    db_book = db.query(models.Book).filter(models.Book.id == review.book_id).first()
    if db_book:
        db_review = models.Review(book_review = review.book_review, rating=review.rating, book_id = review.book_id)
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review
    else:
        return None
