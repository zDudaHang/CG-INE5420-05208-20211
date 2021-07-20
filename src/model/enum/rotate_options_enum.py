from enum import Enum

class RotateOptionsEnum(Enum):
    WORLD = 'Rotacionar em torno do centro do mundo'
    OBJECT = 'Rotacionar em torno do centro do objeto'
    POINT = 'Rotacionar em torno de um ponto'

    def valueOf(value: str):
        if (value == RotateOptionsEnum.WORLD.value):
            return RotateOptionsEnum.WORLD
        if (value == RotateOptionsEnum.OBJECT.value):
            return RotateOptionsEnum.OBJECT
        if (value == RotateOptionsEnum.POINT.value):
            return RotateOptionsEnum.POINT
        return None