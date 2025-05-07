from booking.booking import Booking

with Booking() as bot:
    bot.land_gato()
    bot.aplly_filtration()
    print('Exiting...')