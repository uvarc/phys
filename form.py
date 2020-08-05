from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField
from wtforms.validators import InputRequired, NumberRange

class Form(FlaskForm):
    """Input parameters"""
    model = SelectField(
        'Select a model:',
        [InputRequired()],
        choices=[
            ('A', 'A'),
        ]
    )

    xbj = DecimalField(
        'xbj ',
        [NumberRange(min=0., max=1., message="Please set %(min)s <= xbj <= %(max)s"), InputRequired()]
    )

    t = DecimalField(
        't ',
        [NumberRange(min=-10., max=10., message="Please set %(min)s <= t <= %(max)s"), InputRequired()]
    )

    q2 = DecimalField(
        'q2 ',
        [NumberRange(min=-10., max=100., message="Please set %(min)s <= q2 <= %(max)s"), InputRequired()]
    )

    submit = SubmitField('Submit')
