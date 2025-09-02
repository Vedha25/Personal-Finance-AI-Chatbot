"""
AI Analytics endpoints for advanced financial analysis
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from app.core.security import verify_token
from app.services.watson_service import WatsonService

logger = logging.getLogger(__name__)
router = APIRouter()

class PredictionRequest(BaseModel):
    prediction_type: str = "spending"  # spending, savings, investment
    user_data: Dict[str, Any]

class AIInsightsRequest(BaseModel):
    user_data: Dict[str, Any]

class FinancialAnalysisRequest(BaseModel):
    analysis_type: str = "comprehensive"  # comprehensive, portfolio, spending
    user_data: Dict[str, Any]

@router.post("/predict", response_model=Dict[str, Any])
async def predict_financial_outcomes(
    request: PredictionRequest,
    current_user: Dict[str, Any] = Depends(verify_token)
):
    """Predict financial outcomes using AI and statistical analysis"""
    try:
        user_id = current_user.get("sub")
        logger.info(f"Financial prediction requested for user {user_id}: {request.prediction_type}")
        
        # Initialize Watson service
        watson_service = WatsonService()
        
        # Make prediction
        prediction = await watson_service.predict_financial_outcomes(
            request.user_data,
            request.prediction_type
        )
        
        if "error" in prediction:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=prediction["error"]
            )
        
        logger.info(f"Prediction completed successfully for user {user_id}")
        return prediction
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate prediction. Please try again."
        )

@router.post("/insights", response_model=List[Dict[str, Any]])
async def generate_ai_insights(
    request: AIInsightsRequest,
    current_user: Dict[str, Any] = Depends(verify_token)
):
    """Generate AI-powered financial insights and recommendations"""
    try:
        user_id = current_user.get("sub")
        logger.info(f"AI insights requested for user {user_id}")
        
        # Initialize Watson service
        watson_service = WatsonService()
        
        # Generate insights
        insights = await watson_service.generate_ai_insights(request.user_data)
        
        if not insights:
            return []
        
        logger.info(f"Generated {len(insights)} AI insights for user {user_id}")
        return insights
        
    except Exception as e:
        logger.error(f"AI insights generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate AI insights. Please try again."
        )

@router.post("/analyze", response_model=Dict[str, Any])
async def comprehensive_financial_analysis(
    request: FinancialAnalysisRequest,
    current_user: Dict[str, Any] = Depends(verify_token)
):
    """Perform comprehensive financial analysis using AI"""
    try:
        user_id = current_user.get("sub")
        logger.info(f"Comprehensive analysis requested for user {user_id}: {request.analysis_type}")
        
        # Initialize Watson service
        watson_service = WatsonService()
        
        analysis_results = {}
        
        if request.analysis_type == "comprehensive":
            # Generate all types of insights
            insights = await watson_service.generate_ai_insights(request.user_data)
            analysis_results["ai_insights"] = insights
            
            # Generate predictions for different aspects
            spending_prediction = await watson_service.predict_financial_outcomes(
                request.user_data, "spending"
            )
            analysis_results["spending_prediction"] = spending_prediction
            
            savings_prediction = await watson_service.predict_financial_outcomes(
                request.user_data, "savings"
            )
            analysis_results["savings_prediction"] = savings_prediction
            
            # Add sentiment analysis if user has recent messages
            if request.user_data.get("recent_messages"):
                sentiment_analysis = await watson_service.analyze_sentiment(
                    " ".join(request.user_data["recent_messages"])
                )
                analysis_results["sentiment_analysis"] = sentiment_analysis
        
        elif request.analysis_type == "portfolio":
            # Focus on investment analysis
            if request.user_data.get("portfolio"):
                investment_prediction = await watson_service.predict_financial_outcomes(
                    request.user_data, "investment"
                )
                analysis_results["investment_analysis"] = investment_prediction
        
        elif request.analysis_type == "spending":
            # Focus on spending analysis
            spending_prediction = await watson_service.predict_financial_outcomes(
                request.user_data, "spending"
            )
            analysis_results["spending_analysis"] = spending_prediction
            
            # Add spending insights
            if request.user_data.get("transactions"):
                insights = await watson_service.generate_ai_insights(request.user_data)
                spending_insights = [insight for insight in insights if "spending" in insight.get("type", "")]
                analysis_results["spending_insights"] = spending_insights
        
        analysis_results["analysis_type"] = request.analysis_type
        analysis_results["timestamp"] = datetime.utcnow().isoformat()
        analysis_results["user_id"] = user_id
        
        logger.info(f"Comprehensive analysis completed for user {user_id}")
        return analysis_results
        
    except Exception as e:
        logger.error(f"Comprehensive analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to perform financial analysis. Please try again."
        )

@router.get("/health", response_model=Dict[str, Any])
async def ai_analytics_health():
    """Health check for AI analytics service"""
    return {
        "status": "healthy",
        "service": "AI Analytics Service",
        "capabilities": [
            "Financial Predictions",
            "AI-Powered Insights", 
            "Comprehensive Analysis",
            "Sentiment Analysis",
            "Statistical Modeling"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }
