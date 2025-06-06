import math

def secant_method(f, a: float, b: float, tol: float, max_iters: int = 1000):
    x_prev, x_cur = a, b
    f_prev, f_cur = f(x_prev), f(x_cur)

    if f_prev == f_cur:
        raise ZeroDivisionError("Секущие: f(a) == f(b), деление на ноль.")

    for k in range(1, max_iters + 1):
        x_next = x_cur - (x_cur - x_prev) * f_cur / (f_cur - f_prev)
        if math.isnan(x_next) or math.isinf(x_next):
            raise ArithmeticError("Секущие: получили NaN/Inf.")
        if abs(x_next - x_cur) < tol or abs(f(x_next)) < tol:
            return x_next, f(x_next), k
        x_prev, f_prev = x_cur, f_cur
        x_cur, f_cur = x_next, f(x_next)
    raise RuntimeError("Секущие: не сошлось за max_iters.")