from flask import Flask, render_template, request
import pandas as pd
import json
import numpy as np
from plots.climate import get_PM25_plot, get_NO2_plot
from plots.dark import get_cases_plot, get_deaths_plot

app = Flask(__name__)


# Home page
@app.route('/')
def home():
    return render_template("index.html")

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


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run()