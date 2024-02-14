from pydantic import BaseModel
from typing import List, Optional

class ReviewBase(BaseModel):
    book_review: str
    rating: float
    book_id: int

class Review(ReviewBase):
    id:int
    book_id:Optional[int] = None
    class Config:
        orm_mode = True
        
class BookBase(BaseModel):
    title: str
    author: str
    publication_year: int

class Book(BookBase):
    id: int
    review : List[Review]
    class Config:
        orm_mode = True

class BookResponse(BookBase):
    id:int
    title: str
    author: str
    publication_year: int
    class Config:
        orm_mode = True