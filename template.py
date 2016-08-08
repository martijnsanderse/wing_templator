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

x = (numpy.array(x)+0.1)*100
y = (numpy.array(y)*-1+0.1)*100

print x
print
print y

dwg = svgwrite.Drawing('test.svg', profile='tiny')

for i in xrange(l-1):
    x1 = "{}mm".format(x[i])
    y1 = "{}mm".format(y[i])
    x2 = "{}mm".format(x[i+1])
    y2 = "{}mm".format(y[i+1])
    dwg.add ( 
    	dwg.line( 
    		(x1, y1), 
    		(x2, y2), 
    		stroke=svgwrite.rgb(10, 10, 16, '%'),
            stroke_width="0.1"
    		)
    	)

dwg.save()