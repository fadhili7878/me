"""
Strategy Manager Module for MT5 Trading Bot
Provides advanced strategy management, performance tracking, and optimization
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass, asdict
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class StrategyPerformance:
    strategy_name: str
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    total_profit: float = 0.0
    total_loss: float = 0.0
    max_drawdown: float = 0.0
    win_rate: float = 0.0
    avg_profit: float = 0.0
    avg_loss: float = 0.0
    profit_factor: float = 0.0
    sharpe_ratio: float = 0.0
    last_updated: datetime = None

@dataclass
class TradeRecord:
    timestamp: datetime
    strategy: str
    symbol: str
    action: str
    volume: float
    entry_price: float
    exit_price: float = None
    sl: float = None
    tp: float = None
    profit: float = None
    status: str = "OPEN"  # OPEN, CLOSED, CANCELLED

class StrategyManager:
    def __init__(self, config: dict, db_path: str = "trading_data.db"):
        self.config = config
        self.db_path = db_path
        self.performance_metrics = {}
        self.trade_history = []
        self.active_trades = {}
        
        # Initialize database
        self.init_database()
        
        # Load historical performance
        self.load_performance_data()
        
    def init_database(self):
        """Initialize SQLite database for trade tracking"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create trades table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    strategy TEXT,
                    symbol TEXT,
                    action TEXT,
                    volume REAL,
                    entry_price REAL,
                    exit_price REAL,
                    sl REAL,
                    tp REAL,
                    profit REAL,
                    status TEXT
                )
            ''')
            
            # Create performance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance (
                    strategy_name TEXT PRIMARY KEY,
                    total_trades INTEGER,
                    winning_trades INTEGER,
                    losing_trades INTEGER,
                    total_profit REAL,
                    total_loss REAL,
                    max_drawdown REAL,
                    win_rate REAL,
                    avg_profit REAL,
                    avg_loss REAL,
                    profit_factor REAL,
                    sharpe_ratio REAL,
                    last_updated TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def record_trade(self, trade_record: TradeRecord):
        """Record a new trade in the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO trades (timestamp, strategy, symbol, action, volume,
                                  entry_price, exit_price, sl, tp, profit, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                trade_record.timestamp.isoformat(),
                trade_record.strategy,
                trade_record.symbol,
                trade_record.action,
                trade_record.volume,
                trade_record.entry_price,
                trade_record.exit_price,
                trade_record.sl,
                trade_record.tp,
                trade_record.profit,
                trade_record.status
            ))
            
            conn.commit()
            conn.close()
            
            # Update performance metrics
            self.update_strategy_performance(trade_record.strategy)
            
        except Exception as e:
            logger.error(f"Error recording trade: {e}")
    
    def update_trade(self, trade_id: int, exit_price: float, profit: float, status: str):
        """Update an existing trade when closed"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE trades 
                SET exit_price = ?, profit = ?, status = ?
                WHERE id = ?
            ''', (exit_price, profit, status, trade_id))
            
            # Get strategy name for performance update
            cursor.execute('SELECT strategy FROM trades WHERE id = ?', (trade_id,))
            strategy = cursor.fetchone()[0]
            
            conn.commit()
            conn.close()
            
            # Update performance metrics
            self.update_strategy_performance(strategy)
            
        except Exception as e:
            logger.error(f"Error updating trade: {e}")
    
    def update_strategy_performance(self, strategy_name: str):
        """Calculate and update performance metrics for a strategy"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(
                'SELECT * FROM trades WHERE strategy = ? AND status = "CLOSED"',
                conn, params=(strategy_name,)
            )
            conn.close()
            
            if df.empty:
                return
            
            # Calculate metrics
            total_trades = len(df)
            winning_trades = len(df[df['profit'] > 0])
            losing_trades = len(df[df['profit'] < 0])
            total_profit = df[df['profit'] > 0]['profit'].sum()
            total_loss = abs(df[df['profit'] < 0]['profit'].sum())
            
            win_rate = winning_trades / total_trades if total_trades > 0 else 0
            avg_profit = total_profit / winning_trades if winning_trades > 0 else 0
            avg_loss = total_loss / losing_trades if losing_trades > 0 else 0
            profit_factor = total_profit / total_loss if total_loss > 0 else float('inf')
            
            # Calculate maximum drawdown
            df['cumulative_profit'] = df['profit'].cumsum()
            df['running_max'] = df['cumulative_profit'].expanding().max()
            df['drawdown'] = df['running_max'] - df['cumulative_profit']
            max_drawdown = df['drawdown'].max()
            
            # Calculate Sharpe ratio (simplified)
            returns = df['profit'] / df['entry_price']
            sharpe_ratio = returns.mean() / returns.std() if returns.std() > 0 else 0
            
            # Create performance object
            performance = StrategyPerformance(
                strategy_name=strategy_name,
                total_trades=total_trades,
                winning_trades=winning_trades,
                losing_trades=losing_trades,
                total_profit=total_profit,
                total_loss=total_loss,
                max_drawdown=max_drawdown,
                win_rate=win_rate,
                avg_profit=avg_profit,
                avg_loss=avg_loss,
                profit_factor=profit_factor,
                sharpe_ratio=sharpe_ratio,
                last_updated=datetime.now()
            )
            
            # Save to database
            self.save_performance_data(performance)
            self.performance_metrics[strategy_name] = performance
            
        except Exception as e:
            logger.error(f"Error updating performance for {strategy_name}: {e}")
    
    def save_performance_data(self, performance: StrategyPerformance):
        """Save performance data to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO performance 
                (strategy_name, total_trades, winning_trades, losing_trades,
                 total_profit, total_loss, max_drawdown, win_rate,
                 avg_profit, avg_loss, profit_factor, sharpe_ratio, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                performance.strategy_name,
                performance.total_trades,
                performance.winning_trades,
                performance.losing_trades,
                performance.total_profit,
                performance.total_loss,
                performance.max_drawdown,
                performance.win_rate,
                performance.avg_profit,
                performance.avg_loss,
                performance.profit_factor,
                performance.sharpe_ratio,
                performance.last_updated.isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving performance data: {e}")
    
    def load_performance_data(self):
        """Load historical performance data from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM performance')
            rows = cursor.fetchall()
            
            for row in rows:
                performance = StrategyPerformance(
                    strategy_name=row[0],
                    total_trades=row[1],
                    winning_trades=row[2],
                    losing_trades=row[3],
                    total_profit=row[4],
                    total_loss=row[5],
                    max_drawdown=row[6],
                    win_rate=row[7],
                    avg_profit=row[8],
                    avg_loss=row[9],
                    profit_factor=row[10],
                    sharpe_ratio=row[11],
                    last_updated=datetime.fromisoformat(row[12])
                )
                self.performance_metrics[performance.strategy_name] = performance
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error loading performance data: {e}")
    
    def get_strategy_performance(self, strategy_name: str) -> Optional[StrategyPerformance]:
        """Get performance metrics for a specific strategy"""
        return self.performance_metrics.get(strategy_name)
    
    def get_all_performance(self) -> Dict[str, StrategyPerformance]:
        """Get performance metrics for all strategies"""
        return self.performance_metrics.copy()
    
    def should_disable_strategy(self, strategy_name: str) -> bool:
        """Determine if a strategy should be disabled based on performance"""
        performance = self.get_strategy_performance(strategy_name)
        
        if not performance or performance.total_trades < 10:
            return False
        
        # Disable criteria
        if (performance.win_rate < 0.3 or  # Win rate below 30%
            performance.profit_factor < 0.5 or  # Poor profit factor
            performance.max_drawdown > 0.2):  # Drawdown above 20%
            
            logger.warning(f"Strategy {strategy_name} performance poor, consider disabling")
            return True
        
        return False
    
    def optimize_strategy_weights(self) -> Dict[str, float]:
        """Optimize strategy weights based on performance"""
        weights = {}
        total_score = 0
        
        for strategy_name, performance in self.performance_metrics.items():
            if performance.total_trades < 5:
                weights[strategy_name] = 1.0  # Default weight for new strategies
            else:
                # Calculate performance score
                score = (
                    performance.win_rate * 0.3 +
                    min(performance.profit_factor, 5) * 0.3 +
                    max(0, 1 - performance.max_drawdown) * 0.2 +
                    min(performance.sharpe_ratio, 3) * 0.2
                )
                weights[strategy_name] = max(0.1, score)  # Minimum weight of 0.1
                total_score += weights[strategy_name]
        
        # Normalize weights
        if total_score > 0:
            for strategy_name in weights:
                weights[strategy_name] /= total_score
        
        return weights
    
    def get_trade_history(self, strategy_name: str = None, 
                         days: int = 30) -> pd.DataFrame:
        """Get trade history for analysis"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            if strategy_name:
                query = '''
                    SELECT * FROM trades 
                    WHERE strategy = ? AND timestamp >= ?
                    ORDER BY timestamp DESC
                '''
                cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
                df = pd.read_sql_query(query, conn, params=(strategy_name, cutoff_date))
            else:
                query = '''
                    SELECT * FROM trades 
                    WHERE timestamp >= ?
                    ORDER BY timestamp DESC
                '''
                cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
                df = pd.read_sql_query(query, conn, params=(cutoff_date,))
            
            conn.close()
            
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting trade history: {e}")
            return pd.DataFrame()
    
    def generate_performance_report(self) -> str:
        """Generate a comprehensive performance report"""
        report = []
        report.append("=== TRADING BOT PERFORMANCE REPORT ===")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        total_profit = 0
        total_trades = 0
        
        for strategy_name, performance in self.performance_metrics.items():
            report.append(f"Strategy: {strategy_name}")
            report.append("-" * 40)
            report.append(f"Total Trades: {performance.total_trades}")
            report.append(f"Win Rate: {performance.win_rate:.2%}")
            report.append(f"Total Profit: ${performance.total_profit:.2f}")
            report.append(f"Total Loss: ${performance.total_loss:.2f}")
            report.append(f"Net P&L: ${performance.total_profit - performance.total_loss:.2f}")
            report.append(f"Profit Factor: {performance.profit_factor:.2f}")
            report.append(f"Max Drawdown: {performance.max_drawdown:.2%}")
            report.append(f"Sharpe Ratio: {performance.sharpe_ratio:.2f}")
            report.append("")
            
            total_profit += performance.total_profit - performance.total_loss
            total_trades += performance.total_trades
        
        report.append("=== OVERALL SUMMARY ===")
        report.append(f"Total Net P&L: ${total_profit:.2f}")
        report.append(f"Total Trades: {total_trades}")
        report.append("")
        
        return "\n".join(report)
    
    def export_data(self, export_path: str = "trading_data_export.json"):
        """Export all trading data to JSON file"""
        try:
            export_data = {
                "performance_metrics": {
                    name: asdict(perf) for name, perf in self.performance_metrics.items()
                },
                "export_timestamp": datetime.now().isoformat()
            }
            
            # Convert datetime objects to strings
            for strategy_data in export_data["performance_metrics"].values():
                if strategy_data["last_updated"]:
                    strategy_data["last_updated"] = strategy_data["last_updated"].isoformat()
            
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Data exported to {export_path}")
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
    
    def reset_strategy_performance(self, strategy_name: str):
        """Reset performance metrics for a strategy"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete performance record
            cursor.execute('DELETE FROM performance WHERE strategy_name = ?', (strategy_name,))
            
            # Optionally delete trade history (uncomment if needed)
            # cursor.execute('DELETE FROM trades WHERE strategy = ?', (strategy_name,))
            
            conn.commit()
            conn.close()
            
            # Remove from memory
            if strategy_name in self.performance_metrics:
                del self.performance_metrics[strategy_name]
            
            logger.info(f"Reset performance for strategy: {strategy_name}")
            
        except Exception as e:
            logger.error(f"Error resetting strategy performance: {e}")