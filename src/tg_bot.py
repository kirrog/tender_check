import json

import telebot
from telebot import types
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from main import check_case
from parser import parse_data_from_url

token = "7725548623:AAEEI6tTTaFWvolQ2bv2yvK91W3BBr6xEi4"
bot = telebot.TeleBot(token=token)

user_state = {}

def process_url(message):
    url2process = message.text
    print(url2process)
    resp_json = parse_data_from_url(url2process)

    answers = check_case(resp_json)
    print(answers)

    if 'items_0_name' in answers['technical']:
        if answers['project']['isContractGuaranteeRequired']['value_'] == 'true':
            obespechenie_str = f"""Требуется
            Размер обеспечения на сайте: {answers['project']['contractGuaranteeAmount']['value_']}
            Совпадение в проекте: {answers['project']['contractGuaranteeAmount']['leven_partial_ratio']}%
            Совпадение в тз: {answers['technical']['contractGuaranteeAmount']['leven_partial_ratio']}%
            """
        else:
            obespechenie_str = """Не требуется
            """

        if 'licenseFiles_0' in answers['project']:
            sertificates_str = f"""Присутвует
            Наименование на сайте: {answers['project']['licenseFiles_0']['value_']['name']}
            Совпадение в проекте: {answers['project']['licenseFiles_0']['leven_partial_ratio']}%
            Совпадение в тз: {answers['technical']['licenseFiles_0']['leven_partial_ratio']}%
            """
        else:
            sertificates_str = """Отсутствует
            """


        if 'startCost' in answers['project']:
            cost_needed_str = f"""Начальная цена: присутствует на сайте
            Совпадение в проекте: {answers['project']['startCost']['leven_partial_ratio']}%
            Совпадение в тз: {answers['technical']['startCost']['leven_partial_ratio']}%
    
            Максимальное значение цены контракта: отсутствет на сайте
            """
        else:
            cost_needed_str = f"""Начальная цена: отсутствует на сайте
    
                    Максимальное значение цены контракта: присутствует на сайте
                    Совпадение в проекте: {answers['project']['startCost']['leven_partial_ratio']}%
                    Совпадение в тз: {answers['technical']['startCost']['leven_partial_ratio']}%
                   """

        date = ""
        i = 0
        for i in range(99999):
            if f'deliveries_{str(i)}_periodDateFrom' in answers['project'] and \
                    answers['project'][f'deliveries_{str(i)}_periodDateFrom']['value_'] is not None:
                date += f"Этап {str(i)}\n"
                date += f"""Дата начала поставки на сайте: {answers['project'][f'deliveries_{str(i)}_periodDateFrom']['value_']}
                Совпадение в проекте: {answers['project'][f'deliveries_{str(i)}_periodDateFrom']['leven_partial_ratio']}%
                Совпадение в тз: {answers['technical'][f'deliveries_{str(i)}_periodDateFrom']['leven_partial_ratio']}%\n
                """
            elif f'deliveries_{str(i)}_periodDaysFrom' in answers['project'] and \
                    answers['project'][f'deliveries_{str(i)}_periodDaysFrom']['value_'] is not None:
                date += f"Этап {str(i)}\n"
                date += f"""Начало срока поставки на сайте: {answers['project'][f'deliveries_{str(i)}_periodDaysFrom']['value_']}
                Совпадение в проекте: {answers['project'][f'deliveries_{str(i)}_periodDaysFrom']['leven_partial_ratio']}%
                Совпадение в тз: {answers['technical'][f'deliveries_{str(i)}_periodDaysFrom']['leven_partial_ratio']}%\n
                """
            else:
                date += "\n"
                break

            if f'deliveries_{str(i)}_periodDateTo' in answers['project'] and answers['project'][f'deliveries_{str(i)}_periodDateTo']['value_'] is not None:
                date += f"""Дата окончания поставки на сайте: {answers['project'][f'deliveries_{str(i)}_periodDateTo']['value_']}
                Совпадение в проекте: {answers['project'][f'deliveries_{str(i)}_periodDateTo']['leven_partial_ratio']}%
                Совпадение в тз: {answers['technical'][f'deliveries_{str(i)}_periodDateTo']['leven_partial_ratio']}%\n
                """
            elif f'deliveries_{str(i)}_periodDaysTo' in answers['project'] and answers['project'][f'deliveries_{str(i)}_periodDaysTo']['value_'] is not None:
                date += f"""Окончание срока поставки на сайте: {answers['project'][f'deliveries_{str(i)}_periodDaysTo']['value_']}
                Совпадение в проекте: {answers['project'][f'deliveries_{str(i)}_periodDaysTo']['leven_partial_ratio']}%
                Совпадение в тз: {answers['technical'][f'deliveries_{str(i)}_periodDaysTo']['leven_partial_ratio']}%\n
                """
            else:
                date += "\n"
                break


        i = 0
        if 'items_0_name' in answers['technical']:
            specification_str = "ТЗ присутствует\n"
        else:
            specification_str = "ТЗ отсутствует"
        for i in range(99999):
            if f'items_{str(i)}_name' in answers['technical']:
                specification_str += f"""  
                Наименование спецификации на сайте: {answers['technical'][f'items_{str(i)}_name']['value_']}
                Совпадение в ТЗ: {answers['technical'][f'items_{str(i)}_name']['leven_partial_ratio']}%
                Количество предметов на сайте: {answers['technical'][f'items_{str(i)}_currentValue']['value_']}
                Совпадение в ТЗ: {answers['technical'][f'items_{str(i)}_currentValue']['leven_partial_ratio']}%
                """
            else:
                break

        answer = f"""
            1. Название КС
            На сайте: {answers['project']['name']['value_']}
            Совпадение в проекте: {int(answers['project']['name']['leven_partial_ratio'])}%
            Совпадение в тз: {int(answers['technical']['name']['leven_partial_ratio'])}%

            2. Обеспечение исполнения контракта
            {obespechenie_str}

            3. Наличие сертификатов/лицензий
            {sertificates_str}

            4. График поставки
            {date}

            5. Цена контракта
            {cost_needed_str}

            6. Спецификация
            {specification_str}
            """

    else:
        if answers['project']['isContractGuaranteeRequired']['value_'] == 'true':
            obespechenie_str = f"""Требуется
            Размер обеспечения на сайте: {answers['project']['contractGuaranteeAmount']['value_']}
            Совпадение в проекте: {answers['project']['contractGuaranteeAmount']['leven_partial_ratio']}%
            """
        else:
            obespechenie_str = """Не требуется
            """

        if 'licenseFiles_0' in answers['project']:
            sertificates_str = f"""Присутвует
            Наименование на сайте: {answers['project']['licenseFiles_0']['value_']['name']}
            Совпадение в проекте: {answers['project']['licenseFiles_0']['leven_partial_ratio']}%
            """
        else:
            sertificates_str = """Отсутствует
            """

        if 'startCost' in answers['project']:
            cost_needed_str = f"""Начальная цена: присутствует на сайте
            Совпадение в проекте: {answers['project']['startCost']['leven_partial_ratio']}%

            Максимальное значение цены контракта: отсутствет на сайте
            """
        else:
            cost_needed_str = f"""Начальная цена: отсутствует на сайте

                    Максимальное значение цены контракта: присутствует на сайте
                    Совпадение в проекте: {answers['project']['startCost']['leven_partial_ratio']}%
                   """

        date = ""
        i = 0
        for i in range(99999):
            if f'deliveries_{str(i)}_periodDateFrom' in answers['project'] and \
                    answers['project'][f'deliveries_{str(i)}_periodDateFrom']['value_'] is not None:
                date += f"Этап {str(i)}\n"
                date += f"""Дата начала поставки на сайте: {answers['project'][f'deliveries_{str(i)}_periodDateFrom']['value_']}
                Совпадение в проекте: {answers['project'][f'deliveries_{str(i)}_periodDateFrom']['leven_partial_ratio']}%
                """
            elif f'deliveries_{str(i)}_periodDaysFrom' in answers['project'] and \
                    answers['project'][f'deliveries_{str(i)}_periodDaysFrom']['value_'] is not None:
                date += f"Этап {str(i)}\n"
                date += f"""Начало срока поставки на сайте: {answers['project'][f'deliveries_{str(i)}_periodDaysFrom']['value_']}
                Совпадение в проекте: {answers['project'][f'deliveries_{str(i)}_periodDaysFrom']['leven_partial_ratio']}%
                """
            else:
                date += "\n"
                break

            if f'deliveries_{str(i)}_periodDateTo' in answers['project'] and answers['project'][f'deliveries_{str(i)}_periodDateTo']['value_'] is not None:
                date += f"""Дата окончания поставки на сайте: {answers['project'][f'deliveries_{str(i)}_periodDateTo']['value_']}
                Совпадение в проекте: {answers['project'][f'deliveries_{str(i)}_periodDateTo']['leven_partial_ratio']}%
                """
            elif f'deliveries_{str(i)}_periodDaysTo' in answers['project'] and answers['project'][f'deliveries_{str(i)}_periodDaysTo']['value_'] is not None:
                date += f"""Окончание срока поставки на сайте: {answers['project'][f'deliveries_{str(i)}_periodDaysTo']['value_']}
                Совпадение в проекте: {answers['project'][f'deliveries_{str(i)}_periodDaysTo']['leven_partial_ratio']}%
                """
            else:
                date += "\n"
                break


        specification_str = "ТЗ отсутствует"

        answer = f"""
        1. Название КС
        На сайте: {answers['project']['name']['value_']}
        Совпадение в проекте: {int(answers['project']['name']['leven_partial_ratio'])}%
        
        2. Обеспечение исполнения контракта
        {obespechenie_str}
        
        3. Наличие сертификатов/лицензий
        {sertificates_str}
        
        4. График поставки
        {date}
      
        5. Цена контракта
        {cost_needed_str}
     
        6. Спецификация
        {specification_str}
        """

    # answers['project']['name'] answers['technical']['name'] # Вывести имя (1)
    # answers['project']['isContractGuarateeRequired']['value'] answers['technical']['isContractGuarateeRequired']['value']# если да, то напечатать: answers['ContractGuaranteeAmount'] (2)
    # answers['project']['startCost']['value'] # если есть, то вывести (5)
    # answers['technical']["items_0_name"] # имя спецификации (6)
    # answers['technical']["items_0_currentValue"]  # количество в спецификации (6)

    # for k, v in answers.items():
    #     bot.send_message(message.chat.id, f"{k}: {v}")

    bot.send_message(message.chat.id, answer)
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

@bot.message_handler(func=lambda message: message.text == "Подтвердить корректность КС")
def confirm_correctness(message):
    bot.send_message(message.chat.id, "КС подтверждена!", reply_markup=types.ReplyKeyboardRemove())

# Обработка текста с причиной
@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == 'waiting_for_reason')
def handle_reason(message):
    reason = message.text
    bot.send_message(message.chat.id, f"Снято с публикации по причине: {reason}")
    user_state[message.chat.id] = None

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
