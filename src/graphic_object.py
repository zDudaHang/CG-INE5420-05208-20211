from abc import ABC, abstractmethod
from enum import Enum

class GraphicObjectEnum(Enum):
    POINT = "Ponto"
    LINE = "Reta"
    POLYGON = "Polígono"


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
        super().__init__(name, GraphicObjectEnum.POINT, coordinates)
    
    def draw(self):
        print(f'PONTO: {self.coordinates}')
        
class Line(GraphicObject):

    def __init__(self, name: str, coordinates: list):
        super().__init__(name, GraphicObjectEnum.LINE, coordinates)
    
    def draw(self):
        print(f'LINHA: {self.coordinates}')

class Polygon(GraphicObject):

    def __init__(self, name: str, coordinates: list):
        super().__init__(name, GraphicObjectEnum.POLYGON, coordinates)
    
    def draw(self):
        print(f'POLÍGONO: {self.coordinates}')
