from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField
from wtforms.validators import InputRequired, NumberRange

import femtomesh.femtomesh as fm


class Form(FlaskForm):
    """
    Form class defines the fields format of frontend site. Model list is pulled from either the local mesh model list
    or from the Redis database.

    Forms are prefilled with default values and ranges; they are modified at a later time once the model/gpd is
    selected.
    """

    model_dirs = fm.FemtoMesh.model_search()
    model_choices = [
        (m.split('_', 1)[1], m.split('_', 1)[1].upper() + ' Model') for m in model_dirs
    ]

    gpds = fm.FemtoMesh.gpd_search('model_uva')
    gpd_list = [
        (gpd.split('.')[0], gpd.split('.')[0]) for gpd in gpds
    ]

    model = SelectField(
        'Select a model: ',
        [InputRequired()],
        choices=model_choices
    )

    gpd_model = SelectField(
        'Select GPD: ',
        [InputRequired()],
        choices=gpd_list
    )

    xbj = SelectField(
        'xbj',
        [InputRequired()],
        choices=[],
        validate_choice=False,
        coerce=float
    )

    t = SelectField(
        't',
        [InputRequired()],
        choices=[],
        validate_choice=False,
        coerce=float
    )

    q2 = DecimalField(
        'q2 ',
        [NumberRange(min=1e-4, max=10., message="Please set Q2"), InputRequired()]
    )

    submit = SubmitField('Plot')
    load = SubmitField('Load Model')
    download = SubmitField('Download model as CSV')
