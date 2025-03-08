import numpy as np
import pickle


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
                except IndexError: # Indicates part of piece is out of bounds
                    return False
                
                cells_filled.append(xy_to_m(new_x, new_y))
                
    return cells_filled


def print_space(space):
    max_width = 6

    # Print each row with each element padded to the maximum width
    for row in space:
        row_str = ""
        for item in row:
            if item == -1:
                item = '.'
            elif item == 'b':
                item = '\U0001F4A9'
            elif item == 'w':
                item = '\U0001F480'
            row_str += f"{str(item):<{max_width}} "
        print(row_str.strip())

    print()


def xy_to_m(x, y):
    if 0 <= x <= 1:
        if 0 <= y <= 5:
            return -11 + 6 * x + y
        else:
            raise ValueError(f'Invalid y -- x = {x}, y = {y}')
    elif 2 <= x <= 6:
        if 0 <= y <= 6:
            return 7*x + y - 13
        else:
            raise ValueError(f'Invalid y -- x = {x}, y = {y}')
    elif x == 7:
        if 4 <= y <= 6:
            return 32 + y
        else:
            raise ValueError(f'Invalid y -- x = {x}, y = {y}')
    else:
        raise ValueError(f'Invalid x -- x = {x}, y = {y}')


def m_to_xy(m):
    if -11 <= m <= 0:
        return int(m >= -5), (m + 11) % 6
    elif 1 <= m <= 35:
        x, y = divmod(m - 1, 7)
        return x + 2, y
    elif 36 <= m <= 38:
        return 7, m - 32
    else:
        raise ValueError(f'Invalid m -- {m}')



def add_hole_in_space(space, m):
    x, y = m_to_xy(m)
    space[x][y] = -1


def place_piece(space, cells_filled):
    for m in cells_filled:
        x, y = m_to_xy(m)
        if space[x][y] == 'B':
            space[x][y] = 'b'
        elif space[x][y] == 'W':
            space[x][y] = 'w'
        else:
            raise ValueError(f'Invalid space -- {space[x][y]}')


def remove_piece(space, cells_filled):
    for m in cells_filled:
        x, y = m_to_xy(m)
        if space[x][y] == 'b':
            space[x][y] = 'B'
        elif space[x][y] == 'w':
            space[x][y] = 'W'
        else:
            raise ValueError(f'Invalid space -- {space[x][y]}')


def is_valid_m_triple(m_triple):
    if -11 <= m_triple[0] <= 0 and 1 <= m_triple[1] <= 31 and 32 <= m_triple[2] <= 38:
        if m_triple[0] == -10:
            return m_triple[1] <= 29
        elif m_triple[0] in [-10, -8, -6, -3, -1]:
            return m_triple[1] <= 30
        return True
    
    return False


def get_all_m_triples():
    for m1 in range(-11, 1):
        for m2 in range(1, 32):
            for m3 in range(32, 39):
                if is_valid_m_triple((m1, m2, m3)):
                    yield (m1, m2, m3)



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
            ['B', 'W', 'B', 'W', 'B', 'W', -1],
            ['W', 'B', 'W', 'B', 'W', 'B', -1],
            ['B', 'W', 'B', 'W', 'B', 'W', 'B'],
            ['W', 'B', 'W', 'B', 'W', 'B', 'W'],
            ['B', 'W', 'B', 'W', 'B', 'W', 'B'],
            ['W', 'B', 'W', 'B', 'W', 'B', 'W'],
            ['B', 'W', 'B', 'W', 'B', 'W', 'B'],
            [-1, -1, -1, -1, 'W', 'B', 'W'],
        ]
        add_hole_in_space(my_space, m_triple_hole[0])
        add_hole_in_space(my_space, m_triple_hole[1])
        add_hole_in_space(my_space, m_triple_hole[2])

        # Key: piece number, Value: list of cells filled
        my_dict = dict()
        for i in range(len(piece_set)):
            my_dict[i] = []

        for piece_number, p in enumerate(piece_set):
            for date in range(-11, 39):
                for orientation in generate_orientations(p):
                    cells_filled = can_place(my_space, orientation, date)
                    if cells_filled:
                        my_dict[piece_number].append(cells_filled)


        main_dict[m_triple_hole] = my_dict
        
    return main_dict
    

if __name__ == '__main__':
    my_space = [
        ['B', 'W', 'B', 'W', 'B', 'W', -1],
        ['W', 'B', 'W', 'B', 'W', 'B', -1],
        ['B', 'W', 'B', 'W', 'B', 'W', 'B'],
        ['W', 'B', 'W', 'B', 'W', 'B', 'W'],
        ['B', 'W', 'B', 'W', 'B', 'W', 'B'],
        ['W', 'B', 'W', 'B', 'W', 'B', 'W'],
        ['B', 'W', 'B', 'W', 'B', 'W', 'B'],
        [-1, -1, -1, -1, 'W', 'B', 'W'],
    ]


    md = create_main_dict(pentomino_set_A)
    with open('main_dict_full.pickle', 'wb') as f:
        pickle.dump(md, f)


    # p = pentomino_set_A[0]
    
    # m_triple = (-1, 15, 36)
    # for m in m_triple:
    #     add_hole_in_space(my_space, m)

    # for m in range(-11, 39):
    #     print(f'm = {m}')
    #     for orientation in generate_orientations(p):
    #         cells_filled = can_place(my_space, orientation, m)
    #         if cells_filled:
    #             place_piece(my_space, cells_filled)
    #             print_space(my_space)
    #             remove_piece(my_space, cells_filled)
    #             print()


