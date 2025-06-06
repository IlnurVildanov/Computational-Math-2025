def runge_integral(
    integrator: callable,
    f: callable,
    a: float,
    b: float,
    tol: float,
    order: int
) -> tuple[float, int]:

    n = 4
    I_n = integrator(f, a, b, n)
    I_2n = integrator(f, a, b, 2 * n)

    # пока оценка погрешности > tol, удваиваем n
    while abs(I_2n - I_n) / (2**order - 1) > tol:
        n *= 2
        I_n = integrator(f, a, b, n)
        I_2n = integrator(f, a, b, 2 * n)

    # коррекция Рунге
    I_corr = I_2n + (I_2n - I_n) / (2**order - 1)
    return I_corr, 2 * n
