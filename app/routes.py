import os
import itertools
import femtomesh as fm

from flask import request, render_template, redirect, Response, jsonify

from app import app
from form import Form
from mesh import create_plot


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    form.xbj.choices = [(round(0.0001*value,4)) for value in range(1, 20)]
    form.t.choices = [(round(-0.1*value, 4)) for value in range(1, 20)]


    if request.method == 'POST' and form.validate_on_submit():
        model = request.form['model']
        gpd_model = request.form['gpd_model']
        xbj = float(request.form['xbj'])
        t = float(request.form['t'])
        q2 = float(request.form['q2'])

        try:
            graphJSON = create_plot(model, gpd_model, xbj, t, q2)

            if form.download.data:
                return redirect('/download/gpd_model.csv')

            else:
                return render_template('result.html', title='Result', form=form, graphJSON=graphJSON)

        except:
            return "Error"

    else:
        return render_template('index.html', title='Home', form=form)

@app.route('/<model>/<gpd>')
def params(model=None, gpd=None):
    df = fm.FemtoMesh('data/models/model_{0}/{1}.csv'.format(model, gpd)).open()

    kinematics_array = []

    for (xbj, t, q2) in list(itertools.zip_longest(df.xbj.unique(), df.t.unique(), df.Q2.unique())):
        kinematics = {}
        if xbj is not None:
            kinematics['xbj'] = xbj
        if t is not None:
            kinematics['t'] = t
        if q2 is not None:
            kinematics['q2'] = q2

        kinematics_array.append(kinematics)

    return jsonify({'kinematics': kinematics_array})




@app.route('/result')
def result():
    return render_template('result.html', title='Result')


@app.route('/download/<filename>')
def download(filename):
    path = os.path.join('download', filename)

    def generate():
        with open(path) as f:
            yield from f
        os.remove(path)

    resp = Response(generate(), mimetype='text/csv')
    resp.headers.set('Content-Disposition', 'attachment', filename='gpd_model.csv')
    return resp


@app.route('/help')
def help():
    return render_template('help.html', title='Help')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')
