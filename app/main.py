from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.post import router as post_router
from app.database import init_db

app = FastAPI(
    title="FastAPI CRUD API",
    version="1.0",
    description="A simple CRUD API with authentication",
)


# Initialize database
@app.on_event("startup")
async def startup():
    await init_db()  # Ensure DB tables are created


# API routes
app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(post_router, prefix="/api", tags=["Posts"])


# Root route
@app.get("/", summary="Welcome Route")
async def root():
    return {"message": "Welcome to FastAPI CRUD API!"}
