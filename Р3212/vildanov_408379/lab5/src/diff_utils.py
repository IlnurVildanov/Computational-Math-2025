def build_difference_table(xs, ys):
    n = len(xs)
    deltas = [ys.copy()]
    for i in range(1, n):
        row = []
        prev = deltas[i-1]
        for j in range(n - i):
            row.append(prev[j+1] - prev[j])
        deltas.append(row)
    return deltas

def print_difference_table(deltas):
    n = len(deltas[0])
    print("\nТаблица конечных разностей:")
    for j in range(n):
        for i in range(n - j):
            print(f"{deltas[i][j]:>10.4f}", end=" ")
        print()
    print()
