import numpy
import matplotlib.pyplot as plt
import math
import svgwrite

def read_coordinates(filename):
    with open(filename, "rb") as f:
        lines = f.readlines()

    #print ("Airfoil: ", lines[0])
    coordinates = numpy.array(
        [[float(coordinate) for coordinate in line.split()] for line in lines[1:]]
        )

    return coordinates

def transform(coordinates, scale, translation):
    # todo: use numpy matrix multiplication
    # for affine transformations.

    # scaling
    s_x = scale[0] # mm
    s_y = -scale[1] # mm

    # translation
    t_x = translation[0]
    t_y = translation[1]

    #rotation does not seem to work properly?
    a = 0.0 # degrees
    r = a * numpy.pi/180

    # clockwise rotation
    scale_rotate = numpy.matrix([[s_x * numpy.cos(r),   -numpy.sin(r)    ],
                                 [numpy.sin(r),        s_y*numpy.cos(r)]])
    translate = numpy.matrix([t_x, t_y])

    c = numpy.matrix(coordinates) * scale_rotate + translate

    return numpy.array(c)    

def splinestuff(coordinates):

    #x, y = zip(*coordinates)

    alpha = numpy.linspace(0, 2*math.pi, 4, endpoint=False)
    x = 10 + 5 * numpy.cos(alpha)
    y = 10 + 5 * numpy.sin(alpha)

    from scipy import interpolate
    tck,u=interpolate.splprep([x,y],s=0.0, per=True)

    dwg = svgwrite.Drawing(
        'out.svg', 
        profile='tiny', 
        size=('297mm', '210mm'), # A4 paper in landscape
        viewBox=('0 0 297 210'))

    for i in range(1, len(x)-1):
        dwg.add(
            dwg.path(
                d = "M {},{} C {} {}, {} {}, {} {}".format(
                    x[i], y[i],
                    tck[1][0][i+1], tck[1][1][i+1],
                    x[i+1],y[i+1], # faking it
                    x[i+1],y[i+1]),
                stroke = "black",
                stroke_width = "0.1",
                fill_opacity="0.0")
            )

    dwg.save()

	#x_i,y_i= interpolate.splev(numpy.linspace(0,1,10000),tck)
	# plt.scatter(x[0], y[0], color='blue', label='given')
	# plt.scatter(tck[1][0][0], tck[1][1][0], color='green', label='control points')
    cx = tck[1][0]
    cy = tck[1][1]
    plt.scatter(x, y, color='black', label='given')
    plt.scatter(cx, cy, color='red', label='control points')
    for i in range(len(cx)):
        print i
        plt.plot([x[i], cx[i]], [y[i], cy[i]])
    plt.legend()
    plt.show()

coordinates = read_coordinates('airfoils/ag13.dat');
coordinates = transform(coordinates, (100,100), (10,10))
splinestuff(coordinates)
