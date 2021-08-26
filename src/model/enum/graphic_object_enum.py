from enum import Enum

class GraphicObjectEnum(Enum):
    POINT = "Ponto"
    LINE = "Reta"
    WIREFRAME = "Wireframe"
    CURVE = "Curva"
    OBJECT_3D = "Objeto 3D"
    BICUBIC = "Superfície Bicúbica de Bézier"


    def valueOf(value: str):
        for g in GraphicObjectEnum:
            if value == g.value:
                return g
        return None