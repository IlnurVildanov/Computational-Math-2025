import math
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


def _is_int_string(s: str) -> bool:
    st = s.strip()
    if st.startswith('-'):
        st = st[1:]
    return st.isdigit()


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


def read_interval_and_eps_from_keyboard() -> tuple:
    while True:
        s = input("Введите a (левая граница, float): ").strip()
        if _is_float_string(s):
            a = float(s)
            break
        print("Ошибка: нужно ввести вещественное число.")
    while True:
        s = input("Введите b (правая граница, float): ").strip()
        if _is_float_string(s):
            b = float(s)
            break
        print("Ошибка: нужно ввести вещественное число.")
    while True:
        s = input("Введите ε (точность, float > 0): ").strip()
        if _is_float_string(s) and float(s) > 0:
            eps = float(s)
            break
        print("Ошибка: ε должно быть положительным вещественным числом.")
    return a, b, eps


def read_interval_and_eps_from_file(path: str) -> tuple or None:
    try:
        with open(path, 'r') as f:
            lines = [line.strip() for line in f if line.strip() != ""]
    except IOError:
        return None

    if len(lines) < 3:
        return None

    if not (_is_float_string(lines[0]) and _is_float_string(lines[1]) and _is_float_string(lines[2])):
        return None

    a = float(lines[0])
    b = float(lines[1])
    eps = float(lines[2])
    if eps <= 0:
        return None

    return a, b, eps


def plot_function_on_segment(func, a: float, b: float, points: int = 300):
    xs = np.linspace(a, b, points)
    ys = [func(x) for x in xs]

    plt.figure(figsize=(7, 5))
    plt.plot(xs, ys, label="y = f(x)")
    plt.axhline(0, color='black', linewidth=0.7, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.7, linestyle='--')
    plt.title("График функции на отрезке")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()

    plt.show(block=False)
    plt.pause(0.5)

def plot_function_with_point(func, a: float, b: float, root: float, points: int = 300):
    xs = np.linspace(a, b, points)
    ys = [func(x) for x in xs]

    plt.figure(figsize=(7, 5))
    plt.plot(xs, ys, label="y = f(x)")
    plt.axhline(0, color='black', linewidth=0.7, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.7, linestyle='--')
    plt.scatter([root], [func(root)], color='green', s=60, label=f"Корень ≈ {root:.6f}")
    plt.title("График функции")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.show()

def numeric_derivative(func, h: float = 1e-6):
    return lambda x: (func(x + h) - func(x - h)) / (2 * h)

_raw_equations = {
    1: {
        "description": "f₁(x) = x⁴ − 3·x + 1",
        "f": lambda x: x**4 - 3*x + 1,
        "phi": lambda x: (3*x - 1)**(1/4) if (3*x - 1) >= 0 else -((-(3*x - 1))**(1/4))
    },
    2: {
        "description": "f₂(x) = e^{−x} − x² + 2",
        "f": lambda x: math.exp(-x) - x**2 + 2,
        "phi": lambda x: math.sqrt(math.exp(-x) + 2) if (math.exp(-x) + 2) >= 0 else x
    },
    3: {
        "description": "f₃(x) = x·sin(x) − 1",
        "f": lambda x: x * math.sin(x) - 1,
        "phi": lambda x: math.asin(1/x) if (x != 0 and abs(1/x) <= 1) else x
    },
    4: {
        "description": "f₄(x) = ln(x + 2) + x² − 3",
        "f": lambda x: (math.log(x + 2) + x**2 - 3) if x > -2 else float('inf'),
        "phi": lambda x: (math.sqrt(3 - math.log(x + 2)) if x > -2 and (3 - math.log(x + 2)) >= 0 else x)
    }
}

equations_map = {}
for k, info in _raw_equations.items():
    f_fun = info["f"]
    phi_fun = info["phi"]
    phi_prime_fun = numeric_derivative(phi_fun)

    equations_map[k] = {
        "description": info["description"],
        "f": f_fun,
        "phi": phi_fun,
        "phi_prime": phi_prime_fun
    }