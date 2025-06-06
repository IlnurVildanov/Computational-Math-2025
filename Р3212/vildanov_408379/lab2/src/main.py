import math
import sys

from methods.common_single import (
    read_interval_and_eps_from_keyboard,
    read_interval_and_eps_from_file,
    plot_function_on_segment,
    plot_function_with_point,
    equations_map
)
from methods.chord import chord_method
from methods.secant import secant_method
from methods.simple_iter import simple_iteration_method

from system.common_system import read_initial_guess_system, plot_two_equations
from system.newton_system import newton_system_method

SYSTEMS_MAP = {
    1: {
        'name': "Система 1: x² + 2·y² − 5 = 0;  e^x + y − 1 = 0",
        'functions': lambda x, y: (x**2 + 2*y**2 - 5, math.exp(x) + y - 1),
        'jacobian':  lambda x, y: [[2*x, 4*y], [math.exp(x), 1]]
    },
    2: {
        'name': "Система 2: sin(x) + x·y − 0.5 = 0;  x + cos(y) − 2 = 0",
        'functions': lambda x, y: (math.sin(x) + x*y - 0.5, x + math.cos(y) - 2),
        'jacobian':  lambda x, y: [[math.cos(x) + y, x], [1, -math.sin(y)]]
    }
}


def choose_single_equation():
    print("Доступные одиночные уравнения:")
    for idx, info in equations_map.items():
        print(f"  {idx}) {info['description']}")
    while True:
        s = input("Выберите номер уравнения: ").strip()
        if s.isdigit() and int(s) in equations_map:
            return int(s)
        print("Ошибка: введите корректный номер.")


def choose_system():
    print("Доступные системы:")
    for idx, info in SYSTEMS_MAP.items():
        print(f"  {idx}) {info['name']}")
    while True:
        s = input("Выберите номер системы (1 или 2): ").strip()
        if s.isdigit() and int(s) in SYSTEMS_MAP:
            return int(s)
        print("Ошибка: введите 1 или 2.")


def output_results(choice: str, lines: list[str]):
    if choice == 'console':
        for line in lines:
            print(line)
    else:
        filename = input("Введите имя файла для сохранения (например result.txt): ").strip()
        try:
            with open(filename, 'w') as f:
                for line in lines:
                    f.write(line + "\n")
            print(f"Результаты сохранены в файл '{filename}'")
        except Exception as e:
            print(f"Ошибка при записи в файл: {e}")
            print("Вывожу результат в консоль вместо файла:")
            for line in lines:
                print(line)


def solve_single_equation_flow():
    key = choose_single_equation()
    info = equations_map[key]
    f = info['f']
    phi = info['phi']
    phi_prime = info['phi_prime']

    print("\nСпособ ввода:")
    print("  1) С клавиатуры")
    print("  2) Из файла")
    mode = input("Ваш выбор (1/2): ").strip()
    if mode == '1':
        a, b, eps = read_interval_and_eps_from_keyboard()
    elif mode == '2':
        res = read_interval_and_eps_from_file("input_single.txt")
        if res is None:
            print("Не удалось считать из файла. Проверьте формат.")
            return
        a, b, eps = res
    else:
        print("Ошибка: нужно ввести 1 или 2.")
        return

    try:
        fa = f(a)
        fb = f(b)
        if fa * fb > 0:
            print("\nНа отрезке [a, b] нет гарантии единственного корня.")
            return
    except Exception as e:
        print(f"Ошибка при вычислении f(a) или f(b): {e}")
        return

    print("\nМетоды уточнения корня:")
    print("  1) Метод хорд")
    print("  2) Метод секущих")
    print("  3) Метод простой итерации")
    choice = input("Выберите метод (1–3): ").strip()
    if choice not in ('1', '2', '3'):
        print("Ошибка: нужно ввести 1, 2 или 3.")
        return

    try:
        if choice == '1':
            print("\n---- Метод хорд ----")
            print("Выберите форму:")
            print("  a) фиксируем левый конец (x₀ = b)")
            print("  b) фиксируем правый конец (x₀ = a)")
            form = input("Ваш выбор (a/b): ").strip().lower()
            if form == 'a':
                root, fval, iters = chord_method(f, a, b, eps, max_iters=1000, fixed_end='left')
            elif form == 'b':
                root, fval, iters = chord_method(f, a, b, eps, max_iters=1000, fixed_end='right')
            else:
                print("Ошибка: нужно 'a' или 'b'.")
                return

        elif choice == '2':
            print("\n---- Метод секущих ----")
            root, fval, iters = secant_method(f, a, b, eps, max_iters=1000)

        else:
            print("\n---- Метод простой итерации ----")
            root, fval, iters = simple_iteration_method(f, phi, phi_prime, a, b, eps, max_iters=1000)

    except Exception as e:
        print(f"\nОшибка во время работы метода: {e}")
        return

    lines = []
    lines.append(f"=== Результат одиночного уравнения ({info['description']}) ===")
    lines.append(f"Корень x* = {root:.6f}")
    lines.append(f"f(x*) = {fval:.6e}")
    lines.append(f"Число итераций: {iters}")
    lines.append(f"Точность ε = {eps}")
    lines.append("="*40)

    print("\nВывод результата:")
    print("  1) В консоль")
    print("  2) В файл")
    outm = input("Ваш выбор (1/2): ").strip()
    if outm == '1':
        output_results('console', lines)
    elif outm == '2':
        output_results('file', lines)
    else:
        print("Ошибка: неверный выбор. Вывожу в консоль.")
        output_results('console', lines)

    print("\n(Строим график функции…)")
    plot_function_with_point(f, a, b, root)

def solve_system_flow():
    key = choose_system()
    info = SYSTEMS_MAP[key]
    system = {
        'name': info['name'],
        'functions': info['functions'],
        'jacobian': info['jacobian']
    }

    print("\nВведите начальные приближения для x₀ и y₀:")
    x0, y0 = read_initial_guess_system()

    while True:
        s = input("Введите ε (точность для системы, float > 0): ").strip()
        try:
            eps = float(s)
            if eps > 0:
                break
        except:
            pass
        print("Ошибка: ε должно быть положительным вещественным.")
    max_iters = 200

    try:
        x_root, y_root, errors, iters = newton_system_method(system, x0, y0, eps, max_iters)
    except Exception as e:
        print(f"Ошибка в методе Ньютона для системы: {e}")
        return

    lines = []
    lines.append(f"=== Результат для системы ({system['name']}) ===")
    lines.append(f"Найденное решение: x* = {x_root:.6f}, y* = {y_root:.6f}")
    lines.append(f"Число итераций: {iters}")
    lines.append(f"Вектор погрешностей: {errors}")
    f1_final, f2_final = system['functions'](x_root, y_root)
    lines.append(f"Проверка: f₁(x*,y*) = {f1_final:.2e}, f₂(x*,y*) = {f2_final:.2e}")
    lines.append("="*40)

    print("\nВывод результата:")
    print("  1) В консоль")
    print("  2) В файл")
    outm = input("Ваш выбор (1/2): ").strip()
    if outm == '1':
        output_results('console', lines)
    elif outm == '2':
        output_results('file', lines)
    else:
        print("Ошибка: неверный выбор. Вывожу в консоль.")
        output_results('console', lines)

    print("\n(Строим график системы…)")
    plot_two_equations(system, (x_root, y_root))


if __name__ == "__main__":
    print("=== Решение нелинейных уравнений и систем нелинейных уравнений ===\n")
    print("1) Нелинейное уравнение")
    print("2) Система нелинейных уравнений")
    choice = input("Выберите (1/2): ").strip()
    if choice == '1':
        solve_single_equation_flow()
    elif choice == '2':
        solve_system_flow()
    else:
        print("Ошибка: нужно ввести 1 или 2.")