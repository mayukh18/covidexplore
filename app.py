import os
import argparse

import json
import numpy as np
import pandas as pd

from flask import Flask, render_template, request, redirect
from flask_talisman import Talisman
from plots.climate import get_PM25_plot, get_NO2_plot, get_PM25_plot_diff, get_NO2_plot_diff
from plots.dark import get_cases_plot, get_deaths_plot
from plots.finance import get_finance_plot
import config

parser = argparse.ArgumentParser()
parser.add_argument("--host")
parser.add_argument("--port")

app = Flask(__name__)

talisman = Talisman(app, content_security_policy=None)


cases_data_update_date = os.environ.get('CASES_DATA_UPDATE_DATE', config.CASES_DATA_UPDATE_DATE)
climate_data_update_date = os.environ.get('CLIMATE_DATA_UPDATE_DATE', config.CLIMATE_DATA_UPDATE_DATE)

# Home page
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/dark/cases')
def cases_confirmed():
    script, div = get_cases_plot()
    return render_template("dark.html", script=script, div=div, date=cases_data_update_date, toggle=True)

@app.route('/dark/deaths')
def cases_deaths():
    script, div = get_deaths_plot()
    return render_template("dark.html", script=script, div=div, date=cases_data_update_date, toggle=False)

# NO2 page
@app.route('/NO2')
def climate_no2():
    script, div = get_NO2_plot()
    return render_template("climate.html", script=script, div=div, date=climate_data_update_date, toggle=1)

# PM25 page
@app.route('/PM25')
def climate_pm25():
    script, div = get_PM25_plot()
    return render_template("climate.html", script=script, div=div, date=climate_data_update_date, toggle=0)


# 2019 NO2 page
@app.route('/NO2_19')
def climate_no2_19():
    script, div = get_NO2_plot_diff()
    return render_template("climate.html", script=script, div=div, date=climate_data_update_date, toggle=3)


# 2019 PM25 page
@app.route('/PM25_19')
def climate_pm25_19():
    script, div = get_PM25_plot_diff()
    return render_template("climate.html", script=script, div=div, date=climate_data_update_date, toggle=2)

# 2019 NO2 page
@app.route('/finance')
def finance():
    script, div = get_finance_plot()
    return render_template("finance.html", script=script, div=div, date=climate_data_update_date, toggle=3)



if __name__ == '__main__':
    args = parser.parse_args()
    #app.run(debug=True)
    app.run(host=args.host, port=args.port)
