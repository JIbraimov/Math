import numpy as np
from hypothesis import given, strategies as st, example
from math import pi

# === Пример линейного преобразования ===
def rotate_x_by(angle):
    """Поворот вектора в 3D вокруг оси X на угол angle (в радианах)."""
    c, s = np.cos(angle), np.sin(angle)
    R = np.array([[1, 0, 0],
                  [0, c, -s],
                  [0, s, c]])
    return lambda v: R @ v

# === Пример нелинейного преобразования ===
def square_coords(v):
    return v ** 2


# === Стратегия генерации случайных векторов ===
vector_strategy = st.lists(st.floats(-10, 10, allow_nan=False, allow_infinity=False), min_size=3, max_size=3)
scalar_strategy = st.floats(-10, 10, allow_nan=False, allow_infinity=False)


# === Тест аддитивности ===
@given(u=vector_strategy, v=vector_strategy)
def test_additivity(u, v):
    T = rotate_x_by(pi / 2)
    u, v = np.array(u), np.array(v)
    left = T(u + v)
    right = T(u) + T(v)
    assert np.allclose(left, right, atol=1e-6)

# === Тест масштабирования ===
@given(a=scalar_strategy, u=vector_strategy)
def test_homogeneity(a, u):
    T = rotate_x_by(pi / 2)
    u = np.array(u)
    left = T(a * u)
    right = a * T(u)
    assert np.allclose(left, right, atol=1e-6)

