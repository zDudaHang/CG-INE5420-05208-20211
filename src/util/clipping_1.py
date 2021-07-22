from src.model.point import Point2D
from src.util.objects import wireframe_points_list, flatten

INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

def region_code(ponto: Point2D, window_coordinates: list[Point2D]):
    # Coordenadas do ponto
    x = ponto.x()
    y = ponto.y()

    # Coordenadas da window
    x_min = window_coordinates[2].x() + 10
    y_min = window_coordinates[2].y() + 10
    x_max = window_coordinates[1].x() - 10
    y_max = window_coordinates[1].y() - 10 

    rc = INSIDE
    
    if x < x_min:
        rc |= LEFT
    elif x > x_max:
        rc |= RIGHT
    if y < y_min:
        rc |= BOTTOM
    elif y > y_max:
        rc |= TOP

    return rc


def cohenSutherlandClip(ponto: Point2D, window_coordinates: list[Point2D]):



    ponto_1 = ponto[0]
    ponto_2 = ponto[1]

    rc_point_1 = region_code(ponto_1, window_coordinates)
    rc_point_2 = region_code(ponto_2, window_coordinates)

    point_1 = ponto_1
    point_2 = ponto_2

    # Coordenadas da window
    x_min = window_coordinates[2].x() + 10
    y_min = window_coordinates[2].y() + 10
    x_max = window_coordinates[1].x() - 10
    y_max = window_coordinates[1].y() - 10 

    while True:

        if rc_point_1 == 0 and rc_point_2 == 0:
            return [Point2D(point_1.x(),point_1.y()), Point2D(point_2.x(), point_2.y())]
        elif (rc_point_1 & rc_point_2) != 0:
            #COMPLETAMENTE FORA da window
            return None
        else:
            new_x = 1
            new_y = 1

            if rc_point_1 != 0:
                rc_out = rc_point_1
            else:
                rc_out = rc_point_2

            if rc_out & TOP:

                new_x = point_1.x() + (point_2.x() - point_1.x()) * \
                                (y_max - point_1.y()) / (point_2.y() - point_1.y())
                new_y = y_max
 
            elif rc_out & BOTTOM:
                 
                new_x = point_1.x() + (point_2.x() - point_1.x()) * \
                                (y_min - point_1.y()) / (point_2.y() - point_1.y())
                new_y = y_min
 
            elif rc_out & RIGHT:
                 
                new_y = point_1.y() + (point_2.y() - point_1.y()) * \
                                (x_max - point_1.y()) / (point_2.x() - point_1.x())
                new_x = x_max
 
            elif rc_out & LEFT:

                new_y = point_1.y() + (point_2.y() - point_1.y()) * \
                                (x_min - point_1.y()) / (point_2.x() - point_1.x())
                new_x = x_min
 
 
            if rc_out == rc_point_1:
                point_1 = Point2D(new_x, new_y)
                rc_point_1 = region_code(point_1, window_coordinates)
 
            else:
                point_2 = Point2D(new_x, new_y)
                rc_point_2 = region_code(point_2, window_coordinates)


def cohenSutherlandClipPoint(point: Point2D, window_coordinates: list[Point2D]):

    # Coordenadas da window
    x_min = window_coordinates[2].x() + 10
    y_min = window_coordinates[2].y() + 10
    x_max = window_coordinates[1].x() - 10
    y_max = window_coordinates[1].y() - 10 

    x = point[0].x()
    y = point[0].y()

    if (x < x_min or x > x_max):
        return None
    elif (y < y_min or y > y_max):
        return None
    else:
        return point

def cohenSutherlandClipPolygon(ponto: Point2D, window_coordinates: list[Point2D]):

    new_coordinates = []
    coordinates_list = ponto.copy()
    coordinates_list.append(Point2D(ponto[0].x(), ponto[0].y()))  
   
    for i in range(len(coordinates_list)-1):
        coordinates = [coordinates_list[i], coordinates_list[i+1]]
        clip = cohenSutherlandClip(coordinates, window_coordinates)

        if clip is not None:
            new_coordinates.append(clip)
    new_coordinates = flatten(new_coordinates)

    return new_coordinates

    