import os
import sys
from bot.booking import Booking

def main():
    """Main function to run the bot."""
    try:
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        with Booking(base_path=base_path) as bot:
            bot.land_cachorro_racao_seca_adulto_gigante()
            bot.aplly_filtration()
            print('Exiting...')
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main() 