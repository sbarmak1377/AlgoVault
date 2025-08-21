import math
from .mat_helpers import Matrix, mat_mul, mat_vec_mul, pretty

def rot_trans2d(theta_rad: float, tx: float, ty: float) -> Matrix:
    c, s = math.cos(theta_rad), math.sin(theta_rad)
    return [[c, -s, tx],
            [s,  c, ty],
            [0.0, 0.0, 1.0]]

def apply_hom2d(M: Matrix, x: float, y: float):
    vec = [x, y, 1.0]
    out = mat_vec_mul(M, vec)
    return [out[0]/out[2], out[1]/out[2]]

def main():
    print("2D Rotation & Translation (homogeneous)")
    M = rot_trans2d(math.pi/4, 3.0, -2.0)
    p = apply_hom2d(M, 1.0, 0.0)
    print("Transformed point:", p)

if __name__ == "__main__":
    main()
