from flask import request, render_template, flash, redirect, url_for
import plotly
import plotly.graph_objects as go
from form import Form
from app import app
from mesh import create_plot
import femtomesh
import pandas

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
            graphJSON, df = create_plot(model, gpd_model, xbj, t, q2)
            if form.download.data:
                resp = make_response(df.to_csv('gpd_model.csv', index=False, header=['x', 'u', 'd', 'xu', 'xd']))
                resp.headers["Content-Disposition"] = "attachment; filename='gpd_model.csv'"
                resp.headers["Content-Type"] = "text/csv"
                print(resp)
                return resp
            else:
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
