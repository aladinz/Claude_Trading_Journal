#!/bin/bash

echo "🚀 Setting up Advanced Swing Trading Journal..."

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if pandas and numpy installed correctly (needed for export and advanced features)
python -c "import pandas, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: pandas or numpy may not have installed correctly."
    echo "   Some features (Excel export, advanced analytics) may not work."
    echo "   You can try installing them manually with:"
    echo "   pip install pandas numpy openpyxl"
    echo ""
    read -p "Continue with setup anyway? (y/n): " continue_answer
    if [[ $continue_answer != "y" && $continue_answer != "Y" ]]; then
        echo "Setup aborted. Please fix the dependency issues and try again."
        exit 1
    fi
fi

# Initialize the database
echo "🗃️  Initializing database..."
python app.py &
sleep 2
kill $!

# Seed sample data (optional)
read -p "📊 Would you like to add sample trade data for testing? (y/n): " answer
if [[ $answer == "y" || $answer == "Y" ]]; then
    echo "✨ Adding sample trade data..."
    python seed_data.py
fi

echo ""
echo "✅ Setup complete! You can now run the application with:"
echo "   source venv/bin/activate && python app.py"
echo ""
echo "🌐 Then visit http://127.0.0.1:5000/ in your browser."
echo ""
echo "📝 Features included in this version:"
echo "   • Dark/Light mode toggle"
echo "   • Advanced analytics dashboard"
echo "   • Calendar view of trades"
echo "   • Risk/Reward analysis"
echo "   • AI trading advisor"
echo "   • CSV and Excel export"
echo ""
echo "Happy trading! 📈"