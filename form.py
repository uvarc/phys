from flask_wtf import FlaskForm
from wtforms import RadioField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class Form(FlaskForm):
    """Input parameters"""
    csv = RadioField('csv', [DataRequired()],
                     choices=[('GPD_E.csv', 'GPD_E'),
                              ('GPD_H.csv', 'GPD_H'),
                              ])
    xbj = DecimalField('xbj',
                       [NumberRange(min=0, max=1, message="Invalid number"), DataRequired()])
    t   = DecimalField('t',
                       [NumberRange(min=-10, max=0, message="Invalid number"), DataRequired()])
    q2  = DecimalField('q2',
                       [NumberRange(min=0, max=100, message="Invalid number"), DataRequired()])
    submit = SubmitField('Submit')
