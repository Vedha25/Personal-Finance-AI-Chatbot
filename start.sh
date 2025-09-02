#!/bin/bash

# Personal Finance Chatbot - Quick Start Script
echo "🚀 Starting Personal Finance Chatbot..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your IBM Watson API credentials before continuing."
    echo "   Required: WATSON_API_KEY, WATSON_ASSISTANT_ID, WATSON_URL"
    echo ""
    read -p "Press Enter after updating .env file..."
fi

# Check if required environment variables are set
source .env
if [ -z "$WATSON_API_KEY" ] || [ "$WATSON_API_KEY" = "your_watson_api_key_here" ]; then
    echo "❌ Please set your IBM Watson API credentials in .env file"
    exit 1
fi

echo "✅ Environment variables configured"

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service status
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🎉 Personal Finance Chatbot is starting up!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🗄️  Database: localhost:5432"
echo "🔴 Redis: localhost:6379"
echo ""
echo "📝 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
echo "🔄 To restart: docker-compose restart"
echo ""
echo "✨ Happy financial planning!"
