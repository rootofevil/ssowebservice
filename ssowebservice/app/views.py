from app import app
from flask import render_template, flash, redirect

@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')
