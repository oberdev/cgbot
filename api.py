import requests
BASE_URL = 'https://api.climateguard.info/api'


def is_unhandleable_error(response: requests.Response):
    return response.status_code >= 500


def is_handleable_error(response: requests.Response):
    return response.status_code >= 400


def process_response(response, callback_action, callback_refresh=None, original_function=None, params: dict={}):
    if is_unhandleable_error(response):
        return False
    elif is_handleable_error(response):
        error = response.json()
        if callback_refresh and original_function and error['msg'] == 'Expired JWT Token':
            refresh_result = callback_refresh()
            if refresh_result:
                return original_function(**params)
        else:
            return error
    else:
        return callback_action(response)


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
        response = self.api.post(f'{self.url}/user/login_check', json={
            "username": username,
            "password": password
        })
        return process_response(response, self._token_obtain_process)

    def _token_obtain_process(self, response: requests.Response):
        result = response.json()
        self.refresh_token = result['refresh_token']
        self.token = result['token']
        self.api.headers['Authorization'] = f'Bearer {self.token}'
        return result

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
        response = self.api.get(f'{self.url}/user/objects/hierarchy')
        return process_response(response, lambda x: x.json(), self.token_refresh, self.get_hierarchy)

    def get_recently_params(self, uuid):
        response = self.api.get(f'{self.url}/user/box/{uuid}/last_measures')
        return process_response(response, lambda x: x.json(), self.token_refresh, self.get_recently_params,
                                {'uuid': uuid})

    def get_params_in_interval(self, uuid, start_timestamp, end_timestamp):
        response = self.api.get(
            f'{self.url}/user/box/{uuid}/mean_measures/since/{start_timestamp}/till/{end_timestamp}')
        return process_response(response, lambda x: x.json(), self.token_refresh, self.get_params_in_interval,
                                {'uuid': uuid, 'start_timestamp': start_timestamp, 'end_timestamp': end_timestamp})

    def get_group_for_box(self, uuid):
        response = self.api.get(f'{self.url}/user/box/{uuid}/profile')
        return process_response(response, lambda x: x.json()['profile'], self.token_refresh, self.get_group_for_box,
                                {'uuid': uuid})

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