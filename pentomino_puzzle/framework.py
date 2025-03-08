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


def date_to_xy(date):
    assert 1 <= date <= 31, 'Invalid date'

    date_x, date_y = divmod(date - 1, 7)
    if date > 28:
        date_y += 4
    return date_x, date_y


def xy_to_date(x, y):
    if x <= 3:
        return x * 7 + y + 1
    elif x == 4 and 4 <= y <= 6:
        return 28 + y - 3
    else:
        raise ValueError(f'Invalid x, y coordinates - {x}, {y}')


def add_hole_in_space(space, date):
    date_x, date_y = date_to_xy(date)
    space[date_x][date_y] = -1


def can_place(space, piece, m):
    """
    Check if the piece can be placed on the grid at position (x, y).
    Constraints:
    - All piece cells should remain within grid bounds.
    - piece cells must not overlap with existing filled cells.
    - Space may be non-rectangular or have holes (represented by -1).
    """
    cells_filled = []
    x, y = date_to_xy(m)

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
                
                cells_filled.append(xy_to_date(new_x, new_y))
                
    return cells_filled


def place_piece(space, cells_filled):
    for m in cells_filled:
        x, y = date_to_xy(m)
        space[x][y] = 'b' if m % 2 else 'w'

def remove_piece(space, cells_filled):
    for m in cells_filled:
        x, y = date_to_xy(m)
        space[x][y] = 'B' if m % 2 else 'W'


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

    for hole_date in range(1, 32):

        my_space = [
            ['B', 'W', 'B', 'W', 'B', 'W', 'B'],
            ['W', 'B', 'W', 'B', 'W', 'B', 'W'],
            ['B', 'W', 'B', 'W', 'B', 'W', 'B'],
            ['W', 'B', 'W', 'B', 'W', 'B', 'W'],
            [-1, -1, -1, -1, 'B', 'W', 'B'],
        ]
        add_hole_in_space(my_space, hole_date)

        # Key: piece number, Value: list of cells filled
        my_dict = dict()
        for i in range(len(piece_set)):
            my_dict[i] = []

        for piece_number, p in enumerate(piece_set):
            for date in range(1, 32):
                for orientation in generate_orientations(p):
                    cells_filled = can_place(my_space, orientation, date)
                    if cells_filled:
                        my_dict[piece_number].append(cells_filled)


        main_dict[hole_date] = my_dict
        
    return main_dict
    


if __name__ == '__main__':
    md = create_main_dict(pentomino_set_A)
    with open('main_dict.pickle', 'wb') as f:
        pickle.dump(md, f)


