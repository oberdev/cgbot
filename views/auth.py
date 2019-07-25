from telegram.ext import Updater, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import Bot
from api import CGApiClient
from views_codes import AUTH_USERNAME, AUTH_PASSWORD, AUTH_VALIDATION, APP_MENU_CASES
from utils import app_user_view

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, Update

button_list = [
    [
        InlineKeyboardButton("authenticate", callback_data="authenticate")
    ]
]

markup = InlineKeyboardMarkup(button_list)


def auth_invite(bot: Bot, update: Update):
    bot.send_message(
        reply_to_message_id=update.message.message_id,
        chat_id=update.message.chat_id,
        text="I'm a bot, please talk to me!",
        reply_markup=markup
    )


def auth_username(bot: Bot, update: Updater, user_data: dict):
    user_data.clear()
    query = update.callback_query if update.callback_query else update
    bot.send_message(
        chat_id=query.message.chat_id,
        text="Enter username"
    )
    return AUTH_PASSWORD


def auth_password(bot: Bot, update: Updater, user_data: dict):
    user_data['username'] = update.message.text
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Enter password"
    )
    return AUTH_VALIDATION


def auth_validation(bot: Bot, update: Updater, user_data: dict):
    user_data['password'] = update.message.text
    user_data['api'] = CGApiClient()
    auth_result = user_data['api'].token_obtain(
        user_data['username'], user_data['password'])
    print(auth_result)
    if 'error' in auth_result:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=auth_result['error']
        )
        user_data.clear()
        auth_username(bot, update, user_data)
        return AUTH_PASSWORD
    else:
        del user_data['username']
        del user_data['password']
        app_user_view(bot, update)
        return APP_MENU_CASES
