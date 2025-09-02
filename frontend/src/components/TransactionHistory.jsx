import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Clock, Filter, Download, Eye, MoreHorizontal } from 'lucide-react'

const TransactionHistory = () => {
  const [filter, setFilter] = useState('all')
  const [showDetails, setShowDetails] = useState(null)

  const transactions = [
    {
      id: 1,
      name: "James Smith",
      description: "Graphic Design",
      date: "29/06/22",
      amount: 259.50,
      status: "Completed",
      avatar: "JS",
      category: "design"
    },
    {
      id: 2,
      name: "Robert William",
      description: "Photo Editing",
      date: "28/06/22",
      amount: 189.75,
      status: "Reviewed",
      avatar: "RW",
      category: "editing"
    },
    {
      id: 3,
      name: "Sarah Johnson",
      description: "Web Development",
      date: "27/06/22",
      amount: 450.00,
      status: "Completed",
      avatar: "SJ",
      category: "development"
    },
    {
      id: 4,
      name: "Michael Brown",
      description: "Logo Design",
      date: "26/06/22",
      amount: 320.25,
      status: "Pending",
      avatar: "MB",
      category: "design"
    }
  ]

  const getStatusColor = (status) => {
    switch (status) {
      case 'Completed':
        return 'bg-green-100 text-green-800'
      case 'Pending':
        return 'bg-yellow-100 text-yellow-800'
      case 'Reviewed':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getCategoryColor = (category) => {
    switch (category) {
      case 'design':
        return 'bg-blue-100 text-blue-800'
      case 'editing':
        return 'bg-purple-100 text-purple-800'
      case 'development':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const filteredTransactions = filter === 'all' 
    ? transactions 
    : transactions.filter(t => t.status.toLowerCase() === filter.toLowerCase())

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.5 }}
      className="bg-white rounded-xl shadow-lg border border-gray-100"
    >
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-semibold text-gray-800">Transaction History</h3>
            <p className="text-gray-500">Last 3 Months</p>
          </div>
          <div className="flex items-center space-x-3">
            <div className="relative">
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="appearance-none bg-gray-50 border border-gray-200 rounded-lg px-4 py-2 pr-8 text-sm focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="all">All Status</option>
                <option value="completed">Completed</option>
                <option value="pending">Pending</option>
                <option value="reviewed">Reviewed</option>
              </select>
              <Filter className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
            </div>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 text-gray-600 hover:text-purple-600 transition-colors"
            >
              <Download className="w-5 h-5" />
            </motion.button>
          </div>
        </div>
      </div>

      <div className="p-6">
        <div className="space-y-4">
          <AnimatePresence>
            {filteredTransactions.map((transaction, index) => (
              <motion.div
                key={transaction.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
                onClick={() => setShowDetails(showDetails === transaction.id ? null : transaction.id)}
              >
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                    {transaction.avatar}
                  </div>
                  <div>
                    <div className="font-medium text-gray-800">{transaction.name}</div>
                    <div className="text-sm text-gray-500">{transaction.description}</div>
                    <div className="flex items-center space-x-2 mt-1">
                      <Clock className="w-3 h-3 text-gray-400" />
                      <span className="text-xs text-gray-500">{transaction.date}</span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(transaction.category)}`}>
                        {transaction.category}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <div className="font-semibold text-gray-800">${transaction.amount}</div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(transaction.status)}`}>
                      {transaction.status}
                    </span>
                  </div>
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                  >
                    <MoreHorizontal className="w-4 h-4" />
                  </motion.button>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        {/* Transaction Details */}
        <AnimatePresence>
          {showDetails && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-4 p-4 bg-purple-50 border border-purple-200 rounded-lg"
            >
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-medium text-purple-800">Transaction Details</h4>
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => setShowDetails(null)}
                  className="text-purple-600 hover:text-purple-800"
                >
                  <Eye className="w-4 h-4" />
                </motion.button>
              </div>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-purple-600 font-medium">Transaction ID:</span>
                  <span className="ml-2 text-gray-700">#TX{showDetails.toString().padStart(6, '0')}</span>
                </div>
                <div>
                  <span className="text-purple-600 font-medium">Category:</span>
                  <span className="ml-2 text-gray-700 capitalize">
                    {transactions.find(t => t.id === showDetails)?.category}
                  </span>
                </div>
                <div>
                  <span className="text-purple-600 font-medium">Date:</span>
                  <span className="ml-2 text-gray-700">
                    {transactions.find(t => t.id === showDetails)?.date}
                  </span>
                </div>
                <div>
                  <span className="text-purple-600 font-medium">Status:</span>
                  <span className="ml-2 text-gray-700">
                    {transactions.find(t => t.id === showDetails)?.status}
                  </span>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  )
}

export default TransactionHistory
