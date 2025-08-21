from .mat_helpers import Matrix, mat_mul, pretty

def change_of_basis_2d(bx, by):
    """
    Columns bx, by are the basis vectors in the old coordinates.
    Returns matrix that maps coordinates in the new basis to old basis.
    """
    return [[bx[0], by[0]],
            [bx[1], by[1]]]

def main():
    print("2D Change of Basis")
    B = change_of_basis_2d([2,0], [1,1])
    print("Basis matrix B=\\n"+pretty(B))

if __name__ == "__main__":
    main()
