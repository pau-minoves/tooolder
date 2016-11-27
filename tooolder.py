#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import re
import sched, time
import random
import sys

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def contains_stuff(message):
    if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.text):
        return True
    if message.photo or message.document:
        return True
    return False

def contains_too_old(message):
    return ( 'old' in message.text and not '?' in message.text )

def from_pancake(message):
    return message.from_user.username == 'pancake'

molt_be = [
    'molt be {}!',
    'felicitats {}',
    'te {}, un sugus',
    'que original {}',
    'cada vegada ho fas millor {}',
    'vinga {}, un altre cop!',
    'ooooleee {}',
    'carai! {}',
    '{}: impressionant.',
    'em deixes sense paraules {}',
    'increible! {}'
    'te {}, per tu: 8=====D',
    'te {}, per tu: (__*__)',
    '{}, the man!',
    'les calces al terra {}',
    'no {}, no party'
]

ja_tardes = [
    'Va {}, ja tardes',
    'Va {}, tu pots',
    'Va {}, bat el teu record',
    'Vinga {}!',
    '{}, anims!',
    'Endavant {}',
    'Som-hi {}',
    'Tu pots {}'
]

too_old = [
    'too old',
    'toooooo ooooold',
    'too... wait for it... old',
    'Més vell que cagar ajupit',
    'Va, digues-t\'ho tu mateix',
]


def start(bot, update):
    update.message.reply_text('Hi!')

def reply_too_old(message):
    message[0].reply_text(message[1])

def echo(bot, update):
    # joputa--
    stuff = contains_stuff(update.message)
    if stuff:
       update.message.reply_text(random.choice(too_old))
    if contains_too_old(update.message):
       update.message.reply_text(random.choice(molt_be).format(update.message.from_user.name))

    # joputa++
    #if from_pancake(update.message):
    #    if stuff:
    #    elif contains_too_old(update.message):
    #        update.message.reply_text(random.choice(molt_be))
    #else:
    #    if stuff:
    #        update.message.reply_text(random.choice(ja_tardes), quote=False)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(sys.argv[1])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.all, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
