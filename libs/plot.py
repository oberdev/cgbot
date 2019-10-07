import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
from datetime import datetime
from io import BytesIO

from constants import RECENTLY_PARAMS_KEYS, LABELS_OF_PARAMS


def preprocess_api_data(data: dict) -> dict:
    temp_data = {k: np.array(data[k]) for k in data}
    return temp_data

def draw_limits(limits):
    pass


def build_plots(data: dict):
    if 'code' in data and data['code'] == 404:
        return {'is_success': False, 'msg': data['msg']}
    prepared_data = preprocess_api_data(data)
    dates = [datetime.fromtimestamp(timestamp) for timestamp in prepared_data['timestamp']]
    # param_keys = [key for key in prepared_data.keys() if key != 'timestamp' and key != 'profile']
    param_keys = RECENTLY_PARAMS_KEYS.copy()
    images = []
    for key in param_keys:
        # draw_limits(prepared_data['profile'][key])
        image = BytesIO()
        plt.subplots_adjust(bottom=0.2)
        plt.xticks(rotation=25)
        ax = plt.gca()
        xfmt = md.DateFormatter('%Y-%m-%d')
        ax.xaxis.set_major_formatter(xfmt)
        plt.title(LABELS_OF_PARAMS[key])
        plt.plot(dates, prepared_data[key])
        plt.savefig(image, format='png')
        image.seek(0)
        images.append(image)
        plt.clf()
        plt.cla()
    return {'is_success': True, 'data': images}
