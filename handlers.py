from telegram.ext import Updater, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters, CommandHandler, InlineQueryHandler, Handler, RegexHandler
from views.auth import *
from views_codes import *
from views.app import app_main_menu, app_building_menu, app_buildings_menu, app_boxes_menu, app_rooms_menu, app_box_actions, app_box_first_date, app_box_first_date_handler, app_box_second_date_handler


app_conv_handler = ConversationHandler(
    allow_reentry=True,
    entry_points=[CallbackQueryHandler(
        auth_username, pattern="authenticate", pass_user_data=True)],
    states={
        AUTH_PASSWORD: [MessageHandler(Filters.text, auth_password, pass_user_data=True)],
        AUTH_VALIDATION: [MessageHandler(Filters.text, auth_validation, pass_user_data=True)],
        APP_MENU_CASES: [RegexHandler(
            '^(Buildings|Settings)$', app_main_menu, pass_user_data=True)],
        APP_BUILDINGS_CASES: [MessageHandler(
            Filters.text, app_buildings_menu, pass_user_data=True)],
        APP_BUILDING_CASES: [MessageHandler(
            Filters.text, app_building_menu, pass_user_data=True)],
        APP_BOXES_CASES: [MessageHandler(
            Filters.text, app_boxes_menu, pass_user_data=True)],
        APP_ROOMS_CASES: [MessageHandler(
            Filters.text, app_rooms_menu, pass_user_data=True)],
        APP_BOX_ACTIONS: [MessageHandler(
            Filters.text, app_box_actions, pass_user_data=True)],
        APP_BOX_FIRST_DATE_HANDLE: [MessageHandler(
            Filters.text, app_box_first_date_handler, pass_user_data=True)],
        APP_BOX_SECOND_DATE_HANDLE: [MessageHandler(
            Filters.text, app_box_second_date_handler, pass_user_data=True)],
    },
    fallbacks=[],
)

start_handler = CommandHandler('start', auth_invite)
