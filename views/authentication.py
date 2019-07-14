from telegram.ext import Updater, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import Bot

ENTERING_PASSWORD, VALIDATION = range(2)


def enter_username(bot: Bot, update: Updater):
    query = update.callback_query
    bot.send_message(
        chat_id=query.message.chat_id,
        text="Enter username"
    )
    return ENTERING_PASSWORD


def enter_password(bot: Bot, update: Updater, user_data: dict):
    user_data['username'] = update.message.text
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Enter password"
    )
    return VALIDATION


def validation(bot: Bot, update: Updater, user_data: dict):
    user_data['password'] = update.message.text
    print(user_data)
    return


auth_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        enter_username, pattern='authenticate')],
    states={
        ENTERING_PASSWORD: [
            MessageHandler(Filters.text, enter_password, pass_user_data=True),
        ],
        VALIDATION: [
            MessageHandler(Filters.text, validation, pass_user_data=True)
        ]
    },
    fallbacks=[]
)
