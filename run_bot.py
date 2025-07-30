#!/usr/bin/env python3
"""
MT5 Trading Bot Runner Script
Provides easy startup with different configurations and modes
"""

import argparse
import sys
import time
import signal
from pathlib import Path
import json
import logging
from mt5_trading_bot import MT5TradingBot
from strategy_manager import StrategyManager

def setup_logging(level="INFO", log_file="trading_bot.log"):
    """Setup logging configuration"""
    log_level = getattr(logging, level.upper())
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

def signal_handler(signum, frame):
    """Handle interrupt signals gracefully"""
    print("\nReceived interrupt signal. Shutting down gracefully...")
    sys.exit(0)

def validate_config(config_path):
    """Validate configuration file"""
    if not Path(config_path).exists():
        print(f"Error: Configuration file '{config_path}' not found.")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        required_fields = ['account', 'password', 'server', 'symbols']
        for field in required_fields:
            if field not in config:
                print(f"Error: Missing required field '{field}' in configuration.")
                return False
        
        return True
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in configuration file '{config_path}'.")
        return False

def run_performance_report(config_path):
    """Generate and display performance report"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        manager = StrategyManager(config)
        report = manager.generate_performance_report()
        print(report)
        
        # Export data
        manager.export_data()
        print("\nPerformance data exported to 'trading_data_export.json'")
        
    except Exception as e:
        print(f"Error generating performance report: {e}")

def list_strategies(config_path):
    """List all available strategies and their status"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print("=== AVAILABLE STRATEGIES ===")
        print(f"{'Strategy':<15} {'Status':<10} {'Weight':<8}")
        print("-" * 35)
        
        for strategy, settings in config.get('strategies', {}).items():
            status = "ENABLED" if settings.get('enabled', False) else "DISABLED"
            weight = settings.get('weight', 1.0)
            print(f"{strategy:<15} {status:<10} {weight:<8.1f}")
        
    except Exception as e:
        print(f"Error listing strategies: {e}")

def enable_strategy(config_path, strategy_name):
    """Enable a specific strategy"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if strategy_name in config.get('strategies', {}):
            config['strategies'][strategy_name]['enabled'] = True
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"Strategy '{strategy_name}' enabled successfully.")
        else:
            print(f"Strategy '{strategy_name}' not found in configuration.")
    
    except Exception as e:
        print(f"Error enabling strategy: {e}")

def disable_strategy(config_path, strategy_name):
    """Disable a specific strategy"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if strategy_name in config.get('strategies', {}):
            config['strategies'][strategy_name]['enabled'] = False
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"Strategy '{strategy_name}' disabled successfully.")
        else:
            print(f"Strategy '{strategy_name}' not found in configuration.")
    
    except Exception as e:
        print(f"Error disabling strategy: {e}")

def create_sample_config():
    """Create a sample configuration file"""
    sample_config = {
        "account": 123456,
        "password": "your_mt5_password",
        "server": "your_broker_server",
        "symbols": ["EURUSD", "GBPUSD", "USDJPY"],
        "risk_per_trade": 0.02,
        "max_positions": 5,
        "strategies": {
            "kt_gmac": {"enabled": True, "weight": 1.0},
            "martingale": {"enabled": False, "weight": 1.0},
            "hft": {"enabled": True, "weight": 0.5}
        }
    }
    
    with open("sample_config.json", 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print("Sample configuration created as 'sample_config.json'")
    print("Please edit with your MT5 credentials before running the bot.")

def main():
    parser = argparse.ArgumentParser(description="MT5 Trading Bot Runner")
    parser.add_argument(
        "--config", "-c",
        default="config.json",
        help="Configuration file path (default: config.json)"
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["trade", "report", "list", "sample"],
        default="trade",
        help="Operation mode (default: trade)"
    )
    parser.add_argument(
        "--log-level", "-l",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    parser.add_argument(
        "--log-file",
        default="trading_bot.log",
        help="Log file path (default: trading_bot.log)"
    )
    parser.add_argument(
        "--enable",
        help="Enable a specific strategy"
    )
    parser.add_argument(
        "--disable", 
        help="Disable a specific strategy"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in simulation mode (no real trades)"
    )
    
    args = parser.parse_args()
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Handle special modes
    if args.mode == "sample":
        create_sample_config()
        return
    
    if args.enable:
        enable_strategy(args.config, args.enable)
        return
    
    if args.disable:
        disable_strategy(args.config, args.disable)
        return
    
    if args.mode == "list":
        list_strategies(args.config)
        return
    
    if args.mode == "report":
        run_performance_report(args.config)
        return
    
    # Validate configuration
    if not validate_config(args.config):
        return
    
    # Setup logging
    setup_logging(args.log_level, args.log_file)
    
    print("=" * 50)
    print("MT5 ADVANCED TRADING BOT")
    print("=" * 50)
    print(f"Configuration: {args.config}")
    print(f"Log Level: {args.log_level}")
    print(f"Dry Run: {'Yes' if args.dry_run else 'No'}")
    print("=" * 50)
    
    # Start the bot
    try:
        bot = MT5TradingBot(args.config)
        
        if args.dry_run:
            print("Running in DRY RUN mode - no real trades will be executed")
            # You could modify the bot to support dry run mode
        
        if bot.start():
            print("Bot started successfully!")
            print("Press Ctrl+C to stop the bot")
            print("-" * 50)
            
            # Keep the bot running
            while bot.running:
                time.sleep(1)
        else:
            print("Failed to start the bot. Check your configuration and MT5 connection.")
            
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.error(f"Unexpected error: {e}", exc_info=True)
    finally:
        try:
            bot.stop()
        except:
            pass
        print("Bot stopped successfully")

if __name__ == "__main__":
    main()