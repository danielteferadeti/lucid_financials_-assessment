from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.user_service import signup, login
from app.schemas.user import UserCreate, UserLogin, TokenResponse

router = APIRouter()

# Signup route
@router.post("/signup", summary="Create a new user")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await signup(user_data, db)

# Login route
@router.post("/login", response_model=TokenResponse, summary="User login")
async def user_login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await login(user_data, db)