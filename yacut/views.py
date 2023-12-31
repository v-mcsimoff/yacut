import string
from random import choice

from flask import flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap


SHORT_ID_LENGTH = 6


def generate_short_id():
    characters = string.ascii_letters + string.digits
    while True:
        short_id = "".join(choice(characters) for i in range(SHORT_ID_LENGTH))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/', methods=('GET', 'POST'))
def get_unique_short_id():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short_id = form.custom_id.data
    if short_id and URLMap.query.filter_by(short=short_id).first():
        flash(f'Имя {short_id} уже занято!')
        return render_template('index.html', form=form)
    if not short_id:
        short_id = generate_short_id()
    unique_short_id = URLMap(original=form.original_link.data, short=short_id)
    db.session.add(unique_short_id)
    db.session.commit()
    context = {'short_id': short_id}
    return render_template('index.html', form=form, **context)


@app.route('/<string:short>')
def get_original_link(short):
    link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(link.original, 302)
