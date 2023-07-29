import telebot
import time
from telebot import types
from tokens import TELE_TOKEN
from extensions_by import CryptoConverter, APIException, currencie
import bot_app_by, bot_app_world

# from background import keep_alive  #постоянный онлайн

bot = telebot.TeleBot(TELE_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('/Мировые_курсы_валют')
    btn2 = types.KeyboardButton('/Курсы_валют_Беларусь')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я тестовый бот для твоей статьи для habr.com".format(
                         message.from_user), reply_markup=markup)


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
    # bot_app_by.bot.polling()


# keep_alive() #постоянный онлайн
if __name__ == '__main__':
    bot.polling()
    bot.stop_bot()
    bot_app_by.bot.polling()

