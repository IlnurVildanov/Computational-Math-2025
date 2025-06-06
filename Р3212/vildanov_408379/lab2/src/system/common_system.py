import math
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


def _is_float_string(s: str) -> bool:
    st = s.strip()
    if st.startswith('-'):
        st = st[1:]
    if st.count('.') > 1:
        return False
    if '.' in st:
        parts = st.split('.')
        return all(part.isdigit() for part in parts if part != '')
    return st.isdigit()


def read_initial_guess_system() -> tuple:
    while True:
        xs = input("Введите начальное приближение x₀: ").strip()
        if _is_float_string(xs):
            x0 = float(xs)
            break
        print("Некорректно. Ожидается вещественное число.")
    while True:
        ys = input("Введите начальное приближение y₀: ").strip()
        if _is_float_string(ys):
            y0 = float(ys)
            break
        print("Некорректно. Ожидается вещественное число.")
    return x0, y0


def plot_two_equations(system: dict, root: tuple or None = None):
    f1f2 = system['functions']
    name = system['name']

    x_vals = np.linspace(-3, 3, 300)
    y_vals = np.linspace(-3, 3, 300)
    X, Y = np.meshgrid(x_vals, y_vals)

    F1 = np.vectorize(lambda x, y: f1f2(x, y)[0])(X, Y)
    F2 = np.vectorize(lambda x, y: f1f2(x, y)[1])(X, Y)

    plt.figure(figsize=(7, 7))
    cs1 = plt.contour(X, Y, F1, levels=[0], colors='r', linewidths=1.2)
    plt.clabel(cs1, inline=True, fontsize=10, fmt="f₁=0")
    cs2 = plt.contour(X, Y, F2, levels=[0], colors='b', linewidths=1.2)
    plt.clabel(cs2, inline=True, fontsize=10, fmt="f₂=0")

    if root is not None:
        plt.scatter([root[0]], [root[1]], color='green', s=60, label=f"Корень (≈ {root[0]:.4f}, {root[1]:.4f})")
        plt.legend()

    plt.title(f"График системы: {name}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()