import math
from .mat_helpers import Matrix, mat_mul, pretty

def rot3d_x(theta): 
    c,s = math.cos(theta), math.sin(theta)
    return [[1,0,0],[0,c,-s],[0,s,c]]

def rot3d_y(theta): 
    c,s = math.cos(theta), math.sin(theta)
    return [[c,0,s],[0,1,0],[-s,0,c]]

def rot3d_z(theta): 
    c,s = math.cos(theta), math.sin(theta)
    return [[c,-s,0],[s,c,0],[0,0,1]]

def scale3d(sx, sy, sz):
    return [[sx,0,0],[0,sy,0],[0,0,sz]]

def main():
    print("3D Rotation & Scale")
    R = rot3d_z(math.pi/3)
    S = scale3d(1,2,0.5)
    RS = mat_mul(R, S)
    print("R*S=\\n"+pretty(RS))

if __name__ == "__main__":
    main()
