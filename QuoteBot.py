#!/usr/bin/python3
import random
from tinydb import TinyDB, Query
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

db = TinyDB('db.json')
quotes = db.all()

updater = Updater(token='API_TOKEN_HERE')
dispatcher = updater.dispatcher


def get_random_quote():
    return random.choice(quotes)['text']

def add_quote(bot, update, args):
    quote = " ".join(args)
    print("ADDING QUOTE " + quote)
    db.insert({'text': quote})
    quotes = db.all()

def quote_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=get_random_quote())

def handle_quote(bot, update):
    if ("#quote" in update.message.text):
        bot.send_message(chat_id=update.message.chat_id, text=get_random_quote())

quote_command_handler = CommandHandler('Quote', quote_command)
dispatcher.add_handler(quote_command_handler)

add_command_handler = CommandHandler('AddQuote', add_quote, pass_args=True)
dispatcher.add_handler(add_command_handler)

quote_text_handler = MessageHandler(Filters.text, handle_quote)
dispatcher.add_handler(quote_text_handler)

updater.start_polling()
updater.idle()
