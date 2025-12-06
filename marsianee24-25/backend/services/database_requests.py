import json
import sqlite3
from backend.database import db_session
from backend.src.api_requests import get_all_tiles, get_coords
from backend.tiles import get_field

def fill_database(map_id=1):
    conn = db_session.get_connection()
    cur = conn.cursor()

    # 1. Получаем координаты модулей и цены
    coords = get_coords()
    sender = coords['sender']
    listener = coords['listener']
    price_cuper = coords['price']['cuper']
    price_engel = coords['price']['engel']

    # 2. Сохраняем модули
    cur.execute("INSERT INTO modules (map_id, x, y, name) VALUES (?, ?, ?, ?)",
                (map_id, sender[0], sender[1], "sender"))
    cur.execute("INSERT INTO modules (map_id, x, y, name) VALUES (?, ?, ?, ?)",
                (map_id, listener[0], listener[1], "listener"))

    # 3. Получаем и сохраняем тайлы (опционально, можно хранить поле)
    tiles = get_all_tiles()
    for idx, tile in enumerate(tiles):
        cur.execute("INSERT INTO tiles (map_id, tile_index, data) VALUES (?, ?, ?)",
                    (map_id, idx, json.dumps(tile)))

    # 4. Собираем поле и рассчитываем станции (упрощённо — по пикам)
    field = get_field()
    stations = find_peaks(field, price_cuper, price_engel)
    for (x, y, station_type, price) in stations:
        cur.execute("INSERT INTO stations (map_id, x, y, type, price) VALUES (?, ?, ?, ?, ?)",
                    (map_id, x, y, station_type, price))

    conn.commit()

def find_peaks(field, price_cuper, price_engel):
    # Упрощённый алгоритм: находить локальные максимумы (пики)
    stations = []
    size = len(field)
    threshold = 200  # порог высоты
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            val = field[i][j]
            if val >= threshold:
                neighbors = [
                    field[i-1][j], field[i+1][j],
                    field[i][j-1], field[i][j+1],
                    field[i-1][j-1], field[i+1][j+1],
                    field[i-1][j+1], field[i+1][j-1]
                ]
                if all(val > n for n in neighbors):
                    # Решаем: какую станцию ставить? (упрощённо — только "cuper")
                    stations.append((i, j, 'cuper', price_cuper))
    return stations

def get_stations(map_id=1):
    conn = db_session.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT x, y, type, price FROM stations WHERE map_id = ?", (map_id,))
    return cur.fetchall()

def get_map(map_id=1):
    field = get_field()  # 256x256, значения от 0 до 255
    return field

def get_custom_map(modules=False, stations=False, coverage=False, map_id=1):
    field = [[[0, 0] for _ in range(256)] for _ in range(256)]  # [type, param]

    conn = db_session.get_connection()
    cur = conn.cursor()

    if modules:
        cur.execute("SELECT x, y FROM modules WHERE map_id = ?", (map_id,))
        for x, y in cur.fetchall():
            field[x][y] = [1, 0]  # модуль

    if stations:
        cur.execute("SELECT x, y, type FROM stations WHERE map_id = ?", (map_id,))
        for x, y, typ in cur.fetchall():
            radius = 32 if typ == 'cuper' else 64
            field[x][y] = [2, radius]  # станция

            if coverage:
                # Отметить зону покрытия
                for di in range(-radius, radius + 1):
                    for dj in range(-radius, radius + 1):
                        ni, nj = x + di, y + dj
                        if 0 <= ni < 256 and 0 <= nj < 256:
                            dist_sq = di*di + dj*dj
                            if dist_sq <= radius*radius:
                                if field[ni][nj][0] != 2:  # не перекрывать станции
                                    field[ni][nj] = [3, radius]

    return field