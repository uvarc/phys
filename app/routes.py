from flask import request, render_template, flash, redirect, url_for
from form import Form
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    if request.method == 'POST':
        csv = request.form['csv']
        xbj = request.form['xbj']
        t   = request.form['t']
        q2  = request.form['q2']

        try:
            #Render(csv=csv, xbj=xbj, t=t, q2=q2)
            return render_template('index.html', title='Home')
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
