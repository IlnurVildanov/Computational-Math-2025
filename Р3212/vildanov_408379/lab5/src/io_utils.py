import os
import math

generative_functions = [
    ("sin(x)", lambda x: math.sin(x)),
    ("e^x", lambda x: math.e ** x),
    ("3x^3-2x^2+4", lambda x: 3*x**3 - 2*x**2 + 4),
]

def read_points_console():
    print("Введите точки в формате `x y`. По окончании ввода введите `q`.")
    data = []
    while True:
        line = input().strip()
        if line.lower() == 'q':
            break
        parts = line.split()
        if len(parts) != 2:
            print("Неверный формат, нужно два числа или `q`.")
            continue
        try:
            x,y = float(parts[0]), float(parts[1])
        except ValueError:
            print("Не число, попробуйте снова.")
            continue
        data.append((x,y))
    return zip(*data)

def read_points_file():
    while True:
        fname = input("Введите имя файла с точками: ").strip()
        if not os.path.isfile(fname):
            print(f"Файл «{fname}» не найден. Попробуйте снова.")
            continue
        xs, ys = [], []
        with open(fname, encoding='utf-8') as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith('#'):
                    continue
                parts = s.split()
                if len(parts) != 2:
                    print(f"Пропускаю строку некорр.: {s}")
                    continue
                try:
                    x,y = float(parts[0]), float(parts[1])
                except ValueError:
                    print(f"Не могу распознать числа в: {s}")
                    continue
                xs.append(x); ys.append(y)
        if xs:
            return xs, ys
        print("В файле нет корректных точек.")

def generate_points():
    # Выбор функции
    print("Выберите функцию для генерации узлов:")
    for i,(name,_) in enumerate(generative_functions,1):
        print(f"  {i}. {name}")
    while True:
        idx = int(input("Ваш выбор: "))
        if 1 <= idx <= len(generative_functions):
            fname, f = generative_functions[idx-1]
            break
        print("Нет такой опции.")
    a = float(input("Введите нижнюю границу отрезка: "))
    b = float(input("Введите верхнюю границу отрезка: "))
    n = int(input("Введите число узлов: "))
    h = (b - a) / (n - 1)
    xs = [a + i*h for i in range(n)]
    ys = [f(x) for x in xs]
    return xs, ys

def choose_nodes():
    print("Выберите способ задания функции: консоль — 1, файл — 2, функция — 3")
    while True:
        choice = input("Ваш выбор: ").strip()
        if choice == '1':
            xs, ys = read_points_console()
            break
        if choice == '2':
            xs, ys = read_points_file()
            break
        if choice == '3':
            xs, ys = generate_points()
            break
        print("Введите 1, 2 или 3.")
    return list(xs), list(ys)

def choose_interpolation_point():
    x0 = float(input("Введите точку интерполяции: "))
    return x0
