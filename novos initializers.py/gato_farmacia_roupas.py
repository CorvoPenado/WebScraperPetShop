import os
import sys
from bot.booking import Booking

def main():
    """Main function to run the bot."""
    try:
        # Get the base path
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Initialize and run the bot
        with Booking(base_path=base_path) as bot:
            bot.land_gato_farmacia_roupas()
            bot.aplly_filtration()
            print('Exiting...')
    except Exception as e:
        print(f"Error in main function: {e}")

def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

if __name__ == "__main__":
    main()