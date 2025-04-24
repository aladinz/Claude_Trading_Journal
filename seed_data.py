from datetime import datetime, timedelta
from app import app, db
from models.trade import Trade
import random

# Sample tickers
tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA', 'AMD']

# Sample entry/exit reasons
entry_reasons = [
    "Strong uptrend with increasing volume",
    "Breakout above key resistance level",
    "Positive earnings surprise with gap up",
    "Oversold conditions on RSI with bullish divergence",
    "Bullish engulfing pattern at support level",
    "50-day MA crossing above 200-day MA",
    "Sector rotation into technology",
    "Successful retest of previous resistance as support"
]

exit_reasons = [
    "Profit target reached",
    "Bearish reversal pattern formed",
    "Stop loss triggered",
    "Negative market sentiment",
    "Deteriorating sector performance",
    "Bearish divergence on indicators",
    "Extended overbought conditions",
    "Time-based exit (swing trade duration reached)"
]

notes = [
    "Should have taken partial profits earlier",
    "Good execution on entry, could have improved exit timing",
    "Market was too volatile for this strategy",
    "Trade worked well, consider increasing position size next time",
    "Need to be more patient with winners",
    "Trade thesis played out exactly as expected",
    "Exit was too early, missed additional gains",
    "Need to reduce risk in similar market conditions"
]

def create_sample_trades(num_trades=15):
    """Generate sample trades for testing the application"""
    
    # Clear existing data
    Trade.query.delete()
    
    today = datetime.now()
    
    for i in range(num_trades):
        # Random date within the last 90 days
        days_ago = random.randint(1, 90)
        trade_date = today - timedelta(days=days_ago)
        
        # Random ticker
        ticker = random.choice(tickers)
        
        # Trade type
        trade_type = random.choice(['Buy', 'Sell'])
        
        # Entry and exit prices
        base_price = random.uniform(50, 500)
        entry_price = round(base_price, 2)
        
        # Simulate some winning and some losing trades
        win = random.random() > 0.4  # 60% win rate
        
        price_change_percent = random.uniform(0.02, 0.15)  # 2% to 15% change
        
        if trade_type == 'Buy':
            if win:
                exit_price = round(entry_price * (1 + price_change_percent), 2)
            else:
                exit_price = round(entry_price * (1 - price_change_percent), 2)
        else:  # Sell (short)
            if win:
                exit_price = round(entry_price * (1 - price_change_percent), 2)
            else:
                exit_price = round(entry_price * (1 + price_change_percent), 2)
        
        # Shares
        shares = random.randint(10, 500)
        
        # Holding period
        holding_period = random.randint(1, 15)
        
        # Stop loss (usually a percentage of entry price)
        stop_loss_percent = random.uniform(0.03, 0.08)  # 3% to 8% stop loss
        if trade_type == 'Buy':
            stop_loss = round(entry_price * (1 - stop_loss_percent), 2)
        else:
            stop_loss = round(entry_price * (1 + stop_loss_percent), 2)
        
        # Randomly select reasons and notes
        entry_reason = random.choice(entry_reasons)
        exit_reason = random.choice(exit_reasons)
        note = random.choice(notes)
        
        # Calculate P/L
        if trade_type == 'Buy':
            pl_amount = (exit_price - entry_price) * shares
            pl_percent = ((exit_price - entry_price) / entry_price) * 100
        else:  # Sell (short)
            pl_amount = (entry_price - exit_price) * shares
            pl_percent = ((entry_price - exit_price) / entry_price) * 100
        
        # Create trade
        trade = Trade(
            date=trade_date,
            ticker=ticker,
            trade_type=trade_type,
            entry_price=entry_price,
            exit_price=exit_price,
            shares=shares,
            holding_period=holding_period,
            entry_reason=entry_reason,
            exit_reason=exit_reason,
            stop_loss=stop_loss,
            notes=note,
            pl_amount=pl_amount,
            pl_percent=pl_percent
        )
        
        db.session.add(trade)
    
    db.session.commit()
    print(f"Created {num_trades} sample trades.")

if __name__ == '__main__':
    with app.app_context():
        create_sample_trades(20)  # Generate 20 sample trades