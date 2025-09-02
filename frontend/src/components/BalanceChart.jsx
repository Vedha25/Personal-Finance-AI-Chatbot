import React from 'react'
import { motion } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { TrendingUp } from 'lucide-react'

const BalanceChart = () => {
  const data = [
    { month: 'Jan', balance: 45000, target: 50000 },
    { month: 'Feb', balance: 52000, target: 50000 },
    { month: 'Mar', balance: 48000, target: 50000 },
    { month: 'Apr', balance: 55000, target: 50000 },
    { month: 'May', balance: 58000, target: 50000 },
    { month: 'Jun', balance: 62000, target: 50000 },
    { month: 'Jul', balance: 59000, target: 50000 },
    { month: 'Aug', balance: 65000, target: 50000 },
    { month: 'Sep', balance: 68000, target: 50000 },
    { month: 'Oct', balance: 72000, target: 50000 },
    { month: 'Nov', balance: 75000, target: 50000 },
    { month: 'Dec', balance: 78000, target: 50000 }
  ]

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-800">{label}</p>
          <p className="text-blue-600">Balance: ${payload[0].value?.toLocaleString()}</p>
          <p className="text-gray-500">Target: ${payload[1].value?.toLocaleString()}</p>
        </div>
      )
    }
    return null
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      className="bg-white rounded-xl shadow-lg p-6 border border-gray-100"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-semibold text-gray-800">Balance</h3>
          <p className="text-gray-500">Last 12 Months</p>
        </div>
        <div className="flex items-center space-x-2 text-green-600">
          <TrendingUp className="w-5 h-5" />
          <span className="text-sm font-medium">+15.2%</span>
        </div>
      </div>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="month" 
              stroke="#6b7280"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              stroke="#6b7280"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `$${(value / 1000).toFixed(0)}K`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar 
              dataKey="balance" 
              fill="#8b5cf6" 
              radius={[4, 4, 0, 0]}
              className="hover:opacity-80 transition-opacity"
            />
            <Bar 
              dataKey="target" 
              fill="#e5e7eb" 
              radius={[4, 4, 0, 0]}
              className="hover:opacity-80 transition-opacity"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="flex items-center justify-center space-x-6 mt-4">
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-purple-500 rounded"></div>
          <span className="text-sm text-gray-600">Current Balance</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-gray-300 rounded"></div>
          <span className="text-sm text-gray-600">Target</span>
        </div>
      </div>
    </motion.div>
  )
}

export default BalanceChart
