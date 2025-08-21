from typing import List
import math
from .mat_helpers import Matrix, mat_mul, mat_vec_mul, pretty

def rot2d(theta_rad: float) -> Matrix:
    c, s = math.cos(theta_rad), math.sin(theta_rad)
    return [[c, -s],[s, c]]

def scale2d(sx: float, sy: float) -> Matrix:
    return [[sx, 0.0],[0.0, sy]]

def main():
    print("2D Rotation & Scale")
    R = rot2d(math.pi/6)
    S = scale2d(2.0, 0.5)
    RS = mat_mul(R, S)
    v = [1.0, 1.0]
    print("R*S =\\n"+pretty(RS))
    print("RS * v =", mat_vec_mul(RS, v))

if __name__ == "__main__":
    main()
