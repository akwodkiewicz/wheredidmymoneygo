from flask_wtf import FlaskForm
from wtforms import (
    StringField, DecimalField, SelectField, DateField, SubmitField
)

class TransactionForm(FlaskForm):
    description = StringField()
    amount = DecimalField()
    ttype = SelectField(choices=[('out', 'Outcome'), ('in', 'Income')])
    date = DateField()
    category = SelectField(coerce=int)
    submit = SubmitField()