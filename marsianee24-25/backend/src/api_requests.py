import requests
import json

def get_url():
    with open("./backend/src/url_addr.json", "rt", encoding="utf-8") as f:
        return json.load(f)['url']

def get_all_tiles():
    print('Получение тайлов...')
    url = get_url()
    tiles = []
    while len(tiles) != 16:
        resp = requests.get(url)
        if resp.status_code == 200:
            relief = resp.json()['message']['data']
            if relief not in tiles:
                tiles.append(relief)
    print("Тайлы получены")
    return tiles

def get_coords() -> dict:
    url = get_url()
    while True:
        resp = requests.get(url + "/coords")
        if resp.status_code == 200:
            data = resp.json()['message']
            return {
                'listener': (int(data['listener'][0]), int(data['listener'][1])),
                'sender': (int(data['sender'][0]), int(data['sender'][1])),
                'price': {'cuper': float(data['price'][0]), 'engel': float(data['price'][1])}
            }
        print(resp.status_code)