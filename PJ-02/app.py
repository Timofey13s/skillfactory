import telebot
from extensions import APIException, Converter
from config import name_cur, TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> <в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for cur in name_cur:
        text = '\n'.join([text, cur])
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        val = message.text.lower().split(' ')
        if len(val) != 3:
            raise APIException('Число параметров должно быть равно трем.')
        base, quote, amount = val
        total = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, str(e))
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {name_cur[base]} равна {total} {name_cur[quote]}'
        bot.send_message(message.chat.id, text)

bot.polling()