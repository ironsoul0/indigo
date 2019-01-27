#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import ForceReply
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)


PASSWORD_CHOICE, LOGIN_CHOICE = range(2)

def password_choice(bot, update):
    text = update.message.text
    update.message.reply_text(
        'Your password is {}'.format(text))
    return ConversationHandler.END


def set_password(bot, update):
    update.message.reply_text(
        "Alright dude! Say me your password!",
        reply_markup=ForceReply())
    return PASSWORD_CHOICE

def login_choice(bot, update):
    text = update.message.text
    update.message.reply_text(
        'Your login is {}'.format(text))
    return ConversationHandler.END


def set_login(bot, update):
    update.message.reply_text(
        "Alright dude! Say me your login!",
        reply_markup=ForceReply())
    return LOGIN_CHOICE

def done(bot, update):
    return ConversationHandler.END

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("703572266:AAEztdIDnTV6ka_3AZceqp1SjJDCDB3O2UU")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher



    set_password_handler = ConversationHandler(
        entry_points=[CommandHandler('set_password', set_password)],

        states={
            

            PASSWORD_CHOICE: [MessageHandler(Filters.text,
                                           password_choice),
                            ],


        },
        fallbacks=[]
    )

    
    set_login_handler = ConversationHandler(
        entry_points=[CommandHandler('set_login', set_login)],

        states={
            

            LOGIN_CHOICE: [MessageHandler(Filters.text,
                                           login_choice),
                            ],


        },
        fallbacks=[]
    )

    dp.add_handler(set_password_handler)
    dp.add_handler(set_login_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()