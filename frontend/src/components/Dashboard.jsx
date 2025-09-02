import React, { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { 
  TrendingUp, 
  CreditCard, 
  DollarSign, 
  Shield, 
  GraduationCap,
  Home,
  Car,
  Zap,
  Droplets,
  Wifi,
  Search,
  Calendar,
  Bell,
  Settings,
  MessageCircle,
  Trophy,
  Headphones,
  QuestionMark,
  Plus,
  ArrowUpRight,
  ArrowDownRight,
  Brain
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts'
import CountUp from 'react-countup'
import { useInView } from 'react-intersection-observer'
import { format, subMonths, startOfMonth } from 'date-fns'
import ChatInterface from './ChatInterface'
import TransactionHistory from './TransactionHistory'
import BalanceChart from './BalanceChart'
import QuickActions from './QuickActions'
import NotificationPanel from './NotificationPanel'

const Dashboard = () => {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState('overview')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [notifications, setNotifications] = useState([])
  const [searchQuery, setSearchQuery] = useState('')

  // Mock data for demonstration
  const overviewCards = [
    {
      title: "Shopping Debit & Credit Card",
      amount: 597,
      icon: CreditCard,
      color: "from-blue-500 to-blue-600",
      change: "+12.5%",
      trend: "up"
    },
    {
      title: "Transfer Other Country",
      amount: 875,
      icon: DollarSign,
      color: "from-green-500 to-green-600",
      change: "+8.2%",
      trend: "up"
    },
    {
      title: "Investment & Insurance",
      amount: 1380,
      icon: Shield,
      color: "from-purple-500 to-purple-600",
      change: "+15.3%",
      trend: "up"
    },
    {
      title: "Kids Education & Hobbies",
      amount: 1200,
      icon: GraduationCap,
      color: "from-orange-500 to-orange-600",
      change: "+5.7%",
      trend: "up"
    }
  ]

  const scheduledPayments = [
    {
      title: "Home Cleaning",
      time: "12 Hrs",
      status: "Pending",
      amount: 497,
      icon: Home,
      color: "text-blue-600"
    },
    {
      title: "Kids Education",
      time: "2 Days",
      status: "Pending",
      amount: 136,
      icon: GraduationCap,
      color: "text-green-600"
    },
    {
      title: "Car Insurance",
      time: "3 Days",
      status: "Pending",
      amount: 258,
      icon: Car,
      color: "text-purple-600"
    }
  ]

  const recentPayments = [
    {
      title: "Electric Bill",
      date: "30/07/22",
      status: "Completed",
      amount: 221,
      icon: Zap,
      color: "text-yellow-600"
    },
    {
      title: "Water Bill",
      date: "27/07/22",
      status: "Completed",
      amount: 189,
      icon: Droplets,
      color: "text-blue-600"
    },
    {
      title: "Home Internet Bill",
      date: "19/07/22",
      status: "Completed",
      amount: 75,
      icon: Wifi,
      color: "text-green-600"
    }
  ]

  const navigationItems = [
    { icon: Home, label: "Home", active: true },
    { icon: QuestionMark, label: "Help", active: false },
    { icon: TrendingUp, label: "Analytics", active: false },
    { icon: MessageCircle, label: "Chat", active: false },
    { icon: Trophy, label: "Rewards", active: false },
    { icon: Headphones, label: "Support", active: false },
    { icon: Settings, label: "Settings", active: false }
  ]

  const { ref: countUpRef, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1
  })

  useEffect(() => {
    // Simulate notifications
    setNotifications([
      { id: 1, message: "Payment completed successfully", type: "success", time: "2 min ago" },
      { id: 2, message: "New investment opportunity available", type: "info", time: "1 hour ago" },
      { id: 3, message: "Account security alert", type: "warning", time: "3 hours ago" }
    ])
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Left Sidebar */}
      <motion.div 
        initial={{ x: -300 }}
        animate={{ x: 0 }}
        className="hidden lg:flex lg:flex-col lg:w-20 bg-gradient-to-b from-purple-600 to-purple-700 text-white"
      >
        <div className="flex flex-col items-center py-6">
          <div className="text-2xl font-bold mb-8">Finance</div>
          {navigationItems.map((item, index) => (
            <motion.button
              key={index}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              className={`w-12 h-12 rounded-full flex items-center justify-center mb-4 transition-all ${
                item.active 
                  ? 'bg-white text-purple-600 shadow-lg' 
                  : 'text-white/80 hover:bg-white/10'
              }`}
            >
              <item.icon className="w-6 h-6" />
            </motion.button>
          ))}
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Header */}
        <motion.header 
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="bg-white shadow-sm border-b border-gray-200 px-6 py-4"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
              <div className="text-gray-600">
                Hi {user?.full_name || 'User'}, Good Morning!
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* Search Bar */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>
              
              {/* Calendar */}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 text-gray-600 hover:text-purple-600 transition-colors"
              >
                <Calendar className="w-6 h-6" />
              </motion.button>
              
              {/* Notifications */}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="relative p-2 text-gray-600 hover:text-purple-600 transition-colors"
                onClick={() => setSidebarOpen(!sidebarOpen)}
              >
                <Bell className="w-6 h-6" />
                {notifications.length > 0 && (
                  <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
                )}
              </motion.button>
            </div>
          </div>
        </motion.header>

        {/* Main Dashboard Content */}
        <div className="flex-1 p-6">
          <div className="flex space-x-6">
            {/* Left Column - Main Content */}
            <div className="flex-1 space-y-6">
              {/* Overview Cards */}
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
              >
                {overviewCards.map((card, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    whileHover={{ y: -5 }}
                    className="bg-white rounded-xl shadow-lg p-6 border border-gray-100"
                  >
                    <div className="flex items-center justify-between mb-4">
                      <div className={`p-3 rounded-lg bg-gradient-to-r ${card.color}`}>
                        <card.icon className="w-6 h-6 text-white" />
                      </div>
                      <div className={`flex items-center text-sm ${
                        card.trend === 'up' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {card.trend === 'up' ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
                        {card.change}
                      </div>
                    </div>
                    <h3 className="text-gray-600 text-sm mb-2">{card.title}</h3>
                    <div ref={countUpRef} className="text-2xl font-bold text-gray-800">
                      {inView && <CountUp end={card.amount} prefix="$" duration={1} />}
                    </div>
                  </motion.div>
                ))}
              </motion.div>

              {/* Balance Chart */}
              <BalanceChart />

              {/* Transaction History */}
              <TransactionHistory />

                          {/* Quick Actions */}
            <QuickActions />
            
            {/* AI Chatbot Section */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 }}
              className="bg-gradient-to-r from-purple-500 to-blue-600 rounded-xl p-6 text-white"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center">
                    <Brain className="w-8 h-8" />
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold">Meet Sam - Your AI Financial Advisor</h3>
                    <p className="text-purple-100 text-lg">Get personalized financial advice, take quizzes, and create savings plans</p>
                  </div>
                </div>
                <div className="flex space-x-4">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => window.location.href = '/chat'}
                    className="px-8 py-4 bg-white text-purple-600 rounded-xl font-semibold hover:bg-gray-50 transition-colors shadow-lg"
                  >
                    Chat with Sam
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => window.location.href = '/ai-analytics'}
                    className="px-8 py-4 bg-purple-600 text-white rounded-xl font-semibold hover:bg-purple-700 transition-colors shadow-lg"
                  >
                    AI Analytics
                  </motion.button>
                </div>
              </div>
            </motion.div>
          </div>

            {/* Right Column - Sidebar */}
            <div className="w-80 space-y-6">
              {/* User Profile & Credit Card */}
              <motion.div
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-white rounded-xl shadow-lg p-6 border border-gray-100"
              >
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
                    {user?.full_name?.charAt(0) || 'U'}
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-800">{user?.full_name || 'User Name'}</h3>
                    <p className="text-sm text-gray-500">Premium Member</p>
                  </div>
                </div>
                
                {/* Credit Card */}
                <div className="bg-gradient-to-r from-purple-600 to-purple-700 rounded-xl p-4 text-white">
                  <div className="flex justify-between items-start mb-4">
                    <span className="text-sm opacity-90">CREDIT</span>
                    <div className="w-8 h-6 bg-white/20 rounded"></div>
                  </div>
                  <div className="text-lg font-mono mb-2">**** **** **** 1234</div>
                  <div className="text-sm opacity-90 mb-1">AVAILABLE FUNDS $75,389.25</div>
                  <div className="flex justify-between text-sm opacity-90">
                    <span>EXPIRES 01/23</span>
                    <span>CVV 123</span>
                  </div>
                </div>
              </motion.div>

              {/* Scheduled Payments */}
              <motion.div
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-white rounded-xl shadow-lg p-6 border border-gray-100"
              >
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Schedule Payments</h3>
                <div className="space-y-3">
                  {scheduledPayments.map((payment, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.3 + index * 0.1 }}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                    >
                      <div className="flex items-center space-x-3">
                        <payment.icon className={`w-5 h-5 ${payment.color}`} />
                        <div>
                          <div className="font-medium text-gray-800">{payment.title}</div>
                          <div className="text-sm text-gray-500">{payment.time} - {payment.status}</div>
                        </div>
                      </div>
                      <div className="font-semibold text-gray-800">${payment.amount}</div>
                    </motion.div>
                  ))}
                </div>
              </motion.div>

              {/* Recent Payments */}
              <motion.div
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
                className="bg-white rounded-xl shadow-lg p-6 border border-gray-100"
              >
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Payments</h3>
                <div className="space-y-3">
                  {recentPayments.map((payment, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.5 + index * 0.1 }}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                    >
                      <div className="flex items-center space-x-3">
                        <payment.icon className={`w-5 h-5 ${payment.color}`} />
                        <div>
                          <div className="font-medium text-gray-800">{payment.title}</div>
                          <div className="text-sm text-gray-500">{payment.date} - {payment.status}</div>
                        </div>
                      </div>
                      <div className="font-semibold text-gray-800">${payment.amount}</div>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            </div>
          </div>
        </div>
      </div>

      {/* Notification Panel */}
      <AnimatePresence>
        {sidebarOpen && (
          <NotificationPanel 
            notifications={notifications}
            onClose={() => setSidebarOpen(false)}
          />
        )}
      </AnimatePresence>
    </div>
  )
}

export default Dashboard
