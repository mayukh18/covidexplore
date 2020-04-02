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
from bokeh.models import GeoJSONDataSource, LinearColorMapper, LogColorMapper, ColorBar
from bokeh.palettes import brewer, mpl
import geopandas as gpd

from callbacks import get_callback
from .graphs import get_graph


shapefile = 'data/countries_110m/ne_110m_admin_0_countries.shp'
datafile1 = 'data/cases_per_weeks_bokeh.csv'
datafile2 = 'data/deaths_per_weeks_bokeh.csv'

replacements = {'US':'United States of America',
               'Korea, South':'South Korea',
               'Taiwan*':'Taiwan',
               'Serbia': 'Republic of Serbia'}

gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
gdf.columns = ['country', 'country_code', 'geometry']

gdf = gdf.drop(gdf.index[159]) # Antarctica
gdf.head()

data1 = pd.read_csv(datafile1)
c = np.log10(data1['count'])
c[c == -np.inf] = 0
data1['count_true'] = data1['count']
data1['count'] = c

data2 = pd.read_csv(datafile2)
c = np.log10(data2['count'])
c[c == -np.inf] = 0
data2['count_true'] = data2['count']
data2['count'] = c


for c in replacements:
    data1['country'].replace(c, replacements[c], inplace=True)
    data2['country'].replace(c, replacements[c], inplace=True)


def get_cases_plot():
    merged_df = gdf.merge(data1, on='country', how='left')
    merged_df['week'].fillna(-1, inplace=True)

    # get the line plot
    dark_graph, CurrC = get_graph(data1, field="count_true", op="sum")

    def json_data(selectedWeek):
        week = selectedWeek
        merged = merged_df[(merged_df['week'] == week) | (merged_df['week'] == -1)]
        #print(merged)
        merged_json = json.loads(merged.to_json())
        json_data = json.dumps(merged_json)
        return json_data

    # Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson=json_data(4))

    Overall = ColumnDataSource(data1)
    Curr = ColumnDataSource(data1[data1['week'] == 4])

    # Define a sequential multi-hue color palette.
    palette = brewer['OrRd'][5]
    palette = palette[::-1]

    # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
    color_mapper = LinearColorMapper(palette=palette, low=0, high=5, nan_color='#d9d9d9')

    ticks = {'0':'0', '1':'10', '2':'100', '3':'1000', '4':'10000', '5':'100000'}

    # Create color bar.
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=5, width=15, height=200,
                         border_line_color='black', location=(100, 10), orientation='vertical',
                         major_label_text_align='left', major_label_text_color="white",
                         background_fill_alpha=0, border_line_alpha=0,
                         major_label_overrides=ticks)

    # Create figure object.
    p = figure(plot_height=530, plot_width=1100,
               toolbar_location=None, outline_line_color='white', outline_line_alpha = 0, background='black',
               border_fill_color='black')

    p.title.align = 'center'
    p.add_layout(color_bar, 'left')
    p.background_fill_color = "black"
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False

    # Add patch renderer to figure.
    p.patches('xs', 'ys', source=geosource, fill_color={'field': 'count', 'transform': color_mapper},
              line_color='black', line_width=0.25, fill_alpha=1,
              nonselection_fill_alpha=0.8,
              nonselection_fill_color="#1c1c1c",
              nonselection_line_color="#1c1c1c",
              nonselection_line_alpha=0.2)

    # Add hover tool
    hover = HoverTool(tooltips=[('Country', '@country'), ('cases', '@count_true')], callback=get_callback('hover_cursor'))

    # Add Tap tool
    tap_cb = get_callback('tap_dark', args=[Overall, CurrC])
    tap = TapTool(callback=tap_cb)
    tap_cb.args["graph"] = dark_graph
    tap_cb.args["field_name"] = "count_true"

    # add tools to figure
    p.tools = [hover, tap]


    # slider object
    slider = Slider(title='Week', start=4, end=max(data1['week']), step=1, value=4, margin=(0,0,0,250), orientation="horizontal", width=300)
    callback = get_callback('dark_slider', [Overall, Curr])
    slider.js_on_change('value', callback)
    callback.args["slider"] = slider
    callback.args["map"] = p

    # play button
    button = Button(label='► Play', width=300, margin=(12,0,0,20))
    animate = get_callback('dark_play_button')
    animate.args['button'] = button
    animate.args['slider'] = slider
    button.js_on_click(animate)

    row2 = row(widgetbox(slider), widgetbox(button))
    layout = column(p, row2)
    layout = row(layout, dark_graph)
    curdoc().add_root(layout)
    script, div = components(layout)

    return script, div


def get_deaths_plot():
    merged_df = gdf.merge(data2, on='country', how='left')
    merged_df['week'].fillna(-1, inplace=True)

    # get the line plot
    dark_graph, CurrC = get_graph(data2, field="count_true", op="sum")

    def json_data(selectedWeek):
        week = selectedWeek
        merged = merged_df[(merged_df['week'] == week) | (merged_df['week'] == -1)]
        print(merged)
        merged_json = json.loads(merged.to_json())
        json_data = json.dumps(merged_json)
        return json_data

    # Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson=json_data(4))

    Overall = ColumnDataSource(data2)
    Curr = ColumnDataSource(data2[data2['week'] == 4])

    # Define a sequential multi-hue color palette.
    palette = brewer['OrRd'][5]
    palette = palette[::-1]

    # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
    color_mapper = LinearColorMapper(palette=palette, low=0, high=5, nan_color='#d9d9d9')

    ticks = {'0':'0', '1':'10', '2':'100', '3':'1000', '4':'10000', '5':'100000'}

    # Create color bar.
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=5, width=15, height=200,
                         border_line_color='black', location=(100, 10), orientation='vertical',
                         major_label_text_align='left', major_label_text_color="white",
                         background_fill_alpha=0, border_line_alpha=0,
                         major_label_overrides=ticks)

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
    p.patches('xs', 'ys', source=geosource, fill_color={'field': 'count', 'transform': color_mapper},
              line_color='black', line_width=0.25, fill_alpha=1,
              nonselection_fill_alpha=0.8,
              nonselection_fill_color="#1c1c1c",
              nonselection_line_color="#1c1c1c",
              nonselection_line_alpha=0.2)

    # Add hover tool
    hover = HoverTool(tooltips=[('Country', '@country'), ('deaths', '@count_true')], callback=get_callback('hover_cursor'))

    # Add Tap tool
    tap_cb = get_callback('tap_dark', args=[Overall, CurrC])
    tap = TapTool(callback=tap_cb)
    tap_cb.args["graph"] = dark_graph
    tap_cb.args["field_name"] = "count_true"

    # add tools to figure
    p.tools = [hover, tap]


    # slider object
    slider = Slider(title='Week', start=4, end=max(data2['week']), step=1, value=4, margin=(0,0,0,250), orientation="horizontal", width=300)
    callback = get_callback('dark_slider', [Overall, Curr])
    slider.js_on_change('value', callback)
    callback.args["slider"] = slider
    callback.args["map"] = p

    # play button
    button = Button(label='► Play', width=300, margin=(12,0,0,20))
    animate = get_callback('dark_play_button')
    animate.args['button'] = button
    animate.args['slider'] = slider
    button.js_on_click(animate)

    row2 = row(widgetbox(slider), widgetbox(button))
    layout = column(p, row2)
    layout = row(layout, dark_graph)
    curdoc().add_root(layout)
    script, div = components(layout)

    return script, div
