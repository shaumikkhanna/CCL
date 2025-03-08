import numpy as np
import pickle
from itertools import combinations
from dlx import DancingLinks


def dual_piece(piece):
    new_piece = []
    for row in piece:
        new_row = []
        for cell in row:
            if cell == 'W':
                new_row.append('B')
            elif cell == 'B':
                new_row.append('W')
            else:
                new_row.append(cell)
        new_piece.append(new_row)

    return new_piece 


def rotate(piece):
    return np.rot90(piece).tolist()


def reflect(piece):
    true_reflection = [row[::-1] for row in piece]
    return dual_piece(true_reflection)


def generate_orientations(piece):
    """Generate all unique rotations and reflections of a piece."""

    orientations = set()
    current = piece
    
    for _ in range(4):
        current = rotate(current)
        orientations.add(tuple(map(tuple, current)))
    
    current = reflect(piece)

    for _ in range(4):
        current = rotate(current)
        orientations.add(tuple(map(tuple, current)))
    
    return [list(map(list, orientation)) for orientation in orientations]


def print_piece(piece):
    for row in piece:
        print(''.join(str(cell) for cell in row))
    print()


def m_to_xy(m):
    assert 1 <= m < 43, 'Invalid m'

    m_x, m_y = divmod(m - 1, 7)
    return m_x, m_y


def xy_to_m(x, y):
    if 0 <= x < 6 and 0 <= y < 7:
        return 7 * x + y + 1
    else:
        raise ValueError(f'Invalid x, y coordinates - {x}, {y}')


def add_hole_in_space(space, m):
    m_x, m_y = m_to_xy(m)
    space[m_x][m_y] = -1


def can_place(space, piece, m):
    """
    Check if the piece can be placed on the grid at position m.
    Constraints:
    - All piece cells should remain within grid bounds.
    - piece cells must not overlap with existing filled cells.
    - Space may be non-rectangular or have holes (represented by -1).
    """
    cells_filled = []
    x, y = m_to_xy(m)

    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] in ['B', 'W']:  # Part of the piece shape

                # Check bounds for each cell
                new_x, new_y = x + i, y + j
                # print(f'new_x={new_x}, new_y={new_y}, x={x}, y={y}, i={i}, j={j}')
                # Out of bounds
                if new_x >= len(space) or new_y >= len(space[0]) or new_x < 0 or new_y < 0:
                    # print('Out of bounds')
                    return False
                
                # Check color coding
                try:
                    if space[new_x][new_y] != piece[i][j]:
                        return False
                    # if space[new_x][new_y] == -1:
                    #     return False
                except IndexError: # Indicates part of piece is out of bounds
                    return False
                
                cells_filled.append(xy_to_m(new_x, new_y))
                
    return cells_filled


def place_piece(space, cells_filled):
    for m in cells_filled:
        x, y = m_to_xy(m)
        space[x][y] = 'b' if m % 2 else 'w'

def remove_piece(space, cells_filled):
    for m in cells_filled:
        x, y = m_to_xy(m)
        space[x][y] = 'B' if m % 2 else 'W'


def print_space(space):
    # Print each row with each element padded to the maximum width
    for row in space:
        row_str = ""
        for item in row:
            if item == -1:
                item = '.'
            elif item == 'b':
                item = '0'
            elif item == 'w':
                item = '1'
            row_str += f"{str(item):<{5}} "
        print(row_str.strip())

    print()


def create_main_dict(piece_set):
    """
    Creates a dictionary where - 

    Key: Date where the hole is placed
    Value: Another dictionary where -

    Key: Piece number in the piece set
    Value: All possible arrangements of the piece on the grid, where one arrangement is the list of squares / dates covered
    """

    main_dict = dict()

    for hole1, hole2 in combinations(range(36, 43), 2):

        my_space = [
            ['B', 'W', 'B', 'W', 'B', 'W', 'B'],
            ['W', 'B', 'W', 'B', 'W', 'B', 'W'],
            ['B', 'W', 'B', 'W', 'B', 'W', 'B'],
            ['W', 'B', 'W', 'B', 'W', 'B', 'W'],
            ['B', 'W', 'B', 'W', 'B', 'W', 'B'],
            [-1, -1, 'B', 'W', 'B', 'W', 'B'],
        ]
        add_hole_in_space(my_space, hole1)
        add_hole_in_space(my_space, hole2)

        # Key: piece number, Value: list of cells filled
        my_dict = dict()
        for i in range(len(piece_set)):
            my_dict[i] = []

        for piece_number, p in enumerate(piece_set):
            for m in range(1, 43):
                for orientation in generate_orientations(p):
                    cells_filled = can_place(my_space, orientation, m)
                    if cells_filled:
                        my_dict[piece_number].append(cells_filled)


        main_dict[(hole1, hole2)] = my_dict
        
    return main_dict
    

def save_main_dict(piece_set, filename):
    md = create_main_dict(piece_set)
    with open(filename, 'wb') as f:
        pickle.dump(md, f)


def create_matrix(piece_numbers, holes):
    dancing_links_matrix = []
    for shift, piece_number in enumerate(piece_numbers):
        for cells_filled in my_dict[piece_number]:

            # 40 columns for the 40 dates and one hot encoding for the piece number
            new_row = [0 for _ in range(40 + len(piece_numbers))]

            for cell in cells_filled:
                new_row[cell - 1] = 1

            new_row[40 + shift] = 1
            dancing_links_matrix.append(new_row)


    dancing_links_matrix = np.array(dancing_links_matrix)

    # Remove columns with all zeros which are holes
    dancing_links_matrix = np.delete(dancing_links_matrix, [holes[0] - 1, holes[1] - 1], axis=1)

    return dancing_links_matrix


def main(piece_numbers, holes, multi_solution_flag=False):
    dancing_links_matrix = create_matrix(piece_numbers, holes)
    # indices of the columns where all the values are zero

    dl = DancingLinks(dancing_links_matrix)

    hole1, hole2 = min(holes), max(holes)

    if multi_solution_flag:
        dl.search(multi_solution_flag=True)
        # return dl.no_of_solutions

        for solution in dl.all_solutions:
            for mtx_ind, piece_number in zip(solution, piece_numbers):
                print(f'\nPiece number = {piece_number} ---', end = ' ')
                for ind, cell in enumerate(dancing_links_matrix[mtx_ind][:40]):
                    if cell == 1:
                        if ind < hole1 - 1:
                            print(ind + 1, end=' ')
                        elif ind < hole2 - 1:
                            print(ind + 2, end=' ')
                        else:
                            print(ind + 3, end=' ')
            print('\n')
        return


    solution = dl.solve()

    # Show the solution
    if solution:
        for mtx_ind, piece_number in zip(solution, piece_numbers):
            print(f'\nPiece number = {piece_number} ---', end=' ')
            for ind, cell in enumerate(dancing_links_matrix[mtx_ind][:40]):
                if cell == 1:
                    if ind < hole1 - 1:
                        print(ind + 1, end=' ')
                    elif ind < hole2 - 1:
                        print(ind + 2, end=' ')
                    else:
                        print(ind + 3, end=' ')
        print()
        return True
    else:
        print('No solution')
        return False


if __name__ == '__main__':

    pentomino_set_A = [
        [
            ['W', 0, 0], 
            ['B', 'W', 'B'], 
            [0, 0, 'W']
        ],
        [
            [0, 'B', 0, 0], 
            ['B', 'W', 'B', 'W']
        ],
        [
            [0, 'B', 0], 
            [0, 'W', 0], 
            ['W', 'B', 'W']
        ],
        [
            ['B', 'W'], 
            ['W', 'B'], 
            [0, 'W']
        ],
        [
            ['B', 0, 'B'], 
            ['W', 'B', 'W']
        ],
        [
            ['B', 0, 0], 
            ['W', 0, 0], 
            ['B', 'W', 'B']
        ],
        [
            ['B', 'W', 'B', 0], 
            [0, 0, 'W', 'B']
        ],
        [
            ['W', 'B', 'W', 'B'], 
            [0, 0, 0, 'W']
        ],
        [
            ['B', 'W', 'B', 'W'],
        ],
        [
            ['B', 'W', 'B'],
            [0, 0, 'W'],
        ],
        [
            ['B', 'W', 0],
            [0, 'B', 'W'],
        ],
        [
            ['B', 'W', 'B'],
            ['W', 'B', 'W'],
        ]
    ]

    with open('mini_dict.pickle', 'rb') as f:
        main_dict = pickle.load(f)

    for holes, my_dict in main_dict.items():
        print(f'Holes = {holes}')
        my_space = [
                ['B', 'W', 'B', 'W', 'B', 'W', 'B'],
                ['W', 'B', 'W', 'B', 'W', 'B', 'W'],
                ['B', 'W', 'B', 'W', 'B', 'W', 'B'],
                ['W', 'B', 'W', 'B', 'W', 'B', 'W'],
                ['B', 'W', 'B', 'W', 'B', 'W', 'B'],
                ['W', 'B', 'W', 'B', 'W', 'B', 'W'],
            ]
        add_hole_in_space(my_space, holes[0])
        add_hole_in_space(my_space, holes[1])

        main([0, 1, 2, 3, 4, 5, 6, 7], holes)
        break

    

    # p = pentomino_set_A[4]

    # for m in range(1, 43):
    #     print(f"m = {m}")
    #     for orientation in generate_orientations(p):
    #         cells_filled = can_place(my_space, orientation, m)
    #         if cells_filled:
    #             place_piece(my_space, cells_filled)
    #             print_space(my_space)
    #             remove_piece(my_space, cells_filled)
    #             print()


