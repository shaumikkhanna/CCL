import numpy as np
import matplotlib.pyplot as plt


import numpy as np

# Define the knight's possible moves
knight_moves = [
    (-2, -1), (-2, 1), (2, -1), (2, 1),
    (-1, -2), (-1, 2), (1, -2), (1, 2)
]

# Warnsdorff's heuristic: find the number of valid onward moves for a given cell
def count_onward_moves(x, y, board, visited):
    count = 0
    for dx, dy in knight_moves:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < board.shape[0] and 0 <= new_y < board.shape[1] and board[new_x, new_y] == 1 and not visited[new_x, new_y]:
            count += 1
    return count

# Backtracking function to find the knight's tour
def knights_tour(x, y, board, visited, move_count, path):
    # If we have visited all land cells, return True
    if move_count == np.sum(board):
        return True

    # List of possible knight moves
    possible_moves = []
    
    for dx, dy in knight_moves:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < board.shape[0] and 0 <= new_y < board.shape[1] and board[new_x, new_y] == 1 and not visited[new_x, new_y]:
            # Count onward moves from each potential next move (Warnsdorff's heuristic)
            onward_moves_count = count_onward_moves(new_x, new_y, board, visited)
            possible_moves.append((onward_moves_count, new_x, new_y))
    
    # Sort moves by the number of onward moves (ascending order)
    possible_moves.sort()

    # Try each move from the sorted list
    for _, new_x, new_y in possible_moves:
        visited[new_x, new_y] = True
        path.append((new_x, new_y))

        # Recursively attempt to complete the tour
        if knights_tour(new_x, new_y, board, visited, move_count + 1, path):
            return True

        # Backtrack: undo the move
        visited[new_x, new_y] = False
        path.pop()

    return False

# Main function to solve the knight's tour on land cells
def solve_knights_tour(board):

    # Find the first land cell to start the knight's tour
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j]:
                # Start the knight's tour from this land cell
                visited = np.zeros_like(board, dtype=bool)
                visited[i, j] = True
                path = [(i, j)]
                
                if knights_tour(i, j, board, visited, 1, path):
                    return path

    return None  # No valid tour found


def generate_gaussian(size=8):
    # Generate coordinates for each point in the grid
    scalar = 0.25
    x, y = np.meshgrid(np.linspace(-scalar, scalar, size), np.linspace(-scalar, scalar, size))
    # Define the mean (center of the grid)
    mean = [0, 0]
    # Define the covariance matrix (to control the spread of the distribution)
    covariance = [[0.001, 0], [0, 0.001]]
    # Generate the 2D Gaussian values
    pos = np.dstack((x, y))
    rv = np.random.multivariate_normal(mean, covariance, size=size**2)
    # Calculate the probability density function (pdf) values
    gaussian_values = np.exp(-0.5 * (x**2 + y**2) / 0.1) - 0.1
    return gaussian_values


def create_land(grid):
    # Generate the land grid
    land = np.zeros(grid.shape, dtype=int)
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r][c] > np.random.rand():
                land[r][c] = 1

    return land


def plot_2d_array(array):
    plt.imshow(array, cmap='viridis', interpolation='nearest')
    plt.colorbar(label='Value')
    plt.title('2D Array Grid Visualization')
    plt.show()


g = generate_gaussian()
# plot_2d_array(g)
land = create_land(g)
print(land)
print(f'Number of land squares = {land.sum()}; Ratio = {land.sum() / land.size}')

# Solve the knight's tour
solution = solve_knights_tour(land)
print(solution)
