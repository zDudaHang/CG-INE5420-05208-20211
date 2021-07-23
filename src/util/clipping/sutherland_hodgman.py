from copy import deepcopy
from src.model.point import Point2D
from src.model.graphic_object import Point, WireFrame
from src.util.clipping.cohen_sutherland_clipper import CohenSutherlandLineClipper

class SutherlandHodgman:
    def __init__(self, polygon: WireFrame, window_min: Point2D = Point2D(-1, -1), window_max: Point2D = Point2D(1, 1), \
        bottom_left: Point2D = Point2D(-1,-1), top_left: Point2D = Point2D(-1,1), top_right: Point2D = Point2D(1,1), bottom_right: Point2D = Point2D(1,-1) ):
        
        self.subject_vertices = polygon.coordinates 
        self.clip_polygon = [bottom_left, top_left, top_right, bottom_right]

        self.output = []

        self.x_min = window_min.x() 
        self.y_min = window_min.y()
        self.x_max = window_max.x()
        self.y_max = window_max.y()

        self.old_polygon = polygon
        # self.clipping_area = [bottom_left, top_left, top_right, bottom_right]
        # self.subject = polygon.coordinates

    def point_inside_window(self, point: Point2D) -> bool:
    
        x_inside = self.x_min <= point.x() <= self.x_max
        y_inside = self.y_min <= point.y() <= self.y_max

        return x_inside and y_inside

    def output_list(self):

        polygon = deepcopy(self.old_polygon)
        
        for v in range(len(polygon)-1):
            clip = CohenSutherlandLineClipper([v, v+1]).cohenSutherlandClip()

            if clip is not None:
                self.output_list.append(clip)
        polygon.coordinates = self.output

        return polygon

    


    
