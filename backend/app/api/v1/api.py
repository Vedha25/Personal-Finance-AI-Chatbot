"""
Main API router for Personal Finance Chatbot
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, chat, ai_analytics

api_router = APIRouter()

# Include all endpoint modules
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(chat.router, prefix="/chat", tags=["AI Chat"])
api_router.include_router(ai_analytics.router, prefix="/ai-analytics", tags=["AI Analytics"])
