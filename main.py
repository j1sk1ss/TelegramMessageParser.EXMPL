from telethon.sync import TelegramClient
import datetime
import telebot
from telebot import types
import asyncio

bot = telebot.TeleBot('')
api_id = 0
api_hash = 'str'

now = datetime.datetime.now()
chats = []
words = []
hours = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Вот твоё меню!\n', parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    parse = types.KeyboardButton('Получить сообщения')
    app = types.KeyboardButton('Установить APP_ID')
    key = types.KeyboardButton('Установить HASH_KEY')
    add_words = types.KeyboardButton('Добавить ключевые слова')
    time = types.KeyboardButton('Установить временной промежуток')
    add_groups = types.KeyboardButton('Добавить чаты')
    markup.add(parse, app, key, add_groups, add_words, time)
    mess = f'Приветствую, <b> {message.from_user.first_name}, выберите действие: </b>'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler()
def get_message(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Получить данные!", url="my.telegram.org"))
    if message.text == 'Получить сообщения':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        Parse(message)

    if message.text == 'Установить APP_ID':
        sent = bot.send_message(message.chat.id, 'Укажите ID: \n(Пример: 12345678)', reply_markup=markup)
        bot.register_next_step_handler(sent, set_app)

    if message.text == 'Установить HASH_KEY':
        sent = bot.send_message(message.chat.id, 'Укажите HASH_KEY: \n(Пример '
                                                 '1234567890:XXXXXXXX0xXXXXXXxXXXX0XXxxXxXXx0xXX)',  reply_markup=markup)
        bot.register_next_step_handler(sent, set_key)

    if message.text == 'Добавить чаты':
        sent = bot.send_message(message.chat.id, 'Укажите название чата: ')
        bot.register_next_step_handler(sent, add_chat)

    if message.text == 'Добавить ключевые слова':
        sent = bot.send_message(message.chat.id, 'Укажите слово: ')
        bot.register_next_step_handler(sent, add_word)

    if message.text == 'Установить временной промежуток':
        sent = bot.send_message(message.chat.id, 'Укажите количество часов: ')
        bot.register_next_step_handler(sent, set_time)


def set_time(msg):
    global hours
    try:
        hours = int(msg.text)
        bot.send_message(msg.chat.id, 'Время установлено!\n', parse_mode='html')
    except ValueError:
        bot.send_message(msg.chat.id, 'Произошла ошибка!\n', parse_mode='html')


def add_word(msg):
    if msg.text != 'stop':
        words.append(msg.text)
        sent = bot.send_message(msg.chat.id, 'Укажите слово: ')
        bot.register_next_step_handler(sent, add_word)
    else:
        bot.send_message(msg.chat.id, 'Ключевые слова записаны!\n', parse_mode='html')


def add_chat(msg):
    if msg.text != 'stop':
        chats.append(msg.text)
        sent = bot.send_message(msg.chat.id, 'Укажите название чата: ')
        bot.register_next_step_handler(sent, add_chat)
    else:
        bot.send_message(msg.chat.id, 'Чаты записаны!\n', parse_mode='html')


def set_key(msg):
    global api_hash
    try:
        api_hash = msg.text
        bot.send_message(msg.chat.id, 'HASH_KEY установлен!\n', parse_mode='html')
    except ValueError:
        bot.send_message(msg.chat.id, 'Произошла ошибка!\n', parse_mode='html')


def set_app(msg):
    global api_id
    try:
        api_id = int(msg.text)
        bot.send_message(msg.chat.id, 'APP_ID установлен!\n', parse_mode='html')
    except ValueError:
        bot.send_message(msg.chat.id, 'Произошла ошибка!\n', parse_mode='html')


def checkDate(date):
    if date.day == now.day and date.hour - now.hour < hours and date.month == now.month:
        return True
    else:
        return False


def Parse(chat):
    try:
        with TelegramClient('client', api_id, api_hash) as client:
            for dialog in client.iter_dialogs():
                if dialog.title in chats:
                    for trigger in words:
                        for msg in client.iter_messages(dialog.id, search=str(trigger)):
                            if msg.text is not None and checkDate(msg.date):
                                client.forward_messages(chat.id, msg.id, dialog.id)
    except ValueError:
        bot.send_message(chat.chat.id, 'Произошла ошибка!\n', parse_mode='html')


bot.polling(none_stop=True)
