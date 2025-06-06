import math
import numpy as np


def simple_iteration_method(f, phi, phi_prime, a: float, b: float, tol: float, max_iters: int = 1000):
    xs = np.linspace(a, b, 200)
    q = max(abs(phi_prime(x)) for x in xs)
    if q >= 1:
        raise ValueError(f"Условие сходимости не выполнено: max|φ'| = {q:.4f} ≥ 1")

    x = (a + b) / 2
    for k in range(1, max_iters + 1):
        x_next = phi(x)
        if abs(x_next - x) < tol:
            return x_next, f(x_next), k
        x = x_next
    raise RuntimeError("Простая итерация: не сошлось за max_iters.")