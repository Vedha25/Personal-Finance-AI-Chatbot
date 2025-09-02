"""
Financial service for Personal Finance Chatbot
Handles financial calculations, analysis, and insights
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP

logger = logging.getLogger(__name__)

class FinancialService:
    """Service for financial calculations and analysis"""
    
    def __init__(self):
        """Initialize financial service"""
        self.supported_currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"]
    
    async def calculate_financial_health_score(
        self, 
        user_profile: Dict, 
        financial_data: Dict
    ) -> Dict[str, Any]:
        """Calculate overall financial health score"""
        try:
            scores = {}
            weights = {
                "savings_rate": 0.25,
                "debt_to_income": 0.20,
                "emergency_fund": 0.20,
                "investment_diversity": 0.15,
                "budget_adherence": 0.20
            }
            
            # Calculate individual scores
            scores["savings_rate"] = self._calculate_savings_score(
                financial_data.get("income", 0),
                financial_data.get("expenses", 0)
            )
            
            scores["debt_to_income"] = self._calculate_debt_score(
                financial_data.get("debt", 0),
                financial_data.get("income", 0)
            )
            
            scores["emergency_fund"] = self._calculate_emergency_fund_score(
                financial_data.get("emergency_fund", 0),
                financial_data.get("monthly_expenses", 0)
            )
            
            scores["investment_diversity"] = self._calculate_investment_diversity_score(
                financial_data.get("investment_portfolio", {})
            )
            
            scores["budget_adherence"] = self._calculate_budget_adherence_score(
                financial_data.get("budget", {}),
                financial_data.get("actual_spending", {})
            )
            
            # Calculate weighted average
            total_score = sum(
                scores[metric] * weights[metric] 
                for metric in weights.keys()
            )
            
            # Determine grade
            grade = self._get_financial_grade(total_score)
            
            return {
                "overall_score": round(total_score, 2),
                "grade": grade,
                "component_scores": scores,
                "weights": weights,
                "recommendations": self._generate_health_recommendations(scores, total_score),
                "calculated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate financial health score: {e}")
            return {"error": "Failed to calculate financial health score"}
    
    def _calculate_savings_score(self, income: float, expenses: float) -> float:
        """Calculate savings rate score (0-100)"""
        if income <= 0:
            return 0
        
        savings_rate = (income - expenses) / income
        
        if savings_rate >= 0.3:
            return 100
        elif savings_rate >= 0.2:
            return 80
        elif savings_rate >= 0.15:
            return 60
        elif savings_rate >= 0.1:
            return 40
        elif savings_rate >= 0.05:
            return 20
        else:
            return 0
    
    def _calculate_debt_score(self, debt: float, income: float) -> float:
        """Calculate debt-to-income ratio score (0-100)"""
        if income <= 0:
            return 0
        
        debt_ratio = debt / income
        
        if debt_ratio <= 0.28:
            return 100
        elif debt_ratio <= 0.36:
            return 80
        elif debt_ratio <= 0.43:
            return 60
        elif debt_ratio <= 0.50:
            return 40
        elif debt_ratio <= 0.60:
            return 20
        else:
            return 0
    
    def _calculate_emergency_fund_score(
        self, 
        emergency_fund: float, 
        monthly_expenses: float
    ) -> float:
        """Calculate emergency fund adequacy score (0-100)"""
        if monthly_expenses <= 0:
            return 0
        
        months_covered = emergency_fund / monthly_expenses
        
        if months_covered >= 6:
            return 100
        elif months_covered >= 4:
            return 80
        elif months_covered >= 3:
            return 60
        elif months_covered >= 2:
            return 40
        elif months_covered >= 1:
            return 20
        else:
            return 0
    
    def _calculate_investment_diversity_score(self, portfolio: Dict) -> float:
        """Calculate investment diversity score (0-100)"""
        if not portfolio or not portfolio.get("holdings"):
            return 0
        
        holdings = portfolio["holdings"]
        asset_classes = set()
        
        for holding in holdings:
            asset_type = holding.get("asset_type", "unknown")
            asset_classes.add(asset_type)
        
        # Score based on number of asset classes
        if len(asset_classes) >= 5:
            return 100
        elif len(asset_classes) >= 4:
            return 80
        elif len(asset_classes) >= 3:
            return 60
        elif len(asset_classes) >= 2:
            return 40
        else:
            return 20
    
    def _calculate_budget_adherence_score(
        self, 
        budget: Dict, 
        actual_spending: Dict
    ) -> float:
        """Calculate budget adherence score (0-100)"""
        if not budget or not actual_spending:
            return 50  # Neutral score if no data
        
        total_variance = 0
        categories = 0
        
        for category, budgeted in budget.items():
            if category in actual_spending:
                actual = actual_spending[category]
                variance = abs(actual - budgeted) / budgeted if budgeted > 0 else 1
                total_variance += variance
                categories += 1
        
        if categories == 0:
            return 50
        
        avg_variance = total_variance / categories
        
        if avg_variance <= 0.1:
            return 100
        elif avg_variance <= 0.2:
            return 80
        elif avg_variance <= 0.3:
            return 60
        elif avg_variance <= 0.5:
            return 40
        else:
            return 20
    
    def _get_financial_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        elif score >= 55:
            return "C"
        elif score >= 50:
            return "C-"
        elif score >= 45:
            return "D+"
        elif score >= 40:
            return "D"
        else:
            return "F"
    
    def _generate_health_recommendations(
        self, 
        scores: Dict[str, float], 
        overall_score: float
    ) -> List[str]:
        """Generate personalized recommendations based on scores"""
        recommendations = []
        
        if scores.get("savings_rate", 0) < 60:
            recommendations.append("Increase your savings rate by reducing expenses or increasing income")
        
        if scores.get("debt_to_income", 0) < 60:
            recommendations.append("Focus on paying down high-interest debt to improve your debt-to-income ratio")
        
        if scores.get("emergency_fund", 0) < 60:
            recommendations.append("Build your emergency fund to cover 3-6 months of expenses")
        
        if scores.get("investment_diversity", 0) < 60:
            recommendations.append("Diversify your investment portfolio across different asset classes")
        
        if scores.get("budget_adherence", 0) < 60:
            recommendations.append("Improve budget tracking and adherence to spending limits")
        
        if overall_score < 70:
            recommendations.append("Consider consulting with a financial advisor for personalized guidance")
        
        return recommendations
    
    async def analyze_spending_patterns(
        self, 
        transactions: List[Dict], 
        timeframe: str = "monthly"
    ) -> Dict[str, Any]:
        """Analyze spending patterns over time"""
        try:
            if not transactions:
                return {"error": "No transactions to analyze"}
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(transactions)
            df['transaction_date'] = pd.to_datetime(df['transaction_date'])
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
            
            # Filter by timeframe
            if timeframe == "monthly":
                df['period'] = df['transaction_date'].dt.to_period('M')
            elif timeframe == "weekly":
                df['period'] = df['transaction_date'].dt.to_period('W')
            else:
                df['period'] = df['transaction_date'].dt.to_period('M')
            
            # Group by period and category
            spending_by_period = df.groupby(['period', 'category'])['amount'].sum().reset_index()
            
            # Calculate trends
            trends = self._calculate_spending_trends(spending_by_period)
            
            # Identify anomalies
            anomalies = self._detect_spending_anomalies(spending_by_period)
            
            # Generate insights
            insights = self._generate_spending_insights(spending_by_period, trends, anomalies)
            
            return {
                "timeframe": timeframe,
                "total_transactions": len(transactions),
                "total_spent": float(df['amount'].sum()),
                "spending_by_period": spending_by_period.to_dict('records'),
                "trends": trends,
                "anomalies": anomalies,
                "insights": insights,
                "analyzed_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze spending patterns: {e}")
            return {"error": "Failed to analyze spending patterns"}
    
    def _calculate_spending_trends(self, spending_data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate spending trends over time"""
        try:
            trends = {}
            
            # Overall trend
            total_by_period = spending_data.groupby('period')['amount'].sum()
            if len(total_by_period) > 1:
                trend_slope = np.polyfit(range(len(total_by_period)), total_by_period.values, 1)[0]
                trends["overall"] = {
                    "direction": "increasing" if trend_slope > 0 else "decreasing",
                    "slope": float(trend_slope),
                    "change_percent": float((trend_slope / total_by_period.mean()) * 100)
                }
            
            # Category trends
            category_trends = {}
            for category in spending_data['category'].unique():
                category_data = spending_data[spending_data['category'] == category]
                if len(category_data) > 1:
                    category_totals = category_data.groupby('period')['amount'].sum()
                    if len(category_totals) > 1:
                        cat_slope = np.polyfit(range(len(category_totals)), category_totals.values, 1)[0]
                        category_trends[category] = {
                            "direction": "increasing" if cat_slope > 0 else "decreasing",
                            "slope": float(cat_slope)
                        }
            
            trends["categories"] = category_trends
            return trends
            
        except Exception as e:
            logger.error(f"Failed to calculate spending trends: {e}")
            return {}
    
    def _detect_spending_anomalies(self, spending_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect unusual spending patterns"""
        try:
            anomalies = []
            
            # Calculate z-scores for amount
            amounts = spending_data['amount'].values
            mean_amount = np.mean(amounts)
            std_amount = np.std(amounts)
            
            if std_amount > 0:
                z_scores = np.abs((amounts - mean_amount) / std_amount)
                anomaly_indices = np.where(z_scores > 2)[0]  # 2 standard deviations
                
                for idx in anomaly_indices:
                    row = spending_data.iloc[idx]
                    anomalies.append({
                        "period": str(row['period']),
                        "category": row['category'],
                        "amount": float(row['amount']),
                        "z_score": float(z_scores[idx]),
                        "description": f"Unusually high spending in {row['category']} during {row['period']}"
                    })
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Failed to detect spending anomalies: {e}")
            return []
    
    def _generate_spending_insights(
        self, 
        spending_data: pd.DataFrame, 
        trends: Dict, 
        anomalies: List
    ) -> List[str]:
        """Generate insights from spending analysis"""
        insights = []
        
        # Overall spending trend insight
        if trends.get("overall"):
            overall_trend = trends["overall"]
            if overall_trend["change_percent"] > 10:
                insights.append(f"Your overall spending has increased by {overall_trend['change_percent']:.1f}% over the analyzed period")
            elif overall_trend["change_percent"] < -10:
                insights.append(f"Great job! Your overall spending has decreased by {abs(overall_trend['change_percent']):.1f}% over the analyzed period")
        
        # Category insights
        if trends.get("categories"):
            for category, trend in trends["categories"].items():
                if trend["slope"] > 0:
                    insights.append(f"Spending in {category} is trending upward - consider reviewing this category")
        
        # Anomaly insights
        if anomalies:
            insights.append(f"Detected {len(anomalies)} unusual spending patterns that may need attention")
        
        return insights
    
    async def calculate_retirement_needs(
        self, 
        current_age: int, 
        retirement_age: int, 
        current_savings: float, 
        desired_income: float,
        inflation_rate: float = 0.03,
        investment_return: float = 0.07
    ) -> Dict[str, Any]:
        """Calculate retirement savings needs"""
        try:
            years_to_retirement = retirement_age - current_age
            years_in_retirement = 30  # Assume 30 years in retirement
            
            # Calculate future value of current savings
            future_savings = current_savings * (1 + investment_return) ** years_to_retirement
            
            # Calculate inflation-adjusted desired income
            inflation_adjusted_income = desired_income * (1 + inflation_rate) ** years_to_retirement
            
            # Calculate total retirement needs (simplified)
            total_needed = inflation_adjusted_income * years_in_retirement
            
            # Calculate additional savings needed
            additional_needed = total_needed - future_savings
            
            # Calculate monthly savings required
            if additional_needed > 0:
                monthly_savings = additional_needed / ((1 + investment_return) ** years_to_retirement - 1) * (investment_return / 12)
            else:
                monthly_savings = 0
            
            return {
                "current_age": current_age,
                "retirement_age": retirement_age,
                "years_to_retirement": years_to_retirement,
                "current_savings": current_savings,
                "future_savings": round(future_savings, 2),
                "desired_income": desired_income,
                "inflation_adjusted_income": round(inflation_adjusted_income, 2),
                "total_retirement_needs": round(total_needed, 2),
                "additional_savings_needed": round(max(0, additional_needed), 2),
                "monthly_savings_required": round(max(0, monthly_savings), 2),
                "assumptions": {
                    "inflation_rate": inflation_rate,
                    "investment_return": investment_return,
                    "years_in_retirement": years_in_retirement
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate retirement needs: {e}")
            return {"error": "Failed to calculate retirement needs"}
    
    async def calculate_loan_payment(
        self, 
        principal: float, 
        annual_rate: float, 
        years: int,
        payment_type: str = "monthly"
    ) -> Dict[str, Any]:
        """Calculate loan payment details"""
        try:
            # Convert annual rate to monthly
            monthly_rate = annual_rate / 12 / 100
            
            # Calculate number of payments
            if payment_type == "monthly":
                num_payments = years * 12
            elif payment_type == "weekly":
                num_payments = years * 52
            else:
                num_payments = years * 12
            
            # Calculate payment amount
            if monthly_rate > 0:
                payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
            else:
                payment = principal / num_payments
            
            # Calculate total interest
            total_payments = payment * num_payments
            total_interest = total_payments - principal
            
            return {
                "principal": principal,
                "annual_rate": annual_rate,
                "years": years,
                "payment_type": payment_type,
                "monthly_payment": round(payment, 2),
                "total_payments": round(total_payments, 2),
                "total_interest": round(total_interest, 2),
                "num_payments": num_payments
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate loan payment: {e}")
            return {"error": "Failed to calculate loan payment"}
