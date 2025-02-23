from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, Depends
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.auth import hash_password, verify_password, create_access_token
from app.database import get_db

# Signup a user
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)
    new_user = User(email=user_data.email, password_hash=hashed_password)
    db.add(new_user)
    await db.commit()
    return {"message": "User registered successfully"}

# Login a user
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalars().first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id, "email": user.email})
    return TokenResponse(access_token=token)