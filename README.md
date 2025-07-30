# MetaTrader 5 Advanced Trading Bot

A comprehensive Python-based MetaTrader 5 trading bot featuring multiple advanced strategies with a modern GUI interface for easy strategy selection, configuration, and monitoring.

## 🚀 Features

### Trading Strategies
- **KT + GMAC**: Klinger Oscillator combined with Guppy Multiple Averaging Crossover
- **Martingale**: Progressive position sizing after losses with risk controls
- **Snowball**: Compound winning positions for exponential growth
- **High Frequency Trading (HFT)**: Micro-trend scalping with tight spreads
- **Arbitrage**: Correlation-based pair trading strategies
- **Neural Network**: Machine learning-based predictions using RandomForest
- **AI Model**: Advanced ensemble methods with multiple technical indicators

### GUI Features
- **📊 Strategy Selection**: Easy checkboxes to enable/disable strategies
- **⚙️ Configuration Panel**: Intuitive forms for all settings
- **📈 Real-time Monitoring**: Live account info and position tracking
- **📋 Performance Analytics**: Charts and metrics for each strategy
- **🔧 System Tray Integration**: Minimize to tray with quick controls
- **📝 Live Logging**: Real-time log viewer with filtering
- **💾 Save/Load Configs**: Multiple configuration profiles

### Key Capabilities
- ✅ **Multi-Strategy Execution**: Run multiple strategies simultaneously
- ✅ **Risk Management**: Position sizing, stop losses, and drawdown protection
- ✅ **Real-time Trading**: Live market data and order execution
- ✅ **Modern GUI**: User-friendly interface with tabbed navigation
- ✅ **Configuration**: JSON-based strategy and risk parameter settings
- ✅ **Logging**: Comprehensive trade and error logging
- ✅ **Backtesting Ready**: Modular design for easy backtesting integration
- ✅ **System Tray**: Run in background with quick access controls

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

## 🖥️ GUI Usage

### 🚀 Quick Start with GUI

**Standard GUI (Traditional Interface):**
```bash
python gui_trading_bot.py
# or
python run_bot.py --mode gui
```

**🌌 Quantum GUI (Cyberpunk/Futuristic Interface):**
```bash
python launch_quantum_gui.py
# or
python run_bot.py --mode quantum-gui
```

### 🌟 Quantum Trading Matrix Interface

Experience trading like never before with our cutting-edge **Quantum Trading Matrix** - a cyberpunk-inspired interface that transforms your trading experience:

#### 🎮 Quantum Features
- **🔮 Quantum Processing Matrix**: Real-time animated qubit grid showing trading states
- **🧠 Neural Pattern Recognition**: Advanced pattern visualization with geometric indicators  
- **📊 Predictive Analytics Engine**: Bullish/bearish sentiment analysis with confidence metrics
- **💫 Quantum Data Stream**: Live trading data with color-coded neural network messages
- **🎯 Floating Controls**: Intuitive bot control panel with quantum-themed buttons
- **✨ Animated Background**: Rotating quantum dots and dynamic visual effects

#### 🎨 Visual Design
- **Dark Cyberpunk Theme**: Deep space backgrounds with neon highlights
- **Neon Color Palette**: Cyan, magenta, purple, and green accent colors
- **Futuristic Typography**: Orbitron and Courier New fonts for sci-fi aesthetics
- **Real-time Animations**: Constantly changing quantum grid and particle effects
- **Status Indicators**: "QUANTUM STATE: SUPERPOS | REALITY: SIMULATED"

### 📱 Interface Overview

The GUI provides 6 main tabs:

#### 1. **Control Tab** - Main Dashboard
- Start/Stop bot controls
- Connection status indicator
- Quick performance statistics
- MT5 connection testing

#### 2. **Strategies Tab** - Strategy Selection & Configuration
- **Enable/Disable**: Simple checkboxes for each strategy
- **Weight Settings**: Adjust allocation for each strategy
- **Parameter Tuning**: Strategy-specific settings
- **Performance Indicators**: Real-time strategy performance

#### 3. **Configuration Tab** - Account & Risk Settings
- **MT5 Account**: Account number, password, server
- **Trading Symbols**: Select currency pairs to trade
- **Risk Management**: Position sizing, drawdown limits
- **Load/Save**: Configuration file management

#### 4. **Monitoring Tab** - Real-time Data
- **Account Information**: Balance, equity, margin
- **Active Positions**: Live position tracking with P&L
- **Market Information**: Spread monitoring
- **Auto-refresh**: Updates every 5 seconds

#### 5. **Performance Tab** - Analytics & Charts
- **Performance Metrics**: Win rate, profit factor, Sharpe ratio
- **Interactive Charts**: Cumulative P&L and strategy comparison
- **Export Reports**: Generate detailed performance reports

#### 6. **Logs Tab** - System Messages
- **Real-time Logging**: All bot activities and errors
- **Log Filtering**: Filter by log level (DEBUG, INFO, WARNING, ERROR)
- **Save Logs**: Export logs to file

### 🎯 Strategy Selection Made Easy

**Enable Strategies:**
1. Go to **Strategies** tab
2. Check the boxes for desired strategies:
   - ☑️ **KT + GMAC Strategy** - Technical analysis powerhouse
   - ☑️ **Martingale Strategy** - Progressive recovery system
   - ☑️ **Snowball Strategy** - Compound your wins
   - ☑️ **High Frequency Trading** - Scalping opportunities
   - ☑️ **Arbitrage Strategy** - Market inefficiency exploitation
   - ☑️ **Neural Network Strategy** - AI-powered predictions
   - ☑️ **AI Model Strategy** - Advanced machine learning

**Configure Parameters:**
- Adjust **Weight** for capital allocation
- Fine-tune strategy-specific parameters
- Set risk levels and thresholds
- Save configuration for later use

### 🔧 System Tray Features

When minimized, the bot runs in your system tray with:
- **Quick Status**: Green (running) / Red (stopped) icon
- **Right-click Menu**:
  - Show/Hide main window
  - Start/Stop bot
  - View quick statistics
  - Access logs and settings
  - Exit application
- **Notifications**: Bot status changes and important events

## ⚙️ Configuration

### 1. MT5 Account Setup (GUI)
1. Go to **Configuration** tab
2. Enter your MT5 credentials:
   - Account Number
   - Password
   - Server
3. Click **Test MT5 Connection** to verify
4. **Save Configuration**

### 2. Strategy Selection (GUI)
1. Go to **Strategies** tab
2. Use checkboxes to enable desired strategies
3. Adjust weights and parameters as needed
4. Use **Enable All** / **Disable All** for quick setup

### 3. Risk Management (GUI)
Configure in **Configuration** tab:
- **Risk per Trade**: Percentage of capital per trade
- **Max Positions**: Maximum concurrent trades
- **Daily Loss Limit**: Stop trading after daily loss
- **Drawdown Protection**: Maximum account drawdown

## 🏃‍♂️ Running the Bot

### 🖥️ With GUI (Recommended)
```bash
python gui_trading_bot.py
```

### 💻 Command Line (Advanced)
```bash
# Basic usage
python run_bot.py

# With custom config
python run_bot.py --config my_config.json

# Generate sample config
python run_bot.py --mode sample

# View performance report
python run_bot.py --mode report
```

### 🔧 Advanced CLI Options
```bash
# List strategies
python run_bot.py --mode list

# Enable specific strategy
python run_bot.py --enable kt_gmac

# Disable strategy
python run_bot.py --disable martingale

# Dry run mode
python run_bot.py --dry-run

# Debug logging
python run_bot.py --log-level DEBUG
```

## 📊 Strategy Details

### 1. KT + GMAC Strategy
**GUI Settings**: Enable in Strategies tab
- **Timeframe**: 5-minute charts
- **Signals**: EMA ribbon crossovers with Klinger confirmation
- **Risk**: Configurable stop loss and take profit

### 2. Martingale Strategy
**GUI Settings**: Configure max levels and multiplier
- **Concept**: Double down on losses with safety limits
- **Risk Control**: Maximum 5 levels (configurable)
- **Recovery**: Designed for high win rate strategies

### 3. Snowball Strategy
**GUI Settings**: Set profit threshold and compound factor
- **Trigger**: Build on winning positions
- **Growth**: Exponential profit compounding
- **Safety**: Momentum-based entry confirmation

### 4. High Frequency Trading (HFT)
**GUI Settings**: Configure spread and movement thresholds
- **Speed**: 1-minute timeframe execution
- **Opportunity**: Micro-price movements
- **Volume**: Smaller position sizes, higher frequency

### 5. Arbitrage Strategy
**GUI Settings**: Set correlation and Z-score thresholds
- **Method**: Statistical arbitrage between pairs
- **Detection**: Price divergence identification
- **Execution**: Simultaneous long/short positions

### 6. Neural Network Strategy
**GUI Settings**: Configure confidence threshold and training periods
- **AI**: RandomForest machine learning
- **Features**: 11 technical indicators
- **Adaptation**: Continuous model retraining

### 7. AI Model Strategy
**GUI Settings**: Advanced parameter tuning available
- **Intelligence**: Ensemble methods
- **Indicators**: 20+ technical features
- **Decision**: Multi-factor analysis

## 🛡️ Risk Management

### GUI Risk Controls
Easily configure in the **Configuration** tab:

**Position Sizing**
- Risk per trade: 1-10% of account
- Maximum positions: 1-50 concurrent trades
- Auto-calculation based on account balance

**Protection Limits**
- Daily loss limit: Stop trading after X% loss
- Maximum drawdown: Emergency stop at X% drawdown
- Spread limits: Skip trades with high spreads

**Real-time Monitoring**
- Live P&L tracking in **Monitoring** tab
- Position table with current prices
- Account balance and margin display

## 📈 Performance Monitoring

### GUI Analytics
The **Performance** tab provides:

**Key Metrics Display**
- Total trades and win rate
- Profit factor and Sharpe ratio
- Maximum drawdown
- Total P&L by strategy

**Interactive Charts**
- Cumulative profit/loss over time
- Strategy performance comparison
- Export charts as images

**Real-time Updates**
- Live performance calculation
- Strategy-by-strategy breakdown
- Historical data visualization

## 🐛 Troubleshooting

### GUI Issues

**GUI Won't Start**
```bash
# Check dependencies
pip install tkinter matplotlib pillow pystray

# Try basic version
python gui_trading_bot.py
```

**System Tray Not Working**
```bash
# Install tray dependencies
pip install pystray Pillow

# Or disable tray (edit config)
```

**Charts Not Displaying**
```bash
# Install chart dependencies
pip install matplotlib seaborn plotly
```

### Common Issues

**MT5 Connection Failed**
1. Check MetaTrader 5 is running
2. Verify credentials in **Configuration** tab
3. Use **Test MT5 Connection** button
4. Check server name format

**Strategy Not Trading**
1. Verify strategy is enabled in **Strategies** tab
2. Check market hours
3. Review risk limits in **Configuration**
4. Monitor **Logs** tab for errors

**Performance Issues**
1. Reduce number of active strategies
2. Increase timeframes for less frequent trading
3. Check system resources
4. Monitor **Performance** tab

### Debug Mode
Enable detailed logging:
1. Go to **Logs** tab
2. Set log level to **DEBUG**
3. Monitor all bot activities
4. Save logs for analysis

## 🎮 Pro Tips

### Strategy Selection
- **Start Small**: Enable 2-3 strategies initially
- **Test Period**: Run on demo account for 1-2 weeks
- **Monitor Performance**: Use **Performance** tab regularly
- **Adjust Weights**: Favor performing strategies

### Risk Management
- **Conservative Start**: Use 1-2% risk per trade
- **Diversification**: Don't put all capital in one strategy
- **Stop Losses**: Always use appropriate stop losses
- **Review Daily**: Check performance in **Monitoring** tab

### GUI Efficiency
- **System Tray**: Minimize to tray for background operation
- **Multiple Configs**: Save different setups for different markets
- **Export Reports**: Regular performance analysis
- **Hot Keys**: Learn keyboard shortcuts

## 📞 Support

### GUI Help
- **Built-in Help**: Tooltips and descriptions in GUI
- **Configuration Examples**: Sample configs included
- **Error Messages**: Detailed error reporting in **Logs** tab

### Performance Optimization
- **Strategy Weights**: Use **Performance** tab data
- **Parameter Tuning**: Adjust based on results
- **Resource Monitoring**: Check system resource usage

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

**Happy Trading with the GUI! 🚀📈🖥️**