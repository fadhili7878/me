#!/usr/bin/env python3
"""
MT5 Trading Bot GUI Application
Comprehensive interface for strategy selection, configuration, and monitoring
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import threading
import time
from datetime import datetime, timedelta
import queue
import logging
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from mt5_trading_bot import MT5TradingBot
from strategy_manager import StrategyManager, StrategyPerformance
from gui_system_tray import SystemTrayManager
import sys
import os

class TradingBotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MT5 Advanced Trading Bot GUI")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Initialize variables
        self.bot = None
        self.strategy_manager = None
        self.config = {}
        self.bot_running = False
        self.log_queue = queue.Queue()
        
        # Initialize system tray
        self.tray_manager = SystemTrayManager(self)
        
        # Style configuration
        self.setup_styles()
        
        # Create GUI components
        self.create_main_interface()
        
        # Setup logging
        self.setup_gui_logging()
        
        # Load default config
        self.load_config()
        
        # Start log monitoring
        self.monitor_logs()
        
        # Start system tray
        self.tray_manager.start_tray()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Bind minimize event for system tray
        self.root.bind('<Unmap>', self.on_minimize)
    
    def setup_styles(self):
        """Configure ttk styles for better appearance"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        style.configure('Warning.TLabel', foreground='orange')
        
        # Button styles
        style.configure('Start.TButton', background='green', foreground='white')
        style.configure('Stop.TButton', background='red', foreground='white')
        style.configure('Config.TButton', background='blue', foreground='white')
    
    def create_main_interface(self):
        """Create the main GUI interface"""
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_control_tab()
        self.create_strategies_tab()
        self.create_config_tab()
        self.create_monitoring_tab()
        self.create_performance_tab()
        self.create_logs_tab()
    
    def create_control_tab(self):
        """Create the main control tab"""
        control_frame = ttk.Frame(self.notebook)
        self.notebook.add(control_frame, text="Control")
        
        # Title
        title_label = ttk.Label(control_frame, text="MT5 Advanced Trading Bot", style='Title.TLabel')
        title_label.pack(pady=10)
        
        # Status frame
        status_frame = ttk.LabelFrame(control_frame, text="Bot Status", padding=10)
        status_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.status_label = ttk.Label(status_frame, text="Status: Stopped", style='Error.TLabel')
        self.status_label.pack()
        
        self.connection_label = ttk.Label(status_frame, text="MT5 Connection: Disconnected", style='Error.TLabel')
        self.connection_label.pack()
        
        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(pady=20)
        
        self.start_button = ttk.Button(button_frame, text="Start Bot", 
                                      command=self.start_bot, style='Start.TButton')
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = ttk.Button(button_frame, text="Stop Bot", 
                                     command=self.stop_bot, style='Stop.TButton', state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        self.test_connection_button = ttk.Button(button_frame, text="Test MT5 Connection", 
                                               command=self.test_connection)
        self.test_connection_button.pack(side=tk.LEFT, padx=10)
        
        # Quick stats frame
        stats_frame = ttk.LabelFrame(control_frame, text="Quick Statistics", padding=10)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create stats display
        stats_container = ttk.Frame(stats_frame)
        stats_container.pack(fill=tk.BOTH, expand=True)
        
        # Left column
        left_stats = ttk.Frame(stats_container)
        left_stats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(left_stats, text="Today's Performance:", style='Heading.TLabel').pack(anchor=tk.W)
        self.today_profit_label = ttk.Label(left_stats, text="P&L: $0.00")
        self.today_profit_label.pack(anchor=tk.W)
        self.today_trades_label = ttk.Label(left_stats, text="Trades: 0")
        self.today_trades_label.pack(anchor=tk.W)
        
        # Right column  
        right_stats = ttk.Frame(stats_container)
        right_stats.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(right_stats, text="Active Positions:", style='Heading.TLabel').pack(anchor=tk.W)
        self.active_positions_label = ttk.Label(right_stats, text="Positions: 0")
        self.active_positions_label.pack(anchor=tk.W)
        self.unrealized_pnl_label = ttk.Label(right_stats, text="Unrealized P&L: $0.00")
        self.unrealized_pnl_label.pack(anchor=tk.W)
    
    def create_strategies_tab(self):
        """Create the strategies configuration tab"""
        strategies_frame = ttk.Frame(self.notebook)
        self.notebook.add(strategies_frame, text="Strategies")
        
        # Title
        ttk.Label(strategies_frame, text="Strategy Configuration", style='Title.TLabel').pack(pady=10)
        
        # Create scrollable frame
        canvas = tk.Canvas(strategies_frame)
        scrollbar = ttk.Scrollbar(strategies_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Strategy controls
        self.strategy_vars = {}
        self.strategy_configs = {}
        
        strategies_info = {
            'kt_gmac': {
                'name': 'KT + GMAC Strategy',
                'description': 'Klinger Oscillator + Guppy Multiple Averaging Crossover',
                'params': ['timeframe', 'risk_multiplier', 'stop_loss_pct', 'take_profit_pct']
            },
            'martingale': {
                'name': 'Martingale Strategy', 
                'description': 'Progressive position sizing after losses',
                'params': ['max_levels', 'multiplier', 'base_lot_size', 'profit_target']
            },
            'snowball': {
                'name': 'Snowball Strategy',
                'description': 'Compound winning positions for exponential growth',
                'params': ['compound_factor', 'profit_threshold', 'momentum_period']
            },
            'hft': {
                'name': 'High Frequency Trading',
                'description': 'Rapid micro-trend following with tight spreads',
                'params': ['min_spread', 'max_spread', 'min_movement_pips', 'position_size_factor']
            },
            'arbitrage': {
                'name': 'Arbitrage Strategy',
                'description': 'Exploit price differences between correlated pairs',
                'params': ['correlation_threshold', 'z_score_entry', 'z_score_exit', 'lookback_period']
            },
            'neural': {
                'name': 'Neural Network Strategy',
                'description': 'Machine learning predictions using technical indicators',
                'params': ['confidence_threshold', 'training_period', 'retrain_interval']
            },
            'ai_model': {
                'name': 'AI Model Strategy',
                'description': 'Advanced ensemble methods with multiple indicators',
                'params': ['trend_threshold', 'volatility_quantile', 'rsi_overbought', 'rsi_oversold']
            }
        }
        
        for strategy_key, strategy_info in strategies_info.items():
            self.create_strategy_panel(scrollable_frame, strategy_key, strategy_info)
        
        # Strategy control buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(button_frame, text="Enable All", command=self.enable_all_strategies).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Disable All", command=self.disable_all_strategies).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_strategy_configs).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Configuration", command=self.save_config).pack(side=tk.LEFT, padx=5)
    
    def create_strategy_panel(self, parent, strategy_key, strategy_info):
        """Create a panel for individual strategy configuration"""
        # Main strategy frame
        strategy_frame = ttk.LabelFrame(parent, text=strategy_info['name'], padding=10)
        strategy_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Strategy description
        desc_label = ttk.Label(strategy_frame, text=strategy_info['description'], 
                              font=('Arial', 9), foreground='gray')
        desc_label.pack(anchor=tk.W)
        
        # Enable/disable checkbox
        self.strategy_vars[strategy_key] = tk.BooleanVar()
        enable_check = ttk.Checkbutton(strategy_frame, text="Enable Strategy", 
                                      variable=self.strategy_vars[strategy_key],
                                      command=lambda: self.on_strategy_toggle(strategy_key))
        enable_check.pack(anchor=tk.W, pady=5)
        
        # Parameters frame
        params_frame = ttk.Frame(strategy_frame)
        params_frame.pack(fill=tk.X, pady=5)
        
        # Weight setting
        weight_frame = ttk.Frame(params_frame)
        weight_frame.pack(fill=tk.X, pady=2)
        ttk.Label(weight_frame, text="Weight:", width=15).pack(side=tk.LEFT)
        weight_var = tk.DoubleVar(value=1.0)
        weight_spin = ttk.Spinbox(weight_frame, from_=0.1, to=5.0, increment=0.1, 
                                 textvariable=weight_var, width=10)
        weight_spin.pack(side=tk.LEFT, padx=5)
        
        # Store parameter variables
        if strategy_key not in self.strategy_configs:
            self.strategy_configs[strategy_key] = {}
        self.strategy_configs[strategy_key]['weight'] = weight_var
        
        # Strategy-specific parameters
        for param in strategy_info.get('params', []):
            param_frame = ttk.Frame(params_frame)
            param_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(param_frame, text=f"{param.replace('_', ' ').title()}:", width=15).pack(side=tk.LEFT)
            
            # Create appropriate input widget based on parameter
            if 'threshold' in param or 'factor' in param or 'pct' in param:
                param_var = tk.DoubleVar(value=1.0)
                widget = ttk.Spinbox(param_frame, from_=0.1, to=10.0, increment=0.1, 
                                   textvariable=param_var, width=10)
            elif 'period' in param or 'levels' in param:
                param_var = tk.IntVar(value=10)
                widget = ttk.Spinbox(param_frame, from_=1, to=100, increment=1, 
                                   textvariable=param_var, width=10)
            else:
                param_var = tk.StringVar(value="default")
                widget = ttk.Entry(param_frame, textvariable=param_var, width=15)
            
            widget.pack(side=tk.LEFT, padx=5)
            self.strategy_configs[strategy_key][param] = param_var
        
        # Performance indicator
        perf_frame = ttk.Frame(strategy_frame)
        perf_frame.pack(fill=tk.X, pady=5)
        
        perf_label = ttk.Label(perf_frame, text="Performance: No data", font=('Arial', 8))
        perf_label.pack(anchor=tk.W)
        self.strategy_configs[strategy_key]['perf_label'] = perf_label
    
    def create_config_tab(self):
        """Create the configuration tab"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="Configuration")
        
        # Title
        ttk.Label(config_frame, text="Account & Risk Configuration", style='Title.TLabel').pack(pady=10)
        
        # Create two columns
        main_container = ttk.Frame(config_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left column - Account settings
        left_frame = ttk.LabelFrame(main_container, text="MT5 Account Settings", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Account fields
        self.config_vars = {}
        
        account_fields = [
            ('Account Number', 'account', 'entry'),
            ('Password', 'password', 'password'),
            ('Server', 'server', 'entry'),
        ]
        
        for label_text, key, widget_type in account_fields:
            field_frame = ttk.Frame(left_frame)
            field_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(field_frame, text=f"{label_text}:", width=15).pack(side=tk.LEFT)
            
            if widget_type == 'password':
                var = tk.StringVar()
                widget = ttk.Entry(field_frame, textvariable=var, show='*', width=20)
            else:
                var = tk.StringVar()
                widget = ttk.Entry(field_frame, textvariable=var, width=20)
            
            widget.pack(side=tk.LEFT, padx=5)
            self.config_vars[key] = var
        
        # Symbols configuration
        symbols_frame = ttk.Frame(left_frame)
        symbols_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(symbols_frame, text="Trading Symbols:", style='Heading.TLabel').pack(anchor=tk.W)
        
        self.symbols_text = tk.Text(symbols_frame, height=6, width=30)
        self.symbols_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Right column - Risk settings
        right_frame = ttk.LabelFrame(main_container, text="Risk Management", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        risk_fields = [
            ('Risk per Trade (%)', 'risk_per_trade', 'float', 0.01, 0.1),
            ('Max Positions', 'max_positions', 'int', 1, 50),
            ('Max Daily Loss (%)', 'max_daily_loss', 'float', 0.01, 0.5),
            ('Max Drawdown (%)', 'max_drawdown', 'float', 0.01, 0.5),
            ('Max Spread (pips)', 'max_spread', 'int', 1, 50),
        ]
        
        for label_text, key, var_type, min_val, max_val in risk_fields:
            field_frame = ttk.Frame(right_frame)
            field_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(field_frame, text=f"{label_text}:", width=20).pack(side=tk.LEFT)
            
            if var_type == 'float':
                var = tk.DoubleVar(value=min_val * 10)
                widget = ttk.Spinbox(field_frame, from_=min_val, to=max_val, 
                                   increment=min_val, textvariable=var, width=15)
            else:
                var = tk.IntVar(value=int(min_val * 10))
                widget = ttk.Spinbox(field_frame, from_=int(min_val), to=int(max_val), 
                                   increment=1, textvariable=var, width=15)
            
            widget.pack(side=tk.LEFT, padx=5)
            self.config_vars[key] = var
        
        # Configuration buttons
        config_button_frame = ttk.Frame(config_frame)
        config_button_frame.pack(pady=20)
        
        ttk.Button(config_button_frame, text="Load Config", 
                  command=self.load_config_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(config_button_frame, text="Save Config", 
                  command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(config_button_frame, text="Reset to Defaults", 
                  command=self.reset_config).pack(side=tk.LEFT, padx=5)
    
    def create_monitoring_tab(self):
        """Create the real-time monitoring tab"""
        monitoring_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitoring_frame, text="Monitoring")
        
        # Title
        ttk.Label(monitoring_frame, text="Real-time Monitoring", style='Title.TLabel').pack(pady=10)
        
        # Create monitoring sections
        stats_container = ttk.Frame(monitoring_frame)
        stats_container.pack(fill=tk.X, padx=20, pady=10)
        
        # Account info frame
        account_frame = ttk.LabelFrame(stats_container, text="Account Information", padding=10)
        account_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.account_balance_label = ttk.Label(account_frame, text="Balance: $0.00")
        self.account_balance_label.pack(anchor=tk.W)
        self.account_equity_label = ttk.Label(account_frame, text="Equity: $0.00")
        self.account_equity_label.pack(anchor=tk.W)
        self.account_margin_label = ttk.Label(account_frame, text="Free Margin: $0.00")
        self.account_margin_label.pack(anchor=tk.W)
        
        # Market info frame  
        market_frame = ttk.LabelFrame(stats_container, text="Market Information", padding=10)
        market_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.market_status_label = ttk.Label(market_frame, text="Market: Closed")
        self.market_status_label.pack(anchor=tk.W)
        self.spread_info_label = ttk.Label(market_frame, text="Avg Spread: 0.0 pips")
        self.spread_info_label.pack(anchor=tk.W)
        
        # Active positions table
        positions_frame = ttk.LabelFrame(monitoring_frame, text="Active Positions", padding=10)
        positions_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create treeview for positions
        columns = ('Symbol', 'Type', 'Volume', 'Open Price', 'Current Price', 'P&L', 'Strategy')
        self.positions_tree = ttk.Treeview(positions_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.positions_tree.heading(col, text=col)
            self.positions_tree.column(col, width=100)
        
        # Scrollbar for positions
        positions_scrollbar = ttk.Scrollbar(positions_frame, orient=tk.VERTICAL, 
                                          command=self.positions_tree.yview)
        self.positions_tree.configure(yscrollcommand=positions_scrollbar.set)
        
        self.positions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        positions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Update monitoring data periodically
        self.update_monitoring_data()
    
    def create_performance_tab(self):
        """Create the performance analysis tab"""
        performance_frame = ttk.Frame(self.notebook)
        self.notebook.add(performance_frame, text="Performance")
        
        # Title
        ttk.Label(performance_frame, text="Performance Analysis", style='Title.TLabel').pack(pady=10)
        
        # Create performance sections
        summary_frame = ttk.LabelFrame(performance_frame, text="Performance Summary", padding=10)
        summary_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Performance metrics display
        metrics_container = ttk.Frame(summary_frame)
        metrics_container.pack(fill=tk.X)
        
        # Left metrics
        left_metrics = ttk.Frame(metrics_container)
        left_metrics.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.total_trades_label = ttk.Label(left_metrics, text="Total Trades: 0")
        self.total_trades_label.pack(anchor=tk.W)
        self.win_rate_label = ttk.Label(left_metrics, text="Win Rate: 0%")
        self.win_rate_label.pack(anchor=tk.W)
        self.profit_factor_label = ttk.Label(left_metrics, text="Profit Factor: 0.00")
        self.profit_factor_label.pack(anchor=tk.W)
        
        # Right metrics
        right_metrics = ttk.Frame(metrics_container)
        right_metrics.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.total_profit_label = ttk.Label(right_metrics, text="Total Profit: $0.00")
        self.total_profit_label.pack(anchor=tk.W)
        self.max_drawdown_label = ttk.Label(right_metrics, text="Max Drawdown: 0%")
        self.max_drawdown_label.pack(anchor=tk.W)
        self.sharpe_ratio_label = ttk.Label(right_metrics, text="Sharpe Ratio: 0.00")
        self.sharpe_ratio_label.pack(anchor=tk.W)
        
        # Chart frame
        chart_frame = ttk.LabelFrame(performance_frame, text="Performance Chart", padding=10)
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(12, 6), dpi=100)
        self.chart_canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Chart controls
        chart_controls = ttk.Frame(chart_frame)
        chart_controls.pack(fill=tk.X, pady=5)
        
        ttk.Button(chart_controls, text="Update Chart", 
                  command=self.update_performance_chart).pack(side=tk.LEFT, padx=5)
        ttk.Button(chart_controls, text="Export Report", 
                  command=self.export_performance_report).pack(side=tk.LEFT, padx=5)
    
    def create_logs_tab(self):
        """Create the logs and messages tab"""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="Logs")
        
        # Title
        ttk.Label(logs_frame, text="System Logs & Messages", style='Title.TLabel').pack(pady=10)
        
        # Log controls
        log_controls = ttk.Frame(logs_frame)
        log_controls.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(log_controls, text="Log Level:").pack(side=tk.LEFT, padx=5)
        
        self.log_level_var = tk.StringVar(value="INFO")
        log_level_combo = ttk.Combobox(log_controls, textvariable=self.log_level_var,
                                      values=["DEBUG", "INFO", "WARNING", "ERROR"], 
                                      state="readonly", width=10)
        log_level_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(log_controls, text="Clear Logs", 
                  command=self.clear_logs).pack(side=tk.LEFT, padx=10)
        ttk.Button(log_controls, text="Save Logs", 
                  command=self.save_logs).pack(side=tk.LEFT, padx=5)
        
        # Log display
        log_display_frame = ttk.Frame(logs_frame)
        log_display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_display_frame, height=25, 
                                                 font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for different log levels
        self.log_text.tag_configure("INFO", foreground="black")
        self.log_text.tag_configure("WARNING", foreground="orange")
        self.log_text.tag_configure("ERROR", foreground="red")
        self.log_text.tag_configure("DEBUG", foreground="gray")
    
    def setup_gui_logging(self):
        """Setup logging to display in GUI"""
        class GUILogHandler(logging.Handler):
            def __init__(self, log_queue):
                super().__init__()
                self.log_queue = log_queue
            
            def emit(self, record):
                self.log_queue.put(record)
        
        # Add GUI handler to root logger
        gui_handler = GUILogHandler(self.log_queue)
        gui_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        gui_handler.setFormatter(formatter)
        
        root_logger = logging.getLogger()
        root_logger.addHandler(gui_handler)
    
    def monitor_logs(self):
        """Monitor log queue and display messages in GUI"""
        try:
            while True:
                record = self.log_queue.get_nowait()
                
                # Format log message
                timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')
                message = f"[{timestamp}] {record.levelname}: {record.getMessage()}\n"
                
                # Insert with appropriate tag
                self.log_text.insert(tk.END, message, record.levelname)
                self.log_text.see(tk.END)
                
                # Limit log display size
                if self.log_text.index('end-1c').split('.')[0] > '1000':
                    self.log_text.delete('1.0', '100.end')
                
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.monitor_logs)
    
    def load_config(self, config_path="config.json"):
        """Load configuration from file"""
        try:
            if Path(config_path).exists():
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
                
                # Update GUI with loaded config
                self.update_gui_from_config()
                self.log_message("Configuration loaded successfully", "INFO")
            else:
                self.log_message(f"Config file {config_path} not found, using defaults", "WARNING")
                self.reset_config()
        except Exception as e:
            self.log_message(f"Error loading config: {e}", "ERROR")
            messagebox.showerror("Config Error", f"Failed to load configuration: {e}")
    
    def update_gui_from_config(self):
        """Update GUI elements from loaded configuration"""
        try:
            # Update account settings
            if 'account' in self.config:
                self.config_vars['account'].set(str(self.config.get('account', '')))
            if 'server' in self.config:
                self.config_vars['server'].set(self.config.get('server', ''))
            
            # Update risk settings
            risk_fields = ['risk_per_trade', 'max_positions', 'max_daily_loss', 'max_drawdown', 'max_spread']
            for field in risk_fields:
                if field in self.config and field in self.config_vars:
                    self.config_vars[field].set(self.config[field])
            
            # Update symbols
            symbols = self.config.get('symbols', [])
            self.symbols_text.delete('1.0', tk.END)
            self.symbols_text.insert('1.0', '\n'.join(symbols))
            
            # Update strategy settings
            strategies_config = self.config.get('strategies', {})
            for strategy_key, strategy_config in strategies_config.items():
                if strategy_key in self.strategy_vars:
                    self.strategy_vars[strategy_key].set(strategy_config.get('enabled', False))
                
                if strategy_key in self.strategy_configs:
                    # Update weight
                    if 'weight' in self.strategy_configs[strategy_key]:
                        self.strategy_configs[strategy_key]['weight'].set(
                            strategy_config.get('weight', 1.0)
                        )
                    
                    # Update other parameters
                    for param, var in self.strategy_configs[strategy_key].items():
                        if param in strategy_config and param != 'weight' and param != 'perf_label':
                            try:
                                var.set(strategy_config[param])
                            except:
                                pass
        except Exception as e:
            self.log_message(f"Error updating GUI from config: {e}", "ERROR")
    
    def save_config(self, config_path="config.json"):
        """Save current configuration to file"""
        try:
            # Build config from GUI
            config = {}
            
            # Account settings
            config['account'] = int(self.config_vars['account'].get()) if self.config_vars['account'].get() else 0
            config['password'] = self.config_vars['password'].get()
            config['server'] = self.config_vars['server'].get()
            
            # Risk settings
            config['risk_per_trade'] = self.config_vars['risk_per_trade'].get()
            config['max_positions'] = int(self.config_vars['max_positions'].get())
            config['max_daily_loss'] = self.config_vars['max_daily_loss'].get()
            config['max_drawdown'] = self.config_vars['max_drawdown'].get()
            config['max_spread'] = int(self.config_vars['max_spread'].get())
            
            # Symbols
            symbols_text = self.symbols_text.get('1.0', tk.END).strip()
            config['symbols'] = [s.strip() for s in symbols_text.split('\n') if s.strip()]
            
            # Strategies
            config['strategies'] = {}
            for strategy_key, enabled_var in self.strategy_vars.items():
                strategy_config = {
                    'enabled': enabled_var.get(),
                    'weight': self.strategy_configs[strategy_key]['weight'].get()
                }
                
                # Add strategy-specific parameters
                for param, var in self.strategy_configs[strategy_key].items():
                    if param not in ['weight', 'perf_label']:
                        try:
                            strategy_config[param] = var.get()
                        except:
                            pass
                
                config['strategies'][strategy_key] = strategy_config
            
            # Save to file
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.config = config
            self.log_message("Configuration saved successfully", "INFO")
            messagebox.showinfo("Config Saved", "Configuration saved successfully!")
            
        except Exception as e:
            self.log_message(f"Error saving config: {e}", "ERROR")
            messagebox.showerror("Save Error", f"Failed to save configuration: {e}")
    
    def start_bot(self):
        """Start the trading bot"""
        try:
            if self.bot_running:
                messagebox.showwarning("Bot Running", "Bot is already running!")
                return
            
            # Validate configuration
            if not self.validate_config():
                return
            
            # Save current config
            self.save_config()
            
            # Initialize bot
            self.bot = MT5TradingBot(config_file="config.json")
            self.strategy_manager = StrategyManager(self.config)
            
            # Start bot in separate thread
            def run_bot():
                try:
                                    if self.bot.start():
                    self.bot_running = True
                    self.log_message("Trading bot started successfully", "INFO")
                    self.root.after(0, self.update_control_buttons)
                    self.tray_manager.update_icon_status("running")
                    self.tray_manager.show_notification("Bot Started", "Trading bot is now running")
                else:
                    self.log_message("Failed to start trading bot", "ERROR")
                    self.root.after(0, lambda: messagebox.showerror("Start Error", "Failed to start bot"))
                except Exception as e:
                    self.log_message(f"Bot error: {e}", "ERROR")
                    self.root.after(0, lambda: messagebox.showerror("Bot Error", str(e)))
            
            bot_thread = threading.Thread(target=run_bot, daemon=True)
            bot_thread.start()
            
        except Exception as e:
            self.log_message(f"Error starting bot: {e}", "ERROR")
            messagebox.showerror("Start Error", f"Failed to start bot: {e}")
    
    def stop_bot(self):
        """Stop the trading bot"""
        try:
            if not self.bot_running:
                messagebox.showwarning("Bot Not Running", "Bot is not currently running!")
                return
            
            if self.bot:
                self.bot.stop()
            
            self.bot_running = False
            self.bot = None
            
            self.log_message("Trading bot stopped", "INFO")
            self.update_control_buttons()
            self.tray_manager.update_icon_status("stopped")
            self.tray_manager.show_notification("Bot Stopped", "Trading bot has been stopped")
            
        except Exception as e:
            self.log_message(f"Error stopping bot: {e}", "ERROR")
            messagebox.showerror("Stop Error", f"Failed to stop bot: {e}")
    
    def test_connection(self):
        """Test MT5 connection"""
        try:
            import MetaTrader5 as mt5
            
            if not mt5.initialize():
                messagebox.showerror("Connection Failed", "Failed to initialize MT5")
                return
            
            # Try to login with current config
            account = int(self.config_vars['account'].get()) if self.config_vars['account'].get() else 0
            password = self.config_vars['password'].get()
            server = self.config_vars['server'].get()
            
            if mt5.login(login=account, password=password, server=server):
                account_info = mt5.account_info()
                messagebox.showinfo("Connection Success", 
                                   f"Successfully connected to MT5!\n"
                                   f"Account: {account_info.login}\n"
                                   f"Balance: ${account_info.balance:.2f}")
                self.log_message("MT5 connection test successful", "INFO")
            else:
                messagebox.showerror("Login Failed", "Failed to login to MT5 account")
                self.log_message("MT5 connection test failed", "ERROR")
            
            mt5.shutdown()
            
        except Exception as e:
            self.log_message(f"Connection test error: {e}", "ERROR")
            messagebox.showerror("Connection Error", f"Connection test failed: {e}")
    
    def validate_config(self):
        """Validate current configuration"""
        try:
            # Check required fields
            if not self.config_vars['account'].get():
                messagebox.showerror("Config Error", "Account number is required")
                return False
            
            if not self.config_vars['password'].get():
                messagebox.showerror("Config Error", "Password is required")
                return False
            
            if not self.config_vars['server'].get():
                messagebox.showerror("Config Error", "Server is required")
                return False
            
            # Check if at least one strategy is enabled
            any_enabled = any(var.get() for var in self.strategy_vars.values())
            if not any_enabled:
                messagebox.showerror("Config Error", "At least one strategy must be enabled")
                return False
            
            return True
            
        except Exception as e:
            self.log_message(f"Config validation error: {e}", "ERROR")
            messagebox.showerror("Validation Error", f"Configuration validation failed: {e}")
            return False
    
    def update_control_buttons(self):
        """Update control button states"""
        if self.bot_running:
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Running", style='Success.TLabel')
            self.connection_label.config(text="MT5 Connection: Connected", style='Success.TLabel')
        else:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_label.config(text="Status: Stopped", style='Error.TLabel')
            self.connection_label.config(text="MT5 Connection: Disconnected", style='Error.TLabel')
    
    def update_monitoring_data(self):
        """Update monitoring data periodically"""
        if self.bot_running and self.bot:
            try:
                import MetaTrader5 as mt5
                
                # Update account info
                account_info = mt5.account_info()
                if account_info:
                    self.account_balance_label.config(text=f"Balance: ${account_info.balance:.2f}")
                    self.account_equity_label.config(text=f"Equity: ${account_info.equity:.2f}")
                    self.account_margin_label.config(text=f"Free Margin: ${account_info.margin_free:.2f}")
                
                # Update positions
                self.update_positions_display()
                
            except Exception as e:
                self.log_message(f"Error updating monitoring data: {e}", "ERROR")
        
        # Schedule next update
        self.root.after(5000, self.update_monitoring_data)  # Update every 5 seconds
    
    def update_positions_display(self):
        """Update the positions display"""
        try:
            import MetaTrader5 as mt5
            
            # Clear existing items
            for item in self.positions_tree.get_children():
                self.positions_tree.delete(item)
            
            # Get current positions
            positions = mt5.positions_get()
            if positions:
                for position in positions:
                    # Get current price
                    tick = mt5.symbol_info_tick(position.symbol)
                    current_price = tick.bid if position.type == 0 else tick.ask
                    
                    # Calculate P&L
                    if position.type == 0:  # Buy
                        pnl = (current_price - position.price_open) * position.volume * 100000
                    else:  # Sell
                        pnl = (position.price_open - current_price) * position.volume * 100000
                    
                    # Insert into tree
                    self.positions_tree.insert('', tk.END, values=(
                        position.symbol,
                        "BUY" if position.type == 0 else "SELL",
                        f"{position.volume:.2f}",
                        f"{position.price_open:.5f}",
                        f"{current_price:.5f}",
                        f"${pnl:.2f}",
                        position.comment or "Manual"
                    ))
        except Exception as e:
            self.log_message(f"Error updating positions: {e}", "ERROR")
    
    def update_performance_chart(self):
        """Update the performance chart"""
        try:
            if not self.strategy_manager:
                return
            
            # Clear previous plot
            self.fig.clear()
            
            # Create subplots
            ax1 = self.fig.add_subplot(211)
            ax2 = self.fig.add_subplot(212)
            
            # Get trade history
            df = self.strategy_manager.get_trade_history(days=30)
            
            if not df.empty and 'profit' in df.columns:
                # Cumulative P&L chart
                df['cumulative_pnl'] = df['profit'].cumsum()
                ax1.plot(df['timestamp'], df['cumulative_pnl'])
                ax1.set_title('Cumulative P&L (Last 30 Days)')
                ax1.set_ylabel('P&L ($)')
                ax1.grid(True)
                
                # Strategy performance comparison
                strategy_performance = df.groupby('strategy')['profit'].sum()
                if not strategy_performance.empty:
                    ax2.bar(strategy_performance.index, strategy_performance.values)
                    ax2.set_title('Strategy Performance Comparison')
                    ax2.set_ylabel('Total P&L ($)')
                    ax2.tick_params(axis='x', rotation=45)
            else:
                ax1.text(0.5, 0.5, 'No trade data available', 
                        transform=ax1.transAxes, ha='center', va='center')
                ax2.text(0.5, 0.5, 'No performance data available', 
                        transform=ax2.transAxes, ha='center', va='center')
            
            self.fig.tight_layout()
            self.chart_canvas.draw()
            
        except Exception as e:
            self.log_message(f"Error updating chart: {e}", "ERROR")
    
    def export_performance_report(self):
        """Export performance report"""
        try:
            if not self.strategy_manager:
                messagebox.showwarning("No Data", "No strategy manager available")
                return
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                report = self.strategy_manager.generate_performance_report()
                with open(file_path, 'w') as f:
                    f.write(report)
                
                self.log_message(f"Performance report exported to {file_path}", "INFO")
                messagebox.showinfo("Export Success", f"Report exported to {file_path}")
        
        except Exception as e:
            self.log_message(f"Error exporting report: {e}", "ERROR")
            messagebox.showerror("Export Error", f"Failed to export report: {e}")
    
    def on_strategy_toggle(self, strategy_key):
        """Handle strategy enable/disable toggle"""
        enabled = self.strategy_vars[strategy_key].get()
        self.log_message(f"Strategy {strategy_key} {'enabled' if enabled else 'disabled'}", "INFO")
    
    def enable_all_strategies(self):
        """Enable all strategies"""
        for var in self.strategy_vars.values():
            var.set(True)
        self.log_message("All strategies enabled", "INFO")
    
    def disable_all_strategies(self):
        """Disable all strategies"""
        for var in self.strategy_vars.values():
            var.set(False)
        self.log_message("All strategies disabled", "INFO")
    
    def reset_strategy_configs(self):
        """Reset strategy configurations to defaults"""
        if messagebox.askyesno("Reset Strategies", "Reset all strategy configurations to defaults?"):
            for strategy_key in self.strategy_vars:
                self.strategy_vars[strategy_key].set(True)
                if strategy_key in self.strategy_configs:
                    self.strategy_configs[strategy_key]['weight'].set(1.0)
            self.log_message("Strategy configurations reset to defaults", "INFO")
    
    def reset_config(self):
        """Reset configuration to defaults"""
        if messagebox.askyesno("Reset Config", "Reset all configuration to defaults?"):
            # Reset to default values
            self.config_vars['account'].set("123456")
            self.config_vars['password'].set("")
            self.config_vars['server'].set("your_broker_server")
            self.config_vars['risk_per_trade'].set(0.02)
            self.config_vars['max_positions'].set(10)
            self.config_vars['max_daily_loss'].set(0.05)
            self.config_vars['max_drawdown'].set(0.15)
            self.config_vars['max_spread'].set(10)
            
            # Reset symbols
            self.symbols_text.delete('1.0', tk.END)
            self.symbols_text.insert('1.0', "EURUSD\nGBPUSD\nUSDJPY\nUSDCHF")
            
            self.log_message("Configuration reset to defaults", "INFO")
    
    def load_config_file(self):
        """Load configuration from file dialog"""
        file_path = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            self.load_config(file_path)
    
    def clear_logs(self):
        """Clear the log display"""
        self.log_text.delete('1.0', tk.END)
    
    def save_logs(self):
        """Save logs to file"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".log",
                filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                log_content = self.log_text.get('1.0', tk.END)
                with open(file_path, 'w') as f:
                    f.write(log_content)
                
                self.log_message(f"Logs saved to {file_path}", "INFO")
                messagebox.showinfo("Save Success", f"Logs saved to {file_path}")
        
        except Exception as e:
            self.log_message(f"Error saving logs: {e}", "ERROR")
            messagebox.showerror("Save Error", f"Failed to save logs: {e}")
    
    def log_message(self, message, level="INFO"):
        """Add message to log display"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.insert(tk.END, formatted_message, level)
        self.log_text.see(tk.END)
    
    def on_minimize(self, event):
        """Handle window minimize event"""
        if event.widget == self.root:
            # Minimize to system tray if available
            if hasattr(self.tray_manager, 'icon') and self.tray_manager.icon:
                self.root.withdraw()
                self.tray_manager.show_notification("Minimized to Tray", "Bot is running in system tray")
    
    def on_closing(self):
        """Handle application closing"""
        if self.bot_running:
            if messagebox.askyesno("Quit", "Bot is running. Stop bot and quit?"):
                self.stop_bot()
                self.tray_manager.stop_tray()
                self.root.quit()
                self.root.destroy()
        else:
            self.tray_manager.stop_tray()
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main function to run the GUI"""
    try:
        app = TradingBotGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()