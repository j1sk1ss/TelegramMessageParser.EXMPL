import datetime
import telebot
from telebot import types

import pickle
import os

print('Type bot token: ')
bot = telebot.TeleBot(input())  # creates bot

if os.path.isfile('../filename.pickle'):
    with open('../filename.pickle', 'rb') as handle:
        b = pickle.load(handle)
        app_id = int(b['id'])
        hash_key = b['hash']
        chats = b['chats']
        words = b['words']
else:
    chats = []
    words = []

this_day = datetime.datetime.now()  # gets today's date


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    parse = types.KeyboardButton('Get messages')  # creates six buttons for work with bot
    app = types.KeyboardButton('Select APP_ID')
    key = types.KeyboardButton('Select HASH_KEY')
    add_words = types.KeyboardButton('Add tags')
    add_groups = types.KeyboardButton('Add chats')
    stop = types.KeyboardButton('Stop')
    markup.add(parse, app, key, add_groups, add_words, stop)

    mess = '<b>BUTTONS</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler()
def get_message(message):
    markup = types.InlineKeyboardMarkup()  # save to cash button with link to website
    markup.add(types.InlineKeyboardButton("Get data!", url="my.telegram.org"))

    if message.text == 'SET':
        input_dictionary = {'id': str(app_id), 'hash': str(hash_key), 'chats': chats, 'words': words}
        with open('../filename.pickle', 'wb') as HANDLE:
            pickle.dump(input_dictionary, HANDLE, protocol=pickle.HIGHEST_PROTOCOL)

    if message.text == 'GET':
        bot.send_message(message.chat.id, f"{chats} chats\n{words} words\n{app_id} app_id\n{hash_key} hash_key")

    if message.text == 'Get messages':
        os.system('python SCRIPTS\\Account_Parser.py')

    if message.text == 'Select APP_ID':
        sent = bot.send_message(message.chat.id, 'Set ID: \n(Example: 12345678)', reply_markup=markup)
        bot.register_next_step_handler(sent, set_app)

    if message.text == 'Select HASH_KEY':
        sent = bot.send_message(message.chat.id, 'Select HASH_KEY: \n(Example '
                                                 '5f021969a9e8cfxx59cc94axa11aab7e)', reply_markup=markup)
        bot.register_next_step_handler(sent, set_key)

    if message.text == 'Add chats':
        sent = bot.send_message(message.chat.id, 'Select chat name: ')
        bot.register_next_step_handler(sent, add_chat)

    if message.text == 'Add tags':
        sent = bot.send_message(message.chat.id, 'Select word: ')
        bot.register_next_step_handler(sent, add_word)


def add_word(msg):
    add_to_list(msg, words, 'Word', add_word)


def add_chat(msg):
    add_to_list(msg, chats, 'Chat', add_chat)


def add_to_list(msg, lst, cls, func):
    if msg.text != 'Stop':
        if msg.text not in lst:
            lst.append(msg.text)
        else:
            bot.send_message(msg.chat.id, f"{cls} already wrote!")

        sent = bot.send_message(msg.chat.id, f"Select {cls}:")
        bot.register_next_step_handler(sent, func)
    else:
        bot.send_message(msg.chat.id, f'{cls} wrote!', parse_mode='html')


def set_key(msg):
    global hash_key
    hash_key = get_value(msg, 'HASH_KEY')


def set_app(msg):
    global app_id
    app_id = get_value(msg, 'APP_ID')


def get_value(msg, cls):
    try:
        bot.send_message(msg.chat.id, f'{cls} completed!', parse_mode='html')
        return msg.text
    except ValueError:
        bot.send_message(msg.chat.id, 'Error!', parse_mode='html')


bot.polling(none_stop=True)
