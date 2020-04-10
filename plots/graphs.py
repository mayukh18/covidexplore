from bokeh.plotting import figure, output_file, show
from bokeh.models import Slider, HoverTool, TapTool, CustomJS, ColumnDataSource, Range1d, Band
from callbacks import get_callback

def get_graph(df, field, op, title):
    g = figure(plot_width=420, plot_height=220, outline_line_color='white', outline_line_alpha=0, background='black',
               border_fill_color='black')

    g.y_range.range_padding = 0.8
    g.margin = (50, 0, 0, 0)

    g.xaxis.axis_label = title

    g.background_fill_color = "black"
    g.background_fill_alpha = 0.0
    g.title.text_color = "grey"
    g.title.text_font_style = "italic"


    g.xgrid.grid_line_color = 'grey'
    g.ygrid.grid_line_color = 'grey'
    g.xgrid.grid_line_alpha = 0.3
    g.ygrid.grid_line_alpha = 0.3
    g.axis.visible = True
    g.toolbar_location = None

    # add a line renderer
    grpdf = df.groupby('week')[[field]]

    if op == "mean":
        df = grpdf.mean().reset_index()
    elif op == "sum":
        df = grpdf.sum().reset_index()

    df[field+"_W"] = df[field]
    print(df)
    CurrC = ColumnDataSource(df)
    print(CurrC.data)

    g.line('week', field, source=CurrC, line_width=2, alpha=1.0, color='blue')
    g.circle('week', field, source=CurrC)

    hover = HoverTool(tooltips=[('Week', '@week'), ('Counts', '@count_true')],
                      callback=get_callback('hover_cursor'))
    g.tools = [hover]

    return g, CurrC
