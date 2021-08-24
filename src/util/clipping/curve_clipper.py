INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

x_min = -1 
y_min = -1
x_max = 1
y_max = 1


def region_code(x, y):
    rc = INSIDE
    
    if x < x_min:
        rc |= LEFT
    elif x > x_max:
        rc |= RIGHT
    if y < y_min:
        rc |= BOTTOM
    elif y > y_max:
        rc |= TOP

    return rc
    
def curve_clip(x1, y1, x2, y2):
    
    rc_point_1 = region_code(x1, y1)
    rc_point_2 = region_code(x2, y2)

    while True:

        if rc_point_1 == 0 and rc_point_2 == 0:
            return x1, y1, x2, y2
            
        elif (rc_point_1 & rc_point_2) != 0:
            return None, None, None, None
        else:
            new_x = 1
            new_y = 1

            if rc_point_1 != 0:
                rc_out = rc_point_1
            else:
                rc_out = rc_point_2

            if rc_out & TOP:

                new_x = x1 + (x2 - x1) * \
                                (y_max - y1) / (y2 - y1)
                new_y = y_max

            elif rc_out & BOTTOM:
                
                new_x = x1 + (x2 - x1) * \
                                (y_min - y1) / (y2 - y1)
                new_y = y_min

            elif rc_out & RIGHT:
                
                new_y = y1 + (y2 - y1) * \
                                (x_max - x1) / (x2 - x1)
                new_x = x_max

            elif rc_out & LEFT:

                new_y = y1 + (y2 - y1) * \
                                (x_min - x1) / (x2 - x1)
                new_x = x_min


            if rc_out == rc_point_1:
                rc_point_1 = region_code(new_x, new_y)
            else:
                rc_point_2 = region_code(new_x, new_y)

