import requests
import json
BASE_URL = 'https://api.climateguard.info/api'


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

    def json(self, response: requests.Response):
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            return False
        else:
            return result

    def token_obtain(self, username, password):
        result = self.api.post(f'{self.url}/user/login_check', json={
            "username": username,
            "password": password
        })
        print(type(result) == requests.Response)
        if result.status_code == 401:
            return {'error': result.json()['message']}
        else:
            data = result.json()
            self.refresh_token = data['refresh_token']
            self.token = data['token']
            self.api.headers['Authorization'] = f'Bearer {self.token}'
            return data

    def token_refresh(self):
        result = self.api.post(f'{self.url}/user/token/refresh', json={
            'refresh_token': self.refresh_token
        })
        if result.status_code == 401:
            return False
        elif result.status_code == 200:
            result = result.json()
            self.token = result['token']
            self.api.headers['Authorization'] = f'Bearer {self.token}'
            return True

    def get_hierarchy(self):
        results = self.api.get(f'{self.url}/user/objects/hierarchy')
        if results.status_code == 401:
            refresh_result = self.token_refresh()
            if refresh_result:
                return self.get_hierarchy()
            else:
                return {'code': 401, 'msg': 'Auth is outdated, please reauth'}
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
        print(results.json())
        if results.status_code == 404:
            return DEFAULT_PROFILE
        elif results.status_code == 200:
            return results.json()['profile']

    def get_recently_params_with_previous(self, uuid):
        recently_params: dict = self.get_recently_params(uuid)
        if 'code' in recently_params:
            if recently_params['code'] == 404 or recently_params['code'] == 403:
                return recently_params, None
            elif recently_params['code'] == 401:
                refresh_result = self.token_refresh()
                if refresh_result:
                    return self.get_recently_params_with_previous(uuid)
                else:
                    return {'code': 401, 'msg': 'Auth is outdated, please reauth'}
        else:
            previous_params = self.get_params_in_interval(
                uuid, recently_params['timestamp'] - 1200, recently_params['timestamp'])
            if not 'code' in previous_params and 'timestamp' in previous_params and len(previous_params['timestamp']) > 1:
                true_previous_params = {
                    key: previous_params[key][1] for key in recently_params.keys()}
                return recently_params, true_previous_params
            else:
                return recently_params, None
