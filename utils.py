from telegram.ext import Updater
from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup
from views_codes import APP_BUILDINGS_CASES, APP_BUILDING_CASES, APP_BOXES_CASES, APP_ROOMS_CASES, APP_BOX_ACTIONS, APP_BOX_FIRST_DATE_HANDLE, APP_BOX_SECOND_DATE_HANDLE
from libs.plot import build_plots
from datetime import datetime

main_menu_buttons = ["Buildings", "Settings"]

BUTTON_IN_ROW = 2

EMOJI = {
    'arrows': {
        'up': '⬆',
        'down': '⬇',
        'equal': '↕',
    },
    'no_info': '🚫',
    'colors': {
        'red': '❤',
        'yellow': '💛',
        'orange': '🧡',
        'green': '💚',
        'blue': '💙',
        'purple': '💜',
    }
}

RECENTLY_PARAMS_KEYS = ['temperature', 'vibration',
                        'noise_level', 'dust_concentration', 'light_level', 'light_ripple', 'co2_concentration', 'voc_concentration', 'magnetic_radiation', 'humidity', 'dust_concentration', 'dust_concentration_pm1', 'dust_concentration_pm10']

COLORS_LIST = ['purple', 'blue', 'green', 'yellow', 'red']
REVERSE_COLORS_LIST = ['green', 'yellow', 'red']

LABELS_OF_PARAMS = {
    'timestamp': 'Measuring time',
    'temperature': 'Temperature',
    'humidity': 'Humidity',
    'dust_concentration': 'Particles pm2.5',
    'dust_concentration_pm1': 'Particles pm1.0',
    'dust_concentration_pm10': 'Particles pm10',
    'voc_concentration': 'VOC',
    'co2_concentration': 'CO2',
    'magnetic_radiation': 'Magnetic radiation',
    'noise_level': 'Noise pollution',
    'light_level': 'Light brightness',
    'light_ripple': 'Light pulsation',
    'vibration': 'Vibration'
}

MEANS_OF_PARAMS = {
    'timestamp': '',
    'temperature': '°С',
    'humidity': '%',
    'dust_concentration': 'mg/m3',
    'dust_concentration_pm1': 'mg/m3',
    'dust_concentration_pm10': 'mg/m3',
    'voc_concentration': 'mg/m3',
    'co2_concentration': 'mg/m3',
    'magnetic_radiation': 'µT',
    'noise_level': 'dB',
    'light_level': 'lux',
    'light_ripple': '%',
    'vibration': 'm/c2'
}

button_list = [
    [KeyboardButton(text=button_text) for button_text in main_menu_buttons]
]

markup = ReplyKeyboardMarkup(button_list)

box_actions_list = ['Recently indicators', 'Plot']


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


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
    buildings_keyboard = list(chunks([KeyboardButton(
        text=building['address']) for building in user_data['hierarchy']['buildings']], BUTTON_IN_ROW))
    buildings_keyboard.append([KeyboardButton(text='Back')])
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="Choose building",
        reply_markup=ReplyKeyboardMarkup(buildings_keyboard)
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
    rooms_keyboard = list(chunks([KeyboardButton(
        text=room['name']) for room in user_data['active_building']['rooms']], BUTTON_IN_ROW))
    rooms_keyboard.append([KeyboardButton(text='Back')])
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="Choose room",
        reply_markup=ReplyKeyboardMarkup(rooms_keyboard)
    )
    return APP_ROOMS_CASES


def app_boxes_view(bot: Bot, updater: Updater, user_data: dict, key='active_building'):
    user_data['boxes'] = [box['uuid'] for box in user_data[key]['boxes']]
    boxes_keyboard = list(chunks([KeyboardButton(text=box)
                                  for box in user_data['boxes']], BUTTON_IN_ROW))
    boxes_keyboard.append([KeyboardButton(text='Back')])
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="Choose box",
        reply_markup=ReplyKeyboardMarkup(boxes_keyboard)
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


def _get_compare_emoji(a, b):
    if b == None:
        return EMOJI['no_info']
    elif a > b:
        return EMOJI['arrows']['up']
    elif a < b:
        return EMOJI['arrows']['down']
    else:
        return EMOJI['arrows']['equal']


def _get_level_emoji(param: float, group_node: dict or list):
    individual_scale = {}
    if type(group_node) is dict:
        values_list = [value for value in group_node.values()]
        emoji_list = [EMOJI['colors'][key]
                      for key in REVERSE_COLORS_LIST]
        individual_scale = dict(zip(values_list, emoji_list))
        temp_list = list(individual_scale.items())
        for value, _ in temp_list[::-1]:
            if value < param:
                return individual_scale[value]
        return emoji_list[0]
    elif type(group_node) is list:
        values_list = group_node
        emoji_list = [EMOJI['colors'][key] for key in COLORS_LIST]
        individual_scale = dict(zip(values_list, emoji_list))
        temp_list = list(individual_scale.items())
        for value, _ in temp_list[::-1]:
            if value > param:
                return individual_scale[value]
        return emoji_list[-1]


def build_response(recently_params: dict, previous_params: dict, group):
    if not recently_params:
        return 'There is imposible to convert recently params to message'
    else:
        message = ''
        message += f'Measurement data\n'
        message += f'{LABELS_OF_PARAMS["timestamp"]}: {datetime.fromtimestamp(recently_params["timestamp"])} {MEANS_OF_PARAMS["timestamp"]}\n'
        message += f'Climate parameters\n'
        for key in RECENTLY_PARAMS_KEYS:
            # for key in recently_params.keys():
            if key != 'timestamp':
                dynamic_sign = _get_compare_emoji(
                    recently_params[key], previous_params[key] if previous_params is not None else None)
                level_sign = _get_level_emoji(recently_params[key], group[key] if key not in [
                                              'dust_concentration', 'dust_concentration_pm1', 'dust_concentration_pm10'] else group['dust_concentration'])
                message += f'{LABELS_OF_PARAMS[key]}: {level_sign} {recently_params[key]} {MEANS_OF_PARAMS[key]} {dynamic_sign}\n'
        return message


def app_box_recently_params(bot: Bot, update: Updater, user_data: dict):
    recently_params, previous_params = user_data['api'].get_recently_params_with_previous(
        user_data['active_box'])
    message = ''
    if 'code' in recently_params:
        message = recently_params['msg']
    else:
        message = build_response(recently_params, previous_params,
                                 user_data['api'].get_group_for_box(user_data['active_box']))
    bot.send_message(
        chat_id=update.message.chat_id,
        text=message
    )


def app_box_first_date(bot: Bot, update: Updater, user_data: dict):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Please enter start date in format DD/MM/YY',
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton(text='Cancel')]])
    )
    return APP_BOX_FIRST_DATE_HANDLE


def app_box_second_date(bot: Bot, update: Updater, user_data: dict):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Please enter end date in format DD/MM/YY',
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton(text='Cancel')]])
    )
    return APP_BOX_SECOND_DATE_HANDLE


def app_plotting_view(bot: Bot, update: Updater, user_data: dict):
    start_date = user_data['start_date']
    end_date = user_data['end_date']
    if start_date > end_date:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='End date can\'t be sooner then start date, rewrite end date or press Cancel'
        )
        return APP_BOX_SECOND_DATE_HANDLE
    else:
        # plotting_result = build_plots(user_data['api'].get_params_in_interval(
        #     user_data['active_box'], int(start_date.timestamp()), int(end_date.timestamp())))
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f'sample'
            #            text=plotting_result['msg'] if 'msg' in plotting_result else None,
        )
        return app_box_view(bot, update, user_data)
