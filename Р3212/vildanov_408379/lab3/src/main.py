import math
from tabulate import tabulate

from methods.left_rectangle import left_rectangle
from methods.right_rectangle import right_rectangle
from methods.mid_rectangle import mid_rectangle
from methods.trapezoid import trapezoid
from methods.simpson import simpson
from methods.runge import runge_integral
from plot_function import plot_function

def f1(x: float) -> float:
    return 1 / x

def F1(x: float) -> float:
    return math.log(abs(x))

def f2(x: float) -> float:
    return x**2

def F2(x: float) -> float:
    return x**3 / 3

def f3(x: float) -> float:
    return math.sin(x)

def F3(x: float) -> float:
    return -math.cos(x)

def f4(x: float) -> float:
    return -x**3 - x**2 + x + 3

def F4(x: float) -> float:
    return (-(x**4)/4) - (x**3)/3 + (x**2)/2 + 3*x

func_descriptions = {
    1: ("y = sin(x)",        f3, F3),
    2: ("y = 1/x",           f1, F1),
    3: ("y = -x^3 - x^2 + x + 3", f4, F4),
    4: ("y = x^2",           f2, F2),
}


methods_info = [
    ("Левые прямоугольники",    left_rectangle, 1),
    ("Правые прямоугольники",   right_rectangle, 1),
    ("Средние прямоугольники",  mid_rectangle,  2),
    ("Трапеции",                trapezoid,      2),
    ("Симпсон",                 simpson,        4),
]

def read_float(prompt: str, positive: bool = False) -> float:
    while True:
        try:
            s = input(prompt).strip()
            val = float(s)
            if positive and val <= 0:
                print("Ошибка: нужно ввести положительное число.")
                continue
            return val
        except ValueError:
            print("Ошибка: введите корректное число.")

def main() -> None:
    print("=== Лабораторная №3: Численное интегрирование ===\n")

    for idx, (desc, _, _) in func_descriptions.items():
        print(f"{idx}) {desc}")
    while True:
        try:
            choice = int(input("Ваш выбор (1–4): ").strip())
            if choice in func_descriptions:
                break
            print("Ошибка: выберите индекс от 1 до 4.")
        except ValueError:
            print("Ошибка: введите целое число.")
    desc, f, F_exact = func_descriptions[choice]

    a = read_float("Введите a (левая граница): ")
    b = read_float("Введите b (правая граница, > a): ")
    if b <= a:
        print("Ошибка: правая граница должна быть больше левой.")
        return

    eps = read_float("Введите точность ε (> 0): ", positive=True)

    print(f"\nВыбранная функция: {desc}")
    print(f"Интервал интегрирования: [{a}, {b}], ε = {eps:e}\n")

    plot_function(f, a, b)

    try:
        exact_val = F_exact(b) - F_exact(a)
        print(f"Точное значение ∫[{a}, {b}] f(x) dx = {exact_val:.8f}\n")
    except Exception:
        print("Точное значение не вычислено (нет подходящей первообразной).\n")

    results_table = []

    for method_name, method_func, order in methods_info:
        I_approx, n_used = runge_integral(method_func, f, a, b, eps, order)
        results_table.append((method_name, f"{I_approx:.8f}", n_used))

    print(tabulate(
        results_table,
        headers=["Метод", "I_approx", "n отрезков"],
        tablefmt="github"
    ))

    print("\n=== Расчёт завершён ===")

if __name__ == "__main__":
    main()
