from functions import (
    read_matrix_file,
    read_matrix_user,
    random_matrix,
    check_diagonal,
    matrix_norm,
    gauss_seidel,
    print_matrix
)

def main():
    print("=== Решение СЛАУ методом Гаусса–Зейделя ===")
    print("1) Ввод с клавиатуры")
    print("2) Загрузка из файла")
    print("3) Случайная матрица")
    choice = input("Выберите режим (1/2/3): ").strip()

    if choice == "1":
        data = read_matrix_user()
    elif choice == "2":
        data = read_matrix_file("input.txt")
    elif choice == "3":
        data = random_matrix()
    else:
        print("Некорректный выбор, выход.")
        return

    if data is None:
        print("\nОшибка при получении матрицы. Проверьте ввод.")
        return

    mat, n, tol, max_iters = data

    print("\n=== Введённая (или загруженная) расширенная матрица ===")
    print_matrix(mat)
    print(f"\nТочность: {tol:.6g}")
    print(f"Максимум итераций: {max_iters}\n")

    order = list(range(n))

    if check_diagonal(mat):
        print("Диагональное преобладание выполняется.\n")
    else:
        print("Нет диагонального преобладания, идет перестановка столбцов...\n")
        for i in range(n):
            s = sum(abs(mat[i][j]) for j in range(n) if j != i)
            if abs(mat[i][i]) < s:
                best_j = i
                best_val = abs(mat[i][i])
                for j in range(n):
                    if j != i and abs(mat[i][j]) > best_val:
                        best_val = abs(mat[i][j])
                        best_j = j
                if best_j != i and best_val > s:
                    for row in range(n):
                        mat[row][i], mat[row][best_j] = mat[row][best_j], mat[row][i]
                    order[i], order[best_j] = order[best_j], order[i]
                    if check_diagonal(mat):
                        break

        if check_diagonal(mat):
            print("Достигнуто диагональное преобладание после перестановки.\n")
        else:
            print("Не удалось обеспечить диагональное преобладание.\n")

        print("=== Новый вид матрицы после перестановок ===")
        print_matrix(mat)
        print()

    for i in range(n):
        if abs(mat[i][i]) < 1e-15:
            print("На диагонали найден ноль, решение невозможно.")
            return

    norm_val = matrix_norm(mat)
    print(f"Норма матрицы коэффициентов: {norm_val:.6g}\n")

    solution, errors, iters = gauss_seidel(mat, n, tol, max_iters, order)
    if solution is None:
        print(f"[НЕ СОШЛОСЬ] На {iters}-й итерации не удалось добиться точности {tol}.")
        return

    print(f"Решение найдено за {iters} итераций:")
    print("Вектор решений x =", solution)
    print("Вектор погрешностей r =", errors)

if __name__ == "__main__":
    main()
