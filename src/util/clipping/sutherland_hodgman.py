from copy import deepcopy

from src.model.point import Point3D
from src.model.graphic_object import WireFrame

class SutherlandHodgman:
    
    INSIDE = 0  # 0000
    LEFT = 1    # 0001
    RIGHT = 2   # 0010
    BOTTOM = 4  # 0100
    TOP = 8     # 1000

    def __init__(self, polygon: WireFrame, window_min: Point3D = Point3D(-1, -1), window_max: Point3D = Point3D(1, 1) ):

        self.subject_vertices = deepcopy(polygon.coordinates)
        self.len = len(self.subject_vertices)

        if self.len == 3:
            self.subject_vertices.sort(key=lambda x: x.x())

        self.obj = deepcopy(polygon)

        self.vertices = {}

        self.x_min = window_min.x() 
        self.y_min = window_min.y()
        self.x_max = window_max.x()
        self.y_max = window_max.y()

    def sutherland_hodgman_clip(self):
        self.subject_vertices.append(self.subject_vertices[0])
        self.obj.is_clipped = False

        temp = []
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
                #os dois pontos estão fora
                if rc_v1 in [1,2,4,8] and rc_v2 in [1,2,4,8] and rc_v1 != rc_v2:
                    try:
                        intersection = self.new_vertex(rc_v1, self.subject_vertices[v], self.subject_vertices[v+1])
                        intersection_2 = self.new_vertex(rc_v2, self.subject_vertices[v+1], self.subject_vertices[v])

                        if rc_v1 == 1 or rc_v1 == 2: 
                            if self.y_min < intersection.y() < self.y_max:
                                self.vertices[f'i{i}'] = intersection
                                self.vertices[f'v{v}'] = intersection
                                self.vertices[f'i{i+1}'] = intersection_2
                                i+=2

                        elif rc_v1 == 4 or rc_v1 == 8 and self.x_min < intersection.x() < self.x_max:

                            self.vertices[f'i{i}'] = intersection
                            self.vertices[f'v{v}'] = intersection
                            self.vertices[f'i{i+1}'] = intersection_2
                            i+=2
                    except: pass

                self.obj.is_clipped = True

            if self.obj.is_filled:

                if rc_v1 in [2,8,10] and rc_v2 == 10 or \
                    rc_v1 == 10 and rc_v2 in [2,8,10]:
                    self.vertices[f'v{v}'] = Point3D(self.x_max, self.y_max)
                if rc_v1 in [1,8,9] and rc_v2 == 9 or \
                    rc_v1 == 9 and rc_v2 in [1,8,9]:
                    self.vertices[f'v{v}'] = Point3D(self.x_min, self.y_max)
                if rc_v1 in [1,4,5] and rc_v2 == 5 or \
                    rc_v1 == 5 and rc_v2 in [1,4,5]:
                    self.vertices[f'v{v}'] = Point3D(self.x_min, self.y_min)
                if rc_v1 in [2,4,6] and rc_v2 == 6 or \
                    rc_v1 == 6 and rc_v2 in [2,4,6]:
                    self.vertices[f'v{v}'] = Point3D(self.x_max, self.y_min)
                if rc_v1 == 8 and rc_v2 == 2 or \
                    rc_v1 == 2 and rc_v2 == 8:
                    self.vertices[f'v{v}'] = self.new_vertex(10, self.subject_vertices[v], self.subject_vertices[v+1])
                if rc_v1 == 4 and rc_v2 == 2 or \
                    rc_v1 == 2 and rc_v2 == 4:
                    self.vertices[f'v{v}'] = self.new_vertex(6, self.subject_vertices[v], self.subject_vertices[v+1])
                if rc_v1 == 4 and rc_v2 == 1 or \
                    rc_v1 == 1 and rc_v2 == 4:
                    self.vertices[f'v{v}'] = self.new_vertex(5, self.subject_vertices[v], self.subject_vertices[v+1])
                if rc_v1 == 1 and rc_v2 == 8 or \
                    rc_v1 == 8 and rc_v2 == 1:
                    self.vertices[f'v{v}'] = self.new_vertex(9, self.subject_vertices[v], self.subject_vertices[v+1])
               
        try:
            sub_polygons = [[list(self.vertices.values())[0]]]

            for i in range(1, len(self.vertices)):
                if 'i' in list(self.vertices.keys())[i-1] and 'i' in list(self.vertices.keys())[i]: # duas interseções consecutivas, divide a lista
    
                    sub_polygons.append([list(self.vertices.values())[i]])
                else: sub_polygons[len(sub_polygons) - 1].append(list(self.vertices.values())[i])
        except IndexError:
            sub_polygons = [] # polígono fora da window

        if temp != []:
            sub_polygons.insert(0,temp)

        self.obj.coordinates = sub_polygons

        return self.obj


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


        return Point3D(new_x, new_y)


    
    def region_code(self, ponto: Point3D):
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