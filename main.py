from telethon.sync import TelegramClient
import datetime

api_id = 29874597
api_hash = '1f021960a9e8cfcd59cc94ccc11aab7e'

chats = ['Пивнуха 1.5 литра']

with TelegramClient('client', api_id, api_hash) as client:
    for dialog in client.iter_dialogs():
        if dialog.title in chats:
            for msg in client.iter_messages(dialog.id):
                if msg.text is not None:
                    if '!' in msg.text and msg.date.day == 9 and msg.date.hour - 18 < 1:
                        print(msg.text + " - " + dialog.title + " (" + str(msg.date.day) + ")")
