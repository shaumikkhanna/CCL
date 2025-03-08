import numpy as np
import pickle


piece_list = np.array([ # AS ROWS   
    [0, 1, 1, 1, 1],
    [0, 1, 1, 0, 1],
    [0, 0, 1, 1, 1],
    [0, 1, 0, 1, 1],
    [1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1],
    [0, 0, 1, 0, 1],
    [0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0],
    [1, 0, 0, 0, 1]
])


def get_all_mtx_rows(piece_ind):
    """
    Here is the matrix row structure --
    [10 10 25]
    10 -- Indicates which piece has been used (10 pieces)
    10 -- Indicates which row / column has been occupied (5 rows + 5 columns)
    25 -- The actual matrix (5x5) indicating if that element is occupied or not
    """
    
    piece = piece_list[piece_ind]
    out = []

    # 2 orientations for flipping
    for orientation in [piece, piece[::-1]]:

        # Place as a row
        for i in range(5):
            mtx = np.zeros((5, 5), dtype=int)
            mtx[i] = orientation

            # Indicate that this row has been occupied
            new_row = np.zeros(10, dtype=int)
            new_row[i] = 1

            out.append(np.concatenate((new_row, mtx.reshape(-1))))

        # Place as a column
        for i in range(5):
            mtx = np.zeros((5, 5), dtype=int)
            mtx[:, i] = orientation

            # Indicate that this row has been occupied
            new_row = np.zeros(10, dtype=int)
            new_row[i + 5] = 1

            out.append(np.concatenate((new_row, mtx.reshape(-1))))

    # Indicate that this piece has been used
    indicator_mtx = np.zeros((20, 10), dtype=int)
    indicator_mtx[:, piece_ind] = 1
    
    return np.concatenate((indicator_mtx, np.array(out)), axis=1)    


def save_mtx():
    out = []
    for i in range(10):
        out.append(get_all_mtx_rows(i))

    M = np.concatenate(out, axis=0)
    with open('M.pkl', 'wb') as f:
        pickle.dump(M, f)


if __name__ == '__main__':
    # save_mtx()
    pass


