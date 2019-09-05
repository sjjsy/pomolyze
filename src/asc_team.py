#!/usr/bin/env python
# coding: utf-8

# In[63]:


import holoviews as hv
import pandas as pd
import numpy as np
import datashader as ds
import dask as dk
import geoviews as gv
import bokeh as bo
hv.__version__


# In[64]:


from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.resources import CDN
from io import StringIO, BytesIO


# In[77]:


output_file('../../_includes/bokeh/time_use_by_team.html')


# In[78]:


df_time_use_by_team = pd.read_csv(StringIO("""
Semester,Team,Hours
2016-17,MDI,56.1
2016-17,Ruka,41.2
2016-17,Other,52.8
2017-18,CGI,38.2
2017-18,Verto,39.7
2017-18,Other,67.9
2018-19,Accountor,34.9
2018-19,Elisa,39.4
2018-19,Vainu,45.7
2018-19,Other,51.8"""))
df_time_use_by_team.head()


# In[79]:


x = [(semester, team) for (semester, team) in df_time_use_by_team[['Semester', 'Team']].values.tolist()]


# In[91]:


colpal = bo.palettes.d3['Category10'][10]
source = ColumnDataSource(data=dict(x=x, hours=df_time_use_by_team['Hours']))
p = figure(x_range=FactorRange(*x), plot_width=740, plot_height=300, toolbar_location=None, tools='hover', 
tooltips=[("hours", "@hours{0.0}"),])
p.vbar(x='x', top='hours', width=0.9, source=source, color=colpal[0])
p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None
p.yaxis.axis_label = 'Time use (h)'
show(p)


# In[ ]:




