import telebot
from extensions import Conversion, APIException, ValueException
from config import TOKEN, value_keys

value_bot = telebot.TeleBot(TOKEN)


@value_bot.message_handler(commands=['start'])
def start_message_handler(message: telebot.types.Message):
    help_text = f'Здравствуйте, {message.chat.username}! '\
    'Я - бот, который может конвертировать значение одной валюты в другую.\n\n'\
    'Чтобы начать введите команду в формате:\n' \
    '<имя валюты> <имя валюты, в которую нужно перевести> <количество конвертируемой валюты>\n\n'\
    'Для просмотра доступного списка валют введите команду /values'

    value_bot.reply_to(message, help_text)


@value_bot.message_handler(commands=['help'])
def help_message_handler(message: telebot.types.Message):
    help_text = 'Чтобы начать введите команду в формате:\n' \
    '<имя валюты> <имя валюты, в которую нужно перевести> <количество конвертируемой валюты>\n\n' \
    'Для просмотра доступного списка валют введите команду /values'

    value_bot.reply_to(message, help_text)


@value_bot.message_handler(content_types=['audio'])
def audio_message_handler(message):
    value_bot.reply_to(message, 'Good music !')


@value_bot.message_handler(content_types=['photo'])
def photo_message_handler(message):
    value_bot.reply_to(message, 'Nice meme XDD')


@value_bot.message_handler(commands=['values'])
def value_list_message_handler(message: telebot.types.Message):

    help_text = 'Доступные валюты:\n'
    for key, value in value_keys.items():
        str_value = f'{key} ({value})'
        help_text = '\n'.join((help_text, str_value, ))

    value_bot.reply_to(message, help_text)


@value_bot.message_handler(content_types=['text'])
def convert_value(message: telebot.types.Message):

    try:
        params_list = message.text.split(' ')

        if len(params_list) != 3:
            raise APIException('Неверный формат ввода.\n'
                               'Посмотреть формат ввода можно по команде /help')

        base, quote, amount = params_list
        base_t, quote_t = base.title(), quote.title()
        total_value = Conversion.get_price(base_t, quote_t, amount)

    except APIException as e:
        value_bot.reply_to(message, f'Ошибка пользователя. \n{e}')

    except ValueException as e:
        value_bot.reply_to(message, f'Ошибка сервиса. \n{e}')

    except Exception as e:
        value_bot.reply_to(message, f'Не удалось обработать команду \n{e}')

    else:
        text = f'Стоимость {amount} {base_t} в {quote_t} - {total_value}'
        value_bot.send_message(message.chat.id, text)


value_bot.polling()
