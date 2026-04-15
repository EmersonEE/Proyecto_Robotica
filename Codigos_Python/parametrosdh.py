import sympy as sp

# ===== VARIABLES SIMBÓLICAS =====
theta2, theta3, theta4, theta5, theta6 = sp.symbols(
    "theta2 theta3 theta4 theta5 theta6"
)
d1 = sp.symbols("d1")


# ===== FUNCIÓN DH =====
def dh(theta, d, a, alpha):
    return sp.Matrix(
        [
            [
                sp.cos(theta),
                -sp.sin(theta) * sp.cos(alpha),
                sp.sin(theta) * sp.sin(alpha),
                a * sp.cos(theta),
            ],
            [
                sp.sin(theta),
                sp.cos(theta) * sp.cos(alpha),
                -sp.cos(theta) * sp.sin(alpha),
                a * sp.sin(theta),
            ],
            [0, sp.sin(alpha), sp.cos(alpha), d],
            [0, 0, 0, 1],
        ]
    )


# ===== MATRICES INDIVIDUALES =====
A1 = dh(0, d1, 0, 0)
A2 = dh(theta2, 0, 2, 0)
A3 = dh(theta3, 0, 0, 0)
A4 = dh(theta4, 0, 0, -sp.pi / 2)
A5 = dh(theta5, 0, 0, sp.pi / 2)
A6 = dh(theta6, 1, 0, 0)

# ===== CINEMÁTICA DIRECTA =====
T = A1 * A2 * A3 * A4 * A5 * A6

# ===== SIMPLIFICAR =====
T = sp.simplify(T)

# ===== RESULTADO =====
sp.pprint(T)
