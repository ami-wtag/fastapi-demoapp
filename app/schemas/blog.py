from pydantic import BaseModel, UUID4
from typing import Optional

from app.schemas.base import AppBaseModel


class BlogBasic(BaseModel):
    title: str
    sub_title: str = None
    author: UUID4


class BlogBasicWithAuthor(BlogBasic):
    author: UUID4


class BlogId(BaseModel):
    id: UUID4


class BlogList(BlogBasicWithAuthor, BlogId):
    class Config:
        orm_mode = True


class BlogCreate(BaseModel):
    title: str
    sub_title: str = None
    body: str
    author: UUID4 = '8c8434bc-3ca0-47dd-a820-b2f27ce877a7'

    class Config:
        orm_mode = True


class BlogDetails(AppBaseModel, BlogCreate, BlogId):
    class Config:
        orm_mode = True


class BlogUpdate(BlogId):
    title: Optional[str]
    sub_title: Optional[str]
    body: Optional[str]

    class Config:
        extra = 'forbid'
        orm_mode = True
