from dlx import DancingLinks
import pickle
import numpy as np
import itertools


with open('mini_dict.pickle', 'rb') as f:
    main_dict = pickle.load(f)


def create_matrix(piece_numbers, date):
    dancing_links_matrix = []
    for shift, piece_number in enumerate(piece_numbers):
        for cells_filled in my_dict[piece_number]:

            # 31 columns for the 31 dates and one hot encoding for the piece number
            new_row = [0 for _ in range(31 + len(piece_numbers))]

            for cell in cells_filled:
                new_row[cell - 1] = 1

            new_row[31 + shift] = 1
            dancing_links_matrix.append(new_row)


    dancing_links_matrix = np.array(dancing_links_matrix)

    # Remove columns with all zeros which are holes
    dancing_links_matrix = np.delete(dancing_links_matrix, date - 1, axis=1)

    return dancing_links_matrix


def main(piece_numbers, date, multi_solution_flag=False):
    dancing_links_matrix = create_matrix(piece_numbers, date)
    dl = DancingLinks(dancing_links_matrix)

    if multi_solution_flag:
        dl.search(multi_solution_flag=True)
        # return dl.no_of_solutions

        for solution in dl.all_solutions:
            for mtx_ind, piece_number in zip(solution, piece_numbers):
                print(f'\nPiece number = {piece_number} ---', end = ' ')
                for ind, cell in enumerate(dancing_links_matrix[mtx_ind][:30]):
                    if cell == 1:
                        if ind < date - 1:
                            print(ind + 1, end=' ')
                        else:
                            print(ind + 2, end=' ')
            print('\n')
        return


    solution = dl.solve()

    # Show the solution
    if solution:
        for mtx_ind, piece_number in zip(solution, piece_numbers):
            print(f'\nPiece number = {piece_number} ---', end=' ')
            for ind, cell in enumerate(dancing_links_matrix[mtx_ind][:30]):
                if cell == 1:
                    if ind < date - 1:
                        print(ind + 1, end=' ')
                    else:
                        print(ind + 2, end=' ')
        print()
        return True
    else:
        # print('No solution')
        return False



my_date = 31
my_dict = main_dict[my_date]


# Using only 6 / 8 pentominos
# for date in range(1, 32):
#     print(f'\nDate = {date}')
#     my_date = date
#     my_dict = main_dict[my_date]

#     for combination in itertools.combinations(range(8), 6):
#         main(combination, my_date, multi_solution_flag=False)

    # print(f'Solution count for date {my_date} = {no_of_solutions}')
    

# Using 4 / 8 pentominos; 1 / 1 hexomino; 1 / 3 tetromino
# solution_count = 0
# for combination1 in itertools.combinations(range(8), 4):
#     for combination2 in [8, 9, 10]:
#         combination = combination1 + (combination2,) + (11,)
#         print(combination)
#         solution_count += main(combination, my_date)
#         print('\n')
# print(f'Solution count for date {my_date} = {solution_count}')
