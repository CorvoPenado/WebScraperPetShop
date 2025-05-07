from booking.booking import Booking

with Booking() as bot:
    bot.land_passaro()
    bot.aplly_filtration()
    print('Exiting...')