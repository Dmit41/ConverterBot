import telebot
from extensions import ValueException, ValueConverter
from config import keys, TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def starter(message: telebot.types.Message):
    text = '''Чтобы начать работу введите через пробел:
[валюта] [валюта в какую переводим] [количество]
Пример: доллар рубль 1
Команды:
/values - список валют
/help - помощь'''
    bot.reply_to(message, f"Добрый день, {message.chat.first_name}\n\
Это бот конвертер валют.\n{text}")


@bot.message_handler(commands=['help'])
def starter(message: telebot.types.Message):
    text = '''Введите через пробел:
[валюта] [в какую переводим] [количество]
Пример: доллар рубль 1
Команды:
/values - список валют
/help - помощь'''
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        low = message.text.lower()
        val = low.split(' ')

        if len(val) != 3:
            raise ValueException('Должно быть 3 параметра.')

        base, quote, amount = val
        total = ValueConverter.convert(base, quote, amount)
    except ValueException as e:
        bot.reply_to(message, f'Ошибка.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{amount} {base} - это {total} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling()
