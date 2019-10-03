from telegram import ReplyKeyboardMarkup, KeyboardButton, Update, Bot

from constants import APP_BOX_FIRST_DATE_HANDLE, APP_BOX_SECOND_DATE_HANDLE, APP_BOX_ACTIONS
from libs.plot import build_plots
from utils import build_response

box_actions_list = ['Recently indicators', 'Plot']


def app_box_first_date(bot: Bot, update: Update, user_data: dict):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Please enter start date in format DD/MM/YY',
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton(text='Cancel')]])
    )
    return APP_BOX_FIRST_DATE_HANDLE


def app_box_second_date(bot: Bot, update: Update, user_data: dict):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Please enter end date in format DD/MM/YY',
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton(text='Cancel')]])
    )
    return APP_BOX_SECOND_DATE_HANDLE


def app_box_view(bot: Bot, update: Update, user_data: dict):
    recently_params, previous_params = user_data['api'].get_recently_params_with_previous(
        user_data['active_box'])
    message = ''
    if 'code' in recently_params:
        message = recently_params['msg']
    else:
        message = build_response(recently_params, previous_params,
                                 user_data['api'].get_group_for_box(user_data['active_box']), user_data['active_box'])

    bot.send_message(
        chat_id=update.message.chat_id,
        text=message,
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton(text=action) for action in box_actions_list], [KeyboardButton(text='Back')]])
    )
    return APP_BOX_ACTIONS


def app_box_recently_params(bot: Bot, update: Update, user_data: dict):
    recently_params, previous_params = user_data['api'].get_recently_params_with_previous(
        user_data['active_box'])
    if 'code' in recently_params:
        message = recently_params['msg']
    else:
        message = build_response(recently_params, previous_params,
                                 user_data['api'].get_group_for_box(user_data['active_box']))
    bot.send_message(
        chat_id=update.message.chat_id,
        text=message
    )


def app_plotting_view(bot: Bot, update: Update, user_data: dict):
    start_date = user_data['start_date']
    end_date = user_data['end_date']
    if start_date > end_date:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='End date can\'t be sooner then start date, rewrite end date or press Cancel'
        )
        return APP_BOX_SECOND_DATE_HANDLE
    else:
        user_data['api'].test_query(user_data['active_box'], int(
            start_date.timestamp()), int(end_date.timestamp()))
        plotting_result = build_plots(user_data['api'].get_params_in_interval(
            user_data['active_box'], int(start_date.timestamp()), int(end_date.timestamp())))
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f'sample'
            #            text=plotting_result['msg'] if 'msg' in plotting_result else None,
        )
        return app_box_view(bot, update, user_data)

