import math

def euler_method(f, x0: float, xn: float, y0: float, h: float) -> tuple[list[float], list[float]]:
    xs = [x0]
    ys = [y0]
    x = x0
    while x < xn and not math.isclose(x, xn):
        y_prev = ys[-1]
        y_next = y_prev + h * f(x, y_prev)
        x = round(x + h, 12)
        xs.append(x)
        ys.append(y_next)
    return xs, ys
