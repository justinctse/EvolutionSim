import math
def get_distance(coordinates_1, coordinates_2):
    x1, y1 = coordinates_1[0], coordinates_1[1]
    x2, y2 = coordinates_2[0], coordinates_2[1]
    return math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))
def get_coordinates_from_angle(theta, d):
    radians = theta * math.pi/180
    x = d * math.cos(radians)
    y = d * math.sin(radians)
    return x, y