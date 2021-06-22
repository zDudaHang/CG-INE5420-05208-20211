
def viewport_transform(x_w, y_w, x_w_min, y_w_min, x_w_max, y_w_max, x_v_min, y_v_min, x_v_max, y_v_max):
    x_div = (x_w - x_w_min) / (x_w_max - x_w_min)
    x_v = x_div * (x_v_max - x_v_min)

    y_div = (y_w - y_w_min) / (y_w_max - y_w_min)
    y_v = (1 - y_div) * (y_v_max - y_v_min)

    print((x_v, y_v))
    return (x_v, y_v)
