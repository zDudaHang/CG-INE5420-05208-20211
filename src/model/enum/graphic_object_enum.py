from enum import Enum

class GraphicObjectEnum(Enum):
    POINT = "Ponto"
    LINE = "Reta"
    WIREFRAME = "Wireframe"

    def valueOf(value: str) :
        if value == GraphicObjectEnum.POINT.value:
            return GraphicObjectEnum.POINT
        
        if value == GraphicObjectEnum.LINE.value:
            return GraphicObjectEnum.LINE
        
        if value == GraphicObjectEnum.WIREFRAME.value:
            return GraphicObjectEnum.WIREFRAME
        
        return None