from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Email

from ..models import Category

class CategoryForm(FlaskForm):
    name = StringField()
    keywords = StringField()
    submit = SubmitField()
