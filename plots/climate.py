import os

import pandas as pd
import json
import numpy as np

from bokeh.embed import components
from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool, TapTool, CustomJS, ColumnDataSource, Button, Text
from bokeh.embed import json_item
from bokeh.layouts import widgetbox, row, column
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer, mpl
import geopandas as gpd

from callbacks import get_callback
from .graphs import get_graph


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
data['PM25'] = tmp

for c in replacements:
    data['country'].replace(c, replacements[c], inplace=True)
print(data.head())

def get_NO2_plot():
    merged_df = gdf.merge(data, on='country', how='left')
    merged_df['week'].fillna(-1, inplace=True)
    merged_df['NO2'].fillna("No Data", inplace=True)
    merged_df['PM25'].fillna("No Data", inplace=True)

    # get the line plot
    climate_graph, CurrC = get_graph(data, field="NO2", op="mean")

    def json_data(selectedWeek):
        week = selectedWeek
        merged = merged_df[(merged_df['week'] == week) | (merged_df['week'] == -1)]
        print(merged)
        merged_json = json.loads(merged.to_json())
        json_data = json.dumps(merged_json)
        return json_data

    # Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson=json_data(1))

    Overall = ColumnDataSource(data)
    Curr = ColumnDataSource(data[data['week'] == 1])

    # Define a sequential multi-hue color palette.
    palette = brewer['Reds'][256]
    palette = palette[::-1]

    # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
    color_mapper = LinearColorMapper(palette=palette, low=0, high=np.max(data['NO2'])*0.5, nan_color='#d9d9d9')

    # Create color bar.
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=5, width=15, height=200,
                         border_line_color='black', location=(100, 10), orientation='vertical',
                         major_label_text_align='left', major_label_text_color="white",
                         background_fill_alpha=0, border_line_alpha=0)


    # Create figure object.
    p = figure(plot_height=530, plot_width=1100,
               toolbar_location=None, outline_line_color='white', outline_line_alpha = 0, background='black',
               border_fill_color='black')

    p.add_layout(color_bar, 'left')
    p.background_fill_color = "black"
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False

    # Add patch renderer to figure.
    p.patches('xs', 'ys', source=geosource, fill_color={'field': 'NO2', 'transform': color_mapper},
                    line_color='black', line_width=0.25, fill_alpha=1,
                    nonselection_fill_alpha=0.8,
                    nonselection_fill_color="#1c1c1c",
                    nonselection_line_color="#1c1c1c",
                    nonselection_line_alpha=0.2 )

    # Add hover tool
    hover = HoverTool(tooltips=[('Country/region', '@country'), ('NO2', '@NO2')], callback=get_callback('hover_cursor'))

    # Add Tap tool
    tap_cb = get_callback('tap_climate', args=[Overall, CurrC])
    tap = TapTool(callback=tap_cb)
    tap_cb.args["graph"] = climate_graph
    tap_cb.args["field_name"] = "NO2"

    # add tools to figure
    p.tools = [hover, tap]


    # slider object
    slider = Slider(title='Week', bar_color='white', start=1, end=max(merged_df['week']), step=1, value=1, margin=(0,0,0,250), orientation="horizontal", width=300)
    callback = get_callback('NO2_slider', [Overall, Curr])
    slider.js_on_change('value', callback)
    callback.args["slider"] = slider
    callback.args["map"] = p

    # play button
    button = Button(label='► Play', width=300, margin=(12,0,0,20))
    animate = get_callback('climate_play_button')
    animate.args['button'] = button
    animate.args['slider'] = slider
    animate.args['max_week'] = max(data['week'])
    button.js_on_click(animate)

    row2 = row(widgetbox(slider), widgetbox(button))
    layout = column(p, row2)
    layout = row(layout, climate_graph)
    curdoc().add_root(layout)
    script, div = components(layout)

    return script, div


def get_PM25_plot():
    merged_df = gdf.merge(data, on='country', how='left')
    merged_df['week'].fillna(-1, inplace=True)
    merged_df['NO2'].fillna("No Data", inplace=True)
    merged_df['PM25'].fillna("No Data", inplace=True)

    # get the line plot
    climate_graph, CurrC = get_graph(data, field="PM25", op="mean")

    def json_data(selectedWeek):
        week = selectedWeek
        merged = merged_df[(merged_df['week'] == week) | (merged_df['week'] == -1)]
        print(merged)
        merged_json = json.loads(merged.to_json())
        json_data = json.dumps(merged_json)
        return json_data

    # Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson=json_data(1))

    Overall = ColumnDataSource(data)
    Curr = ColumnDataSource(data[data['week'] == 1])

    # Define a sequential multi-hue color palette.
    palette = brewer['Reds'][256]
    palette = palette[::-1]

    # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
    color_mapper = LinearColorMapper(palette=palette, low=0, high=np.max(data['PM25'])*0.8, nan_color='#d9d9d9')

    # Create color bar.
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=5, width=15, height=200,
                         border_line_color='black', location=(100, 10), orientation='vertical',
                         major_label_text_align='left', major_label_text_color="white",
                         background_fill_alpha=0, border_line_alpha=0)


    # Create figure object.
    p = figure(plot_height=530, plot_width=1100,
               toolbar_location=None, outline_line_color='white', outline_line_alpha = 0, background='black',
               border_fill_color='black')

    p.add_layout(color_bar, 'left')
    p.background_fill_color = "black"
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False

    # Add patch renderer to figure.
    p.patches('xs', 'ys', source=geosource, fill_color={'field': 'PM25', 'transform': color_mapper},
                    line_color='black', line_width=0.25, fill_alpha=1,
                    nonselection_fill_alpha=0.8,
                    nonselection_fill_color="#1c1c1c",
                    nonselection_line_color="#1c1c1c",
                    nonselection_line_alpha=0.2 )

    # Add hover tool
    hover = HoverTool(tooltips=[('Country/region', '@country'), ('PM25', '@PM25')], callback=get_callback('hover_cursor'))

    # Add Tap tool
    tap_cb = get_callback('tap_climate', args=[Overall, CurrC])
    tap = TapTool(callback=tap_cb)
    tap_cb.args["graph"] = climate_graph
    tap_cb.args["field_name"] = "PM25"

    # add tools to figure
    p.tools = [hover, tap]


    # slider object
    slider = Slider(title='Week', bar_color='white', start=1, end=max(merged_df['week']), step=1, value=1, margin=(0,0,0,250), orientation="horizontal", width=300)
    callback = get_callback('PM25_slider', [Overall, Curr])
    slider.js_on_change('value', callback)
    callback.args["slider"] = slider
    callback.args["map"] = p

    # play button
    button = Button(label='► Play', width=300, margin=(12,0,0,20))
    animate = get_callback('climate_play_button')
    animate.args['button'] = button
    animate.args['slider'] = slider
    animate.args['max_week'] = max(data['week'])
    button.js_on_click(animate)

    row2 = row(widgetbox(slider), widgetbox(button))
    layout = column(p, row2)
    layout = row(layout, climate_graph)
    curdoc().add_root(layout)
    script, div = components(layout)

    return script, div