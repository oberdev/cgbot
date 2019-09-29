import numpy as np
import matplotlib.pyplot as plt


def preprocess_api_data(data: dict) -> dict:
    return {k: np.array(data[k]) for k in data}


def build_plots(data: dict):
    if 'code' in data and data['code'] == 404:
        return {'is_success': False, 'msg': data['msg']}
    prepared_data = preprocess_api_data(data)
    print(prepared_data)
    param_keys = [key for key in prepared_data.keys() if key != 'timestamp']
    for key in param_keys:
        plt.plot(prepared_data['timestamp'], prepared_data[key])
        plt.show()
