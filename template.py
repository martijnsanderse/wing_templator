import sys # for argv
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt


filename = sys.argv[1]
with open(filename, "rb") as f:
    lines = f.readlines()

print "Airfoil: ", lines[0]
coordinates = [[float(coordinate) for coordinate in line.split()] for line in lines[1:]]

l = len(coordinates)
x, y = zip(*coordinates)

x_top = np.array(x[0:l/2+1])
y_top = np.array(y[0:l/2+1])

x_bot = np.array(x[l/2:])
y_bot = np.array(y[l/2:])

template_height = 0.1 # should become an absolute value after scaling
template_lead_width = 0.1 # idem
x_tem = np.array([x_top[0],
                    x_top[0]+template_lead_width, 
                   x_top[0]+template_lead_width,
                   x_top[-1]-template_lead_width,
                   x_top[-1]-template_lead_width,
                   x_top[-1]])
y_tem = np.array([y_top[0],
                    y_top[0],
                  y_top[0]-template_height,
                  y_top[-1]-template_height,
                  y_top[-1],
                  y_top[-1]])

print x_top[0], y_top[0]
print x_top[-1], y_top[-1]
print x_bot[0], y_bot[0]
print x_bot[-1], y_bot[-1]

plt.plot(x_bot, y_bot)
plt.plot(x_top, y_top)
plt.plot(x_tem, y_tem)
plt.axis('equal')
plt.show()