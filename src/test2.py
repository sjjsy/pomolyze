#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# For documentation and other information (including about licensing),
# read the README at the project root.

from collections import OrderedDict

import pandas as pd

from bokeh.charts import Donut, show, output_file
from bokeh.sampledata.olympics2014 import data
from bokeh.io import export_png

# throw the data into a pandas data frame
df = pd.io.json.json_normalize(data['data'])

# filter by countries with at least one medal and sort
df = df[df['medals.total'] > 8]
df = df.sort("medals.total", ascending=False)

# get the countries and we group the data by medal type
countries = df.abbr.values.tolist()
gold = df['medals.gold'].astype(float).values
silver = df['medals.silver'].astype(float).values
bronze = df['medals.bronze'].astype(float).values

# build a dict containing the grouped data
medals = OrderedDict()
medals['bronze'] = bronze
medals['silver'] = silver
medals['gold'] = gold

# any of the following commented are also valid Donut inputs
#medals = list(medals.values())
#medals = np.array(list(medals.values()))
#medals = pd.DataFrame(medals)

output_file("./out/test2.html")

donut = Donut(medals, countries)

show(donut)

# Export the figure
export_png(p, filename="./out/test2.png")

# EOF
