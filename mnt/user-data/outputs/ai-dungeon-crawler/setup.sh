#!/bin/bash
# AI Dungeon Crawler - Setup Script

echo "================================"
echo "AI Dungeon Crawler - Setup"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt --break-system-packages

echo ""
echo "================================"
echo "Setup complete!"
echo "================================"
echo ""
echo "To run the game:"
echo "  python main.py"
echo ""
echo "To run with Python 3 explicitly:"
echo "  python3 main.py"
echo ""
