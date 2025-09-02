"""
Database configuration and models for Personal Finance Chatbot
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional
import json

from app.core.config import settings

# Database URL conversion for async
async_database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine
engine = create_async_engine(
    async_database_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create async session
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency to get database session
async def get_db():
    """Get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# User Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    age = Column(Integer)
    occupation = Column(String(100))
    income_level = Column(String(50))  # low, medium, high
    financial_goals = Column(JSON)  # Store goals as JSON
    risk_tolerance = Column(String(20))  # low, medium, high
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="user")
    goals = relationship("FinancialGoal", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")
    financial_profile = relationship("FinancialProfile", back_populates="user", uselist=False)

# Transaction Model
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    category = Column(String(100), nullable=False)
    subcategory = Column(String(100))
    description = Column(Text)
    transaction_date = Column(DateTime, nullable=False)
    transaction_type = Column(String(20))  # income, expense, transfer
    tags = Column(JSON)  # Store tags as JSON array
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transactions")

# Financial Goal Model
class FinancialGoal(Base):
    __tablename__ = "financial_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    currency = Column(String(3), default="USD")
    target_date = Column(DateTime)
    goal_type = Column(String(50))  # savings, investment, debt_payoff
    priority = Column(String(20))  # low, medium, high
    status = Column(String(20), default="active")  # active, completed, paused
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="goals")

# Financial Profile Model
class FinancialProfile(Base):
    __tablename__ = "financial_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    net_worth = Column(Float, default=0.0)
    monthly_income = Column(Float, default=0.0)
    monthly_expenses = Column(Float, default=0.0)
    savings_rate = Column(Float, default=0.0)
    debt_to_income_ratio = Column(Float, default=0.0)
    emergency_fund = Column(Float, default=0.0)
    investment_portfolio = Column(JSON)  # Store portfolio as JSON
    credit_score = Column(Integer)
    financial_health_score = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="financial_profile")

# Chat Session Model
class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String(255), unique=True, index=True)
    context = Column(JSON)  # Store conversation context
    user_profile = Column(JSON)  # Store user profile snapshot
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session")

# Chat Message Model
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    message_type = Column(String(20))  # user, assistant, system
    content = Column(Text, nullable=False)
    metadata = Column(JSON)  # Store additional message data
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("ChatSession", back_populates="messages")

# Financial Category Model
class FinancialCategory(Base):
    __tablename__ = "financial_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    category_type = Column(String(20))  # income, expense, investment
    icon = Column(String(100))
    color = Column(String(7))  # Hex color code
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# AI Model Response Cache
class AIResponseCache(Base):
    __tablename__ = "ai_response_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    query_hash = Column(String(255), unique=True, index=True)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    model_used = Column(String(100))
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

# Financial Insights Model
class FinancialInsight(Base):
    __tablename__ = "financial_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    insight_type = Column(String(50))  # spending_pattern, savings_opportunity, investment_tip
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    data = Column(JSON)  # Store insight data as JSON
    priority = Column(String(20))  # low, medium, high
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")

# Initialize database
async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Database utilities
async def get_db_session():
    """Get database session"""
    async with AsyncSessionLocal() as session:
        return session

async def close_db():
    """Close database connections"""
    await engine.dispose()
