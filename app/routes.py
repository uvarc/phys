from flask import request, render_template, flash, redirect, url_for, Response
import os
import plotly
import plotly.graph_objects as go
from form import Form
from app import app
from mesh import create_plot

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    if request.method == 'POST' and form.validate_on_submit():
        model = request.form['model']
        gpd_model = request.form['gpd_model']
        xbj = float(request.form['xbj'])
        t   = float(request.form['t'])
        q2  = float(request.form['q2'])

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
