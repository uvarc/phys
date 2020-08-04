from flask import request, render_template, flash, redirect, url_for
import plotly
import plotly.graph_objects as go
import json
from form import Form
from app import app
from mesh import create_plot

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    if request.method == 'POST':
        model = request.form['model']
        xbj = float(request.form['xbj'])
        t   = float(request.form['t'])
        q2  = float(request.form['q2'])

        try:
            graphJSON = create_plot(model, xbj, t, q2)
            return render_template('result.html', title='Result', form=form, graphJSON=graphJSON)

        except:
            return "Error"

    else:
        return render_template('index.html', title='Home', form=form)

@app.route('/result')
def result():
    return render_template('result.html', title='Result')

@app.route('/help')
def help():
    return render_template('help.html', title='Help')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')
