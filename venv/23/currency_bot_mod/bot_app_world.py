import telebot
import time
from telebot import types
from tokens import TELE_TOKEN
from extensions_world import CryptoConverter, APIException, currencie
import bot_app_by



# from background import keep_alive  #постоянный онлайн

bot = telebot.TeleBot(TELE_TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('/Мировые_курсы_валют')
    btn2 = types.KeyboardButton('/Курсы_валют_Беларусь')
    markup.add(btn1, btn2)
    text = 'Привет! Я Бот-Конвертер валют и я могу:  \n\n' \
           '- Показать список доступных валют и их кодов через команду: /values' \
           '\n\n-- Вывести конвертацию валюты через команду:\n' \
           '<Код валюты для перевода>  ' \
           '<Код валюты в кототую нужно перевести>  ' \
           '<Количество переводимой валюты>' \
           '\n\nПример ввода: USD RUB 10' \
           '\n\n' \
           'Напомнить, что я могу через команду: /help'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=['Мировые_курсы_валют'])
def start(message):
    bot.send_message(message.chat.id,
                     text="Отправляемся путешествовать по миру!".format(
                         message.from_user))


@bot.message_handler(commands=['Курсы_валют_Беларусь'])
def start(message):
    bot.send_message(message.chat.id,
                     text="Мы в беларуси!".format(
                         message.from_user))


@bot.message_handler(commands=['help'])
def helpp(message: telebot.types.Message):
    text = 'Чтобы начать конвертацию, введите команду в следующем формате: \n' \
           '<Код валюты для перевода>  <Код валюты в кототую нужно перевести> <Количество переводимой валюты>' \
           '\n\nПример ввода: USD RUB 10 \n\nЧтобы увидеть список всех доступных валют и их кодов введите команду:\n/values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in dict(sorted(currencie.items())):
        text = '\n'.join((text, f'{key} - {currencie[key]}'))
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=[])
def help(message: telebot.types.Message):
    raise APIException('Я не знаю такой команды')


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException('Слишком много параметров :( '
                               '\n\nПопробуй ешё раз\nПример ввода: USD RUB 10')

        elif len(values) < 3:
            raise APIException('Слишком мало параметров :( '
                               '\n\nПопробуй ешё раз\nПример ввода: USD RUB 10')

        quote, base, amount = values[0].upper(), values[1].upper(), values[2]
        total_base = CryptoConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ты ошибся с вводом\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')

    else:
        text = f'{amount} {quote} = {total_base} {base}\n' \
               f'Согласно сайту www.cryptocompare.com на {time.strftime("%d %b %Y %H:%M:%S")}'
        bot.send_message(message.chat.id, text)


# keep_alive() #постоянный онлайн
if __name__ == '__main__':
    bot.polling()
