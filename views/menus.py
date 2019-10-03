from telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup
from utils import app_empty_view, main_menu_buttons, app_user_view, mock_view, chunks
from constants import APP_MENU_CASES, BUTTON_IN_ROW, APP_ROOMS_CASES, APP_BUILDING_CASES, APP_BUILDINGS_CASES, \
    APP_BOXES_CASES
import datetime

from views.box import app_box_first_date, app_box_second_date, app_plotting_view, app_box_recently_params, app_box_view, \
    box_actions_list


def app_buildings_view(bot: Bot, updater: Update, user_data: dict):
    buildings_keyboard = list(chunks([KeyboardButton(
        text=building['address']) for building in user_data['hierarchy']['buildings']], BUTTON_IN_ROW))
    buildings_keyboard.append([KeyboardButton(text='Back')])
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="Choose building",
        reply_markup=ReplyKeyboardMarkup(buildings_keyboard)
    )
    return APP_BUILDINGS_CASES


def app_building_view(bot: Bot, updater: Update, user_data: dict):
    buttons = []
    active_building = user_data['active_building']
    if 'boxes' in active_building:
        buttons.append('boxes')
    if 'rooms' in active_building:
        buttons.append('rooms')
    if len(buttons) == 2:
        bot.send_message(
            chat_id=updater.message.chat_id,
            text="Choose subject",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton(text=button) for button in buttons], [KeyboardButton(text='Back')]])
        )
        return APP_BUILDING_CASES
    elif len(buttons) == 1:
        user_data['from'] = 'buildings_menu'
        if buttons[0] == 'boxes':
            return app_boxes_view(bot, updater, user_data)
        if buttons[1] == 'rooms':
            return app_rooms_view(bot, updater, user_data)


def app_rooms_view(bot: Bot, updater: Update, user_data: dict):
    rooms_keyboard = list(chunks([KeyboardButton(
        text=room['name']) for room in user_data['active_building']['rooms']], BUTTON_IN_ROW))
    rooms_keyboard.append([KeyboardButton(text='Back')])
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="Choose room",
        reply_markup=ReplyKeyboardMarkup(rooms_keyboard)
    )
    return APP_ROOMS_CASES


def app_main_menu(bot: Bot, update: Update, user_data: dict):
    if update.message.text == main_menu_buttons[0]:
        user_data['hierarchy'] = user_data['api'].get_hierarchy()
        if 'buildings' not in user_data['hierarchy']:
            app_empty_view(bot, update)
            return
        elif 'code' in user_data['hierarchy'] and user_data['hierarchy']['code'] == 401:
            bot.send_message(text=user_data['hierarchy']['msg'])
        else:
            return app_buildings_view(bot, update, user_data)
    if update.message.text == main_menu_buttons[1]:
        mock_view(bot, update, user_data)


def app_buildings_menu(bot: Bot, update: Update, user_data: dict):
    if update.message.text == "Back":
        app_user_view(bot, update)
        return APP_MENU_CASES
    else:
        buildings = list(filter(
            lambda building: building['address'] == update.message.text, user_data['hierarchy']['buildings']))
        if buildings:
            user_data['active_building'] = buildings[0]
            return app_building_view(bot, update, user_data)


def app_building_menu(bot: Bot, update: Update, user_data: dict):
    if update.message.text == "Back":
        return app_buildings_view(bot, update, user_data)
    else:
        if update.message.text in user_data["active_building"]:
            if update.message.text == 'rooms':
                user_data['from'] = 'rooms'
                return app_rooms_view(bot, update, user_data)
            if update.message.text == 'boxes':
                user_data['from'] = 'buildings'
                return app_boxes_view(bot, update, user_data)


def app_boxes_menu(bot: Bot, update: Update, user_data: dict):
    if update.message.text == "Back":
        if user_data['from'] == 'buildings':
            return app_building_view(bot, update, user_data)
        elif user_data['from'] == 'rooms':
            return app_rooms_view(bot, update, user_data)
        elif user_data['from'] == 'buildings_menu':
            return app_buildings_view(bot, update, user_data)
    elif update.message.text in user_data['boxes']:
        user_data['active_box'] = update.message.text
        return app_box_view(bot, update, user_data)


def app_rooms_menu(bot: Bot, update: Update, user_data: dict):
    if update.message.text == "Back":
        return app_building_view(bot, update, user_data)
    else:
        rooms = list(filter(
            lambda room: room['name'] == update.message.text, user_data['active_building']['rooms']))
        if rooms:
            user_data['active_room'] = rooms[0]
            return app_boxes_view(bot, update, user_data, 'active_room')


def app_box_actions(bot: Bot, update: Update, user_data: dict):
    if update.message.text == "Back":
        return app_boxes_view(bot, update, user_data)
    elif update.message.text == box_actions_list[0]:
        app_box_recently_params(bot, update, user_data)
    elif update.message.text == box_actions_list[1]:
        return app_box_first_date(bot, update, user_data)


def app_box_first_date_handler(bot: Bot, update: Update, user_data: dict):
    if update.message.text == 'Cancel':
        return app_box_view(bot, update, user_data)
    else:
        try:
            user_data['start_date'] = datetime.datetime.strptime(
                update.message.text, "%d/%m/%y")
        except ValueError:
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Invalid Date, try another or cancel'
            )
        else:
            return app_box_second_date(bot, update, user_data)


def app_box_second_date_handler(bot: Bot, update: Update, user_data: dict):
    if update.message.text == 'Cancel':
        return app_box_view(bot, update, user_data)
    else:
        try:
            user_data['end_date'] = datetime.datetime.strptime(
                update.message.text, "%d/%m/%y")
        except ValueError:
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Invalid Date, try another or cancel'
            )
        else:
            return app_plotting_view(bot, update, user_data)


def app_boxes_view(bot: Bot, update: Update, user_data: dict, key='active_building'):
    user_data['boxes'] = [box['uuid'] for box in user_data[key]['boxes']]
    boxes_keyboard = list(chunks([KeyboardButton(text=box)
                                  for box in user_data['boxes']], BUTTON_IN_ROW))
    boxes_keyboard.append([KeyboardButton(text='Back')])
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Choose box",
        reply_markup=ReplyKeyboardMarkup(boxes_keyboard)
    )
    return APP_BOXES_CASES
