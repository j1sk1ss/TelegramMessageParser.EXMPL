from telethon.sync import TelegramClient
import datetime
import telebot
from telebot import types
import asyncio

bot = telebot.TeleBot('')
api_id = 0
api_hash = ''

now = datetime.datetime.now()
chats = []
words = []
hours = 1


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Вот твоё меню!\n', parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    parse = types.KeyboardButton('Получить сообщения')
    markup.add(parse)
    mess = f'Приветствую, <b> {message.from_user.first_name}, выберите действие: </b>'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler()
def get_message(message):
    if message.text == 'Получить сообщения':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        Parse()
    if message.text[0] == '.':
        chats.append(message.text[1:])
        bot.send_message(message.chat.id, chats[-1])
    if message.text[0] == ',':
        words.append(message.text[1:])
        bot.send_message(message.chat.id, words[-1])
    if message.text[0] == ';':
        try:
            hours = int(message.text[1:])
        except:
            hours = 1


def checkDate(date):
    if date.day == now.day and date.hour - now.hour < hours and date.month == now.month:
        return True
    else:
        return False


def Parse():
    temp = ''
    with TelegramClient('client', api_id, api_hash) as client:
        for dialog in client.iter_dialogs():
            if dialog.title in chats:
                for trigger in words:
                    for msg in client.iter_messages(dialog.id, search=str(trigger)):
                        if msg.text is not None and checkDate(msg.date):
                            client.forward_messages(5511006797, msg.id, dialog.id)


bot.polling(none_stop=True)
