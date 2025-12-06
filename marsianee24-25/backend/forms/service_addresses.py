from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class ServiceAddress(FlaskForm):
    url = StringField('Адрес API', validators=[DataRequired(), URL()])
    submit = SubmitField('Загрузить данные')