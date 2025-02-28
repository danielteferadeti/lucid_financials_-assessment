from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, Depends
from app.models.post import Post
from app.schemas.post import PostCreate
from app.dependencies.auth_dependency import get_current_user
from app.database import get_db
from cachetools import TTLCache

# In-memory cache for GetPosts
cache = TTLCache(maxsize=100, ttl=300)


# Add Post
async def add_post(
    post_data: PostCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    if len(post_data.text.encode("utf-8")) > 1024 * 1024:
        raise HTTPException(status_code=400, detail="Post size exceeds 1MB")

    new_post = Post(text=post_data.text, user_id=user["user_id"])
    db.add(new_post)
    await db.commit()
    return {"postID": new_post.id}


# Get Posts
async def get_posts(
    db: AsyncSession = Depends(get_db), 
    user=Depends(get_current_user)
):
    user_id = user["user_id"]

    if user_id in cache:
        return {"posts": cache[user_id]}

    result = await db.execute(select(Post).where(Post.user_id == user_id))
    posts = result.scalars().all()

    # Cache results for 5 minutes
    cache[user_id] = posts
    return {"posts": posts}


# Delete Post
async def delete_post(
    post_id: int, db: AsyncSession = Depends(get_db), 
    user=Depends(get_current_user)
):
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.user_id == user["user_id"])
    )
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    await db.delete(post)
    await db.commit()
    return {"message": "Post deleted successfully"}
