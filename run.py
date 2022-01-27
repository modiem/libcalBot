from libcalBot.main import Booking

with Booking() as bot:
  bot.to_reserve_page()
  bot.login()
  bot.select_loc()
  bot.to_date()
  bot.pick_room(capacity="1")
  print(bot.room)
  bot.reserve_room(time="8:30am")
  bot.make_another_reservation()

  bot.select_loc()
  bot.to_date()
  bot.reserve_room(time="11:30am")
