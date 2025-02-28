from pydantic import BaseModel, constr
from typing import List


# For creating a post
class PostCreate(BaseModel):
    text: constr(min_length=1, max_length=1000)


# For post response
class PostResponse(BaseModel):
    id: int
    text: str
    user_id: int

    class Config:
        from_attributes = True


# For listing posts
class PostListResponse(BaseModel):
    posts: List[PostResponse]
