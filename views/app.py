from telegram import Bot, Update


def app_main_menu(bot: Bot, update: Update, user_data: dict):
    print(user_data)
