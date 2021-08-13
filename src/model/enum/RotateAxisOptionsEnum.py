from enum import IntEnum

class RotateAxisOptionsEnum(IntEnum):
    X = 0
    Y = 1
    Z = 2
    ARBITRARY = 3

    def valueOf(value: int):
        if value == RotateAxisOptionsEnum.X.value:
            return RotateAxisOptionsEnum.X
        
        if value == RotateAxisOptionsEnum.Y.value:
            return RotateAxisOptionsEnum.Y
        
        if value == RotateAxisOptionsEnum.Z.value:
            return RotateAxisOptionsEnum.Z

        if value == RotateAxisOptionsEnum.ARBITRARY.value:
            return RotateAxisOptionsEnum.ARBITRARY
        return None
    
    def _to_str(value: int):
        if value == RotateAxisOptionsEnum.X.value:
            return 'X'
        
        if value == RotateAxisOptionsEnum.Y.value:
            return 'Y'
        
        if value == RotateAxisOptionsEnum.Z.value:
            return 'Z'

        if value == RotateAxisOptionsEnum.ARBITRARY.value:
            return 'Arbitrário'
        return None
