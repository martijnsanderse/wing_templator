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


chord = float(sys.argv[2])
template_height = 0.15 # normalized
template_lead_width = 0.15 # normalized


x_top = np.array(x[0:l/2])
y_top = np.array(y[0:l/2])+0.25

x_bot = np.array(x[l/2:])
y_bot = np.array(y[l/2:])+0.25

x_tem_top = np.array([x_top[0],
                    x_top[0]+template_lead_width,
                   x_top[0]+template_lead_width,
                   x_top[-1]-template_lead_width,
                   x_top[-1]-template_lead_width,
                   x_top[-1]])
y_tem_top = np.array([y_top[0],
                    y_top[0],
                  y_top[0]-template_height,
                  y_top[-1]-template_height,
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


# When drawing this in a picture here's how it goes:
# figuresize  (in inch) and dpi (in print_figure) determine 
# the size of the png
# All x,y coordinates are relative, ie. in the range [0,1]

figureSize = [chord, chord]
fig = Figure(figsize=figureSize, dpi=118)
#ax = Axes(fig, [.1,.1,.8,.8])
ax = Axes(fig, [0,0,1,1]) # axes run from 0% of the image size to 100%. Ie. no border.
ax.set_autoscale_on(False)
fig.add_axes(ax)

#l = Line2D([0,1],[0,1])
#ax.add_line(l)
ax.plot(x_top,y_top)
ax.plot(x_bot,y_bot)

canvas = FigureCanvasAgg(fig)
canvas.print_figure("line_ex.png", dpi=118  )


# plt.plot(x_top, y_top)
# plt.plot(x_tem_top, y_tem_top)
# plt.axis('equal')
# plt.savefig("bottom.pdf")

#plt.show()