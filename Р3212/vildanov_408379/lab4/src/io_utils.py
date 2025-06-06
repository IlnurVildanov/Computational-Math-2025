import os

def choose_input():
    while True:
        choice = input("Выберите способ ввода: консоль — '1', файл — '2': ").strip()
        if choice == '1':
            data = []
            print("Введите точки в формате `x y`. По окончании ввода введите `q`.")
            while True:
                line = input().strip()
                if line.lower() == 'q':
                    break
                parts = line.split()
                if len(parts) != 2:
                    print("Неверный формат, введите два числа через пробел или `q`.")
                    continue
                try:
                    x, y = float(parts[0]), float(parts[1])
                except ValueError:
                    print("Ошибка: не число. Попробуйте снова.")
                    continue
                data.append((x, y))
            if not data:
                print("Нет ни одной точки! Попробуйте заново.")
                continue

        elif choice == '2':
            filename = input("Введите имя входного файла: ").strip()
            if not os.path.isfile(filename):
                print(f"Файл '{filename}' не найден.")
                continue
            data = []
            with open(filename, encoding='utf-8') as f:
                for line in f:
                    s = line.strip()
                    if not s or s.startswith('#'):
                        continue
                    parts = s.split()
                    if len(parts) != 2:
                        print(f"Пропускаю строку с неверным форматом: {s}")
                        continue
                    try:
                        x, y = float(parts[0]), float(parts[1])
                    except ValueError:
                        print(f"Не могу преобразовать числа в строке: {s}")
                        continue
                    data.append((x, y))
            if not data:
                print("В файле нет корректных точек. Выберите другой файл.")
                continue

        else:
            print("Введите '1' или '2'.")
            continue

        X, Y = zip(*data)
        n = len(X)
        if not (8 <= n <= 12):
            print(f"Ошибка: требуется от 8 до 12 точек, у вас {n}. Попробуйте снова.\n")
            continue

        return list(X), list(Y)


def choose_output():
    while True:
        choice = input("Выберите способ вывода: консоль — '1', файл — '2': ").strip()
        if choice == '1':
            return None
        elif choice == '2':
            return "result.txt"
        else:
            print("Введите '1' или '2'.")
