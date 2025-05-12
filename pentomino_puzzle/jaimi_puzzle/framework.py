import numpy as np
import pickle
import datetime



def rotate(piece):
    return np.rot90(piece).tolist()


def reflect(piece):
    true_reflection = [row[::-1] for row in piece]
    return true_reflection


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


def can_place(space, piece, m):
    """
    Check if the piece can be placed on the grid at position m = (x, y).
    Constraints:
    - All piece cells should remain within grid bounds.
    - piece cells must not overlap with existing filled cells.
    - Space may be non-rectangular or have holes (represented by -1).
    """
    cells_filled = []
    x, y = m_to_xy(m)

    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j]:  # Part of the piece shape

                # Check bounds for each cell
                new_x, new_y = x + i, y + j

                # Out of bounds
                if new_x >= len(space) or new_y >= len(space[0]) or new_x < 0 or new_y < 0:
                    # print('Out of bounds')
                    return False
                
                # Check holes
                try:
                    if space[new_x][new_y] == -1:
                        return False
                except IndexError: # Indicates part of piece is out of bounds
                    return False
                
                cells_filled.append(xy_to_m(new_x, new_y))
                
    return cells_filled


def print_space(space):
    max_width = 1

    # Print each row with each element padded to the maximum width
    for row in space:
        row_str = ""
        for item in row:
            if item == -1:
                item = '.'
            elif item == 1:
                item = '1'
            elif item == 0:
                item = '0'
            row_str += f"{str(item):<{max_width}} "
        print(row_str.strip())

    print()


def xy_to_m(x, y):
    if 0 <= x <= 6:
        if 0 <= y <= 6:
            return 7 * x + y + 1
        else:
            raise ValueError(f'Invalid y -- x = {x}, y = {y}')
    elif x == 7:
        if 3 <= y <= 6:
            return 47 + y
        else:
            raise ValueError(f'Invalid y -- x = {x}, y = {y}')
    else:
        raise ValueError(f'Invalid x -- x = {x}, y = {y}')


def m_to_xy(m):
    if 1 <= m <= 49:
        return divmod(m - 1, 7)
    elif 50 <= m <= 53:
        return 7, m - 47
    else:
        raise ValueError(f'Invalid m -- {m}')


def add_hole_in_space(space, m):
    x, y = m_to_xy(m)
    space[x][y] = -1


def place_piece(space, cells_filled):
    for m in cells_filled:
        x, y = m_to_xy(m)
        if space[x][y] == 0:
            space[x][y] = 1
        else:
            raise ValueError(f'Invalid space -- {space[x][y]}')


def remove_piece(space, cells_filled):
    for m in cells_filled:
        x, y = m_to_xy(m)
        if space[x][y] == 1:
            space[x][y] = 0
        else:
            raise ValueError(f'Invalid space -- {space[x][y]}')


def get_all_m_triples():
    for month in range(1, 13):
        for date in range(1, 32):

            try:
                dt = datetime.datetime(2025, month, date)
                day = dt.weekday() + 1
            except ValueError:
                continue

            m_month = month if 1 <= month <= 6 else month + 1
            m_date = date + 14
            m_day = day + 45 if 1 <= day <= 4 else day + 46

            yield (m_month, m_date, m_day)


def create_main_dict(piece_set):
    """
    Creates a dictionary where - 

    Key: Date where the hole is placed
    Value: Another dictionary where -

    Key: Piece number in the piece set
    Value: All possible arrangements of the piece on the grid, where one arrangement is the list of squares / dates covered
    """

    main_dict = dict()

    for m_triple_hole in get_all_m_triples():

        my_space = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, 0, 0, 0, 0],
        ]

        add_hole_in_space(my_space, m_triple_hole[0])
        add_hole_in_space(my_space, m_triple_hole[1])
        add_hole_in_space(my_space, m_triple_hole[2])

        # Key: piece number, Value: list of cells filled
        my_dict = dict()
        for i in range(len(piece_set)):
            my_dict[i] = []

        for piece_number, p in enumerate(piece_set):
            for m in range(1, 54):
                for orientation in generate_orientations(p):
                    cells_filled = can_place(my_space, orientation, m)
                    if cells_filled:
                        my_dict[piece_number].append(cells_filled)


        main_dict[m_triple_hole] = my_dict
        
    return main_dict



pentomino_set = [
    [
        [1, 0, 0], 
        [1, 1, 1], 
        [0, 0, 1]
    ],
    [
        [0, 1, 0, 0], 
        [1, 1, 1, 1]
    ],
    [
        [0, 1, 0], 
        [0, 1, 0], 
        [1, 1, 1]
    ],
    [
        [1, 1], 
        [1, 1], 
        [0, 1]
    ],
    [
        [1, 0, 1], 
        [1, 1, 1]
    ],
    [
        [1, 0, 0], 
        [1, 0, 0], 
        [1, 1, 1]
    ],
    [
        [1, 1, 1, 0], 
        [0, 0, 1, 1]
    ],
    [
        [1, 1, 1, 1], 
        [0, 0, 0, 1]
    ],
    [
        [1, 1, 1, 1, 1]
    ],
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 1]
    ],
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ],
    [
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 1]
    ],
]


if __name__ == '__main__':
    pass

    md = create_main_dict(pentomino_set)
    # with open('main_dict_full.pickle', 'wb') as f:
    #     pickle.dump(md, f)


    # my_space = [
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [-1, -1, -1, 0, 0, 0, 0],
    # ]

    # p = pentomino_set[1]
    # m_triple = (6, 39, 48)
    # for m in m_triple:
    #     add_hole_in_space(my_space, m)

    # for m in range(1, 54):
    #     print(f'm = {m}')
    #     for orientation in generate_orientations(p):
    #         cells_filled = can_place(my_space, orientation, m)
    #         if cells_filled:
    #             place_piece(my_space, cells_filled)
    #             print_space(my_space)
    #             remove_piece(my_space, cells_filled)
    #             print()


