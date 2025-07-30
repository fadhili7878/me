# MetaTrader 5 Advanced Trading Bot

A comprehensive Python-based MetaTrader 5 trading bot featuring multiple advanced strategies including KT+GMAC, Martingale, Snowball, HFT, Arbitrage, Neural Networks, and AI Model strategies.

## 🚀 Features

### Trading Strategies
- **KT + GMAC**: Klinger Oscillator combined with Guppy Multiple Averaging Crossover
- **Martingale**: Progressive position sizing after losses with risk controls
- **Snowball**: Compound winning positions for exponential growth
- **High Frequency Trading (HFT)**: Micro-trend scalping with tight spreads
- **Arbitrage**: Correlation-based pair trading strategies
- **Neural Network**: Machine learning-based predictions using RandomForest
- **AI Model**: Advanced ensemble methods with multiple technical indicators

### Key Capabilities
- ✅ **Multi-Strategy Execution**: Run multiple strategies simultaneously
- ✅ **Risk Management**: Position sizing, stop losses, and drawdown protection
- ✅ **Real-time Trading**: Live market data and order execution
- ✅ **Configuration**: JSON-based strategy and risk parameter settings
- ✅ **Logging**: Comprehensive trade and error logging
- ✅ **Backtesting Ready**: Modular design for easy backtesting integration

## 📋 Prerequisites

### Software Requirements
- Python 3.8 or higher
- MetaTrader 5 terminal installed
- MT5 account with a broker supporting algorithmic trading

### Python Dependencies
```bash
pip install -r requirements.txt
```

### TA-Lib Installation
TA-Lib requires additional setup:

**Windows:**
```bash
pip install TA-Lib
```

**Linux/macOS:**
```bash
# Install dependencies first
sudo apt-get install build-essential wget
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
pip install TA-Lib
```

## ⚙️ Configuration

### 1. MT5 Account Setup
Edit `config.json` with your MT5 credentials:

```json
{
    "account": YOUR_ACCOUNT_NUMBER,
    "password": "YOUR_PASSWORD",
    "server": "YOUR_BROKER_SERVER"
}
```

### 2. Strategy Configuration
Each strategy can be individually enabled/disabled and configured:

```json
"strategies": {
    "kt_gmac": {
        "enabled": true,
        "weight": 1.0,
        "timeframe": "M5"
    },
    "martingale": {
        "enabled": true,
        "max_levels": 5,
        "multiplier": 2
    }
}
```

### 3. Risk Management
Configure position sizing and risk limits:

```json
"risk_management": {
    "max_daily_loss": 0.05,
    "max_drawdown": 0.15,
    "position_sizing_method": "fixed_fractional"
}
```

## 🏃‍♂️ Running the Bot

### Basic Usage
```bash
python mt5_trading_bot.py
```

### Using Custom Config
```bash
python mt5_trading_bot.py --config custom_config.json
```

### Running Specific Strategies
Modify the `config.json` to enable only desired strategies:

```json
"strategies": {
    "kt_gmac": {"enabled": true},
    "martingale": {"enabled": false},
    "hft": {"enabled": true}
}
```

## 📊 Strategy Details

### 1. KT + GMAC Strategy
**Concept**: Combines Klinger Oscillator momentum with Guppy Multiple Averaging Crossover
- **Timeframe**: M5 (5-minute)
- **Signals**: Generated on EMA ribbon crossovers
- **Risk**: 1% stop loss, 2% take profit

### 2. Martingale Strategy
**Concept**: Progressive position sizing to recover from losses
- **Timeframe**: M1 (1-minute)
- **Maximum Levels**: 5 (configurable)
- **Risk Control**: Maximum exposure limits

### 3. Snowball Strategy
**Concept**: Compound profitable positions using momentum
- **Trigger**: $50+ profit threshold
- **Multiplier**: 1.5x position sizing
- **Indicator**: 10-period momentum

### 4. High Frequency Trading (HFT)
**Concept**: Rapid micro-trend following with tight spreads
- **Timeframe**: M1 (1-minute)
- **Entry**: 1+ pip movements
- **Position Size**: 50% of normal size

### 5. Arbitrage Strategy
**Concept**: Exploit price differences between correlated pairs
- **Method**: Statistical arbitrage using Z-scores
- **Threshold**: 2.0 standard deviations
- **Correlation**: 0.8+ required

### 6. Neural Network Strategy
**Concept**: Machine learning predictions using technical indicators
- **Model**: RandomForest Classifier
- **Features**: 11 technical indicators
- **Confidence**: 70%+ threshold required

### 7. AI Model Strategy
**Concept**: Advanced ensemble methods with multiple indicators
- **Features**: 20+ technical indicators
- **Timeframe**: M15 (15-minute)
- **Logic**: Multi-factor decision making

## 🛡️ Risk Management

### Position Sizing
```python
# Fixed fractional method
position_size = account_balance * risk_per_trade / stop_loss_distance
```

### Risk Controls
- **Maximum Positions**: 10 concurrent trades
- **Daily Loss Limit**: 5% of account
- **Maximum Drawdown**: 15% stop trading
- **Spread Limits**: Maximum 10 pips

### Stop Loss & Take Profit
Each strategy implements appropriate SL/TP ratios:
- **Conservative**: 1:2 risk/reward
- **Aggressive**: 1:1.5 risk/reward
- **HFT**: 1:1 with rapid execution

## 📈 Performance Monitoring

### Logging
- **Trade Logs**: All orders with strategy attribution
- **Error Logs**: System and strategy errors
- **Performance**: P&L tracking per strategy

### Metrics Tracked
- Win rate per strategy
- Average profit/loss
- Maximum drawdown
- Sharpe ratio
- Total trades executed

## 🔧 Customization

### Adding New Strategies
1. Create a new class inheriting from `BaseStrategy`
2. Implement the `generate_signals()` method
3. Add to the strategy registry in `init_strategies()`
4. Configure in `config.json`

Example:
```python
class MyCustomStrategy(BaseStrategy):
    def generate_signals(self) -> List[TradeSignal]:
        signals = []
        # Your strategy logic here
        return signals
```

### Modifying Existing Strategies
Each strategy is modular and can be modified independently:
- Change timeframes
- Adjust risk parameters
- Modify technical indicators
- Update entry/exit conditions

## ⚠️ Important Warnings

### Financial Risk
- **Demo First**: Always test on demo accounts
- **Risk Capital**: Only trade with money you can afford to lose
- **Market Risk**: All trading involves significant risk
- **No Guarantees**: Past performance doesn't guarantee future results

### Technical Risks
- **Connection**: Ensure stable internet connection
- **VPS Recommended**: For 24/7 trading
- **Backup Power**: Uninterrupted power supply
- **Monitor Positions**: Regular position monitoring required

### Legal Considerations
- Check local regulations for algorithmic trading
- Ensure broker allows automated trading
- Comply with tax obligations
- Understand terms of service

## 🐛 Troubleshooting

### Common Issues

**MT5 Connection Failed**
```
Error: MT5 initialization failed
Solution: Check MT5 is running and credentials are correct
```

**Missing TA-Lib**
```
Error: No module named 'talib'
Solution: Install TA-Lib properly (see installation section)
```

**Strategy Not Executing**
```
Issue: No trades being placed
Check: 
1. Strategy is enabled in config.json
2. Market is open
3. Sufficient account balance
4. Risk limits not exceeded
```

### Debug Mode
Enable detailed logging:
```json
"logging": {
    "level": "DEBUG"
}
```

## 📞 Support

### Documentation
- Strategy explanations in code comments
- Configuration examples provided
- Error handling with descriptive messages

### Community
- Review code for improvements
- Submit issues for bugs
- Contribute new strategies
- Share configuration optimizations

## 📜 License

This project is provided for educational purposes. Users are responsible for:
- Testing thoroughly before live trading
- Understanding all risks involved
- Complying with local regulations
- Using appropriate risk management

## 🙏 Disclaimer

**USE AT YOUR OWN RISK**

This trading bot is provided as-is without any warranties. The authors are not responsible for any financial losses. Trading forex and CFDs involves significant risk and may not be suitable for all investors. Always seek independent financial advice and never trade with money you cannot afford to lose.

---

**Happy Trading! 🚀📈**