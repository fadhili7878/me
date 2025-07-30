# Quantum Dashboard for MetaTrader 5

A futuristic quantum-themed dashboard Expert Advisor (EA) for MetaTrader 5 that displays **real-time market data** in a sci-fi interface inspired by quantum computing concepts. **Now positioned on the right side of the chart to avoid blocking market view!**

## 🆕 Latest Updates

- ✅ **Right-side positioning**: Dashboard automatically anchors to the right side of the chart
- ✅ **Real market data integration**: No more simulated data - reads actual market prices, volume, and indicators
- ✅ **Dynamic sizing**: Automatically adjusts position when chart window is resized
- ✅ **Advanced predictions**: Uses real technical indicators (RSI, MACD, Moving Averages, Bollinger Bands, etc.)
- ✅ **Live market analysis**: Displays current price, change percentage, volume, and spread

## Features

### 🔬 Quantum Processing Matrix
- Dynamic 8x8 colored matrix display based on **real market indicators**
- Real-time qubit count and processing speed derived from **market volatility**
- Quantum state information reflecting actual market conditions
- Colors now reflect actual market sentiment (green=bullish, red=bearish, yellow=neutral)

### 🎯 Pattern Recognition Matrix  
- Pattern detection indicators based on **real market analysis**
- Technical indicator strength visualization
- Dynamic pattern state changes reflecting market momentum

### 📊 Predictive Analytics Engine
- **Real trend predictions** based on multiple technical indicators
- Accuracy and confidence percentages calculated from market volatility
- Time horizon display for prediction reliability
- Visual analytics bars showing actual market sentiment from 10 different indicators

### 💫 Quantum Data Stream (**New Real Market Data!**)
- **Live current price** with real-time price changes
- **Actual percentage change** and volume information
- **Real spread data** and symbol information  
- **Live RSI and MACD values** from market analysis
- **Intelligent predictions** based on combined indicator analysis:
  - BULLISH ↑ (when average indicators > 0.2)
  - BEARISH ↓ (when average indicators < -0.2)  
  - SIDEWAYS ↔ (when market is neutral)
- Dynamic timestamp updates

### 📈 Status Bar
- Current quantum state reflecting market conditions
- Real-time dimensional and simulation status

## Installation

1. Copy `QuantumDashboard.mq5` to your MetaTrader 5 `Experts` folder:
   ```
   MT5_Data_Folder/MQL5/Experts/QuantumDashboard.mq5
   ```

2. Open MetaTrader 5 and refresh the Navigator panel

3. Drag the Expert Advisor onto any chart

4. Enable "Allow algo trading" in MT5 settings

5. **The dashboard will automatically position itself on the right side of your chart!**

## Customization

The dashboard includes several input parameters you can modify:

```mql5
input int PanelMarginRight = 20;       // Distance from right edge
input int PanelMarginTop = 30;         // Distance from top edge  
input int PanelWidth = 350;            // Panel width
input int PanelHeight = 150;           // Panel height
input color BackgroundColor = C'20,20,40';   // Dark blue background
input color BorderColor = C'0,255,255';      // Cyan borders
input color TextColor = C'255,255,255';      // White text
input color AccentColor = C'255,0,255';      // Magenta accents
```

## Visual Elements

### Color Scheme
- **Background**: Dark blue (`C'20,20,40'`)
- **Borders**: Cyan (`C'0,255,255'`)
- **Text**: White (`C'255,255,255'`)
- **Accents**: Magenta (`C'255,0,255'`)
- **Matrix Colors**: Dynamic based on actual market indicators
  - Green: Bullish market conditions
  - Red: Bearish market conditions  
  - Yellow: Neutral/sideways market
  - Cyan: Mild bullish sentiment
  - Gray: Low volatility/flat market

### Dashboard Layout (Right-Side Positioned)
```
                                    Chart Area                    │ Dashboard │
                                                                 │           │
                              📊 Market Data                     │ ┌───────┐ │
                                                                 │ │QUANTUM│ │
                           🕯️ Candlesticks                       │ │MATRIX │ │
                                                                 │ │ 8x8   │ │
                               📈 Indicators                     │ └───────┘ │
                                                                 │           │
                                                                 │ ┌───────┐ │
                                                                 │ │PATTERN│ │
                           User can see all market data          │ │RECOGN │ │
                              without obstruction                │ └───────┘ │
                                                                 │           │
                                                                 │ ┌───────┐ │
                                                                 │ │PREDICT│ │
                                                                 │ │ENGINE │ │
                                                                 │ └───────┘ │
                                                                 │           │
                                                                 │ ┌───────┐ │
                                                                 │ │ LIVE  │ │
                                                                 │ │MARKET │ │
                                                                 │ │ DATA  │ │
                                                                 │ └───────┘ │
```

## Real-Time Market Integration

### Technical Indicators Used
- **RSI (14-period)**: Momentum oscillator
- **MACD**: Moving Average Convergence Divergence  
- **Moving Averages**: 20 vs 50 period comparison
- **Bollinger Bands**: Price position within bands
- **Volume Analysis**: Current vs average volume
- **Momentum**: Price momentum over 10 periods
- **Support/Resistance**: Price proximity to recent highs/lows
- **Candlestick Patterns**: Real-time pattern strength analysis
- **Market Sentiment**: Price vs moving average position
- **Volatility Index**: Market volatility measurement

### Real-Time Updates

The dashboard updates every second with:
- ✅ **Real market prices** and price changes
- ✅ **Actual volume and spread data**
- ✅ **Live technical indicator values**
- ✅ **Matrix colors based on market conditions**
- ✅ **Pattern indicators reflecting market momentum**
- ✅ **Analytics bars showing real indicator strength**
- ✅ **Intelligent predictions from combined analysis**
- ✅ **Dynamic positioning on chart resize**

## Performance

- **Update Frequency**: 1 second
- **Memory Usage**: Optimized with efficient indicator calculations
- **CPU Impact**: Low (real-time market data processing)
- **Positioning**: Automatic right-side anchoring, responsive to window resizing

## Technical Details

### MQL5 Features Used
- **Real-time market data**: `SymbolInfoTick()`, `iClose()`, `iOpen()`, `iHigh()`, `iLow()`, `iVolume()`
- **Technical indicators**: `iMA()`, `iBands()`, custom RSI, MACD calculations
- **Dynamic positioning**: `ChartGetInteger()` for window dimensions
- **Chart events**: `OnChartEvent()` for responsive resizing
- **Object-oriented GUI**: `OBJ_RECTANGLE_LABEL` and `OBJ_LABEL`
- **Timer events**: Real-time updates with market data integration
- **Memory management**: Proper array handling and object cleanup

### File Structure
```
QuantumDashboard.mq5
├── Market data integration functions
├── Technical indicator calculations  
├── Dynamic positioning system
├── Real-time dashboard updates
├── Chart event handling
└── Advanced prediction algorithms
```

## Compatibility

- **Platform**: MetaTrader 5 (Build 3540+)
- **Language**: MQL5
- **Chart Types**: All (works on any timeframe/symbol)
- **Operating Systems**: Windows, Mac, Linux (via MT5)
- **Market Data**: Works with any MT5 symbol (Forex, Stocks, Commodities, Crypto)

## Future Enhancements

Potential additions for future versions:
- [ ] Sound alerts for significant market events
- [ ] Export market analysis data to CSV
- [ ] Multiple color themes
- [ ] Customizable indicator parameters
- [ ] Email/SMS notifications for predictions
- [ ] Multi-timeframe analysis display

## License

Copyright 2024 - Educational and demonstration purposes.

## Support

For issues or customization requests, please refer to the MQL5 community forums or MetaTrader 5 documentation.

---

*"Real quantum-powered market analysis - now positioned where it belongs!"* 🚀📊