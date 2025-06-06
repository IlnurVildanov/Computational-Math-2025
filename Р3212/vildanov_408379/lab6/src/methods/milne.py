import math
from methods.rk4 import rk4_method


def milne_method(f, x0: float, xn: float, y0: float, h: float) -> tuple[list[float], list[float]]:
    xs_rk, ys_rk = rk4_method(f, x0, x0 + 3*h, y0, h)
    xs = xs_rk.copy()
    ys = ys_rk.copy()

    while xs[-1] < xn and not math.isclose(xs[-1], xn):
        i = len(xs) - 1  # текущий индекс
        x_i   = xs[i];    y_i   = ys[i]
        x_im1, y_im1 = xs[i-1], ys[i-1]
        x_im2, y_im2 = xs[i-2], ys[i-2]
        x_im3, y_im3 = xs[i-3], ys[i-3]

        # предиктор
        y_pred = y_im3 + (4*h/3) * (
            2*f(x_im2, y_im2)
            - f(x_im1, y_im1)
            + 2*f(x_i,   y_i)
        )
        x_next = round(x_i + h, 12)

        # корректор
        y_corr = y_im1 + (h/3) * (
            f(x_im1, y_im1)
            + 4 * f(x_i, y_i)
            + f(x_next, y_pred)
        )

        xs.append(x_next)
        ys.append(y_corr)

    return xs, ys
