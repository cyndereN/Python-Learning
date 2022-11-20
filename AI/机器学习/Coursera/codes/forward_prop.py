X = np.array([200, 17])
W = np.array([[1, -3, 5], 
              [-2, 4, 6]])
b = np.array([-1, 1, 2])

def dense(a_in, W, b, g):
    units = W.shape[1]
    a_out = np.zeros(units)
    for j in range(units):
        w = W[:, j]
        z = np.dot(w, a_in) + b[j]
        a_out[j] = g(z)
    return a_out  # [1, 0 ,1]

# Matrix
X = np.array([200, 17])
W = np.array([[1, -3, 5], 
              [-2, 4, 6]])
B = np.array([[-1, 1, 2]])

def dense(a_in, W, b, g):
    # Vectorized
    Z = np.matmul(A_in, W) + B
    A_out = g(Z)
    return A_out  # [[1, 0 ,1]]


def sequential(x):
    a1 = dense(x, W1, b1)
    a2 = dense(a2, W2, b2)
    a3 = dense(a3, W3, b3)
    a4 = dense(a4, W4, b4)
    f_x = a4
    return f_x