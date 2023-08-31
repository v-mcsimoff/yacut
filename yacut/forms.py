from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Input a link',
        validators=[DataRequired(message='Required field'),
                    Length(1, 512)]
    )
    custom_id = StringField(
        'Short link option',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Create')
