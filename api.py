import requests
import json
BASE_URL = 'https://api.climateguard.info/api'

DEFAULT_PROFILE = {
    'temperature': [
        18,
        23,
        25,
        26,
    ],
    'vibration': {
        "1": 0,
        "2": 1.3,
        "3": 1.4
    },
    "noise_level": {
        "1": 0,
        "2": 50,
        "3": 80
    },
    "dust_concentration": {
        "1": 0,
        "2": 0.16,
        "3": 0.15
    },
    "light_level": [
        50,
        100,
        550,
        750
    ],
    "light_ripple": {
        "1": 0,
        "2": 25,
        "3": 50
    },
    "co2_concentration": {
        "1": 0,
        "2": 600,
        "3": 1000
    },
    "voc_concentration": {
        "1": 0,
        "2": 1,
        "3": 40
    },
    "magnetic_radiation": {
        "1": 0,
        "2": 100,
        "3": 500
    },
    "humidity": [
        30,
        37.5,
        45,
        60
    ],
}


class CGApiClient(object):

    def __init__(self, token=None, refresh_token=None, url=BASE_URL):
        api = requests.Session()
        api.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.api = api
        self.url = url
        self.token = token
        if self.token:
            self.api.headers['Authorization'] = f'Bearer {self.token}'
        self.refresh_token = refresh_token

    def token_obtain(self, username, password):
        result = self.api.post(f'{self.url}/user/login_check', json={
            "username": username,
            "password": password
        })
        if result.status_code == 401:
            return {'error': result.json()['message']}
        else:
            data = result.json()
            self.refresh_token = data['refresh_token']
            self.token = data['token']
            self.api.headers['Authorization'] = f'Bearer {self.token}'
            return data

    def token_refresh(self):
        pass

    def get_hierarchy(self):
        results = self.api.get(f'{self.url}/user/objects/hierarchy')
        return results.json()

    def get_recently_params(self, uuid):
        results = self.api.get(f'{self.url}/user/box/{uuid}/last_measures')
        return results.json()

    def get_params_in_interval(self, uuid, startstamp, endstamp):
        results = self.api.get(
            f'{self.url}/user/box/{uuid}/measures/since/{startstamp}/till/{endstamp}')
        return results.json()

    def get_group_for_box(self, uuid):
        results = self.api.get(f'{self.url}/user/box/{uuid}/profile')
        if results.status_code == 404:
            return DEFAULT_PROFILE
        elif results.status_code == 200:
            return results.json()

    def get_recently_params_with_previous(self, uuid):
        recently_params: dict = self.get_recently_params(uuid)
        print(recently_params['code'])
        if 'code' in recently_params and (recently_params['code'] == 404 or recently_params['code'] == 403):
            return None, None
        else:
            previous_params = self.get_params_in_interval(
                uuid, recently_params['timestamp'] - 600, recently_params['timestamp'])
            if not 'code' in previous_params and 'timestamp' in previous_params and len(previous_params['timestamp']) > 1:
                true_previous_params = {
                    key: previous_params[key][1] for key in recently_params.keys()}
                return recently_params, true_previous_params
            else:
                return recently_params, None
