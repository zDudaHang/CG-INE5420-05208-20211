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

        self.subject_vertices = polygon.coordinates 

        self.output = deepcopy(polygon.coordinates)
        self.obj = deepcopy(polygon)

        self.vertices = []

        self.x_min = window_min.x() 
        self.y_min = window_min.y()
        self.x_max = window_max.x()
        self.y_max = window_max.y()

    def region_code(self, ponto: Point2D):
        # Coordenadas do ponto
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

    def sutherland_hodgman_clip(self):
        self.output.append(self.output[0])
        self.obj.is_clipped = False
        rc = [1,2,4,8]
        clip_region = []

        for v in range(len(self.output)-1):
        
            rc_v1 = self.region_code(self.output[v])
            rc_v2 = self.region_code(self.output[v+1])

            if rc_v1 in rc and rc_v2 == 0:   
                clip_region.append(self.clip_region(rc_v1))          
                intersection = self.new_vertex(rc_v1, self.output[v], self.output[v+1])
                self.vertices.extend([intersection, self.output[v+1]])
                self.obj.is_clipped = True

            elif rc_v1 == 0 and rc_v2 in rc: 
                clip_region.append(self.clip_region(rc_v2))    
                intersection = self.new_vertex(rc_v2, self.output[v], self.output[v+1])
                self.vertices.append(intersection)
                self.obj.is_clipped = True
            elif rc_v1 == 0 and rc_v2 == 0:
                self.vertices.append(self.output[v+1])
            else:
                self.obj.is_clipped = True

        if 'D' in clip_region:
            if 'B' not in clip_region:
                self.vertices = self.vertices[-2:] + self.vertices[:-2]
        if 'T' in clip_region: 
            if 'E' not in clip_region:
                self.vertices = self.vertices[-3:] + self.vertices[:-3]

        self.obj.coordinates = self.vertices
        return self.obj
      # (-10,-10),(-10,100),(100,100),(100,-10)
      # (100,50),(150,150),(200,50)
      #(100,100),(100,230),(230,230),(150,145),(230,100)
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
        

        return Point2D(new_x, new_y)

    def clip_region(self, rc):
        clip = ''
        if rc == 1:
            clip = 'E'
        elif rc == 2:
            clip = 'D'
        elif rc == 4:
            clip = 'B'
        else:
            clip = 'T'
        return clip