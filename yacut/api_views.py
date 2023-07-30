from flask import jsonify, request, url_for

from . import app, db
from .models import URLMap
from .views import generate_short_id
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def get_short_id():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса', 404)
    custom_id = data.get('custom_id')
    if custom_id is None:
        custom_id = generate_short_id()
    if 'url' not in data:
        raise InvalidAPIUsage('Поле "url" является обязательным', 404)
    if custom_id is not None and len(custom_id) > 16:
        raise InvalidAPIUsage('Указано некорректное имя для короткой ссылки', 404)
    if 'custom_id' in data:
        if not custom_id:
            data['custom_id'] = generate_short_id()
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(f'Ссылка {custom_id} уже используется.', 404)
    urlmap = URLMap(original=data['url'], short=custom_id)
    db.session.add(urlmap)
    db.session.commit()
    return (
        jsonify(
            {
                'url': urlmap.original,
                'short_link': url_for(
                    'get_original_link', short=urlmap.short, _external=True
                ),
            }
        ),
        201,
    )


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        raise InvalidAPIUsage('id не найден', 404)
    return jsonify({'url': link.original})
