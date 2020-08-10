from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField, RadioField
from wtforms.validators import InputRequired, NumberRange
import femtomesh as fm

class Form(FlaskForm):
    """Input parameters"""

# search for model names
    model_dirs = fm.FemtoMesh.model_search()
    model_choices = [
        (m.split('_', 1)[1], m.split('_', 1)[1].upper() + ' Model' ) for m in model_dirs
    ]

    model = SelectField(
        'Select a model:',
        [InputRequired()],
        choices = model_choices
    )

    gpd_model = RadioField(
        'GPD',
        [InputRequired()],
        choices=[
            ('GPD_E.csv','GPD_E'),
            ('GPD_H.csv','GPD_H')
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

    submit = SubmitField('Plot')

    download = SubmitField('Download model as CSV')
