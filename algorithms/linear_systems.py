import numpy as np

def gauss_elimination(a: np.ndarray, b: np.ndarray):
    if a.shape[0] != a.shape[1]:
        raise ValueError("Matrix A must be a square matrix")
    if b.shape[1] != 1 or a.shape[0] != b.shape[0]:
        raise ValueError("Matrix b must be a column matrix whose number of rows equals the degree of matrix A.")

    a_prim = np.copy(a)
    b_prim = np.copy(b)

    E = 1.0**(-8)

    rows, cols = a_prim.shape

    print(a_prim, end = "\n\n")
    for k in range(cols - 1):
        d_max = a_prim[k, k]
        d_max_i = k
        for i in range(k + 1, rows):
            if abs(d_max) < abs(a_prim[i, k]):
                d_max = a_prim[i, k]
                d_max_i = i

        if abs(d_max) < E:
            continue

        if d_max_i != k:
            a_prim[[k, d_max_i]] = a_prim[[d_max_i, k]]


        for i in range(k + 1, rows):
            d = a_prim[i, k] / d_max
            for j in range(cols):
                a_prim[i, j] = a_prim[i, j] - d * a_prim[k, j]
            b_prim[i, 0] = b_prim[i, 0] - d * b_prim[k, 0]

    x = np.full(b_prim.shape, 0.0)
    for i in range(cols - 1, -1, -1):
        the_sum = 0.0
        for j in range(i + 1, cols):
            the_sum = the_sum + a_prim[i, j] * x[j, 0]
        x[i, 0] = (b_prim[i, 0] - the_sum)/ a_prim[i,i]

    return x




    # for k = rows:-1: 1
    #   suma = 0;
    #   for i = rows:-1: (k + 1)
    #      suma = suma + A(k, i) * x(i);
    #   end
    #   x(k) = (A(k, cols) - suma) / A(k, k);
    # end
