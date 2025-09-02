import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Bot, User, Loader2, Brain, Target, TrendingUp, Lightbulb, BookOpen, Calculator, Star, Trophy, Gift } from 'lucide-react'
import { chatAPI } from '../services/api'
import toast from 'react-hot-toast'

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "Hi! I'm Sam, your AI Financial Advisor! 🎯",
      timestamp: new Date(),
      sender: 'Sam'
    },
    {
      id: 2,
      type: 'bot',
      content: "I can help you with:\n• 📊 Financial Quizzes & Knowledge\n• 💡 Personalized Financial Advice\n• 🎯 Savings Plans & Goals\n• 📈 Investment Strategies\n• 💰 Budget Planning\n\nWhat would you like to explore today?",
      timestamp: new Date(),
      sender: 'Sam'
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [currentQuiz, setCurrentQuiz] = useState(null)
  const [quizScore, setQuizScore] = useState(0)
  const [showQuizResults, setShowQuizResults] = useState(false)
  const [activeMode, setActiveMode] = useState('chat') // chat, quiz, advice, savings
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Financial Quiz Questions
  const quizQuestions = [
    {
      id: 1,
      question: "What is the 50/30/20 rule for budgeting?",
      options: [
        "50% needs, 30% wants, 20% savings",
        "50% savings, 30% needs, 20% wants",
        "50% wants, 30% savings, 20% needs",
        "50% bills, 30% food, 20% entertainment"
      ],
      correct: 0,
      explanation: "The 50/30/20 rule suggests allocating 50% of income to needs, 30% to wants, and 20% to savings and debt repayment."
    },
    {
      id: 2,
      question: "What is compound interest?",
      options: [
        "Interest earned only on the principal amount",
        "Interest earned on both principal and accumulated interest",
        "A type of bank fee",
        "A loan payment method"
      ],
      correct: 1,
      explanation: "Compound interest is interest earned on both the initial principal and the accumulated interest from previous periods."
    },
    {
      id: 3,
      question: "What is an emergency fund?",
      options: [
        "Money for vacations",
        "3-6 months of living expenses saved for emergencies",
        "Investment portfolio",
        "Credit card balance"
      ],
      correct: 1,
      explanation: "An emergency fund should cover 3-6 months of living expenses for unexpected situations like job loss or medical emergencies."
    },
    {
      id: 4,
      question: "What is diversification in investing?",
      options: [
        "Putting all money in one stock",
        "Spreading investments across different assets",
        "Selling all investments",
        "Borrowing money to invest"
      ],
      correct: 1,
      explanation: "Diversification means spreading investments across different asset classes to reduce risk."
    },
    {
      id: 5,
      question: "What is a credit score?",
      options: [
        "Your bank account balance",
        "A number that represents your creditworthiness",
        "Your monthly income",
        "Your tax return amount"
      ],
      correct: 1,
      explanation: "A credit score is a number that lenders use to assess your creditworthiness and likelihood of repaying loans."
    }
  ]

  // Quick Action Buttons
  const quickActions = [
    {
      id: 'quiz',
      title: 'Take Financial Quiz',
      icon: Brain,
      color: 'from-blue-500 to-blue-600',
      description: 'Test your financial knowledge'
    },
    {
      id: 'advice',
      title: 'Get Financial Advice',
      icon: Lightbulb,
      color: 'from-green-500 to-green-600',
      description: 'Personalized recommendations'
    },
    {
      id: 'savings',
      title: 'Savings Plan',
      icon: Target,
      color: 'from-purple-500 to-purple-600',
      description: 'Create a savings strategy'
    },
    {
      id: 'budget',
      title: 'Budget Help',
      icon: Calculator,
      color: 'from-orange-500 to-orange-600',
      description: 'Budget planning assistance'
    }
  ]

  const handleQuickAction = (actionId) => {
    setActiveMode(actionId)
    setCurrentQuiz(null)
    setShowQuizResults(false)
    
    let message = ''
    switch (actionId) {
      case 'quiz':
        message = "Great choice! Let's test your financial knowledge. I'll ask you 5 questions about personal finance. Ready to start?"
        startQuiz()
        break
      case 'advice':
        message = "I'd love to give you personalized financial advice! Tell me about your current financial situation, goals, or any specific concerns you have."
        break
      case 'savings':
        message = "Excellent! Let's create a personalized savings plan. First, tell me about your current savings, income, and what you're saving for (emergency fund, vacation, house, retirement, etc.)."
        break
      case 'budget':
        message = "Budgeting is key to financial success! Share your monthly income and expenses, and I'll help you create a realistic budget plan."
        break
      default:
        message = "How can I help you today?"
    }
    
    addMessage(message, 'bot', 'Sam')
  }

  const startQuiz = () => {
    setCurrentQuiz({
      currentQuestion: 0,
      questions: quizQuestions,
      answers: []
    })
    setQuizScore(0)
    setShowQuizResults(false)
  }

  const handleQuizAnswer = (answerIndex) => {
    if (!currentQuiz) return
    
    const question = currentQuiz.questions[currentQuiz.currentQuestion]
    const isCorrect = answerIndex === question.correct
    
    if (isCorrect) {
      setQuizScore(prev => prev + 1)
    }
    
    // Show answer explanation
    addMessage(`Your answer: ${question.options[answerIndex]}\n\n${isCorrect ? '✅ Correct!' : '❌ Incorrect!'}\n\n${question.explanation}`, 'bot', 'Sam')
    
    // Move to next question or end quiz
    if (currentQuiz.currentQuestion < currentQuiz.questions.length - 1) {
      setCurrentQuiz(prev => ({
        ...prev,
        currentQuestion: prev.currentQuestion + 1
      }))
      
      // Show next question after a delay
      setTimeout(() => {
        const nextQuestion = currentQuiz.questions[currentQuiz.currentQuestion + 1]
        addMessage(`Question ${currentQuiz.currentQuestion + 2}: ${nextQuestion.question}`, 'bot', 'Sam')
      }, 2000)
    } else {
      // Quiz completed
      setTimeout(() => {
        showQuizResults()
      }, 2000)
    }
  }

  const showQuizResults = () => {
    const percentage = (quizScore / quizQuestions.length) * 100
    let resultMessage = ''
    
    if (percentage >= 80) {
      resultMessage = `🎉 Congratulations! You scored ${quizScore}/${quizQuestions.length} (${percentage}%)\n\n🏆 You're a financial expert! Keep up the great work and continue learning about personal finance.`
    } else if (percentage >= 60) {
      resultMessage = `👍 Good job! You scored ${quizScore}/${quizQuestions.length} (${percentage}%)\n\n📚 You have a solid foundation. Let's work on improving your knowledge together!`
    } else {
      resultMessage = `📖 Nice effort! You scored ${quizScore}/${quizQuestions.length} (${percentage}%)\n\n💡 Don't worry - financial literacy is a journey. I'm here to help you learn and grow!`
    }
    
    addMessage(resultMessage, 'bot', 'Sam')
    setShowQuizResults(true)
    setCurrentQuiz(null)
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!inputMessage.trim() || isLoading) return

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage.trim(),
      timestamp: new Date(),
      sender: 'You'
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      // Generate AI response based on the message content
      const response = await generateAIResponse(inputMessage.trim())
      addMessage(response, 'bot', 'Sam')
    } catch (error) {
      addMessage("I'm having trouble processing your request right now. Please try again!", 'bot', 'Sam')
      toast.error('Failed to get response from Sam')
    } finally {
      setIsLoading(false)
    }
  }

  const generateAIResponse = async (message) => {
    // Simulate AI response generation
    const lowerMessage = message.toLowerCase()
    
    if (lowerMessage.includes('savings') || lowerMessage.includes('save')) {
      return `💡 **Savings Strategy**:\n\n1. **Emergency Fund First**: Aim for 3-6 months of expenses\n2. **Automate Savings**: Set up automatic transfers\n3. **50/30/20 Rule**: 20% of income to savings\n4. **High-Yield Account**: Use accounts with better interest rates\n5. **Track Progress**: Monitor your savings goals regularly\n\nWhat specific savings goal are you working towards?`
    }
    
    if (lowerMessage.includes('budget') || lowerMessage.includes('spending')) {
      return `📊 **Budgeting Tips**:\n\n1. **Track Everything**: Use apps or spreadsheets\n2. **Categorize Expenses**: Needs vs. Wants vs. Savings\n3. **Set Realistic Goals**: Start small and build up\n4. **Review Monthly**: Adjust your budget as needed\n5. **Use Envelope Method**: Allocate cash for different categories\n\nWould you like me to help you create a specific budget plan?`
    }
    
    if (lowerMessage.includes('invest') || lowerMessage.includes('investment')) {
      return `📈 **Investment Basics**:\n\n1. **Start Early**: Time is your biggest advantage\n2. **Diversify**: Don't put all eggs in one basket\n3. **Index Funds**: Low-cost, broad market exposure\n4. **Risk Tolerance**: Match investments to your comfort level\n5. **Long-term Focus**: Avoid trying to time the market\n\nWhat's your investment timeline and risk tolerance?`
    }
    
    if (lowerMessage.includes('debt') || lowerMessage.includes('credit')) {
      return `💳 **Debt Management**:\n\n1. **High-Interest First**: Pay off credit cards first\n2. **Debt Snowball**: Start with smallest debts\n3. **Consolidation**: Consider combining multiple debts\n4. **Avoid New Debt**: Stop adding to existing balances\n5. **Seek Help**: Consider credit counseling if needed\n\nWhat type of debt are you dealing with?`
    }
    
    if (lowerMessage.includes('retirement') || lowerMessage.includes('401k')) {
      return `🏖️ **Retirement Planning**:\n\n1. **Start Now**: Even small amounts add up over time\n2. **Employer Match**: Contribute enough to get full match\n3. **Roth vs Traditional**: Consider tax implications\n4. **Increase Contributions**: Aim for 15% of income\n5. **Diversify**: Mix of stocks, bonds, and other assets\n\nHow many years until you plan to retire?`
    }
    
    // Default response
    return `Thanks for your message! I'm here to help with all things finance. You can:\n\n• Ask me specific financial questions\n• Take the financial quiz to test your knowledge\n• Get personalized advice for your situation\n• Create a savings plan\n• Get help with budgeting\n\nWhat would you like to focus on?`
  }

  const addMessage = (text, sender, name = 'Sam') => {
    const newMessage = {
      id: Date.now(),
      type: sender,
      content: text,
      timestamp: new Date(),
      sender: name
    }
    setMessages(prev => [...prev, newMessage])
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      handleSendMessage(e)
    }
  }

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const resetChat = () => {
    setMessages([
      {
        id: 1,
        type: 'bot',
        content: "Hi! I'm Sam, your AI Financial Advisor! 🎯",
        timestamp: new Date(),
        sender: 'Sam'
      },
      {
        id: 2,
        type: 'bot',
        content: "I can help you with:\n• 📊 Financial Quizzes & Knowledge\n• 💡 Personalized Financial Advice\n• 🎯 Savings Plans & Goals\n• 📈 Investment Strategies\n• 💰 Budget Planning\n\nWhat would you like to explore today?",
        timestamp: new Date(),
        sender: 'Sam'
      }
    ])
    setCurrentQuiz(null)
    setShowQuizResults(false)
    setActiveMode('chat')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <div className="flex items-center justify-center space-x-3 mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-blue-600 rounded-full flex items-center justify-center">
              <Brain className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-800">Sam - AI Financial Advisor</h1>
              <p className="text-gray-600">Your personal finance expert & quiz master</p>
            </div>
          </div>
          
          {/* Quick Actions */}
          <div className="flex flex-wrap justify-center gap-4 mb-6">
            {quickActions.map((action) => (
              <motion.button
                key={action.id}
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => handleQuickAction(action.id)}
                className={`p-4 rounded-xl bg-white shadow-lg border border-gray-200 hover:shadow-xl transition-all duration-200 ${activeMode === action.id ? 'ring-2 ring-purple-500' : ''}`}
              >
                <div className="flex flex-col items-center space-y-2">
                  <div className={`p-3 rounded-lg bg-gradient-to-r ${action.color}`}>
                    <action.icon className="w-6 h-6 text-white" />
                  </div>
                  <div className="text-center">
                    <h3 className="font-semibold text-gray-800 text-sm">{action.title}</h3>
                    <p className="text-xs text-gray-500">{action.description}</p>
                  </div>
                </div>
              </motion.button>
            ))}
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Chat Interface */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden"
            >
              {/* Chat Header */}
              <div className="bg-gradient-to-r from-purple-500 to-blue-600 p-4 text-white">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                      <Bot className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="font-semibold">Chat with Sam</h3>
                      <p className="text-sm opacity-90">AI Financial Advisor</p>
                    </div>
                  </div>
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={resetChat}
                    className="p-2 bg-white/20 rounded-lg hover:bg-white/30 transition-colors"
                  >
                    <Trophy className="w-5 h-5" />
                  </motion.button>
                </div>
              </div>

              {/* Chat Messages */}
              <div className="h-96 overflow-y-auto p-4 bg-gray-50">
                <div className="space-y-4">
                  {messages.map((message) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl ${
                          message.type === 'user'
                            ? 'bg-gradient-to-r from-purple-500 to-blue-600 text-white'
                            : 'bg-white text-gray-800 border border-gray-200 shadow-sm'
                        }`}
                      >
                        <div className="flex items-start space-x-2">
                          {message.type === 'bot' && (
                            <div className="w-6 h-6 bg-gradient-to-r from-purple-500 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                              <span className="text-white text-xs font-bold">S</span>
                            </div>
                          )}
                          <div className="flex-1">
                            <div className="text-xs opacity-70 mb-1">{message.sender}</div>
                            <div className="whitespace-pre-line">{message.content}</div>
                            <div className={`text-xs mt-2 ${
                              message.type === 'user' ? 'text-purple-100' : 'text-gray-500'
                            }`}>
                              {formatTime(message.timestamp)}
                            </div>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                  
                  {/* Loading Indicator */}
                  {isLoading && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="flex justify-start"
                    >
                      <div className="bg-white text-gray-800 border border-gray-200 rounded-2xl px-4 py-3 shadow-sm">
                        <div className="flex items-center space-x-2">
                          <div className="w-6 h-6 bg-gradient-to-r from-purple-500 to-blue-600 rounded-full flex items-center justify-center">
                            <span className="text-white text-xs font-bold">S</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                            <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </div>
                <div ref={messagesEndRef} />
              </div>

              {/* Chat Input */}
              <div className="p-4 bg-white border-t border-gray-200">
                <form onSubmit={handleSendMessage} className="flex space-x-3">
                  <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask Sam about finances, take a quiz, or get advice..."
                    className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    disabled={isLoading}
                  />
                  <motion.button
                    type="submit"
                    disabled={isLoading || !inputMessage.trim()}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-600 text-white rounded-xl font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg transition-all"
                  >
                    <Send className="w-5 h-5" />
                  </motion.button>
                </form>
              </div>
            </motion.div>
          </div>

          {/* Quiz Panel */}
          <div className="lg:col-span-1">
            <AnimatePresence>
              {currentQuiz && (
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  className="bg-white rounded-2xl shadow-xl border border-gray-200 p-6"
                >
                  <div className="text-center mb-6">
                    <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Brain className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-xl font-bold text-gray-800">Financial Quiz</h3>
                    <p className="text-gray-600">Question {currentQuiz.currentQuestion + 1} of {currentQuiz.questions.length}</p>
                  </div>

                  <div className="mb-6">
                    <h4 className="font-semibold text-gray-800 mb-4">
                      {currentQuiz.questions[currentQuiz.currentQuestion].question}
                    </h4>
                    
                    <div className="space-y-3">
                      {currentQuiz.questions[currentQuiz.currentQuestion].options.map((option, index) => (
                        <motion.button
                          key={index}
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                          onClick={() => handleQuizAnswer(index)}
                          className="w-full p-3 text-left bg-gray-50 hover:bg-purple-50 border border-gray-200 hover:border-purple-300 rounded-lg transition-all duration-200"
                        >
                          {option}
                        </motion.button>
                      ))}
                    </div>
                  </div>

                  <div className="text-center">
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${((currentQuiz.currentQuestion + 1) / currentQuiz.questions.length) * 100}%` }}
                      ></div>
                    </div>
                    <p className="text-sm text-gray-600 mt-2">
                      Progress: {currentQuiz.currentQuestion + 1}/{currentQuiz.questions.length}
                    </p>
                  </div>
                </motion.div>
              )}

              {showQuizResults && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="bg-white rounded-2xl shadow-xl border border-gray-200 p-6"
                >
                  <div className="text-center">
                    <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Trophy className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-xl font-bold text-gray-800 mb-2">Quiz Complete!</h3>
                    <p className="text-gray-600 mb-4">Great job completing the financial quiz!</p>
                    
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => {
                        setShowQuizResults(false)
                        handleQuickAction('quiz')
                      }}
                      className="px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-600 text-white rounded-xl font-medium hover:shadow-lg transition-all"
                    >
                      Take Quiz Again
                    </motion.button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface
