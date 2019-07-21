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

    def token_obtain(self, username, password):
        result = self.api.post(f'{self.url}/user/login_check', json={
            "username": username,
            "password": password
        })
        print(result.headers)
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


GCApi = CGApiClient()
