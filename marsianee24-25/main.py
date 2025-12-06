import os
import requests
import json
from dotenv import load_dotenv
from flask import Flask, render_template, abort
from backend.database import db_session
from backend.routers import graphics, users
from backend.services.database_requests import get_stations, get_map, get_custom_map, fill_database
from backend.forms.service_addresses import ServiceAddress

app = Flask(__name__)
app.config['SECRET_KEY'] = "Otcheburashim"

def count_price():
    d = {'cuper': 0, 'engel': 0}
    prices = {'cuper': 0, 'engel': 0}
    stations_list = get_stations()
    for i in stations_list:
        station_type = i[2]
        if station_type in d:
            d[station_type] += 1
            prices[station_type] = i[3]
        # Игнорируем неизвестные типы
    return (d['cuper'], prices['cuper'], d['engel'], prices['engel'])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ServiceAddress()
    if form.validate_on_submit():
        url = form.url.data
        try:
            req = requests.get(url)
        except Exception:
            abort(400)
        with open('backend/src/url_addr.json', 'w') as f:
            json.dump({"url": url}, f)
        with open('map_id.json', 'r') as f:
            map_id = json.load(f)['map_id']
        with open('map_id.json', 'w') as f:
            json.dump({"map_id": map_id + 1}, f)
        fill_database(map_id + 1)
        return render_template("index.html", form=form)
    return render_template("index.html", form=form)

@app.route('/map', methods=['GET', 'POST'])
def map():
    with open('map_id.json', 'r') as f:
        map_id = json.load(f)['map_id']
    map_data = get_map(map_id)
    return render_template("map.html", map=map_data, len=len(map_data), p=count_price())

@app.route('/full', methods=['GET', 'POST'])
def full():
    with open('map_id.json', 'r') as f:
        map_id = json.load(f)['map_id']
    map_data = get_custom_map(modules=True, stations=True, coverage=True, map_id=map_id)
    return render_template("full.html", map=map_data, len=len(map_data), p=count_price())

@app.route('/station', methods=['GET', 'POST'])
def station():
    with open('map_id.json', 'r') as f:
        map_id = json.load(f)['map_id']
    map_data = get_custom_map(modules=False, stations=True, coverage=False, map_id=map_id)
    return render_template("station.html", map=map_data, len=len(map_data), p=count_price())

@app.route('/coverage', methods=['GET', 'POST'])
def coverage():
    with open('map_id.json', 'r') as f:
        map_id = json.load(f)['map_id']
    map_data = get_custom_map(modules=False, stations=True, coverage=True, map_id=map_id)
    return render_template("coverage.html", map=map_data, len=len(map_data), p=count_price())

@app.route('/module', methods=['GET', 'POST'])
def module():
    with open('map_id.json', 'r') as f:
        map_id = json.load(f)['map_id']
    map_data = get_custom_map(modules=True, stations=False, coverage=False, map_id=map_id)
    return render_template("module.html", map=map_data, len=len(map_data), p=count_price())

if __name__ == "__main__":
    db_session.init()
    if not os.path.exists('backend/database/predprof.db'):
        fill_database()
    app.register_blueprint(graphics.blueprint)
    app.register_blueprint(users.blueprint)
    load_dotenv()
    app.run(port=int(os.getenv('SERVER_PORT', 8080)), host=os.getenv('SERVER_HOST', '127.0.0.1'), threaded=True)