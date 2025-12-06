from flask import Blueprint, jsonify

blueprint = Blueprint('graphics', __name__)

@blueprint.route('/api/stations_count')
def stations_count():
    # Пример API для графиков (можно расширить)
    return jsonify({"cuper": 12, "engel": 3})