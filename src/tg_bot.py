import json

import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from src.main import check_case
from src.parser import parse_data_from_url

token = "6292849744:AAHrXcVM6LJmO9a78D05KiSFWQD64YS22Ow"
bot = telebot.TeleBot(token=token)

user_state = {}
def get_color_emoji(percentage):
    if percentage < 30:
        return "🔴"
    elif 30 <= percentage < 80:
        return "🟡"
    else:
        return "🟢"

def process_url(message):
    url2process = message.text
    print(url2process)
    # resp_json = parse_data_from_url(url2process)
    #
    # answers = check_case(resp_json)
    # print(answers)
    #
    # for k, v in answers.items():
    #     bot.send_message(message.chat.id, f"{k}: {v}")


#     bot.send_message(
#         message.chat.id,
#         r'''
#     *1\. Название КС:*
#     На сайте:
#     Совпадение в проекте: 22%
#     Совпадение в ТЗ: 50%
#
# *2\. Обеспечение исполнения контракта:*
#     \(\ требуется\)
#     Размер обеспечения на сайте:
#     Cовпадение в проекте: 90%
#     Совпадение в ТЗ: 80%
#
# *3\. Наличие сертификатов/лицензий:*
# *4\. График поставки:*
#     ''',
#         parse_mode='MarkdownV2'
#     )

    project_match_ks = 22
    tz_match_ks = 50
    project_match_contract = 90
    tz_match_contract = 80

    bot.send_message(
        message.chat.id,
        r'''
    *1\. Название КС:*
    На сайте: 
    Совпадение в проекте: {}% {}
    Совпадение в ТЗ: {}% {}

    *2\. Обеспечение исполнения контракта:*
    \(\ требуется\)
    Размер обеспечения на сайте:
    Совпадение в проекте: {}% {}
    Совпадение в ТЗ: {}% {}

    *3\. Наличие сертификатов/лицензий:*
    *4\. График поставки:*
    '''.format(project_match_ks, get_color_emoji(project_match_ks),
               tz_match_ks, get_color_emoji(tz_match_ks),
               project_match_contract, get_color_emoji(project_match_contract),
               tz_match_contract, get_color_emoji(tz_match_contract)),
        parse_mode='MarkdownV2'
    )



    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = KeyboardButton('Снять с публикации КС')
    button2 = KeyboardButton('Подтвердить корректность КС')

    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Выберите одну из опций:", reply_markup=markup)


# Обработка сообщений
@bot.message_handler(func=lambda message: message.text == "Снять с публикации КС")
def remove_from_publication(message):
    user_state[message.chat.id] = 'waiting_for_reason'
    bot.send_message(message.chat.id, "Пожалуйста, укажите причину снятия с публикации",
                     reply_markup=types.ReplyKeyboardRemove())


# Обработка текста с причиной
@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == 'waiting_for_reason')
def handle_reason(message):
    reason = message.text
    bot.send_message(message.chat.id, f"Снято с публикации по причине: {reason}")
    user_state[message.chat.id] = None

@bot.message_handler(func=lambda message: message.text == "Подтвердить корректность КС")
def confirm_correctness(message):
    bot.send_message(message.chat.id, "КС подтверждена!", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Введите URL:")
    bot.register_next_step_handler(message, process_url)


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
