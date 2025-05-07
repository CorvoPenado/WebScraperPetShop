from booking.booking import Booking

with Booking() as bot:
    bot.land_testePeixe()
    bot.aplly_filtration()
    print('Exiting...')