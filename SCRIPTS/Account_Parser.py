import datetime
import os
import pickle

from telethon import events
from telethon.sync import TelegramClient

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

this_day = datetime.datetime.now()

client = TelegramClient('client', app_id, hash_key)
client.start()


@client.on(events.NewMessage())
async def main(event):
    try:
        print(event.message.id, event.chat.title, event.message.text)
        if event.chat.title in chats:
            for word in words:
                if word in event.message.text:
                    await client.forward_messages(5511006797, event.message.id, event.chat.id)
                break
    except ValueError:
        print('ERROR is CORRUPTED!')
with client:
    client.run_until_disconnected()
