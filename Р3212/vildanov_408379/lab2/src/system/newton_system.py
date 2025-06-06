import math

def newton_system_method(system: dict, x0: float, y0: float, tol: float, max_iters: int = 100):
    f1f2 = system['functions']
    jac = system['jacobian']

    x, y = x0, y0
    errors = []

    for k in range(1, max_iters + 1):
        f1_val, f2_val = f1f2(x, y)
        J11, J12 = jac(x, y)[0]
        J21, J22 = jac(x, y)[1]
        det = J11 * J22 - J12 * J21
        if abs(det) < 1e-14:
            raise ValueError("Якобиан вырождён (det≈0).")

        # dx dy через формулу Крамера
        dx = (-f1_val * J22 + f2_val * J12) / det
        dy = (J11 * (-f2_val) + f1_val * J21) / det

        x_new = x + dx
        y_new = y + dy
        err = math.hypot(dx, dy)
        errors.append(err)

        if err < tol:
            return x_new, y_new, errors, k

        x, y = x_new, y_new

    raise RuntimeError("Ньютон (система): не сошлось за max_iters.")