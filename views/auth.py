from telegram.ext import ConversationHandler
from api import CGApiClient
from constants import AUTH_PASSWORD, AUTH_VALIDATION, APP_MENU_CASES
from utils import app_user_view
from telegram import Bot, Update


def auth_invite(bot: Bot, update: Update, user_data: dict):
    user_data = {}
    bot.send_message(
        reply_to_message_id=update.message.message_id,
        chat_id=update.message.chat_id,
        text="I'm a bot, please talk to me!",
    )
    return auth_user(bot, update, user_data)


def auth_user(bot: Bot, update: Update, user_data: dict):
    user_data.clear()
    query = update.callback_query if update.callback_query else update
    bot.send_message(
        chat_id=query.message.chat_id,
        text="Enter username"
    )
    return AUTH_PASSWORD


def auth_password(bot: Bot, update: Update, user_data: dict):
    user_data['username'] = update.message.text
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Enter password"
    )
    return AUTH_VALIDATION


def auth_validation(bot: Bot, update: Update, user_data: dict):
    user_data['password'] = update.message.text
    user_data['api'] = CGApiClient()
    auth_result = user_data['api'].token_obtain(
        user_data['username'], user_data['password'])
    if 'message' in auth_result:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=auth_result['message']
        )
        user_data.clear()
        return auth_user(bot, update, user_data)
    else:
        del user_data['username']
        del user_data['password']
        app_user_view(bot, update)
        return APP_MENU_CASES


def logout(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Successful logout. If you want login again send /start command'
    )
    return ConversationHandler.END
