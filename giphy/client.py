import requests
import json
from random import randint


API_KEY = 'dc6zaTOxFJmzC'
SEARCH_URI ='http://api.giphy.com/v1/gifs/search'

session = requests.Session()
session.params = {
    'api_key': API_KEY
}

def get(term='dancing bears', get_content=False):
    res = session.get(SEARCH_URI, params={
        'q': term
    })

    json_data = res.json()
    if not 'data' in json_data:
        print(json_data)
        return None
    images = json_data['data']
    if not len(images):
        print(json_data)
        return None

    pick = randint(0, len(images) - 1)
    url = images[pick]['images']['original']['url']

    if get_content:
        content = requests.get(url).text
        return content
    return url

if __name__ == '__main__':
    import sys
    print(get(' '.join(sys.argv[1:])))

