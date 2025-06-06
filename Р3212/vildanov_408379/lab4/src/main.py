from io_utils import choose_input, choose_output
from approximations import run_approximations
from plot_utils import plot_results

def quality_R2(R2):
    if R2 >= 0.95:
        return "Высокая аппроксимация"
    elif R2 >= 0.75:
        return "Удовлетворительная аппроксимация"
    elif R2 >= 0.5:
        return "Слабая аппроксимация"
    else:
        return "Нет аппроксимации"

def format_result(res):
    lines = [
        f"Аппроксимирующая функция: {res['name']}",
        f"Функция: φ(x) = {res['formula']}",
        f"Среднеквадратичное отклонение: σ = {res['sigma']:.3f}",
        f"Коэффициент детерминации: R² = {res['R2']:.3f} ({quality_R2(res['R2'])})",
        f"Мера отклонения (SSE): S = {res['S']:.3f}",
        "",
        # печатаем массивы
        "Массивы значений:",
        "xᵢ: " + ", ".join(f"{x:.3f}" for x in res['X']),
        "yᵢ: " + ", ".join(f"{y:.3f}" for y in res['Y']),
        "φ(xᵢ): " + ", ".join(f"{p:.3f}" for p in res['PHI_list']),
        "εᵢ: " + ", ".join(f"{e:.3f}" for e in res['EPS_list']),
        "=" * 50
    ]
    if res['r'] is not None:
        lines.insert(5, f"Коэффициент корреляции Пирсона: r = {res['r']:.3f}")
    return "\n".join(lines)

def main():
    X, Y = choose_input()

    results = run_approximations(X, Y)

    for r in results:
        r['X'] = X
        r['Y'] = Y
        phi_list = [r['phi'](x) for x in X]
        r['PHI_list'] = phi_list
        r['EPS_list'] = [p - y for p, y in zip(phi_list, Y)]

    best = max(results, key=lambda r: r['R2'])

    out_file = choose_output()
    if out_file:
        with open(out_file, 'w', encoding='utf-8') as f:
            for r in results:
                f.write(format_result(r) + "\n")
            f.write(f"\nЛучшая аппроксимирующая функция: {best['name']}\n")
            f.write(f"Формула: φ(x) = {best['formula']}\n")
        print(f"Результаты сохранены в {out_file}")
    else:
        for r in results:
            print(format_result(r))
        print(f"Лучшая аппроксимирующая функция: {best['name']}")
        print(f"Формула: φ(x) = {best['formula']}")

    plot_results(X, Y, results)

if __name__ == "__main__":
    main()
