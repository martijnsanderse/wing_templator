import sys # for argv
import svgwrite
import numpy


filename = sys.argv[1]
with open(filename, "rb") as f:
    lines = f.readlines()

print ("Airfoil: ", lines[0])
coordinates = [[float(coordinate) for coordinate in line.split()] for line in lines[1:]]

l = len(coordinates)
x, y = zip(*coordinates)

x = (numpy.array(x))*100+30
y = (numpy.array(y)*-1)*100 + 10

half_l = len(x)/2

dwg = svgwrite.Drawing(
    'test.svg', 
    profile='tiny', 
    size=('170mm', '130mm'), 
    viewBox=('0 0 170 130'))

for i in xrange(half_l-1):
    x1 = "{}".format(x[i])
    y1 = "{}".format(y[i])
    x2 = "{}".format(x[i+1])
    y2 = "{}".format(y[i+1])
    dwg.add ( 
    	dwg.line( 
    		(x1, y1), 
    		(x2, y2), 
    		stroke="black",
            stroke_width="0.1"
    		)
    	)
    print x1,y1, x2,y2

#right horizontal line
x1 = "{}".format(x[0])
y1 = "{}".format(y[0])
x2 = "{}".format(x[0]+20)
y2 = "{}".format(y[0])

dwg.add ( 
    dwg.line(
        (x1, y1),
        (x2, y2),
        stroke="black",
        stroke_width="0.1"
        )
    )

#right vertical line
x1 = "{}".format(x[0]+20)
y1 = "{}".format(y[0])
x2 = "{}".format(x[0]+20)
y2 = "{}".format(y[0]+10)

dwg.add ( 
    dwg.line (
        (x1, y1),
        (x2, y2),
        stroke="black",
        stroke_width="0.1"
        )
    )

#bottom horizontal line
x1 = "{}".format(x[0]+20)
y1 = "{}".format(y[0]+10)
x2 = "{}".format(10)
y2 = "{}".format(y[0]+10)

dwg.add (
    dwg.line (
        (x1, y1),
        (x2, y2),
        stroke="black",
        stroke_width="0.1"
        )
    )

#left vertical line
x1 = "{}".format(10)
y1 = "{}".format(y[0]+10)
x2 = "{}".format(10)
y2 = "{}".format(y[0]+5)

dwg.add (
    dwg.line (
        (x1, y1),
        (x2, y2),
        stroke="black",
        stroke_width="0.1"
        )
    )

dwg.add(
    dwg.path(
        d = "M {},{} C {} {}, {} {}, {} {}".format(
            x[half_l], y[half_l],
            x[half_l]-5, y[half_l]+5,
            x[half_l]-5, y[half_l]+5,
            10,y[0]+5),
        stroke = "black",
        stroke_width = "0.1",
        fill_opacity="0.0")
    )

dwg.save()