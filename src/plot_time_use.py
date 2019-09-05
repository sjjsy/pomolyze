#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# For documentation and other information (including about licensing),
# read the README at the project root.

import bokeh as bo
import bokeh.plotting as boplot
import pandas as pd

def plot_time_use_by_time_period(df, by='M'):
  """Plot a vertical bar plot of time use by month or week"""
  bywk = by == 'W'
  # Prepare the data frame
  dfb = df['Seconds'].resample(by, label='left').sum()
  # ~ print(dfb.head())
  # ~ print('Totals: %s' % (dfb.values))
  # ~ print(dfb.describe())

  lbl_full = dfb.index.strftime('%Y-W%W' if bywk else '%Y-%m')
  if bywk:
    lbl_hier = [(str(dt.year), '%02d' % (dt.week)) for dt in dfb.index]
  else:
    lbl_hier = [(str(dt.year), '%02d' % (dt.month)) for dt in dfb.index]

  # Define the data source
  dsrc = bo.models.ColumnDataSource(data={
    'lbl': lbl_hier,
    'tdu': (dfb.values / 3600),
    # ~ 'lbl': ['2019-01', '2019-02', '2019-03', '2019-04'], #dfm.index.strftime('%Y-%m'), # %Y-%W
    # ~ 'tdu': [1, 2, 3, 4], # dfm.values,
  })

  # ~ print(dsrc)
  # ~ print(dsrc.data['lbl'])
  # ~ print(dsrc.data['tdu'])

  # Define the hover tool
  thvr = bo.models.HoverTool(mode='vline', line_policy='nearest', names=['b1'], tooltips=[('week' if bywk else 'month', "@lbl"), ("time use", "@tdu{0.0}")])

  # Define the color palette
  colpal = bo.palettes.d3['Category10'][10]

  # Define the figure and plot
  p = boplot.figure(x_range=bo.models.FactorRange(*dsrc.data['lbl']), plot_width=740, plot_height=300, toolbar_location=None, tools=[thvr])
  #p.line(x='smon', y='tdu', line_color=colpal[0], line_width=3, source=source, name='l1', legend=None)
  p.vbar(x='lbl', bottom=0, top='tdu', width=0.9, fill_color=colpal[0], fill_alpha=0.8, source=dsrc, name='b1', legend=None)

  # Define the labels
  p.xaxis.axis_label = 'Week' if bywk else 'Month'
  p.yaxis.axis_label = 'Time use (hours)'
  #p.xaxis.major_label_orientation = 1

  return p

def plot_time_use_by_activity(df, by='C', zlbl=14, zheight=740):
  """Plot on overview of total time use by activity"""
  # Prepare the data frame
  dfb = df[['Seconds', 'ActivityPath']]
  dfb = dfb.groupby(['ActivityPath']).sum()
  # ~ print('dfb: %s' % (dfb))
  # ~ print('dfb.index: %s' % (dfb.index))

  ## Remove shared root path
  vsap = dfb.index[0].split('/')
  #print('vsap: %s' % (vsap))
  while len(vsap) > 1:
    vsap = vsap[:-1]
    sap = '/'.join(vsap) + '/'
    #print('sap: %s --> %s' % (sap, dfb.index.str.startswith(sap)))
    if all(dfb.index.str.startswith(sap)):
      dfb.index = dfb.index.str.replace(sap, '', regex=False)
      break
  print('dfb: %s' % (dfb))

  ## Define a hierarchical index
  dfb.index = dfb.index.str.replace(r'^(\w+/\w+)/.*', r'\1')
  dfb = dfb.groupby(dfb.index).sum()
  vvsact = [sact.split('/')[0:2] for sact in dfb.index.values]
  vvslbl = [(vsact[0], vsact[1] if len(vsact) > 1 else '*') for vsact in vvsact]
  dfb.index = pd.MultiIndex.from_tuples(vvslbl, names=['Category', 'Group'])
  dfb.sort_values(by=['Category', 'Seconds', 'Group'], inplace=True)
  print('dfb: %s' % (dfb))

  ## Group by category while limiting the maximum number
  dfc = dfb.groupby(level=['Category']).sum()
  dfc.sort_values(by=['Seconds', 'Category'], inplace=True)
  btailed = len(dfc.index) > zlbl
  if btailed:
    dfc.loc['(other)'] = dfc[0:len(dfc.index)-zlbl].sum()
    dfc = pd.concat([dfc.iloc[[-1],:], dfc[-(zlbl+1):-1]], axis=0)

  if by == 'C':
    dfx = dfc
  elif by == 'G':
    ## Group by group
    vscat = [scat for scat in dfc.index] # index[btailed:]
    dfd = dfb.loc[dfb.index.get_level_values('Category').isin(vscat)]
    if btailed:
      dfd.loc[('(other)', '*'), 'Seconds'] = dfc.loc['(other)', 'Seconds']
    dfd['Rank'] = 0
    for i, scat in enumerate(vscat):
      dfd.loc[scat]['Rank'] = (i*1000)
    #dfd = dfd.loc[(slice(None), slice('*'))]['Rank'] -= 1
    #print(dfd.loc[(slice(None), '*')])
    # ~ print(dfd.loc[('supervision', '*')])
    # ~ df.loc[:, ['B', 'A']] = df[['A', 'B']].to_numpy()
    # ~ print(dfd[[(slice(None), '*')]])
    #dfd.loc(axis=0)[(slice(None), '*'), 'Rank'] = dfd.loc(axis=0)[(slice(None), '*'), 'Rank'] - 1
    #print(dfd.loc(axis=0)[:, '*']['Rank'])
    dfd.sort_values(by=['Rank', 'Seconds', 'Group'], inplace=True)
    dfx = dfd
  elif by == 'M':
    dfe = df[['Seconds', 'ActivityPath']]
    dfe = dfe.groupby(['ActivityPath']).sum()
    dfe.sort_values(by=['Seconds', 'ActivityPath'], inplace=True)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
      print('dfe: %s' % (dfe))
    btailed = len(dfc.index) > zlbl
    if btailed:
      dfe.loc['(other)'] = dfe[0:len(dfe.index)-zlbl].sum()
      dfe = pd.concat([dfe.iloc[[-1],:], dfe[-(zlbl+1):-1]], axis=0)
    dfx = dfe

  print('dfx: %s' % (dfx))

  # Define the data source
  dsrc = bo.models.ColumnDataSource(data={
    'lbl': dfx.index,
    'tdu': (dfx.Seconds.values / 3600),
  })

  # ~ print(dsrc)
  # ~ print(dsrc.data['lbl'])
  # ~ print(dsrc.data['tdu'])

  # Define the hover tool
  thvr = bo.models.HoverTool(mode='hline', line_policy='nearest', names=['b1'], tooltips=[('activity', '@lbl'), ('time use', '@tdu{0.0}')])

  # Define the color palette
  colpal = bo.palettes.d3['Category10'][10]

  # Define the figure and plot
  p = boplot.figure(y_range=bo.models.FactorRange(*dsrc.data['lbl']), plot_width=740, plot_height=zheight, toolbar_location=None, tools=[thvr])
  #p.line(x='smon', y='tdu', line_color=colpal[0], line_width=3, source=source, name='l1', legend=None)
  p.hbar(y='lbl', left=0, right='tdu', height=0.8, fill_color=colpal[0], fill_alpha=0.8, source=dsrc, name='b1', legend=None)

  # Define the labels
  p.yaxis.axis_label = 'Activity'
  p.xaxis.axis_label = 'Time use (hours)'

  p.yaxis.major_label_orientation = 0
  p.yaxis.major_label_text_align = 'right'
  # ~ p.yaxis.subgroup_label_orientation = 0.2
  # ~ p.yaxis.subgroup_text_baseline = 'top'
  p.yaxis.group_label_orientation = 0.7
  p.yaxis.group_text_align = 'left'
  p.yaxis.group_text_baseline = 'top'
  p.yaxis.separator_line_width = 0

  return p
