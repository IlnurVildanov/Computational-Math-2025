import numpy as np
import matplotlib.pyplot as plt

def plot_function(f: callable, a: float, b: float, points: int = 500) -> None:
    xs = np.linspace(a, b, points)
    ys = [f(x) for x in xs]
    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, 'b-', label='f(x)')
    plt.title(f'График функции на [{a:.3g}, {b:.3g}]')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.show()
