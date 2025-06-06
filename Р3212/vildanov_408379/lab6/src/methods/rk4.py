import math


def rk4_method(f, x0: float, xn: float, y0: float, h: float) -> tuple[list[float], list[float]]:
    xs = [x0]
    ys = [y0]
    x = x0
    while x < xn and not math.isclose(x, xn):
        y = ys[-1]

        k1 = h * f(x, y)
        k2 = h * f(x + h / 2, y + k1 / 2)
        k3 = h * f(x + h / 2, y + k2 / 2)
        k4 = h * f(x + h, y + k3)

        y_next = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x = round(x + h, 12)
        xs.append(x)
        ys.append(y_next)
    return xs, ys
