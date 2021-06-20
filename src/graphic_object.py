from abc import ABC, abstractmethod
from enum import Enum

class GraphicObjectEnum(Enum):
    POINT = "Ponto"
    LINE = "Reta"
    WIREFRAME = "Wireframe"

    def valueOf(value: str) :
        if (value == GraphicObjectEnum.POINT.value):
            return GraphicObjectEnum.POINT
        if (value == GraphicObjectEnum.LINE.value):
            return GraphicObjectEnum.LINE
        if (value == GraphicObjectEnum.WIREFRAME.value):
            return GraphicObjectEnum.WIREFRAME
        return None


class GraphicObject(ABC):

    def __init__(self, name: str, type : GraphicObjectEnum, coordinates: list):
        self.name = name
        self.type = type
        self.coordinates = coordinates

    @abstractmethod
    def draw(self):
        ...

    def __str__(self):
        return f'{self.type.value} ({self.name})'
    
class Point(GraphicObject):

    def __init__(self, name: str, coordinates: list):
        if len(coordinates) != 2:
            raise ValueError("Um ponto deve ter apenas um par de coordenadas (x,y).")
        super().__init__(name, GraphicObjectEnum.POINT, coordinates)
    
    def draw(self):
        print(f'PONTO: {self.coordinates}')
        
class Line(GraphicObject):

    def __init__(self, name: str, coordinates: list):
        if len(coordinates) != 4:
            raise ValueError("Uma linha deve ter apenas 2 pares de coordenadas (x1,y1) e (x2, y2).")
        # TODO: Validar se essas coordenadas nao podem representar um ponto x1 = x2 e y1 = y2
        super().__init__(name, GraphicObjectEnum.LINE, coordinates)
    
    def draw(self):
        print(f'LINHA: {self.coordinates}')

class WireFrame(GraphicObject):

    def __init__(self, name: str, coordinates: list):
        if len(coordinates) % 2 != 0:
            raise ValueError("Um wireframe deve ter um número par de tuplas de coordenadas.")
        if len(coordinates) < 6:
            raise ValueError("Um wireframe deve ter no mínimo três pares de coordenadas.")
        super().__init__(name, GraphicObjectEnum.WIREFRAME, coordinates)
    
    def draw(self):
        print(f'WIREFRAME: {self.coordinates}')
