#!/usr/bin/env python3
"""
Quantum Trading GUI Launcher
Direct launcher for the quantum-themed trading interface
"""

import sys
import os
from pathlib import Path

def main():
    """Launch the quantum trading GUI"""
    print("=" * 60)
    print("🌌 QUANTUM TRADING MATRIX INITIALIZING 🌌")
    print("=" * 60)
    print("Loading quantum trading interface...")
    print("Establishing entanglement with market data...")
    print("Calibrating quantum processing matrix...")
    print("=" * 60)
    
    try:
        # Import and launch quantum GUI
        from quantum_trading_gui import QuantumTradingGUI
        
        print("✓ Quantum interface loaded successfully")
        print("✓ Reality simulation: ACTIVE")
        print("✓ Quantum state: SUPERPOSITION")
        print("\nLaunching quantum trading matrix...")
        print("=" * 60)
        
        # Create and run the quantum GUI
        gui = QuantumTradingGUI()
        gui.run()
        
    except ImportError as e:
        print(f"❌ Failed to import quantum GUI: {e}")
        print("\nPlease ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching quantum GUI: {e}")
        sys.exit(1)
    finally:
        print("\nQuantum trading matrix deactivated")
        print("Returning to classical reality...")

if __name__ == "__main__":
    main()