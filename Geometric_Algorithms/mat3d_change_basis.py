from .mat_helpers import Matrix, pretty

def change_of_basis_3d(bx, by, bz):
    return [[bx[0], by[0], bz[0]],
            [bx[1], by[1], bz[1]],
            [bx[2], by[2], bz[2]]]

def main():
    print("3D Change of Basis")
    B = change_of_basis_3d([1,0,0],[0,2,0],[1,1,1])
    print("B=\\n"+pretty(B))

if __name__ == "__main__":
    main()
