from telegram.nclient import TelegramClient
from time import time, sleep
# from anne.report import Report
from giphy.client import get as getgif
from json import loads


# get the token from the file
token = ''
with open('token', 'r') as f:
    token = f.read().strip()

# telegram client
tClient = TelegramClient(token)
PUSH_URL = 'https://fuwa.co.uk/' + token
tClient.set_web_hook(PUSH_URL)

"""
report = Report()
def search(term, chat_id):
    anime, closest = report.search(term)
    try:
        anime.fill()
        info = anime.info

        table = ''
        for key in sorted(list(info.keys())):
            value = info[key]
            print(key, value)
            if isinstance(value, list):
                value = ', '.join([str(v) for v in value])
            print(value)
            table += ''.join([key, '\n', value, '\n\n'])

        if len(closest) > 1:
            table += 'Other matched titles:\n' + ', '.join(closest[1:])
        return table
    except:
        pass
    return 'can\'t find ' + term
"""

def gif(term, chat_id):
    url = getgif(term)
    if url:
        tClient.send_photo(chat_id, url)
        return None
    return 'No gif found for ' + term

commands = {
    '/gif': gif
}

def process(body):
    try:
        update = loads(body)
    except:
        print('invalid body', body)
        return False

    if not 'text' in update['message']:
        return False

    chat_id = update['message']['chat']['id']
    text = update['message']['text']
    text = text.split(' ')
    command = text[0]

    if command in commands:
        tClient.send_chat_action(chat_id)
        result = commands[command](' '.join(text[1:]), chat_id)
        if result:
            tClient.send_message(chat_id, result)

def app(environ, start_response):
    method = environ['REQUEST_METHOD']
    uri = environ['RAW_URI']
    body = environ['wsgi.input'].read().decode('utf-8')

    if uri[1:] == token:
        process(body)

    start_response("200 OK", [])
    return iter([])

