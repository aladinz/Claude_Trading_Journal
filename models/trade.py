from datetime import datetime
from models import db

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    exit_date = db.Column(db.DateTime, nullable=True)
    ticker = db.Column(db.String(10), nullable=False)
    trade_type = db.Column(db.String(10), nullable=False)  # Buy or Sell
    entry_price = db.Column(db.Float, nullable=False)
    exit_price = db.Column(db.Float, nullable=True)
    shares = db.Column(db.Integer, nullable=False)
    holding_period = db.Column(db.Integer, nullable=True)  # in days
    stop_loss = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    pl_amount = db.Column(db.Float, nullable=True)  # profit/loss amount
    pl_percent = db.Column(db.Float, nullable=True)  # profit/loss percentage
    
    # Psychological tracking fields
    entry_emotion = db.Column(db.String(20), nullable=True)  # Emotion at entry
    exit_emotion = db.Column(db.String(20), nullable=True)  # Emotion at exit
    entry_reason = db.Column(db.Text, nullable=True)  # Reason for entry
    exit_reason = db.Column(db.Text, nullable=True)  # Reason for exit
    followed_plan = db.Column(db.Boolean, nullable=True)  # Whether trade followed plan
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # List of valid emotions for UI selection
    EMOTIONS = [
        'confident', 'cautious', 'fearful', 'greedy', 
        'fomo', 'regretful', 'impulsive', 'patient',
        'anxious', 'excited', 'indifferent', 'hopeful'
    ]
    
    def __repr__(self):
        return f"<Trade {self.ticker} {self.trade_type} on {self.date}>"