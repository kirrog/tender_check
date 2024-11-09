import telebot

token = None
bot = telebot.TeleBot(token=token.txt)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Введите URL:")
    bot.register_next_step_handler(message)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, "/start - начать проверку")
    bot.send_message(message.chat.id, "/edit – редактирование котировочной сессии")
    bot.send_message(message.chat.id, "/confirm – подтвердить корректность котировочной сессии")
    bot.send_message(message.chat.id, "/reject – снять с публикации котировочную сессию")
    bot.send_message(message.chat.id, "/end_session – закончить сессию")


@bot.message_handler(commands=['edit'])  # редактирование котировочной сессии
def edit_message(message):
    bot.send_message(message.chat.id, '''edit message is okay''')


@bot.message_handler(commands=['confirm'])  # подтвердить корректность котировочной сессии
def confirm_message(message):
    bot.send_message(message.chat.id, '''confirm is okay''')


@bot.message_handler(commands=['reject'])  # снять с публикации котировочную сессию
def reject_message(message):
    bot.send_message(message.chat.id, '''reject is okay''')


@bot.message_handler(commands=['end_session'])  # закончить сессию
def end_session_message(message):
    bot.send_message(message.chat.id, '''end_session is okay''')


bot.infinity_polling(none_stop=True)