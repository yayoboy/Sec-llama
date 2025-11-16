#!/bin/bash
# Web UI Full - Setup Script

set -e

echo "🎨 Sec-Llama Web UI - Setup"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi

# Check Node.js
if ! command -v npm &> /dev/null; then
    echo "❌ Node.js/npm not found"
    exit 1
fi

# Backend setup
echo "📦 Setting up backend..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Link shared libraries
ln -sf ../../shared ./shared

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend
npm install
cd ..

# Create directories
mkdir -p logs reports database

# Create .env if not exists
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# Web UI Configuration
WEB_UI_PORT=8080
SECRET_KEY=change-this-secret-key
DATABASE_URL=sqlite:///database/sec_llama.db
OLLAMA_HOST=http://localhost:11434
LOG_LEVEL=INFO
EOF
    echo "⚙️ Created .env (edit as needed)"
fi

# Optional: Install Ollama
read -p "Install Ollama? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    curl -fsSL https://ollama.com/install.sh | sh
    ollama pull llama3.1:8b
fi

# Build frontend
echo "🏗️ Building frontend..."
cd frontend
npm run build
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Start with: ./start.sh"
echo "Then open: http://localhost:8080"
echo ""
