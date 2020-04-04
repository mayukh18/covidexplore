from flask import Flask, render_template, request, redirect

import pandas as pd
import json
import numpy as np
import argparse
from plots.climate import get_PM25_plot, get_NO2_plot
from plots.dark import get_cases_plot, get_deaths_plot

parser = argparse.ArgumentParser()
parser.add_argument("--host")
parser.add_argument("--port")

app = Flask(__name__)

"""
@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)
"""

# Home page
@app.route('/')
def home():
    print("=================== HEADER ============== ", request.headers["X-Forwarded-Proto"])
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/dark/cases')
def cases_confirmed():
    script, div = get_cases_plot()
    return render_template("dark.html", script=script, div=div, toggle=True)

@app.route('/dark/deaths')
def cases_deaths():
    script, div = get_deaths_plot()
    return render_template("dark.html", script=script, div=div, toggle=False)

# NO2 page
@app.route('/NO2')
def climate_no2():
    script, div = get_NO2_plot()
    return render_template("climate.html", script=script, div=div, toggle=False)

# PM25 page
@app.route('/PM25')
def climate_pm25():
    script, div = get_PM25_plot()
    return render_template("climate.html", script=script, div=div, toggle=True)


if __name__ == '__main__':
    args = parser.parse_args()
    #app.env = "development"
    #print(app.env)
    app.run(host=args.host, port=args.port)