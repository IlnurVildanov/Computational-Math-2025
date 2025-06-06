import math
import random

def is_integer(s: str) -> bool:
    s2 = s.strip()
    if s2.startswith('-'):
        s2 = s2[1:]
    return s2.isdigit()

def is_float(s: str) -> bool:
    s2 = s.strip()
    if s2.startswith('-'):
        s2 = s2[1:]
    if s2.count('.') > 1:
        return False
    if '.' in s2:
        parts = s2.split('.')
        return all(part.isdigit() for part in parts if part != '')
    return s2.isdigit()

def read_matrix_file(filename: str):
    try:
        f = open(filename, 'r')
    except IOError:
        return None
    lines = [line.strip() for line in f if line.strip() != '']
    f.close()
    if len(lines) < 3:
        return None
    # n
    if not is_integer(lines[0]):
        return None
    n = int(lines[0])
    if n <= 0:
        return None
    # tol
    if not is_float(lines[1]):
        return None
    tol = float(lines[1])
    if tol <= 0:
        return None
    # max_iters
    if not is_integer(lines[2]):
        return None
    max_iters = int(lines[2])
    if max_iters <= 0:
        return None
    data_lines = lines[3:]
    if len(data_lines) != n:
        return None
    mat = []
    for row_str in data_lines:
        parts = row_str.split()
        if len(parts) != n + 1:
            return None
        if not all(is_float(tok) for tok in parts):
            return None
        mat.append([float(tok) for tok in parts])
    return mat, n, tol, max_iters

def read_matrix_user():
    while True:
        s = input("Введите порядок системы (целое > 0): ").strip()
        if is_integer(s) and int(s) > 0:
            n = int(s)
            break
        print("Ошибка: нужно целое положительное число.")
    while True:
        s = input("Введите точность (вещественное > 0): ").strip()
        if is_float(s) and float(s) > 0:
            tol = float(s)
            break
        print("Ошибка: нужно вещественное число > 0.")
    while True:
        s = input("Введите макс. число итераций (целое > 0): ").strip()
        if is_integer(s) and int(s) > 0:
            max_iters = int(s)
            break
        print("Ошибка: нужно целое число > 0.")
    print(f"Теперь введите расширенную матрицу ({n} строк по {n+1} чисел):")
    mat = []
    for i in range(n):
        row_str = input(f"Строка {i+1}: ").strip().split()
        if len(row_str) != n + 1:
            return None
        if not all(is_float(tok) for tok in row_str):
            return None
        mat.append([float(tok) for tok in row_str])
    return mat, n, tol, max_iters

def random_matrix():
    while True:
        s = input("Введите порядок системы (целое > 0): ").strip()
        if is_integer(s) and int(s) > 0:
            n = int(s)
            break
        print("Ошибка: нужно целое положительное число.")
    while True:
        s = input("Введите точность (вещественное > 0): ").strip()
        if is_float(s) and float(s) > 0:
            tol = float(s)
            break
        print("Ошибка: нужно вещественное число > 0.")
    while True:
        s = input("Введите макс. число итераций (целое > 0): ").strip()
        if is_integer(s) and int(s) > 0:
            max_iters = int(s)
            break
        print("Ошибка: нужно целое число > 0.")
    mat = [[float(random.randint(1, 9)) for _ in range(n + 1)] for _ in range(n)]
    return mat, n, tol, max_iters

def check_diagonal(mat):
    n = len(mat)
    strict_found = False
    for i in range(n):
        s = 0.0
        for j in range(n):
            if i == j:
                continue
            s += abs(mat[i][j])
        if abs(mat[i][i]) < s:
            return False
        if abs(mat[i][i]) > s:
            strict_found = True
    return strict_found

def matrix_norm(mat):
    n = len(mat)
    best = 0.0
    for i in range(n):
        row_sum = sum(abs(mat[i][j]) for j in range(n))
        if row_sum > best:
            best = row_sum
    return best

def gauss_seidel(mat, n, tol, max_iters, order):
    x_old = [0.0] * n
    x_new = [0.0] * n
    errors = [0.0] * n
    iters = 0
    diff = tol + 1.0

    while diff > tol and iters < max_iters:
        for i in range(n):
            s = 0.0
            for j in range(n):
                if j != i:
                    s += mat[i][j] * x_new[j]
            x_new[i] = (mat[i][n] - s) / mat[i][i]

        diff = 0.0
        for i in range(n):
            d = abs(x_new[i] - x_old[i])
            errors[i] = d
            if d > diff:
                diff = d

        x_old = x_new.copy()
        iters += 1

    if diff > tol:
        return None, None, iters

    final = [0.0] * n
    for idx_new, orig_idx in enumerate(order):
        final[orig_idx] = x_new[idx_new]
    return final, errors, iters

def print_matrix(mat):
    n = len(mat)
    for i in range(n):
        line = " ".join(f"{mat[i][j]:>7.3f}" for j in range(n))
        line += " | " + f"{mat[i][n]:>7.3f}"
        print(line)
