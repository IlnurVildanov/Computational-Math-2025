def trapezoid(f, a: float, b: float, n: int) -> float:
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        x_i = a + i * h
        total += 2 * f(x_i)
    return total * h / 2
