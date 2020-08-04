from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField
from wtforms.validators import InputRequired, NumberRange

class Form(FlaskForm):
    """Input parameters"""
    model = SelectField('Select a model:', [InputRequired()],
                       choices=[('A', 'A'), ])
    xbj = DecimalField('xbj = ',
                       validators=[NumberRange(min=0., max=1., message="xbj should be between %(min)s and %(max)s"), InputRequired()])
    t   = DecimalField('t = ',
                       validators=[NumberRange(min=-10., max=10., message="t should be between %(min)s and %(max)s"), InputRequired()])
    q2  = DecimalField('q2 = ',
                       validators=[NumberRange(min=-10., max=100., message="q2 should be between %(min)s and %(max)s"), InputRequired()])
    submit = SubmitField('Submit')
