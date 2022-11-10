from telethon.sync import TelegramClient
import datetime
import telebot
from telebot import types
import asyncio
import pickle
import os

print('Type bot token: ')
bot = telebot.TeleBot(input())  # creates bot

isActivated = False

if os.path.isfile('filename.pickle'):
    with open('filename.pickle', 'rb') as handle:
        b = pickle.load(handle)
        app_id = int(b['id'])
        hash_key = b['hash']
        chats = b['chats']
        words = b['words']
else:
    chats = []
    words = []

this_day = datetime.datetime.now()  # gets today's date


@bot.message_handler(commands=['старт'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    parse = types.KeyboardButton('📩Получить сообщения📩')  # creates six buttons for work with bot
    app = types.KeyboardButton('⏩Установить APP_ID⏪')
    key = types.KeyboardButton('⏩Установить HASH_KEY⏪')
    add_words = types.KeyboardButton('🔑Добавить ключевые слова🔑')
    add_groups = types.KeyboardButton('📧Добавить чаты📧')
    markup.add(parse, app, key, add_groups, add_words)

    mess = '⏬<b>КНОПКИ</b>⏬'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler()
def get_message(message):
    markup = types.InlineKeyboardMarkup()  # save to cash button with link to website
    markup.add(types.InlineKeyboardButton("Получить данные!", url="my.telegram.org"))

    if message.text == '📩Получить сообщения📩':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        Parse()

    if message.text == '⏩Установить APP_ID⏪':
        sent = bot.send_message(message.chat.id, '🆔Укажите ID: \n🆔(Пример: 12345678)🆔', reply_markup=markup)
        bot.register_next_step_handler(sent, set_app)

    if message.text == '⏩Установить HASH_KEY⏪':
        sent = bot.send_message(message.chat.id, '🔑Укажите HASH_KEY: \n🔑(Пример '
                                                 '1234567890:XXXXXXXX0xXXXXXXxXXXX0XXxxXxXXx0xXX)🔑',
                                reply_markup=markup)
        bot.register_next_step_handler(sent, set_key)

    if message.text == '📧Добавить чаты📧':
        sent = bot.send_message(message.chat.id, '📧Укажите название чата: ')
        bot.register_next_step_handler(sent, add_chat)

    if message.text == '🔑Добавить ключевые слова🔑':
        sent = bot.send_message(message.chat.id, '📩Укажите слово: ')
        bot.register_next_step_handler(sent, add_word)


def add_word(msg):
    add_to_list(msg, words, 'Слово', add_word)


def add_chat(msg):
    add_to_list(msg, chats, 'Чат', add_chat)


def add_to_list(msg, lst, cls, func):
    if msg.text != 'stop':
        if msg.text not in lst:
            lst.append(msg.text)
        else:
            bot.send_message(msg.chat.id, f"❌{cls} уже записан!❌")

        sent = bot.send_message(msg.chat.id, f"📃Укажите {cls}:")
        bot.register_next_step_handler(sent, func)
    else:
        bot.send_message(msg.chat.id, f'✅{cls} записан!✅', parse_mode='html')


def set_key(msg):
    global hash_key
    hash_key = get_value(msg, 'HASH_KEY')


def set_app(msg):
    global app_id
    app_id = get_value(msg, 'APP_ID')


def get_value(msg, cls):
    try:
        bot.send_message(msg.chat.id, f'✅{cls} установлен!✅', parse_mode='html')
        return msg.text
    except ValueError:
        bot.send_message(msg.chat.id, '❌Произошла ошибка!❌', parse_mode='html')


def Parse():
    input_dictionary = {'id': str(app_id), 'hash': str(hash_key), 'chats': chats, 'words': words}
    with open('filename.pickle', 'wb') as HANDLE:
        pickle.dump(input_dictionary, HANDLE, protocol=pickle.HIGHEST_PROTOCOL)

    try:
        with TelegramClient('client', app_id, hash_key) as client:
            for dialog in client.iter_dialogs():
                if dialog.title in chats:
                    for msg in client.iter_messages(dialog.id):
                        for word in words:
                            if word in msg.text:
                                if msg.text is not None and this_day.hour - 5 == msg.date.hour \
                                        and this_day.day == msg.date.day:
                                    client.forward_messages(5511006797, msg.id, dialog.id)
                                else:
                                    break
                        else:
                            continue
                    else:
                        continue
    except ValueError:
        bot.send_message(msg.chat.id, '❌Произошла ошибка!❌', parse_mode='html')


bot.polling(none_stop=True)
