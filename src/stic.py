#!/usr/bin/env python
# coding: utf-8

#import holoviews as hv
import pandas as pd
#import numpy as np
#import datashader as ds
#import dask as dk
#import geoviews as gv
import bokeh as bo
import bokeh.io as boio
import bokeh.plotting as boplot

from plot_time_use import plot_time_use_by_time_period, plot_time_use_by_activity
#from bokeh.io import show, save, output_file, export_png
#from bokeh.models import ColumnDataSource, FactorRange
#from bokeh.plotting import figure
#from bokeh.resources import CDN
#from io import StringIO, BytesIO

### Load the data

# Read the data and setup the DatetimeIndex
df = pd.read_csv('./data/stic3.csv', delimiter='\t', dtype={'Timestamp': 'int', 'Seconds': 'float', 'Activity': 'str'})
# Note: the data was created with the command:
#   zos pon xcsv stic3.csv 2018-09-01--2019-08-01 '^stic/'
df['DTUTC'] = pd.to_datetime(df["Timestamp"], unit='s', utc=True)
df.set_index('DTUTC', inplace=True)

# Add the week column
df['Week'] = df.index.week

# Add the activity path column
df['ActivityPath'] = df['Activity'].replace(r'(\w+):.*', r'\1', regex=True)

print(df.index)
print(df.head())

### Vertical bar plots of time use by month

boio.output_file('./out/smoti_time_use_by_month.html')
p = plot_time_use_by_time_period(df, by='M')
boio.export_png(p, filename="./out/smoti_time_use_by_month.png")
boio.save(p)
boplot.reset_output()

boio.output_file('./out/smoti_time_use_by_week.html')
p = plot_time_use_by_time_period(df, by='W')
boio.export_png(p, filename="./out/smoti_time_use_by_week.png")
boio.save(p)
boplot.reset_output()

### Plots of time use by activity

boio.output_file('./out/smoti_time_use_by_activity_category.html')
p = plot_time_use_by_activity(df, by='C', zlbl=14, zheight=350)
boio.export_png(p, filename="./out/smoti_time_use_by_activity_category.png")
boio.save(p)
boplot.reset_output()

boio.output_file('./out/smoti_time_use_by_activity_group.html')
p = plot_time_use_by_activity(df, by='G', zlbl=14)
boio.export_png(p, filename="./out/smoti_time_use_by_activity_group.png")
boio.save(p)
boplot.reset_output()

boio.output_file('./out/smoti_time_use_by_activity_path.html')
p = plot_time_use_by_activity(df, by='M', zlbl=30)
boio.export_png(p, filename="./out/smoti_time_use_by_activity_path.png")
boio.save(p)
boplot.reset_output()
