"""
User models for Personal Finance Chatbot
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    """Base user model"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)
    age: Optional[int] = Field(None, ge=13, le=120)
    occupation: Optional[str] = Field(None, max_length=100)
    income_level: Optional[str] = Field(None, regex="^(low|medium|high)$")
    risk_tolerance: Optional[str] = Field(None, regex="^(low|medium|high)$")

class UserCreate(UserBase):
    """User creation model"""
    password: str = Field(..., min_length=8, max_length=128)
    
    @validator('username')
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError('Username must contain only alphanumeric characters')
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    """User update model"""
    full_name: Optional[str] = Field(None, max_length=255)
    age: Optional[int] = Field(None, ge=13, le=120)
    occupation: Optional[str] = Field(None, max_length=100)
    income_level: Optional[str] = Field(None, regex="^(low|medium|high)$")
    risk_tolerance: Optional[str] = Field(None, regex="^(low|medium|high)$")
    financial_goals: Optional[List[dict]] = None

class UserResponse(UserBase):
    """User response model"""
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user: UserResponse

class PasswordChange(BaseModel):
    """Password change model"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('New password must be at least 8 characters long')
        return v

class UserProfile(BaseModel):
    """User profile model"""
    user: UserResponse
    financial_profile: Optional[dict] = None
    goals: Optional[List[dict]] = None
    recent_transactions: Optional[List[dict]] = None
    insights: Optional[List[dict]] = None

class FinancialGoalCreate(BaseModel):
    """Financial goal creation model"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    target_amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=3)
    target_date: Optional[datetime] = None
    goal_type: str = Field(..., regex="^(savings|investment|debt_payoff|emergency_fund|retirement|other)$")
    priority: str = Field(default="medium", regex="^(low|medium|high)$")

class FinancialGoalUpdate(BaseModel):
    """Financial goal update model"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    target_amount: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, max_length=3)
    target_date: Optional[datetime] = None
    goal_type: Optional[str] = Field(None, regex="^(savings|investment|debt_payoff|emergency_fund|retirement|other)$")
    priority: Optional[str] = Field(None, regex="^(low|medium|high)$")
    status: Optional[str] = Field(None, regex="^(active|completed|paused|cancelled)$")

class FinancialGoalResponse(BaseModel):
    """Financial goal response model"""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    target_amount: float
    current_amount: float
    currency: str
    target_date: Optional[datetime]
    goal_type: str
    priority: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    """Transaction creation model"""
    amount: float
    currency: str = Field(default="USD", max_length=3)
    category: str = Field(..., max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    transaction_date: datetime
    transaction_type: str = Field(..., regex="^(income|expense|transfer)$")
    tags: Optional[List[str]] = None

class TransactionUpdate(BaseModel):
    """Transaction update model"""
    amount: Optional[float] = None
    currency: Optional[str] = Field(None, max_length=3)
    category: Optional[str] = Field(None, max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    transaction_date: Optional[datetime] = None
    transaction_type: Optional[str] = Field(None, regex="^(income|expense|transfer)$")
    tags: Optional[List[str]] = None

class TransactionResponse(BaseModel):
    """Transaction response model"""
    id: int
    user_id: int
    amount: float
    currency: str
    category: str
    subcategory: Optional[str]
    description: Optional[str]
    transaction_date: datetime
    transaction_type: str
    tags: Optional[List[str]]
    created_at: datetime
    
    class Config:
        from_attributes = True

class FinancialProfileUpdate(BaseModel):
    """Financial profile update model"""
    net_worth: Optional[float] = None
    monthly_income: Optional[float] = None
    monthly_expenses: Optional[float] = None
    emergency_fund: Optional[float] = None
    credit_score: Optional[int] = Field(None, ge=300, le=850)
    investment_portfolio: Optional[dict] = None

class FinancialProfileResponse(BaseModel):
    """Financial profile response model"""
    id: int
    user_id: int
    net_worth: float
    monthly_income: float
    monthly_expenses: float
    savings_rate: float
    debt_to_income_ratio: float
    emergency_fund: float
    investment_portfolio: Optional[dict]
    credit_score: Optional[int]
    financial_health_score: float
    last_updated: datetime
    
    class Config:
        from_attributes = True

class UserPreferences(BaseModel):
    """User preferences model"""
    notification_settings: Optional[dict] = None
    privacy_settings: Optional[dict] = None
    ui_preferences: Optional[dict] = None
    financial_goals_visibility: Optional[str] = Field(None, regex="^(public|private|friends_only)$")

class UserStats(BaseModel):
    """User statistics model"""
    total_transactions: int
    total_goals: int
    completed_goals: int
    total_saved: float
    current_month_spending: float
    current_month_income: float
    streak_days: int
    financial_health_score: float
