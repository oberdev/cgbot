from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, Update

button_list = [
    [
        InlineKeyboardButton("authenticate", callback_data="authenticate")
    ]
]

markup = InlineKeyboardMarkup(button_list)


def welcome(bot: Bot, update: Update):
    bot.send_message(
        reply_to_message_id=update.message.message_id,
        chat_id=update.message.chat_id,
        text="I'm a bot, please talk to me!",
        reply_markup=markup
    )