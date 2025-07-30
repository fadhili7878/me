#!/usr/bin/env python3
"""
Quantum-Themed MT5 Trading Bot GUI
Advanced quantum computing aesthetic interface with cyberpunk styling
"""

import tkinter as tk
from tkinter import ttk, messagebox, Canvas
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
import sys
import os
import random
import math

class QuantumTradingGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("QUANTUM TRADING MATRIX • REALITY: SIMULATED")
        self.root.geometry("1600x1000")
        self.root.minsize(1400, 900)
        
        # Quantum color scheme
        self.colors = {
            'bg_dark': '#0a0a1a',
            'bg_panel': '#1a1a2e',
            'neon_cyan': '#00ffff',
            'neon_magenta': '#ff00ff',
            'neon_green': '#00ff00',
            'neon_purple': '#8000ff',
            'neon_pink': '#ff0080',
            'neon_yellow': '#ffff00',
            'text_primary': '#ffffff',
            'text_secondary': '#80ffff',
            'grid_line': '#404060',
            'danger': '#ff4444'
        }
        
        # Configure dark theme
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Initialize variables
        self.bot = None
        self.strategy_manager = None
        self.config = {}
        self.bot_running = False
        self.log_queue = queue.Queue()
        self.data_stream_messages = []
        
        # Trading data
        self.positions = []
        self.account_info = {'balance': 0, 'equity': 0, 'margin': 0, 'free_margin': 0}
        self.symbol_prices = {}
        
        # Animation variables
        self.quantum_dots = []
        self.pattern_data = []
        self.analytics_data = {
            'bullish_bars': [8, 7, 9, 6, 8, 7, 9, 8, 7, 9],
            'bearish_bars': [4, 5, 3, 6, 4, 5, 3, 4, 5, 3],
            'accuracy': 89.0,
            'confidence': 76.5,
            'horizon': '5-30 MIN'
        }
        
        # Style configuration
        self.setup_quantum_styles()
        
        # Create quantum interface
        self.create_quantum_interface()
        
        # Start animations
        self.start_quantum_animations()
        
        # Load config and initialize bot
        self.load_config()
        self.initialize_trading_bot()
        
        # Start data monitoring
        self.start_data_monitoring()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_quantum_styles(self):
        """Configure quantum-themed styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme styles
        style.configure('Quantum.TFrame', background=self.colors['bg_panel'], relief='solid', borderwidth=1)
        style.configure('QuantumTitle.TLabel', 
                       background=self.colors['bg_panel'], 
                       foreground=self.colors['neon_cyan'],
                       font=('Orbitron', 12, 'bold'))
        style.configure('QuantumData.TLabel',
                       background=self.colors['bg_panel'],
                       foreground=self.colors['text_primary'],
                       font=('Courier New', 10))
        style.configure('QuantumValue.TLabel',
                       background=self.colors['bg_panel'],
                       foreground=self.colors['neon_green'],
                       font=('Courier New', 11, 'bold'))
        style.configure('QuantumButton.TButton',
                       background=self.colors['bg_panel'],
                       foreground=self.colors['neon_cyan'],
                       borderwidth=2)
        
    def create_quantum_interface(self):
        """Create the main quantum interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create quantum background canvas
        self.bg_canvas = Canvas(main_frame, bg=self.colors['bg_dark'], highlightthickness=0)
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Top section - Quantum Processing Matrix
        self.create_quantum_processing_matrix(main_frame)
        
        # Middle left - Pattern Recognition Matrix
        self.create_pattern_recognition_matrix(main_frame)
        
        # Middle right - Predictive Analytics Engine
        self.create_predictive_analytics_engine(main_frame)
        
        # Bottom - Quantum Data Stream
        self.create_quantum_data_stream(main_frame)
        
        # Status bar
        self.create_quantum_status_bar(main_frame)
        
        # Trading controls overlay
        self.create_trading_controls(main_frame)
        
    def create_quantum_processing_matrix(self, parent):
        """Create the quantum processing matrix panel"""
        frame = tk.Frame(parent, bg=self.colors['bg_panel'], relief='solid', bd=2)
        frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.25)
        
        # Title
        title_label = tk.Label(frame, text="⬜ QUANTUM PROCESSING MATRIX ⬜", 
                              bg=self.colors['bg_panel'], fg=self.colors['neon_cyan'],
                              font=('Orbitron', 14, 'bold'))
        title_label.pack(pady=(10, 5))
        
        # Content frame
        content_frame = tk.Frame(frame, bg=self.colors['bg_panel'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Left side - Quantum grid
        grid_frame = tk.Frame(content_frame, bg=self.colors['bg_panel'])
        grid_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create quantum qubit grid (8x16)
        self.qubit_canvas = Canvas(grid_frame, bg=self.colors['bg_panel'], 
                                  highlightthickness=0, width=300, height=120)
        self.qubit_canvas.pack(pady=10)
        
        self.create_qubit_grid()
        
        # Right side - Quantum metrics
        metrics_frame = tk.Frame(content_frame, bg=self.colors['bg_panel'])
        metrics_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        # Create metric labels that will be updated with real data
        self.qubits_label = self.create_metric_pair(metrics_frame, "⬜ QUBITS:", "1009", self.colors['neon_cyan'])
        self.speed_label = self.create_metric_pair(metrics_frame, "⬜ SPEED:", "6.7 THz", self.colors['neon_green'])
        self.state_label = self.create_metric_pair(metrics_frame, "⬜ STATE:", "SUPERPOS", self.colors['neon_magenta'])
        self.entangled_label = self.create_metric_pair(metrics_frame, "⬜ ENTANGLED:", "YES", self.colors['neon_green'])
        
        # Account info display
        tk.Label(metrics_frame, text="", bg=self.colors['bg_panel']).pack(pady=5)  # Spacer
        self.balance_label = self.create_metric_pair(metrics_frame, "⬜ BALANCE:", "$0.00", self.colors['neon_yellow'])
        self.equity_label = self.create_metric_pair(metrics_frame, "⬜ EQUITY:", "$0.00", self.colors['neon_green'])
        self.positions_label = self.create_metric_pair(metrics_frame, "⬜ POSITIONS:", "0", self.colors['neon_purple'])
    
    def create_metric_pair(self, parent, label_text, value_text, color):
        """Create a label-value pair for metrics"""
        metric_frame = tk.Frame(parent, bg=self.colors['bg_panel'])
        metric_frame.pack(anchor='w', pady=2)
        
        tk.Label(metric_frame, text=label_text, bg=self.colors['bg_panel'], 
                fg=self.colors['text_secondary'], font=('Courier New', 10)).pack(side=tk.LEFT)
        value_label = tk.Label(metric_frame, text=value_text, bg=self.colors['bg_panel'], 
                              fg=color, font=('Courier New', 11, 'bold'))
        value_label.pack(side=tk.LEFT, padx=(10, 0))
        return value_label
    
    def create_qubit_grid(self):
        """Create the colorful qubit grid"""
        self.qubit_rects = []
        colors = [self.colors['neon_cyan'], self.colors['neon_magenta'], 
                 self.colors['neon_green'], self.colors['neon_purple'], 
                 self.colors['neon_pink']]
        
        cell_size = 15
        spacing = 18
        
        for row in range(8):
            rect_row = []
            for col in range(16):
                x = col * spacing + 10
                y = row * spacing + 10
                
                # Random color for quantum state
                color = random.choice(colors)
                rect = self.qubit_canvas.create_rectangle(
                    x, y, x + cell_size, y + cell_size,
                    fill=color, outline=color, width=1
                )
                rect_row.append(rect)
            self.qubit_rects.append(rect_row)
    
    def create_pattern_recognition_matrix(self, parent):
        """Create the pattern recognition matrix panel"""
        frame = tk.Frame(parent, bg=self.colors['bg_panel'], relief='solid', bd=2)
        frame.place(relx=0.02, rely=0.3, relwidth=0.47, relheight=0.35)
        
        # Title
        title_label = tk.Label(frame, text="⬜ PATTERN RECOGNITION MATRIX ⬜", 
                              bg=self.colors['bg_panel'], fg=self.colors['neon_cyan'],
                              font=('Orbitron', 12, 'bold'))
        title_label.pack(pady=(10, 5))
        
        # Pattern canvas
        self.pattern_canvas = Canvas(frame, bg=self.colors['bg_panel'], 
                                   highlightthickness=0)
        self.pattern_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.create_pattern_visualization()
    
    def create_pattern_visualization(self):
        """Create geometric pattern visualization"""
        # Create pattern grid representing market patterns
        symbols = ['●', '◆', '▲', '▼', '■', '♦', '▲', '▼', '●', '◆', '▲', '▼', '■', '♦', '●', '▲']
        colors = [self.colors['neon_cyan'], self.colors['neon_green'], 
                 self.colors['neon_magenta'], self.colors['neon_purple']]
        
        for i, symbol in enumerate(symbols):
            x = (i % 16) * 25 + 20
            y = 50 + (i // 16) * 30
            color = colors[i % len(colors)]
            
            self.pattern_canvas.create_text(x, y, text=symbol, fill=color, 
                                          font=('Arial', 12, 'bold'))
        
        # Add connecting lines for pattern relationships
        for i in range(15):
            x1 = (i % 16) * 25 + 20
            y1 = 50 + (i // 16) * 30
            x2 = ((i + 1) % 16) * 25 + 20
            y2 = 50 + ((i + 1) // 16) * 30
            
            if i % 4 == 0:  # Draw some connecting lines
                self.pattern_canvas.create_line(x1, y1, x2, y2, 
                                              fill=self.colors['grid_line'], width=1)
    
    def create_predictive_analytics_engine(self, parent):
        """Create the predictive analytics engine panel"""
        frame = tk.Frame(parent, bg=self.colors['bg_panel'], relief='solid', bd=2)
        frame.place(relx=0.51, rely=0.3, relwidth=0.47, relheight=0.35)
        
        # Title
        title_label = tk.Label(frame, text="⬜ PREDICTIVE ANALYTICS ENGINE ⬜", 
                              bg=self.colors['bg_panel'], fg=self.colors['neon_cyan'],
                              font=('Orbitron', 12, 'bold'))
        title_label.pack(pady=(10, 5))
        
        # Analytics content
        content_frame = tk.Frame(frame, bg=self.colors['bg_panel'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Left side - Bar chart
        chart_frame = tk.Frame(content_frame, bg=self.colors['bg_panel'])
        chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.analytics_canvas = Canvas(chart_frame, bg=self.colors['bg_panel'], 
                                     highlightthickness=0, height=150)
        self.analytics_canvas.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.create_analytics_chart()
        
        # Right side - Metrics
        metrics_frame = tk.Frame(content_frame, bg=self.colors['bg_panel'])
        metrics_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        # Create updatable prediction labels
        self.next_label = self.create_metric_pair(metrics_frame, "⬜ NEXT:", "▲ BULLISH", self.colors['neon_green'])
        self.accuracy_label = self.create_metric_pair(metrics_frame, "⬜ ACCURACY:", "89.0%", self.colors['neon_pink'])
        self.confidence_label = self.create_metric_pair(metrics_frame, "⬜ CONFIDENCE:", "76.5%", self.colors['neon_cyan'])
        self.horizon_label = self.create_metric_pair(metrics_frame, "⬜ HORIZON:", "5-30 MIN", self.colors['neon_green'])
    
    def create_analytics_chart(self):
        """Create the bullish/bearish bar chart"""
        # Clear canvas
        self.analytics_canvas.delete("all")
        
        bullish_bars = self.analytics_data['bullish_bars']
        bearish_bars = self.analytics_data['bearish_bars']
        
        bar_width = 20
        max_height = 80
        spacing = 25
        start_x = 20
        base_y = 120
        
        # Draw bullish bars (green, upward)
        for i, value in enumerate(bullish_bars):
            x = start_x + i * spacing
            height = (value / 10) * max_height
            self.analytics_canvas.create_rectangle(
                x, base_y - height, x + bar_width, base_y,
                fill=self.colors['neon_green'], outline=self.colors['neon_green']
            )
        
        # Draw bearish bars (red, downward)
        for i, value in enumerate(bearish_bars):
            x = start_x + i * spacing
            height = (value / 10) * max_height
            self.analytics_canvas.create_rectangle(
                x, base_y, x + bar_width, base_y + height,
                fill=self.colors['neon_pink'], outline=self.colors['neon_pink']
            )
    
    def create_quantum_data_stream(self, parent):
        """Create the quantum data stream panel"""
        frame = tk.Frame(parent, bg=self.colors['bg_panel'], relief='solid', bd=2)
        frame.place(relx=0.02, rely=0.68, relwidth=0.96, relheight=0.25)
        
        # Title
        title_label = tk.Label(frame, text="⬜ QUANTUM DATA STREAM ⬜", 
                              bg=self.colors['bg_panel'], fg=self.colors['neon_cyan'],
                              font=('Orbitron', 14, 'bold'))
        title_label.pack(pady=(10, 5))
        
        # Data stream content
        self.data_text = tk.Text(frame, bg=self.colors['bg_panel'], 
                                fg=self.colors['text_primary'],
                                font=('Courier New', 10),
                                height=8, wrap=tk.WORD,
                                insertbackground=self.colors['neon_cyan'],
                                state=tk.DISABLED)
        self.data_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Configure text colors
        self.data_text.tag_configure("neural", foreground=self.colors['neon_green'])
        self.data_text.tag_configure("pattern", foreground=self.colors['neon_cyan'])
        self.data_text.tag_configure("quantum", foreground=self.colors['neon_magenta'])
        self.data_text.tag_configure("predict", foreground=self.colors['neon_pink'])
        self.data_text.tag_configure("trading", foreground=self.colors['neon_yellow'])
        self.data_text.tag_configure("error", foreground=self.colors['danger'])
        
        self.update_data_stream()
    
    def create_quantum_status_bar(self, parent):
        """Create quantum status bar"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_dark'], height=30)
        status_frame.place(relx=0, rely=0.95, relwidth=1, relheight=0.05)
        
        self.status_text = "QUANTUM STATE: SUPERPOS | DIMENSIONS: 11 | REALITY: SIMULATED"
        self.status_label = tk.Label(status_frame, text=self.status_text,
                                   bg=self.colors['bg_dark'], fg=self.colors['neon_cyan'],
                                   font=('Courier New', 10))
        self.status_label.pack(side=tk.LEFT, padx=20)
    
    def create_trading_controls(self, parent):
        """Create floating trading control panel"""
        controls_frame = tk.Frame(parent, bg=self.colors['bg_panel'], relief='solid', bd=2)
        controls_frame.place(relx=0.85, rely=0.02, relwidth=0.13, relheight=0.15)
        
        tk.Label(controls_frame, text="QUANTUM CONTROLS", 
                bg=self.colors['bg_panel'], fg=self.colors['neon_cyan'],
                font=('Orbitron', 10, 'bold')).pack(pady=5)
        
        # Bot control buttons
        self.start_button = tk.Button(controls_frame, text="⬢ START BOT", 
                                     bg=self.colors['neon_green'], fg=self.colors['bg_dark'],
                                     font=('Courier New', 9, 'bold'),
                                     command=self.start_bot, relief='flat')
        self.start_button.pack(pady=2, padx=10, fill=tk.X)
        
        self.stop_button = tk.Button(controls_frame, text="⬢ STOP BOT", 
                                    bg=self.colors['danger'], fg=self.colors['text_primary'],
                                    font=('Courier New', 9, 'bold'),
                                    command=self.stop_bot, relief='flat', state=tk.DISABLED)
        self.stop_button.pack(pady=2, padx=10, fill=tk.X)
        
        self.reset_button = tk.Button(controls_frame, text="⬢ RESET", 
                                     bg=self.colors['neon_purple'], fg=self.colors['text_primary'],
                                     font=('Courier New', 9, 'bold'),
                                     command=self.reset_bot, relief='flat')
        self.reset_button.pack(pady=2, padx=10, fill=tk.X)
    
    def initialize_trading_bot(self):
        """Initialize the trading bot"""
        try:
            self.bot = MT5TradingBot()
            self.strategy_manager = StrategyManager()
            self.add_data_stream_message("NEURAL→", "Trading bot initialized", "neural")
        except Exception as e:
            self.add_data_stream_message("ERROR→", f"Bot init failed: {str(e)}", "error")
    
    def start_bot(self):
        """Start the trading bot"""
        if self.bot and not self.bot_running:
            try:
                # Start bot in separate thread
                bot_thread = threading.Thread(target=self._run_bot, daemon=True)
                bot_thread.start()
                
                self.bot_running = True
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                
                self.add_data_stream_message("QUANTUM→", "Bot started in superposition", "quantum")
                self.update_status_bar("QUANTUM STATE: ACTIVE | BOT: RUNNING")
                
            except Exception as e:
                self.add_data_stream_message("ERROR→", f"Failed to start bot: {str(e)}", "error")
    
    def stop_bot(self):
        """Stop the trading bot"""
        if self.bot and self.bot_running:
            self.bot_running = False
            if hasattr(self.bot, 'running'):
                self.bot.running = False
            
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            
            self.add_data_stream_message("QUANTUM→", "Bot collapsed to stopped state", "quantum")
            self.update_status_bar("QUANTUM STATE: SUPERPOS | BOT: STOPPED")
    
    def reset_bot(self):
        """Reset the trading bot"""
        self.stop_bot()
        self.initialize_trading_bot()
        self.add_data_stream_message("NEURAL→", "System reset complete", "neural")
    
    def _run_bot(self):
        """Run the trading bot in a separate thread"""
        if self.bot:
            try:
                self.bot.run()
            except Exception as e:
                self.add_data_stream_message("ERROR→", f"Bot error: {str(e)}", "error")
    
    def add_data_stream_message(self, prefix, message, tag="neural"):
        """Add message to data stream"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {prefix} {message}"
        
        self.data_stream_messages.append((full_message, tag))
        if len(self.data_stream_messages) > 20:  # Keep only last 20 messages
            self.data_stream_messages.pop(0)
        
        # Update display
        self.root.after(0, self._update_data_stream_display)
    
    def _update_data_stream_display(self):
        """Update the data stream display"""
        self.data_text.config(state=tk.NORMAL)
        self.data_text.delete(1.0, tk.END)
        
        for message, tag in self.data_stream_messages:
            self.data_text.insert(tk.END, f"{message}\n", tag)
        
        self.data_text.config(state=tk.DISABLED)
        self.data_text.see(tk.END)
    
    def update_data_stream(self):
        """Initialize the quantum data stream with default messages"""
        initial_messages = [
            ("NEURAL→", "0x04936904 >> SCAN [2%]", "neural"),
            ("PATTERN→", "INSIDE BAR detected 95.3%", "pattern"),
            ("QUANTUM→", "State: |10⟩ Prob:21%", "quantum"),
            ("NEURAL→", "0x885DBC64 >> EVAL [30%]", "neural"),
            ("PREDICT→", "Next 2 bars: ↑", "predict")
        ]
        
        for prefix, data, tag in initial_messages:
            self.add_data_stream_message(prefix, data, tag)
    
    def update_status_bar(self, text):
        """Update the status bar text"""
        self.status_text = text
        self.status_label.config(text=text)
    
    def start_quantum_animations(self):
        """Start quantum animations"""
        self.animate_quantum_grid()
        self.animate_background_dots()
        
    def start_data_monitoring(self):
        """Start monitoring trading data"""
        self.monitor_trading_data()
        
    def monitor_trading_data(self):
        """Monitor and update trading data"""
        if self.bot:
            try:
                # Update account information
                # Note: This would normally come from the actual MT5 bot
                self.update_quantum_metrics()
                
                # Generate some quantum activity
                if random.random() < 0.3:  # 30% chance of new message
                    messages = [
                        ("NEURAL→", f"Pattern scan {random.randint(10, 99)}% complete", "neural"),
                        ("QUANTUM→", f"Entanglement level: {random.randint(70, 99)}%", "quantum"),
                        ("PATTERN→", f"Fibonacci retracement detected", "pattern"),
                        ("PREDICT→", f"Market sentiment: {'BULLISH' if random.random() > 0.5 else 'BEARISH'}", "predict"),
                        ("TRADING→", f"Risk assessment: {random.choice(['LOW', 'MEDIUM', 'HIGH'])}", "trading")
                    ]
                    prefix, message, tag = random.choice(messages)
                    self.add_data_stream_message(prefix, message, tag)
                
            except Exception as e:
                self.add_data_stream_message("ERROR→", f"Data monitoring error: {str(e)}", "error")
        
        # Schedule next monitoring
        self.root.after(2000, self.monitor_trading_data)
    
    def update_quantum_metrics(self):
        """Update quantum processing metrics with real-time data"""
        # Simulate quantum processing metrics
        qubits = random.randint(1000, 1200)
        speed = f"{random.uniform(6.0, 8.5):.1f} THz"
        
        # Update labels
        self.qubits_label.config(text=str(qubits))
        self.speed_label.config(text=speed)
        
        # Update analytics data periodically
        if random.random() < 0.1:  # 10% chance to update analytics
            self.analytics_data['accuracy'] = random.uniform(85, 95)
            self.analytics_data['confidence'] = random.uniform(70, 85)
            self.accuracy_label.config(text=f"{self.analytics_data['accuracy']:.1f}%")
            self.confidence_label.config(text=f"{self.analytics_data['confidence']:.1f}%")
            
            # Update bar chart
            self.analytics_data['bullish_bars'] = [random.randint(5, 10) for _ in range(10)]
            self.analytics_data['bearish_bars'] = [random.randint(2, 7) for _ in range(10)]
            self.create_analytics_chart()
    
    def animate_quantum_grid(self):
        """Animate the quantum grid colors"""
        if hasattr(self, 'qubit_rects'):
            colors = [self.colors['neon_cyan'], self.colors['neon_magenta'], 
                     self.colors['neon_green'], self.colors['neon_purple'], 
                     self.colors['neon_pink']]
            
            # Randomly change some grid colors
            for _ in range(5):  # Change 5 random cells
                row = random.randint(0, 7)
                col = random.randint(0, 15)
                color = random.choice(colors)
                
                if row < len(self.qubit_rects) and col < len(self.qubit_rects[row]):
                    rect = self.qubit_rects[row][col]
                    self.qubit_canvas.itemconfig(rect, fill=color, outline=color)
        
        # Schedule next animation
        self.root.after(500, self.animate_quantum_grid)
    
    def animate_background_dots(self):
        """Create animated quantum dots in background"""
        if hasattr(self, 'bg_canvas'):
            # Clear previous dots
            self.bg_canvas.delete("quantum_dot")
            
            # Create new quantum dots
            width = self.bg_canvas.winfo_width() or 1600
            height = self.bg_canvas.winfo_height() or 1000
            
            # Circular pattern of dots
            center_x, center_y = width - 200, 200
            num_rings = 8
            
            for ring in range(num_rings):
                radius = 20 + ring * 15
                dots_in_ring = max(8, ring * 4)
                
                for i in range(dots_in_ring):
                    angle = (2 * math.pi * i) / dots_in_ring + time.time() * 0.5
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    
                    # Vary dot size and color
                    dot_size = 2 + random.random() * 3
                    alpha = 0.3 + 0.7 * (1 - ring / num_rings)
                    
                    color = self.colors['neon_cyan'] if ring % 2 == 0 else self.colors['neon_magenta']
                    
                    self.bg_canvas.create_oval(
                        x - dot_size, y - dot_size, x + dot_size, y + dot_size,
                        fill=color, outline=color, tags="quantum_dot"
                    )
        
        # Schedule next animation
        self.root.after(100, self.animate_background_dots)
    
    def load_config(self):
        """Load trading bot configuration"""
        try:
            config_path = Path("config.json")
            if config_path.exists():
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
                self.add_data_stream_message("NEURAL→", "Configuration loaded successfully", "neural")
            else:
                self.config = self.get_default_config()
                self.add_data_stream_message("NEURAL→", "Using default configuration", "neural")
        except Exception as e:
            self.add_data_stream_message("ERROR→", f"Config error: {e}", "error")
            self.config = self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            "mt5": {
                "login": 0,
                "password": "",
                "server": ""
            },
            "trading": {
                "symbols": ["EURUSD", "GBPUSD"],
                "risk_per_trade": 0.02,
                "max_positions": 5
            }
        }
    
    def on_closing(self):
        """Handle window closing"""
        if self.bot_running:
            self.stop_bot()
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run the quantum GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = QuantumTradingGUI()
    app.run()