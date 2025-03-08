import pickle
from dlx import DancingLinks
import numpy as np
from string import ascii_uppercase as au


def load_big_mtx():
    with open("big_mtx.pkl", "rb") as f:
        return pickle.load(f)



def create_row_restriction(big_M, row_restriction: str, row_number: int):
    """
    Returns the index of the row in the matrix that satisfies the restriction
    """
    cols_to_be_removed = []
    row_index = row_number - 1

    # Piece restriction
    piece_number, flipped_flag = divmod(au.index(row_restriction), 2)
    cols_to_be_removed.append(piece_number)

    # Row occupation restriction
    cols_to_be_removed.append(10 + row_index)

    # Matrix restriction
    mtx = np.zeros((5, 5), dtype=int)
    piece = piece_list[piece_number] if not flipped_flag else piece_list[piece_number][::-1]
    mtx[row_index] = piece

    cols_to_be_removed.extend([x + 20 for x in np.where(mtx.reshape(-1) == 1)][0])

    return np.where(np.all(big_M[:, cols_to_be_removed] == 1, axis=1))[0][0]


def create_col_restriction(big_M, col_restriction: str, col_number: int):
    """
    Returns the index of the row in the matrix that satisfies the restriction
    """
    cols_to_be_removed = []
    col_index = col_number - 1

    # Piece restriction
    piece_number, flipped_flag = divmod(int(col_restriction) - 1, 2)
    cols_to_be_removed.append(piece_number)

    # Col occupation restriction
    cols_to_be_removed.append(15 + col_index)

    # Matrix restriction
    mtx = np.zeros((5, 5), dtype=int)
    piece = piece_list[piece_number] if not flipped_flag else piece_list[piece_number][::-1]
    mtx[:, col_index] = piece

    cols_to_be_removed.extend([x + 20 for x in np.where(mtx.reshape(-1) == 1)][0])

    return np.where(np.all(big_M[:, cols_to_be_removed] == 1, axis=1))[0][0]


def create_restriction(big_m, restriction, number):
    if restriction in au:
        return create_row_restriction(big_m, restriction, number)
    else:
        return create_col_restriction(big_m, restriction, number)



def main():
    M = load_big_mtx()

    pre_solution = []
    while True:
        input_piece = input('Enter piece number / "solve": ')
        if input_piece == "solve":
            print('\n')
            break

        input_row_col = int(input('Enter row / col number: '))
        assert 1 <= input_row_col <= 5, "Row / Col number should be between 1 and 5"
        pre_solution.append(create_restriction(M, input_piece, input_row_col))


    dl = DancingLinks(M)
    sol = dl.solve(pre_solution=pre_solution)

    if not sol:
        print("No solution found")
        return

    for ind in sol:
        mtx_row = M[ind]
        print(f'Piece number: {np.where(mtx_row[:10] == 1)[0][0]}')
        row_flag, col_flag = mtx_row[10:15], mtx_row[15:20]

        if row_flag.sum():
            print(f'Filling Row number: {np.argmax(row_flag == 1) + 1}')
        elif col_flag.sum():
            print(f'Filling Column number: {np.argmax(col_flag == 1) + 1}')
        else:
            print('Error')

        print(mtx_row[20:].reshape(5, 5))
        print()



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

if __name__ == '__main__':
    main()

