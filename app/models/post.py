from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1000), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relation to User
    user = relationship("User", back_populates="posts")
