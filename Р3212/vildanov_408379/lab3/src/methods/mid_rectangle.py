def mid_rectangle(f, a: float, b: float, n: int) -> float:
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        x_mid = a + (i + 0.5) * h
        total += f(x_mid)
    return total * h
