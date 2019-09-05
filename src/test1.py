#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# For documentation and other information (including about licensing),
# read the README at the project root.

from bokeh.plotting import figure, output_file, show
from bokeh.io import export_png

output_file('./out/test1.html')

x = [1, 3, 5, 7]
y = [2, 4, 6, 8]

p = figure()

p.circle(x, y, size=10, color='red', legend='circle')
p.line(x, y, color='blue', legend='line')
p.triangle(y, x, color='gold', size=10, legend='triangle')

p.legend.click_policy='hide'

show(p)

# Export the figure
export_png(p, filename="./out/test1.png")

# EOF
