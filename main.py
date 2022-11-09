from telethon.sync import TelegramClient
import datetime
import telebot
from telebot import types
import asyncio

print('Type bot token: ')
bot = telebot.TeleBot(input())  # creates bot

app_id = 0  # creates app_id variable
hash_key = ''  # creates hash_key variable

this_day = datetime.datetime.now()  # gets today's date
chats = []
words = []
hours = 0


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    parse = types.KeyboardButton('Получить сообщения')  # creates six buttons for work with bot
    app = types.KeyboardButton('Установить APP_ID')
    key = types.KeyboardButton('Установить HASH_KEY')
    add_words = types.KeyboardButton('Добавить ключевые слова')
    time = types.KeyboardButton('Установить временной промежуток')
    add_groups = types.KeyboardButton('Добавить чаты')
    markup.add(parse, app, key, add_groups, add_words, time)

    mess = 'Ваши <b>кнопки</b> выведены ниже.'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler()
def get_message(message):
    markup = types.InlineKeyboardMarkup()  # save to cash button with link to website
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


def add_word(msg):
    add_to_list(msg, words, 'Слово', add_word)


def add_chat(msg):
    add_to_list(msg, chats, 'Чат', add_chat)


def add_to_list(msg, lst, cls, func):
    if msg.text != 'stop':
        if msg.text not in lst:
            lst.append(msg.text)
        else:
            bot.send_message(msg.chat.id, f"{cls} уже записан!")
        sent = bot.send_message(msg.chat.id, f"Укажите {cls}:")
        bot.register_next_step_handler(sent, func)
    else:
        bot.send_message(msg.chat.id, f'{cls} записан!\n', parse_mode='html')


def set_key(msg):
    global hash_key
    hash_key = get_value(msg, 'HASH_KEY')


def set_app(msg):
    global app_id
    app_id = get_value(msg, 'APP_ID')


def set_time(msg):
    global hours
    hours = int(get_value(msg, 'Время'))


def get_value(msg, cls):
    try:
        bot.send_message(msg.chat.id, f'{cls} установлен!\n', parse_mode='html')
        return msg.text
    except ValueError:
        bot.send_message(msg.chat.id, 'Произошла ошибка!\n', parse_mode='html')


def checkDate(date):
    if date.day == this_day.day and date.hour - this_day.hour < hours and date.month == this_day.month:
        return True
    else:
        return False


def Parse(chat):
    try:
        with TelegramClient('client', app_id, hash_key) as client:
            for dialog in client.iter_dialogs():
                if dialog.title in chats:
                    for trigger in words:
                        for msg in client.iter_messages(dialog.id, search=str(trigger)):
                            if msg.text is not None and checkDate(msg.date):
                                client.forward_messages(chat.id, msg.id, dialog.id)
    except ValueError:
        bot.send_message(chat.chat.id, 'Произошла ошибка!\n', parse_mode='html')


bot.polling(none_stop=True)
