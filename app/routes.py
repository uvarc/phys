from flask import request, render_template, flash, redirect, url_for
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('index.html', title='Home')
    return render_template('index.html', title='Home')

@app.route('/result')
def result():
    return render_template('result.html', title='Contact')

@app.route('/help')
def help():
    return render_template('help.html', title='Contact')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')
