from telegram.ext import Updater, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters, CommandHandler, InlineQueryHandler, Handler, RegexHandler
from views.auth import *
from views.app import *
from views_codes import *


app_conv_handler = ConversationHandler(
    allow_reentry=True,
    entry_points=[CallbackQueryHandler(
        auth_username, pattern="authenticate", pass_user_data=True)],
    states={
        AUTH_PASSWORD: [MessageHandler(Filters.text, auth_password, pass_user_data=True)],
        AUTH_VALIDATION: [MessageHandler(Filters.text, auth_validation, pass_user_data=True)],
        APP_MENU_CASES: [RegexHandler(
            '^(Buildings|Settings)$', app_main_menu, pass_user_data=True)]
    },
    fallbacks=[],
)

start_handler = CommandHandler('start', auth_invite)
