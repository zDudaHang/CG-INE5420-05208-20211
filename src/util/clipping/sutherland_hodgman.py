from copy import deepcopy

from src.model.point import Point2D
from src.model.graphic_object import Point, WireFrame

class SutherlandHodgman:
    
    INSIDE = 0  # 0000
    LEFT = 1    # 0001
    RIGHT = 2   # 0010
    BOTTOM = 4  # 0100
    TOP = 8     # 1000

    def __init__(self, polygon: WireFrame, window_min: Point2D = Point2D(-1, -1), window_max: Point2D = Point2D(1, 1) ):

        self.subject_vertices = deepcopy(polygon.coordinates)
        self.obj = deepcopy(polygon)

        self.vertices = {}

        self.x_min = window_min.x() 
        self.y_min = window_min.y()
        self.x_max = window_max.x()
        self.y_max = window_max.y()

    def sutherland_hodgman_clip(self):
        self.subject_vertices.append(self.subject_vertices[0])
        self.obj.is_clipped = False

        i = 0

        for v in range(len(self.subject_vertices)-1):
        
            rc_v1 = self.region_code(self.subject_vertices[v])
            rc_v2 = self.region_code(self.subject_vertices[v+1])

            if rc_v1 != 0 and rc_v2 == 0:             
                intersection = self.new_vertex(rc_v1, self.subject_vertices[v], self.subject_vertices[v+1])
                self.vertices[f'i{i}'] = intersection
                self.vertices[f'v{v}'] = self.subject_vertices[v+1]
                i += 1
                self.obj.is_clipped = True

            elif rc_v1 == 0 and rc_v2 != 0:  
                intersection = self.new_vertex(rc_v2, self.subject_vertices[v], self.subject_vertices[v+1])
                self.vertices[f'v{v}'] = self.subject_vertices[v]
                self.vertices[f'i{i}'] = intersection
                i += 1
                self.obj.is_clipped = True
            elif rc_v1 == 0 and rc_v2 == 0:
                self.vertices[f'v{v}'] = self.subject_vertices[v]
                self.vertices[f'v{v+1}'] = self.subject_vertices[v+1]
            else:
                self.obj.is_clipped = True

        try:
            sub_polygons = [[list(self.vertices.values())[0]]]

            for i in range(1, len(self.vertices)):
                if 'i' in list(self.vertices.keys())[i-1] and 'i' in list(self.vertices.keys())[i]: # duas interseções consecutivas, divide a lista
                    sub_polygons.append([list(self.vertices.values())[i]])
                else: sub_polygons[len(sub_polygons) - 1].append(list(self.vertices.values())[i])
        except IndexError:
            sub_polygons = [] # polígono fora da window
    
        
        self.obj.coordinates = sub_polygons
        return self.obj
        
      #(100,100),(100,230),(230,230),(150,145),(230,100)
      # curva (0,0),(0,5),(5,5),(5,0),(5,-5),(10,0)

    def new_vertex(self, rc, point_1, point_2):

        if rc == 1:
            new_y = point_1.y() + (point_2.y() - point_1.y()) * (self.x_min - point_1.x()) / (point_2.x() - point_1.x())
            new_x = self.x_min
        if rc == 2:
            new_y = point_1.y() + (point_2.y() - point_1.y()) * (self.x_max - point_1.x()) / (point_2.x() - point_1.x())
            new_x = self.x_max
        if rc == 4:
            new_x = point_1.x() + (point_2.x() - point_1.x()) * (self.y_min - point_1.y()) / (point_2.y() - point_1.y())
            new_y = self.y_min
        if rc == 8:
            new_x = point_1.x() + (point_2.x() - point_1.x()) * (self.y_max - point_1.y()) / (point_2.y() - point_1.y())
            new_y = self.y_max
        
        if rc == 5:
            # Primeiro caso:
            x_bot = point_1.x() + (point_2.x() - point_1.x()) * (self.y_min - point_1.y()) / (point_2.y() - point_1.y())
            # Segundo caso:
            y_esq = point_1.y() + (point_2.y() - point_1.y()) * (self.x_min - point_1.x()) / (point_2.x() - point_1.x())

            if x_bot > self.x_min:
                new_x = x_bot
                new_y = self.y_min
            elif y_esq > self.y_min:
                new_x = self.x_min
                new_y = y_esq
            else:
                new_x = self.x_min
                new_y = self.y_min

        if rc == 6:
            # Primeiro caso:
            x_bot = point_1.x() + (point_2.x() - point_1.x()) * (self.y_min - point_1.y()) / (point_2.y() - point_1.y())
            # Segundo caso:
            y_dir = point_1.y() + (point_2.y() - point_1.y()) * (self.x_max - point_1.x()) / (point_2.x() - point_1.x())

            if x_bot < self.x_max:
                new_x = x_bot
                new_y = self.y_min
            elif y_dir > self.y_min:
                new_x = self.x_max
                new_y = y_dir
            else:
                new_x = self.x_max
                new_y = self.y_min

        if rc == 9:
            # Primeiro caso:
            x_top = point_1.x() + (point_2.x() - point_1.x()) * (self.y_max - point_1.y()) / (point_2.y() - point_1.y())
            # Segundo caso:
            y_esq = point_1.y() + (point_2.y() - point_1.y()) * (self.x_min - point_1.x()) / (point_2.x() - point_1.x())

            if x_top > self.x_min:
                new_x = x_top
                new_y = self.y_max
            elif y_esq < self.y_max:
                new_x = self.x_min
                new_y = y_esq
            else:
                new_x = self.x_min
                new_y = self.y_max

        if rc == 10:
            # Primeiro caso:
            x_top = point_1.x() + (point_2.x() - point_1.x()) * (self.y_max - point_1.y()) / (point_2.y() - point_1.y())
            # Segundo caso:
            y_dir = point_1.y() + (point_2.y() - point_1.y()) * (self.x_max - point_1.x()) / (point_2.x() - point_1.x())

            if x_top < self.x_max:
                new_x = x_top
                new_y = self.y_max
            elif y_dir < self.y_max:
                new_x = self.x_max
                new_y = y_dir
            else:
                new_x = self.x_max
                new_y = self.y_max


        return Point2D(new_x, new_y)


    
    def region_code(self, ponto: Point2D):
        x = ponto.x()
        y = ponto.y()
        
        rc = self.INSIDE
        
        if x < self.x_min:
            rc |= self.LEFT
        elif x > self.x_max:
            rc |= self.RIGHT
        if y < self.y_min:
            rc |= self.BOTTOM
        elif y > self.y_max:
            rc |= self.TOP

        return rc