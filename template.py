import sys # for argv
from scipy import interpolate
import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.backends.backend_agg import FigureCanvasAgg

filename = sys.argv[1]
with open(filename, "rb") as f:
    lines = f.readlines()

print "Airfoil: ", lines[0]
coordinates = [[float(coordinate) for coordinate in line.split()] for line in lines[1:]]

l = len(coordinates)
x, y = zip(*coordinates)

template_height = 0.15 # normalized
template_lead_width = 0.15 # normalized

chord_relative = (1 - 2*template_lead_width)
chord = float(sys.argv[2]) / chord_relative


# When drawing these airfoils in a picture here's how it goes:
# figuresize  (in inch) and dpi (in print_figure) determine
# the size of the png
# All x,y coordinates are relative, ie. in the range [0,1]

# so we want a chord size specified in  sys.argv[2]

# total width = 2* template_lead_width + chord
#

x_top = np.array(x[0:l/2]) * chord_relative + template_lead_width
y_top = np.array(y[0:l/2]) * chord_relative + 0.75

x_reference = np.array(x) * chord_relative + template_lead_width
y_reference = np.array(y) * chord_relative + 0.5

x_bot = np.array(x[l/2:]) * chord_relative + template_lead_width
y_bot = np.array(y[l/2:]) * chord_relative + 0.25

x_tem_top = np.array([x_top[0],
                    x_top[0]+template_lead_width,
                   x_top[0]+template_lead_width,
                   x_top[-1]-template_lead_width,
                   x_top[-1]-template_lead_width,
                   x_top[-1]])
y_tem_top = np.array([y_top[0],
                    y_top[0],
                  y_top[0] - template_height,
                  y_top[-1] - template_height,
                  y_top[-1],
                  y_top[-1]])

x_tem_bot = np.array([x_bot[-1],
                    x_bot[-1]+template_lead_width,
                   x_bot[-1]+template_lead_width,
                   x_bot[0]-template_lead_width,
                   x_bot[0]-template_lead_width,
                   x_bot[0]])
y_tem_bot = np.array([y_bot[-1],
                    y_bot[-1],
                  y_bot[-1]-template_height,
                  y_bot[0]-template_height,
                  y_bot[0],
                  y_bot[0]])


fig = Figure(figsize=[chord, chord], dpi=300)
#ax = Axes(fig, [.1,.1,.8,.8])
ax = Axes(fig, [0,0,1,1])
ax.set_autoscale_on(False)
fig.add_axes(ax)

ax.plot(x_top,y_top)
ax.plot(x_tem_top,y_tem_top)

ax.plot(x_bot, y_bot)
ax.plot(x_tem_bot, y_tem_bot)

ax.plot(x_reference, y_reference)

canvas = FigureCanvasAgg(fig)
canvas.print_figure("line_ex.png", dpi=300)
