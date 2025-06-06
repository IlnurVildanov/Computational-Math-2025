import math
import numpy as np

def linear_approximation(X, Y):
    sx = sum(X)
    sxx = sum(x*x for x in X)
    sy = sum(Y)
    sxy = sum(x*y for x, y in zip(X, Y))
    A, B = np.linalg.solve([[len(X), sx], [sx, sxx]], [sy, sxy])
    return A, B

def square_approximation(X, Y):
    sx = sum(X)
    sxx = sum(x*x for x in X)
    sxxx = sum(x**3 for x in X)
    sxxxx = sum(x**4 for x in X)
    sy = sum(Y)
    sxy = sum(x*y for x, y in zip(X, Y))
    sxxy = sum(x*x*y for x, y in zip(X, Y))
    A, B, C = np.linalg.solve(
        [[len(X), sx, sxx],
         [sx, sxx, sxxx],
         [sxx, sxxx, sxxxx]],
        [sy, sxy, sxxy]
    )
    return A, B, C

def cube_approximation(X, Y):
    sx = sum(X)
    sxx = sum(x*x for x in X)
    sxxx = sum(x**3 for x in X)
    sxxxx = sum(x**4 for x in X)
    sxxxxx = sum(x**5 for x in X)
    sxxxxxx = sum(x**6 for x in X)
    sy = sum(Y)
    sxy = sum(x*y for x, y in zip(X, Y))
    sxxy = sum(x*x*y for x, y in zip(X, Y))
    sxxxy = sum(x**3 * y for x, y in zip(X, Y))
    A, B, C, D = np.linalg.solve(
        [[len(X), sx,   sxx,   sxxx],
         [sx,     sxx,  sxxx,  sxxxx],
         [sxx,    sxxx, sxxxx, sxxxxx],
         [sxxx,   sxxxx, sxxxxx, sxxxxxx]],
        [sy, sxy, sxxy, sxxxy]
    )
    return A, B, C, D

def exponential_approximation(X, Y):
    lnY = [math.log(y) for y in Y]
    A, b = linear_approximation(X, lnY)
    return math.exp(A), b

def logarithmic_approximation(X, Y):
    lnX = [math.log(x) for x in X]
    A, b = np.linalg.solve(
        [[len(X), sum(lnX)], [sum(lnX), sum(v*v for v in lnX)]],
        [sum(Y), sum(y*lx for y, lx in zip(Y, lnX))]
    )
    return A, b

def power_approximation(X, Y):
    lnX = [math.log(x) for x in X]
    lnY = [math.log(y) for y in Y]
    A, b = linear_approximation(lnX, lnY)
    return math.exp(A), b

def get_linear_approximation(X, Y):
    A, B = linear_approximation(X, Y)
    return lambda x: A + B*x

def get_square_approximation(X, Y):
    A, B, C = square_approximation(X, Y)
    return lambda x: A + B*x + C*x**2

def get_cube_approximation(X, Y):
    A, B, C, D = cube_approximation(X, Y)
    return lambda x: A + B*x + C*x**2 + D*x**3

def get_exponential_approximation(X, Y):
    A, b = exponential_approximation(X, Y)
    return lambda x: A * np.exp(b*x)

def get_logarithmic_approximation(X, Y):
    A, b = logarithmic_approximation(X, Y)
    return lambda x: A + b*np.log(x)

def get_power_approximation(X, Y):
    A, b = power_approximation(X, Y)
    return lambda x: A * x**b

def count_correlation(X, Y):
    mx, my = sum(X)/len(X), sum(Y)/len(Y)
    num = sum((x-mx)*(y-my) for x,y in zip(X,Y))
    den = math.sqrt(sum((x-mx)**2 for x in X) * sum((y-my)**2 for y in Y))
    return num/den

def count_R2(Y, PHI):
    m = sum(PHI)/len(PHI)
    ss_res = sum((y - p)**2 for y, p in zip(Y, PHI))
    ss_tot = sum((y - m)**2 for y in Y)
    return 1 - ss_res/ss_tot

def count_sigma(Y, PHI):
    n = len(Y)
    return math.sqrt(sum((y - p)**2 for y,p in zip(Y,PHI)) / n)

FUNCTIONS = [
    (linear_approximation, get_linear_approximation, "Линейная",
     lambda c: f"{c[1]:.3f}x + {c[0]:.3f}"),
    (square_approximation, get_square_approximation, "Полиноминальная 2-й степени",
     lambda c: f"{c[2]:.3f}x^2 + {c[1]:.3f}x + {c[0]:.3f}"),
    (cube_approximation, get_cube_approximation, "Полиноминальная 3-й степени",
     lambda c: f"{c[3]:.3f}x^3 + {c[2]:.3f}x^2 + {c[1]:.3f}x + {c[0]:.3f}"),
    (exponential_approximation, get_exponential_approximation, "Экспоненциальная",
     lambda c: f"{c[0]:.3f} * e^{c[1]:.3f}x"),
    (logarithmic_approximation, get_logarithmic_approximation, "Логарифмическая",
     lambda c: f"{c[1]:.3f} * ln(x) + {c[0]:.3f}"),
    (power_approximation, get_power_approximation, "Степенная",
     lambda c: f"{c[0]:.3f} * x^{c[1]:.3f}"),
]

def run_approximations(X, Y):
    results = []
    for approx, maker, name, fmt in FUNCTIONS:
        try:
            coeffs = approx(X, Y)
            phi = maker(X, Y)
            PHI = [phi(x) for x in X]
            sigma = count_sigma(Y, PHI)
            R2 = count_R2(Y, PHI)
            S = sum((y - p)**2 for y,p in zip(Y,PHI))
            r = count_correlation(X, Y) if name == "Линейная" else None
            results.append({
                "name": name,
                "formula": fmt(coeffs),
                "sigma": sigma,
                "R2": R2,
                "S": S,
                "r": r,
                "phi": phi
            })
        except Exception:
            pass
    return results
