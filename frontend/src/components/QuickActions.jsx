import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Plus, 
  Send, 
  Download, 
  Upload, 
  CreditCard, 
  TrendingUp,
  Shield,
  Gift,
  Zap,
  Star
} from 'lucide-react'

const QuickActions = () => {
  const [selectedAction, setSelectedAction] = useState(null)

  const actions = [
    {
      id: 'send',
      title: 'Send Money',
      description: 'Transfer to friends & family',
      icon: Send,
      color: 'from-blue-500 to-blue-600',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200'
    },
    {
      id: 'receive',
      title: 'Request Money',
      description: 'Get paid by others',
      icon: Download,
      color: 'from-green-500 to-green-600',
      bgColor: 'bg-green-50',
      borderColor: 'border-green-200'
    },
    {
      id: 'invest',
      title: 'Invest',
      description: 'Grow your wealth',
      icon: TrendingUp,
      color: 'from-purple-500 to-purple-600',
      bgColor: 'bg-purple-50',
      borderColor: 'border-purple-200'
    },
    {
      id: 'insurance',
      title: 'Insurance',
      description: 'Protect your assets',
      icon: Shield,
      color: 'from-orange-500 to-orange-600',
      bgColor: 'bg-orange-50',
      borderColor: 'border-orange-200'
    },
    {
      id: 'rewards',
      title: 'Rewards',
      description: 'Earn cashback & points',
      icon: Gift,
      color: 'from-pink-500 to-pink-600',
      bgColor: 'bg-pink-50',
      borderColor: 'border-pink-200'
    },
    {
      id: 'payments',
      title: 'Pay Bills',
      description: 'Quick bill payments',
      icon: Zap,
      color: 'from-yellow-500 to-yellow-600',
      bgColor: 'bg-yellow-50',
      borderColor: 'border-yellow-200'
    }
  ]

  const handleActionClick = (actionId) => {
    setSelectedAction(actionId)
    // Simulate action processing
    setTimeout(() => setSelectedAction(null), 2000)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.6 }}
      className="bg-white rounded-xl shadow-lg border border-gray-100 p-6"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-semibold text-gray-800">Quick Actions</h3>
          <p className="text-gray-500">Access your most used features</p>
        </div>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="p-2 text-purple-600 hover:bg-purple-50 rounded-lg transition-colors"
        >
          <Plus className="w-5 h-5" />
        </motion.button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {actions.map((action, index) => (
          <motion.div
            key={action.id}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.7 + index * 0.1 }}
            whileHover={{ y: -5, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`${action.bgColor} ${action.borderColor} border-2 rounded-xl p-4 cursor-pointer transition-all duration-200 hover:shadow-lg`}
            onClick={() => handleActionClick(action.id)}
          >
            <div className="flex flex-col items-center text-center space-y-3">
              <motion.div
                whileHover={{ rotate: 360 }}
                transition={{ duration: 0.6 }}
                className={`p-3 rounded-lg bg-gradient-to-r ${action.color}`}
              >
                <action.icon className="w-6 h-6 text-white" />
              </motion.div>
              <div>
                <h4 className="font-semibold text-gray-800 text-sm">{action.title}</h4>
                <p className="text-xs text-gray-600 mt-1">{action.description}</p>
              </div>
              
              {/* Loading State */}
              {selectedAction === action.id && (
                <motion.div
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="flex items-center space-x-2 text-xs text-purple-600"
                >
                  <div className="w-3 h-3 border-2 border-purple-600 border-t-transparent rounded-full animate-spin"></div>
                  <span>Processing...</span>
                </motion.div>
              )}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Featured Action */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.0 }}
        className="mt-6 p-4 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl text-white"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-white/20 rounded-lg">
              <Star className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-semibold">Premium Features</h4>
              <p className="text-sm opacity-90">Unlock advanced financial tools</p>
            </div>
          </div>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-4 py-2 bg-white text-purple-600 rounded-lg font-medium hover:bg-gray-50 transition-colors"
          >
            Upgrade
          </motion.button>
        </div>
      </motion.div>

      {/* Action Tips */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2 }}
        className="mt-4 p-3 bg-gray-50 rounded-lg"
      >
        <p className="text-xs text-gray-600 text-center">
          💡 <strong>Tip:</strong> Use quick actions to save time on common financial tasks. 
          Your most used actions will appear at the top.
        </p>
      </motion.div>
    </motion.div>
  )
}

export default QuickActions
