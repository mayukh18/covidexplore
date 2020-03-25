import os

import pandas as pd
import json
import numpy as np

from bokeh.embed import components
from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool, CustomJS, ColumnDataSource, Button, Text
from bokeh.embed import json_item
from bokeh.layouts import widgetbox, row, column
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer, mpl
import geopandas as gpd

from callbacks import get_callback


shapefile = 'data/countries_110m/ne_110m_admin_0_countries.shp'
datafile = 'data/aqi_df.csv'

replacements = {'UK':'United Kingdom',
               'USA':'United States of America',
               'Serbia':'Republic of Serbia',
               'Czech Republic':'Czechia'}

gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
gdf.columns = ['country', 'country_code', 'geometry']

gdf = gdf.drop(gdf.index[159]) # Antarctica
gdf.head()

data = pd.read_csv(datafile)
tmp = []
for x in data['NO2']:
    if np.isnan(x):
        tmp.append(x)
    else:
        tmp.append(int(x))
data['NO2'] = tmp

tmp = []
for x in data['PM2.5']:
    if np.isnan(x):
        tmp.append(x)
    else:
        tmp.append(int(x))
data['PM2.5'] = tmp

for c in replacements:
    data['country'].replace(c, replacements[c], inplace=True)
print(data.head())

def get_NO2_plot():
    merged_df = gdf.merge(data, on='country', how='left')
    merged_df['week'].fillna(-1, inplace=True)
    merged_df['NO2'].fillna("No Data", inplace=True)
    merged_df['PM2.5'].fillna("No Data", inplace=True)

    def json_data(selectedWeek):
        week = selectedWeek
        merged = merged_df[(merged_df['week'] == week) | (merged_df['week'] == -1)]
        print(merged)
        merged_json = json.loads(merged.to_json())
        json_data = json.dumps(merged_json)
        return json_data

    # Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson=json_data(0))

    # Define a sequential multi-hue color palette.
    palette = mpl['Magma'][256]

    # Reverse color order so that dark blue is highest obesity.
    palette = palette[::-1]

    # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
    color_mapper = LinearColorMapper(palette=palette, low=0, high=np.max(data['NO2']), nan_color='#d9d9d9')


    # Add hover tool
    hover = HoverTool(tooltips=[('Country/region', '@country'), ('NO2', '@NO2')], callback=get_callback('hover_cursor'))

    # Create color bar.
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=20, height=500,
                         border_line_color=None, location=(0, 0), orientation='vertical')

    # Create figure object.
    p = figure(title='NO2 concentration from the start of year 2020', plot_height=550, plot_width=1100,
               toolbar_location=None,
               tools=[hover])
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False

    # Add patch renderer to figure.
    p.patches('xs', 'ys', source=geosource, fill_color={'field': 'NO2', 'transform': color_mapper},
              line_color='black', line_width=0.25, fill_alpha=1)


    #x = [-170]
    #y = [-50]
    #s = ["100pt"]
    #a = "sample"
    #text = [a]
    #source = ColumnDataSource(dict(x=x, y=y, text=text, size=s))
    #glyph = Text(x="x", y="y", text="text", text_font_size="size", angle=0, text_color="#96deb3")
    #p.add_glyph(source, glyph)


    p.add_layout(color_bar, 'right')

    Overall = ColumnDataSource(data)
    Curr = ColumnDataSource(data[data['week'] == 0])

    callback = get_callback('NO2_slider', [Overall, Curr])

    animate = get_callback('climate_play_button')

    # Make a slider object: slider
    slider = Slider(title='Week', start=0, end=11, step=1, value=0, orientation="horizontal", width=505)
    slider.js_on_change('value', callback)
    callback.args["slider"] = slider
    callback.args["map"] = p

    button = Button(label='► Play', width=505)
    button.js_on_click(animate)
    animate.args['button'] = button
    animate.args['slider'] = slider

    row2 = row(widgetbox(slider), widgetbox(button))
    layout = column(p, row2)
    curdoc().add_root(layout)
    script, div = components(layout)
    return script, div


def get_PM25_plot():
    merged_df = gdf.merge(data, on='country', how='left')
    merged_df['week'].fillna(-1, inplace=True)
    merged_df['NO2'].fillna("No Data", inplace=True)
    merged_df['PM2.5'].fillna("No Data", inplace=True)

    def json_data(selectedWeek):
        week = selectedWeek
        merged = merged_df[(merged_df['week'] == week) | (merged_df['week'] == -1)]
        print(merged)
        merged_json = json.loads(merged.to_json())
        json_data = json.dumps(merged_json)
        return json_data

    # Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson=json_data(0))

    # Define a sequential multi-hue color palette.
    palette = mpl['Magma'][256]

    # Reverse color order so that dark blue is highest obesity.
    palette = palette[::-1]

    # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
    color_mapper = LinearColorMapper(palette=palette, low=0, high=np.max(data['PM2.5']), nan_color='#d9d9d9')

    # Add hover tool
    hover = HoverTool(tooltips=[('Country/region', '@country'), ('PM2.5', '@PM2.5')], callback=get_callback('hover_cursor'))

    # Create color bar.
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=20, height=500,
                         border_line_color=None, location=(0, 0), orientation='vertical')

    # Create figure object.
    p = figure(title='PM2.5 concentration from the start of year 2020', plot_height=550, plot_width=1100,
               toolbar_location=None,
               tools=[hover])
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False

    # Add patch renderer to figure.
    p.patches('xs', 'ys', source=geosource, fill_color={'field': 'PM2.5', 'transform': color_mapper},
              line_color='black', line_width=0.25, fill_alpha=1)

    p.add_layout(color_bar, 'right')

    Overall = ColumnDataSource(data)
    Curr = ColumnDataSource(data[data['week'] == 0])

    callback = get_callback('PM25_slider', [Overall, Curr])

    animate = get_callback('climate_play_button')

    # Make a slider object: slider
    slider = Slider(title='Week', start=0, end=11, step=1, value=0, orientation="horizontal", width=505)
    slider.js_on_change('value', callback)
    callback.args["slider"] = slider
    callback.args["map"] = p

    button = Button(label='► Play', width=505)
    button.js_on_click(animate)
    animate.args['button'] = button
    animate.args['slider'] = slider

    row2 = row(widgetbox(slider), widgetbox(button))
    layout = column(p, row2)
    curdoc().add_root(layout)
    script, div = components(layout)
    return script, div
