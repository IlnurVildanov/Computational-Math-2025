import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

def plot_interpolations(xs, ys, x0, methods):
    x_min, x_max = min(xs), max(xs)
    margin = (x_max - x_min)*0.05
    x_vals = np.linspace(x_min-margin, x_max+margin, 400)

    plt.figure()
    plt.title("Интерполяция функции")
    plt.xlabel("x")
    plt.ylabel("y")

    for name, func in methods:
        y_vals = [func(x) for x in x_vals]
        plt.plot(x_vals, y_vals, label=name, linewidth=1)

    plt.scatter(xs, ys, color='black', label='Точки')

    for name, func in methods:
        y0 = func(x0)
        plt.scatter([x0], [y0], marker='x', s=70, label=f"{name} в x={x0}")

    plt.legend(loc='best')
    plt.grid(True)
    plt.show()
