from flask import Flask, render_template, request
import pandas as pd
import json
import numpy as np
from plots.climate import get_PM25_plot, get_NO2_plot

app = Flask(__name__)


# Home page
@app.route('/')
def home():
    return render_template("index.html")

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
    app.run(port=5000, debug=True)