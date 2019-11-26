from motion_detection import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df['Start_string'] = df['Start'].dt.strftime('%d-%m-%Y %H:%m:%s')
df['End_string'] = df['End'].dt.strftime('%d-%m-%Y %H:%m:%s')

x = ColumnDataSource(df)

p = figure(x_axis_type = 'datetime', height=100, width=500, sizing_mode='scale_both', title="Object Detection Graph")
hover  = HoverTool(tooltips=[('Start','@Start_string'),('End','@End_string')])
p.add_tools(hover)
q = p.quad(left="Start", right="End", bottom=0, top=1, color="teal", source=x)

output_file("Graph.html")
show(p)
