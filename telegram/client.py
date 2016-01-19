import requests
from urllib.request import urlretrieve
from time import time
from redis import StrictRedis
from json import dumps, loads


class TelegramClient:
    method_url = 'https://api.telegram.org/bot{token}/{method}'
    redis = None

    def __init__(self, token):
        self.token = token
        self.__init_redis()
    
    def __init_redis(self):
        try:
            redis = StrictRedis()
            redis.ping()    # raises an exception if it failes
            self.redis = redis
        except:
            pass

    def __generate_url(self, method, path):
        url = self.method_url.format(token=self.token, method=method)
        if path:
            url = '/'.join((url, path))
        return url

    def __to_cache(self, url, content, expire=86400):
        if self.redis:
            self.redis.set(url, content)
            if expire:
                self.redis.expire(url, expire)
        return False

    def __from_cache(self, url):
        try:
            return self.redis.get(url)
        except:
            return None

    def __make_request(self, method, path=None, data={}, params={}, files={}):
        try:
            url = self.__generate_url(method, path)
            print('>', url)
            res = requests.post(url, data=data, params=params, files=files)
            content = res.json()
            print(res.status_code, content)
            return content
        except:
            return None

    def set_web_hook(self, hook_url):
        return self.__make_request('setWebHook', data={
            'url': hook_url
        })

    def get_updates(self, offset=0):
        return self.__make_request('getUpdates', params={
            'offset': offset
        })

    def send_message(self, chat_id, text):
        return self.__make_request('sendMessage', data={
            'chat_id': chat_id,
            'text': text
        })

    def send_photo(self, chat_id, photo_url):
        file_handler = self.__from_cache(photo_url)
        print('got file_id', file_handler)
        if not file_handler:
            filename = str(time()) + '_photo.gif'
            urlretrieve(photo_url, filename)
            file_handler = open(filename, 'rb')
        content = self.__make_request('sendDocument', data={
            'chat_id': chat_id
        }, files={
            'document': file_handler
        })
        file_id = content['result']['document']['file_id']
        self.__to_cache(photo_url, file_id, expire=None)
        return content

    def send_chat_action(self, chat_id, action='typing'):
        return self.__make_request('sendChatAction', data={
            'chat_id': chat_id,
            'action': action
        })

