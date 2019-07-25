from telegram import Bot, Update
from utils import app_empty_view, main_menu_buttons, app_buildings_view, app_user_view, app_building_view, app_rooms_view, app_boxes_view, app_box_view, app_boxes_view, mock_view, box_actions_list, app_box_recently_params
from views_codes import APP_MENU_CASES, APP_BUILDINGS_CASES


def app_main_menu(bot: Bot, update: Update, user_data: dict):
    if update.message.text == main_menu_buttons[0]:
        user_data['hierarchy'] = user_data['api'].get_hierarchy()
        if not user_data['hierarchy']['buildings']:
            app_empty_view(bot, update)
            return
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
            del user_data['from']
            return app_building_view(bot, update, user_data)
        elif user_data['from'] == 'rooms':
            del user_data['from']
            return app_rooms_view(bot, update, user_data)
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
        return mock_view(bot, update, user_data)
