from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    credits = Column(Integer, default=20, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    generations = relationship("Generation", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")


class Generation(Base):
    __tablename__ = "generations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(10), nullable=False)
    model = Column(String(50), nullable=False)
    prompt = Column(Text, nullable=False)
    credits_used = Column(Integer, nullable=False)
    status = Column(String(20), default="pending")
    result_url = Column(Text, nullable=True)
    is_public = Column(Boolean, default=True)
    settings = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="generations")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(10), nullable=False)
    credits = Column(Integer, nullable=False)
    usd_amount = Column(Float, nullable=True)
    stripe_payment_id = Column(String(255), nullable=True)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
