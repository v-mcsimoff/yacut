import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .models import URLMap
from .views import generate_short_id
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def get_short_id():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Request body is missing', HTTPStatus.BAD_REQUEST)
    custom_id = data.get('custom_id')
    if custom_id is None:
        custom_id = generate_short_id()
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" is a required field!', HTTPStatus.BAD_REQUEST)
    if custom_id and not re.match(r'^[a-zA-Z0-9]*$', custom_id):
        raise InvalidAPIUsage("Invalid name for a short link is provided", HTTPStatus.BAD_REQUEST)
    if custom_id and len(custom_id) > 16:
        raise InvalidAPIUsage("Invalid name for a short link is provided", HTTPStatus.BAD_REQUEST)
    if 'custom_id' in data:
        if not custom_id:
            data['custom_id'] = generate_short_id()
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage('The name "py" is already taken.', HTTPStatus.BAD_REQUEST)
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
        HTTPStatus.CREATED,
    )


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        raise InvalidAPIUsage('The id is not found', HTTPStatus.NOT_FOUND)
    return jsonify({'url': link.original})
