def simpson(f, a: float, b: float, n: int) -> float:
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    total = f(a) + f(b)
    # сумма для нечетных индексов: 4 * f(a + (2k+1)h)
    for i in range(1, n, 2):
        x_i = a + i * h
        total += 4 * f(x_i)
    # сумма для четных индексов: 2 * f(a + 2k h)
    for i in range(2, n, 2):
        x_i = a + i * h
        total += 2 * f(x_i)
    return total * (h / 3)
