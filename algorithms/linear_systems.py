import numpy as np

def gauss_elimination(a: np.ndarray, b: np.ndarray):
    if a.shape[0] != a.shape[1]:
        raise ValueError("Matrix A must be a square matrix")
    if b.shape[1] != 1 or a.shape[0] != b.shape[0]:
        raise ValueError("Matrix b must be a column matrix whose number of rows equals the degree of matrix A.")

    a_prim = np.copy(a)
    b_prim = np.copy(b)

    E = 10**(-8)

    rows, cols = a_prim.shape
    print(b_prim)
    for k in range(cols - 1):
        print(f"Numer iteracji: {k}")
        d_max = a_prim[k, k]
        d_max_i = k
        for i in range(k + 1, rows):
            if abs(d_max) < abs(a_prim[i, k]):
                d_max = a_prim[i, k]
                d_max_i = i
        print(E)
        if abs(d_max) < E:
            print(f"d_max: {d_max}")
            continue

        if d_max_i != k:
            a_prim[[k, d_max_i]] = a_prim[[d_max_i, k]]
            b_prim[[k, d_max_i]] = b_prim[[d_max_i, k]]

        for i in range(k + 1, rows):
            d = a_prim[i, k] / d_max
            for j in range(cols):
                a_prim[i, j] = a_prim[i, j] - d * a_prim[k, j]
            b_prim[i, 0] = b_prim[i, 0] - d * b_prim[k, 0]

        print(a_prim, b_prim, sep="\n\n")

    x = np.full(b_prim.shape, 0.0)
    for i in range(cols - 1, -1, -1):
        the_sum = 0.0
        for j in range(i + 1, cols):
            the_sum = the_sum + a_prim[i, j] * x[j, 0]
        x[i, 0] = (b_prim[i, 0] - the_sum)/ a_prim[i,i]

    return x

def jacobian(a: np.ndarray, b: np.ndarray):
    if a.shape[0] != a.shape[1]:
        raise ValueError("Matrix A must be a square matrix")
    if b.shape[1] != 1 or a.shape[0] != b.shape[0]:
        raise ValueError("Matrix b must be a column matrix whose number of rows equals the degree of matrix A.")

    n_max = 500
    E = 1**(-8)

    H = np.copy(a)
    G = np.copy(b)

    rows, cols = H.shape

    the_max_sum = 0.0
    for i in range(rows):
        G[i, 0] = G[i, 0] / H[i, i]
        for j in range(cols):
            H[i, j] = -H[i,j]/H[i,i]
        H[i,i] = 0.0
        the_sum = 0.0
        for j in range(cols):
            the_sum = the_sum + abs(H[i,j])

        if the_max_sum < the_sum:
            the_max_sum = the_sum

    x_n = None
    if 1 == 0:
        raise ArithmeticError
    else:
        x_0 = np.copy(G)
        x_n = np.copy(x_0)

        for k in range(n_max):

            for i in range(rows):
                the_sum = 0.0
                for j in range(cols):
                    the_sum = the_sum + H[i, j] * x_0[j, 0]
                x_n[i, 0] = G[i, 0] + the_sum
            x_0 = np.copy(x_n)

            if np.abs(x_0 - x_n).all() < E:
                break

        return x_n

