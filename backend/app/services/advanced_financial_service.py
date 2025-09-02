"""
Advanced Financial Service with AI/ML Capabilities
Provides sophisticated financial analysis, predictions, and insights
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import yfinance as yf
import pandas_ta as ta
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

logger = logging.getLogger(__name__)

class AdvancedFinancialService:
    """Advanced financial analysis service with AI/ML capabilities"""
    
    def __init__(self):
        """Initialize the advanced financial service"""
        try:
            # Initialize ML models
            self.spending_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
            self.risk_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            self.anomaly_detector = RandomForestClassifier(n_estimators=50, random_state=42)
            
            # Data preprocessing
            self.scaler = StandardScaler()
            self.label_encoder = LabelEncoder()
            
            # Market data cache
            self.market_cache = {}
            self.cache_expiry = {}
            
            # Financial indicators
            self.technical_indicators = [
                'sma', 'ema', 'rsi', 'macd', 'bollinger_hbands', 'bollinger_lbands',
                'stoch', 'williams_r', 'cci', 'adx'
            ]
            
            logger.info("Advanced Financial Service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Advanced Financial Service: {e}")
    
    async def analyze_portfolio_risk(
        self, 
        portfolio_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze portfolio risk using modern financial metrics"""
        try:
            # Extract portfolio components
            assets = portfolio_data.get('assets', [])
            if not assets:
                return {"error": "No portfolio data provided"}
            
            # Calculate modern risk metrics
            risk_metrics = await self._calculate_risk_metrics(assets)
            
            # Portfolio optimization suggestions
            optimization = await self._suggest_portfolio_optimization(assets, risk_metrics)
            
            # Stress testing
            stress_test = await self._perform_stress_test(assets, risk_metrics)
            
            return {
                "risk_metrics": risk_metrics,
                "optimization_suggestions": optimization,
                "stress_test_results": stress_test,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Portfolio risk analysis failed: {e}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    async def _calculate_risk_metrics(self, assets: List[Dict]) -> Dict[str, Any]:
        """Calculate comprehensive risk metrics"""
        try:
            # Extract returns and weights
            returns_data = []
            weights = []
            
            for asset in assets:
                if asset.get('returns') and asset.get('weight'):
                    returns_data.append(asset['returns'])
                    weights.append(asset['weight'])
            
            if not returns_data:
                return {"error": "Insufficient data for risk calculation"}
            
            # Convert to numpy arrays
            returns_array = np.array(returns_data)
            weights_array = np.array(weights)
            
            # Calculate risk metrics
            portfolio_return = np.sum(returns_array * weights_array)
            portfolio_volatility = np.sqrt(
                np.dot(weights_array.T, np.dot(np.cov(returns_array), weights_array))
            )
            
            # Sharpe ratio (assuming risk-free rate of 2%)
            risk_free_rate = 0.02
            sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility if portfolio_volatility > 0 else 0
            
            # Value at Risk (VaR) - 95% confidence
            portfolio_returns = np.sum(returns_array * weights_array, axis=0)
            var_95 = np.percentile(portfolio_returns, 5)
            
            # Maximum drawdown
            cumulative_returns = np.cumprod(1 + portfolio_returns)
            running_max = np.maximum.accumulate(cumulative_returns)
            drawdown = (cumulative_returns - running_max) / running_max
            max_drawdown = np.min(drawdown)
            
            # Beta calculation (if market data available)
            beta = await self._calculate_portfolio_beta(returns_array, weights_array)
            
            return {
                "portfolio_return": float(portfolio_return),
                "portfolio_volatility": float(portfolio_volatility),
                "sharpe_ratio": float(sharpe_ratio),
                "var_95": float(var_95),
                "max_drawdown": float(max_drawdown),
                "beta": float(beta),
                "diversification_score": self._calculate_diversification_score(assets)
            }
            
        except Exception as e:
            logger.error(f"Risk metrics calculation failed: {e}")
            return {"error": f"Risk calculation failed: {str(e)}"}
    
    async def _calculate_portfolio_beta(
        self, 
        returns_array: np.ndarray, 
        weights_array: np.ndarray
    ) -> float:
        """Calculate portfolio beta relative to market"""
        try:
            # This would typically use market data (e.g., S&P 500)
            # For now, return a default value
            return 1.0
        except Exception as e:
            logger.error(f"Beta calculation failed: {e}")
            return 1.0
    
    def _calculate_diversification_score(self, assets: List[Dict]) -> float:
        """Calculate portfolio diversification score"""
        try:
            if len(assets) < 2:
                return 0.0
            
            # Calculate Herfindahl-Hirschman Index (HHI)
            weights = [asset.get('weight', 0) for asset in assets]
            hhi = sum(w**2 for w in weights)
            
            # Convert to diversification score (0-100)
            # Lower HHI = more diversified
            diversification_score = max(0, 100 - (hhi * 100))
            
            return round(diversification_score, 2)
            
        except Exception as e:
            logger.error(f"Diversification score calculation failed: {e}")
            return 50.0
    
    async def predict_spending_patterns(
        self, 
        historical_data: List[Dict],
        user_profile: Dict
    ) -> Dict[str, Any]:
        """Predict future spending patterns using ML"""
        try:
            if len(historical_data) < 30:  # Need sufficient data
                return {"error": "Insufficient historical data for prediction"}
            
            # Prepare features for ML model
            features = await self._extract_spending_features(historical_data, user_profile)
            
            # Train model if we have enough data
            if len(features) > 50:
                predictions = await self._train_and_predict_spending(features)
            else:
                predictions = await self._simple_spending_forecast(historical_data)
            
            # Generate insights
            insights = await self._generate_spending_insights(predictions, historical_data)
            
            return {
                "predictions": predictions,
                "insights": insights,
                "confidence": 0.85 if len(features) > 50 else 0.70,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Spending prediction failed: {e}")
            return {"error": f"Prediction failed: {str(e)}"}
    
    async def _extract_spending_features(
        self, 
        historical_data: List[Dict], 
        user_profile: Dict
    ) -> List[Dict]:
        """Extract features for ML model from spending data"""
        try:
            features = []
            
            for i, transaction in enumerate(historical_data):
                if i < 7:  # Skip first week
                    continue
                
                # Get previous week's data
                prev_week = historical_data[max(0, i-7):i]
                
                feature_vector = {
                    'day_of_week': transaction.get('date', datetime.now()).weekday(),
                    'day_of_month': transaction.get('date', datetime.now()).day,
                    'month': transaction.get('date', datetime.now()).month,
                    'is_weekend': transaction.get('date', datetime.now()).weekday() >= 5,
                    'prev_week_total': sum(t.get('amount', 0) for t in prev_week),
                    'prev_week_count': len(prev_week),
                    'category_encoded': hash(transaction.get('category', 'other')) % 100,
                    'amount': abs(transaction.get('amount', 0)),
                    'income_level': self._encode_income_level(user_profile.get('income_level', 'medium')),
                    'age_group': self._encode_age_group(user_profile.get('age', 30))
                }
                
                features.append(feature_vector)
            
            return features
            
        except Exception as e:
            logger.error(f"Feature extraction failed: {e}")
            return []
    
    def _encode_income_level(self, income_level: str) -> int:
        """Encode income level for ML model"""
        encoding = {'low': 0, 'medium': 1, 'high': 2}
        return encoding.get(income_level.lower(), 1)
    
    def _encode_age_group(self, age: int) -> int:
        """Encode age group for ML model"""
        if age < 25:
            return 0
        elif age < 35:
            return 1
        elif age < 50:
            return 2
        else:
            return 3
    
    async def _train_and_predict_spending(
        self, 
        features: List[Dict]
    ) -> Dict[str, Any]:
        """Train ML model and make predictions"""
        try:
            # Prepare data
            X = []
            y = []
            
            for i, feature in enumerate(features[:-1]):  # Use all but last for training
                X.append([v for k, v in feature.items() if k != 'amount'])
                y.append(feature['amount'])
            
            # Train model
            X_array = np.array(X)
            y_array = np.array(y)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X_array)
            
            # Train model
            self.spending_predictor.fit(X_scaled, y_array)
            
            # Make prediction for next period
            last_features = [v for k, v in features[-1].items() if k != 'amount']
            last_features_scaled = self.scaler.transform([last_features])
            
            predicted_amount = self.spending_predictor.predict(last_features_scaled)[0]
            
            return {
                "next_period_prediction": float(predicted_amount),
                "model_accuracy": float(self.spending_predictor.score(X_scaled, y_array)),
                "prediction_interval": self._calculate_prediction_interval(X_scaled, y_array, last_features_scaled)
            }
            
        except Exception as e:
            logger.error(f"ML training and prediction failed: {e}")
            return {"error": f"ML prediction failed: {str(e)}"}
    
    def _calculate_prediction_interval(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray, 
        X_pred: np.ndarray
    ) -> Dict[str, float]:
        """Calculate prediction interval for uncertainty quantification"""
        try:
            # Simple approach: use standard error of prediction
            y_pred = self.spending_predictor.predict(X_train)
            residuals = y_train - y_pred
            mse = np.mean(residuals**2)
            
            # 95% prediction interval
            std_error = np.sqrt(mse)
            interval_95 = 1.96 * std_error
            
            return {
                "lower_bound": float(y_pred[0] - interval_95),
                "upper_bound": float(y_pred[0] + interval_95),
                "confidence_level": 0.95
            }
            
        except Exception as e:
            logger.error(f"Prediction interval calculation failed: {e}")
            return {"lower_bound": 0, "upper_bound": 0, "confidence_level": 0.95}
    
    async def _simple_spending_forecast(
        self, 
        historical_data: List[Dict]
    ) -> Dict[str, Any]:
        """Simple forecasting when insufficient data for ML"""
        try:
            # Calculate moving average
            amounts = [abs(t.get('amount', 0)) for t in historical_data[-7:]]  # Last week
            moving_avg = np.mean(amounts)
            
            # Add seasonal adjustment
            current_month = datetime.now().month
            seasonal_factor = self._get_seasonal_factor(current_month)
            
            forecast = moving_avg * seasonal_factor
            
            return {
                "next_period_prediction": float(forecast),
                "method": "moving_average_with_seasonal_adjustment",
                "confidence": 0.70
            }
            
        except Exception as e:
            logger.error(f"Simple forecast failed: {e}")
            return {"error": f"Simple forecast failed: {str(e)}"}
    
    def _get_seasonal_factor(self, month: int) -> float:
        """Get seasonal adjustment factor for spending"""
        # Simple seasonal factors (could be more sophisticated)
        seasonal_factors = {
            1: 1.1,   # January - New Year spending
            2: 0.9,   # February - Post-holiday lull
            3: 1.0,   # March - Normal
            4: 1.0,   # April - Normal
            5: 1.0,   # May - Normal
            6: 1.0,   # June - Normal
            7: 1.0,   # July - Normal
            8: 1.0,   # August - Normal
            9: 1.0,   # September - Normal
            10: 1.0,  # October - Normal
            11: 1.2,  # November - Holiday preparation
            12: 1.3   # December - Holiday spending
        }
        
        return seasonal_factors.get(month, 1.0)
    
    async def generate_financial_insights(
        self, 
        user_data: Dict,
        market_data: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Generate comprehensive financial insights"""
        try:
            insights = []
            
            # Spending analysis
            if user_data.get('transactions'):
                spending_insights = await self._analyze_spending_behavior(
                    user_data['transactions']
                )
                insights.extend(spending_insights)
            
            # Savings analysis
            if user_data.get('income') and user_data.get('expenses'):
                savings_insights = await self._analyze_savings_opportunities(
                    user_data['income'],
                    user_data['expenses']
                )
                insights.extend(savings_insights)
            
            # Investment analysis
            if user_data.get('portfolio'):
                investment_insights = await self._analyze_investment_strategy(
                    user_data['portfolio'],
                    user_data.get('profile', {})
                )
                insights.extend(investment_insights)
            
            # Market context
            if market_data:
                market_insights = await self._analyze_market_context(market_data)
                insights.extend(market_insights)
            
            # Sort by priority and return top insights
            insights.sort(key=lambda x: x.get('priority_score', 0), reverse=True)
            return insights[:5]  # Return top 5 insights
            
        except Exception as e:
            logger.error(f"Financial insights generation failed: {e}")
            return []
    
    async def _analyze_spending_behavior(
        self, 
        transactions: List[Dict]
    ) -> List[Dict[str, Any]]:
        """Analyze spending behavior patterns"""
        try:
            insights = []
            
            # Categorize transactions
            categories = {}
            for transaction in transactions:
                category = transaction.get('category', 'Other')
                amount = abs(transaction.get('amount', 0))
                
                if category not in categories:
                    categories[category] = {'total': 0, 'count': 0}
                
                categories[category]['total'] += amount
                categories[category]['count'] += 1
            
            # Find top spending categories
            top_categories = sorted(
                categories.items(),
                key=lambda x: x[1]['total'],
                reverse=True
            )[:3]
            
            # Generate insights
            if top_categories:
                top_category, top_data = top_categories[0]
                total_spending = sum(cat['total'] for cat in categories.values())
                top_percentage = (top_data['total'] / total_spending) * 100
                
                if top_percentage > 40:
                    insights.append({
                        "type": "spending_pattern",
                        "title": "High Concentration in Single Category",
                        "description": f"Your top spending category '{top_category}' represents {top_percentage:.1f}% of total spending.",
                        "recommendation": "Consider diversifying your spending or reviewing this category for potential savings.",
                        "priority_score": 8,
                        "category": "spending"
                    })
                
                # Check for unusual spending patterns
                if await self._detect_spending_anomalies(transactions):
                    insights.append({
                        "type": "anomaly_detection",
                        "title": "Unusual Spending Pattern Detected",
                        "description": "We've detected unusual spending patterns that may require attention.",
                        "recommendation": "Review your recent transactions and consider setting spending alerts.",
                        "priority_score": 7,
                        "category": "spending"
                    })
            
            return insights
            
        except Exception as e:
            logger.error(f"Spending behavior analysis failed: {e}")
            return []
    
    async def _detect_spending_anomalies(self, transactions: List[Dict]) -> bool:
        """Detect unusual spending patterns using statistical methods"""
        try:
            if len(transactions) < 10:
                return False
            
            amounts = [abs(t.get('amount', 0)) for t in transactions]
            
            # Use Z-score method for anomaly detection
            mean_amount = np.mean(amounts)
            std_amount = np.std(amounts)
            
            if std_amount == 0:
                return False
            
            # Check if any transaction is more than 2 standard deviations from mean
            z_scores = [(amount - mean_amount) / std_amount for amount in amounts]
            anomalies = [abs(z) > 2 for z in z_scores]
            
            return any(anomalies)
            
        except Exception as e:
            logger.error(f"Anomaly detection failed: {e}")
            return False
    
    async def _analyze_savings_opportunities(
        self, 
        income: float, 
        expenses: float
    ) -> List[Dict[str, Any]]:
        """Analyze savings opportunities and optimization"""
        try:
            insights = []
            
            savings_rate = ((income - expenses) / income) * 100 if income > 0 else 0
            
            # Savings rate analysis
            if savings_rate < 20:
                insights.append({
                    "type": "savings_optimization",
                    "title": "Low Savings Rate",
                    "description": f"Your current savings rate is {savings_rate:.1f}%, below the recommended 20%.",
                    "recommendation": "Review your expenses and identify areas to cut back. Consider the 50/30/20 rule.",
                    "priority_score": 9,
                    "category": "savings"
                })
            elif savings_rate < 30:
                insights.append({
                    "type": "savings_optimization",
                    "title": "Good Savings Rate",
                    "description": f"Your savings rate of {savings_rate:.1f}% is good, but could be improved.",
                    "recommendation": "Consider increasing to 30% for better financial security and faster goal achievement.",
                    "priority_score": 6,
                    "category": "savings"
                })
            else:
                insights.append({
                    "type": "savings_optimization",
                    "title": "Excellent Savings Rate",
                    "description": f"Your savings rate of {savings_rate:.1f}% is excellent!",
                    "recommendation": "Consider investing excess savings or setting more ambitious financial goals.",
                    "priority_score": 4,
                    "category": "savings"
                })
            
            return insights
            
        except Exception as e:
            logger.error(f"Savings analysis failed: {e}")
            return []
    
    async def _analyze_investment_strategy(
        self, 
        portfolio: Dict, 
        user_profile: Dict
    ) -> List[Dict[str, Any]]:
        """Analyze investment strategy and provide recommendations"""
        try:
            insights = []
            
            risk_tolerance = user_profile.get('risk_tolerance', 'moderate')
            age = user_profile.get('age', 30)
            
            # Age-based investment recommendations
            if age < 30:
                insights.append({
                    "type": "investment_strategy",
                    "title": "Time Advantage for Growth",
                    "description": "You have decades ahead for compound growth to work in your favor.",
                    "recommendation": "Consider a more aggressive allocation with 80-90% in stocks for maximum growth potential.",
                    "priority_score": 8,
                    "category": "investment"
                })
            elif age > 50:
                insights.append({
                    "type": "investment_strategy",
                    "title": "Capital Preservation Focus",
                    "description": "As you approach retirement, focus on preserving capital while maintaining growth.",
                    "recommendation": "Consider reducing stock allocation to 40-50% and increasing bond allocation.",
                    "priority_score": 9,
                    "category": "investment"
                })
            
            # Risk tolerance alignment
            current_allocation = portfolio.get('allocation', {})
            if current_allocation:
                stock_allocation = current_allocation.get('stocks', 0)
                
                if risk_tolerance == 'conservative' and stock_allocation > 40:
                    insights.append({
                        "type": "risk_alignment",
                        "title": "Risk Tolerance Mismatch",
                        "description": "Your portfolio allocation doesn't align with your conservative risk tolerance.",
                        "recommendation": "Consider reducing stock allocation to 20-30% and increasing bond allocation.",
                        "priority_score": 8,
                        "category": "investment"
                    })
                elif risk_tolerance == 'aggressive' and stock_allocation < 70:
                    insights.append({
                        "type": "risk_alignment",
                        "title": "Growth Opportunity",
                        "description": "Your portfolio could benefit from higher growth potential.",
                        "recommendation": "Consider increasing stock allocation to 80-90% for maximum growth.",
                        "priority_score": 6,
                        "category": "investment"
                    })
            
            return insights
            
        except Exception as e:
            logger.error(f"Investment analysis failed: {e}")
            return []
    
    async def _analyze_market_context(self, market_data: Dict) -> List[Dict[str, Any]]:
        """Analyze market context and provide relevant insights"""
        try:
            insights = []
            
            # Market trend analysis
            if market_data.get('market_trend') == 'bear':
                insights.append({
                    "type": "market_context",
                    "title": "Bear Market Opportunities",
                    "description": "Current market conditions may present buying opportunities for long-term investors.",
                    "recommendation": "Consider dollar-cost averaging and focus on quality companies with strong fundamentals.",
                    "priority_score": 7,
                    "category": "market"
                })
            
            # Interest rate impact
            if market_data.get('interest_rates', 0) > 5:
                insights.append({
                    "type": "market_context",
                    "title": "High Interest Rate Environment",
                    "description": "High interest rates can impact both borrowing costs and investment returns.",
                    "recommendation": "Consider high-yield savings accounts and review any variable-rate debt.",
                    "priority_score": 6,
                    "category": "market"
                })
            
            return insights
            
        except Exception as e:
            logger.error(f"Market context analysis failed: {e}")
            return []
    
    async def get_market_data(self, symbols: List[str]) -> Dict[str, Any]:
        """Get real-time market data for financial analysis"""
        try:
            market_data = {}
            
            for symbol in symbols:
                if symbol in self.market_cache:
                    # Check if cache is still valid (5 minutes)
                    if datetime.now() < self.cache_expiry.get(symbol, datetime.min):
                        market_data[symbol] = self.market_cache[symbol]
                        continue
                
                # Fetch new data
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    
                    # Get historical data for technical analysis
                    hist = ticker.history(period="1mo")
                    
                    if not hist.empty:
                        # Calculate technical indicators
                        technical_data = await self._calculate_technical_indicators(hist)
                        
                        market_data[symbol] = {
                            "current_price": info.get('currentPrice', 0),
                            "change_percent": info.get('regularMarketChangePercent', 0),
                            "market_cap": info.get('marketCap', 0),
                            "pe_ratio": info.get('trailingPE', 0),
                            "dividend_yield": info.get('dividendYield', 0),
                            "technical_indicators": technical_data,
                            "last_updated": datetime.now().isoformat()
                        }
                        
                        # Cache the data
                        self.market_cache[symbol] = market_data[symbol]
                        self.cache_expiry[symbol] = datetime.now() + timedelta(minutes=5)
                        
                except Exception as e:
                    logger.error(f"Failed to fetch data for {symbol}: {e}")
                    continue
            
            return market_data
            
        except Exception as e:
            logger.error(f"Market data fetch failed: {e}")
            return {}
    
    async def _calculate_technical_indicators(self, hist_data: pd.DataFrame) -> Dict[str, float]:
        """Calculate technical indicators for market analysis"""
        try:
            indicators = {}
            
            # Simple Moving Averages
            indicators['sma_20'] = float(hist_data['Close'].rolling(window=20).mean().iloc[-1])
            indicators['sma_50'] = float(hist_data['Close'].rolling(window=50).mean().iloc[-1])
            
            # RSI
            rsi = ta.rsi(hist_data['Close'], length=14)
            indicators['rsi'] = float(rsi.iloc[-1]) if not rsi.empty else 50.0
            
            # MACD
            macd = ta.macd(hist_data['Close'])
            indicators['macd'] = float(macd.iloc[-1]) if not macd.empty else 0.0
            
            # Bollinger Bands
            bb = ta.bbands(hist_data['Close'])
            indicators['bb_upper'] = float(bb['BBU_20_2.0'].iloc[-1]) if not bb.empty else 0.0
            indicators['bb_lower'] = float(bb['BBL_20_2.0'].iloc[-1]) if not bb.empty else 0.0
            
            return indicators
            
        except Exception as e:
            logger.error(f"Technical indicators calculation failed: {e}")
            return {}
    
    async def generate_financial_report(
        self, 
        user_data: Dict,
        report_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """Generate comprehensive financial report"""
        try:
            report = {
                "report_type": report_type,
                "generated_at": datetime.utcnow().isoformat(),
                "user_profile": user_data.get('profile', {}),
                "summary": {},
                "detailed_analysis": {},
                "recommendations": [],
                "charts": {}
            }
            
            # Generate summary metrics
            if user_data.get('transactions'):
                summary = await self._generate_summary_metrics(user_data['transactions'])
                report["summary"] = summary
            
            # Generate detailed analysis
            if report_type == "comprehensive":
                detailed = await self._generate_detailed_analysis(user_data)
                report["detailed_analysis"] = detailed
            
            # Generate recommendations
            recommendations = await self.generate_financial_insights(user_data)
            report["recommendations"] = recommendations[:5]  # Top 5
            
            # Generate charts (placeholder for now)
            report["charts"] = {
                "spending_trends": "chart_url_placeholder",
                "portfolio_allocation": "chart_url_placeholder",
                "savings_progress": "chart_url_placeholder"
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Financial report generation failed: {e}")
            return {"error": f"Report generation failed: {str(e)}"}
    
    async def _generate_summary_metrics(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Generate summary financial metrics"""
        try:
            total_spent = sum(abs(t.get('amount', 0)) for t in transactions)
            total_income = sum(t.get('amount', 0) for t in transactions if t.get('amount', 0) > 0)
            total_expenses = sum(abs(t.get('amount', 0)) for t in transactions if t.get('amount', 0) < 0)
            
            # Categorize transactions
            categories = {}
            for transaction in transactions:
                category = transaction.get('category', 'Other')
                amount = abs(transaction.get('amount', 0))
                
                if category not in categories:
                    categories[category] = 0
                categories[category] += amount
            
            top_categories = sorted(
                categories.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            return {
                "total_transactions": len(transactions),
                "total_spent": total_spent,
                "total_income": total_income,
                "total_expenses": total_expenses,
                "net_flow": total_income - total_expenses,
                "top_spending_categories": top_categories,
                "average_transaction": total_spent / len(transactions) if transactions else 0
            }
            
        except Exception as e:
            logger.error(f"Summary metrics generation failed: {e}")
            return {}
    
    async def _generate_detailed_analysis(self, user_data: Dict) -> Dict[str, Any]:
        """Generate detailed financial analysis"""
        try:
            analysis = {}
            
            # Spending analysis
            if user_data.get('transactions'):
                spending_analysis = await self._analyze_spending_behavior(
                    user_data['transactions']
                )
                analysis["spending"] = spending_analysis
            
            # Savings analysis
            if user_data.get('income') and user_data.get('expenses'):
                savings_analysis = await self._analyze_savings_opportunities(
                    user_data['income'],
                    user_data['expenses']
                )
                analysis["savings"] = savings_analysis
            
            # Investment analysis
            if user_data.get('portfolio'):
                investment_analysis = await self._analyze_investment_strategy(
                    user_data['portfolio'],
                    user_data.get('profile', {})
                )
                analysis["investment"] = investment_analysis
            
            return analysis
            
        except Exception as e:
            logger.error(f"Detailed analysis generation failed: {e}")
            return {}
