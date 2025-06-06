def left_rectangle(f, a: float, b: float, n: int) -> float:
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        x_i = a + i * h
        total += f(x_i)
    return total * h
