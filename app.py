from flask import Flask, render_template, request, redirect, url_for, flash, Response, send_file
from datetime import datetime, timedelta, date
import os
import io
import json
import csv
import pandas as pd
import numpy as np
import calendar as cal
from collections import defaultdict
import random

from models import db
from models.trade import Trade

app = Flask(__name__)
# Use environment variable for secret key or default to a generated one
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))

# Database configuration
# Use environment variable for database URL or default to SQLite
db_path = os.environ.get('DATABASE_URL', 'sqlite:///trading_journal.db')
# Handle special case for Postgres URLs from Vercel/Heroku
if db_path.startswith("postgres://"):
    db_path = db_path.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

from sqlalchemy import case, nulls_last, desc, asc

@app.route('/')
def index():
    # Get a few recent trades for the landing page
    trades = Trade.query.order_by(Trade.date.desc()).limit(10).all()
    return render_template('index.html', trades=trades)

@app.route('/journal')
@app.route('/journal/<sort_by>')
def journal(sort_by=None):
    # Sort options with null handling
    sort_options = {
        'date_desc': Trade.date.desc(),
        'date_asc': Trade.date.asc(),
        # Handle NULL pl_amount values by placing them last
        'profit_desc': nulls_last(Trade.pl_amount.desc()),
        'profit_asc': nulls_last(Trade.pl_amount.asc()),
        'ticker_asc': Trade.ticker.asc(),
        'ticker_desc': Trade.ticker.desc(),
        # Handle NULL holding_period values by placing them last
        'holding_desc': nulls_last(Trade.holding_period.desc()),
        'holding_asc': nulls_last(Trade.holding_period.asc())
    }
    
    # Default sort: date descending (newest first)
    if sort_by not in sort_options:
        sort_by = 'date_desc'
    
    # Start query
    query = Trade.query
    
    # Check for ticker search
    search_ticker = request.args.get('search_ticker', '').strip().upper()
    if search_ticker:
        # Use partial matching with LIKE for more flexible search
        query = query.filter(Trade.ticker.like(f'%{search_ticker}%'))
    
    # Check for filters
    filter_type = request.args.get('filter')
    if filter_type:
        if filter_type == 'open':
            query = query.filter(Trade.exit_price == None)
        elif filter_type == 'profitable':
            query = query.filter(Trade.pl_amount > 0)
        elif filter_type == 'losing':
            query = query.filter(Trade.pl_amount < 0)
    
    # Query trades with filtering and sorting
    trades = query.order_by(sort_options[sort_by]).all()
    
    return render_template('journal.html', trades=trades, sort_by=sort_by)

@app.route('/add_trade', methods=['GET', 'POST'])
def add_trade():
    if request.method == 'POST':
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d')
        
        # Handle exit date if provided
        exit_date = None
        if request.form.get('exit_date'):
            exit_date = datetime.strptime(request.form['exit_date'], '%Y-%m-%d')
        
        ticker = request.form['ticker'].upper()
        trade_type = request.form['trade_type']
        entry_price = float(request.form['entry_price'])
        exit_price = float(request.form['exit_price']) if request.form['exit_price'] else None
        shares = int(request.form['shares'])
        
        # Calculate holding period from dates
        holding_period = None
        if exit_date:
            delta = exit_date - date
            holding_period = delta.days
        
        stop_loss = float(request.form['stop_loss']) if request.form['stop_loss'] else None
        notes = request.form['notes']
        
        # Get psychological data
        entry_emotion = request.form.get('entry_emotion')
        exit_emotion = request.form.get('exit_emotion')
        entry_reason = request.form.get('entry_reason')
        exit_reason = request.form.get('exit_reason')
        followed_plan = True if request.form.get('followed_plan') == 'true' else None
        
        # Calculate profit/loss
        pl_amount = None
        pl_percent = None
        if exit_price is not None:
            if trade_type == 'Buy':
                pl_amount = (exit_price - entry_price) * shares
                pl_percent = ((exit_price - entry_price) / entry_price) * 100
            else:  # Sell (short)
                pl_amount = (entry_price - exit_price) * shares
                pl_percent = ((entry_price - exit_price) / entry_price) * 100
        
        new_trade = Trade(
            date=date,
            exit_date=exit_date,
            ticker=ticker,
            trade_type=trade_type,
            entry_price=entry_price,
            exit_price=exit_price,
            shares=shares,
            holding_period=holding_period,
            stop_loss=stop_loss,
            notes=notes,
            pl_amount=pl_amount,
            pl_percent=pl_percent,
            # Psychological tracking fields
            entry_emotion=entry_emotion,
            exit_emotion=exit_emotion,
            entry_reason=entry_reason,
            exit_reason=exit_reason,
            followed_plan=followed_plan
        )
        
        db.session.add(new_trade)
        db.session.commit()
        flash('Trade added successfully!', 'success')
        return redirect(url_for('index'))
        
    # Pass today's date to the template
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('add_trade.html', today=today)

@app.route('/edit_trade/<int:id>', methods=['GET', 'POST'])
def edit_trade(id):
    trade = Trade.query.get_or_404(id)
    
    if request.method == 'POST':
        date_str = request.form['date']
        trade.date = datetime.strptime(date_str, '%Y-%m-%d')
        
        # Handle exit date if provided
        trade.exit_date = None
        if request.form.get('exit_date'):
            trade.exit_date = datetime.strptime(request.form['exit_date'], '%Y-%m-%d')
        
        trade.ticker = request.form['ticker'].upper()
        trade.trade_type = request.form['trade_type']
        trade.entry_price = float(request.form['entry_price'])
        trade.exit_price = float(request.form['exit_price']) if request.form['exit_price'] else None
        trade.shares = int(request.form['shares'])
        
        # Calculate holding period from dates
        trade.holding_period = None
        if trade.exit_date:
            delta = trade.exit_date - trade.date
            trade.holding_period = delta.days
        
        trade.stop_loss = float(request.form['stop_loss']) if request.form['stop_loss'] else None
        trade.notes = request.form['notes']
        
        # Update psychological data
        trade.entry_emotion = request.form.get('entry_emotion')
        trade.exit_emotion = request.form.get('exit_emotion')
        trade.entry_reason = request.form.get('entry_reason')
        trade.exit_reason = request.form.get('exit_reason') 
        trade.followed_plan = True if request.form.get('followed_plan') == 'true' else None
        
        # Recalculate profit/loss
        if trade.exit_price is not None:
            if trade.trade_type == 'Buy':
                trade.pl_amount = (trade.exit_price - trade.entry_price) * trade.shares
                trade.pl_percent = ((trade.exit_price - trade.entry_price) / trade.entry_price) * 100
            else:  # Sell (short)
                trade.pl_amount = (trade.entry_price - trade.exit_price) * trade.shares
                trade.pl_percent = ((trade.entry_price - trade.exit_price) / trade.entry_price) * 100
        else:
            trade.pl_amount = None
            trade.pl_percent = None
        
        db.session.commit()
        flash('Trade updated successfully!', 'success')
        return redirect(url_for('index'))
        
    return render_template('edit_trade.html', trade=trade)

@app.route('/delete_trade/<int:id>')
def delete_trade(id):
    trade = Trade.query.get_or_404(id)
    db.session.delete(trade)
    db.session.commit()
    flash('Trade deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/analytics')
def analytics():
    trades = Trade.query.all()
    
    # Basic analytics
    total_trades = len(trades)
    profitable_trades = sum(1 for trade in trades if trade.pl_amount and trade.pl_amount > 0)
    losing_trades = sum(1 for trade in trades if trade.pl_amount and trade.pl_amount < 0)
    
    win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
    
    # Total P/L
    total_pl = sum(trade.pl_amount for trade in trades if trade.pl_amount is not None)
    
    # Average P/L per trade
    avg_pl = total_pl / total_trades if total_trades > 0 else 0
    
    # Performance by ticker
    ticker_performance = {}
    for trade in trades:
        if trade.pl_amount is not None:
            if trade.ticker not in ticker_performance:
                ticker_performance[trade.ticker] = {
                    'count': 0, 
                    'total_pl': 0,
                    'wins': 0,
                    'losses': 0
                }
            
            ticker_performance[trade.ticker]['count'] += 1
            ticker_performance[trade.ticker]['total_pl'] += trade.pl_amount
            
            if trade.pl_amount > 0:
                ticker_performance[trade.ticker]['wins'] += 1
            elif trade.pl_amount < 0:
                ticker_performance[trade.ticker]['losses'] += 1
    
    return render_template('analytics.html', 
                          total_trades=total_trades,
                          profitable_trades=profitable_trades,
                          losing_trades=losing_trades,
                          win_rate=win_rate,
                          total_pl=total_pl,
                          avg_pl=avg_pl,
                          ticker_performance=ticker_performance,
                          now=datetime.now())

# Removed Dashboard route - AI Insights moved to AI Advisor page

@app.route('/calendar')
def calendar():
    try:
        # Get the month and year from the query parameters or use current month/year
        try:
            current_month = int(request.args.get('month', datetime.now().month))
            current_year = int(request.args.get('year', datetime.now().year))
        except (ValueError, TypeError):
            # If there's an error, default to current month/year
            current_month = datetime.now().month
            current_year = datetime.now().year
    
        # Calculate previous and next month/year
        if current_month == 1:
            prev_month = (12, current_year - 1)
        else:
            prev_month = (current_month - 1, current_year)
            
        if current_month == 12:
            next_month = (1, current_year + 1)
        else:
            next_month = (current_month + 1, current_year)
        
        # Get all trades for the selected month
        start_date = date(current_year, current_month, 1)
        if current_month == 12:
            end_date = date(current_year + 1, 1, 1)
        else:
            end_date = date(current_year, current_month + 1, 1)
        
        trades = Trade.query.filter(
            Trade.date >= start_date,
            Trade.date < end_date
        ).order_by(Trade.date).all()
        
        # Group trades by day
        trades_by_day = defaultdict(list)
        for trade in trades:
            if trade.date is not None:
                day_key = trade.date.strftime('%Y-%m-%d')
                trades_by_day[day_key].append(trade)
        
        # Get the first day of the month (0 = Monday, 6 = Sunday)
        first_day = date(current_year, current_month, 1)
        first_day_of_month_weekday = first_day.weekday()
        
        # Convert to Sunday-based week (0 = Sunday, 6 = Saturday)
        first_day_of_month_weekday = (first_day_of_month_weekday + 1) % 7
        
        # Get the number of days in the month
        days_in_month = cal.monthrange(current_year, current_month)[1]
        
        # Get the month name
        month_name = cal.month_name[current_month]
        
        # Monthly statistics
        monthly_stats = {
            'total_trades': len(trades),
            'trading_days': len(trades_by_day),
            'wins': sum(1 for trade in trades if trade.pl_amount is not None and trade.pl_amount > 0),
            'losses': sum(1 for trade in trades if trade.pl_amount is not None and trade.pl_amount < 0),
            'total_pl': sum(trade.pl_amount for trade in trades if trade.pl_amount is not None) or 0,
        }
        
        # Calculate win rate
        monthly_stats['win_rate'] = (monthly_stats['wins'] / monthly_stats['total_trades'] * 100) if monthly_stats['total_trades'] > 0 else 0
        
        # Calculate average P/L
        monthly_stats['avg_pl'] = monthly_stats['total_pl'] / monthly_stats['total_trades'] if monthly_stats['total_trades'] > 0 else 0
        
        # Prepare data for monthly performance chart
        chart_data = defaultdict(float)
        for day_key, day_trades in trades_by_day.items():
            # Make sure we're only summing non-None values
            day_pl = sum(trade.pl_amount for trade in day_trades if trade.pl_amount is not None)
            # Make sure we have a valid day key format
            try:
                day_num = int(day_key.split('-')[2])
                chart_data[day_num] = round(day_pl, 2)
            except (IndexError, ValueError):
                continue
        
        # Sort by day number and prepare for the chart
        chart_dates = sorted(chart_data.keys())
        chart_values = [chart_data[day] for day in chart_dates]
        
        # Add to monthly stats
        monthly_stats['chart_dates'] = [str(d) for d in chart_dates]
        monthly_stats['chart_values'] = chart_values

        # Ensure all values in monthly_stats are not None
        for key in monthly_stats:
            if monthly_stats[key] is None:
                if isinstance(monthly_stats[key], (list, dict)):
                    monthly_stats[key] = []
                elif isinstance(monthly_stats[key], (int, float)):
                    monthly_stats[key] = 0
        
        return render_template('calendar.html',
                              trades_by_day=trades_by_day,
                              current_month=current_month,
                              current_year=current_year,
                              month_name=month_name,
                              first_day_of_month_weekday=first_day_of_month_weekday,
                              days_in_month=days_in_month,
                              prev_month=prev_month,
                              next_month=next_month,
                              monthly_stats=monthly_stats)
    except Exception as e:
        # Fall back to a simplified calendar template
        try:
            # A basic simplified calendar without complex filters
            return render_template('simple/calendar.html',
                                trades_by_day=trades_by_day if 'trades_by_day' in locals() else {},
                                current_month=current_month,
                                current_year=current_year,
                                month_name=month_name if 'month_name' in locals() else cal.month_name[datetime.now().month],
                                first_day_of_month_weekday=first_day_of_month_weekday if 'first_day_of_month_weekday' in locals() else 0,
                                days_in_month=days_in_month if 'days_in_month' in locals() else 30,
                                prev_month=prev_month if 'prev_month' in locals() else (datetime.now().month-1, datetime.now().year),
                                next_month=next_month if 'next_month' in locals() else (datetime.now().month+1, datetime.now().year),
                                monthly_stats={'total_trades': 0, 'trading_days': 0})
        except Exception as inner_e:
            # If even the simplified template fails, return plain text error
            return f"Error in calendar: {str(e)}<br>Internal error: {str(inner_e)}"

@app.route('/risk_reward')
def risk_reward():
    # Get all trades with complete data for risk/reward analysis
    trades = Trade.query.filter(Trade.stop_loss.isnot(None), Trade.exit_price.isnot(None)).all()
    
    # Calculate risk and reward for each trade
    risk_reward_trades = []
    for trade in trades:
        if trade.trade_type == 'Buy':
            risk = trade.entry_price - trade.stop_loss
            reward = trade.exit_price - trade.entry_price
        else:  # Sell (short)
            risk = trade.stop_loss - trade.entry_price
            reward = trade.entry_price - trade.exit_price
        
        # Skip trades with invalid risk values
        if risk <= 0:
            continue
            
        # Calculate R/R ratio and add to list
        rr_ratio = reward / risk
        risk_reward_trades.append({
            'id': trade.id,
            'date': trade.date,
            'ticker': trade.ticker,
            'trade_type': trade.trade_type,
            'entry_price': trade.entry_price,
            'exit_price': trade.exit_price,
            'stop_loss': trade.stop_loss,
            'shares': trade.shares,
            'risk': risk,
            'reward': reward,
            'rr_ratio': rr_ratio,
            'pl_amount': trade.pl_amount
        })
    
    # Calculate overall risk/reward ratio
    if risk_reward_trades:
        overall_rr = sum(trade['rr_ratio'] for trade in risk_reward_trades) / len(risk_reward_trades)
    else:
        overall_rr = 0
    
    # Categorize trades by risk level
    low_risk = []
    medium_risk = []
    high_risk = []
    
    # Use dollar risk per share as the measurement
    for trade in risk_reward_trades:
        risk_amount = trade['risk'] * trade['shares']
        
        if risk_amount < 50:  # Less than $50 at risk
            low_risk.append(trade)
        elif risk_amount < 200:  # Between $50-$200 at risk
            medium_risk.append(trade)
        else:  # More than $200 at risk
            high_risk.append(trade)
    
    # Calculate risk distribution
    risk_distribution = {
        'low': len(low_risk),
        'medium': len(medium_risk),
        'high': len(high_risk)
    }
    
    # Calculate win rates by risk level
    def calculate_win_rate(trades_list):
        if not trades_list:
            return 0
        wins = sum(1 for t in trades_list if t['pl_amount'] and t['pl_amount'] > 0)
        return (wins / len(trades_list) * 100)
    
    def calculate_avg_return(trades_list):
        if not trades_list:
            return 0
        total_return = sum(t['pl_amount'] for t in trades_list if t['pl_amount'] is not None)
        return total_return / len(trades_list)
    
    risk_win_rates = {
        'low': calculate_win_rate(low_risk),
        'medium': calculate_win_rate(medium_risk),
        'high': calculate_win_rate(high_risk)
    }
    
    risk_returns = {
        'low': calculate_avg_return(low_risk),
        'medium': calculate_avg_return(medium_risk),
        'high': calculate_avg_return(high_risk)
    }
    
    # Get trades with best and worst R/R ratios
    sorted_by_rr = sorted(risk_reward_trades, key=lambda x: x['rr_ratio'], reverse=True)
    best_rr_trades = sorted_by_rr[:5]
    worst_rr_trades = sorted_by_rr[-5:] if len(sorted_by_rr) >= 5 else sorted_by_rr[::-1]
    
    # Prepare data for Risk vs Return scatter plot
    risk_return_data = {
        'risk': [t['risk'] * t['shares'] for t in risk_reward_trades],
        'return': [t['pl_amount'] for t in risk_reward_trades],
        'tickers': [t['ticker'] for t in risk_reward_trades]
    }
    
    # AI Risk Insights (simulated)
    risk_insights = {
        'assessment': "Your overall risk/reward ratio is good, but there's room for improvement in consistency. Your best trades have a risk/reward ratio above 3.0, which is excellent.",
        'recommendations': [
            "For technology stocks, aim for a minimum risk/reward ratio of 2.5:1 which has proven most profitable in your trading history.",
            "Consider narrowing your stop-loss range to 3-5% below entry price for long positions, which shows a higher success rate in your data.",
            "Your low-risk trades have the highest win rate, suggesting you may benefit from taking more trades with lower risk amounts rather than fewer high-risk trades."
        ],
        'key_finding': "Trades with clearly defined stop-losses have a 68% higher probability of success in your trading history."
    }
    
    return render_template('risk_reward.html',
                          overall_rr=overall_rr,
                          risk_distribution=risk_distribution,
                          risk_win_rates=risk_win_rates,
                          risk_returns=risk_returns,
                          best_rr_trades=best_rr_trades,
                          worst_rr_trades=worst_rr_trades,
                          risk_return_data=risk_return_data,
                          risk_insights=risk_insights)

@app.route('/ai_advisor')
def ai_advisor():
    # Get all trades for analysis
    trades = Trade.query.all()
    trades_with_emotions = Trade.query.filter(Trade.entry_emotion.isnot(None) | Trade.exit_emotion.isnot(None)).all()
    
    # Calculate win rate for context
    win_rate = 0
    if trades:
        profitable_trades = sum(1 for trade in trades if trade.pl_amount and trade.pl_amount > 0)
        win_rate = (profitable_trades / len(trades)) * 100 if len(trades) > 0 else 0
    
    # Add trading insights section from the dashboard
    ai_trading_insights = {
        'summary': "Your trading performance has been improving over time. Win rate has increased and your average profit per trade is up compared to the previous period.",
        'recommendations': [
            "Continue your disciplined approach with stop losses, which has significantly improved your risk management.",
            "Consider holding your winning trades longer, as there's a pattern of early exits in profitable positions.",
            "Focus more on technology and healthcare sectors where your win rate exceeds 65%."
        ],
        'pattern': "Your most profitable trades occur on market pullbacks of 2-3% followed by a reversal. Consider watching for these setups more actively."
    }
    
    # Add psychological analysis to trading insights
    if trades_with_emotions:
        # Track emotions and patterns
        emotional_insights = []
        emotional_problems = []
        
        # Analyze emotional states during trades
        entry_emotions = {}
        exit_emotions = {}
        for trade in trades_with_emotions:
            is_win = trade.pl_amount is not None and trade.pl_amount > 0
            
            # Entry emotions
            if trade.entry_emotion:
                if trade.entry_emotion not in entry_emotions:
                    entry_emotions[trade.entry_emotion] = {'wins': 0, 'total': 0}
                entry_emotions[trade.entry_emotion]['total'] += 1
                if is_win:
                    entry_emotions[trade.entry_emotion]['wins'] += 1
                    
            # Exit emotions
            if trade.exit_emotion:
                if trade.exit_emotion not in exit_emotions:
                    exit_emotions[trade.exit_emotion] = {'wins': 0, 'total': 0}
                exit_emotions[trade.exit_emotion]['total'] += 1
                if is_win:
                    exit_emotions[trade.exit_emotion]['wins'] += 1
        
        # Find best and worst emotions
        best_entry = None
        worst_entry = None
        for emotion, stats in entry_emotions.items():
            if stats['total'] >= 2:
                win_rate = (stats['wins'] / stats['total']) * 100
                if best_entry is None or win_rate > (entry_emotions[best_entry]['wins'] / entry_emotions[best_entry]['total']) * 100:
                    best_entry = emotion
                if worst_entry is None or win_rate < (entry_emotions[worst_entry]['wins'] / entry_emotions[worst_entry]['total']) * 100:
                    worst_entry = emotion
        
        # Add insights
        if best_entry and worst_entry and best_entry != worst_entry:
            best_rate = (entry_emotions[best_entry]['wins'] / entry_emotions[best_entry]['total']) * 100
            worst_rate = (entry_emotions[worst_entry]['wins'] / entry_emotions[worst_entry]['total']) * 100
            emotional_insights.append(f"Trades entered feeling '{best_entry}' have a {best_rate:.1f}% win rate vs. only {worst_rate:.1f}% when feeling '{worst_entry}'.")
        
        # Check for fear-based exits
        fearful_exits = [t for t in trades_with_emotions if t.exit_emotion == 'fearful' and t.pl_amount is not None and t.pl_amount > 0]
        if len(fearful_exits) >= 2:
            emotional_problems.append("You tend to exit profitable trades early when feeling fearful, potentially limiting gains.")
        
        # Check for FOMO entries
        fomo_entries = [t for t in trades_with_emotions if t.entry_emotion == 'fomo']
        if len(fomo_entries) >= 2:
            fomo_win_rate = sum(1 for t in fomo_entries if t.pl_amount is not None and t.pl_amount > 0) / len(fomo_entries) * 100
            if fomo_win_rate < win_rate * 0.8:
                emotional_problems.append(f"FOMO-driven entries have a low {fomo_win_rate:.1f}% win rate, suggesting impulsive decisions may be hurting performance.")
        
        # Add to trading insights
        ai_trading_insights['psychology'] = {
            'insights': emotional_insights,
            'problems': emotional_problems
        }
    
    # Simulated AI data for the advisor page
    ai_data = {
        'summary': ai_trading_insights['summary'],
        'recommendations': ai_trading_insights['recommendations'],
        'pattern': ai_trading_insights['pattern'],
        'psychology': ai_trading_insights.get('psychology', None),
        'performance_summary': "Based on your trading history, you've shown a consistent improvement over time with a positive trend in both win rate and average profit per trade. Your discipline in implementing stop losses has been particularly effective, reducing your average loss by 23% compared to your earlier trades.",
        'performance_score': 72,
        'strengths': [
            "Strong win rate (67%) in technology sector trades",
            "Effective risk management with consistent stop loss implementation",
            "Good discipline in position sizing, keeping risk below 2% per trade",
            "Profitable swing trading strategy with average hold time of 4.3 days"
        ],
        'improvement_areas': [
            "Tendency to exit winning trades too early (average profit: $215 vs potential: $340)",
            "Inconsistent performance in volatile market conditions",
            "Lower win rate (42%) in financial sector trades",
            "Higher than average drawdowns during market corrections"
        ],
        'patterns': [
            {
                'name': "Early Exit Pattern",
                'description': "You frequently exit winning trades at around 5-7% profit, but analysis shows these trades often continue to 12-15% gains afterward.",
                'confidence': 87
            },
            {
                'name': "Sector Strength",
                'description': "Your trading performance is significantly better in technology and healthcare sectors compared to financials and energy.",
                'confidence': 92
            },
            {
                'name': "Market Condition Sensitivity",
                'description': "Your win rate drops from 68% to 41% during high-volatility periods (VIX > 25).",
                'confidence': 78
            }
        ],
        'recommendations': [
            {
                'title': "Implement Scaling Out Strategy",
                'description': "To address the early exit pattern, consider selling 50% of your position at your current target and holding the remainder with a trailing stop.",
                'action_items': [
                    "Set 50% position exit at 7% profit",
                    "Move stop loss to breakeven after first partial exit",
                    "Use 10% trailing stop on remaining position"
                ]
            },
            {
                'title': "Sector Focus Optimization",
                'description': "Allocate more capital to sectors where you've shown consistent edge.",
                'action_items': [
                    "Increase allocation to technology and healthcare stocks to 60-70% of portfolio",
                    "Reduce or eliminate trades in financial sector until strategy is refined",
                    "Consider paper trading new sectors before committing real capital"
                ]
            },
            {
                'title': "Volatility-Based Position Sizing",
                'description': "Adjust position sizes based on market volatility conditions.",
                'action_items': [
                    "Reduce position size by 30-40% when VIX is above 25",
                    "Focus on stocks with beta < 1.5 during high volatility periods",
                    "Consider adding inverse ETF hedges during market corrections"
                ]
            }
        ],
        'best_setups': [
            {
                'name': "Pullback to Moving Average",
                'description': "Buying established uptrend stocks on pullbacks to the 20-day moving average.",
                'win_rate': 74,
                'avg_return': 267.50,
                'occurrences': 23
            },
            {
                'name': "Earnings Gap and Go",
                'description': "Buying stocks that gap up on earnings and continue upward momentum.",
                'win_rate': 68,
                'avg_return': 352.75,
                'occurrences': 17
            },
            {
                'name': "Sector Rotation",
                'description': "Entering stocks in sectors showing new relative strength compared to the broader market.",
                'win_rate': 61,
                'avg_return': 198.30,
                'occurrences': 28
            }
        ]
    }
    
    # Add detailed psychological analysis if we have data
    if trades_with_emotions:
        # Track win rates by emotional state
        entry_emotions = {}
        exit_emotions = {}
        followed_plan_success = {'followed': 0, 'followed_total': 0, 'deviated': 0, 'deviated_total': 0}
        
        # Analyze trading psychology
        for trade in trades_with_emotions:
            is_win = trade.pl_amount is not None and trade.pl_amount > 0
            
            # Track entry emotions
            if trade.entry_emotion:
                if trade.entry_emotion not in entry_emotions:
                    entry_emotions[trade.entry_emotion] = {'wins': 0, 'total': 0, 'pl': 0}
                entry_emotions[trade.entry_emotion]['total'] += 1
                if is_win:
                    entry_emotions[trade.entry_emotion]['wins'] += 1
                if trade.pl_amount:
                    entry_emotions[trade.entry_emotion]['pl'] += trade.pl_amount
            
            # Track exit emotions
            if trade.exit_emotion:
                if trade.exit_emotion not in exit_emotions:
                    exit_emotions[trade.exit_emotion] = {'wins': 0, 'total': 0, 'pl': 0}
                exit_emotions[trade.exit_emotion]['total'] += 1
                if is_win:
                    exit_emotions[trade.exit_emotion]['wins'] += 1
                if trade.pl_amount:
                    exit_emotions[trade.exit_emotion]['pl'] += trade.pl_amount
            
            # Track plan adherence
            if trade.followed_plan is not None and trade.pl_amount is not None:
                if trade.followed_plan:
                    followed_plan_success['followed_total'] += 1
                    if is_win:
                        followed_plan_success['followed'] += 1
                else:
                    followed_plan_success['deviated_total'] += 1
                    if is_win:
                        followed_plan_success['deviated'] += 1
        
        # Calculate win rates by emotion
        emotions_data = []
        best_entry_emotion = None
        worst_entry_emotion = None
        
        for emotion, stats in entry_emotions.items():
            if stats['total'] >= 2:  # Only consider emotions with at least 2 trades
                stats['win_rate'] = (stats['wins'] / stats['total']) * 100
                stats['avg_pl'] = stats['pl'] / stats['total']
                
                emotions_data.append({
                    'emotion': emotion,
                    'type': 'entry',
                    'win_rate': round(stats['win_rate'], 1),
                    'avg_pl': round(stats['avg_pl'], 2),
                    'count': stats['total']
                })
                
                if best_entry_emotion is None or stats['win_rate'] > entry_emotions[best_entry_emotion]['win_rate']:
                    best_entry_emotion = emotion
                
                if worst_entry_emotion is None or stats['win_rate'] < entry_emotions[worst_entry_emotion]['win_rate']:
                    worst_entry_emotion = emotion
        
        for emotion, stats in exit_emotions.items():
            if stats['total'] >= 2:  # Only consider emotions with at least 2 trades
                stats['win_rate'] = (stats['wins'] / stats['total']) * 100
                stats['avg_pl'] = stats['pl'] / stats['total']
                
                emotions_data.append({
                    'emotion': emotion,
                    'type': 'exit',
                    'win_rate': round(stats['win_rate'], 1),
                    'avg_pl': round(stats['avg_pl'], 2),
                    'count': stats['total']
                })
        
        # Calculate plan adherence win rates
        followed_plan_win_rate = (followed_plan_success['followed'] / followed_plan_success['followed_total'] * 100) if followed_plan_success['followed_total'] > 0 else 0
        deviated_plan_win_rate = (followed_plan_success['deviated'] / followed_plan_success['deviated_total'] * 100) if followed_plan_success['deviated_total'] > 0 else 0
        
        plan_adherence_data = [
            {'label': 'Followed Plan', 'win_rate': round(followed_plan_win_rate, 1), 'count': followed_plan_success['followed_total']},
            {'label': 'Deviated from Plan', 'win_rate': round(deviated_plan_win_rate, 1), 'count': followed_plan_success['deviated_total']}
        ]
        
        # Generate psychological insights
        psychological_insights = []
        
        if best_entry_emotion and worst_entry_emotion and best_entry_emotion != worst_entry_emotion:
            psychological_insights.append({
                'title': 'Emotional Impact on Entries',
                'insight': f"Trades entered feeling '{best_entry_emotion.capitalize()}' have a {entry_emotions[best_entry_emotion]['win_rate']:.1f}% win rate vs. only {entry_emotions[worst_entry_emotion]['win_rate']:.1f}% when feeling '{worst_entry_emotion.capitalize()}'.",
                'recommendation': f"Try to cultivate a '{best_entry_emotion}' mindset before entering trades. Consider journaling or meditation to manage '{worst_entry_emotion}' emotions."
            })
        
        if followed_plan_success['followed_total'] > 0 and followed_plan_success['deviated_total'] > 0:
            plan_diff = followed_plan_win_rate - deviated_plan_win_rate
            if plan_diff > 10:  # Only if there's a significant difference
                psychological_insights.append({
                    'title': 'Trading Plan Discipline',
                    'insight': f"Following your trading plan yields a {followed_plan_win_rate:.1f}% win rate vs. {deviated_plan_win_rate:.1f}% when deviating from it.",
                    'recommendation': "Strengthen your trading discipline by writing down your rules before each session and reviewing adherence afterward."
                })
        
        # Find potentially problematic emotional patterns
        emotion_problems = []
        
        # Check for fear-based early exits in profitable trades
        fearful_exits = [t for t in trades_with_emotions if t.exit_emotion == 'fearful' and t.pl_amount is not None and t.pl_amount > 0]
        if len(fearful_exits) >= 2:
            avg_holding = sum([t.holding_period for t in fearful_exits if t.holding_period is not None]) / len([t for t in fearful_exits if t.holding_period is not None]) if any(t.holding_period is not None for t in fearful_exits) else 0
            avg_holding_all = sum([t.holding_period for t in trades if t.holding_period is not None]) / len([t for t in trades if t.holding_period is not None]) if any(t.holding_period is not None for t in trades) else 0
            
            if avg_holding > 0 and avg_holding_all > 0 and avg_holding < avg_holding_all * 0.7:
                emotion_problems.append({
                    'problem': "Fear-Based Early Exits",
                    'description': "You tend to exit profitable trades early when feeling fearful, potentially limiting gains.",
                    'solution': "Set predetermined exit points and consider using trailing stops to let winners run while managing risk."
                })
        
        # Check for FOMO entries
        fomo_entries = [t for t in trades_with_emotions if t.entry_emotion == 'fomo']
        if len(fomo_entries) >= 2:
            fomo_win_rate = sum(1 for t in fomo_entries if t.pl_amount is not None and t.pl_amount > 0) / len(fomo_entries) * 100
            if fomo_win_rate < win_rate * 0.8:  # If FOMO win rate is significantly lower than overall
                emotion_problems.append({
                    'problem': "FOMO-Driven Entries",
                    'description': f"FOMO-driven entries have a low {fomo_win_rate:.1f}% win rate, suggesting impulsive decisions may be hurting performance.",
                    'solution': "Implement a mandatory cooling-off period before entering trades that weren't in your watchlist or pre-planned."
                })
        
        # Add psychological data to ai_data
        ai_data['psychology'] = {
            'emotions_data': emotions_data,
            'plan_adherence': plan_adherence_data,
            'insights': psychological_insights,
            'problems': emotion_problems
        }
    
    # Get the AI answer if provided
    ai_answer = request.args.get('answer', None)
    
    return render_template('ai_advisor.html', ai_data=ai_data, ai_answer=ai_answer)

@app.route('/ai_question', methods=['POST'])
def ai_question():
    question = request.form.get('question', '')
    
    # In a real app, you would process this question with an AI model
    # Here we just redirect back with a simulated answer
    sample_answers = [
        "Based on your trading history, you should focus on technology stocks like AAPL, MSFT, and NVDA as they've given you the best win rate (73%) compared to other sectors.",
        "To improve your win rate, consider holding your winning trades longer. Your data shows you tend to exit profitable trades after an average of 2.3 days, while your most successful trades were held for 4-7 days.",
        "Your risk management could be improved by setting more consistent stop losses. I notice that trades with a defined stop loss have a 67% win rate compared to 41% for trades without one.",
        "The best time for you to enter trades appears to be mid-week (Tuesday-Thursday). Your Monday entries have a significantly lower success rate (38% vs. 64% for other days)."
    ]
    
    ai_answer = random.choice(sample_answers)
    
    return redirect(url_for('ai_advisor', answer=ai_answer))

@app.route('/export_csv')
def export_csv():
    trades = Trade.query.order_by(Trade.date.desc()).all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Date', 'Ticker', 'Trade Type', 'Entry Price', 'Exit Price', 'Shares',
        'Holding Period', 'Stop Loss', 'P/L Amount', 'P/L Percent',
        'Entry Reason', 'Exit Reason', 'Notes'
    ])
    
    # Write data
    for trade in trades:
        writer.writerow([
            trade.date.strftime('%Y-%m-%d'),
            trade.ticker,
            trade.trade_type,
            trade.entry_price,
            trade.exit_price or '',
            trade.shares,
            trade.holding_period or '',
            trade.stop_loss or '',
            trade.pl_amount or '',
            trade.pl_percent or '',
            trade.entry_reason or '',
            trade.exit_reason or '',
            trade.notes or ''
        ])
    
    # Prepare response
    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=trading_journal_export.csv"}
    )

@app.route('/export_excel')
def export_excel():
    trades = Trade.query.order_by(Trade.date.desc()).all()
    
    # Create pandas DataFrame
    data = []
    for trade in trades:
        data.append({
            'Date': trade.date,
            'Ticker': trade.ticker,
            'Trade Type': trade.trade_type,
            'Entry Price': trade.entry_price,
            'Exit Price': trade.exit_price,
            'Shares': trade.shares,
            'Holding Period': trade.holding_period,
            'Stop Loss': trade.stop_loss,
            'P/L Amount': trade.pl_amount,
            'P/L Percent': trade.pl_percent,
            'Entry Reason': trade.entry_reason,
            'Exit Reason': trade.exit_reason,
            'Notes': trade.notes
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Trades', index=False)
        
        # Add a simple analytics sheet
        analytics = pd.DataFrame([
            {'Metric': 'Total Trades', 'Value': len(trades)},
            {'Metric': 'Winning Trades', 'Value': sum(1 for t in trades if t.pl_amount and t.pl_amount > 0)},
            {'Metric': 'Losing Trades', 'Value': sum(1 for t in trades if t.pl_amount and t.pl_amount < 0)},
            {'Metric': 'Win Rate', 'Value': f"{(sum(1 for t in trades if t.pl_amount and t.pl_amount > 0) / len(trades) * 100):.2f}%" if trades else "0%"},
            {'Metric': 'Total P/L', 'Value': f"${sum(t.pl_amount for t in trades if t.pl_amount is not None):.2f}"},
            {'Metric': 'Average P/L', 'Value': f"${(sum(t.pl_amount for t in trades if t.pl_amount is not None) / len(trades)):.2f}" if trades else "$0.00"}
        ])
        analytics.to_excel(writer, sheet_name='Analytics', index=False)
    
    # Prepare response
    output.seek(0)
    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="trading_journal_export.xlsx"
    )

# Add a context processor to inject the current year into all templates
@app.route('/position_calculator')
def position_calculator():
    return render_template('position_calculator.html')

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)