from enum import IntEnum

class CoordsEnum(IntEnum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3

    def valueOf(value: int) -> str:
        if value == CoordsEnum.TOP_LEFT:
            return 'TOP_LEFT'
        
        if value == CoordsEnum.TOP_RIGHT:
            return 'TOP_RIGHT'
        
        if value == CoordsEnum.BOTTOM_LEFT:
            return 'BOTTOM_LEFT'
        
        if value == CoordsEnum.BOTTOM_RIGHT:
            return 'BOTTOM_RIGHT'
        
        return None