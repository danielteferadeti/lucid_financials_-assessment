from pydantic import BaseModel, EmailStr, constr


# For user signup
class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)


# For user response (excluding password)
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


# For login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# For login response (token)
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
