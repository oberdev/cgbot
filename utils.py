from telegram.ext import Updater
from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup
from views_codes import APP_BUILDINGS_CASES, APP_BUILDING_CASES, APP_BOXES_CASES, APP_ROOMS_CASES, APP_BOX_ACTIONS

main_menu_buttons = ["Buildings", "Settings"]

button_list = [
    [KeyboardButton(text=button_text) for button_text in main_menu_buttons]
]

markup = ReplyKeyboardMarkup(button_list)

box_actions_list = ['Recently indicators', 'Plot']


def app_user_view(bot: Bot, updater: Updater):
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="Main menu",
        reply_markup=markup
    )


def app_empty_view(bot: Bot, updater: Updater):
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="There are no content to show",
        # reply_markup=markup
    )


def app_buildings_view(bot: Bot, updater: Updater, user_data: dict):
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="Choose building",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton(text=building['address']) for building in user_data['hierarchy']['buildings']], [KeyboardButton(text='Back')]])
    )
    return APP_BUILDINGS_CASES


def app_building_view(bot: Bot, updater: Updater, user_data: dict):
    buttons = []
    active_building = user_data['active_building']
    if 'boxes' in active_building:
        buttons.append('boxes')
    if 'rooms' in active_building:
        buttons.append('rooms')
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="Choose subject",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton(text=button) for button in buttons], [KeyboardButton(text='Back')]])
    )
    return APP_BUILDING_CASES


def app_rooms_view(bot: Bot, updater: Updater, user_data: dict):
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="Choose room",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton(text=room['name']) for room in user_data['active_building']['rooms']], [KeyboardButton(text='Back')]])
    )
    return APP_ROOMS_CASES


def app_boxes_view(bot: Bot, updater: Updater, user_data: dict, key='active_building'):
    user_data['boxes'] = [box['uuid'] for box in user_data[key]['boxes']]
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="Choose box",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton(text=box) for box in user_data['boxes']], [KeyboardButton(text='Back')]])
    )
    return APP_BOXES_CASES


def app_box_view(bot: Bot, updater: Updater, user_data: dict):
    bot.send_message(
        chat_id=updater.message.chat_id,
        text=f"The box_id is {user_data['active_box']}",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton(text=action) for action in box_actions_list], [KeyboardButton(text='Back')]])
    )
    return APP_BOX_ACTIONS


def mock_view(bot: Bot, updater: Updater, user_data: dict):
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="In developing",
    )


def app_box_recently_params(bot: Bot, update: Updater, user_data: dict):
    params = user_data['api'].get_recently_params(user_data['active_box'])
    bot.send_message(
        chat_id=update.message.chat_id,
        text='\n'.join(
            [f'{key}: {value}' for key, value in params.items()]),
    )
