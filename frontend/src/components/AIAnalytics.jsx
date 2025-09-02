import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Brain, 
  TrendingUp, 
  TrendingDown, 
  Target, 
  BarChart3, 
  PieChart,
  LineChart,
  DollarSign,
  Calendar,
  AlertTriangle,
  CheckCircle,
  Info,
  Zap,
  Lightbulb,
  Calculator,
  ArrowRight,
  RefreshCw,
  Play,
  Pause
} from 'lucide-react'
import { LineChart as RechartsLineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart as RechartsPieChart, Pie, Cell } from 'recharts'
import CountUp from 'react-countup'
import { useInView } from 'react-intersection-observer'
import toast from 'react-hot-toast'

const AIAnalytics = () => {
  const [activeTab, setActiveTab] = useState('predictions')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResults, setAnalysisResults] = useState(null)
  const [selectedTimeframe, setSelectedTimeframe] = useState('1_year')
  
  const { ref: headerRef, inView: headerInView } = useInView({
    triggerOnce: true,
    threshold: 0.1
  })
  
  const { ref: chartRef, inView: chartInView } = useInView({
    triggerOnce: true,
    threshold: 0.1
  })

  // Mock data for demonstration
  const mockUserData = {
    profile: {
      age: 28,
      risk_tolerance: 'moderate',
      income_level: 'medium'
    },
    transactions: [
      { amount: -1200, category: 'Housing', date: '2024-01-15' },
      { amount: -450, category: 'Food', date: '2024-01-14' },
      { amount: -200, category: 'Transportation', date: '2024-01-13' },
      { amount: -150, category: 'Entertainment', date: '2024-01-12' },
      { amount: 5000, category: 'Salary', date: '2024-01-01' }
    ],
    current_savings: 15000,
    monthly_contribution: 800,
    portfolio: {
      assets: [
        { name: 'S&P 500 ETF', value: 8000, expected_return: 0.08 },
        { name: 'Bond Fund', value: 4000, expected_return: 0.04 },
        { name: 'Cash', value: 3000, expected_return: 0.02 }
      ]
    }
  }

  const tabs = [
    { id: 'predictions', label: 'AI Predictions', icon: TrendingUp },
    { id: 'insights', label: 'Smart Insights', icon: Brain },
    { id: 'analysis', label: 'Deep Analysis', icon: BarChart3 },
    { id: 'portfolio', label: 'Portfolio AI', icon: PieChart }
  ]

  const timeframes = [
    { value: '1_year', label: '1 Year' },
    { value: '3_years', label: '3 Years' },
    { value: '5_years', label: '5 Years' },
    { value: '10_years', label: '10 Years' }
  ]

  const handleAnalysis = async (analysisType = 'comprehensive') => {
    setIsAnalyzing(true)
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      // Mock results
      const mockResults = generateMockResults(analysisType)
      setAnalysisResults(mockResults)
      
      toast.success('AI Analysis completed successfully!')
    } catch (error) {
      toast.error('Analysis failed. Please try again.')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const generateMockResults = (analysisType) => {
    const baseResults = {
      timestamp: new Date().toISOString(),
      analysis_type: analysisType,
      user_id: 'user_123'
    }

    if (analysisType === 'comprehensive') {
      return {
        ...baseResults,
        ai_insights: [
          {
            type: 'ai_spending_insight',
            title: 'AI-Powered Spending Analysis',
            description: 'Advanced analysis of your spending patterns using AI algorithms',
            insights: [
              'Your top spending category Housing represents 45.2% of total spending. Consider diversifying expenses.',
              'Your spending is concentrated in few categories. Consider diversifying for better financial health.'
            ],
            priority: 'high',
            ai_generated: true
          },
          {
            type: 'ai_savings_insight',
            title: 'AI-Powered Savings Analysis',
            description: 'Intelligent analysis of your savings behavior and optimization opportunities',
            insights: [
              'Good savings rate! AI suggests increasing to 30% for better financial security and faster goal achievement.'
            ],
            priority: 'medium',
            ai_generated: true
          }
        ],
        spending_prediction: {
          prediction_type: 'spending_patterns',
          next_month_prediction: 1850.50,
          confidence_interval: {
            lower: 1650.25,
            upper: 2050.75,
            confidence_level: 0.95
          },
          category_predictions: {
            'Housing': { predicted: 1200, confidence: 0.92 },
            'Food': { predicted: 450, confidence: 0.88 },
            'Transportation': { predicted: 200, confidence: 0.85 }
          }
        },
        savings_prediction: {
          prediction_type: 'savings_growth',
          current_savings: 15000,
          monthly_contribution: 800,
          expected_annual_return: 0.07,
          predictions: {
            '1_years': {
              future_value: 25800,
              total_contributions: 9600,
              interest_earned: 1200,
              growth_multiplier: 1.72
            },
            '5_years': {
              future_value: 65000,
              total_contributions: 48000,
              interest_earned: 2000,
              growth_multiplier: 4.33
            }
          }
        }
      }
    }

    return baseResults
  }

  const renderPredictionsTab = () => (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl p-6 text-white"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-2xl font-bold">AI Financial Predictions</h3>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => handleAnalysis('comprehensive')}
            disabled={isAnalyzing}
            className="px-6 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-50 transition-colors disabled:opacity-50"
          >
            {isAnalyzing ? (
              <>
                <RefreshCw className="w-4 h-4 inline mr-2 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Zap className="w-4 h-4 inline mr-2" />
                Run AI Analysis
              </>
            )}
          </motion.button>
        </div>
        <p className="text-blue-100 text-lg">
          Our AI analyzes your financial data to predict spending patterns, savings growth, and investment returns
        </p>
      </motion.div>

      {analysisResults && (
        <AnimatePresence>
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="grid grid-cols-1 md:grid-cols-2 gap-6"
          >
            {/* Spending Prediction */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white rounded-xl p-6 shadow-lg border-l-4 border-l-red-500"
            >
              <div className="flex items-center justify-between mb-4">
                <h4 className="text-xl font-semibold text-gray-800">Spending Prediction</h4>
                <TrendingUp className="w-6 h-6 text-red-500" />
              </div>
              
              {analysisResults.spending_prediction && (
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-red-600">
                      ${analysisResults.spending_prediction.next_month_prediction.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">Predicted Next Month</div>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="text-sm font-medium text-gray-700 mb-2">Confidence Interval (95%)</div>
                    <div className="flex justify-between text-sm">
                      <span>${analysisResults.spending_prediction.confidence_interval.lower.toLocaleString()}</span>
                      <span>${analysisResults.spending_prediction.confidence_interval.upper.toLocaleString()}</span>
                    </div>
                  </div>
                </div>
              )}
            </motion.div>

            {/* Savings Prediction */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white rounded-xl p-6 shadow-lg border-l-4 border-l-green-500"
            >
              <div className="flex items-center justify-between mb-4">
                <h4 className="text-xl font-semibold text-gray-800">Savings Growth</h4>
                <Target className="w-6 h-6 text-green-500" />
              </div>
              
              {analysisResults.savings_prediction && (
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-600">
                      ${analysisResults.savings_prediction.predictions['5_years'].future_value.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">5-Year Projection</div>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="text-sm font-medium text-gray-700 mb-2">Growth Multiplier</div>
                    <div className="text-2xl font-bold text-green-600">
                      {analysisResults.savings_prediction.predictions['5_years'].growth_multiplier.toFixed(1)}x
                    </div>
                  </div>
                </div>
              )}
            </motion.div>
          </motion.div>
        </AnimatePresence>
      )}
    </div>
  )

  const renderInsightsTab = () => (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-green-500 to-blue-600 rounded-xl p-6 text-white"
      >
        <div className="flex items-center space-x-3 mb-4">
          <Brain className="w-8 h-8" />
          <h3 className="text-2xl font-bold">AI-Powered Financial Insights</h3>
        </div>
        <p className="text-green-100 text-lg">
          Discover personalized financial recommendations powered by advanced AI algorithms
        </p>
      </motion.div>

      {analysisResults?.ai_insights && (
        <div className="space-y-4">
          {analysisResults.ai_insights.map((insight, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-xl p-6 shadow-lg border-l-4 border-l-blue-500"
            >
              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                    <Lightbulb className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
                
                <div className="flex-1">
                  <h4 className="text-xl font-semibold text-gray-800 mb-2">
                    {insight.title}
                  </h4>
                  <p className="text-gray-600 mb-4">{insight.description}</p>
                  
                  <div className="space-y-2">
                    {insight.insights.map((insightText, i) => (
                      <div key={i} className="flex items-start space-x-2">
                        <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                        <span className="text-gray-700">{insightText}</span>
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-4 flex items-center space-x-2">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      insight.priority === 'high' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {insight.priority} priority
                    </span>
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
                      AI Generated
                    </span>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  )

  const renderAnalysisTab = () => (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-purple-500 to-pink-600 rounded-xl p-6 text-white"
      >
        <div className="flex items-center space-x-3 mb-4">
          <BarChart3 className="w-8 h-8" />
          <h3 className="text-2xl font-bold">Deep Financial Analysis</h3>
        </div>
        <p className="text-purple-100 text-lg">
          Comprehensive analysis of your financial health with actionable insights
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Financial Health Score */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-xl p-6 shadow-lg text-center"
        >
          <div className="w-20 h-20 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl font-bold text-white">85</span>
          </div>
          <h4 className="text-xl font-semibold text-gray-800 mb-2">Financial Health Score</h4>
          <p className="text-gray-600 text-sm">Excellent financial standing</p>
        </motion.div>

        {/* Risk Assessment */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-xl p-6 shadow-lg text-center"
        >
          <div className="w-20 h-20 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl font-bold text-white">M</span>
          </div>
          <h4 className="text-xl font-semibold text-gray-800 mb-2">Risk Profile</h4>
          <p className="text-gray-600 text-sm">Moderate risk tolerance</p>
        </motion.div>

        {/* Savings Rate */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-xl p-6 shadow-lg text-center"
        >
          <div className="w-20 h-20 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl font-bold text-white">24%</span>
          </div>
          <h4 className="text-xl font-semibold text-gray-800 mb-2">Savings Rate</h4>
          <p className="text-gray-600 text-sm">Above recommended 20%</p>
        </motion.div>
      </div>

      {/* Charts Section */}
      <motion.div
        ref={chartRef}
        initial={{ opacity: 0, y: 20 }}
        animate={chartInView ? { opacity: 1, y: 0 } : {}}
        className="bg-white rounded-xl p-6 shadow-lg"
      >
        <h4 className="text-xl font-semibold text-gray-800 mb-6">Financial Trends</h4>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Spending Trend Chart */}
          <div>
            <h5 className="text-lg font-medium text-gray-700 mb-4">Monthly Spending Trend</h5>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <RechartsLineChart data={[
                  { month: 'Jan', spending: 1800 },
                  { month: 'Feb', spending: 1650 },
                  { month: 'Mar', spending: 1900 },
                  { month: 'Apr', spending: 1750 },
                  { month: 'May', spending: 2000 },
                  { month: 'Jun', spending: 1850 }
                ]}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="month" stroke="#6b7280" />
                  <YAxis stroke="#6b7280" />
                  <Tooltip />
                  <Line type="monotone" dataKey="spending" stroke="#ef4444" strokeWidth={3} />
                </RechartsLineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Category Distribution */}
          <div>
            <h5 className="text-lg font-medium text-gray-700 mb-4">Spending by Category</h5>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <RechartsPieChart>
                  <Pie
                    data={[
                      { name: 'Housing', value: 45, color: '#ef4444' },
                      { name: 'Food', value: 20, color: '#10b981' },
                      { name: 'Transportation', value: 15, color: '#3b82f6' },
                      { name: 'Entertainment', value: 10, color: '#8b5cf6' },
                      { name: 'Other', value: 10, color: '#f59e0b' }
                    ]}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {[
                      { name: 'Housing', value: 45, color: '#ef4444' },
                      { name: 'Food', value: 20, color: '#10b981' },
                      { name: 'Transportation', value: 15, color: '#3b82f6' },
                      { name: 'Entertainment', value: 10, color: '#8b5cf6' },
                      { name: 'Other', value: 10, color: '#f59e0b' }
                    ].map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </RechartsPieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )

  const renderPortfolioTab = () => (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-indigo-500 to-cyan-600 rounded-xl p-6 text-white"
      >
        <div className="flex items-center space-x-3 mb-4">
          <PieChart className="w-8 h-8" />
          <h3 className="text-2xl font-bold">AI Portfolio Analysis</h3>
        </div>
        <p className="text-indigo-100 text-lg">
          Intelligent portfolio optimization and risk assessment powered by AI
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Portfolio Overview */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white rounded-xl p-6 shadow-lg"
        >
          <h4 className="text-xl font-semibold text-gray-800 mb-6">Portfolio Overview</h4>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="font-medium text-gray-700">Total Value</span>
              <span className="text-xl font-bold text-gray-800">$15,000</span>
            </div>
            
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="font-medium text-gray-700">Expected Return</span>
              <span className="text-xl font-bold text-green-600">6.2%</span>
            </div>
            
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="font-medium text-gray-700">Risk Level</span>
              <span className="text-xl font-bold text-yellow-600">Moderate</span>
            </div>
          </div>
        </motion.div>

        {/* Asset Allocation */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white rounded-xl p-6 shadow-lg"
        >
          <h4 className="text-xl font-semibold text-gray-800 mb-6">Asset Allocation</h4>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-4 h-4 bg-blue-500 rounded"></div>
                <span className="text-gray-700">S&P 500 ETF</span>
              </div>
              <span className="font-semibold text-gray-800">53%</span>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-4 h-4 bg-green-500 rounded"></div>
                <span className="text-gray-700">Bond Fund</span>
              </div>
              <span className="font-semibold text-gray-800">27%</span>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-4 h-4 bg-purple-500 rounded"></div>
                <span className="text-gray-700">Cash</span>
              </div>
              <span className="font-semibold text-gray-800">20%</span>
            </div>
          </div>
        </motion.div>
      </div>

      {/* AI Recommendations */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl p-6 shadow-lg"
      >
        <h4 className="text-xl font-semibold text-gray-800 mb-6">AI Portfolio Recommendations</h4>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-blue-50 rounded-lg p-4 border-l-4 border-blue-500">
            <div className="flex items-start space-x-3">
              <CheckCircle className="w-6 h-6 text-blue-600 mt-1" />
              <div>
                <h5 className="font-semibold text-blue-800 mb-2">Rebalance Portfolio</h5>
                <p className="text-blue-700 text-sm">Consider rebalancing to maintain target allocation and reduce risk</p>
              </div>
            </div>
          </div>
          
          <div className="bg-green-50 rounded-lg p-4 border-l-4 border-green-500">
            <div className="flex items-start space-x-3">
              <TrendingUp className="w-6 h-6 text-green-600 mt-1" />
              <div>
                <h5 className="font-semibold text-green-800 mb-2">Increase Equity Exposure</h5>
                <p className="text-green-700 text-sm">With your moderate risk tolerance, consider increasing stock allocation</p>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          ref={headerRef}
          initial={{ opacity: 0, y: -20 }}
          animate={headerInView ? { opacity: 1, y: 0 } : {}}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            AI Financial Analytics
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Experience the future of financial planning with our AI-powered analytics, 
            predictions, and personalized insights
          </p>
        </motion.div>

        {/* Tabs */}
        <div className="bg-white rounded-xl shadow-lg p-2 mb-8">
          <div className="flex space-x-2">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-medium transition-all ${
                  activeTab === tab.id
                    ? 'bg-blue-500 text-white shadow-md'
                    : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
                }`}
              >
                <tab.icon className="w-5 h-5" />
                <span>{tab.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Tab Content */}
        <AnimatePresence mode="wait">
          {activeTab === 'predictions' && (
            <motion.div
              key="predictions"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              {renderPredictionsTab()}
            </motion.div>
          )}

          {activeTab === 'insights' && (
            <motion.div
              key="insights"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              {renderInsightsTab()}
            </motion.div>
          )}

          {activeTab === 'analysis' && (
            <motion.div
              key="analysis"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              {renderAnalysisTab()}
            </motion.div>
          )}

          {activeTab === 'portfolio' && (
            <motion.div
              key="portfolio"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              {renderPortfolioTab()}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

export default AIAnalytics
