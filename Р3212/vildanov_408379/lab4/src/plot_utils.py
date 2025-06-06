import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

def plot_results(X, Y, results):
    x_min, x_max = min(X), max(X)
    dx = (x_max - x_min) * 0.05
    x_vals = np.linspace(x_min - dx, x_max + dx, 400)

    all_y = list(Y)
    for res in results:
        yv = res["phi"](x_vals)
        all_y.extend(yv if isinstance(yv, np.ndarray) else list(yv))
    y_min, y_max = min(all_y), max(all_y)
    dy = (y_max - y_min) * 0.05 if y_max != y_min else max(abs(y_max),1)*0.05

    plt.figure()
    plt.title("Аппроксимация функции")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.scatter(X, Y, label="Вводные точки")
    for res in results:
        y_vals = res["phi"](x_vals)
        plt.plot(x_vals, y_vals, label=res["name"], linewidth=1)

    plt.xlim(x_min - dx, x_max + dx)
    plt.ylim(y_min - dy, y_max + dy)
    plt.legend()
    plt.grid(True)
    plt.show()
