import math

def chord_method(f, a: float, b: float, tol: float, max_iters: int = 1000, fixed_end: str = 'left'):
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise ValueError("На данном отрезке нет единственного корня.")

    if fixed_end == 'left':
        x_prev = b
        fixed_val = a
    elif fixed_end == 'right':
        x_prev = a
        fixed_val = b
    else:
        raise ValueError("fixed_end должен быть 'left' или 'right'")

    for k in range(1, max_iters + 1):
        ff = f(fixed_val)
        fx = f(x_prev)
        denom = fx - ff
        if denom == 0:
            raise ZeroDivisionError("Деление на ноль при вычислении хорд.")
        x_next = x_prev - (x_prev - fixed_val) * fx / denom

        if math.isnan(x_next) or math.isinf(x_next):
            raise ArithmeticError("Хорд: вычислен NaN/Inf.")

        if abs(x_next - x_prev) < tol or abs(f(x_next)) < tol:
            return x_next, f(x_next), k

        x_prev = x_next

    raise RuntimeError("Хорды: не сошлось за max_iters.")