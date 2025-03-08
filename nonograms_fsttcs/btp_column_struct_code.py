from itertools import product

def check_row_sums(matrix, row_sums):
    n = len(matrix)
    calculated_row_sums = [sum(matrix[i]) for i in range(n)]
    return calculated_row_sums == row_sums

def brute_force_fit_all_solutions(n, m, column_blocks, row_sums):
    matrix = [[0] * m for _ in range(n)]
    solutions = []
    column_placements = []
    for block in column_blocks:
        block_len = len(block)
        valid_placements = []
        for start_row in range(n - block_len + 1):
            placement = [0] * n
            for i in range(block_len):
                placement[start_row + i] = int(block[i])
            valid_placements.append(placement)
        column_placements.append(valid_placements)

    for combination in product(*column_placements):
        matrix = [[0] * m for _ in range(n)]

        for col_idx in range(m):
            for row_idx in range(n):
                matrix[row_idx][col_idx] = combination[col_idx][row_idx]

        if check_row_sums(matrix, row_sums):
            solutions.append([row[:] for row in matrix])

    if solutions:
        print(f"{len(solutions)} solution(s) found:")
        for sol_num, solution in enumerate(solutions, 1):
            print(f"\nSolution {sol_num}:")
            for row in solution:
                print(row)
    else:
        print("No solution found.")
    return solutions


# Example usage
n = 4  # Number of rows
m = 3  # Number of columns

# Binary strings representing the blocks for each column
column_blocks = [
    "101",  # Block for column 1
    "01",   # Block for column 2
    "10",   # Block for column 3
]

# Row sums (the target sum for each row)
row_sums = [1, 2, 1, 1]

brute_force_fit_all_solutions(n, m, column_blocks, row_sums)
