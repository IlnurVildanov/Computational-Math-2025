import math
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

from methods.euler import euler_method
from methods.rk4 import rk4_method
from methods.milne import milne_method


funcs = [
    [
        "y' = y/3 + 2x",
        lambda x, y: y / 3 + 2 * x,
        lambda x, x0, y0: ((y0 + 6 * x0 + 18) / math.exp(x0 / 3)) * math.exp(x / 3) - 6 * x - 18
    ],
    [
        "y' = x + y",
        lambda x, y: x + y,
        lambda x, x0, y0: ((y0 + x0 + 1) / math.exp(x0)) * math.exp(x) - x - 1
    ],
    [
        "y' = 2y + cos(x)",
        lambda x, y: 2 * y + math.cos(x),
        lambda x, x0, y0: (
            (y0 + 2 * math.cos(x0) / 5 - math.sin(x0) / 5) / math.exp(2 * x0)
        ) * math.exp(2 * x)
        + math.sin(x) / 5 - 2 * math.cos(x) / 5
    ],
    [
        "y' = y + (1 + x)·y²",
        lambda x, y: y + (1 + x) * y ** 2,
        lambda x, x0, y0: -math.exp(x) / (x * math.exp(x) - (x0 * math.exp(x0) * y0 + math.exp(x0)) / y0)
    ]
]

methods = [
    ("Метод Эйлера (p=1)", euler_method, 1, "o"),
    ("Метод Рунге-Кутта 4-го порядка (p=4)", rk4_method, 4, "s"),
    ("Метод Милна", milne_method, None, "^")
]


def read_float(prompt: str, positive: bool = False) -> float:
    while True:
        s = input(prompt).strip()
        try:
            v = float(s)
            if positive and v <= 0:
                print("Ошибка: введите положительное число.")
                continue
            return v
        except:
            print("Ошибка: нужно ввести вещественное число.")


def run_method(name: str, method_func, p: int, marker: str, f, y_true, x0, xn, y0, h_initial, eps) -> tuple[list[float], list[float], str, float]:
    print(f"\n=== {name} ===")
    h = h_initial
    min_pts = 4

    if p is None:
        needed = (xn - x0) / h + 1
        if needed < min_pts:
            print("Слишком большой шаг для метода Милна!")
            print(f"Нужно не менее {min_pts} точек: (xn − x0)/h +1 ≥ {min_pts}")
            h = (xn - x0) / (min_pts - 1)
            print("Автоматически назначен шаг h =", h)

    while True:
        xs_h, ys_h = method_func(f, x0, xn, y0, h)

        if p is not None:
            xs_h2, ys_h2 = method_func(f, x0, xn, y0, h / 2)
            y_h  = ys_h[-1]
            y_h2 = ys_h2[-1]
            inaccuracy = abs(y_h - y_h2) / (2 ** p - 1)

            if inaccuracy < eps:
                print(f"Достигнута точность ε = {eps:.2e} при эффективном шаге h = {h/2:g}")
                print("Погрешность:", f"{inaccuracy:.6g}")

                xs_tab = xs_h2
                ys_tab = ys_h2
                out_x = []
                out_y = []
                out_true = []
                out_err = []
                for xi, yi in zip(xs_tab, ys_tab):
                    yt = y_true(xi, x0, y0)
                    out_x.append(xi)
                    out_y.append(yi)
                    out_true.append(yt)
                    out_err.append(abs(yt - yi))
                print(tabulate(
                    list(zip(out_x, out_y, out_true, out_err)),
                    headers=["x", "y_num", "y_true", "погрешность"],
                    floatfmt=(".6g", ".6g", ".6g", ".6g")
                ))
                return xs_h2, ys_h2, name, inaccuracy
            else:
                h /= 2
                if h < 1e-6:
                    print("Шаг слишком мал, останавливаю подбор.")
                    return xs_h, ys_h, name, inaccuracy

        else:
            # оценка точности Милна
            errors = [abs(y_true(xi, x0, y0) - yi) for xi, yi in zip(xs_h, ys_h)]
            inaccuracy = max(errors)
            if inaccuracy <= eps:
                print(f"Достигнута точность ε = {eps:.2e} при эффективном шаге h = {h:g}")
                print("Погрешность:", f"{inaccuracy:.6g}")

                xs_tab = xs_h
                ys_tab = ys_h
                out_x = []
                out_y = []
                out_true = []
                out_err = []
                for xi, yi in zip(xs_tab, ys_tab):
                    yt = y_true(xi, x0, y0)
                    out_x.append(xi)
                    out_y.append(yi)
                    out_true.append(yt)
                    out_err.append(abs(yt - yi))
                print(tabulate(
                    list(zip(out_x, out_y, out_true, out_err)),
                    headers=["x", "y_num", "y_true", "погрешность"],
                    floatfmt=(".6g", ".6g", ".6g", ".6g")
                ))
                return xs_h, ys_h, name, inaccuracy
            else:
                h /= 2
                if h < 1e-6:
                    print("Шаг слишком мал, останавливаю подбор.")
                    return xs_h, ys_h, name, inaccuracy


def draw_combined(xs_all: list[list[float]],
                  ys_all: list[list[float]],
                  y_true_func,
                  x0: float,
                  y0: float,
                  names: list[str],
                  markers: list[str]):

    x_min = x0
    x_max = max(xs[-1] for xs in xs_all)
    x_plot = np.linspace(x_min, x_max, 400)
    y_plot = [y_true_func(x, x0, y0) for x in x_plot]

    plt.figure(figsize=(8, 6))
    plt.plot(x_plot, y_plot, "r-", label="Точное решение")

    colors = ["b", "g", "m"]
    for i in range(len(xs_all)):
        xs = xs_all[i]
        ys = ys_all[i]
        plt.plot(xs, ys, color=colors[i], linestyle="-", marker=markers[i], markersize=6, label=names[i])

    plt.title("Сравнение численных методов")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()


def main():
    print("=== Лабораторная №6: Численное решение ОДУ ===\n")
    for idx, entry in enumerate(funcs, start=1):
        print(f"{idx}) {entry[0]}")
    while True:
        try:
            choice = int(input("Ваш выбор (1–4): ").strip())
            if 1 <= choice <= len(funcs):
                break
            else:
                print("Ошибка: введите число от 1 до 4.")
        except:
            print("Ошибка: введите целое число.")
    desc, f, y_true = funcs[choice - 1]

    x0 = read_float("Введите x0 (начало): ")
    xn = read_float("Введите xn (конец, > x0): ")
    if xn <= x0:
        print("Ошибка: xn должен быть больше x0.")
        return
    y0 = read_float("Введите y(x0) = y0: ")
    h_initial = read_float("Введите начальный шаг h: ", positive=True)
    eps = read_float("Введите точность ε: ", positive=True)

    xs_all   = []
    ys_all   = []
    names    = []
    markers  = []

    for (name, method_func, p, marker) in methods:
        xs_h, ys_h, mname, inacc = run_method(
            name, method_func, p, marker,
            f, y_true, x0, xn, y0, h_initial, eps
        )
        xs_all.append(xs_h)
        ys_all.append(ys_h)
        names.append(mname)
        markers.append(marker)
        print("\n" + "-" * 60)

    draw_combined(xs_all, ys_all, y_true, x0, y0, names, markers)

    print("\n=== Работа завершена ===")


if __name__ == "__main__":
    main()
