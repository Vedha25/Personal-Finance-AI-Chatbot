"""
Chat endpoints for AI Financial Advisor
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any
import logging

from app.core.security import verify_token
from app.services.watson_service import WatsonService
from app.services.financial_service import FinancialService

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    confidence: float = 0.0

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    chat_request: ChatRequest,
    current_user: Dict[str, Any] = Depends(verify_token)
):
    """Chat with AI Financial Advisor"""
    try:
        # Get user context for personalized responses
        user_id = current_user.get("sub")
        
        # Process the message and generate response
        # This is a simplified response - you can integrate with Watson or other AI services
        response = generate_financial_advice(chat_request.message, current_user)
        
        logger.info(f"AI chat response generated for user {user_id}")
        
        return ChatResponse(
            response=response,
            confidence=0.85
        )
        
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate response. Please try again."
        )

def generate_financial_advice(message: str, user_context: Dict[str, Any]) -> str:
    """Generate financial advice based on user message and context"""
    
    message_lower = message.lower()
    
    # Basic keyword-based responses (you can enhance this with AI/ML)
    if any(word in message_lower for word in ['invest', 'investment', 'stock', 'portfolio']):
        risk_tolerance = user_context.get('risk_tolerance', 'moderate')
        if risk_tolerance == 'conservative':
            return "For conservative investors, I recommend focusing on low-risk investments like government bonds, high-quality corporate bonds, and dividend-paying blue-chip stocks. Consider a 60/40 bond-to-stock ratio for stability."
        elif risk_tolerance == 'aggressive':
            return "With an aggressive risk profile, you might consider growth stocks, emerging markets, and alternative investments. However, ensure you have a diversified portfolio and can handle market volatility."
        else:
            return "For moderate risk tolerance, a balanced portfolio with 50% stocks, 30% bonds, and 20% alternative investments could work well. Consider index funds for broad market exposure."
    
    elif any(word in message_lower for word in ['budget', 'saving', 'expense']):
        return "Start by tracking all your expenses for a month. Use the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings. Consider using budgeting apps and setting up automatic transfers to savings accounts."
    
    elif any(word in message_lower for word in ['debt', 'credit', 'loan']):
        return "Focus on high-interest debt first (credit cards, payday loans). Consider debt consolidation or balance transfers for better rates. Pay more than minimum payments when possible. For student loans, explore income-driven repayment plans."
    
    elif any(word in message_lower for word in ['retirement', '401k', 'ira']):
        age = user_context.get('age', 30)
        if age < 30:
            return "Start early! Contribute to your 401(k) up to the employer match, then consider a Roth IRA. With decades ahead, you can afford to be more aggressive in your investments."
        elif age < 50:
            return "Maximize your 401(k) contributions and consider catch-up contributions if you're over 50. Review your asset allocation and ensure you're on track for your retirement goals."
        else:
            return "Focus on preserving capital while maintaining growth. Consider reducing stock exposure and increasing bond allocation. Review your retirement timeline and adjust your strategy accordingly."
    
    elif any(word in message_lower for word in ['emergency', 'fund']):
        return "Aim for 3-6 months of living expenses in an emergency fund. Keep it in a high-yield savings account for easy access. Start small and build it up gradually."
    
    elif any(word in message_lower for word in ['insurance', 'protection']):
        return "Ensure you have health, auto, and home/renters insurance. Consider life insurance if you have dependents, and disability insurance to protect your income. Review your coverage annually."
    
    elif any(word in message_lower for word in ['tax', 'deduction', 'refund']):
        return "Maximize tax-advantaged accounts like 401(k)s and IRAs. Consider itemizing deductions if you have significant expenses. Keep good records and consider consulting a tax professional for complex situations."
    
    else:
        return "I'd be happy to help with your financial questions! You can ask me about investments, budgeting, debt management, retirement planning, emergency funds, insurance, or taxes. What specific area would you like to discuss?"
