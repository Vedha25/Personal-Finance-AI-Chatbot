"""
Enhanced IBM Watson service for Personal Finance Chatbot
Handles chatbot interactions, NLP, financial guidance, and modern AI capabilities
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import asyncio
import aiohttp
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import ibm_watson
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions, KeywordsOptions

from app.core.config import settings
from app.core.security import hash_query, sanitize_input

logger = logging.getLogger(__name__)

class WatsonService:
    """Enhanced IBM Watson service with modern AI capabilities"""
    
    def __init__(self):
        """Initialize Watson services and modern AI components"""
        try:
            # Initialize Watson Assistant
            authenticator = IAMAuthenticator(settings.WATSON_API_KEY)
            self.assistant = AssistantV2(
                version=settings.WATSON_VERSION,
                authenticator=authenticator
            )
            self.assistant.set_service_url(settings.WATSON_URL)
            self.assistant_id = settings.WATSON_ASSISTANT_ID
            
            # Initialize Natural Language Understanding
            self.nlu = NaturalLanguageUnderstandingV1(
                version='2023-11-15',
                authenticator=authenticator
            )
            self.nlu.set_service_url(settings.WATSON_URL)
            
            # Initialize ML models for financial predictions
            self.spending_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
            self.risk_assessor = RandomForestRegressor(n_estimators=50, random_state=42)
            self.scaler = StandardScaler()
            
            # Market data cache
            self.market_cache = {}
            self.cache_expiry = {}
            
            # Financial knowledge base
            self.financial_kb = self._initialize_financial_knowledge_base()
            
            logger.info("Enhanced Watson services initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Watson services: {e}")
            self.assistant = None
            self.nlu = None
    
    def _initialize_financial_knowledge_base(self) -> Dict[str, Any]:
        """Initialize comprehensive financial knowledge base"""
        return {
            "investment_strategies": {
                "conservative": {
                    "allocation": {"bonds": 70, "stocks": 20, "cash": 10},
                    "recommendations": ["Government bonds", "Blue-chip dividend stocks", "High-yield savings"],
                    "risk_level": "Low",
                    "expected_return": "3-5% annually"
                },
                "moderate": {
                    "allocation": {"stocks": 60, "bonds": 30, "cash": 10},
                    "recommendations": ["Index funds", "Corporate bonds", "REITs"],
                    "risk_level": "Medium",
                    "expected_return": "6-8% annually"
                },
                "aggressive": {
                    "allocation": {"stocks": 80, "bonds": 15, "cash": 5},
                    "recommendations": ["Growth stocks", "International ETFs", "Alternative investments"],
                    "risk_level": "High",
                    "expected_return": "8-12% annually"
                }
            },
            "savings_goals": {
                "emergency_fund": {"target": "3-6 months expenses", "priority": "High"},
                "retirement": {"target": "25x annual expenses", "priority": "High"},
                "down_payment": {"target": "20% of home value", "priority": "Medium"},
                "vacation": {"target": "Flexible", "priority": "Low"}
            },
            "debt_strategies": {
                "avalanche": "Pay highest interest rate first",
                "snowball": "Pay smallest balance first",
                "consolidation": "Combine multiple debts into one",
                "refinancing": "Lower interest rates when possible"
            }
        }
    
    async def create_session(self, user_id: str) -> Optional[str]:
        """Create a new chat session"""
        try:
            if not self.assistant:
                return None
                
            response = self.assistant.create_session(
                assistant_id=self.assistant_id
            ).get_result()
            
            session_id = response['session_id']
            logger.info(f"Created Watson session: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to create Watson session: {e}")
            return None
    
    async def send_message(
        self, 
        session_id: str, 
        message: str, 
        user_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Send message to Watson Assistant and get enhanced response"""
        try:
            if not self.assistant:
                return await self._enhanced_fallback_response(message, user_context)
            
            # Sanitize input
            sanitized_message = sanitize_input(message)
            
            # Prepare context
            context = self._prepare_context(user_context)
            
            # Send message to Watson
            response = self.assistant.message(
                assistant_id=self.assistant_id,
                session_id=session_id,
                input={
                    'message_type': 'text',
                    'text': sanitized_message
                },
                context=context
            ).get_result()
            
            # Process response and enhance with AI insights
            base_response = self._process_watson_response(response, message)
            enhanced_response = await self._enhance_response_with_ai(
                base_response, message, user_context
            )
            
            return enhanced_response
            
        except Exception as e:
            logger.error(f"Failed to send message to Watson: {e}")
            return await self._enhanced_fallback_response(message, user_context)
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of financial text with enhanced AI capabilities"""
        try:
            if not self.nlu:
                return {"sentiment": "neutral", "score": 0.0}
            
            response = self.nlu.analyze(
                text=text,
                features=Features(
                    sentiment=SentimentOptions(),
                    keywords=KeywordsOptions()
                )
            ).get_result()
            
            sentiment = response.get('sentiment', {})
            
            # Enhanced sentiment analysis with financial context
            sentiment_label = sentiment.get('document', {}).get('label', 'neutral')
            sentiment_score = sentiment.get('document', {}).get('score', 0.0)
            
            # Financial sentiment classification
            financial_sentiment = self._classify_financial_sentiment(text, sentiment_label, sentiment_score)
            
            return {
                "sentiment": sentiment_label,
                "score": sentiment_score,
                "financial_sentiment": financial_sentiment,
                "keywords": [
                    kw['text'] for kw in response.get('keywords', [])
                ],
                "confidence": min(abs(sentiment_score) * 1.5, 1.0)
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze sentiment: {e}")
            return {"sentiment": "neutral", "score": 0.0}
    
    def _classify_financial_sentiment(self, text: str, sentiment: str, score: float) -> str:
        """Classify financial sentiment based on context and keywords"""
        text_lower = text.lower()
        
        # Financial stress indicators
        stress_keywords = ['debt', 'broke', 'struggling', 'worried', 'anxious', 'stress', 'overwhelmed']
        if any(keyword in text_lower for keyword in stress_keywords):
            return "financial_stress"
        
        # Financial confidence indicators
        confidence_keywords = ['confident', 'secure', 'stable', 'growing', 'investing', 'saving']
        if any(keyword in text_lower for keyword in confidence_keywords):
            return "financial_confidence"
        
        # Financial planning indicators
        planning_keywords = ['plan', 'goal', 'future', 'retirement', 'budget', 'strategy']
        if any(keyword in text_lower for keyword in planning_keywords):
            return "financial_planning"
        
        # Neutral financial discussion
        if sentiment == "neutral":
            return "financial_neutral"
        
        return "general_financial"
    
    async def get_financial_insights(
        self, 
        user_profile: Dict, 
        financial_data: Dict
    ) -> List[Dict[str, Any]]:
        """Generate personalized financial insights"""
        try:
            insights = []
            
            # Analyze spending patterns
            if financial_data.get('transactions'):
                spending_insight = await self._analyze_spending_patterns(
                    financial_data['transactions']
                )
                insights.append(spending_insight)
            
            # Analyze savings opportunities
            if financial_data.get('income') and financial_data.get('expenses'):
                savings_insight = await self._analyze_savings_opportunities(
                    financial_data['income'],
                    financial_data['expenses']
                )
                insights.append(savings_insight)
            
            # Generate investment advice
            if user_profile.get('risk_tolerance'):
                investment_insight = await self._generate_investment_advice(
                    user_profile['risk_tolerance'],
                    financial_data.get('investment_portfolio', {})
                )
                insights.append(investment_insight)
            
            # Tax optimization tips
            tax_insight = await self._generate_tax_tips(user_profile, financial_data)
            insights.append(tax_insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate financial insights: {e}")
            return []
    
    async def _analyze_spending_patterns(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Analyze spending patterns and provide insights"""
        try:
            # Group transactions by category
            categories = {}
            total_spent = 0
            
            for transaction in transactions:
                category = transaction.get('category', 'Other')
                amount = abs(transaction.get('amount', 0))
                
                if category not in categories:
                    categories[category] = 0
                categories[category] += amount
                total_spent += amount
            
            # Find top spending categories
            top_categories = sorted(
                categories.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:3]
            
            # Generate insights
            insights = []
            if top_categories:
                top_category, top_amount = top_categories[0]
                top_percentage = (top_amount / total_spent) * 100
                
                if top_percentage > 40:
                    insights.append(f"Your top spending category is {top_category} at {top_percentage:.1f}% of total spending. Consider reviewing this area for potential savings.")
                
                if len(categories) < 5:
                    insights.append("You have a concentrated spending pattern. Consider diversifying your expenses across more categories.")
            
            return {
                "type": "spending_pattern",
                "title": "Spending Pattern Analysis",
                "description": "Analysis of your spending habits and opportunities for optimization",
                "data": {
                    "top_categories": top_categories,
                    "total_spent": total_spent,
                    "category_count": len(categories)
                },
                "insights": insights,
                "priority": "medium"
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze spending patterns: {e}")
            return self._default_insight("spending_pattern")
    
    async def _analyze_savings_opportunities(
        self, 
        income: float, 
        expenses: float
    ) -> Dict[str, Any]:
        """Analyze savings opportunities"""
        try:
            savings_rate = ((income - expenses) / income) * 100 if income > 0 else 0
            
            insights = []
            if savings_rate < 20:
                insights.append("Your savings rate is below the recommended 20%. Consider reviewing your expenses for areas to cut back.")
            elif savings_rate < 30:
                insights.append("Good savings rate! Consider increasing it to 30% for better financial security.")
            else:
                insights.append("Excellent savings rate! You're on track for financial independence.")
            
            return {
                "type": "savings_opportunity",
                "title": "Savings Analysis",
                "description": "Analysis of your savings rate and opportunities for improvement",
                "data": {
                    "income": income,
                    "expenses": expenses,
                    "savings_rate": savings_rate
                },
                "insights": insights,
                "priority": "high" if savings_rate < 20 else "medium"
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze savings opportunities: {e}")
            return self._default_insight("savings_opportunity")
    
    async def _generate_investment_advice(
        self, 
        risk_tolerance: str, 
        portfolio: Dict
    ) -> Dict[str, Any]:
        """Generate personalized investment advice"""
        try:
            risk_levels = {
                "low": "conservative",
                "medium": "moderate", 
                "high": "aggressive"
            }
            
            risk_level = risk_levels.get(risk_tolerance.lower(), "moderate")
            
            advice = {
                "low": "Consider low-risk investments like bonds, CDs, and dividend-paying stocks. Focus on capital preservation.",
                "medium": "A balanced portfolio with 60% stocks and 40% bonds might suit your risk tolerance. Consider index funds for diversification.",
                "high": "You can consider growth stocks, sector ETFs, and alternative investments. Ensure you have a long-term investment horizon."
            }
            
            return {
                "type": "investment_advice",
                "title": "Investment Recommendations",
                "description": f"Personalized investment advice based on your {risk_tolerance} risk tolerance",
                "data": {
                    "risk_tolerance": risk_tolerance,
                    "risk_level": risk_level,
                    "current_portfolio": portfolio
                },
                "insights": [advice.get(risk_level, advice["medium"])],
                "priority": "medium"
            }
            
        except Exception as e:
            logger.error(f"Failed to generate investment advice: {e}")
            return self._default_insight("investment_advice")
    
    async def _generate_tax_tips(
        self, 
        user_profile: Dict, 
        financial_data: Dict
    ) -> Dict[str, Any]:
        """Generate tax optimization tips"""
        try:
            tips = []
            
            # Check for retirement contributions
            if financial_data.get('retirement_contributions', 0) < 6000:
                tips.append("Consider maximizing your IRA contributions to reduce taxable income.")
            
            # Check for health savings account
            if not financial_data.get('hsa_contributions'):
                tips.append("If eligible, consider contributing to an HSA for tax-free medical expenses.")
            
            # Check for charitable donations
            if not financial_data.get('charitable_donations'):
                tips.append("Charitable donations can provide tax deductions. Consider donating to causes you care about.")
            
            return {
                "type": "tax_tips",
                "title": "Tax Optimization Tips",
                "description": "Personalized tax-saving strategies and recommendations",
                "data": {
                    "user_profile": user_profile,
                    "financial_data": financial_data
                },
                "insights": tips,
                "priority": "medium"
            }
            
        except Exception as e:
            logger.error(f"Failed to generate tax tips: {e}")
            return self._default_insight("tax_tips")
    
    def _prepare_context(self, user_context: Optional[Dict]) -> Optional[Dict]:
        """Prepare context for Watson Assistant"""
        if not user_context:
            return None
        
        return {
            "skills": {
                "actions": [
                    {
                        "name": "get_user_profile",
                        "parameters": user_context
                    }
                ]
            }
        }
    
    def _process_watson_response(
        self, 
        response: Dict, 
        original_message: str
    ) -> Dict[str, Any]:
        """Process Watson Assistant response"""
        try:
            output = response.get('output', {})
            generic = output.get('generic', [])
            
            if generic:
                message_text = generic[0].get('text', '')
                response_type = generic[0].get('response_type', 'text')
                
                return {
                    "message": message_text,
                    "response_type": response_type,
                    "confidence": response.get('output', {}).get('confidence', 0.8),
                    "intents": response.get('output', {}).get('intents', []),
                    "entities": response.get('output', {}).get('entities', []),
                    "context": response.get('context', {}),
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                return self._fallback_response(original_message)
                
        except Exception as e:
            logger.error(f"Failed to process Watson response: {e}")
            return self._fallback_response(original_message)
    
    def _fallback_response(self, message: str) -> Dict[str, Any]:
        """Fallback response when Watson is unavailable"""
        # Simple keyword-based responses for common financial questions
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['save', 'saving', 'savings']):
            response = "To improve your savings, try the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings. Start by setting up automatic transfers to a high-yield savings account."
        elif any(word in message_lower for word in ['invest', 'investment', 'portfolio']):
            response = "For investments, consider starting with index funds for diversification. Your allocation should match your risk tolerance and time horizon. Remember to regularly rebalance your portfolio."
        elif any(word in message_lower for word in ['tax', 'taxes', 'deduction']):
            response = "Common tax deductions include retirement contributions, mortgage interest, and charitable donations. Consider consulting a tax professional for personalized advice."
        elif any(word in message_lower for word in ['budget', 'budgeting', 'spend']):
            response = "Create a budget by tracking all income and expenses. Use apps or spreadsheets to monitor your spending. Set realistic goals and review your budget monthly."
        else:
            response = "I'm here to help with your financial questions! You can ask me about saving, investing, taxes, budgeting, or any other financial topics. What would you like to know?"
        
        return {
            "message": response,
            "response_type": "text",
            "confidence": 0.6,
            "intents": [],
            "entities": [],
            "context": {},
            "timestamp": datetime.utcnow().isoformat(),
            "fallback": True
        }
    
    def _default_insight(self, insight_type: str) -> Dict[str, Any]:
        """Default insight when analysis fails"""
        return {
            "type": insight_type,
            "title": f"{insight_type.replace('_', ' ').title()}",
            "description": "Unable to generate specific insights at this time",
            "data": {},
            "insights": ["Please check back later for personalized financial insights."],
            "priority": "low"
        }
    
    async def close_session(self, session_id: str) -> bool:
        """Close Watson Assistant session"""
        try:
            if not self.assistant:
                return False
                
            self.assistant.delete_session(
                assistant_id=self.assistant_id,
                session_id=session_id
            )
            
            logger.info(f"Closed Watson session: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to close Watson session: {e}")
            return False
    
    async def predict_financial_outcomes(
        self, 
        user_data: Dict, 
        prediction_type: str = "spending"
    ) -> Dict[str, Any]:
        """Predict financial outcomes using AI and statistical analysis"""
        try:
            if prediction_type == "spending":
                return await self._predict_spending_patterns(user_data)
            elif prediction_type == "savings":
                return await self._predict_savings_growth(user_data)
            elif prediction_type == "investment":
                return await self._predict_investment_returns(user_data)
            else:
                return {"error": f"Unknown prediction type: {prediction_type}"}
                
        except Exception as e:
            logger.error(f"Financial prediction failed: {e}")
            return {"error": f"Prediction failed: {str(e)}"}
    
    async def _predict_spending_patterns(self, user_data: Dict) -> Dict[str, Any]:
        """Predict future spending patterns using statistical analysis"""
        try:
            transactions = user_data.get('transactions', [])
            if len(transactions) < 10:
                return {"error": "Insufficient transaction data for prediction"}
            
            # Extract spending data
            spending_data = []
            for transaction in transactions:
                if transaction.get('amount', 0) < 0:  # Negative amounts are expenses
                    spending_data.append({
                        'amount': abs(transaction.get('amount', 0)),
                        'category': transaction.get('category', 'Other'),
                        'date': transaction.get('date', datetime.now())
                    })
            
            if not spending_data:
                return {"error": "No spending data found"}
            
            # Calculate spending statistics
            amounts = [item['amount'] for item in spending_data]
            mean_spending = np.mean(amounts)
            std_spending = np.std(amounts)
            
            # Predict next month's spending
            predicted_spending = mean_spending * 1.02  # 2% monthly growth assumption
            
            # Calculate confidence intervals
            confidence_95 = 1.96 * std_spending / np.sqrt(len(amounts))
            
            # Category-based predictions
            category_spending = {}
            for item in spending_data:
                category = item['category']
                if category not in category_spending:
                    category_spending[category] = []
                category_spending[category].append(item['amount'])
            
            category_predictions = {}
            for category, amounts_list in category_spending.items():
                if len(amounts_list) >= 3:
                    category_predictions[category] = {
                        'predicted': np.mean(amounts_list) * 1.02,
                        'confidence': min(0.95, 1.0 - (std_spending / mean_spending))
                    }
            
            return {
                "prediction_type": "spending_patterns",
                "next_month_prediction": float(predicted_spending),
                "confidence_interval": {
                    "lower": float(predicted_spending - confidence_95),
                    "upper": float(predicted_spending + confidence_95),
                    "confidence_level": 0.95
                },
                "category_predictions": category_predictions,
                "statistics": {
                    "mean_monthly_spending": float(mean_spending),
                    "spending_volatility": float(std_spending),
                    "data_points": len(spending_data)
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Spending prediction failed: {e}")
            return {"error": f"Spending prediction failed: {str(e)}"}
    
    async def _predict_savings_growth(self, user_data: Dict) -> Dict[str, Any]:
        """Predict savings growth over time"""
        try:
            current_savings = user_data.get('current_savings', 0)
            monthly_contribution = user_data.get('monthly_contribution', 0)
            annual_return_rate = user_data.get('expected_return_rate', 0.07)  # 7% default
            
            if current_savings <= 0 and monthly_contribution <= 0:
                return {"error": "Insufficient savings data for prediction"}
            
            # Calculate future savings for different time periods
            time_periods = [1, 3, 5, 10, 20]  # years
            predictions = {}
            
            for years in time_periods:
                months = years * 12
                monthly_rate = annual_return_rate / 12
                
                # Future value formula: FV = PV(1+r)^n + PMT * ((1+r)^n - 1) / r
                future_value = current_savings * (1 + monthly_rate) ** months
                if monthly_contribution > 0:
                    future_value += monthly_contribution * ((1 + monthly_rate) ** months - 1) / monthly_rate
                
                predictions[f"{years}_years"] = {
                    "future_value": float(future_value),
                    "total_contributions": float(monthly_contribution * months),
                    "interest_earned": float(future_value - current_savings - (monthly_contribution * months)),
                    "growth_multiplier": float(future_value / current_savings) if current_savings > 0 else float('inf')
                }
            
            return {
                "prediction_type": "savings_growth",
                "current_savings": float(current_savings),
                "monthly_contribution": float(monthly_contribution),
                "expected_annual_return": float(annual_return_rate),
                "predictions": predictions,
                "recommendations": self._generate_savings_recommendations(current_savings, monthly_contribution),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Savings prediction failed: {e}")
            return {"error": f"Savings prediction failed: {str(e)}"}
    
    def _generate_savings_recommendations(self, current_savings: float, monthly_contribution: float) -> List[str]:
        """Generate personalized savings recommendations"""
        recommendations = []
        
        # Emergency fund recommendations
        if current_savings < 5000:
            recommendations.append("Build an emergency fund of at least $5,000 for unexpected expenses")
        
        # Contribution recommendations
        if monthly_contribution < 500:
            recommendations.append("Consider increasing monthly savings to at least $500 for better financial security")
        elif monthly_contribution < 1000:
            recommendations.append("Great savings rate! Consider increasing to $1,000 monthly for faster goal achievement")
        
        # Investment recommendations
        if current_savings > 10000 and monthly_contribution > 500:
            recommendations.append("Consider investing excess savings in index funds for long-term growth")
        
        return recommendations
    
    async def _predict_investment_returns(self, user_data: Dict) -> Dict[str, Any]:
        """Predict investment returns based on portfolio and market conditions"""
        try:
            portfolio = user_data.get('portfolio', {})
            risk_tolerance = user_data.get('profile', {}).get('risk_tolerance', 'moderate')
            
            if not portfolio:
                return {"error": "No portfolio data available for prediction"}
            
            # Risk-adjusted return expectations
            risk_returns = {
                'conservative': {'expected_return': 0.05, 'volatility': 0.08},
                'moderate': {'expected_return': 0.08, 'volatility': 0.15},
                'aggressive': {'expected_return': 0.12, 'volatility': 0.25}
            }
            
            risk_profile = risk_returns.get(risk_tolerance.lower(), risk_returns['moderate'])
            expected_return = risk_profile['expected_return']
            volatility = risk_profile['volatility']
            
            # Calculate portfolio-weighted expected return
            total_value = sum(asset.get('value', 0) for asset in portfolio.get('assets', []))
            if total_value <= 0:
                return {"error": "Invalid portfolio values"}
            
            weighted_return = 0
            for asset in portfolio.get('assets', []):
                asset_value = asset.get('value', 0)
                asset_weight = asset_value / total_value
                asset_return = asset.get('expected_return', expected_return)
                weighted_return += asset_weight * asset_return
            
            # Generate return predictions for different time periods
            time_periods = [1, 3, 5, 10]  # years
            return_predictions = {}
            
            for years in time_periods:
                # Simple compound growth with volatility
                expected_value = total_value * (1 + weighted_return) ** years
                
                # Monte Carlo simulation approximation (simplified)
                volatility_impact = total_value * volatility * np.sqrt(years) * 0.5
                
                return_predictions[f"{years}_years"] = {
                    "expected_value": float(expected_value),
                    "expected_return": float(weighted_return * years),
                    "volatility_range": {
                        "lower": float(expected_value - volatility_impact),
                        "upper": float(expected_value + volatility_impact)
                    },
                    "confidence_level": 0.68  # 1 standard deviation
                }
            
            return {
                "prediction_type": "investment_returns",
                "current_portfolio_value": float(total_value),
                "expected_annual_return": float(weighted_return),
                "risk_tolerance": risk_tolerance,
                "return_predictions": return_predictions,
                "risk_metrics": {
                    "volatility": float(volatility),
                    "sharpe_ratio": float(weighted_return / volatility) if volatility > 0 else 0,
                    "max_drawdown_estimate": float(volatility * 2)  # Rough estimate
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Investment prediction failed: {e}")
            return {"error": f"Investment prediction failed: {str(e)}"}
    
    async def generate_ai_insights(self, user_data: Dict) -> List[Dict[str, Any]]:
        """Generate AI-powered financial insights and recommendations"""
        try:
            insights = []
            
            # Analyze spending patterns
            if user_data.get('transactions'):
                spending_insight = await self._generate_ai_spending_insight(user_data['transactions'])
                insights.append(spending_insight)
            
            # Analyze savings behavior
            if user_data.get('income') and user_data.get('expenses'):
                savings_insight = await self._generate_ai_savings_insight(
                    user_data['income'], 
                    user_data['expenses']
                )
                insights.append(savings_insight)
            
            # Generate personalized recommendations
            if user_data.get('profile'):
                personalized_insight = await self._generate_personalized_ai_insight(user_data['profile'])
                insights.append(personalized_insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"AI insights generation failed: {e}")
            return []
    
    async def _generate_ai_spending_insight(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Generate AI-powered spending insights"""
        try:
            # Analyze spending patterns
            categories = {}
            total_spent = 0
            
            for transaction in transactions:
                if transaction.get('amount', 0) < 0:  # Expenses
                    category = transaction.get('category', 'Other')
                    amount = abs(transaction.get('amount', 0))
                    
                    if category not in categories:
                        categories[category] = 0
                    categories[category] += amount
                    total_spent += amount
            
            if not categories:
                return {"error": "No spending data available"}
            
            # Find insights
            top_category = max(categories.items(), key=lambda x: x[1])
            top_percentage = (top_category[1] / total_spent) * 100
            
            insights = []
            if top_percentage > 40:
                insights.append(f"Your top spending category '{top_category[0]}' represents {top_percentage:.1f}% of total spending. Consider diversifying expenses.")
            
            if len(categories) < 5:
                insights.append("Your spending is concentrated in few categories. Consider diversifying for better financial health.")
            
            return {
                "type": "ai_spending_insight",
                "title": "AI-Powered Spending Analysis",
                "description": "Advanced analysis of your spending patterns using AI algorithms",
                "insights": insights,
                "data": {
                    "total_spent": float(total_spent),
                    "category_count": len(categories),
                    "top_category": top_category[0],
                    "top_percentage": float(top_percentage)
                },
                "priority": "high" if top_percentage > 40 else "medium",
                "ai_generated": True
            }
            
        except Exception as e:
            logger.error(f"AI spending insight generation failed: {e}")
            return {"error": f"AI insight generation failed: {str(e)}"}
    
    async def _generate_ai_savings_insight(self, income: float, expenses: float) -> Dict[str, Any]:
        """Generate AI-powered savings insights"""
        try:
            savings_rate = ((income - expenses) / income) * 100 if income > 0 else 0
            
            insights = []
            if savings_rate < 20:
                insights.append("Your savings rate is below the recommended 20%. AI analysis suggests reviewing expenses for optimization opportunities.")
            elif savings_rate < 30:
                insights.append("Good savings rate! AI suggests increasing to 30% for better financial security and faster goal achievement.")
            else:
                insights.append("Excellent savings rate! AI recommends considering investment opportunities for excess savings.")
            
            return {
                "type": "ai_savings_insight",
                "title": "AI-Powered Savings Analysis",
                "description": "Intelligent analysis of your savings behavior and optimization opportunities",
                "insights": insights,
                "data": {
                    "income": float(income),
                    "expenses": float(expenses),
                    "savings_rate": float(savings_rate),
                    "recommended_rate": 20.0
                },
                "priority": "high" if savings_rate < 20 else "medium",
                "ai_generated": True
            }
            
        except Exception as e:
            logger.error(f"AI savings insight generation failed: {e}")
            return {"error": f"AI insight generation failed: {str(e)}"}
    
    async def _generate_personalized_ai_insight(self, profile: Dict) -> Dict[str, Any]:
        """Generate personalized AI insights based on user profile"""
        try:
            age = profile.get('age', 30)
            risk_tolerance = profile.get('risk_tolerance', 'moderate')
            income_level = profile.get('income_level', 'medium')
            
            insights = []
            
            # Age-based insights
            if age < 30:
                insights.append("AI analysis shows you have time advantage for compound growth. Consider starting investments early.")
            elif age > 50:
                insights.append("AI recommends focusing on capital preservation while maintaining growth as you approach retirement.")
            
            # Risk tolerance insights
            if risk_tolerance == 'conservative':
                insights.append("Your conservative approach is suitable for capital preservation. AI suggests laddering CDs for steady returns.")
            elif risk_tolerance == 'aggressive':
                insights.append("Your aggressive approach can maximize returns. AI recommends ensuring long-term horizon and emergency fund.")
            
            # Income level insights
            if income_level == 'low':
                insights.append("AI suggests starting small and building gradually. Every dollar saved counts towards financial goals.")
            elif income_level == 'high':
                insights.append("AI identifies great opportunities for wealth building with your income level. Consider tax optimization strategies.")
            
            return {
                "type": "personalized_ai_insight",
                "title": "Personalized AI Financial Guidance",
                "description": "AI-generated insights tailored to your specific financial profile and circumstances",
                "insights": insights,
                "data": {
                    "age": age,
                    "risk_tolerance": risk_tolerance,
                    "income_level": income_level
                },
                "priority": "high",
                "ai_generated": True,
                "personalized": True
            }
            
        except Exception as e:
            logger.error(f"Personalized AI insight generation failed: {e}")
            return {"error": f"Personalized insight generation failed: {str(e)}"}

    async def _enhance_response_with_ai(
        self, 
        base_response: Dict, 
        original_message: str, 
        user_context: Optional[Dict]
    ) -> Dict[str, Any]:
        """Enhance Watson response with AI-powered insights"""
        try:
            enhanced = base_response.copy()
            
            # Add sentiment analysis
            sentiment = await self.analyze_sentiment(original_message)
            enhanced["sentiment"] = sentiment
            
            # Add financial insights if relevant
            if self._is_financial_question(original_message):
                insights = await self._generate_contextual_insights(
                    original_message, user_context
                )
                enhanced["financial_insights"] = insights
            
            # Add market context if relevant
            if self._is_market_question(original_message):
                market_data = await self._get_relevant_market_data(original_message)
                enhanced["market_context"] = market_data
            
            # Add personalized recommendations
            if user_context:
                recommendations = await self._generate_personalized_recommendations(
                    original_message, user_context
                )
                enhanced["personalized_recommendations"] = recommendations
            
            return enhanced
            
        except Exception as e:
            logger.error(f"Failed to enhance response: {e}")
            return base_response
    
    async def _enhanced_fallback_response(
        self, 
        message: str, 
        user_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Enhanced fallback response with AI capabilities"""
        try:
            # Use advanced keyword analysis
            response_data = await self._analyze_message_intent(message)
            
            # Generate contextual response
            if user_context:
                response_data = await self._personalize_response(
                    response_data, user_context
                )
            
            return {
                "message": response_data["response"],
                "response_type": "text",
                "confidence": response_data["confidence"],
                "intents": response_data["intents"],
                "entities": response_data["entities"],
                "context": user_context or {},
                "timestamp": datetime.utcnow().isoformat(),
                "fallback": True,
                "ai_enhanced": True
            }
            
        except Exception as e:
            logger.error(f"Failed to generate enhanced fallback: {e}")
            return self._fallback_response(message)
    
    async def _analyze_message_intent(self, message: str) -> Dict[str, Any]:
        """Advanced intent analysis using NLP and financial knowledge"""
        message_lower = message.lower()
        
        # Financial categories and their keywords
        categories = {
            "savings": ["save", "saving", "savings", "emergency fund", "nest egg"],
            "investment": ["invest", "investment", "portfolio", "stocks", "bonds", "etf"],
            "budgeting": ["budget", "budgeting", "spend", "expense", "track"],
            "debt": ["debt", "credit", "loan", "pay off", "consolidate"],
            "retirement": ["retirement", "401k", "ira", "pension", "social security"],
            "taxes": ["tax", "taxes", "deduction", "refund", "filing"],
            "insurance": ["insurance", "coverage", "policy", "protect"],
            "real_estate": ["house", "home", "mortgage", "down payment", "real estate"]
        }
        
        # Find matching categories
        matched_categories = []
        for category, keywords in categories.items():
            if any(keyword in message_lower for keyword in keywords):
                matched_categories.append(category)
        
        # Generate contextual response
        response = await self._generate_category_response(matched_categories, message)
        
        return {
            "response": response,
            "confidence": 0.8 if matched_categories else 0.6,
            "intents": matched_categories,
            "entities": [],
            "categories": matched_categories
        }
    
    async def _generate_category_response(
        self, 
        categories: List[str], 
        message: str
    ) -> str:
        """Generate intelligent responses based on financial categories"""
        if not categories:
            return "I'm here to help with your financial questions! You can ask me about saving, investing, budgeting, debt management, retirement planning, taxes, insurance, or real estate. What would you like to know?"
        
        # Get the primary category
        primary_category = categories[0]
        
        responses = {
            "savings": "Great question about savings! Let me help you create a personalized savings strategy. What are you saving for - emergency fund, vacation, down payment, or retirement?",
            "investment": "Excellent! Investment planning is crucial for building wealth. I can help you understand different investment options based on your risk tolerance and goals. What's your investment timeline?",
            "budgeting": "Smart thinking! Budgeting is the foundation of financial success. I can help you create a budget that works for your lifestyle. What's your current monthly income?",
            "debt": "Debt management is important for financial health. I can help you create a debt payoff strategy. What types of debt do you currently have?",
            "retirement": "Retirement planning is essential! The earlier you start, the better. I can help you calculate how much you need and create a savings plan. How old are you?",
            "taxes": "Tax optimization can save you money! I can help you identify deductions and strategies. What's your filing status and income level?",
            "insurance": "Insurance protects your financial future. I can help you assess your coverage needs. What types of insurance are you considering?",
            "real_estate": "Real estate can be a great investment! I can help you understand the costs and benefits. Are you looking to buy, sell, or invest in real estate?"
        }
        
        base_response = responses.get(primary_category, responses["savings"])
        
        # Add personalized elements if possible
        if "how much" in message.lower() or "calculate" in message.lower():
            base_response += " I can help you calculate the specific amounts you need. Would you like me to walk you through the calculations?"
        
        return base_response
    
    async def _personalize_response(
        self, 
        response_data: Dict, 
        user_context: Dict
    ) -> Dict[str, Any]:
        """Personalize response based on user context"""
        try:
            personalized = response_data.copy()
            
            # Add user-specific information
            if user_context.get("risk_tolerance"):
                risk_level = user_context["risk_tolerance"]
                personalized["risk_context"] = f"Based on your {risk_level} risk tolerance, "
            
            if user_context.get("age"):
                age = user_context["age"]
                if age < 30:
                    personalized["age_context"] = "Since you're young, you have time on your side for compound growth. "
                elif age < 50:
                    personalized["age_context"] = "You're in your prime earning years - great time to maximize savings. "
                else:
                    personalized["age_context"] = "Focus on preserving capital while maintaining growth. "
            
            if user_context.get("income_level"):
                income = user_context["income_level"]
                if income == "low":
                    personalized["income_context"] = "Start small and build gradually. Every dollar saved counts! "
                elif income == "high":
                    personalized["income_context"] = "With higher income, you have great opportunities for wealth building. "
            
            return personalized
            
        except Exception as e:
            logger.error(f"Failed to personalize response: {e}")
            return response_data
    
    def _is_financial_question(self, message: str) -> bool:
        """Check if message is a financial question"""
        financial_keywords = [
            "money", "finance", "invest", "save", "budget", "debt", "credit",
            "loan", "retirement", "tax", "insurance", "mortgage", "stock",
            "bond", "portfolio", "wealth", "income", "expense"
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in financial_keywords)
    
    def _is_market_question(self, message: str) -> bool:
        """Check if message is about market conditions"""
        market_keywords = [
            "market", "stock market", "economy", "recession", "inflation",
            "interest rate", "fed", "trading", "bull market", "bear market"
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in market_keywords)
    
    async def _get_relevant_market_data(self, message: str) -> Dict[str, Any]:
        """Get relevant market data for market-related questions"""
        try:
            # This would integrate with real market data APIs
            # For now, return mock data
            return {
                "market_status": "Bull Market",
                "sp500_change": "+0.5%",
                "nasdaq_change": "+0.8%",
                "treasury_yield": "4.2%",
                "inflation_rate": "3.1%",
                "fed_rate": "5.25%"
            }
        except Exception as e:
            logger.error(f"Failed to get market data: {e}")
            return {}
    
    async def _generate_contextual_insights(
        self, 
        message: str, 
        user_context: Optional[Dict]
    ) -> List[Dict[str, Any]]:
        """Generate contextual financial insights"""
        try:
            insights = []
            
            # Add general financial insights
            insights.append({
                "type": "general",
                "title": "Financial Wellness Tip",
                "description": "Regular financial check-ins help you stay on track with your goals.",
                "priority": "medium"
            })
            
            # Add personalized insights if user context available
            if user_context:
                if user_context.get("risk_tolerance"):
                    risk_insight = await self._generate_risk_based_insight(
                        user_context["risk_tolerance"]
                    )
                    insights.append(risk_insight)
                
                if user_context.get("age"):
                    age_insight = await self._generate_age_based_insight(
                        user_context["age"]
                    )
                    insights.append(age_insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate contextual insights: {e}")
            return []
    
    async def _generate_risk_based_insight(self, risk_tolerance: str) -> Dict[str, Any]:
        """Generate insight based on user's risk tolerance"""
        insights = {
            "conservative": {
                "title": "Conservative Strategy Insight",
                "description": "Your conservative approach focuses on capital preservation. Consider laddering CDs for steady returns.",
                "priority": "high"
            },
            "moderate": {
                "title": "Balanced Approach Insight", 
                "description": "Your moderate risk tolerance allows for growth while maintaining stability. Consider target-date funds.",
                "priority": "medium"
            },
            "aggressive": {
                "title": "Growth Strategy Insight",
                "description": "Your aggressive approach can maximize returns. Ensure you have a long-term horizon and emergency fund.",
                "priority": "medium"
            }
        }
        
        return insights.get(risk_tolerance.lower(), insights["moderate"])
    
    async def _generate_age_based_insight(self, age: int) -> Dict[str, Any]:
        """Generate insight based on user's age"""
        if age < 30:
            return {
                "title": "Early Career Insight",
                "description": "Time is your biggest asset! Start investing early to benefit from compound growth.",
                "priority": "high"
            }
        elif age < 50:
            return {
                "title": "Mid-Career Insight",
                "description": "Focus on maximizing retirement contributions and building multiple income streams.",
                "priority": "high"
            }
        else:
            return {
                "title": "Pre-Retirement Insight", 
                "description": "Consider reducing risk and focusing on income-generating investments.",
                "priority": "high"
            }
    
    async def _generate_personalized_recommendations(
        self, 
        message: str, 
        user_context: Dict
    ) -> List[Dict[str, Any]]:
        """Generate personalized financial recommendations"""
        try:
            recommendations = []
            
            # Risk-based recommendations
            if user_context.get("risk_tolerance"):
                risk_recs = await self._get_risk_based_recommendations(
                    user_context["risk_tolerance"]
                )
                recommendations.extend(risk_recs)
            
            # Age-based recommendations
            if user_context.get("age"):
                age_recs = await self._get_age_based_recommendations(
                    user_context["age"]
                )
                recommendations.extend(age_recs)
            
            # Income-based recommendations
            if user_context.get("income_level"):
                income_recs = await self._get_income_based_recommendations(
                    user_context["income_level"]
                )
                recommendations.extend(income_recs)
            
            return recommendations[:3]  # Limit to top 3
            
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            return []
    
    async def _get_risk_based_recommendations(self, risk_tolerance: str) -> List[Dict[str, Any]]:
        """Get recommendations based on risk tolerance"""
        recommendations = {
            "conservative": [
                {"type": "investment", "title": "High-Yield Savings", "description": "Consider online banks for better rates"},
                {"type": "debt", "title": "Emergency Fund", "description": "Build 6 months of expenses in liquid savings"}
            ],
            "moderate": [
                {"type": "investment", "title": "Index Fund Portfolio", "description": "60% stocks, 30% bonds, 10% alternatives"},
                {"type": "retirement", "title": "Maximize 401(k)", "description": "Contribute up to employer match"}
            ],
            "aggressive": [
                {"type": "investment", "title": "Growth Portfolio", "description": "80% stocks, 15% bonds, 5% alternatives"},
                {"type": "education", "title": "Financial Education", "description": "Learn about advanced investment strategies"}
            ]
        }
        
        return recommendations.get(risk_tolerance.lower(), recommendations["moderate"])
    
    async def _get_age_based_recommendations(self, age: int) -> List[Dict[str, Any]]:
        """Get recommendations based on age"""
        if age < 30:
            return [
                {"type": "investment", "title": "Start Early", "description": "Begin with Roth IRA contributions"},
                {"type": "education", "title": "Financial Literacy", "description": "Learn about investing and budgeting"}
            ]
        elif age < 50:
            return [
                {"type": "retirement", "title": "Catch-up Contributions", "description": "Use catch-up contributions if over 50"},
                {"type": "insurance", "title": "Life Insurance", "description": "Ensure adequate coverage for dependents"}
            ]
        else:
            return [
                {"type": "retirement", "title": "Income Planning", "description": "Focus on income-generating investments"},
                {"type": "estate", "title": "Estate Planning", "description": "Review wills and beneficiary designations"}
            ]
    
    async def _get_income_based_recommendations(self, income_level: str) -> List[Dict[str, Any]]:
        """Get recommendations based on income level"""
        recommendations = {
            "low": [
                {"type": "budgeting", "title": "Zero-Based Budget", "description": "Track every dollar to maximize savings"},
                {"type": "debt", "title": "Debt Snowball", "description": "Focus on paying off high-interest debt first"}
            ],
            "medium": [
                {"type": "savings", "title": "Automated Savings", "description": "Set up automatic transfers to savings"},
                {"type": "investment", "title": "Diversified Portfolio", "description": "Start with index funds and ETFs"}
            ],
            "high": [
                {"type": "tax", "title": "Tax Optimization", "description": "Maximize tax-advantaged accounts"},
                {"type": "estate", "title": "Wealth Preservation", "description": "Consider trusts and estate planning"}
            ]
        }
        
        return recommendations.get(income_level.lower(), recommendations["medium"])
