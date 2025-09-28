#!/bin/bash

# MailHub AI Recruitment Agent Runner
echo "🚀 Starting MailHub AI Recruitment Agent"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Please copy .env.example to .env and add your API keys:"
    echo "   cp .env.example .env"
    echo "   # Then edit .env with your keys"
    exit 1
fi

# Run the agent
echo "🤖 Starting recruitment agent..."
python3 AgentEmail.py