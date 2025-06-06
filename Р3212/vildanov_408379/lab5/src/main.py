from io_utils import choose_nodes, choose_interpolation_point
from diff_utils import build_difference_table, print_difference_table
from interpolation import (lagrange, newton_divided, newton_finite, stirling, bessel, is_equidistant)
from plot_utils import plot_interpolations

def main():
    xs, ys = choose_nodes()

    x0 = choose_interpolation_point()

    deltas = build_difference_table(xs, ys)
    print_difference_table(deltas)

    methods = [
        ("Лагранжа", lagrange(xs, ys)),
        ("Ньютона (разд.)", newton_divided(xs, ys)),
    ]

    if is_equidistant(xs):
        methods.append(("Ньютона (кон.)", newton_finite(xs, ys, deltas)))

        try:
            methods.append(("Стирлинга", stirling(xs, ys, deltas)))
        except ValueError as e:
            print("Интерполирующая функция Стирлинга → ОШИБКА:", e)

        try:
            methods.append(("Бесселя", bessel(xs, ys, deltas)))
        except ValueError as e:
            print("Интерполирующая функция Бесселя → ОШИБКА:", e)
    else:
        print("Стирлинга и Бесселя пропущены: узлы неравномерные")

    print()
    for name, func in methods:
        try:
            val = func(x0)
            print(f"Интерполирующая функция: Интерполяционный многочлен {name}")
            print(f"P({x0}) = {val}")
        except Exception as err:
            print(f"{name} → ОШИБКА при вычислении: {err}")
        print("="*50)

    plot_interpolations(xs, ys, x0, methods)

if __name__ == "__main__":
    main()
