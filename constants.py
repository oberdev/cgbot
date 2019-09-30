APP_BOX_ACTIONS, AUTH_INVITE, AUTH_USERNAME, AUTH_PASSWORD, AUTH_VALIDATION, APP_MENU_CASES, APP_BUILDINGS_CASES, APP_BUILDING_CASES, APP_BOXES_CASES, APP_ROOMS_CASES, APP_BOX_FIRST_DATE_HANDLE, APP_BOX_SECOND_DATE_HANDLE = range(
    12)

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
                        'noise_level', 'light_level', 'light_ripple', 'co2_concentration', 'voc_concentration', 'magnetic_radiation', 'humidity', 'dust_concentration_pm1', 'dust_concentration', 'dust_concentration_pm10']

COLORS_LIST = ['purple', 'blue', 'green', 'yellow', 'red']
REVERSE_COLORS_LIST = ['green', 'orange', 'red']

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