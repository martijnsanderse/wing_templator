import sys # for argv
import svgwrite
import numpy

def read_coordinates(filename):
    filename = sys.argv[1]
    with open(filename, "rb") as f:
        lines = f.readlines()

    print ("Airfoil: ", lines[0])
    coordinates = [[float(coordinate) for coordinate in line.split()] for line in lines[1:]]

    x, y = zip(*coordinates)

    return x, y

def transform(x, y):
    # todo: use numpy matrix multiplication
    # for affine transformations.
    x_temp = []
    y_temp = []
    for x_t in x:
        transformed = x_t * 100 + 30
        x_temp.append(transformed)
    for y_t in y:
        transformed = y_t * -100 + 10
        y_temp.append(transformed)
    return x_temp, y_temp

def box_lines(dwg, x, y):
    """Returns the lines that form all of the straight edges."""

    #right horizontal, right vertical, bottom horizontal, left vertical
    x1 = ["{}".format(x[0]), 
        "{}".format(x[0]+20), 
        "{}".format(x[0]+20),
        "{}".format(10)]
    y1 = ["{}".format(y[0]), 
        "{}".format(y[0]), 
        "{}".format(y[0]+10),
        "{}".format(y[0]+10)]
    x2 = ["{}".format(x[0]+20), 
        "{}".format(x[0]+20),
        "{}".format(10),
        "{}".format(10)]
    y2 = ["{}".format(y[0]), 
        "{}".format(y[0]+10),
        "{}".format(y[0]+10),
        "{}".format(y[0]+5)]

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

def upper_half_lines(dwg, x, y):
    """returns lines that form the upper half of the airfoil."""
    half_l = int(len(x)/2)

    lines = []
    for i in range(half_l-1):
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

def draw_template(filename):

    x, y = read_coordinates(filename)
    x, y = transform(x, y)

    l = len(x)
    half_l = int(l/2)

    dwg = svgwrite.Drawing(
        'test.svg', 
        profile='tiny', 
        size=('170mm', '130mm'), 
        viewBox=('0 0 170 130'))    

    for line in upper_half_lines(dwg, x, y):
        dwg.add(line)

    for line in box_lines(dwg, x, y):
        dwg.add(line)

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

if __name__ == "__main__":

    draw_template(sys.argv[1])