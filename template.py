import sys # for argv
from PIL import Image, ImageDraw


def main():  
    filename = sys.argv[1]
    with open(filename, "rb") as f:
        lines = f.readlines()

    print "Airfoil: ", lines[0]
    coordinates = [[float(coordinate) for coordinate in line.split()] for line in lines[1:]]

    # x, y = zip(*coordinates)
    # minX = min(x)
    # maxX = max(x)
    # minY = min(y)
    # maxY = max(y)

    im = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(im)
    
    for i in range(1, len(coordinates)):
        draw.line((coordinates[i-1][0]*200+50,
        			coordinates[i-1][1]*200+200,
        			coordinates[i][0]*200+50,
        			coordinates[i][1]*200+200), fill="black")
    
    im.save("test.png")


if __name__ == "__main__":
    main()
