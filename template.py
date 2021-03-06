import sys # for argv
import svgwrite
import numpy

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

def box_lines(dwg, x, y):
    """Returns the lines that form all of the straight edges."""

    #print "x, y", x, y

    #right horizontal, right vertical, bottom horizontal, left vertical
    x1 = ["{}".format(x), 
        "{}".format(x+20), 
        "{}".format(x+20),
        "{}".format(10)]
    y1 = ["{}".format(y), 
        "{}".format(y), 
        "{}".format(y+20),
        "{}".format(y+20)]
    x2 = ["{}".format(x+20), 
        "{}".format(x+20),
        "{}".format(10),
        "{}".format(10)]
    y2 = ["{}".format(y), 
        "{}".format(y+20),
        "{}".format(y+20),
        "{}".format(y+5)]

    print "lengte onderste rand: ", x+20 - 10
    
    lines = [
        dwg.line(
            (x1[i], y1[i]),
            (x2[i], y2[i]),
            stroke="black",
            stroke_width="0.1"
            )
        for i in range(len(x1))
        ]

    return lines

def upper_half_lines(dwg, coordinates):
    """returns lines that form the upper half of the airfoil."""

    x, y = zip(*coordinates)

    lines = []
    for i in range(len(x)-1):
        x1 = "{}".format(x[i])
        y1 = "{}".format(y[i])
        x2 = "{}".format(x[i+1])
        y2 = "{}".format(y[i+1])

        lines.append(
            dwg.line( 
                (x1, y1), 
                (x2, y2), 
                stroke="black",
                stroke_width="0.1"
                )
            )
    return lines

def draw_upper_template(dwg, filename, size, offset, skiplines1, skiplines2):
    coordinates = read_coordinates(filename)
    coordinates = transform(coordinates, size, offset)

    x, y = zip(*coordinates)

    l = len(x)
    half_l = int(l/2)

    for line in upper_half_lines(dwg, coordinates[0:half_l+1-skiplines1]):
        dwg.add(line)

    for line in box_lines(dwg, coordinates[0][0], coordinates[0][1] ):
        dwg.add(line)

    dwg.add(
        dwg.path(
            d = "M {},{} C {} {}, {} {}, {} {}".format(
                x[half_l-skiplines2], y[half_l-skiplines2],
                x[half_l]-5, y[half_l]+5,
                x[half_l]-5, y[half_l]+5,
                10,y[0]+5),
            stroke = "black",
            stroke_width = "0.1",
            fill_opacity="0.0")
        )

def draw_lower_template(dwg, filename, size, offset, skiplines1, skiplines2):
    coordinates = read_coordinates(filename)
    coordinates = transform(coordinates, size, offset)

    #print (coordinates.shape)
    l = coordinates.shape[0]
    half_l = int(l/2)

    for line in upper_half_lines(dwg, coordinates[half_l+skiplines1:]):
        dwg.add(line)

    x = coordinates[-1][0]
    y = coordinates[-1][1]

    for line in box_lines(dwg, coordinates[-1][0], coordinates[-1][1]):
        dwg.add(line)

    x = coordinates[half_l+skiplines2][0]
    y = coordinates[half_l+skiplines2][1]

    dwg.add(
        dwg.path(
            d = "M {},{} C {} {}, {} {}, {} {}".format(
                x, y,
                x-5, y-5,
                x-5, y-5,
                10,y-5),
            stroke = "black",
            stroke_width = "0.1",
            fill_opacity="0.0")
        )
    # ugly fix
    dwg.add(
        dwg.line(
            (10, y-5),
            (10, y+5),
            stroke="black",
            stroke_width="0.1"
            ))

def draw_template(filename, size):

    dwg = svgwrite.Drawing(
        'test.svg', 
        profile='tiny', 
        size=('297mm', '210mm'), # A4 paper in landscape
        viewBox=('0 0 297 210'))

    # the offset is just chosen so that the templates 
    # fit on the paper, and do not overlap
    draw_upper_template(dwg, filename, size, (25,10))
    draw_lower_template(dwg, filename, size, (25,40))

    dwg.save()

if __name__ == "__main__":

    # Usage: python tempate.py airfoil.dat <inches>

    mm_per_inch = 25.4
    #size_inch = float(sys.argv[2])
    #size_mm = size_inch * mm_per_inch
    #draw_template(sys.argv[1], (size_mm,size_mm))

    # draw templates separately

    dwg = svgwrite.Drawing(
        'ag13-6.2_ag13-4.6_ag14-2.4.svg', 
        profile='tiny', 
        size=('220mm', '220mm'), # < A4 paper in landscape
        viewBox=('0 0 220 220')
        )

    # the offset is just chosen so that the templates 
    # fit on the paper, and do not overlap
    filenames = ['airfoils/ag13.dat', 'airfoils/ag13.dat', 'airfoils/ag14.dat']
    sizes = [(6.2*mm_per_inch,6.2*mm_per_inch), (4.6*mm_per_inch,4.6*mm_per_inch), (2.4*mm_per_inch,2.4*mm_per_inch)]

    for i in range(3):
        draw_upper_template(dwg, filenames[i], sizes[i], (25,10+(70*i)), 3, 3)
        draw_lower_template(dwg, filenames[i], sizes[i], (25,40+(70*i)), 2, 2)

    dwg.save()

    # draw templates overlayed

    dwg = svgwrite.Drawing(
        'ag13-6.2_ag13-4.6_ag14-2.4-ovelayed.svg', 
        profile='tiny', 
        size=('220mm', '220mm'), # < A4 paper in landscape
        viewBox=('0 0 220 220')
        )

    # the offset is just chosen so that the templates 
    # fit on the paper, and do not overlap
    filenames = ['airfoils/ag13.dat', 'airfoils/ag13.dat', 'airfoils/ag14.dat']
    sizes = [(6.2*mm_per_inch,6.2*mm_per_inch), (4.6*mm_per_inch,4.6*mm_per_inch), (2.4*mm_per_inch,2.4*mm_per_inch)]

    for i in range(3):
        draw_upper_template(dwg, filenames[i], sizes[i], (25,10+(40*i)), 0, 3)
        draw_lower_template(dwg, filenames[i], sizes[i], (25,10+(40*i)), 0, 2)

    dwg.save()

    
