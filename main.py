from utilities import Converter, ConvertException
import telebot
from config import keys, token_

bot = telebot.TeleBot(token_)


@bot.message_handler(commands=['start', 'help'])
def help_command(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Введите /currency или /cur чтобы вывести список доступных валют.\n '
                                      '\nЧтобы узнать стоимость валюты, введите:\n'
                                      '<конвертируемая валюта> <валюта, в которую конвертировать> <сумма>, '
                                      '\nнапример "рубль доллар 1000" или "btc usd 1".')


@bot.message_handler(commands=['currency', 'cur'])
def help_command(message: telebot.types.Message):
    text = "Валюты, доступные по имени:"
    for key in keys:
        text += f'\n    {key}'
    text += '\nТакже 150 других валют доступно по ISO коду (например "btc usd 100").\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise ConvertException('Неверный формат.')
        quote, base, amount = values
        value = Converter.convert(quote, base, amount)

    except ConvertException as e:
        bot.send_message(message.chat.id, f'{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать запрос\n{e}')
    else:
        text = f'Цена {amount} {quote.lower()} в {base.lower()}: {value}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
