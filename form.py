from flask_wtf import FlaskForm
from wtforms import RadioField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class Form(FlaskForm):
    """Input parameters"""
    model = RadioField('Select a model:', [DataRequired()],
                       choices=[('A', 'A'), ])
    xbj = DecimalField('xbj = ',
                       validators=[NumberRange(min=0, max=1, message="Invalid number"), DataRequired()])
    t   = DecimalField('t = ',
                       validators=[NumberRange(min=-10, max=0, message="Invalid number"), DataRequired()])
    q2  = DecimalField('q2 = ',
                       validators=[NumberRange(min=0, max=100, message="Invalid number"), DataRequired()])
    submit = SubmitField('Submit')
