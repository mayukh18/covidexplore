from bokeh.plotting import figure, output_file, show
from bokeh.models import Slider, HoverTool, TapTool, CustomJS, ColumnDataSource, Range1d


def get_graph(df, field, op):
    g = figure(plot_width=400, plot_height=200, outline_line_color='white', outline_line_alpha=0, background='black',
               border_fill_color='black')

    g.y_range.range_padding = 0.8
    g.margin = (50, 0, 0, 0)


    g.background_fill_color = "black"
    g.background_fill_alpha = 0.0
    g.xgrid.grid_line_color = 'grey'
    g.ygrid.grid_line_color = 'grey'
    g.xgrid.grid_line_alpha = 0.2
    g.ygrid.grid_line_alpha = 0.2
    g.axis.visible = True
    g.toolbar_location = None

    # add a line renderer
    grpdf = df.groupby('week')[[field]]\

    if op == "mean":
        df = grpdf.mean().reset_index()
    elif op == "sum":
        df = grpdf.sum().reset_index()

    df[field+"_W"] = df[field]
    print(df)
    CurrC = ColumnDataSource(df)


    g.line('week', field, source=CurrC, line_width=2, alpha=1.0, color='blue')
    return g, CurrC
