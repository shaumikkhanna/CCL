from itertools import permutations

def normalize(board):
    """
    Normalize the board to its canonical form by applying rotations and reflections
    and choosing the lexicographically smallest configuration.
    """
    transformations = [
        lambda b: b,                                       # original
        lambda b: [b[6], b[3], b[0], b[7], b[4], b[1], b[8], b[5], b[2]],  # rotate 90
        lambda b: [b[8], b[7], b[6], b[5], b[4], b[3], b[2], b[1], b[0]],  # rotate 180
        lambda b: [b[2], b[5], b[8], b[1], b[4], b[7], b[0], b[3], b[6]],  # rotate 270
        lambda b: [b[2], b[1], b[0], b[5], b[4], b[3], b[8], b[7], b[6]],  # reflect horizontally
        lambda b: [b[6], b[7], b[8], b[3], b[4], b[5], b[0], b[1], b[2]],  # reflect vertically
        lambda b: [b[8], b[5], b[2], b[7], b[4], b[1], b[6], b[3], b[0]],  # diagonal top-left to bottom-right
        lambda b: [b[0], b[3], b[6], b[1], b[4], b[7], b[2], b[5], b[8]]   # diagonal top-right to bottom-left
    ]
    # Return the lexicographically smallest transformation
    return min("".join(trans(board)) for trans in transformations)

def check_win(board):
    """
    Check if there is a three-in-a-row on the board, indicating a completed game.
    """
    winning_positions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for pos in winning_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] != " ":
            return True
    return False

def generate_boards():
    """
    Generate unique intermediate Tic-Tac-Toe board configurations where it's O's turn.
    """
    unique_boards = set()
    for x_count in range(1, 5):  # We only need up to 5 moves by X for intermediate states
        o_count = x_count - 1
        # Generate a base board with x_count X's, o_count O's, and the remaining as spaces
        base_board = "X" * x_count + "O" * o_count + " " * (9 - x_count - o_count)
        
        # Generate permutations and filter out invalid or duplicate configurations
        for perm in set(permutations(base_board)):
            board = list(perm)
            
            # Exclude configurations where the game is already won
            if not check_win(board):
                # Normalize to avoid duplicates due to rotation/reflection symmetry
                normalized = normalize(board)
                unique_boards.add(normalized)
                    
    # Convert the unique normalized strings back to 2D board lists for display
    return [list(board) for board in unique_boards]

# Run the function and display the results
unique_tic_tac_toe_boards = generate_boards()
print(f"Number of unique intermediate boards: {len(unique_tic_tac_toe_boards)}")

all_boards_dict = dict((i, []) for i in range(1, 5))

for board in unique_tic_tac_toe_boards:
    move_num = sum(' ' == cell for row in board for cell in row)
    if move_num == 8:
        all_boards_dict[1].append(board)
    elif move_num == 6:
        all_boards_dict[2].append(board)
    elif move_num == 4:
        all_boards_dict[3].append(board)
    elif move_num == 2:
        all_boards_dict[4].append(board)


# for b in all_boards[4]:
#     print(b[:3])
#     print(b[3:6])
#     print(b[6:])
#     print('-----------------')


# for i in range(1, 5):
#     print(f"Number of unique intermediate boards after {i} move(s): {len(all_boards[i])}")


all_boards_list = []
for i in range(1, 5):
    for board in all_boards_dict[i]:
        all_boards_list.append(''.join(board))

import pickle
with open('all_boards.pkl', 'wb') as f:
    pickle.dump(all_boards_list, f)
