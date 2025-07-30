"""
System Tray Integration for MT5 Trading Bot GUI
Provides minimize to tray functionality and quick access controls
"""

import tkinter as tk
from tkinter import messagebox
import threading
import sys
import os
from PIL import Image, ImageDraw
import io
import base64

try:
    import pystray
    from pystray import MenuItem as item
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    print("pystray not available. System tray functionality disabled.")

class SystemTrayManager:
    def __init__(self, gui_app):
        self.gui_app = gui_app
        self.icon = None
        self.tray_thread = None
        self.running = False
        
        if TRAY_AVAILABLE:
            self.setup_tray_icon()
    
    def create_icon_image(self, color="green"):
        """Create a simple icon image for the system tray"""
        # Create a 64x64 image with a circle
        size = (64, 64)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw circle based on bot status
        if color == "green":
            fill_color = (0, 255, 0, 255)  # Green for running
        elif color == "red":
            fill_color = (255, 0, 0, 255)  # Red for stopped
        else:
            fill_color = (255, 165, 0, 255)  # Orange for error
        
        # Draw main circle
        draw.ellipse([8, 8, 56, 56], fill=fill_color, outline=(0, 0, 0, 255), width=2)
        
        # Draw MT5 text
        try:
            from PIL import ImageFont
            # Try to load a font, fall back to default if not available
            try:
                font = ImageFont.truetype("arial.ttf", 12)
            except:
                font = ImageFont.load_default()
            
            # Get text size and center it
            text = "MT5"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (size[0] - text_width) // 2
            y = (size[1] - text_height) // 2
            
            draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
        except:
            # Fallback to simple text
            draw.text((22, 28), "MT5", fill=(255, 255, 255, 255))
        
        return image
    
    def setup_tray_icon(self):
        """Setup the system tray icon and menu"""
        if not TRAY_AVAILABLE:
            return
        
        # Create initial icon
        icon_image = self.create_icon_image("red")  # Start with red (stopped)
        
        # Create menu items
        menu = pystray.Menu(
            item('Show/Hide Window', self.toggle_window),
            item('Bot Status', self.show_status),
            pystray.Menu.SEPARATOR,
            item('Start Bot', self.start_bot_from_tray, enabled=lambda item: not self.gui_app.bot_running),
            item('Stop Bot', self.stop_bot_from_tray, enabled=lambda item: self.gui_app.bot_running),
            pystray.Menu.SEPARATOR,
            item('Quick Stats', self.show_quick_stats),
            item('View Logs', self.show_logs),
            pystray.Menu.SEPARATOR,
            item('Settings', self.show_settings),
            item('Exit', self.quit_application)
        )
        
        # Create icon
        self.icon = pystray.Icon(
            "MT5TradingBot",
            icon_image,
            "MT5 Advanced Trading Bot",
            menu
        )
    
    def start_tray(self):
        """Start the system tray in a separate thread"""
        if not TRAY_AVAILABLE or self.running:
            return
        
        self.running = True
        self.tray_thread = threading.Thread(target=self._run_tray, daemon=True)
        self.tray_thread.start()
    
    def _run_tray(self):
        """Run the system tray (internal method)"""
        try:
            self.icon.run()
        except Exception as e:
            print(f"Tray error: {e}")
    
    def stop_tray(self):
        """Stop the system tray"""
        if self.icon and self.running:
            self.running = False
            try:
                self.icon.stop()
            except:
                pass
    
    def update_icon_status(self, status):
        """Update the tray icon based on bot status"""
        if not TRAY_AVAILABLE or not self.icon:
            return
        
        try:
            if status == "running":
                new_image = self.create_icon_image("green")
                title = "MT5 Trading Bot - Running"
            elif status == "stopped":
                new_image = self.create_icon_image("red")
                title = "MT5 Trading Bot - Stopped"
            else:
                new_image = self.create_icon_image("orange")
                title = "MT5 Trading Bot - Error"
            
            self.icon.icon = new_image
            self.icon.title = title
        except Exception as e:
            print(f"Error updating tray icon: {e}")
    
    def show_notification(self, title, message, timeout=5):
        """Show a system notification"""
        if not TRAY_AVAILABLE or not self.icon:
            return
        
        try:
            self.icon.notify(message, title=title, timeout=timeout)
        except Exception as e:
            print(f"Error showing notification: {e}")
    
    def toggle_window(self, icon, item):
        """Toggle main window visibility"""
        try:
            if self.gui_app.root.state() == 'withdrawn':
                self.gui_app.root.deiconify()
                self.gui_app.root.lift()
                self.gui_app.root.focus_force()
            else:
                self.gui_app.root.withdraw()
        except Exception as e:
            print(f"Error toggling window: {e}")
    
    def show_status(self, icon, item):
        """Show bot status in a message box"""
        try:
            if self.gui_app.bot_running:
                status = "Bot is currently RUNNING"
                # Get additional stats if available
                if hasattr(self.gui_app, 'strategy_manager') and self.gui_app.strategy_manager:
                    performance = self.gui_app.strategy_manager.get_all_performance()
                    total_trades = sum(p.total_trades for p in performance.values())
                    status += f"\n\nTotal Trades: {total_trades}"
                    
                    if performance:
                        total_profit = sum(p.total_profit - p.total_loss for p in performance.values())
                        status += f"\nTotal P&L: ${total_profit:.2f}"
            else:
                status = "Bot is currently STOPPED"
            
            # Show message box in main thread
            self.gui_app.root.after(0, lambda: messagebox.showinfo("Bot Status", status))
            
        except Exception as e:
            print(f"Error showing status: {e}")
    
    def start_bot_from_tray(self, icon, item):
        """Start bot from tray menu"""
        try:
            self.gui_app.root.after(0, self.gui_app.start_bot)
            self.show_notification("Bot Starting", "Trading bot is starting up...")
        except Exception as e:
            print(f"Error starting bot from tray: {e}")
    
    def stop_bot_from_tray(self, icon, item):
        """Stop bot from tray menu"""
        try:
            self.gui_app.root.after(0, self.gui_app.stop_bot)
            self.show_notification("Bot Stopping", "Trading bot is shutting down...")
        except Exception as e:
            print(f"Error stopping bot from tray: {e}")
    
    def show_quick_stats(self, icon, item):
        """Show quick statistics"""
        try:
            stats_msg = "Quick Statistics:\n\n"
            
            if self.gui_app.bot_running and hasattr(self.gui_app, 'strategy_manager') and self.gui_app.strategy_manager:
                performance = self.gui_app.strategy_manager.get_all_performance()
                
                if performance:
                    total_trades = sum(p.total_trades for p in performance.values())
                    total_profit = sum(p.total_profit - p.total_loss for p in performance.values())
                    avg_win_rate = sum(p.win_rate for p in performance.values()) / len(performance)
                    
                    stats_msg += f"Total Trades: {total_trades}\n"
                    stats_msg += f"Total P&L: ${total_profit:.2f}\n"
                    stats_msg += f"Average Win Rate: {avg_win_rate:.1%}\n"
                    
                    # Show best performing strategy
                    best_strategy = max(performance.items(), key=lambda x: x[1].total_profit - x[1].total_loss)
                    stats_msg += f"\nBest Strategy: {best_strategy[0]}\n"
                    stats_msg += f"P&L: ${best_strategy[1].total_profit - best_strategy[1].total_loss:.2f}"
                else:
                    stats_msg += "No performance data available yet."
            else:
                stats_msg += "Bot is not running.\nNo statistics available."
            
            # Show in main thread
            self.gui_app.root.after(0, lambda: messagebox.showinfo("Quick Statistics", stats_msg))
            
        except Exception as e:
            print(f"Error showing quick stats: {e}")
            self.gui_app.root.after(0, lambda: messagebox.showerror("Error", f"Error getting statistics: {e}"))
    
    def show_logs(self, icon, item):
        """Show the main window with logs tab active"""
        try:
            # Show main window
            self.gui_app.root.deiconify()
            self.gui_app.root.lift()
            self.gui_app.root.focus_force()
            
            # Switch to logs tab
            self.gui_app.notebook.select(5)  # Logs is the 6th tab (index 5)
            
        except Exception as e:
            print(f"Error showing logs: {e}")
    
    def show_settings(self, icon, item):
        """Show the main window with configuration tab active"""
        try:
            # Show main window
            self.gui_app.root.deiconify()
            self.gui_app.root.lift()
            self.gui_app.root.focus_force()
            
            # Switch to configuration tab
            self.gui_app.notebook.select(2)  # Configuration is the 3rd tab (index 2)
            
        except Exception as e:
            print(f"Error showing settings: {e}")
    
    def quit_application(self, icon, item):
        """Quit the entire application"""
        try:
            # Ask for confirmation in main thread
            def confirm_quit():
                if self.gui_app.bot_running:
                    result = messagebox.askyesno(
                        "Quit Application", 
                        "Bot is running. Stop bot and quit application?"
                    )
                else:
                    result = messagebox.askyesno(
                        "Quit Application", 
                        "Are you sure you want to quit the application?"
                    )
                
                if result:
                    self.gui_app.on_closing()
            
            self.gui_app.root.after(0, confirm_quit)
            
        except Exception as e:
            print(f"Error quitting application: {e}")

# Installation helper for pystray
def install_pystray():
    """Helper function to install pystray if not available"""
    try:
        import subprocess
        import sys
        
        print("Installing pystray for system tray functionality...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pystray', 'Pillow'])
        print("pystray installed successfully!")
        return True
    except Exception as e:
        print(f"Failed to install pystray: {e}")
        return False

def check_tray_dependencies():
    """Check if system tray dependencies are available"""
    try:
        import pystray
        from PIL import Image, ImageDraw
        return True
    except ImportError as e:
        print(f"Missing dependencies for system tray: {e}")
        print("To enable system tray functionality, install with:")
        print("pip install pystray Pillow")
        return False

if __name__ == "__main__":
    # Test the tray functionality
    if check_tray_dependencies():
        print("System tray dependencies are available")
    else:
        print("System tray dependencies are missing")
        if input("Install now? (y/n): ").lower() == 'y':
            install_pystray()