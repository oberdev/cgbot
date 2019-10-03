from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup, Update
from datetime import datetime
from constants import EMOJI, RECENTLY_PARAMS_KEYS, COLORS_LIST, REVERSE_COLORS_LIST, LABELS_OF_PARAMS, \
    MEANS_OF_PARAMS

main_menu_buttons = ["Buildings", "Settings"]

button_list = [
    [KeyboardButton(text=button_text) for button_text in main_menu_buttons]
]

markup = ReplyKeyboardMarkup(button_list)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def app_user_view(bot: Bot, updater: Update):
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="Main menu",
        reply_markup=markup
    )


def app_empty_view(bot: Bot, updater: Update):
    bot.send_message(
        chat_id=updater.message.chat_id,
        text="There are no content to show"
    )


def mock_view(bot: Bot, update: Update, user_data: dict):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="In developing",
    )


def _get_compare_emoji(a, b):
    if b is None:
        return EMOJI['no_info']
    elif a > b:
        return EMOJI['arrows']['up']
    elif a < b:
        return EMOJI['arrows']['down']
    else:
        return EMOJI['arrows']['equal']


def _get_level_emoji(param: float, group_node: dict or list):
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
        values_list = group_node.copy()
        values_list.insert(0, -float('inf'))
        emoji_list = [EMOJI['colors'][key] for key in COLORS_LIST]
        individual_scale = dict(zip(values_list, emoji_list))
        temp_list = list(individual_scale.items())
        for value, _ in temp_list[::-1]:
            if value < param:
                return individual_scale[value]
        return emoji_list[-1]


def build_response(recently_params: dict, previous_params: dict, group, box_name=''):
    if not recently_params:
        return 'There is imposible to convert recently params to message'
    else:
        message = ''
        message += '' if box_name == '' else f'The box_id is {box_name}\n'
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
                message += f'{LABELS_OF_PARAMS[key]}: {level_sign} {recently_params[key]} {MEANS_OF_PARAMS[key]}' \
                           f' {dynamic_sign}\n'
        return message
