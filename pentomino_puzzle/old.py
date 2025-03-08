import numpy as np


def rotate(matrix):
    """Rotate the matrix 90 degrees clockwise."""
    return np.rot90(matrix).tolist()


def reflect(matrix):
    """Reflect the matrix horizontally."""
    return [row[::-1] for row in matrix]


def generate_orientations(pentomino):
    """Generate all unique rotations and reflections of a pentomino."""
    orientations = set()
    current = pentomino
    
    # Generate four rotations
    for _ in range(4):
        current = rotate(current)
        orientations.add(tuple(map(tuple, current)))  # Convert to tuple for hashing
    
    # Generate four more with reflection
    current = reflect(pentomino)
    for _ in range(4):
        current = rotate(current)
        orientations.add(tuple(map(tuple, current)))

    # Convert back to list for usability
    return [list(map(list, orientation)) for orientation in orientations]


def can_place(space, pentomino, x, y):
    """
    Check if the pentomino can be placed on the grid at position (x, y).
    Constraints:
    - All pentomino cells should remain within grid bounds.
    - Pentomino cells must not overlap with existing filled cells.
    - Space may be non-rectangular or have holes (represented by -1).
    """

    for i in range(len(pentomino)):
        for j in range(len(pentomino[0])):
            if pentomino[i][j] == 1:  # Part of the pentomino shape
                # Check bounds for each cell
                new_x, new_y = x + i, y + j

                out_of_bounds = new_x >= len(space) or new_y >= len(space[0]) or new_x < 0 or new_y < 0
                try:
                    overlapping = space[new_x][new_y] != 0 # Overlapping a filled cell or in a hole
                except IndexError: # Indicates part of pentomino is out of bounds
                    overlapping = True
                    # print(f'new_x={new_x}, new_y={new_y} created an IndexError')

                if out_of_bounds or overlapping:
                    return False
    return True


def place_pentomino(space, pentomino, x, y, letter):
    """Place the pentomino on the grid at position (x, y) using its corresponding letter."""
    for i in range(len(pentomino)):
        for j in range(len(pentomino[0])):
            if pentomino[i][j] == 1:
                space[x + i][y + j] = letter
    return space


def remove_pentomino(space, pentomino, x, y):
    """Remove the pentomino from the grid by setting cells back to 0 at position (x, y)."""
    for i in range(len(pentomino)):
        for j in range(len(pentomino[0])):
            if pentomino[i][j] != 0:
                space[x + i][y + j] = 0
    return space
    

def is_fully_filled(space):
    """Check if the space has no empty cells left (all cells are 1)."""
    return all(cell != 0 for row in space for cell in row)


def can_fill_space(space, pentominos, letters):
    """
    Attempt to fill the space with a given list of pentominos, each represented by a unique letter.
    - `letters` is a list of letters corresponding to each pentomino in `pentominos`.
    """
    # Base case: if no pentominos left, check if the space is fully filled
    if is_fully_filled(space):
        return True

    current_pentomino = pentominos[0]
    current_letter = letters[0]  # Get the corresponding letter
    remaining_pentominos = pentominos[1:]
    remaining_letters = letters[1:]

    # Try each cell in the space as a possible top-left corner for this pentomino
    for x in range(len(space)):
        for y in range(len(space[0])):
            # Try each orientation of the current pentomino
            for orientation in generate_orientations(current_pentomino):
                if can_place(space, orientation, x, y):
                    # Place the pentomino with its corresponding letter
                    place_pentomino(space, orientation, x, y, current_letter)
                    if can_fill_space(space, remaining_pentominos, remaining_letters):
                        return True
                    # Backtrack if it leads to no solution
                    remove_pentomino(space, orientation, x, y)

    return False  # No solution found for this configuration


def show_pentominos(pentominos):
    """Print the pentominos in a human-readable format."""
    for pentomino in pentominos:
        for row in pentomino:
            print(''.join(['#' if cell == 1 else '.' for cell in row]))
        print()


def visualize_solution(space):
    """Print the solution space in a human-readable format."""
    for row in space:
        out = ''
        for cell in row:
            if cell == -1:
                out += ' '
            elif cell == 0:
                out += '.'
            else:
                out += cell

        print(out)



PENTOMINOS = [
    [[1, 0, 0], [1, 1, 1], [0, 0, 1]],
    [[0, 1, 0, 0], [1, 1, 1, 1]],
    [[0, 1, 0], [0, 1, 0], [1, 1, 1]],
    [[1, 1], [1, 1], [0, 1]],
    [[1, 0, 1], [1, 1, 1]],
    [[1, 0, 0], [1, 0, 0], [1, 1, 1]],
    [[1, 1, 1, 0], [0, 0, 1, 1]],
    [[1, 1, 1, 1], [0, 0, 0, 1]]
]

LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

def add_hole_in_space(space, date):
    assert 1 <= date <= 31, 'Invalid date'
    date_x, date_y = divmod(date - 1, 7)
    if date > 28:
        date_y += 4    
    space[date_x][date_y] = -1


SPACE = [[0 for _ in range(7)] for _ in range(4)] + [[-1, -1, -1, -1, 0, 0, 0]]
add_hole_in_space(SPACE, 22)

test_space = [[0 for _ in range(8)] for _ in range(5)]

can_fill_space(SPACE, PENTOMINOS, LABELS)
visualize_solution(SPACE)

