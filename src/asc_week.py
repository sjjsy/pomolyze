#!/usr/bin/env python
# coding: utf-8

# In[2]:


import holoviews as hv
import pandas as pd
import numpy as np
import datashader as ds
import dask as dk
import geoviews as gv
import bokeh as bo
hv.__version__


# In[3]:


from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.resources import CDN
from io import StringIO, BytesIO


# In[4]:


output_file('../../_includes/bokeh/time_use_by_week.html')


# In[9]:


df = pd.read_csv(StringIO("""
Week,2016-17,2017-18,2018-19
35,0.0,0.0,0.2
36,0.0,0.1,0.9
37,0.0,0.3,0.9
38,0.0,8.8,0.7
39,0.0,8.7,0.0
40,0.0,9.1,0.0
41,0.0,1.5,2.4
42,0.0,7.1,3.4
43,0.0,8.5,7.4
44,0.0,8.5,6.5
45,0.0,3.9,7.7
46,0.0,3.1,6.0
47,0.0,2.9,6.0
48,0.0,4.5,9.8
49,0.0,6.9,7.6
50,0.0,8.1,6.6
51,0.2,5.4,0.5
52,0.2,3.9,0.5
1,0.2,2.7,0.7
2,1.7,2.8,2.3
3,2.9,2.1,8.5
4,7.7,1.5,8.8
5,8.8,1.4,7.3
6,7.7,0.1,3.3
7,3.9,0.1,4.5
8,3.8,3.6,7.6
9,8.6,6.1,10.6
10,7.6,7.1,10.2
11,5.3,5.0,8.6
12,4.4,2.5,3.9
13,5.4,1.4,2.1
14,6.7,0.2,2.8
15,2.8,1.9,6.8
16,1.8,2.1,8.5
17,0.1,2.0,6.2
18,0.1,2.9,1.9
19,0.1,2.8,0.0
20,0.0,3.2,0.0
21,0.0,1.2,0.0
22,0.0,1.2,0.0
23,0.0,0.7,0.0"""), dtype={'Week': 'str'})
df.head()


# In[86]:


source = ColumnDataSource(data={
  'week': df['Week'],
  'h1': df['2016-17'],
  'h2': df['2017-18'],
  'h3': df['2018-19'],
})


# In[87]:


#hover = bo.models.HoverTool(mode='vline', line_policy='next', tooltips=[("Week", "@week"),
#    ("2016-17", "@h1{0.0}"), ("2017-18", "@h2{0.0}"), ("2018-19", "@h3{0.0}")])
hover1 = bo.models.HoverTool(mode='vline', line_policy='nearest', names=['h1'], tooltips=[("2016-17", "@h1{0.0}")])
hover2 = bo.models.HoverTool(mode='vline', line_policy='nearest', names=['h2'], tooltips=[("2017-18", "@h2{0.0}")])
hover3 = bo.models.HoverTool(mode='vline', line_policy='nearest', names=['h3'], tooltips=[("2018-19", "@h3{0.0}")])
colpal = bo.palettes.d3['Category10'][10]
p = figure(x_range=df['Week'], plot_width=740, plot_height=300, toolbar_location=None, tools=[hover1,hover2,hover3])
p.circle(x='week', y='h1', line_color=colpal[0], line_width=3, source=source)
p.circle(x='week', y='h2', line_color=colpal[1], line_width=3, source=source)
p.circle(x='week', y='h3', line_color=colpal[2], line_width=3, source=source)
p.line(x='week', y='h1', line_color=colpal[0], line_width=3, source=source, name='h1', legend='2016-17')
p.line(x='week', y='h2', line_color=colpal[1], line_width=3, source=source, name='h2', legend='2017-18')
p.line(x='week', y='h3', line_color=colpal[2], line_width=3, source=source, name='h3', legend='2018-19')
#p.multi_line(xs=['week','week','week'], ys=['h1','h2','h3'], line_width=3, color=colpal[0:3], source=source)
p.yaxis.axis_label = 'Time use (h/week)'
show(p)


# In[ ]:




