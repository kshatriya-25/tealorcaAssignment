#OM VIGHNHARTAYE NAMO NAMAH :

from pydantic import BaseModel, EmailStr
from typing import Optional
from decimal import Decimal

# User Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

# Book Schemas
class BookCreate(BaseModel):
    title: str
    author_id: int
    published_year: Optional[int]

class BookResponse(BaseModel):
    id: int
    title: str
    author_id: int
    published_year: Optional[int]

    class Config:
        from_attributes = True

# Author Schemas
class AuthorCreate(BaseModel):
    name: str

class AuthorResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# Genre Schemas
class GenreCreate(BaseModel):
    genre_name: str

class GenreResponse(BaseModel):
    id: int
    genre_name: str

    class Config:
        from_attributes = True

# Review Schemas
class ReviewCreate(BaseModel):
    user_id: int
    book_id: int
    rating: Decimal
    review_text: Optional[str]

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: Decimal
    review_text: Optional[str]

    class Config:
        from_attributes = True
