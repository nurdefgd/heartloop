from sqlalchemy import Boolean, Column, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from datetime import date

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=True)
    phone_verified = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    birth_date = Column(Date)
    gender = Column(String)
    bio = Column(String, nullable=True)
    profile_photo = Column(String, nullable=True)
    location = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(Date, default=date.today)
    verification_code = Column(String, nullable=True)
    verification_code_expires = Column(Date, nullable=True)

    # Дополнительные поля можно добавить позже:
    # interests = relationship("Interest", back_populates="user")
    # matches = relationship("Match", back_populates="user")
    # messages = relationship("Message", back_populates="user") 