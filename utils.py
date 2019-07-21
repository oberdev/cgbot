from telegram.ext import Updater
from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup

button_list = [
    [
        KeyboardButton(text="Buildings"),
        KeyboardButton(text="Settings")
    ]
]

markup = ReplyKeyboardMarkup(button_list)


def app_user_view(bot: Bot, updater: Updater, user_data: dict):
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="Main menu",
        reply_markup=markup
    )
