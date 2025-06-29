# Advanced Swing Trading Journal

A sophisticated web-based personal swing trading journal application built with Python and Flask. This application helps you track, analyze, and improve your trading performance through comprehensive analytics and AI-powered insights.

## 🌟 Key Features

- **Complete Trade Tracking**: Log buy/sell stock transactions with comprehensive details
- **Advanced Analytics Dashboard**: Visualize your trading performance with interactive charts
- **Calendar View**: See your trading activity in a month-view calendar
- **Risk/Reward Analysis**: Analyze your trade risk management with detailed metrics
- **AI Trading Advisor**: Get AI-powered insights and recommendations based on your trading patterns
- **Dark Mode Support**: Toggle between light and dark themes for comfortable viewing
- **Data Export**: Download your trade data in CSV or Excel format
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 📊 Data Tracked for Each Trade

- Date
- Ticker Symbol
- Trade Type (Buy/Sell)
- Entry Price
- Exit Price
- Number of Shares
- Holding Period
- Reason for Entry
- Reason for Exit
- Stop-Loss Price
- Notes/Observations
- Calculated P/L Amount
- Calculated P/L Percentage
- Risk/Reward Ratio (calculated when stop-loss is defined)

## 📈 Analytics & Insights

- **Main Analytics**:
  - Win/Loss ratio and win rate percentage
  - Total and average profit/loss
  - Performance by ticker
  - Trade count and success metrics

- **Dashboard**:
  - Period-over-period performance comparison
  - Performance over time chart
  - Win/loss distribution
  - Top performing tickers
  - Recent trades list
  - AI-generated insights

- **Calendar View**:
  - Monthly trading activity overview
  - Daily trade performance
  - Monthly performance summary
  - Trading days count

- **Risk/Reward Analysis**:
  - Overall risk/reward ratio
  - Risk distribution analysis
  - Win rate by risk level
  - Best and worst risk/reward trades
  - Risk vs. return visualization

- **AI Advisor**:
  - Performance scoring and assessment
  - Strengths and improvement areas
  - Pattern recognition
  - Strategy recommendations
  - Best setup identification
  - Interactive Q&A for personalized advice

## 🚀 Installation

### Local Development

1. Clone this repository
2. Create a virtual environment (recommended)
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages
   ```
   pip install -r requirements.txt
   ```
4. Run the setup script (creates database and adds sample data if desired)
   ```
   ./setup.sh
   ```
5. Start the application
   ```
   python app.py
   ```
6. Open your browser and go to `http://127.0.0.1:5000/`

### Streamlit Version

A simplified Streamlit version is also available:

```bash
# Run Streamlit version locally on port 8504
./run_streamlit.sh

# Or manually
venv/Scripts/python.exe -m streamlit run streamlit_app.py --server.port 8504
```

- **Streamlit Cloud**: Automatically deployed
- **Local Streamlit**: http://localhost:8504
- **Files**: `streamlit_app.py` (minimal), `streamlit_app_backup.py` (full-featured)

### Vercel Deployment

This application is configured for deployment on Vercel's serverless platform.

#### Environment Variables

Set the following environment variables in your Vercel project:

- `SECRET_KEY`: A secret key for session security
- `DATABASE_URL`: (Optional) URL to your database service. If not provided, a local SQLite database will be used.

#### Deployment Steps

1. Fork or clone this repository to your GitHub account
2. Connect your Vercel account to your GitHub repository
3. Import the project into Vercel
4. Set the required environment variables
5. Deploy!

## 🖼️ Screenshots

(Add screenshots of your application here)

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **UI Components**: Font Awesome Icons
- **Charts & Visualization**: Chart.js
- **Data Export**: CSV, Excel (via pandas)

## 🔮 Future Enhancements

- Integration with brokerage APIs for automatic trade import
- Advanced statistical analysis with machine learning
- Option trade tracking and analysis
- Portfolio allocation tracking
- Market conditions correlation
- Strategy backtesting tools
- Mobile app version

## 📄 License

MIT License

## 👤 Author

Aladin Zahran

---

Happy Trading and Good Luck! 📊 💹 📉 📈
