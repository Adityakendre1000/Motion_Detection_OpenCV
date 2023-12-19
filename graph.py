# Importing necessary libraries
from motion_detector import df  # Importing the DataFrame from the motion_detector script
from bokeh.plotting import figure, output_file, show  # Importing Bokeh plotting tools
from bokeh.models import HoverTool, ColumnDataSource  # Importing Bokeh models
import pandas  # Importing pandas library

# Creating a Bokeh ColumnDataSource from the DataFrame
cds = ColumnDataSource(df)

# Creating a Bokeh figure for the motion graph
g = figure(x_axis_type='datetime', height=300, width=1500, sizing_mode="scale_both", title="Motion Graph")
g.yaxis.minor_tick_line_color = None
g.yaxis[0].ticker.desired_num_ticks = 1
g.yaxis.visible = False

# Adding a HoverTool to display detailed information on the graph
hover = HoverTool(tooltips=[("Start: ", "@Start{%d/%m/%Y %H:%M:%S}"), ("End: ", "@End{%d/%m/%Y %H:%M:%S}")],
                  formatters={"@Start": "datetime", "@End": "datetime"})

g.add_tools(hover)  # Adding the hover tool to the figure

# Creating a quad glyph to represent the motion intervals on the graph
q = g.quad(left="Start", right="End", bottom=0, top=1, color="green", source=cds)

# Setting the output file for the motion graph
output_file("Motion graph.html")

# Displaying the graph
show(g)
