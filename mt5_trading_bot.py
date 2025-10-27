import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import time
import threading
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple
import json
from dataclasses import dataclass
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import talib
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class TradeSignal:
    symbol: str
    action: str  # 'BUY' or 'SELL'
    volume: float
    sl: float = None
    tp: float = None
    strategy: str = ""

@dataclass
class Position:
    ticket: int
    symbol: str
    volume: float
    type: int
    open_price: float
    sl: float
    tp: float
    profit: float

class MT5TradingBot:
    def __init__(self, config_file: str = "config.json"):
        self.config = self.load_config(config_file)
        self.strategies = {}
        self.active_positions = {}
        self.running = False
        self.ai_model = None
        self.scaler = StandardScaler()
        
        # Initialize strategies
        self.init_strategies()
        
    def load_config(self, config_file: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found, using defaults")
            return self.get_default_config()
    
    def get_default_config(self) -> dict:
        """Return default configuration"""
        return {
            "account": 123456,
            "password": "your_password",
            "server": "your_broker_server",
            "symbols": ["EURUSD", "GBPUSD", "USDJPY", "USDCHF"],
            "risk_per_trade": 0.02,
            "max_positions": 10,
            "strategies": {
                "kt_gmac": {"enabled": True, "weight": 1.0},
                "martingale": {"enabled": True, "weight": 1.0, "max_levels": 5},
                "snowball": {"enabled": True, "weight": 1.0},
                "hft": {"enabled": True, "weight": 1.0, "min_spread": 1},
                "arbitrage": {"enabled": True, "weight": 1.0},
                "neural": {"enabled": True, "weight": 1.0},
                "ai_model": {"enabled": True, "weight": 1.0}
            }
        }
    
    def connect_mt5(self) -> bool:
        """Connect to MetaTrader 5"""
        if not mt5.initialize():
            logger.error("MT5 initialization failed")
            return False
        
        # Login to account
        if not mt5.login(
            login=self.config["account"],
            password=self.config["password"],
            server=self.config["server"]
        ):
            logger.error("MT5 login failed")
            return False
        
        logger.info("Successfully connected to MT5")
        return True
    
    def disconnect_mt5(self):
        """Disconnect from MetaTrader 5"""
        mt5.shutdown()
        logger.info("Disconnected from MT5")
    
    def get_market_data(self, symbol: str, timeframe: int, count: int = 100) -> pd.DataFrame:
        """Get market data for a symbol"""
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        if rates is None:
            return pd.DataFrame()
        
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df
    
    def calculate_position_size(self, symbol: str, risk_percent: float = None) -> float:
        """Calculate position size based on risk management"""
        if risk_percent is None:
            risk_percent = self.config["risk_per_trade"]
        
        account_info = mt5.account_info()
        if account_info is None:
            return 0.01
        
        balance = account_info.balance
        risk_amount = balance * risk_percent
        
        # Get symbol info for tick value calculation
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return 0.01
        
        # Simple position sizing (can be enhanced)
        lot_size = min(risk_amount / 1000, symbol_info.volume_max)
        return max(lot_size, symbol_info.volume_min)
    
    def send_order(self, signal: TradeSignal) -> bool:
        """Send trading order to MT5"""
        symbol_info = mt5.symbol_info(signal.symbol)
        if symbol_info is None:
            logger.error(f"Symbol {signal.symbol} not found")
            return False
        
        if not symbol_info.visible:
            if not mt5.symbol_select(signal.symbol, True):
                logger.error(f"Failed to select symbol {signal.symbol}")
                return False
        
        # Determine order type
        order_type = mt5.ORDER_TYPE_BUY if signal.action == "BUY" else mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(signal.symbol).ask if signal.action == "BUY" else mt5.symbol_info_tick(signal.symbol).bid
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": signal.symbol,
            "volume": signal.volume,
            "type": order_type,
            "price": price,
            "sl": signal.sl,
            "tp": signal.tp,
            "deviation": 20,
            "magic": 123456,
            "comment": f"Bot_{signal.strategy}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Order failed: {result.comment}")
            return False
        
        logger.info(f"Order successful: {signal.strategy} {signal.action} {signal.volume} {signal.symbol}")
        return True
    
    def close_position(self, ticket: int) -> bool:
        """Close an open position"""
        positions = mt5.positions_get(ticket=ticket)
        if not positions:
            return False
        
        position = positions[0]
        order_type = mt5.ORDER_TYPE_SELL if position.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(position.symbol).bid if position.type == mt5.POSITION_TYPE_BUY else mt5.symbol_info_tick(position.symbol).ask
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": order_type,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": 123456,
            "comment": "Bot_close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        return result.retcode == mt5.TRADE_RETCODE_DONE
    
    def init_strategies(self):
        """Initialize all trading strategies"""
        self.strategies = {
            "kt_gmac": KTGMACStrategy(self),
            "martingale": MartingaleStrategy(self),
            "snowball": SnowballStrategy(self),
            "hft": HFTStrategy(self),
            "arbitrage": ArbitrageStrategy(self),
            "neural": NeuralStrategy(self),
            "ai_model": AIModelStrategy(self)
        }
    
    def run_strategies(self):
        """Run all enabled strategies"""
        while self.running:
            try:
                for name, strategy in self.strategies.items():
                    if self.config["strategies"][name]["enabled"]:
                        signals = strategy.generate_signals()
                        for signal in signals:
                            if self.should_execute_trade(signal):
                                self.send_order(signal)
                
                time.sleep(1)  # Wait 1 second between iterations
                
            except Exception as e:
                logger.error(f"Error in strategy execution: {e}")
                time.sleep(5)
    
    def should_execute_trade(self, signal: TradeSignal) -> bool:
        """Check if trade should be executed based on risk management"""
        # Check maximum positions
        positions = mt5.positions_total()
        if positions >= self.config["max_positions"]:
            return False
        
        # Additional risk checks can be added here
        return True
    
    def start(self):
        """Start the trading bot"""
        if not self.connect_mt5():
            return False
        
        self.running = True
        logger.info("Trading bot started")
        
        # Start strategy execution in a separate thread
        strategy_thread = threading.Thread(target=self.run_strategies)
        strategy_thread.daemon = True
        strategy_thread.start()
        
        return True
    
    def stop(self):
        """Stop the trading bot"""
        self.running = False
        self.disconnect_mt5()
        logger.info("Trading bot stopped")

class BaseStrategy:
    """Base class for all trading strategies"""
    def __init__(self, bot: MT5TradingBot):
        self.bot = bot
        self.name = self.__class__.__name__
    
    def generate_signals(self) -> List[TradeSignal]:
        """Generate trading signals - to be implemented by subclasses"""
        raise NotImplementedError

class KTGMACStrategy(BaseStrategy):
    """KT + GMAC Strategy - Combining Klinger Oscillator with GMAC"""
    
    def generate_signals(self) -> List[TradeSignal]:
        signals = []
        
        for symbol in self.bot.config["symbols"]:
            try:
                df = self.bot.get_market_data(symbol, mt5.TIMEFRAME_M5, 200)
                if df.empty:
                    continue
                
                # Calculate Klinger Oscillator
                df['hlc3'] = (df['high'] + df['low'] + df['close']) / 3
                df['dm'] = df['high'] - df['low']
                df['cm'] = df['close'] - df['close'].shift(1)
                df['trend'] = np.where(df['cm'] > 0, 1, -1)
                df['sv'] = df['tick_volume'] * df['trend']
                
                # GMAC (Guppy Multiple Averaging Crossover)
                short_periods = [3, 5, 8, 10, 12, 15]
                long_periods = [30, 35, 40, 45, 50, 60]
                
                short_emas = [talib.EMA(df['close'], period) for period in short_periods]
                long_emas = [talib.EMA(df['close'], period) for period in long_periods]
                
                short_avg = np.mean(short_emas, axis=0)
                long_avg = np.mean(long_emas, axis=0)
                
                # Generate signals
                if len(df) > 50:
                    current_price = df['close'].iloc[-1]
                    prev_short = short_avg[-2]
                    curr_short = short_avg[-1]
                    prev_long = long_avg[-2]
                    curr_long = long_avg[-1]
                    
                    # Bullish crossover
                    if prev_short <= prev_long and curr_short > curr_long:
                        volume = self.bot.calculate_position_size(symbol)
                        sl = current_price * 0.99  # 1% stop loss
                        tp = current_price * 1.02  # 2% take profit
                        
                        signals.append(TradeSignal(
                            symbol=symbol,
                            action="BUY",
                            volume=volume,
                            sl=sl,
                            tp=tp,
                            strategy="KT_GMAC"
                        ))
                    
                    # Bearish crossover
                    elif prev_short >= prev_long and curr_short < curr_long:
                        volume = self.bot.calculate_position_size(symbol)
                        sl = current_price * 1.01  # 1% stop loss
                        tp = current_price * 0.98  # 2% take profit
                        
                        signals.append(TradeSignal(
                            symbol=symbol,
                            action="SELL",
                            volume=volume,
                            sl=sl,
                            tp=tp,
                            strategy="KT_GMAC"
                        ))
                        
            except Exception as e:
                logger.error(f"Error in KT_GMAC strategy for {symbol}: {e}")
        
        return signals

class MartingaleStrategy(BaseStrategy):
    """Martingale Strategy - Double position size after losses"""
    
    def __init__(self, bot: MT5TradingBot):
        super().__init__(bot)
        self.martingale_levels = {}
        self.max_levels = bot.config["strategies"]["martingale"]["max_levels"]
    
    def generate_signals(self) -> List[TradeSignal]:
        signals = []
        
        for symbol in self.bot.config["symbols"]:
            try:
                df = self.bot.get_market_data(symbol, mt5.TIMEFRAME_M1, 50)
                if df.empty:
                    continue
                
                # Simple trend following for martingale
                sma_20 = talib.SMA(df['close'], 20)
                current_price = df['close'].iloc[-1]
                current_sma = sma_20.iloc[-1]
                
                # Check for losing positions to apply martingale
                positions = mt5.positions_get(symbol=symbol)
                losing_positions = [p for p in positions if p.profit < 0]
                
                if losing_positions and symbol not in self.martingale_levels:
                    self.martingale_levels[symbol] = 1
                elif losing_positions:
                    self.martingale_levels[symbol] = min(
                        self.martingale_levels[symbol] + 1, 
                        self.max_levels
                    )
                else:
                    self.martingale_levels[symbol] = 0
                
                if self.martingale_levels.get(symbol, 0) < self.max_levels:
                    base_volume = self.bot.calculate_position_size(symbol)
                    martingale_multiplier = 2 ** self.martingale_levels.get(symbol, 0)
                    volume = base_volume * martingale_multiplier
                    
                    if current_price > current_sma:
                        signals.append(TradeSignal(
                            symbol=symbol,
                            action="BUY",
                            volume=volume,
                            sl=current_price * 0.995,
                            tp=current_price * 1.01,
                            strategy="Martingale"
                        ))
                    elif current_price < current_sma:
                        signals.append(TradeSignal(
                            symbol=symbol,
                            action="SELL",
                            volume=volume,
                            sl=current_price * 1.005,
                            tp=current_price * 0.99,
                            strategy="Martingale"
                        ))
                        
            except Exception as e:
                logger.error(f"Error in Martingale strategy for {symbol}: {e}")
        
        return signals

class SnowballStrategy(BaseStrategy):
    """Snowball Strategy - Compound winning positions"""
    
    def __init__(self, bot: MT5TradingBot):
        super().__init__(bot)
        self.compound_factor = 1.5
    
    def generate_signals(self) -> List[TradeSignal]:
        signals = []
        
        for symbol in self.bot.config["symbols"]:
            try:
                # Check for profitable positions to compound
                positions = mt5.positions_get(symbol=symbol)
                profitable_positions = [p for p in positions if p.profit > 50]  # $50 profit threshold
                
                if profitable_positions:
                    df = self.bot.get_market_data(symbol, mt5.TIMEFRAME_M5, 30)
                    if df.empty:
                        continue
                    
                    # Use momentum indicator for snowball entries
                    momentum = talib.MOM(df['close'], 10)
                    current_momentum = momentum.iloc[-1]
                    
                    if current_momentum > 0:  # Positive momentum
                        base_volume = self.bot.calculate_position_size(symbol)
                        compound_volume = base_volume * self.compound_factor
                        current_price = df['close'].iloc[-1]
                        
                        signals.append(TradeSignal(
                            symbol=symbol,
                            action="BUY",
                            volume=compound_volume,
                            sl=current_price * 0.997,
                            tp=current_price * 1.015,
                            strategy="Snowball"
                        ))
                    elif current_momentum < 0:  # Negative momentum
                        base_volume = self.bot.calculate_position_size(symbol)
                        compound_volume = base_volume * self.compound_factor
                        current_price = df['close'].iloc[-1]
                        
                        signals.append(TradeSignal(
                            symbol=symbol,
                            action="SELL",
                            volume=compound_volume,
                            sl=current_price * 1.003,
                            tp=current_price * 0.985,
                            strategy="Snowball"
                        ))
                        
            except Exception as e:
                logger.error(f"Error in Snowball strategy for {symbol}: {e}")
        
        return signals

class HFTStrategy(BaseStrategy):
    """High Frequency Trading Strategy"""
    
    def generate_signals(self) -> List[TradeSignal]:
        signals = []
        min_spread = self.bot.config["strategies"]["hft"]["min_spread"]
        
        for symbol in self.bot.config["symbols"]:
            try:
                tick = mt5.symbol_info_tick(symbol)
                if tick is None:
                    continue
                
                spread = (tick.ask - tick.bid) / tick.bid * 10000  # Spread in pips
                
                if spread >= min_spread:
                    # Get very short-term data
                    df = self.bot.get_market_data(symbol, mt5.TIMEFRAME_M1, 10)
                    if df.empty:
                        continue
                    
                    # Calculate micro trend
                    price_change = (df['close'].iloc[-1] - df['close'].iloc[-3]) / df['close'].iloc[-3]
                    
                    if abs(price_change) > 0.0001:  # 1 pip movement
                        volume = self.bot.calculate_position_size(symbol) * 0.5  # Smaller positions for HFT
                        
                        if price_change > 0:
                            signals.append(TradeSignal(
                                symbol=symbol,
                                action="BUY",
                                volume=volume,
                                sl=tick.ask * 0.9999,  # Very tight stop
                                tp=tick.ask * 1.0005,  # Small profit target
                                strategy="HFT"
                            ))
                        else:
                            signals.append(TradeSignal(
                                symbol=symbol,
                                action="SELL",
                                volume=volume,
                                sl=tick.bid * 1.0001,  # Very tight stop
                                tp=tick.bid * 0.9995,  # Small profit target
                                strategy="HFT"
                            ))
                            
            except Exception as e:
                logger.error(f"Error in HFT strategy for {symbol}: {e}")
        
        return signals

class ArbitrageStrategy(BaseStrategy):
    """Arbitrage Strategy - Exploit price differences"""
    
    def generate_signals(self) -> List[TradeSignal]:
        signals = []
        symbols = self.bot.config["symbols"]
        
        try:
            # Look for correlation arbitrage opportunities
            if len(symbols) >= 2:
                for i in range(len(symbols)):
                    for j in range(i + 1, len(symbols)):
                        symbol1, symbol2 = symbols[i], symbols[j]
                        
                        df1 = self.bot.get_market_data(symbol1, mt5.TIMEFRAME_M5, 50)
                        df2 = self.bot.get_market_data(symbol2, mt5.TIMEFRAME_M5, 50)
                        
                        if df1.empty or df2.empty:
                            continue
                        
                        # Calculate correlation
                        correlation = df1['close'].corr(df2['close'])
                        
                        if abs(correlation) > 0.8:  # Strong correlation
                            # Calculate price ratio
                            ratio = df1['close'].iloc[-1] / df2['close'].iloc[-1]
                            ratio_mean = (df1['close'] / df2['close']).mean()
                            ratio_std = (df1['close'] / df2['close']).std()
                            
                            # Z-score for mean reversion
                            z_score = (ratio - ratio_mean) / ratio_std
                            
                            if z_score > 2:  # Ratio too high, expect reversion
                                volume = self.bot.calculate_position_size(symbol1)
                                signals.append(TradeSignal(
                                    symbol=symbol1,
                                    action="SELL",
                                    volume=volume,
                                    strategy="Arbitrage"
                                ))
                                signals.append(TradeSignal(
                                    symbol=symbol2,
                                    action="BUY",
                                    volume=volume,
                                    strategy="Arbitrage"
                                ))
                            elif z_score < -2:  # Ratio too low, expect reversion
                                volume = self.bot.calculate_position_size(symbol1)
                                signals.append(TradeSignal(
                                    symbol=symbol1,
                                    action="BUY",
                                    volume=volume,
                                    strategy="Arbitrage"
                                ))
                                signals.append(TradeSignal(
                                    symbol=symbol2,
                                    action="SELL",
                                    volume=volume,
                                    strategy="Arbitrage"
                                ))
                                
        except Exception as e:
            logger.error(f"Error in Arbitrage strategy: {e}")
        
        return signals

class NeuralStrategy(BaseStrategy):
    """Neural Network Trading Strategy"""
    
    def __init__(self, bot: MT5TradingBot):
        super().__init__(bot)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self.feature_columns = []
    
    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare features for neural network"""
        if df.empty or len(df) < 50:
            return np.array([])
        
        features = []
        
        # Technical indicators
        df['sma_20'] = talib.SMA(df['close'], 20)
        df['ema_12'] = talib.EMA(df['close'], 12)
        df['rsi'] = talib.RSI(df['close'], 14)
        df['macd'], df['macd_signal'], _ = talib.MACD(df['close'])
        df['bb_upper'], df['bb_middle'], df['bb_lower'] = talib.BBANDS(df['close'])
        
        # Price features
        df['price_change'] = df['close'].pct_change()
        df['volatility'] = df['price_change'].rolling(20).std()
        df['volume_sma'] = df['tick_volume'].rolling(20).mean()
        
        self.feature_columns = [
            'sma_20', 'ema_12', 'rsi', 'macd', 'macd_signal',
            'bb_upper', 'bb_middle', 'bb_lower', 'price_change',
            'volatility', 'volume_sma'
        ]
        
        # Create feature matrix
        feature_matrix = df[self.feature_columns].dropna()
        return feature_matrix.values
    
    def train_model(self, symbol: str):
        """Train the neural network model"""
        try:
            # Get historical data for training
            df = self.bot.get_market_data(symbol, mt5.TIMEFRAME_H1, 1000)
            if df.empty:
                return
            
            features = self.prepare_features(df)
            if len(features) == 0:
                return
            
            # Create labels (1 for price up, 0 for price down)
            df['future_return'] = df['close'].shift(-1) / df['close'] - 1
            df['label'] = (df['future_return'] > 0).astype(int)
            
            labels = df['label'].dropna().values
            
            # Align features and labels
            min_len = min(len(features), len(labels))
            features = features[:min_len]
            labels = labels[:min_len]
            
            if len(features) > 100:  # Minimum data for training
                self.model.fit(features, labels)
                self.is_trained = True
                logger.info(f"Neural model trained for {symbol}")
                
        except Exception as e:
            logger.error(f"Error training neural model for {symbol}: {e}")
    
    def generate_signals(self) -> List[TradeSignal]:
        signals = []
        
        for symbol in self.bot.config["symbols"]:
            try:
                if not self.is_trained:
                    self.train_model(symbol)
                    continue
                
                df = self.bot.get_market_data(symbol, mt5.TIMEFRAME_H1, 100)
                if df.empty:
                    continue
                
                features = self.prepare_features(df)
                if len(features) == 0:
                    continue
                
                # Predict with the latest features
                latest_features = features[-1].reshape(1, -1)
                prediction = self.model.predict(latest_features)[0]
                confidence = self.model.predict_proba(latest_features)[0].max()
                
                if confidence > 0.7:  # High confidence threshold
                    volume = self.bot.calculate_position_size(symbol)
                    current_price = df['close'].iloc[-1]
                    
                    if prediction == 1:  # Buy signal
                        signals.append(TradeSignal(
                            symbol=symbol,
                            action="BUY",
                            volume=volume,
                            sl=current_price * 0.98,
                            tp=current_price * 1.03,
                            strategy="Neural"
                        ))
                    else:  # Sell signal
                        signals.append(TradeSignal(
                            symbol=symbol,
                            action="SELL",
                            volume=volume,
                            sl=current_price * 1.02,
                            tp=current_price * 0.97,
                            strategy="Neural"
                        ))
                        
            except Exception as e:
                logger.error(f"Error in Neural strategy for {symbol}: {e}")
        
        return signals

class AIModelStrategy(BaseStrategy):
    """Advanced AI Model Strategy with ensemble methods"""
    
    def __init__(self, bot: MT5TradingBot):
        super().__init__(bot)
        self.models = {}
        self.scalers = {}
        self.prediction_history = {}
    
    def create_advanced_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create advanced features for AI model"""
        if df.empty or len(df) < 100:
            return pd.DataFrame()
        
        # Technical indicators
        df['rsi'] = talib.RSI(df['close'], 14)
        df['macd'], df['macd_signal'], df['macd_hist'] = talib.MACD(df['close'])
        df['bb_upper'], df['bb_middle'], df['bb_lower'] = talib.BBANDS(df['close'])
        df['atr'] = talib.ATR(df['high'], df['low'], df['close'], 14)
        df['cci'] = talib.CCI(df['high'], df['low'], df['close'], 14)
        df['williams_r'] = talib.WILLR(df['high'], df['low'], df['close'], 14)
        
        # Price action features
        df['hl_ratio'] = (df['high'] - df['low']) / df['close']
        df['oc_ratio'] = (df['open'] - df['close']) / df['close']
        df['volume_price'] = df['tick_volume'] * df['close']
        
        # Moving averages
        for period in [5, 10, 20, 50]:
            df[f'sma_{period}'] = talib.SMA(df['close'], period)
            df[f'ema_{period}'] = talib.EMA(df['close'], period)
        
        # Momentum features
        df['momentum'] = talib.MOM(df['close'], 10)
        df['roc'] = talib.ROC(df['close'], 10)
        
        return df
    
    def generate_signals(self) -> List[TradeSignal]:
        signals = []
        
        for symbol in self.bot.config["symbols"]:
            try:
                df = self.bot.get_market_data(symbol, mt5.TIMEFRAME_M15, 500)
                if df.empty:
                    continue
                
                df = self.create_advanced_features(df)
                
                # Simple ensemble prediction (placeholder for more advanced AI)
                df['price_change'] = df['close'].pct_change()
                df['trend'] = df['price_change'].rolling(10).mean()
                df['volatility'] = df['price_change'].rolling(20).std()
                
                current_trend = df['trend'].iloc[-1]
                current_vol = df['volatility'].iloc[-1]
                current_rsi = df['rsi'].iloc[-1]
                
                # AI decision logic (simplified)
                if (current_trend > 0.001 and current_rsi < 70 and 
                    current_vol < df['volatility'].quantile(0.8)):
                    
                    volume = self.bot.calculate_position_size(symbol)
                    current_price = df['close'].iloc[-1]
                    
                    signals.append(TradeSignal(
                        symbol=symbol,
                        action="BUY",
                        volume=volume,
                        sl=current_price * 0.985,
                        tp=current_price * 1.025,
                        strategy="AI_Model"
                    ))
                    
                elif (current_trend < -0.001 and current_rsi > 30 and 
                      current_vol < df['volatility'].quantile(0.8)):
                    
                    volume = self.bot.calculate_position_size(symbol)
                    current_price = df['close'].iloc[-1]
                    
                    signals.append(TradeSignal(
                        symbol=symbol,
                        action="SELL",
                        volume=volume,
                        sl=current_price * 1.015,
                        tp=current_price * 0.975,
                        strategy="AI_Model"
                    ))
                    
            except Exception as e:
                logger.error(f"Error in AI Model strategy for {symbol}: {e}")
        
        return signals

def main():
    """Main function to run the trading bot"""
    bot = MT5TradingBot()
    
    try:
        if bot.start():
            logger.info("Bot is running. Press Ctrl+C to stop.")
            while bot.running:
                time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    finally:
        bot.stop()

if __name__ == "__main__":
    main()