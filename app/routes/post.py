from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.post_service import add_post, get_posts, delete_post
from app.schemas.post import PostCreate
from app.dependencies.auth_dependency import get_current_user

router = APIRouter()

# Add Post Route
@router.post("/posts", summary="Create a new post")
async def create_post(post_data: PostCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await add_post(post_data, db, user)

# Get Posts Route
@router.get("/posts", summary="Retrieve all posts")
async def list_posts(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await get_posts(db, user)

# Delete Post Route
@router.delete("/posts/{post_id}", summary="Delete a post")
async def remove_post(post_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await delete_post(post_id, db, user)