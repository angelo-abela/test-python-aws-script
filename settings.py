import requests
from decouple import config


class Config:
    def __init__(self):
        self.AWS_ACCESS_KEY = config('AWS_ACCESS_KEY')
        self.AWS_SECRET_KEY = config('AWS_SECRET_KEY')
        self.REGIONS = config('REGIONS')
        self.CRON_TIME = config('CRON_TIME') or 5


class Request:
    def __init__(self):
        self.url = config('API_URL')
        self.headers = {
            'x-editor-id': 'test_editor_id',
            'Content-Type': 'application/json'
        }
        self.timeout = 5

    def get(self, params=None):
        res = requests.get(self.url, params=params, headers=self.headers, timeout=self.timeout)
        return res.text

    def post(self, data=None, json_data=None):
        res = requests.post(self.url, data=data, json=json_data, headers=self.headers, timeout=self.timeout)
        return res.text

    def put(self, data=None):
        res = requests.put(self.url, data=data, headers=self.headers, timeout=self.timeout)
        return res.text
