import pickle


def normalize(board):
    """
    Normalize the board to its canonical form by applying rotations and reflections
    and choosing the lexicographically smallest configuration.
    """
    transformations = [
        lambda b: b,                                       # original
        lambda b: [b[2], b[5], b[8], b[1], b[4], b[7], b[0], b[3], b[6]],  # rotate 270
        lambda b: [b[8], b[7], b[6], b[5], b[4], b[3], b[2], b[1], b[0]],  # rotate 180
        lambda b: [b[6], b[3], b[0], b[7], b[4], b[1], b[8], b[5], b[2]],  # rotate 90
        lambda b: [b[2], b[1], b[0], b[5], b[4], b[3], b[8], b[7], b[6]],  # reflect horizontally
        lambda b: [b[6], b[7], b[8], b[3], b[4], b[5], b[0], b[1], b[2]],  # reflect vertically
        lambda b: [b[8], b[5], b[2], b[7], b[4], b[1], b[6], b[3], b[0]],  # diagonal top-left to bottom-right
        lambda b: [b[0], b[3], b[6], b[1], b[4], b[7], b[2], b[5], b[8]]   # diagonal top-right to bottom-left
    ]
    
    # Return the lexicographically smallest transformation
    sister_boards = ["".join(trans(board)) for trans in transformations]
    min_ind, min_board = 0, sister_boards[0]

    for ind, sister_board in enumerate(sister_boards[1:]):
        if sister_board < min_board:
            min_ind, min_board = ind + 1, sister_board

    return min_ind, min_board


with open('all_boards.pkl', 'rb') as f:
    all_boards = pickle.load(f)


def main():
    moves = []

    while True:
        str_board_input = input('Enter the board configuration: ("game" for game over) \n')
        
        if str_board_input == 'game': # Game over
            print(moves)
            moves = []
            continue
        
        try:
            ind, str_board = normalize(str_board_input.upper()) # Normalize the board configuration
            board_number = all_boards.index(str_board) # Find the board number
            
            print(f'Board number: {board_number} : Rotation number: {ind}')
            moves.append((board_number, ind))
        
        except ValueError:
            print("Board not found") # Something went wrong
        except IndexError:
            print("Incorrect format input") # Something went wrong



if __name__ == '__main__':
    main()

