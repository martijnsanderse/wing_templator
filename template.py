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

x_top = np.array(x[0:l/2])*float(sys.argv[2]) 
y_top = np.array(y[0:l/2])*float(sys.argv[2])

x_bot = np.array(x[l/2:])*float(sys.argv[2])
y_bot = np.array(y[l/2:])*float(sys.argv[2])

template_height = 20 # should become an absolute value after scaling
template_lead_width = 20 # idem

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


plt.subplot(211)
plt.plot(x_bot, y_bot)
plt.plot(x_tem_bot, y_tem_bot)
plt.axis('equal')

plt.subplot(212)
plt.plot(x_top, y_top)
plt.plot(x_tem_top, y_tem_top)
plt.axis('equal')

plt.show()