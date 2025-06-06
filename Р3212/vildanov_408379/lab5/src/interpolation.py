from functools import reduce
import math

def lagrange(xs, ys):
    n = len(xs)
    def P(x):
        total = 0
        for i in range(n):
            term = ys[i]
            for j in range(n):
                if i != j:
                    term *= (x - xs[j])/(xs[i] - xs[j])
            total += term
        return total
    return P

def newton_divided(xs, ys):
    n = len(xs)
    coeffs = [ys[0]] * n
    def compute(a, b):
        if a == b:
            return ys[a]
        num = compute(a+1, b) - compute(a, b-1)
        den = xs[b] - xs[a]
        res = num/den
        if a == 0:
            coeffs[b] = res
        return res
    compute(0, n-1)
    def P(x):
        res = coeffs[0]
        prod = 1
        for k in range(1, n):
            prod *= (x - xs[k-1])
            res += coeffs[k] * prod
        return res
    return P

def is_equidistant(xs, tol=1e-8):
    h = xs[1] - xs[0]
    return all(abs((xs[i] - xs[i-1]) - h) < tol for i in range(2, len(xs)))

def newton_finite(xs, ys, deltas):
    def P(x):
        h = xs[1] - xs[0]
        mid = (xs[0] + xs[-1]) / 2
        if x <= mid:
            t = (x - xs[0]) / h
            res = deltas[0][0]
            for i in range(1, len(deltas)):
                term = deltas[i][0]
                for j in range(i):
                    term *= (t - j)
                term /= math.factorial(i)
                res += term
            return res
        else:
            t = (x - xs[-1]) / h
            res = deltas[0][-1]
            for i in range(1, len(deltas)):
                term = deltas[i][-1]
                for j in range(i):
                    term *= (t + j)
                term /= math.factorial(i)
                res += term
            return res
    return P

def stirling(xs, ys, deltas):
    n = len(xs)
    if not is_equidistant(xs) or n % 2 == 0:
        raise ValueError("Для многочлена Стирлинга нужны нечётные равномерные узлы")
    def P(x):
        zero = n // 2
        h = xs[1] - xs[0]
        t = (x - xs[zero]) / h
        res = ys[zero]
        for i in range(1, zero+1):
            d1 = deltas[2*i-1][zero - i]
            d2 = deltas[2*i-1][zero - i + 1]
            num = d1 + d2
            term = t
            for j in range(1, i):
                term *= (t**2 - j**2)
            term *= num/(2 * math.factorial(2*i-1))
            res += term
            d  = deltas[2*i][zero - i]
            term2 = 1
            for j in range(i):
                term2 *= (t**2 - j**2)
            term2 *= d/math.factorial(2*i)
            res += term2
        return res
    return P

def bessel(xs, ys, deltas):
    n = len(xs)
    if not is_equidistant(xs) or n % 2 != 0:
        raise ValueError("Число узлов должно быть чётным и равномерным")
    def P(x):
        zero = n//2 - 1
        h = xs[1] - xs[0]
        t = (x - xs[zero]) / h
        res = 0
        for i in range(zero+1):
            d_even = deltas[2*i][zero - i]
            term_e = 1
            for j in range(-i, i):
                term_e *= (t + j)
            term_e *= (d_even)/(math.factorial(2*i)*2)
            res += term_e

            if 2*i+1 < len(deltas):
                d_odd = deltas[2*i+1][zero - i]
                term_o = (t - 0.5)
                for j in range(-i, i):
                    term_o *= (t + j)
                term_o *= d_odd/math.factorial(2*i+1)
                res += term_o
        return res
    return P
