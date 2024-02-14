from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base
class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True)
    author = Column(String)
    publication_year = Column(Integer)

    review = relationship("Review")

class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id', ondelete="CASCADE"))
    book_review = Column(String)
    rating = Column(Float)

    # Define the relationship with Book and enable cascading delete
    book = relationship("Book", back_populates="review", cascade="all, delete")