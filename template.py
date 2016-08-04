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

x = (numpy.array(x)+0.1)*1000
y = (numpy.array(y)+0.1)*1000



dwg = svgwrite.Drawing('test.svg', profile='tiny')

for i in xrange(l-1):
    dwg.add(dwg.line((x[i], y[i]), (x[i+1], y[i+1]), stroke=svgwrite.rgb(10, 10, 16, '%')))

dwg.save()